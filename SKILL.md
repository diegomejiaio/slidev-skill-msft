---
name: slidev
description: Create and present web-based slidedecks for developers using Slidev with Markdown, Vue components, code highlighting, animations, and interactive features. Use when building technical presentations, conference talks, code walkthroughs, teaching materials, or developer decks.
---

# Slidev - Presentation Slides for Developers

Web-based slides maker built on Vite, Vue, and Markdown.

## When to Use

- Technical presentations or slidedecks with live code examples
- Syntax-highlighted code snippets with animations
- Interactive demos (Monaco editor, runnable code)
- Mathematical equations (LaTeX) and diagrams (hand-authored SVG/Vue, Excalidraw, Mermaid)
- Record presentations with presenter notes
- Export to PDF, PPTX, or host as SPA
- Code walkthroughs for developer talks or workshops

## Quick Start

```bash
pnpm create slidev    # Create project
pnpm run dev          # Start dev server (opens http://localhost:3030)
pnpm run build        # Build static SPA
pnpm run export       # Export to PDF (requires playwright-chromium)
```

**Verify**: After `pnpm run dev`, confirm slides load at `http://localhost:3030`. After `pnpm run export`, check the output PDF exists in the project root.

## Basic Syntax

```md
---
theme: default
title: My Presentation
---

# First Slide

Content here

---

# Second Slide

More content

<!--
Presenter notes go here
-->
```

- `---` separates slides
- First frontmatter = headmatter (deck config)
- HTML comments = presenter notes

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Markdown Syntax | Slide separators, frontmatter, notes, code blocks | [core-syntax](references/core-syntax.md) |
| Animations | v-click, v-clicks, motion, transitions | [core-animations](references/core-animations.md) |
| Headmatter | Deck-wide configuration options | [core-headmatter](references/core-headmatter.md) |
| Frontmatter | Per-slide configuration options | [core-frontmatter](references/core-frontmatter.md) |
| CLI Commands | Dev, build, export, theme commands | [core-cli](references/core-cli.md) |
| Components | Built-in Vue components | [core-components](references/core-components.md) |
| Layouts | Built-in slide layouts | [core-layouts](references/core-layouts.md) |
| Exporting | PDF, PPTX, PNG export options | [core-exporting](references/core-exporting.md) |
| Hosting | Build and deploy to various platforms | [core-hosting](references/core-hosting.md) |
| Global Context | $nav, $slidev, composables API | [core-global-context](references/core-global-context.md) |

## Feature Reference

### Code & Editor

