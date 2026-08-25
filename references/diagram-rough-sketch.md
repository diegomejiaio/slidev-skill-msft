---
name: rough-sketch
description: Hand-drawn architecture diagrams with rough.js, click-staged and resize-safe
---

# Hand-Drawn Diagrams (rough.js)

Full sketchy diagrams — boxes, arrows, arcs, filled shapes — that look drawn by
hand on paper. Different from [`animation-rough-marker`](animation-rough-marker.md),
which uses **rough-notation** to annotate existing text. This uses **rough.js**
itself to draw the whole graphic.

Use it when a Mermaid/PlantUML diagram feels too corporate and you want the
"napkin sketch" register: early-stage architecture, mental models, metaphors.

```bash
npm i roughjs
```

## The core pattern

Three layers, always:

```
<div ref="wrap">          ← measured container, position: relative
  <svg ref="overlay" />   ← rough.js draws here, position: absolute, inset 0
  <div class="box">…</div> ← HTML labels absolutely positioned ON TOP
</div>
```

**Labels are HTML `<div>`, never SVG `<text>`.** SVG text can't use `clamp()`,
flexbox, icon components, or CSS variables. Keeping labels in HTML means the
sketch layer stays purely geometric and the typography stays fully CSS-driven.

Geometry is declared in **percentages** of the container, converted to px at
draw time. The diagram then scales identically on a laptop and a projector.

## Base component

Copy this and replace the `boxes` / `arrows` data:

