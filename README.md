<h1 align="center">5.5eSheets</h1>

<p align="center">
  <b>Print-ready D&D 5e character sheets, built as a plain web page instead of a PDF.</b>
</p>

<p align="center">
  <a href="https://jooms.github.io/5.5e_Sheets/"><img alt="Live demo" src="https://img.shields.io/badge/live%20demo-online-brightgreen"></a>
  <img alt="Built with HTML &amp; CSS" src="https://img.shields.io/badge/built%20with-HTML%20%26%20CSS-e34c26">
  <img alt="Zero dependencies" src="https://img.shields.io/badge/dependencies-none-success">
  <img alt="11 classes" src="https://img.shields.io/badge/classes-11-orange">
  <a href="LICENSE"><img alt="License: CC BY-NC 4.0" src="https://img.shields.io/badge/license-CC%20BY--NC%204.0-blue"></a>
</p>

<p align="center">
  <a href="https://jooms.github.io/5.5e_Sheets/">
    <img src="docs/screenshots/hero.png" alt="A Cleric character sheet: Character, Cleric, Vitals, Gear, and Skills sections" width="620">
  </a>
</p>

<p align="center"><i>The Cleric sheet, page one. Every box and line is plain <code>div</code>/<code>span</code> with CSS borders.</i></p>

This project rebuilds the hornbook1776 D&D 5e character sheets (`Master.pdf`, 34
pages) as HTML and CSS. A PDF is heavy and hard to change. This page keeps a
layout close to the original, but you can restyle it or swap out fields whenever
you like. Every sheet is drawn by hand from plain `div` and `span` elements with
CSS borders. **No canvas, no images, no framework.**

## Try it

- **Live page:** **<https://jooms.github.io/5.5e_Sheets/>**
- **On your computer:** open `index.html` in any browser. It runs straight from
  the file system, so there is no server to start and nothing to install.
- Use the picker in the top-left corner (screen only) to switch class. You can
  also link straight to one with `index.html?class=cleric`.
- The page is a fixed 594px wide and prints cleanly onto letter paper.

## Classes

Eleven classes are ready to go. Each one is a single scrolling column of titled
sections. The section colors come from the original PDF, and spellcasters get
two extra panels for Cantrips and Spells Known.

<p align="center">
  <img src="docs/screenshots/paladin.png"   alt="Paladin sheet"   width="185">
  <img src="docs/screenshots/wizard.png"    alt="Wizard sheet"    width="185">
  <img src="docs/screenshots/barbarian.png" alt="Barbarian sheet" width="185">
  <img src="docs/screenshots/rogue.png"     alt="Rogue sheet"     width="185">
</p>
<p align="center"><i>Paladin, Wizard, Barbarian, and Rogue. Same frame, a different class panel on each.</i></p>

The full set: Barbarian, Bard, Cleric, Druid, Fighter, Monk, Paladin, Rogue,
Sorcerer, Warlock, and Wizard.

### Printed spell lists

Caster sheets can print the whole class spell list right on the page. You tick a
box instead of writing every spell out by hand. Here is the Cleric's:

<p align="center">
  <img src="docs/screenshots/spell-list.png" alt="The Cleric's printed spell list and blank Cantrips grid" width="600">
</p>

## Why it works this way

- **Easy to change.** The layout, the styling, and every field live in the
  markup and the stylesheets. It is easy to read and easy to edit.
- **Almost no JavaScript.** The only scripts are the class picker and a small
  `<sheet-section>` helper that copies shared markup into place. No framework, no
  bundler.
- **Prints cleanly.** The width is locked at 594px and tuned to land on letter
  pages.
- **HTML and CSS first.** If a thing can be done in HTML or CSS, it is done
  there. That rule is a fun challenge, and it keeps the whole project easy to
  poke at.

## Use it on your site

You are welcome to drop these sheets into your own site. If you do, the license
(below) asks for one thing back: a visible credit that links to the project.
Pick one of the snippets below and paste it near the sheets. Both bring their own
styles inline, and the GitHub logo is an inline SVG, so there is nothing extra to
load.

A GitHub-style button:

