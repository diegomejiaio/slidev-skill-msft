---
name: studio
description: Visual, Keynote-style editor for a Slidev deck that only ever writes small Markdown diffs
---

# Studio (Visual Editor)

Community addon: [`slidev-addon-studio`](https://github.com/BobTheShoplifter/slidev-addon-studio)
(not an official Slidev addon). Select, drag, resize, animate and compose slides on the canvas
while the deck stays plain Markdown — every action is a small, readable edit to the `.md` file.

## Install

```bash
pnpm add -D slidev-addon-studio
```

Enable in the deck's headmatter:

```md
---
addons:
  - slidev-addon-studio
---
```

(Or under `"slidev": { "addons": [...] }` in `package.json` to apply it to every deck in the
project.)

## Usage

Press `E`, or click the pencil button in Slidev's bottom bar, to open/close Studio. It adds
nothing to the slide while closed.

| Panel | What it edits |
|-------|----------------|
| Element | Position, size, rotation, component props, utility classes, order, duplicate, delete, raw Markdown of the selection |
| Components | Markdown basics plus every component the deck can use, with live previews; click to insert, drag to place freely |
| Animate | Click steps, reveal/hide, entrance animations, staggered lists, motion presets, slide transitions |
| Layout | Layout thumbnails, the frontmatter keys that layout reads, title/classes/background/zoom/click count/notes |
| Slides | Live thumbnails, drag to reorder, add, duplicate, delete |
| Assets | Drop images into `public/` and insert them |

### Keyboard

| Key | Action |
|-----|--------|
| `E` | Open/close Studio |
| Double click | Edit a block's text in place |
| Drag | Move the selection (a plain click never repositions) |
| Backspace / Delete | Delete the selected element |
| Esc | Back out one layer (drag → text editor → selection) |
| Ctrl+Z / Ctrl+Shift+Z | Undo / redo |
| Alt (held) | Bypass snapping while dragging |
| Shift (held) | Keep aspect ratio, or snap rotation to 15° |

Undo history lives in the page only — a reload, or any action that renumbers the deck (add,
duplicate, delete, reorder, skip a slide), clears it. The deck is a file in git; that is the real
undo.

## Teaching Studio about your own components

- A component's doc-comment usage example becomes its palette snippet automatically:
  `/** <BigCount :to="138723" label="Enheter" /> */`.
- Props are read from `defineProps`; a string union becomes a dropdown, a number is bound, a
  boolean is a toggle, values that look like colors get a swatch picker from the deck's own CSS
  custom properties.
- For anything more, add a `<studio lang="yaml">` custom SFC block with `description`, `category`,
  `snippet`, `preview`, `hidden`, and per-prop `label`/`hidden`/`options`/`control`/`fields`.
- A layout's frontmatter-only text (e.g. `layout: fact` with `value:`/`label:`) is exposed by
  marking the template: `<h1 data-studio-prop="title">{{ title }}</h1>`.

## Configuration

All optional, under `studio` in the headmatter:

```md
---
studio:
  annotate: all         # all | html | off — how much source-tracing metadata to render
  hideComponents:
    - InternalThing
---
```

Slidev's own `editor: false` disables Studio completely.

## Limitations

- Only works while `slidev` is running with the editor enabled — a built/exported/printed deck
  contains none of it.
- Slides imported via `src:` can only be reordered within their own file; the entry file's first
  slide (deck-wide frontmatter) can't be deleted or moved.
- Components Slidev itself generates from fenced code (`Monaco`, `Mermaid`, `PlantUml`) don't
  appear in the palette — write the fenced block instead.
- A component with multiple root template nodes is left out (Vue drops fallthrough attrs on a
  fragment root, so it can't carry the selection annotation).
- Only `defineProps` / Options API props are auto-detected; anything more exotic needs a manual
  `<studio>` block.
- If the project sets its own `slidev.markdown.markdownSetup` in Vite config, it replaces the
  addon's and click-to-select breaks — call `studioMarkdownSetup(md)` from your setup to restore it.

## Resources

- Addon repo: https://github.com/BobTheShoplifter/slidev-addon-studio
- Addon Gallery: https://sli.dev/resources/addon-gallery