| Feature | Usage | Reference |
|---------|-------|-----------|
| Line highlighting | `` ```ts {2,3} `` | [code-line-highlighting](references/code-line-highlighting.md) |
| Click-based highlighting | `` ```ts {1\|2-3\|all} `` | [code-line-highlighting](references/code-line-highlighting.md) |
| Line numbers | `lineNumbers: true` or `{lines:true}` | [code-line-numbers](references/code-line-numbers.md) |
| Scrollable code | `{maxHeight:'100px'}` | [code-max-height](references/code-max-height.md) |
| Code tabs | `::code-group` (requires `comark: true`) | [code-groups](references/code-groups.md) |
| Monaco editor | `` ```ts {monaco} `` | [editor-monaco](references/editor-monaco.md) |
| Run code | `` ```ts {monaco-run} `` | [editor-monaco-run](references/editor-monaco-run.md) |
| Edit files | `<<< ./file.ts {monaco-write}` | [editor-monaco-write](references/editor-monaco-write.md) |
| Code animations | `` ````md magic-move `` | [code-magic-move](references/code-magic-move.md) |
| TypeScript types | `` ```ts twoslash `` | [code-twoslash](references/code-twoslash.md) |
| Import code | `<<< @/snippets/file.js` | [code-import-snippet](references/code-import-snippet.md) |

### Diagrams & Math

**Choosing a diagram approach.** Reach in this order, not alphabetically:

1. **Hand-authored SVG/Vue** — [diagram-rough-sketch](references/diagram-rough-sketch.md)
   (sketchy) or [animation-svg-anime](references/animation-svg-anime.md) (polished,
   animated). Full control of layout, colour, staging and animation. Default
   choice for anything that carries the argument of the talk: architecture,
   flows, mental models.
2. **Excalidraw** — [diagram-excalidraw](references/diagram-excalidraw.md). When
   you want to *draw* it rather than code it, and it won't need click staging.
3. **Mermaid / PlantUML** — only when the diagram is genuinely generated from
   structure (a real state machine, an ER model, an exact sequence with
   timings), or when it's throwaway. Auto-layout will fight you on spacing,
   theming and reveal order, and the output reads as generic.

LaTeX is orthogonal — use it for any real math.

| Feature | Usage | Reference |
|---------|-------|-----------|
| Hand-drawn sketch diagrams | `rough.svg(el)` in a Vue component (`npm i roughjs`) | [diagram-rough-sketch](references/diagram-rough-sketch.md) |
| Animated SVG diagrams | anime.js in a Vue component | [animation-svg-anime](references/animation-svg-anime.md) |
| Excalidraw drafts | `<Excalidraw drawFilePath="..." />` (addon, `pnpm add slidev-addon-excalidraw`) | [diagram-excalidraw](references/diagram-excalidraw.md) |
| LaTeX math | `$inline$` or `$$block$$` | [diagram-latex](references/diagram-latex.md) |
| Mermaid diagrams | `` ```mermaid `` — structural/throwaway only | [diagram-mermaid](references/diagram-mermaid.md) |
| PlantUML diagrams | `` ```plantuml `` — structural/throwaway only | [diagram-plantuml](references/diagram-plantuml.md) |

### Layout & Styling

| Feature | Usage | Reference |
|---------|-------|-----------|
| Canvas size | `canvasWidth`, `aspectRatio` | [layout-canvas-size](references/layout-canvas-size.md) |
| Zoom slide | `zoom: 0.8` | [layout-zoom](references/layout-zoom.md) |
| Scale elements | `<Transform :scale="0.5">` | [layout-transform](references/layout-transform.md) |
| Layout slots | `::right::`, `::default::` | [layout-slots](references/layout-slots.md) |
| Scoped CSS | `<style>` in slide | [style-scoped](references/style-scoped.md) |
| Global layers | `global-top.vue`, `global-bottom.vue` | [layout-global-layers](references/layout-global-layers.md) |
| Draggable elements | `v-drag`, `<v-drag>` | [layout-draggable](references/layout-draggable.md) |
| Icons | `<mdi-icon-name />` | [style-icons](references/style-icons.md) |

### Animation & Interaction

| Feature | Usage | Reference |
|---------|-------|-----------|
| Click animations | `v-click`, `<v-clicks>` | [core-animations](references/core-animations.md) |
| Rough markers | `v-mark.underline`, `v-mark.circle` | [animation-rough-marker](references/animation-rough-marker.md) |
| Drawing mode | Press `C` or config `drawings:` | [animation-drawing](references/animation-drawing.md) |
| Direction styles | `forward:delay-300` | [style-direction](references/style-direction.md) |
| Note highlighting | `[click]` in notes | [animation-click-marker](references/animation-click-marker.md) |

### Syntax Extensions

| Feature | Usage | Reference |
|---------|-------|-----------|
| Comark syntax | `comark: true` + `{style="color:red"}` | [syntax-comark](references/syntax-comark.md) |
| Block frontmatter | `` ```yaml `` instead of `---` | [syntax-block-frontmatter](references/syntax-block-frontmatter.md) |
| Import slides | `src: ./other.md` | [syntax-importing-slides](references/syntax-importing-slides.md) |
| Merge frontmatter | Main entry wins | [syntax-frontmatter-merging](references/syntax-frontmatter-merging.md) |

### Presenter & Recording

| Feature | Usage | Reference |
|---------|-------|-----------|
| Recording | Press `G` for camera | [presenter-recording](references/presenter-recording.md) |
| Laser pointer | Settings → Cursor Style → Laser (v52+) | [presenter-laser-pointer](references/presenter-laser-pointer.md) |
| Timer | `duration: 30min`, `timer: countdown` | [presenter-timer](references/presenter-timer.md) |
| Remote control | `slidev --remote` | [presenter-remote](references/presenter-remote.md) |
| Ruby text | `notesAutoRuby:` | [presenter-notes-ruby](references/presenter-notes-ruby.md) |

### Export & Build

| Feature | Usage | Reference |
|---------|-------|-----------|
| Export options | `slidev export` | [core-exporting](references/core-exporting.md) |
| Build & deploy | `slidev build` | [core-hosting](references/core-hosting.md) |
| Build with PDF | `download: true` | [build-pdf](references/build-pdf.md) |
| Cache images | Automatic for remote URLs | [build-remote-assets](references/build-remote-assets.md) |
| OG image | `seoMeta.ogImage` or `og-image.png` | [build-og-image](references/build-og-image.md) |
| SEO tags | `seoMeta:` | [build-seo-meta](references/build-seo-meta.md) |
| Offline / PWA | `pwa: 'build'` (v52.17+, `npm i -D vite-plugin-pwa`) | [build-pwa](references/build-pwa.md) |

