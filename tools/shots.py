#!/usr/bin/env python3
"""Regenerate the README screenshots in docs/screenshots/.

Pipeline, per shot:
  1. Build a throwaway shot.html: a copy of index.html with a screenshot-only
     print override that hides the picker/footer and paints a solid #E0E5C1
     backdrop. This lives only in a temp dir, so the committed source is never
     touched and a real Ctrl-P print stays background-free.
  2. Print the class to PDF with headless Chrome (--print-to-pdf).
  3. Rasterize the wanted page with pdftoppm.
  4. Crop tight to the sheet, then re-pad an even #E0E5C1 border.

Stdlib only (matches pngdiff.py). Shells out to Google Chrome and pdftoppm.
Chrome path defaults to the macOS location; override with the CHROME env var.

    python3 tools/shots.py            # regenerate every shot
    python3 tools/shots.py hero       # regenerate one (by output name stem)
"""
import os, sys, glob, struct, zlib, subprocess, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "screenshots"
CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
BG = (0xE0, 0xE5, 0xC1)  # screenshot backdrop; keep in sync with the README ask

# (class, pdf page, output file, render dpi, border px)
SHOTS = [
    ("cleric",    1, "hero.png",       200, 48),  # page 1: Character..Skills
    ("cleric",    3, "spell-list.png", 200, 48),  # page 3: Cantrips + spell list
    ("paladin",   1, "paladin.png",     96, 32),  # gallery thumbnails (page 1)
    ("wizard",    1, "wizard.png",      96, 32),
    ("barbarian", 1, "barbarian.png",   96, 32),
    ("rogue",     1, "rogue.png",       96, 32),
]

OVERRIDE = """  <style id="shot-override">
    @media print {
      .picker, .print-footer { display: none !important; }
      html, body {
        background: #E0E5C1 !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }
      @page { margin: 0; }
      body { padding: 20px; }
    }
  </style>
</head>"""


def build_shot_html(tmp):
    src = (ROOT / "index.html").read_text()
    src = src.replace('href="style.css"', f'href="file://{ROOT}/style.css"')
    src = src.replace('href="sheet.css"', f'href="file://{ROOT}/sheet.css"')
    src = src.replace("</head>", OVERRIDE, 1)
    path = pathlib.Path(tmp) / "shot.html"
    path.write_text(src)
    return path


def to_pdf(shot_html, cls, tmp):
    pdf = pathlib.Path(tmp) / f"{cls}.pdf"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", f"file://{shot_html}?class={cls}"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return pdf


def rasterize(pdf, page, dpi, tmp):
    prefix = pathlib.Path(tmp) / f"{pdf.stem}_p{page}"
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-f", str(page), "-l",
                    str(page), str(pdf), str(prefix)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    hits = glob.glob(f"{prefix}*.png")
    if not hits:
        raise SystemExit(f"pdftoppm produced no page {page} for {pdf}")
    return hits[0]


# --- pure-python PNG read / crop-and-pad / write (RGB) ----------------------

def read_png(path):
    d = open(path, "rb").read(); i = 8; idat = b""; ct = 6
    while i < len(d):
        ln = struct.unpack(">I", d[i:i+4])[0]; typ = d[i+4:i+8]; data = d[i+8:i+8+ln]
        if typ == b"IHDR": w, h, _, ct = struct.unpack(">IIBB", data[:10])
        elif typ == b"IDAT": idat += data
        elif typ == b"IEND": break
        i += 12 + ln
    raw = zlib.decompress(idat); ch = {0:1,2:3,3:1,4:2,6:4}[ct]; stride = w*ch
    out = bytearray(); prev = bytearray(stride); p = 0
    for _ in range(h):
        f = raw[p]; p += 1; line = bytearray(raw[p:p+stride]); p += stride
        for x in range(stride):
            a = line[x-ch] if x >= ch else 0; b = prev[x]; c = prev[x-ch] if x >= ch else 0
            if f == 1: line[x] = (line[x]+a) & 255
            elif f == 2: line[x] = (line[x]+b) & 255
            elif f == 3: line[x] = (line[x]+((a+b) >> 1)) & 255
            elif f == 4:
                pp = a+b-c; pa = abs(pp-a); pb = abs(pp-b); pc = abs(pp-c)
                line[x] = (line[x]+(a if (pa <= pb and pa <= pc) else (b if pb <= pc else c))) & 255
        out += line; prev = line
    return w, h, ch, bytes(out)


def write_rgb(path, w, h, px):
    raw = bytearray()
    for y in range(h):
        raw.append(0); raw += px[y*w*3:(y+1)*w*3]
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t+d) & 0xffffffff)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        f.write(chunk(b"IEND", b""))


def frame(inp, outp, pad):
    """Crop tight to non-background content, then pad an even border in bg."""
    w, h, ch, px = read_png(inp)
    def rgb(o): return (px[o], px[o+1], px[o+2]) if ch >= 3 else (px[o],)*3
    bg = rgb(0)
    minx, miny, maxx, maxy = w, h, 0, 0
    for y in range(h):
        row = y*w*ch
        for x in range(w):
            if rgb(row+x*ch) != bg:
                minx = min(minx, x); maxx = max(maxx, x)
                miny = min(miny, y); maxy = max(maxy, y)
    if maxx < minx:  # blank page guard
        raise SystemExit(f"{inp}: no content found")
    cw, chh = maxx-minx+1, maxy-miny+1
    ow, oh = cw+2*pad, chh+2*pad
    out = bytearray(bytes(BG)*(ow*oh))
    for y in range(chh):
        for x in range(cw):
            o = ((y+pad)*ow + (x+pad))*3; s = (miny+y)*w*ch + (minx+x)*ch
            out[o], out[o+1], out[o+2] = rgb(s)
    write_rgb(outp, ow, oh, bytes(out))
    return ow, oh


def main():
    only = set(sys.argv[1:])  # optional output stems, e.g. "hero" "wizard"
    shots = [s for s in SHOTS if not only or s[2].removesuffix(".png") in only]
    if only and not shots:
        raise SystemExit(f"no shot matches {only}; known: "
                         + ", ".join(s[2].removesuffix('.png') for s in SHOTS))
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        shot_html = build_shot_html(tmp)
        pdfs = {}
        for cls, page, name, dpi, pad in shots:
            if cls not in pdfs:
                pdfs[cls] = to_pdf(shot_html, cls, tmp)
            raw_png = rasterize(pdfs[cls], page, dpi, tmp)
            ow, oh = frame(raw_png, OUT / name, pad)
            print(f"  {name:16} {cls} p{page} @ {dpi}dpi -> {ow}x{oh}")
    print(f"wrote {len(shots)} image(s) to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
