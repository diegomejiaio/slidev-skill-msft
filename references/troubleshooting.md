---
name: troubleshooting
description: Common Slidev quirks, edge cases, and CSS overrides for issues that aren't bugs but surprise everyone the first time
---

# Slidev Troubleshooting & Common Gotchas

Real issues that catch people off guard. Each entry is *what you see* → *why it happens* → *the fix*.

---

## Goto dialog appears as if "G" is being held

### Symptoms
A small input box / dropdown appears at the top-right of the slide, looking like a search
or "go to slide N" prompt. It seems to be permanently visible — as if the `G` keyboard
shortcut is stuck. Reloading doesn't help.

### Cause
Slidev ships a goto-by-number dialog triggered by pressing `G`. The element is **always
in the DOM** and positioned off-screen with utility classes `fixed right-5 -top-20` (i.e.
`top: -5rem`). When `G` is pressed it animates into view; when dismissed it animates back.

But: any of the following can pin it visible:
- A custom transform / z-index / `position: relative` on a parent that breaks the off-screen
  positioning.
- A custom theme that overrides `top` on `.fixed` selectors.
- HMR mid-animation leaving it stuck in the "open" state.
- Running PDF export — the dialog can be captured if it's mid-state.

### Fix
Add this to your deck's `style.css` (or any global stylesheet):

```css
/* Hide Slidev's goto dialog when it's in the closed/parked position.
   Without this, it can render as a stuck input box top-right depending
   on layout / transform context. */
.fixed.right-5.-top-20 {
  visibility: hidden !important;
  pointer-events: none !important;
}
```

The selector targets only the parked state (`-top-20`). When the user presses `G`,
Slidev removes `-top-20` and the dialog becomes visible normally.

### Verify
- Press `G` — dialog should appear.
- Press `Esc` or click outside — dialog should disappear cleanly.
- Export to PDF — no rogue input box in any slide.

---

## Verifying slide changes with Playwright (without lying screenshots)

### Symptoms
You change CSS, take a screenshot via Playwright, and the title looks gigantic — but
when you measure it with `getComputedStyle`, the font-size is exactly what you set.
Or you screenshot slide `/12` and get the *cover slide* instead. Or you query a card
that should contain a `<code>` element and the element is in the DOM but shows
`getBoundingClientRect()` = `0,0,0,0`.

### Cause
1. **Slidev's canvas is rendered at fixed pixel dimensions** (e.g. 1920×1080) and then
   CSS-transformed (`scale()`) to fit the viewport. Screenshots capture *post-scale*
   pixels, so a 24.8px title in canvas coords looks ~50px when the viewport is wider.
   Visual screenshots can mislead about typography sizing.
2. **URL-based navigation (`location.hash = '#/12'`) is unreliable** — Slidev preloads
   adjacent slides, hot-reloads can throw off the route, and the page sometimes ends
   up on a different slide than the URL suggests.
3. **Off-canvas slides remain in the DOM** for preloading. `document.querySelector('.card')`
   matches cards from slides you can't even see — those have `getBoundingClientRect()`
   width/height of `0`.

### Fix

**Navigate via Slidev's API, not the URL:**
```js
await page.evaluate(async (n, c) => {
  if (window.$slidev?.nav) await window.$slidev.nav.go(n, c);
  await new Promise(r => setTimeout(r, 800));   // let the slide settle
}, 12, 3);
```

**Filter to currently-visible elements only:**
```js
const visibleCards = Array.from(document.querySelectorAll('.card'))
  .filter(c => c.getBoundingClientRect().width > 0);
```

**Verify CSS with `getComputedStyle`, not the screenshot:**
```js
const el = document.querySelector('.ask-title');
const cs = getComputedStyle(el);
console.log({ fontSize: cs.fontSize, fontWeight: cs.fontWeight });
// fontSize: "24.8px" → 1.55rem at 16px base. The screenshot just *looks* bigger
// because the canvas is being scaled up to fit the viewport.
```

