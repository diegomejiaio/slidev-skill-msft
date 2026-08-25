---
name: excalidraw
description: Render .excalidraw drafts as SVG inside a slide via the community addon
---

# Excalidraw Drafts

Render `.excalidraw` files to SVG with Excalidraw's modern export pipeline (including
`Excalifont`), so a hand-drawn draft stays an editable source instead of a flattened screenshot.

Community addon: [`slidev-addon-excalidraw`](https://github.com/haydenull/slidev-addon-excalidraw)
(not an official Slidev addon).

## Install

```bash
pnpm add slidev-addon-excalidraw
```

## Enable

In the deck's headmatter:

```md
---
addons:
  - slidev-addon-excalidraw
---
```

(Or under `"slidev": { "addons": [...] }` in `package.json` if the addon should apply
project-wide rather than per-deck.)

## Usage

The `.excalidraw` file must live under `public/` and `drawFilePath` is resolved relative to the
Vite [public base path](https://vitejs.dev/guide/build.html#public-base-path) — not relative to
the `.md` file.

```md
<Excalidraw
  drawFilePath="/diagrams/my-draft.excalidraw"
  class="w-[600px]"
  :darkMode="false"
  :background="false"
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `drawFilePath` | string | — | Path to the `.excalidraw` file, relative to the public base path |
| `darkMode` | boolean | `false` | Render with Excalidraw's dark palette |
| `background` | boolean | `false` | Include the canvas background in the export |

## Notes

- Restart the dev server after installing — Vite doesn't pick up a new addon via HMR.
- The component loads `exportToSvg` from `@excalidraw/excalidraw` via esm.sh at runtime, so the
  export machinery isn't bundled locally.
- For offline/self-hosted font assets, set `window.EXCALIDRAW_ASSET_PATH` before Slidev mounts.

## Resources

- Addon repo: https://github.com/haydenull/slidev-addon-excalidraw
- Addon Gallery: https://sli.dev/resources/addon-gallery
