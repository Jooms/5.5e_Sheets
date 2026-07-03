---
description: Retake the README screenshots and scan the repo for features the README doesn't mention yet
---

Refresh the project README. Two jobs: regenerate the screenshots, then find
anything about the project that has changed since the README was last written and
tell the user how to bring it up to date. Read `CLAUDE.md` first for the
project's architecture.

Do NOT rewrite the whole README on your own. Report what needs updating, suggest
the exact edits, and apply them once the user agrees. Keep the README's voice: no
em-dashes, around a 10th-grade reading level, mildly upbeat but not hyped.

## Phase 1 — Regenerate the screenshots

Run the committed tool:

```sh
python3 tools/shots.py            # all six, into docs/screenshots/
python3 tools/shots.py hero       # or just one, by output stem
```

How it works (so you can fix it if a sheet changed): it copies `index.html` into
a throwaway `shot.html`, injects a screenshot-only `@media print` override that
hides the picker/footer and paints a solid `#E0E5C1` backdrop, prints each class
to PDF with headless Chrome, rasterizes the page with `pdftoppm`, then crops
tight to the sheet and re-pads an even `#E0E5C1` border. The backdrop lives only
in the temp copy, so the committed CSS is untouched and a real Ctrl-P print stays
background-free. **Never** move that backdrop into `style.css`/`sheet.css`;
`print-color-adjust: exact` would then bleed into everyone's printout.

Needs Google Chrome and `pdftoppm` (poppler) on the machine. The Chrome path
defaults to the macOS location; override with `CHROME=... python3 tools/shots.py`.

Then verify:

- `Read` each image in `docs/screenshots/`. Confirm it is crisp, shows the right
  class and page, has an even `#E0E5C1` border on all sides, and nothing is
  clipped. The script prints each file's size; every corner should already be
  `#E0E5C1`.
- The shot list lives in the `SHOTS` table at the top of `tools/shots.py`:
  `(class, pdf page, output file, dpi, border)`. `hero.png` is Cleric page 1 and
  `spell-list.png` is Cleric page 3. If a sheet's pagination changed (for example
  a class that used to print on 3 pages now prints on 2), the page numbers in
  `SHOTS` may point at the wrong page. Fix the table, rerun, and re-verify.
- If you feature a newly added or newly migrated class, update `SHOTS` and the
  README's gallery together. Prefer migrated (2024) sheets for the hero; their
  class tab reads plain (for example "Cleric"), while un-migrated ones still read
  "(old)".

Stage the regenerated images with `git add docs/screenshots` (they are Git LFS
objects). Leave the commit to the user unless they ask you to commit.

## Phase 2 — Scan for features the README misses

Compare what the README claims against the real project, and list every gap.
Check at least these:

- **Class count and list.** The README says "Eleven classes", lists all eleven
  by name, and carries a `classes-11` badge. Count the `<option>`s in
  `#classpick` and the `<div class="sheet" data-class="...">` blocks in
  `index.html`. If the count changed, the number, the prose list, and the badge
  URL (`.../classes-N-orange`) all need updating.
- **New sections or shared components.** Look at the `<template>` elements near
  the bottom of `index.html` and the `<!-- ===== ... ===== -->` banners. The
  README names the shared sections (Character, Vitals, Gear, Skills, the page-2
  blocks, Cantrips, Spells Known) and the printed spell list. A new shared panel
  should be mentioned, and a big new one may deserve its own screenshot.
- **New user-facing behavior.** Search the picker script and markup for anything
  beyond `?class=` (new query params, new controls, print changes, new
  attribution snippets, the funding/sponsor button in `.github/FUNDING.yml`).
- **New files or dirs.** `ls` the repo and compare against the "Project layout"
  table. New tools (like `tools/shots.py`), docs, or top-level files that a
  reader should know about belong there. Note that `tools/shots.py` itself is new
  and is not in the table yet.
- **License or attribution changes.** Confirm the `LICENSE`, the CC BY-NC 4.0
  badge, and both attribution snippets still match reality.

Useful commands:

```sh
grep -n 'data-class=' index.html | wc -l          # sheet count
grep -oE '<option value="[a-z]+"' index.html      # picker classes
grep -n 'name="' index.html | grep template       # shared <template>s
ls -1 && ls -1 tools .github                       # files vs. the layout table
```

## Wrap up

Report:

1. Which screenshots you regenerated, and anything you had to change in `SHOTS`.
2. A checklist of README gaps you found, each with the section to edit and
   suggested wording (matching the README's plain, mildly upbeat voice).
3. Offer to apply the edits. If the user says go, make them and re-stage.
