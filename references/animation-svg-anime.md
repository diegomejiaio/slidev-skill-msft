# Animated SVG Diagrams with anime.js v4 in Slidev

Custom SVG components driven by `animejs` v4 are the highest-leverage way to build
storytelling slides in Slidev — sequence diagrams, n-tier architecture reveals, packet
flows, animated handoffs, etc. They also have **non-obvious failure modes** that waste
hours when you hit them for the first time. This reference captures the patterns and
gotchas that recur across every such component.

Use this when you need:

- A "story slide" that progresses with `$clicks` (e.g. sequence diagram, step-by-step flow)
- An animated architecture diagram (tiers fade in, links draw, packets travel)
- Any custom Vue component that animates SVG `<g>` / `<circle>` / `<rect>` / `<path>` elements

Pair it with **[`style-microsoft-modern`](style-microsoft-modern.md)** for the visual
language and **[`core-animations`](core-animations.md)** for click semantics.

---

## Setup

```bash
pnpm add animejs
```

```ts
// Vue component
import { animate, createTimeline, stagger, utils } from 'animejs'
```

`animejs` v4 API differences from v3:

| v3                  | v4                                |
|---------------------|-----------------------------------|
| `anime({...})`      | `animate(target, params)`         |
| `anime.timeline()`  | `createTimeline({ defaults: ... })` |
| `anime.set(el, p)`  | `utils.set(el, p)`                |
| `anime.stagger(n)`  | `stagger(n)` (named import)        |

Easing names are camelCase: `'inOutCubic'`, `'outBack'`, `'outQuad'`, `'inOutSine'`.

---

## Component skeleton

A click-driven animated SVG component always follows the same shape:

```vue
<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { animate, createTimeline, stagger, utils } from 'animejs'

const props = defineProps<{ clicks?: number }>()

const root = ref<HTMLElement | null>(null)
let tl: ReturnType<typeof createTimeline> | null = null

function setInitialState() {
  if (!root.value) return
  // Hide everything that animates in
  utils.set(root.value.querySelectorAll('.thing'), { opacity: 0 })
  // For stroke-draw paths, prime the dash offset
  utils.set(root.value.querySelectorAll('.link'), {
    strokeDashoffset: (el: SVGPathElement) => el.dataset.dash,
  })
}

function buildTimeline() {
  if (!root.value) return null
  const t = createTimeline({ autoplay: false, defaults: { ease: 'inOutCubic' } })
  // ...
  return t
}

function syncToClicks(c: number) {
  if (!tl) return
  if (c >= 2) tl.seek(tl.duration)
  else if (c === 1) tl.seek(tl.duration * 0.55)
  else tl.seek(tl.duration * 0.18)
}

onMounted(async () => {
  // wait two frames so layout & path totalLength are accurate
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))
  // Compute path lengths for stroke-draw
  if (root.value) {
    root.value.querySelectorAll<SVGPathElement>('.link').forEach((p) => {
      const len = Math.ceil(p.getTotalLength())
      p.dataset.dash = String(len)
      p.style.strokeDasharray = String(len)
      p.style.strokeDashoffset = String(len)
    })
  }
  setInitialState()
  tl = buildTimeline()
  syncToClicks(props.clicks ?? 0)
})

watch(() => props.clicks, (c) => syncToClicks(c ?? 0))
onBeforeUnmount(() => { tl?.pause(); tl = null })
</script>

<template>
  <div ref="root" class="diagram">
    <svg viewBox="0 0 1600 920" preserveAspectRatio="xMidYMid meet">
      <!-- ... -->
    </svg>
  </div>
</template>
```

Slot it into a slide with:

```md
---
title: 'My animated story'
clicks: 3
---

<div class="stage">
  <MyDiagram :clicks="$clicks" />
</div>

<style scoped>
.stage { position: absolute; left: 1.2rem; right: 1.2rem; top: 7.5rem; bottom: 0.6rem; }
</style>
```

`clicks: 3` declares the slide expects 3 click steps. `:clicks="$clicks"` passes the
current click count from Slidev into the component.

---

## Click semantics

`$clicks` increases as the user presses Space / Right. `clicks=N` means **N elements
have been revealed** — so step indices `0..N-1` are visible.

For diagrams, choose between two patterns:

- **Single timeline + `seek()`** — best for n-tier diagrams with 3-4 phases. Map each
  click to a labelled position (`'s2'`, `'s3'`) and `seek()` to it.