```vue
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick, markRaw } from 'vue'
import rough from 'roughjs'

const props = withDefaults(defineProps<{ stage?: number }>(), { stage: 0 })

const wrap = ref<HTMLElement | null>(null)
const overlay = ref<SVGSVGElement | null>(null)

type Kind = 'input' | 'core' | 'tool' | 'output'
type Box = { id: string; l: number; t: number; w: number; h: number; label: string; kind: Kind; icon?: any }

// l/t/w/h are PERCENTAGES of the wrapper — never px.
const boxes: Box[] = [
  { id: 'in',   l: 1,  t: 10, w: 15, h: 14, label: 'Input',   kind: 'input' },
  { id: 'core', l: 40, t: 5,  w: 20, h: 18, label: 'Core',    kind: 'core' },
  { id: 'out',  l: 84, t: 10, w: 15, h: 14, label: 'Output',  kind: 'output' },
  { id: 't1',   l: 30, t: 50, w: 16, h: 14, label: 'Tool A',  kind: 'tool' },
  { id: 't2',   l: 54, t: 50, w: 16, h: 14, label: 'Tool B',  kind: 'tool' },
]
const arrows: [string, string][] = [['in', 'core'], ['core', 'out']]

// Which click reveals which kind.
const STAGE: Record<Kind, number> = { input: 1, core: 2, tool: 3, output: 4 }
const shown = (k: Kind) => props.stage >= STAGE[k]

const INK = '#2B2620', ACCENT = '#476BFF', GREEN = '#1B7A55', AMBER = '#D9930A', DIM = '#B8AEA0'

function draw() {
  const svg = overlay.value, cont = wrap.value
  if (!svg || !cont) return
  const W = cont.clientWidth, H = cont.clientHeight
  if (!W || !H) return                        // container not laid out yet

  svg.setAttribute('viewBox', `0 0 ${W} ${H}`)
  while (svg.firstChild) svg.removeChild(svg.firstChild)   // full redraw
  const rc = rough.svg(svg)

  const px = (b: Box) => ({ x: (b.l/100)*W, y: (b.t/100)*H, w: (b.w/100)*W, h: (b.h/100)*H })
  const at = (id: string) => px(boxes.find(b => b.id === id)!)

  const strokeFor = (k: Kind) =>
    k === 'core' ? ACCENT : k === 'output' ? GREEN : k === 'input' ? AMBER : INK

  boxes.forEach(b => {
    if (!shown(b.kind)) return
    const p = px(b)
    svg.appendChild(rc.rectangle(p.x, p.y, p.w, p.h, {
      roughness: 1.6, bowing: 1.2, strokeWidth: 2, stroke: strokeFor(b.kind),
    }))
  })

  // rough.js has no arrowheads — build them from two short lines at ±0.4 rad.
  const arrow = (x1: number, y1: number, x2: number, y2: number, color: string) => {
    svg.appendChild(rc.line(x1, y1, x2, y2, { roughness: 1.3, strokeWidth: 2, stroke: color }))
    const a = Math.atan2(y2 - y1, x2 - x1), L = 10
    const head = { roughness: 1, strokeWidth: 2, stroke: color }
    svg.appendChild(rc.line(x2, y2, x2 - L*Math.cos(a - 0.4), y2 - L*Math.sin(a - 0.4), head))
    svg.appendChild(rc.line(x2, y2, x2 - L*Math.cos(a + 0.4), y2 - L*Math.sin(a + 0.4), head))
  }

  arrows.forEach(([from, to]) => {
    const target = boxes.find(b => b.id === to)!
    if (!shown(target.kind)) return           // don't draw into an invisible box
    const a = at(from), b = at(to)
    arrow(a.x + a.w, a.y + a.h/2, b.x, b.y + b.h/2, strokeFor(target.kind))
  })

  if (shown('tool')) {                        // fan from core down to each tool
    const c = at('core')
    const fanX = c.x + c.w/2, fanY = c.y + c.h
    boxes.filter(b => b.kind === 'tool')
      .forEach(t => { const p = px(t); arrow(fanX, fanY, p.x + p.w/2, p.y, INK) })
  }
}

let ro: ResizeObserver
onMounted(() => {
  draw()
  ro = new ResizeObserver(() => draw())
  if (wrap.value) ro.observe(wrap.value)
})
onUnmounted(() => ro?.disconnect())
watch(() => props.stage, () => nextTick(draw))

const styleOf = (b: Box) => ({ left: b.l + '%', top: b.t + '%', width: b.w + '%', height: b.h + '%' })
</script>

<template>
  <div ref="wrap" class="wrap">
    <svg ref="overlay" class="overlay" />
    <div
      v-for="b in boxes"
      v-show="shown(b.kind)"
      :key="b.id"
      class="box"
      :class="b.kind"
      :style="styleOf(b)"
    >
      <component :is="b.icon" v-if="b.icon" class="bicon" :size="20" />
      <span>{{ b.label }}</span>
    </div>
  </div>
</template>

<style scoped>
.wrap { position: relative; width: 100%; height: 380px; }
.overlay {
  position: absolute; inset: 0; width: 100%; height: 100%;
  pointer-events: none;               /* clicks pass through to the slide */
}
.box {
  position: absolute;
  display: flex; align-items: center; justify-content: center; gap: 0.35rem;
  font-family: 'Kalam', cursive; font-weight: 700;
  text-align: center; line-height: 1.02; padding: 0 0.2rem;
  color: var(--ink);
}
.box.input  { color: #7A5200; font-size: clamp(0.62rem, 1.1vw, 0.92rem); }
.box.tool   { color: #2B2620; font-size: clamp(0.62rem, 1.1vw, 0.92rem); flex-direction: column; }
.box.core   { color: #1B2E8A; font-size: 1.4rem; }
.box.output { color: #12563B; font-size: clamp(0.7rem, 1.1vw, 0.95rem); }
</style>
```

Drive it from a slide with the click count:

```md
---
clicks: 4
---

# Architecture

<ArchSketch :stage="$clicks" />
```

## rough.js options that matter

| Option | Range that reads as "hand-drawn" | Notes |
|---|---|---|
| `roughness` | `1.3`–`2.2` | Wobble amount. `0` = clean vector. Above `2.5` looks broken, not sketchy. |
| `bowing` | `0.8`–`1.4` | How much straight lines bow outward. |
| `strokeWidth` | `1.4`–`2.4` | Use `1.4` for secondary/hint connectors, `2` for primary. |
| `fillStyle` | `'solid'` \| `'hachure'` | `'hachure'` (default) is the crosshatch look; `'solid'` for large areas like roads or ponds. |
| `fill` | any colour | Combine with `fillStyle: 'solid'` for flat shapes with wobbly outlines. |
| `seed` | integer | Fixes the randomness — see below. |

Shape methods: `rc.rectangle(x,y,w,h,o)`, `rc.line(x1,y1,x2,y2,o)`,
`rc.circle(cx,cy,d,o)`, `rc.ellipse(cx,cy,w,h,o)`, `rc.polygon(points,o)`,
`rc.path(svgPathString,o)`. Each **returns** an SVG node you must
`svg.appendChild(...)` yourself.

