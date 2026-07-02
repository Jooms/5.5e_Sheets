---
description: Migrate a class sheet from 2014 to 2024 (5.5e) rules, then verify it prints on 3 pages
argument-hint: <class> (e.g. wizard)
---

Migrate the **$1** class sheet from 2014 rules to 2024 (5.5e) rules, mirroring the
Cleric and Paladin migrations already in the repo. Work through the phases below
in order. Read `CLAUDE.md` first for the project's architecture and conventions —
they override anything here.

The class to migrate this run is: **$ARGUMENTS**

## Phase 1 — Gap analysis (do this first, before editing)

Compare the current `$1` sheet against the 2024 PHB and report what's missing or
changed, then get the go-ahead before editing (the user usually says "make the
changes, I'll tweak formatting after").

- Find the class's markup (`<div class="sheet" data-class="$1">`) in `index.html`
  and its panel CSS (`.sec-$1` in `sheet.css`).
- Look at the live 2014 reference if useful: `https://jooms.github.io/5.5e_Sheets/?class=$1`.
- Enumerate the 2024 changes: renamed/replaced features, new level-1 features
  (e.g. Weapon Mastery), features that became Channel Divinity options or spells,
  new counters/charges, Epic Boon, and for casters the spell-list deltas.
- Verify class rules against an authoritative 2024 source. When fetching a wiki
  page redirect-loops (https↔http), use `curl` via Bash and parse the HTML with
  Python instead of WebFetch. D&D Beyond's class spell page lists homebrew too —
  filter it out and confirm official counts.

## Phase 2 — Rewrite the class panel

- Panel markup goes in the `data-class="$1"` sheet; panel palette + layout CSS is
  single-use, scoped under `.sec-$1` at the bottom of that class's block in
  `sheet.css`. Structure lives in markup; CSS only themes.
- Compose existing primitives (`.box`, `.lbl`, `.cbx`, `.ring`, `.lined`) before
  adding new ones. Match the Cleric/Paladin panels for idiom (corner `.lbl` labels
  like "Level" top-left, charge circles like `③②①`, checkbox feature lists).

## Phase 3 — Spell list (casters only)

If `$1` is a spellcaster, replace the blank write-in table with a pre-printed
`.cs-list` (see the "Pre-printed spell lists" section of `CLAUDE.md`):

- Scope its CSS under `.sec-$1-spells` in `sheet.css`, mirroring `.sec-cleric-spells`
  / `.sec-paladin-spells`. Tint via `--panel` / `--tab`, not hard-coded colors.
- **Rebuild the level bands with a throwaway Python generator** in the scratchpad
  (don't hand-edit the wrapped spans). Model it on
  `scratchpad/gen_paladin_spells.py`: a per-level `[col1..col4]` spell table with
  casting-time tags, alphabetical top-to-bottom then left-to-right, remainder +
  write-in `.cs-line` rows in column 4, spliced between the section's start
  comment and the sheet's closing tag. Back up `index.html` first and verify the
  spell count afterward.
- Casting tags are class-specific and RAW: `A` Action, `BA` Bonus Action, `R`
  Reaction, `RT` Ritual, `T` Time to cast. For a spell this class can cast as
  **either an Action or a Ritual**, use the stacked dual tag (`A` over `RT`, soft-grey
  dotted divider). Don't apply the dual tag to anything else. No "Always Prepared" tag.

## Phase 4 — Presentation pass

Iterate on layout from screenshots. Screenshot with headless Chrome at a tall
window and view the crop:

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --screenshot=out.png --window-size=950,3600 --force-device-scale-factor=2 \
  --hide-scrollbars "file://$PWD/index.html?class=$1"
```

No PIL/imagemagick here — use `scratchpad/pngcrop.py` (`pngcrop.py in out x y w h`)
to crop, and `tools/pngdiff.py a.png b.png` to diff against a `Master.pdf` render.
Apply the user's formatting tweaks as they come.

## Phase 5 — Verify it prints on 3 pages (required)

The print model (see the `@media print` block in `sheet.css`): **page 1** =
Character…Skills, **page 2** = Money…Background, **page 3** = Cantrips/Spells, at
`zoom: 1.10`. A taller 2024 panel can push Skills onto a blank 4th page.

Render to PDF and count pages — must be **3** (or 2 for a non-caster):

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=out.pdf "file://$PWD/index.html?class=$1"
python3 -c "import re;d=open('out.pdf','rb').read();print('pages:',len(re.findall(rb'/Type\s*/Page[^s]',d)))"
```

If it's 4 pages, page 1 is overflowing. Render pages with `pdftoppm -png -r 90
out.pdf pp` and view them to confirm where it spills, then **trim the class panel's
row heights** (not the shared sections) — e.g. shrink the Oath/features full-width
row's `min-height`, reduce a tall box's `padding-top`, or tighten a split row.
Re-render and re-count until it's 3 pages, then screenshot page 1 to confirm the
last Skills rows and both Skill Feature boxes still fit with margin, and page 3 to
confirm the spell list isn't clipped.

## Wrap up

Report: the 2024 changes applied, the spell count (if a caster), the final page
count, and any panel heights you trimmed to make it fit.