- **Per-step `animate()` calls** — best for sequence diagrams with 8-10+ steps. Each
  step is independent: `if (c >= i+1) showStep(i); else hideStep(i);` Cleaner reverse
  logic when the user navigates back.

Always handle reverse: when the user presses Left, `$clicks` decreases — the diagram
must roll back to the earlier state. With per-step `animate()`, call a `reset(i)`
function on steps with index ≥ c.

---

## Critical gotchas

### 1 · anime.js + SVG `transform` conflict (the #1 trap)

**Symptom**: an SVG `<g transform="translate(120, 200)">` element being animated by
anime.js (e.g. `scale: [0.6, 1]` or `translateY: [-18, 0]`) **silently moves to position
(0, 0)**. Other elements at that group's position appear correctly, but the animated
group doesn't.

**Cause**: anime.js applies its animations as a **CSS `transform`** property
(`transform: translate3d(0,0,0) scale(1)`). For SVG elements, the CSS `transform` value
**fully overrides** the SVG `transform` attribute. So your `transform="translate(X, Y)"`
positioning is wiped out the moment anime.js touches the element.

**Fix — the double-wrap pattern**: separate positioning from animation by using two
nested `<g>` elements. The outer `<g>` carries the SVG positioning attribute; the inner
`<g>` is what anime.js animates.

```html
<!-- ❌ Broken: anime.js scale wipes the translate -->
<g transform="translate(800, 300)" class="badge">
  <circle r="12" />
  <text>1</text>
</g>

<!-- ✅ Works: outer positions, inner animates -->
<g transform="translate(800, 300)">
  <g class="badge">
    <circle r="12" />
    <text>1</text>
  </g>
</g>
```

This applies to **any** SVG element you `scale`, `translate`, `rotate`, or `opacity`-
animate — badges, pulse rings, callouts, agent figures, packet dots, you name it. If the
group has both a position and an anime.js target class, double-wrap.

### 2 · `marker-end` triangles don't follow `stroke-dashoffset`

**Symptom**: animating a `<path>` with `stroke-dashoffset` (the classic "draw the arrow"
trick) reveals the arrowhead immediately at its endpoint, even when the rest of the line
is invisible. At `clicks=0` you see a row of orphan triangles floating where arrows
would land.

**Cause**: SVG markers (`marker-end`) are rendered at the path's geometric endpoint
regardless of the dash state. The browser does not "draw" the marker progressively.

**Fix**: gate the entire path with `opacity` instead of relying on dash visibility.

```ts
function reset(i: number) {
  utils.set(arrowEl(i), { opacity: 0, strokeDashoffset: dashLen(i) })
}
function show(i: number) {
  utils.set(arrowEl(i), { opacity: 1 })
  animate(arrowEl(i), { strokeDashoffset: 0, duration: 460, ease: 'inOutCubic' })
}
```

The dash animation still gives the "draw" effect, but the marker is only visible while
the line is being drawn or fully drawn.

### 3 · HTML overlays drift relative to SVG content (use `<foreignObject>`)

**Symptom**: you build an SVG with bubble labels positioned as HTML divs over the SVG
container, computing positions as `left: pct(X) + '%'` from viewBox math. At
1280×720 it looks fine; at 1600×900 it drifts 80px to the right. Bubbles no longer
land on the lifelines they label.

**Cause**: `preserveAspectRatio="xMidYMid meet"` (the default) preserves the SVG's
aspect ratio while scaling it to fit the container. If the container's aspect ratio
differs from the viewBox, "meet" leaves whitespace on one axis and centers the SVG
inside it. Any HTML overlay positioned by `% of container` does **not** get that
centering offset, so it drifts.

**Fix**: put the HTML inside the SVG via `<foreignObject>`. The `x`, `y`, `width`,
`height` are in viewBox units, so they automatically scale and align with arrows /
lifelines / circles drawn by the SVG.

```html
<svg viewBox="0 0 1700 760">
  <line x1="230" y1="120" x2="230" y2="700" class="lifeline" />
  <foreignObject x="70" y="200" width="320" height="56">
    <div xmlns="http://www.w3.org/1999/xhtml" class="bubble">
      Sí, pasaron las validaciones SUNAT
    </div>
  </foreignObject>
</svg>
```

`xmlns` on the inner div is required for the HTML to render.