## Curved connectors with `rc.path`

When a row of items is horizontally tight, loop the connector **below** them
instead of squeezing it between. An SVG arc with sweep-flag `0` bows downward:

```ts
const rad = (x2 - x1) / 2
const d = `M ${x1} 0 A ${rad} ${rad} 0 0 0 ${x2} 0`
svg.appendChild(rc.path(d, { roughness: 1.4, bowing: 1, strokeWidth: 2, stroke: INK }))
// tangent at the far end points straight up, so the arrowhead is two fixed lines
svg.appendChild(rc.line(x2, 0, x2 - 6, 11, { roughness: 1, strokeWidth: 2, stroke: INK }))
svg.appendChild(rc.line(x2, 0, x2 + 6, 11, { roughness: 1, strokeWidth: 2, stroke: INK }))
// label the arc at its lowest point
labels.push({ x: (x1 + x2) / 2, y: rad, text: '+ trust' })
```

## Pitfalls

**Slidev's `transform: scale()` corrupts DOM measurements.** If you position
connectors by measuring real elements (rather than declaring percentages),
`getBoundingClientRect()` returns *scaled* screen pixels while your SVG
viewBox is in local pixels. Divide the scale back out:

```ts
const base = root.getBoundingClientRect()
const s = base.width / root.offsetWidth || 1      // the slide's scale factor
const centerX = (el.getBoundingClientRect().left + w/2 - base.left) / s
```

Without this, arcs land correctly at 100% zoom and drift everywhere else.

**Redraw, don't patch.** rough.js emits static SVG nodes with baked-in
randomness. On every resize or stage change, clear the SVG
(`while (svg.firstChild) svg.removeChild(svg.firstChild)`) and redraw. Trying to
mutate existing nodes fights the library.

**Guard against a zero-size container.** `draw()` can fire before layout; bail
on `if (!W || !H) return` and let the `ResizeObserver` call it again.

**Randomness re-rolls on every draw.** Decorative elements will visibly jump on
each resize. Either pass a fixed `seed` per shape, or generate positions from a
seeded PRNG:

```ts
const rng = (seed: number) => () => (seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296
const rand = rng(42)
const trees = Array.from({ length: 12 }, () => ({ x: rand() * W, y: rand() * H }))
```

**`markRaw()` your icon components.** Storing a Vue component inside a reactive
data array makes Vue try to make the component definition itself reactive.
`icon: markRaw(Bell)` avoids the warning and the overhead.

**`pointer-events: none` on the overlay**, or the SVG swallows the clicks that
advance the slide.

**Watch with `nextTick`.** `watch(() => props.stage, () => nextTick(draw))` —
without it you redraw before the `v-show` labels have updated.

## The look, beyond rough.js

Wobbly geometry alone still reads as corporate if the typography and palette
don't follow:

```css
@import url('https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&display=swap');

:root {
  --bg:      #FAF8F4;   /* warm cream — never pure white */
  --ink:     #2B2620;   /* warm near-black — never pure black */
  --ink-dim: #857B6E;   /* muted, for secondary connectors and labels */
}

.font-hand { font-family: 'Kalam', cursive; }
```

Three rules:

1. **Labels inside sketches use a handwriting font** (Kalam, Caveat, Patrick
   Hand). Body copy and headings stay in your normal typeface — mixing the two
   is what makes it look intentional rather than themed.
2. **Warm off-white background, warm near-black ink.** Pure `#fff`/`#000` kills
   the paper illusion instantly.
3. **Colour carries meaning, not decoration.** One hue per role (input / core /
   output), applied to both the rough stroke and its HTML label.

No paper texture image and no CSS wobble animation are needed — the effect is
entirely rough.js geometry plus the handwriting font.

## When not to use it

- Diagrams the audience must read precisely (sequence diagrams with exact
  timings, ER models) — use [`diagram-mermaid`](diagram-mermaid.md).
- Formal / executive decks — see
  [`style-microsoft-modern`](style-microsoft-modern.md).
- Just emphasising text — use [`animation-rough-marker`](animation-rough-marker.md).

## Credits

Patterns adapted from
[`bronto-community/ai-sre-talk`](https://github.com/bronto-community/ai-sre-talk)
by Severin Neumann, whose code is MIT-licensed (`LICENSE-CODE`). Live deck:
<https://ai-sre-talk.vercel.app/>.