**When something "isn't visible", check if it's clipped vs. missing:**
```js
const code = card.querySelector('code');
const codeRect = code.getBoundingClientRect();
const cardRect = card.getBoundingClientRect();
const clipped = codeRect.bottom > cardRect.bottom || codeRect.top < cardRect.top;
// If clipped is true and the card has overflow:hidden, the element exists but
// it's positioned outside the parent's clip region. You don't have a render
// bug — you have a layout-overflow bug. (See style-microsoft-modern.md gotcha #12.)
```

### Verify
- `await window.$slidev.nav.go(12, 3)` lands you on slide 12 with 3 clicks fired.
- Filtered queries return only cards with non-zero rects (cards on the visible slide).
- Computed font-size matches the value declared in `style.css`.
- For "missing" content, comparing element rect vs. parent rect tells you whether
  it's truly absent or just clipped by `overflow: hidden`.

---

## Laser pointer dot is invisible / renders off-screen

### Symptoms
You enabled Laser via Settings → Cursor Style → Laser (v52+), the body has
the `slidev-self-laser-active` class, and `.laser-pointer` exists in the
DOM with the right `left%`/`top%` style — but no red dot is visible, OR it
appears squished against the left edge of the screen.

### Cause
The `LaserPointer.vue` template wraps the dot in
`<div class="absolute top-0 left-0 right-0 bottom-0 ...">`. Two project
configs commonly break it:

1. **UnoCSS purging `right-0`**: UnoCSS does not scan
   `node_modules/@slidev/client/`. If no other file in your project uses
   `right-0`, the class is purged → the wrapper has no `right: 0` →
   collapses to ~16px wide → dot positions at `(51% of 16px) ≈ 8px` from
   the slide edge.
2. **Custom CSS targeting `div.absolute.bottom-0.left-0`**: a common
   selector for nav-controls overrides also matches the LaserPointer
   wrapper (which has `bottom-0 left-0 absolute` too). Any `right: auto`
   or `width` rule there collapses the wrapper.

### Fix

```ts
// uno.config.ts
safelist: ['right-0']
```

```css
/* style.css — scope nav-controls overrides so they don't catch
   the LaserPointer wrapper. Use :has() to require a <nav> child. */
div.absolute.bottom-0.left-0:has(> nav.flex.flex-col) {
  /* your nav-controls overrides here */
}
```

Verify with `getComputedStyle(wrapper).right === '0px'` and
`wrapper.getBoundingClientRect().width === slideWidth`.

---

## v52 build fails with "resolves outside of Vite server.fs.allow"

### Symptoms
After upgrading from v51 → v52, `slidev build` errors with:
```
RolldownError: [slidev] Import "/icons/foo.svg" from slide Markdown
resolves outside of Vite server.fs.allow: /icons/foo.svg
```
Dev mode (`slidev`) may still work; only the build breaks.

### Cause
v52 switched to Rolldown which strictly enforces `server.fs.allow`. Plain
`<img src="/path/to/file">` is now resolved at build time and rejected.

### Fix
Convert all absolute-path images to Vue `:src` bindings (the `:` prefix
defers resolution to runtime, where Vite serves from `public/`):

```html
<!-- breaks v52 build -->
<img src="/icons/foo.svg" />

<!-- works v52 build -->
<img :src="'/icons/foo.svg'" />
```

Bulk fix with `perl -i -pe 's{<img\s+src="(/[^"]+)"}{<img :src="'"'"'$1'"'"'"}g' slides.md`.

---

## Future entries

When you discover other Slidev quirks worth documenting, add them here in the same
*Symptoms → Cause → Fix → Verify* format. Common candidates:

- Native focus ring on `v-click` elements (they get `tabindex` and the browser draws a
  big outline on click). Fix: `outline: none` + custom `:focus-visible` halo + a
  click-handler that `.blur()`s the focused element after a short delay.
- `layout: center` clipping content vertically when it overflows.
- HMR not picking up changes to `uno.config.ts`, `package.json`, `global-*.vue`, or
  files in `public/` — those need a full server restart.
- Self-hosted fonts not loading because `presetWebFonts` defaults to fetching from
  Google Fonts. Fix: `provider: 'none'` in the preset config.
- Slide transitions interacting badly with non-transparent layouts (global-bottom layers
  flash / disappear during fade).