The bubble is now a peer of the SVG geometry — perfect alignment, no manual % math, no
drift across resolutions.

### 4 · Selectors for HTML elements outside the animated SVG

**Symptom**: you write `.add('.tier-1 .arch-tier-label', { opacity: [0, 1] })` and the
labels never fade in. Validation shows `opacity: 0` is set (from `setInitialState()`)
but the timeline never transitions them.

**Cause**: the labels are HTML `<div>`s rendered as **siblings** of the SVG (typically
"tier badge chips" floating over the diagram), not children of the `<g class="tier-1">`
SVG group. The descendant selector matches nothing.

**Fix**: use a flat selector that matches the actual DOM:

```html
<svg>
  <g class="tier tier-1">…</g>
</svg>
<div class="arch-tier-label arch-tier-label-1">1 Frontend</div>
```

```ts
// ❌ Doesn't match — label isn't inside .tier-1
.add('.tier-1 .arch-tier-label', { opacity: [0, 1] })

// ✅ Matches the flat HTML class
.add('.arch-tier-label-1', { opacity: [0, 1] })
```

Always cross-check the selector against the actual rendered DOM. Easy to miss when the
SVG and the HTML overlay grow apart over iterations.

### 5 · Stroke-dash priming requires two `requestAnimationFrame` waits

**Symptom**: `path.getTotalLength()` returns `0` or a wrong value when called from
`onMounted()`, so the dash never fully hides the line and you see the path appear
from a half-drawn state.

**Cause**: Vue's `onMounted` fires before the browser has computed the SVG layout in
some scenarios. `getTotalLength()` is only reliable once the path is laid out.

**Fix**: wait two frames before measuring:

```ts
onMounted(async () => {
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))
  root.value!.querySelectorAll<SVGPathElement>('.link').forEach((p) => {
    const len = Math.ceil(p.getTotalLength())
    p.dataset.dash = String(len)
    p.style.strokeDasharray = String(len)
    p.style.strokeDashoffset = String(len)
  })
  // ...
})
```

Store the length on `dataset.dash` so the timeline can read it back as
`(el) => el.dataset.dash` — that lets a single `.add('.link', ...)` animate paths of
varying lengths correctly.

### 6 · `setInitialState()` must run before the timeline is built

If you build the timeline first and call `utils.set(...)` to hide things afterwards,
the timeline captures the *visible* state as the "from" value. The animation then has
nothing to animate from, and elements pop in instead of fading.

```ts
onMounted(async () => {
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))
  // 1. measure paths
  // 2. setInitialState() — hide everything
  // 3. buildTimeline() — captures hidden state as "from"
  // 4. syncToClicks(props.clicks ?? 0)
})
```

### 7 · `position: relative` on the wrapper is required for HTML overlays

If your SVG diagram has HTML overlays (chips, labels, badges that sit *next* to the
SVG, not inside `<foreignObject>`), the wrapper `div` must be `position: relative` for
the overlay's `position: absolute` to anchor correctly.

```css
.diagram {
  position: relative;       /* ← this anchors overlays */
  width: 100%;
  height: 100%;
}
.diagram .svg { position: absolute; inset: 0; width: 100%; height: 100%; }
.diagram .chip { position: absolute; top: 1%; left: 0; }
```

### 8 · Looping pulse rings must be in their own `animate()` call, not the timeline

`createTimeline()` advances linearly and stops at the end. If you want a pulse ring
that loops while the slide sits at clicks=N, attach it via a separate `animate(...,
{ loop: true })` and start/stop it from `syncToClicks` — don't put it inside the
timeline.

```ts
let pulseTl: ReturnType<typeof animate> | null = null

function startPulse() {
  if (!root.value) return
  pulseTl?.pause()
  pulseTl = animate(root.value.querySelectorAll('.pulse-ring'), {
    scale: [0.6, 2.4],
    opacity: [0.7, 0],
    duration: 1600,
    loop: true,
    ease: 'outQuad',
  })
}

function stopPulse() {
  pulseTl?.pause()
  pulseTl = null
  if (root.value) utils.set(root.value.querySelectorAll('.pulse-ring'), { opacity: 0 })
}
```

(Pulse rings also need the **double-wrap pattern from gotcha 1** — they animate `scale`,
which requires a positioning outer `<g>` and an animated inner `<g>` with `cx="0" cy="0"`.)

### 9 · `slidev` async shells get killed mid-session