**Export prerequisite**: `pnpm add -D playwright-chromium` is required for PDF/PPTX/PNG export. If export fails with a browser error, install this dependency first.

### Editor & Tools

| Feature | Usage | Reference |
|---------|-------|-----------|
| Side editor | Click edit icon | [editor-side](references/editor-side.md) |
| VS Code extension | Install `antfu.slidev` | [editor-vscode](references/editor-vscode.md) |
| Prettier | `prettier-plugin-slidev` | [editor-prettier](references/editor-prettier.md) |
| Eject theme | `slidev theme eject` | [tool-eject-theme](references/tool-eject-theme.md) |
| Visual editor (Studio) | Press `E` (addon, `pnpm add -D slidev-addon-studio`) | [tool-studio](references/tool-studio.md) |
| MCP server (AI agents) | `http://localhost:3030/__mcp` or `slidev mcp` | [tool-mcp](references/tool-mcp.md) |

**Editing slides as an agent**: when a dev server is running, prefer the MCP
tools over raw markdown edits for slide-level operations (update / insert /
remove / move). They handle Slidev's compound separators correctly, hot-reload
instantly, and `slidev-goto-slide` navigates the live browser so you can verify
the result visually.

### Lifecycle & API

| Feature | Usage | Reference |
|---------|-------|-----------|
| Slide hooks | `onSlideEnter()`, `onSlideLeave()` | [api-slide-hooks](references/api-slide-hooks.md) |
| Navigation API | `$nav`, `useNav()` | [core-global-context](references/core-global-context.md) |

## Common Layouts

| Layout | Purpose |
|--------|---------|
| `cover` | Title/cover slide |
| `center` | Centered content |
| `default` | Standard slide |
| `two-cols` | Two columns (use `::right::`) |
| `two-cols-header` | Header + two columns |
| `image` / `image-left` / `image-right` | Image layouts |
| `iframe` / `iframe-left` / `iframe-right` | Embed URLs |
| `quote` | Quotation |
| `section` | Section divider |
| `fact` / `statement` | Data/statement display |
| `intro` / `end` | Intro/end slides |

## Theme Recipes

Pre-built, opinionated style packs that go beyond the default theme. Each recipe is a
single self-contained reference — drop the files in, tweak content, ship.

| Recipe | Look & feel | Reference |
|--------|-------------|-----------|
| Microsoft Modern | Light "paper" canvas + animated MS-brand swoosh + glass cards + Selawik (Segoe substitute). For MS customer / partner / ISV decks. | [style-microsoft-modern](references/style-microsoft-modern.md) |

## Icon Packs

Official icon sources beyond the default Carbon set, with installation and usage patterns.

| Pack | What you get | Reference |
|------|--------------|-----------|
| Microsoft & Azure icons | Fluent System Icons (open MIT) · Azure Architecture Icons (custom UnoCSS collection) · Microsoft brand logos · fallbacks for Fabric, Power Platform, Defender/Sentinel/Entra, partner logos, GitHub/VS Code/dev tech, 3D illustrated keynote icons | [style-microsoft-icons](references/style-microsoft-icons.md) |

## Troubleshooting

Slidev quirks and edge cases that aren't bugs but surprise everyone the first time.
**Read this when something visually weird happens that doesn't match the docs.**

| Symptom | Reference |
|---------|-----------|
| Goto dialog stuck visible (looks like `G` is held) · v-click focus rings · self-hosted font load failures · `layout: center` content clipping · HMR not picking up config changes · Playwright screenshots / queries returning misleading results · laser pointer dot invisible after enabling · v52 build fails with `server.fs.allow` on plain `<img src="/...">` | [troubleshooting](references/troubleshooting.md) |
| Tailwind `text-*` not shrinking `<h2>` titles · cards clipping their bottom line in flex-col grids · need a content-slide title token · need a compact card variant for dense grids | [style-microsoft-modern](references/style-microsoft-modern.md) (gotchas #11, #12 + `.ask-title`, `.card-compact`) |

## Resources

- Documentation: https://sli.dev
- Theme Gallery: https://sli.dev/resources/theme-gallery
- Showcases: https://sli.dev/resources/showcases
