# 5.5eSheets

This project rebuilds the hornbook1776 D&D 5e character sheets (`Master.pdf`, 34
pages) as a web page. Instead of a heavy PDF, the layout is HTML and CSS, so it
matches the original but the look and fields are easy to change. All eleven
classes from `Master.pdf` are ported: Barbarian, Bard, Cleric, Druid, Fighter,
Monk, Paladin, Rogue, Sorcerer, Warlock, and Wizard. New classes now come from
other books or from homebrew rather than from `Master.pdf`.

Each sheet is built by hand from normal-flow `div` and `span` elements with CSS
borders. Every area uses `div`/`span` for structure, CSS `border`s for the box
lines, and `padding`/`margin`/`gap` for spacing. The section tint shows through
the gaps.

## Run it

Open `index.html` in a browser. It works over `file://`, so no server is needed.
The width is fixed at 594px, there is no scaling, and it prints cleanly. A
screen-only class picker (`<select id="classpick">`) shows one `.sheet` at a
time. The JavaScript stays small: the picker, plus a `<sheet-section>` helper
that clones shared markup. Emblems like the axe and the AC shield are dashed
`.emblem` placeholders, not images.

## Files

| File | Role |
|------|------|
| `index.html` | Markup only, plus the `#classpick` picker. Links `style.css` and then `sheet.css` (order matters); there is no inline `<style>`. One `.sheet` per class. |
| `style.css` | The shared component library: reusable box-model primitives like `.section`, `.box`, `.lbl`, and `.lined`. Edit once and every section updates. Linked first. |
| `sheet.css` | The per-sheet styles: section palettes (`.sec-* { --panel/--tab }`) and per-section layout, namespaced under `.sec-NAME`. Linked after `style.css`. Grouped one class panel at a time; search a class banner like `PALADIN SHEET` to find its block. |
| `Master.pdf` | The original PDF. Kept as a layout and style reference. |
| `tools/` | `pngdiff.py` for screenshot diffing (see "Verify a change"). |

## Design

The page holds one `<div class="sheet" data-class="…">` per class, and each one
is a single column of `.section` panels. A class sheet runs Character, the class
panel, Vitals, Gear, Skills, then Money, Equipment, Attuned, Feats, and
Background. Spellcasters also get Cantrips and Spells Known. New classes go at the
bottom of the `.page` and get an `<option>` in the picker.

**Three layers** (each file is commented with these headings):

1. Component library (`style.css`): reusable primitives that every section
   shares. Edit one here and it changes everywhere.
   - `.page`: the 594px stacked column.
   - `.section`: a titled panel with a rotated `.tab` and a `.body`. The interior
     tint comes from `--panel`, and the tab-strip color comes from `--tab`
     (page-2 panels are white with only the tab colored).
   - `.box`: the standard white field with an ink border and a corner `.lbl`
     (modifiers `.lbl.big`, `.right`, `.center`).
   - `.cbx` (checkbox square), `.ring` (proficiency/advantage circle), `.emblem`
     (art placeholder), and `.lined`/`.ln` (ruled write-in rows, like Attuned and
     Feats and the custom-equipment columns).
2. Section palettes (`sheet.css`): one line per section. `.sec-NAME { --panel }`
   for page-1 tints, or `.sec-NAME { --tab; border }` for page-2. Colors are
   sampled from `Master.pdf` by rendering a page with `pdftoppm` and reading
   pixels.
3. Section content (`sheet.css`): per-section layout. Every selector is
   namespaced under `.sec-NAME` so sections can't interfere with each other.

**One thing to watch.** Structure belongs in the markup and CSS only themes. And
CSS `/* */` comments do not nest. Nesting them was an earlier bug that blanked the
whole page.

## Adding a class

Every `Master.pdf` class is ported already. To add a new one from another book or
from homebrew, build its sheet the same way and follow the same steps. Put the
class's markup at the bottom of the `.page` in `index.html` and its styles at the
bottom of `sheet.css`. If you are transcribing from a PDF source, `pdftotext
-bbox -f N -l N source.pdf tools/work/pN.bbox.xml` pulls exact text and
coordinates (`tools/work/` is gitignored). For each block, the main question is
whether it is single-use or common:

- Single-use class panel (like `Barbarian`): specific to one class. Scope its
  palette and layout CSS to `.sec-<class>` at the bottom of `sheet.css` behind a
  class banner, and put its markup at the bottom of `.page`.
- New common component (like `Cantrips` or `Spells Known`, which every
  spellcaster shares): put its reusable CSS in `style.css` next to the other
  primitives, with a documented class and markup contract, so later classes reuse
  it. Tint it per class through the existing `--panel` and `--tab` tokens instead
  of hard-coded colors.
- Reused shared sections (Character, Vitals, Gear, Skills, the page-2 blocks):
  copy the existing markup. Their `.sec-*` CSS is already there and applies to
  every instance.

Rule of thumb: a block that shows up on one class sheet is single-use (CSS in
`sheet.css`, under `.sec-NAME`), and a block that shows up on several is a common
component (CSS in `style.css`). Try to compose the existing primitives (`.box`,
`.lined`, `.cbx`, …) before adding new ones.

## Pre-printed spell lists (the `.cs-list` component)

Some class panels reproduce the class's full pre-printed spell list from
`Master.pdf` (for example the Cleric's "Cleric Spells" box on page 8). That is
different from the blank Spells Known table, which is a caster's own write-in
`.sp-row`s. The list is single-use for now, scoped under `.sec-cleric-spells` in
`sheet.css`. Promote its CSS to `style.css` once a second class reuses the same
shape.

**Structure.** `.cs-list` (bordered box) holds one `.cs-lvl` band per spell level
(a big `.cs-num` down the left, plus a `.cs-cols` CSS grid of 4 `.cs-col`), then a
`.cs-legend` footer. One spell is a `.cs-spell` holding `[.cbx][.cs-tag]` and a
`.cs-name`. The `.cbx` and `.cs-tag` boxes stretch the full row height (the parent
is `align-items:stretch` and the boxes are `height:auto`), the same look as the
equipment `.qty` boxes. Don't give them fixed heights.

**Layout rules.**
- Spells flow alphabetically top-to-bottom, then left-to-right across the 4
  columns. Balance the columns roughly evenly. The remainder spills into column 4,
  which then gets `.cs-line` write-in rows (blank ruled lines for the class's
  Domain or subclass spells) filling the rest of its height.
- `.cs-tag` is the casting-time abbreviation, matching the `.cs-legend` footer:
  `A` Action, `BA` Bonus Action, `R` Reaction, `RT` Ritual, `T` Time to cast
  (longer than an action), `Z` Always Prepped. Center the tag text.

**Editing a band.** The formatted markup is line-wrapped and hard to
string-match, so rebuild the bands with a script instead of hand-editing spans.
Use a throwaway Python script in the scratchpad that rebuilds the markup from a
per-level `[col1..col4]` spell table and splices it between the `<!-- Level 1 -->`
and `<!-- casting-abbreviation legend -->` anchors (leave the legend intact). Back
up `index.html` first, and verify the spell count afterward.

**Content source.** The base list was transcribed from `Master.pdf` (2014 PHB)
with `pdftotext -bbox`. Keep the sheet's exact text unless you are asked to update
it. To convert a list to 2024 rules (5.5e), the base class list gains about a
dozen spells (mostly Xanathar's and Tasha's folded in, plus a few new ones) and
drops none. Verify against an authoritative source, and note that D&D Beyond's
class spell page lists homebrew too, so filter it out. Per-subclass Domain spells
are separate (the sheet only has blank `.cs-line` write-in rows for them), so
don't fold domain-list changes into the printed base list.

## Verify a change

`tools/pngdiff.py a.png b.png` reports the mean and max pixel difference between
two screenshots, which confirms whether a render still matches. Screenshot the
sheet with headless Chrome at a tall window (it's one long page), for example
`--window-size=700,2100`, and compare a section crop against the same area
rendered from `Master.pdf` with `pdftoppm`:

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --screenshot=out.png --window-size=700,2100 "file://$PWD/index.html"
```