The Slidev dev server (started via `./run.sh` in an async bash shell) routinely exits
with code 143 (SIGTERM) after the runtime cleans up long-running shells. When this
happens you'll see HMR stop working and screenshots show stale content.

**Fix**: relaunch in a **new** shellId (`slidev2`, `slidev3`, …). A short helper makes
this trivial:

```bash
# run.sh — kills any prior process on the port then starts fresh
#!/usr/bin/env bash
PORT=3035
lsof -ti:$PORT | xargs kill 2>/dev/null
exec pnpm exec slidev --port $PORT
```

---

## Two storytelling patterns

### Pattern A — Sequence diagram (Cliente · Asesor · Agente)

Use for "user journey" or "system handoff" stories. Three vertical lifelines, ~10
messages, each step is one click.

Constants that work well at viewBox `0 0 1700 760`:

```ts
const X_LANE_1 = 230
const X_LANE_2 = 850
const X_LANE_3 = 1380   // leave ~300px of right margin for self-action bubbles
const Y_HEAD   = 86     // actor header row
const Y_FIRST  = 188    // first message row (clears actor + sublabel)
const ROW_H    = 52
```

Per step you draw:

- An arrow `<path>` between two lanes (or self-loop on a single lane), gated by
  `opacity` (gotcha 2)
- An HTML bubble inside `<foreignObject>` with the message text
- A numbered badge `<g>` using the double-wrap pattern (gotcha 1)
- Optional pulse ring on the receiver, also double-wrapped, attached to a separate
  looping `animate()` (gotcha 8)

Self-action bubbles (e.g. "Agente verifica documentos") extend rightward from the
rightmost lane. Either reduce that lane's X position or set the bubble's
`<foreignObject>` to extend past the lane.

### Pattern B — N-tier architecture reveal

Use for "show our 3-tier / 4-tier architecture" overview slides. Each tier is one row;
clicks reveal tiers in order, with connecting lines drawing in between and packets
flowing along them once everything is in.

- One labelled position per tier in `createTimeline`: `'s2'`, `'s3'`, …
- `syncToClicks(c)` does `tl.seek(tl.duration * 0.55)` for `c=1`, etc.
- Connecting paths use the stroke-draw pattern (gotcha 5)
- Floating chips for each tier ("1 Frontend", "2 BFF + Orchestrator", "3 Validation")
  use white translucent backgrounds with backdrop-blur and live in a flat HTML class
  (gotcha 4)
- Packet circles (`<circle class="packet">`) loop along the connectors with
  `loop: true, delay: stagger(280)` once all tiers are in

---

## Checklist when building a new animated SVG component

- [ ] Component takes `:clicks` prop and `watch`es it
- [ ] `setInitialState()` hides every animated element (and primes path dash offsets)
- [ ] Two `requestAnimationFrame` waits before measuring `getTotalLength()`
- [ ] Every `<g>` that anime.js targets is **double-wrapped** with positioning outside
- [ ] Stroke-draw paths use `opacity` to hide the marker (not just dash state)
- [ ] HTML labels are either inside `<foreignObject>` (for SVG-aligned bubbles) or
      have flat selectors (for floating chips)
- [ ] Pulse / looping animations live outside the timeline in their own `animate()`
- [ ] `onBeforeUnmount` pauses everything and nulls refs
- [ ] Wrapper has `position: relative`; SVG uses `position: absolute; inset: 0`
- [ ] Labels and chips have `z-index: 2` if they need to sit on top of SVG content
- [ ] Reverse navigation (`$clicks` decreases) rolls steps back, doesn't leave artifacts

---

## Worked examples in production

These two components live in
`docs/ppts/components/` of the BCP KYC platform deck and exercise every pattern above:

- `story-sequence.vue` — 10-step Cliente · Asesor · Agente IA sequence diagram with
  HTML bubbles via `<foreignObject>`, double-wrapped numbered badges, pulse ring on
  the agent, and per-step `animate()` for clean reverse navigation.
- `architecture-tiers-animated.vue` — 3-tier architecture hero (Frontend / BFF + MCP /
  Validation MCP + Workers) with stroke-drawn connectors, staggered card reveals,
  floating chip labels with progressive fade-in, and looping data packets.

Both use the **Microsoft Modern** style language (Selawik typography, brand colours,
glass cards) — see [`style-microsoft-modern`](style-microsoft-modern.md) for the
visual primitives.