```html
<!-- 5.5eSheets attribution -->
<a href="https://github.com/Jooms/5.5e_Sheets"
   style="display:inline-flex;align-items:center;gap:8px;padding:6px 14px;
          font:600 14px/1.4 -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
          color:#fff;background:#24292f;border:1px solid rgba(27,31,36,.15);
          border-radius:6px;text-decoration:none;">
  <svg height="16" width="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
             0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
             -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66
             .07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15
             -.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0
             1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82
             1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01
             1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8Z"></path>
  </svg>
  Built with 5.5eSheets
</a>
```

Or a plain text link, if that fits your page better:

```html
<!-- 5.5eSheets attribution -->
Character sheets by
<a href="https://github.com/Jooms/5.5e_Sheets"
   style="color:#0969da;text-decoration:none;border-bottom:1px solid currentColor;">5.5eSheets</a>
```

## Contributing

The sheets are built from three layers. Each layer is documented in the file it
lives in.

1. **Primitives** (`style.css`): the reusable box-model pieces every sheet
   shares, like `.section`, `.box`, `.lbl`, `.cbx`, `.ring`, and `.lined`. Change
   one here and every sheet updates. Linked first.
2. **Palettes** (`sheet.css`): one tint line per section, with colors sampled
   from `Master.pdf`.
3. **Layout** (`sheet.css`): per-section positioning. Every rule is namespaced
   under a `.sec-NAME` so classes cannot step on each other.

Structure lives in the markup, and CSS only handles theme and positioning. Watch
out for one thing: CSS `/* */` comments do not nest. Nest one by accident and the
whole page goes blank.

### Where do I edit for X?

| Want to change… | Edit |
|---|---|
| How a box, checkbox, or label looks *everywhere* | `style.css` |
| One class's panel | its banner in `sheet.css` (styles) plus its `<!-- ===== CLASS SHEET ===== -->` banner in `index.html` (markup) |
| A section every class shares (Character, Vitals, Gear, Skills, page-2 blocks, Cantrips, Spells Known) | the shared `<template>` near the bottom of `index.html`, plus the matching `.sec-*` block in `sheet.css` |

### Add a class

Every `Master.pdf` class is already ported. To add a new one from another
sourcebook or a homebrew, build its sheet the same way the others are built:

1. Work out the sheet's sections from your source. Every class has Character,
   Vitals, Gear, Skills, and the page-2 blocks. Add Cantrips and Spells Known if
   it casts spells. Sample the tints so the new sheet matches the rest.
2. Add the markup to the bottom of `.page` in `index.html`. Reuse the shared
   `<sheet-section>` blocks and the existing primitives where you can.
3. Add the class's palette and layout CSS to the bottom of `sheet.css`, all
   scoped under `.sec-<class>` behind a banner comment.
4. Add an `<option>` to the `#classpick` picker.

For the full detail, read `CLAUDE.md`. It covers the three layers, adding a
class, the printed spell-list component, and how the colors are sampled. It is a
good read before a big change.

### Project layout

| File / dir | What it is |
|------------|------------|
| `index.html` | Markup only, plus the `#classpick` picker. Links `style.css` then `sheet.css` (order matters). One `<div class="sheet">` per class. |
| `style.css`  | The component library. It holds the reusable box-model pieces every sheet shares. Linked first. |
| `sheet.css`  | Per-sheet styles: section palettes and per-section layout, namespaced under `.sec-NAME`, grouped one class at a time behind banner comments. Linked after `style.css`. |
| `Master.pdf` | The original 34-page PDF, kept as a layout and style reference. Left out of the GitHub Pages build. |
| `CLAUDE.md`  | Deeper design notes (see above). |
| `docs/`      | README screenshots. Left out of the live site. |
| `tools/`     | Helper scripts. `shots.py` regenerates the README screenshots; `pngdiff.py` diffs two screenshots to confirm a change still renders the same. |

## License

5.5eSheets is released under Creative Commons Attribution-NonCommercial 4.0
(CC BY-NC 4.0). In short: use it, restyle it, and build on it for free; credit
the project with a visible link when it is on a website; and please do not sell
it or ship it in a paid product without asking first. The full terms are in
[LICENSE](LICENSE).

The license covers the HTML, CSS, and layout here. The D&D rules text, spell
names, and trademarks belong to Wizards of the Coast. This is an unofficial
project and is not affiliated with them.
