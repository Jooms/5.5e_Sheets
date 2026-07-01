# 5.5eSheets

This project rebuilds the hornbook1776 D&D 5e character sheets (`Master.pdf`) as
a plain web page. Instead of a heavy PDF, you get HTML and CSS that keep the
original layout but let you change the look and the fields whenever you want.
Every sheet is built by hand from ordinary `div` and `span` elements with CSS
borders. No canvas, no images, no framework.

**Live page: <https://jooms.github.io/5.5e_Sheets/>**

## Design goal

Keep the project HTML- and CSS-based. The layout, the styling, and every field
live in the markup and stylesheets, which is what keeps the sheets easy to read
and easy to change. JavaScript stays as small as it can be. The only scripts are
plain vanilla JS for adding and removing sections: the class picker that shows
one sheet at a time, and the `<sheet-section>` helper that copies shared markup
into place. No framework, no build step, no bundler. If you can do something in
HTML or CSS, do it there. Sticking to that is a fun constraint, and it keeps the
whole thing easy to hack on.

## Run it

Open `index.html` in any browser. It runs straight from the filesystem
(`file://`), so there is no server to start and nothing to install. The page is a
fixed 594px wide and prints cleanly. A picker in the top-left corner (screen
only) shows one class sheet at a time. You can also jump straight to a class with
`index.html?class=cleric`.

## Project layout

| File / dir | What it is |
|------------|------------|
| `index.html` | Markup only, plus the `#classpick` picker. It links `style.css` and then `sheet.css` (that order matters) and holds the small picker script. One `<div class="sheet">` per class. |
| `style.css`  | The component library: the reusable box-model pieces every sheet shares, like `.section`, `.box`, `.lbl`, `.cbx`, `.ring`, and `.lined`. Change a piece here and every sheet updates. Linked first. |
| `sheet.css`  | The per-sheet styles: section color palettes and per-section layout. Every rule is namespaced under a `.sec-NAME` so classes can't step on each other. The file is grouped one class at a time behind banner comments like `PALADIN SHEET`. Linked after `style.css`. |
| `Master.pdf` | The original 34-page PDF, committed to the repo as a reference for how the sheets should look. `_config.yml` excludes it from the Jekyll build, so GitHub Pages never serves it. |
| `CLAUDE.md`  | Deeper design notes: the three layers, how to add a class, the pre-printed spell-list component, and how colors are sampled. Worth reading before a big change. |
| `tools/`     | `pngdiff.py`, a small script that diffs two screenshots to confirm a change renders the same. |

### The three layers

1. Primitives (`style.css`): the shapes shared by everything.
2. Palettes (`sheet.css`): one tint line per section, with colors sampled from
   `Master.pdf`.
3. Layout (`sheet.css`): per-section positioning, namespaced under `.sec-NAME`.

Structure lives in the markup, and CSS only handles the theme and the
positioning. Watch out for one thing: CSS `/* */` comments do not nest. Nest one
by accident and the whole page goes blank.

## Where do I edit for X?

- Change how a box, checkbox, or label looks everywhere: `style.css`.
- Change one class's panel: find its banner in `sheet.css` for the styles and its
  `<!-- ===== CLASS SHEET =====-->` banner in `index.html` for the markup.
- Change a section that every class shares (Character, Vitals, Gear, Skills, the
  page-2 blocks, Cantrips, Spells Known): the shared markup lives once in a
  `<template>` near the bottom of `index.html`, and its CSS is the matching
  `.sec-*` block in `sheet.css`.

## Add a class

Every class from `Master.pdf` is already ported. To add a new class from a
different sourcebook, a homebrew write-up, or any other material, build its sheet
the same way the existing ones are built and follow the same steps. (`Master.pdf`
stays around only as a style and layout reference.)

1. Work out the sheet's layout from your source. Decide which sections it needs
   (every class has Character, Vitals, Gear, Skills, and the page-2 blocks), what
   belongs in its own class panel, and whether it casts spells (if so, add
   Cantrips and Spells Known). Sample the section tints and match the style of the
   existing sheets so the new one fits in.
2. Add the sheet's markup to the bottom of `.page` in `index.html`, reusing the
   shared `<sheet-section>` blocks and the existing primitives where you can.
3. Add the class's palette and layout CSS to the bottom of `sheet.css`, all
   scoped under `.sec-<class>` behind a banner comment.
4. Add an `<option>` to the `#classpick` picker.

## Use it on your site

You're welcome to drop these sheets into your own site. If you do, the license
(see below) asks for one thing back: a visible credit that links to the project.
Pick one of the two snippets below and paste it near the sheets. Both are
self-contained. The styles are inline and the GitHub logo is an inline SVG, so
there is nothing extra to load.

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

Or a plain link, if that fits your page better:

```html
<!-- 5.5eSheets attribution -->
Character sheets by
<a href="https://github.com/Jooms/5.5e_Sheets"
   style="color:#0969da;text-decoration:none;border-bottom:1px solid currentColor;">5.5eSheets</a>
```

## License

5.5eSheets is released under Creative Commons Attribution-NonCommercial 4.0
(CC BY-NC 4.0). The short version: use it, restyle it, and build on it for free;
credit the project with a visible link when it's on a website; and don't sell it
or ship it in a paid product without asking first. Full terms are in
[LICENSE](LICENSE).

The license covers the HTML, CSS, and layout here. D&D rules text, spell names,
and trademarks belong to Wizards of the Coast. This is an unofficial project and
is not affiliated with them.
