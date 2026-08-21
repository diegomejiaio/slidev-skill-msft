# Microsoft Modern Style for Slidev

A complete, opinionated, light-theme style for Slidev that produces decks that look like
Microsoft's "Modern" / Fluent design language — animated brand-color swoosh, paper grain,
glass cards with accent-tinted borders, and Selawik (Microsoft's open-source Segoe UI
substitute) typography that renders the same on every OS.

Use it for: Microsoft-facing customer presentations, internal MSFT decks, partner / ISV
talks where the deck should *feel* like an MS keynote without using a heavy MS-internal
template.

---

## What it looks like

- **Light "paper" canvas** (#F8F7F6 → #EDEBEA gradient) with two stacked SVG noise layers
  for visible grain — feels like printed Microsoft collateral, not a default Slidev light theme.
- **Animated corner swoosh**: 3 morphing polygons in MS brand colors (orange → magenta →
  blue / yellow accent) that re-shape per slide. A slower **echo** layer behind them
  creates a "trail" so the swoosh never fully disappears during slide transitions.
- **Glass cards** (`rgba(255,255,255,0.6)` + `backdrop-filter: blur(12px)`) with **accent-tinted
  borders** — each variant exposes its accent color through a CSS custom property so border,
  shadow halo and icon all use the same color from a single source.
- **Selawik typography** — self-hosted, metric-compatible substitute for Segoe UI. No platform
  drift between macOS / Windows / Linux.
- **Microsoft chrome**: 4-square logo + wordmark top-left, breadcrumb top-right, copyright
  bottom-left — all via `global-top.vue`.

---

## File anatomy

```
my-deck/
├── slides.md
├── package.json
├── style.css                    ← tokens, typography, cards, transitions
├── uno.config.ts                ← wires Selawik, icons, safelist
├── global-top.vue               ← MS logo, breadcrumb, copyright
├── global-bottom.vue            ← swoosh + grain + canvas (fixed-position)
├── run.sh                       ← restart helper (kill :3030 → relaunch)
└── public/
    └── fonts/
        ├── Selawik-Light.ttf
        ├── Selawik-Semilight.ttf
        ├── Selawik-Regular.ttf
        ├── Selawik-Semibold.ttf
        └── Selawik-Bold.ttf
```

---

## Bootstrap

### 1 · Create the project

```bash
pnpm create slidev my-deck
cd my-deck
pnpm add -D @iconify-json/carbon seedrandom @types/seedrandom
pnpm add -D playwright-chromium   # only if you need PDF/PPTX export
```

### 2 · Download Selawik (required — typography won't render correctly without it)

Selawik is Microsoft's open-source, OFL-licensed, **metric-compatible** substitute for
Segoe UI. Same widths everywhere → no layout drift between platforms. Source:
[github.com/microsoft/Selawik](https://github.com/microsoft/Selawik).

```bash
mkdir -p public/fonts
BASE="https://github.com/microsoft/Selawik/raw/master/fonts/TTF"
for w in Light Semilight Regular Semibold Bold; do
  curl -fsSL -o "public/fonts/Selawik-${w}.ttf" "${BASE}/Selawik-${w}.ttf"
done
ls -la public/fonts/   # should show 5 .ttf files (~1.5MB total)
```

> ⚠️ Selawik only ships **5 weights** (300 / 350 / 400 / 600 / 700) — no italics, no Black.
> Designs that need italics should fall back to the system stack via `font-style: italic`.

### 3 · Drop the four config files (next sections)

### 4 · Restart and verify

```bash
chmod +x run.sh
./run.sh
```

Open `http://localhost:3030`. **Verify**: swoosh visible bottom-right, grain texture
visible (not flat), title font renders (no FOUT to Times), MS logo top-left.

> Adding `public/fonts/` or editing `uno.config.ts` requires a **full server restart** —
> Slidev's HMR won't pick those up. Pressing `r` in the terminal only re-evaluates
> slides.md and CSS.

---

## File: `style.css`

```css
/* =========================================================================
   Microsoft Modern theme for Slidev
   ========================================================================= */

/* ----- Selawik (Microsoft's open-source Segoe UI substitute) ----- */
@font-face { font-family: 'Selawik'; src: url('/fonts/Selawik-Light.ttf')     format('truetype'); font-weight: 300; font-display: swap; }
@font-face { font-family: 'Selawik'; src: url('/fonts/Selawik-Semilight.ttf') format('truetype'); font-weight: 350; font-display: swap; }
@font-face { font-family: 'Selawik'; src: url('/fonts/Selawik-Regular.ttf')   format('truetype'); font-weight: 400; font-display: swap; }
@font-face { font-family: 'Selawik'; src: url('/fonts/Selawik-Semibold.ttf')  format('truetype'); font-weight: 600; font-display: swap; }
@font-face { font-family: 'Selawik'; src: url('/fonts/Selawik-Bold.ttf')      format('truetype'); font-weight: 700; font-display: swap; }

:root {
  /* Microsoft Fluent palette */
  --ms-bg:        #F3F2F1;
  --ms-bg-soft:   #FAFAFA;
  --ms-ink:       #201F1E;
  --ms-ink-soft:  #605E5C;
  --ms-line:      #E1DFDD;
  --ms-card-bg:   #FFFFFF;

  --ms-blue:      #0078D4;   /* primary accent */
  --ms-blue-deep: #004578;
  --ms-cyan:      #00A4EF;   /* logo cyan */
  --ms-purple:    #7160E8;
  --ms-magenta:   #E3008C;
  --ms-orange:    #F25022;   /* logo orange */
  --ms-amber:     #FFB900;   /* logo amber */
  --ms-green:     #7FBA00;   /* logo green */
  --ms-teal:      #008272;

  --slidev-code-padding: 8px 10px;
  --slidev-code-background: #1F1F1F !important;
}

/* ----- Slide layer must be transparent -----
   Canvas + grain + swoosh live in global-bottom.vue (position: fixed) so they
   persist across transitions. If .slidev-layout has a background, the swoosh
   disappears during fade-out. */
.slidev-layout {
  background: transparent !important;
  color: var(--ms-ink);
  font-family: 'Selawik', 'Segoe UI', system-ui, -apple-system, sans-serif;
  padding-top: 64px !important;     /* room for top chrome */
  padding-bottom: 56px !important;  /* room for copyright */
}
#slide-content,
.slidev-page,
.slidev-slide-container {
  background: transparent !important;
}

.slidev-layout h1,
.slidev-layout h2,
.slidev-layout h3 { color: var(--ms-ink); }

.slidev-layout h1 { font-weight: 600; letter-spacing: -0.02em; line-height: 1.05; }
.slidev-layout h2,
.slidev-layout h3,
.slidev-layout h6 {
  text-transform: initial !important;
  font-weight: 500 !important;
  letter-spacing: 0 !important;
  color: var(--ms-ink);
}
.slidev-layout p,
.slidev-layout li,
.slidev-layout span { color: var(--ms-ink); }

/* Eyebrow label above big titles ("ASK #1", "MICROSOFT × KPMG", etc.) */
.ask-eyebrow {
  font-size: 0.72rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ms-ink-soft);
  margin-bottom: 0.4rem;
  font-weight: 600;
}

/* Content-slide title — sibling of .ask-eyebrow.
   Use <div class="ask-title"> on content slides INSTEAD of <h2>. The
   .slidev-layout h2 cascade overrides Tailwind text-* utilities, so the
   only clean way to control content-title size without `!important` is to
   use a non-h element and hang the typography off this token. */
.ask-title {
  font-size: 1.55rem;
  line-height: 1.2;
  font-weight: 600;
  letter-spacing: -0.005em;
  color: var(--ms-ink);
  margin: 0 0 0.85rem 0;
}

/* Microsoft pill tag (used in MS keynote decks for "Azure AI Foundry", etc.) */
.ms-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  border-radius: 999px;
  background: #FFFFFF;
  border: 1px solid var(--ms-line);
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--ms-ink);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

/* ===== Cards =====
   Glass cards over the swoosh. Accent color is exposed via CSS custom props
   (--card-accent + --card-accent-rgb) so border + halo + icon all use the
   same color from one source. The chrome (border + halo) carries the accent
   in a *whisper* — the icon does the loud talking. This keeps multi-card
   slides from looking visually noisy when several variants share the screen. */
.card {
  --card-accent: var(--ms-blue);
  --card-accent-rgb: 0, 120, 212;
  background: rgba(255, 255, 255, 0.6);
  border: 1.5px solid rgba(var(--card-accent-rgb), 0.22);
  border-radius: 12px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  /* Neutral base shadow + a faint accent halo. The icon carries the category
     signal, not the chrome. */
  box-shadow:
    0 4px 14px rgba(0, 0, 0, 0.04),
    0 0 0 1px rgba(var(--card-accent-rgb), 0.04);
  backdrop-filter: blur(12px) saturate(130%);
  -webkit-backdrop-filter: blur(12px) saturate(130%);
  transition:
    transform 250ms cubic-bezier(.2,.9,.3,1),
    box-shadow 250ms ease,
    background 250ms ease,
    border-color 250ms ease;
  position: relative;
  outline: none;   /* v-click adds tabindex; we replace native ring below */
}

.card:focus,
.card:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 3px rgba(var(--card-accent-rgb), 0.10),
    0 4px 14px rgba(0, 0, 0, 0.04);
}

.card:hover {
  background: rgba(255, 255, 255, 0.75);
  border-color: rgba(var(--card-accent-rgb), 0.4);
  transform: translateY(-2px);
  box-shadow:
    0 8px 22px rgba(0, 0, 0, 0.06),
    0 0 0 1px rgba(var(--card-accent-rgb), 0.07);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.85rem 1rem;
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--ms-ink);
  border-bottom: 1px solid rgba(32, 31, 30, 0.06);
  background: rgba(255, 255, 255, 0.35);
}

.card-body {
  padding: 1rem 1.1rem;
  font-size: 0.9rem;
  color: var(--ms-ink);
  line-height: 1.55;
  flex: 1;
}

.card-icon {
  font-size: 1.15rem;
  /* Muted by default — matches the breadcrumb / soft-ink color so the icon
     reads as a glyph, not a brand callout. The card border tint and the
     numbered label do the category signaling. Override per-instance with
     inline `style="color: var(--ms-blue)"` only when an icon is the visual
     hero of the slide (big section headers, cover pills, etc.). */
  color: var(--ms-ink-soft);
}

/* Color variants — only the border tint carries the accent.
   Header text and icons stay neutral for clean hierarchy. */
.card-blue    { --card-accent: var(--ms-blue);    --card-accent-rgb:   0, 120, 212; }
.card-amber   { --card-accent: var(--ms-amber);   --card-accent-rgb: 255, 185,   0; }
.card-green   { --card-accent: var(--ms-green);   --card-accent-rgb: 127, 186,   0; }
.card-purple  { --card-accent: var(--ms-purple);  --card-accent-rgb: 113,  96, 232; }
.card-magenta { --card-accent: var(--ms-magenta); --card-accent-rgb: 227,   0, 140; }
.card-orange  { --card-accent: var(--ms-orange);  --card-accent-rgb: 242,  80,  34; }

/* Compact variant for tight grids (cards next to a table, multiple cards
   stacked in a narrow column, etc). Pair with `.card` and color variant. */
.card-compact .card-header { padding: 0.6rem 0.8rem; font-size: 0.85rem; }
.card-compact .card-body   { padding: 0.65rem 0.8rem; font-size: 0.8rem; line-height: 1.45; }

/* Big number / gradient text (cover slides, section dividers) */
.ask-number-big {
  background: linear-gradient(135deg, var(--ms-blue) 0%, var(--ms-purple) 60%, var(--ms-magenta) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  font-size: 5rem;
  line-height: 1;
}

/* ===== Click transitions ===== */
.slidev-vclick-target {
  transition:
    opacity 500ms ease,
    transform 500ms cubic-bezier(.2,.9,.3,1),
    filter 200ms ease,
    color 300ms ease;
}
.slidev-vclick-hidden {
  opacity: 0;
  pointer-events: none;
  filter: blur(3px);
}

/* Slide-level fade-out (works with the global swoosh because layout is transparent) */
.fade-out-leave-active {
  transition:
    opacity calc(var(--slidev-transition-duration) * 0.6) ease-out,
    filter 200ms ease;
}
.fade-out-enter-active {
  transition:
    opacity calc(var(--slidev-transition-duration) * 0.8) ease-in,
    filter 200ms ease;
  transition-delay: calc(var(--slidev-transition-duration) * 0.6);
}
.fade-out-enter-from,
.fade-out-leave-to {
  opacity: 0;
  filter: blur(5px);
}

/* Code block on light theme */
.slidev-code {
  border: 1px solid var(--ms-line);
  border-radius: 8px;
  background: #1F1F1F !important;
}

/* Always-visible nav controls (light variant, readable on light bg) */
.nav-controls,
.slidev-controls { opacity: 1 !important; }
.nav-controls .slidev-icon-btn {
  color: var(--ms-ink) !important;
  background: rgba(255, 255, 255, 0.85) !important;
  border: 1px solid var(--ms-line) !important;
  border-radius: 6px !important;
  backdrop-filter: blur(6px);
}
.nav-controls .slidev-icon-btn:hover {
  color: var(--ms-blue) !important;
  background: #ffffff !important;
  border-color: var(--ms-blue) !important;
}
.slidev-page-no {
  opacity: 0.85 !important;
  background: rgba(255, 255, 255, 0.85);
  color: var(--ms-ink-soft) !important;
  padding: 2px 8px;
  border-radius: 6px;
  border: 1px solid var(--ms-line);
}

/* Hide the goto dialog when not active */
.fixed.right-5.-top-20 {
  visibility: hidden !important;
  pointer-events: none !important;
}
```

---

## File: `uno.config.ts`

```ts
// @ts-expect-error - missing types for the slidev uno config export
import config from '@slidev/client/uno.config'
import { mergeConfigs, presetAttributify, presetIcons, presetWebFonts, presetWind3 } from 'unocss'

export default mergeConfigs([
  config,
  {
    safelist: [
      // animation-delay utilities used by staggered v-clicks
      ...Array.from({ length: 30 }, (_, i) => `delay-${(i + 1) * 100}`),
      'animate-pulse',
    ],
    theme: {
      fontFamily: {
        sans: "'Selawik', 'Segoe UI', system-ui, -apple-system, sans-serif",
        mono: "'Cascadia Code', ui-monospace, SFMono-Regular, Menlo, monospace",
      },
    },
    presets: [
      presetWind3({ dark: 'class' }),
      presetAttributify(),
      presetIcons({
        prefix: 'i-',
        extraProperties: { display: 'inline-block', 'vertical-align': 'middle' },
        warn: true,
      }),
      presetWebFonts({
        // CRITICAL: 'none' tells UnoCSS to use the family name as-is and NOT
        // try to fetch from Google Fonts (Selawik isn't there). Self-hosted
        // via @font-face in style.css.
        provider: 'none',
        fonts: {
          sans: [{ name: 'Selawik' }, { name: 'Segoe UI' }],
          mono: [{ name: 'Cascadia Code' }],
        },
      }),
    ],
  },
])
```

---

## File: `global-top.vue` (Microsoft chrome)

The 4-square logo can be rendered in two variants:

- **Monochrome** (recommended for sober / customer-facing / partner decks) — the 4
  squares share `currentColor`, inheriting from the wrapper. The shape stays iconic
  but the chrome reads as restrained, letting the deck content carry the brand color.
- **4-color** (the canonical Microsoft brand mark) — for product launches, marketing
  decks, anything that needs the full brand expression.

```vue
<script setup lang="ts">
import { useNav } from '@slidev/client'
import { computed } from 'vue'

const { currentSlideRoute } = useNav()
const isCover = computed(() => currentSlideRoute.value?.no === 1)
</script>

<template>
  <div class="ms-chrome pointer-events-none" aria-hidden="true">
    <!-- Microsoft 4-square logo (monochrome — inherits color from .ms-chrome).
         Swap the four `fill="currentColor"` for `#F25022 / #7FBA00 / #00A4EF / #FFB900`
         (orange / green / cyan / yellow, in that order) for the 4-color version. -->
    <div class="ms-logo">
      <svg viewBox="0 0 23 23" width="22" height="22">
        <rect x="1"  y="1"  width="10" height="10" fill="currentColor" />
        <rect x="12" y="1"  width="10" height="10" fill="currentColor" />
        <rect x="1"  y="12" width="10" height="10" fill="currentColor" />
        <rect x="12" y="12" width="10" height="10" fill="currentColor" />
      </svg>
      <span class="ms-wordmark">Microsoft</span>
    </div>

    <div v-if="!isCover" class="ms-crumb">
      <!-- EDIT THIS — your deck's breadcrumb -->
      My Deck · Subtitle
    </div>

    <div class="ms-copy">
      © 2026 Microsoft Corporation. All rights reserved.
    </div>
  </div>
</template>

<style scoped>
.ms-chrome {
  position: absolute;
  inset: 0;
  z-index: 5;
  font-family: 'Selawik', 'Segoe UI', system-ui, sans-serif;
  /* Single ink color flows into the monochrome logo via currentColor. */
  color: #323130;
}
.ms-logo {
  position: absolute;
  top: 18px;
  left: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.ms-wordmark {
  font-size: 14px;
  font-weight: 600;
  color: #323130;
}
.ms-crumb {
  position: absolute;
  top: 22px;
  right: 24px;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: #605E5C;
}
.ms-copy {
  position: absolute;
  bottom: 14px;
  left: 24px;
  font-size: 10px;
  color: #8A8886;
}
</style>
```

### When to use which logo variant

| Variant | Best for | Implementation |
|---|---|---|
| **Monochrome** (default in this recipe) | Customer-facing decks, partner / advisory presentations, internal working sessions, anything where the deck content already carries brand color (swoosh, accent cards). The chrome stays out of the way. | Four `fill="currentColor"` — color comes from `.ms-chrome { color: … }`. |
| **4-color** | Cover slides of major external announcements, brand-led marketing, deck templates where the logo is the visual hero. | Replace `currentColor` with `#F25022`, `#7FBA00`, `#00A4EF`, `#FFB900` in the four `<rect>` (top-left, top-right, bottom-left, bottom-right respectively). |

Some decks use **mixed** chrome — 4-color logo on the cover slide only, monochrome on
every internal slide. Achieve this with a `v-if="isCover"` switch around the two SVGs.

---

## File: `global-bottom.vue` (animated swoosh + grain)

This is the visual heart of the theme. Three morphing polygons in MS brand colors, each
re-shaped on every slide change via `seedrandom` (deterministic per slide). The **echo
layer** is a duplicate set with a slower 7s transition, sitting one z-index behind the
main 4s layer — this gives the "trail" feel so the swoosh never visually disappears
during fade-out.

```vue
<script setup lang="ts">
import { useNav } from '@slidev/client'
import seedrandom from 'seedrandom'
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'

/**
 * Per-slide frontmatter overrides:
 *   glow:        'left' | 'right' | 'top' | 'bottom' | 'full'
 *                | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center'
 *   glowOpacity: number   (default 0.55)
 *   glowHue:     number   (default 0 — degrees of hue-rotate)
 *   glowSeed:    string|false (default 'default'; false = random per render)
 */

const { currentSlideRoute } = useNav()

export type Range = [number, number]
export type Distribution =
  | 'full' | 'top' | 'bottom' | 'left' | 'right'
  | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'
  | 'center' | 'topmost'

const formatter = computed(() => (currentSlideRoute.value?.meta?.slide as any)?.frontmatter || {})
const distribution = computed(() => (formatter.value.glow || 'bottom-right') as Distribution)
const opacity = computed<number>(() => +(formatter.value.glowOpacity ?? 0.55))
const hue = computed<number>(() => +(formatter.value.glowHue || 0))
const seed = computed<string>(() =>
  (formatter.value.glowSeed === 'false' || formatter.value.glowSeed === false)
    ? Date.now().toString()
    : formatter.value.glowSeed || 'default',
)

// Smaller overflow = more contained swoosh. Bigger = dramatic spill across whole slide.
const overflow = 0.15
const disturb = 0.15
const disturbChance = 0.3

function distributionToLimits(dist: Distribution) {
  const min = -0.2
  const max = 1.2
  let x: Range = [min, max]
  let y: Range = [min, max]
  const intersect = (a: Range, b: Range): Range => [Math.max(a[0], b[0]), Math.min(a[1], b[1])]
  for (const limit of dist.split('-')) {
    switch (limit) {
      case 'topmost': y = intersect(y, [-0.5, 0]); break
      case 'top':     y = intersect(y, [min, 0.6]); break
      case 'bottom':  y = intersect(y, [0.4, max]); break
      case 'left':    x = intersect(x, [min, 0.6]); break
      case 'right':   x = intersect(x, [0.4, max]); break
      case 'center':
        x = intersect(x, [0.25, 0.75])
        y = intersect(y, [0.25, 0.75])
        break
      case 'full':
        x = intersect(x, [0, 1])
        y = intersect(y, [0, 1])
        break
    }
  }
  return { x, y }
}

function distance2([x1, y1]: Range, [x2, y2]: Range) {
  return (x2 - x1) ** 2 + (y2 - y1) ** 2
}

function usePoly(number = 16) {
  function getPoints(): Range[] {
    const limits = distributionToLimits(distribution.value)
    const rng = seedrandom(`${seed.value}-${currentSlideRoute.value?.no ?? 0}`)
    const randomBetween = ([a, b]: Range) => rng() * (b - a) + a
    const applyOverflow = (random: number, overflow: number) => {
      random = random * (1 + overflow * 2) - overflow
      return rng() < disturbChance ? random + (rng() - 0.5) * disturb : random
    }
    return Array.from({ length: number }).fill(0).map(() => [
      applyOverflow(randomBetween(limits.x), overflow),
      applyOverflow(randomBetween(limits.y), overflow),
    ] as Range)
  }

  const points = ref<Range[]>(getPoints())
  const poly = computed(() => points.value.map(([x, y]) => `${x * 100}% ${y * 100}%`).join(', '))

  function jumpPoints() {
    const newPoints = new Set(getPoints())
    points.value = points.value.map((o) => {
      let minDistance = Number.POSITIVE_INFINITY
      let closest: Range | undefined
      for (const n of newPoints) {
        const d = distance2(o, n)
        if (d < minDistance) { minDistance = d; closest = n }
      }
      if (closest) newPoints.delete(closest)
      return closest ?? o
    })
  }

  watch(currentSlideRoute, () => jumpPoints())
  return poly
}

const poly1 = usePoly(10)
const poly2 = usePoly(6)
const poly3 = usePoly(3)

// Drop focus on click so keyboard arrows keep navigating the deck
function handleClick(e: MouseEvent) {
  const t = (e.target as HTMLElement | null)?.closest('button, a, [tabindex]') as HTMLElement | null
  if (t) setTimeout(() => t.blur(), 80)
}
onMounted(() => document.addEventListener('click', handleClick, true))
onUnmounted(() => document.removeEventListener('click', handleClick, true))
</script>

<template>
  <div>
    <!-- Canvas color (fixed-position so it persists across transitions) -->
    <div class="canvas pointer-events-none" aria-hidden="true" />

    <!-- Echo layer: 7s transition, behind the main one -->
    <div
      class="bg bg-echo transform-gpu overflow-hidden pointer-events-none"
      :style="{ filter: `blur(60px) hue-rotate(${hue}deg)` }"
      aria-hidden="true"
    >
      <div class="clip bg-gradient-to-br from-[#F25022] via-[#E3008C] to-[#7160E8]"
           :style="{ 'clip-path': `polygon(${poly1})`, 'opacity': opacity * 0.45 }" />
      <div class="clip bg-gradient-to-tr from-[#0078D4] via-[#7160E8] to-[#E3008C]"
           :style="{ 'clip-path': `polygon(${poly2})`, 'opacity': opacity * 0.4 }" />
    </div>

    <!-- Main swoosh: 4s transition -->
    <div
      class="bg bg-main transform-gpu overflow-hidden pointer-events-none"
      :style="{ filter: `blur(48px) hue-rotate(${hue}deg)` }"
      aria-hidden="true"
    >
      <div class="clip bg-gradient-to-br from-[#F25022] via-[#E3008C] to-[#7160E8]"
           :style="{ 'clip-path': `polygon(${poly1})`, 'opacity': opacity }" />
      <div class="clip bg-gradient-to-tr from-[#0078D4] via-[#7160E8] to-[#E3008C]"
           :style="{ 'clip-path': `polygon(${poly2})`, 'opacity': opacity * 0.85 }" />
      <div class="clip bg-gradient-to-r from-[#FFB900] to-[#F25022]"
           :style="{ 'clip-path': `polygon(${poly3})`, 'opacity': 0.35 }" />
    </div>

    <!-- Two-layer paper grain -->
    <div class="grain grain-fine pointer-events-none" aria-hidden="true" />
    <div class="grain grain-coarse pointer-events-none" aria-hidden="true" />
  </div>
</template>

<style scoped>
.canvas {
  position: fixed;
  inset: 0;
  z-index: -20;
  background: linear-gradient(135deg, #F8F7F6 0%, #EDEBEA 100%);
}
.bg, .clip { transition: all 4s cubic-bezier(.4, 0, .2, 1); }
.bg { position: fixed; inset: 0; z-index: -10; }
.bg-echo { z-index: -11; transition: all 7s cubic-bezier(.4, 0, .2, 1); }
.bg-echo .clip { transition: all 7s cubic-bezier(.4, 0, .2, 1); }
.clip { clip-path: circle(75%); aspect-ratio: 16 / 9; position: absolute; inset: 0; }

.grain { position: fixed; inset: 0; z-index: -8; }
.grain-fine {
  opacity: 0.5;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='1.6' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.32 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
}
.grain-coarse {
  opacity: 0.28;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.95' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.45 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
}
</style>
```

---

## File: `slides.md` headmatter

```yaml
---
theme: default
highlighter: shiki
css: unocss
colorSchema: light
transition: fade-out          # works because .slidev-layout is transparent
title: My Deck Title
exportFilename: my-deck
lineNumbers: false
mdc: true
clicks: 0
preload: false
glowSeed: 229                 # global default; per-slide can override
routerMode: hash
---
```

### Per-slide frontmatter (placement of the swoosh)

```md
---
title: 'My Slide'
glowSeed: 175                 # changes the polygon shape — pick anything
glow: bottom-left             # bottom-right | top-left | center | full | …
glowHue: 30                   # rotates all swoosh colors by N degrees
---
```

### Avoid `layout: center` for content-heavy slides

`layout: center` clips content vertically when it overflows. Use the **default** layout
(top-anchored) for any slide with multiple cards, chat mockups, or stacked sections. Only
use `center` for true title / cover / single-statement slides.

---

## File: `run.sh` (restart helper)

```bash
#!/usr/bin/env bash
# Restart the Slidev dev server on port 3030.
set -euo pipefail
PORT="${PORT:-3030}"
cd "$(dirname "$0")"
if pids="$(lsof -ti ":${PORT}" 2>/dev/null)"; then
  if [[ -n "${pids}" ]]; then
    echo "→ killing pid(s) on :${PORT}: ${pids}"
    kill ${pids} 2>/dev/null || true
    sleep 0.5
  fi
fi
echo "→ starting slidev on :${PORT}"
exec pnpm exec slidev --port "${PORT}"
```

```bash
chmod +x run.sh
./run.sh                 # default :3030
PORT=4000 ./run.sh       # override port
```

---

## Slide patterns

### Cover slide

```md
<div class="flex flex-col h-full justify-center px-12">

<div class="ask-eyebrow">Microsoft × Partner · Project Codename</div>

<h1 class="!text-7xl !leading-none mt-2">
  Big Title<br/>Goes Here
</h1>

<div class="text-xl mt-6 max-w-2xl" style="color: var(--ms-ink-soft)">
  One-line subtitle that frames the deck
</div>

<div class="flex gap-3 mt-10">
  <span class="ms-pill"><div class="i-carbon:user-multiple text-base" style="color: var(--ms-blue)" /> Topic 1</span>
  <span class="ms-pill"><div class="i-carbon:code text-base" style="color: var(--ms-orange)" /> Topic 2</span>
  <span class="ms-pill"><div class="i-carbon:chat text-base" style="color: var(--ms-teal)" /> Topic 3</span>
</div>

</div>
```

### Compact section header (icon + eyebrow + title in one row)

```md
<div
  v-click
  class="flex items-center gap-4 mb-5 transition duration-500 ease-in-out"
  :class="$clicks < 1 ? 'translate-x--6 opacity-0' : 'translate-x-0 opacity-100'"
>
  <div class="i-carbon:user-multiple" style="font-size:48px; color: var(--ms-blue)" />
  <div>
    <div class="ask-eyebrow">Section #1</div>
    <h1 class="!text-3xl !mt-0">Section title here</h1>
  </div>
</div>
```

### Card grid (3-up, staggered v-click reveal)

```md
<div class="grid grid-cols-3 gap-3">

<div
  v-click="2"
  class="card card-blue p-0 transition duration-500 ease-in-out"
  :class="$clicks < 2 ? 'translate-y-4 opacity-0' : 'translate-y-0 opacity-100'"
>
  <div class="px-4 py-3">
    <div class="i-carbon:network-3 text-2xl mb-2" style="color: var(--ms-blue)" />
    <div class="font-semibold text-sm">Card title</div>
    <div class="text-[11px] mt-1" style="color: var(--ms-ink-soft)">Short description</div>
  </div>
</div>

<!-- repeat for v-click="3", v-click="4" with different card-* variants -->

</div>
```

### Two-team / handshake strip

For "two parties working together" framing — vendor + customer, MSFT + partner, two teams:

```md
<div class="grid grid-cols-12 gap-3 items-stretch mb-5">
  <div class="col-span-5 card card-blue">
    <div class="px-4 py-3">
      <div class="text-[10px] uppercase tracking-wider font-semibold" style="color: var(--ms-blue)">Microsoft</div>
      <div class="font-semibold text-sm mb-0.5">Cross-Sell team</div>
      <div class="text-[11px]" style="color: var(--ms-ink-soft)">Building the SDK & integration</div>
    </div>
  </div>

  <div class="col-span-2 flex flex-col items-center justify-center text-center">
    <div class="i-carbon:arrows-horizontal text-2xl" style="color: var(--ms-ink-soft)" />
    <div class="text-[10px] mt-1 font-medium" style="color: var(--ms-ink-soft)">joint working<br/>session</div>
  </div>

  <div class="col-span-5 card card-purple">
    <div class="px-4 py-3">
      <div class="text-[10px] uppercase tracking-wider font-semibold" style="color: var(--ms-purple)">KPMG</div>
      <div class="font-semibold text-sm mb-0.5">Company Insight eng</div>
      <div class="text-[11px]" style="color: var(--ms-ink-soft)">Owners of the existing tool</div>
    </div>
  </div>
</div>
```

### Pill at the bottom (footnote-style takeaway)

```md
<div class="mt-5 flex items-center justify-center gap-2 text-sm" style="color: var(--ms-ink-soft)">
  <div class="i-carbon:idea text-base" style="color: var(--ms-amber)" />
  <span>A working session — <b>not a demo</b></span>
</div>
```

### Closing disclaimer slide (always include this)

A confidentiality / property disclaimer is **standard on every Microsoft deck shared
externally** — customer presentations, partner sessions, advisory work, anything that
contains MS confidential or customer-identifying material. Include it as the last slide.

Visual treatment: large light-weight "Disclaimer" heading, generous whitespace, body
text in `--ms-ink-soft`, **no swoosh** (set `glowOpacity: 0` in the slide frontmatter so
the canvas stays neutral).

```md
---
title: Disclaimer
layout: default
glowOpacity: 0          # turns off the swoosh for this slide
hideInToc: true         # don't show in the auto-generated table of contents
---

<div class="h-full flex flex-col px-12 py-8">

<h1 class="!text-6xl !font-light !mt-6"
    style="color: var(--ms-ink); letter-spacing: -0.01em">Disclaimer</h1>

<div class="flex-1 flex items-center max-w-3xl mt-12">
  <p class="text-base leading-relaxed"
     style="color: var(--ms-ink-soft); font-weight: 400">
    This presentation is the property of Microsoft and is shared with the intended
    recipient(s) for their exclusive use. Its contents are confidential and must not
    be distributed, reproduced, or referenced outside of Microsoft and the intended
    recipient organization without prior written consent. Unauthorized use, disclosure,
    or copying of any part of this material is strictly prohibited.
  </p>
</div>

</div>
```

> ⚠️ **Use your organization's approved disclaimer wording when one exists.** Many
> Microsoft business units, customer success teams, and legal organizations have a
> specific approved confidentiality statement. Get it from your manager or
> account / legal team and substitute it into the `<p>` above. The wording shown here
> is generic, functionally-equivalent placeholder language — not the official
> Microsoft template.

**When to include it:**

| Deck context | Disclaimer needed? |
|---|---|
| External customer / partner presentation | ✅ Always |
| Internal MS team meeting with confidential roadmap | ✅ Always |
| Conference / public talk where slides will be shared | ⚠️ Use a *different* disclaimer (typically attribution + "views are my own" rather than confidentiality) |
| Internal demo / open-source talk | ❌ Optional |

The `hideInToc: true` keeps it out of the table of contents (so navigation jumps land
on real content slides), and `glowOpacity: 0` removes the swoosh so the disclaimer reads
as restrained and serious — matching the legal-document tone.

### Inline chat / agent mockup

For illustrating real or hypothetical agent conversations (PII redactions, tool calls,
agent gaps). Use monospace blocks for tool calls, glass bubbles for User / Agent, and a
magenta-bordered annotation strip for the takeaway:

```md
<div class="card card-green">
  <div class="card-header" style="padding: 0.5rem 0.85rem">
    <div class="i-carbon:document text-sm" style="color: var(--ms-teal)" />
    <span class="font-mono text-[11px]">conversation-0142.json</span>
    <span class="ml-auto text-[9px] px-2 py-0.5 rounded-full"
          style="background: rgba(127,186,0,0.15); color: var(--ms-teal); border: 1px solid rgba(127,186,0,0.35)">PII REMOVED</span>
  </div>
  <div class="px-3 py-2.5 space-y-1.5 text-[11px]">

  <!-- User bubble -->
  <div class="flex gap-1.5">
    <div class="i-carbon:user-avatar text-sm flex-shrink-0 mt-0.5" style="color: var(--ms-blue)" />
    <div class="bg-white/70 px-2 py-1 rounded border" style="border-color: rgba(0,120,212,0.25)">
      <span class="text-[9px] uppercase tracking-wider mr-1.5" style="color: var(--ms-ink-soft)">User</span>
      What can we offer <span class="font-mono" style="background: rgba(227,0,140,0.1); padding: 0 4px; border-radius: 3px; color: var(--ms-magenta)">[CLIENT_47]</span>?
    </div>
  </div>

  <!-- Tool call (monospace, dashed border) -->
  <div class="flex gap-1.5 ml-5">
    <div class="i-carbon:tool-kit text-sm flex-shrink-0 mt-0.5" style="color: var(--ms-orange)" />
    <div class="font-mono px-2 py-1 rounded text-[10px]"
         style="background: rgba(32,31,30,0.04); border: 1px dashed rgba(32,31,30,0.15); color: var(--ms-ink-soft)">
      <span style="color: var(--ms-orange)">tool_call</span> · <span style="color: var(--ms-ink)">getClientHistory</span>(id="...")
    </div>
  </div>

  <!-- Agent bubble -->
  <div class="flex gap-1.5">
    <div class="i-carbon:bot text-sm flex-shrink-0 mt-0.5" style="color: var(--ms-teal)" />
    <div class="bg-white/70 px-2 py-1 rounded border" style="border-color: rgba(127,186,0,0.3)">
      <span class="text-[9px] uppercase tracking-wider mr-1.5" style="color: var(--ms-ink-soft)">Agent</span>
      Top 3: <b>Service A</b>, <b>Service B</b>, <b>Service C</b>.
    </div>
  </div>

  <!-- Takeaway annotation (left-bordered) -->
  <div class="flex gap-1.5 mt-1 px-2 py-1.5 rounded"
       style="background: rgba(227,0,140,0.06); border-left: 2px solid var(--ms-magenta)">
    <div class="i-carbon:warning-alt text-sm flex-shrink-0 mt-0.5" style="color: var(--ms-magenta)" />
    <div class="text-[10px]" style="color: var(--ms-ink-soft)">
      <b style="color: var(--ms-magenta)">Gap captured.</b> Real intent, no capability — exactly what we need.
    </div>
  </div>

  </div>
</div>
```

---

## Critical gotchas (the things you'd waste hours on otherwise)

### 1 · Slide layout MUST be transparent

If `.slidev-layout` has any background color, the swoosh **disappears during fade-out**
because the leaving slide covers `global-bottom`. Solution: keep the canvas + grain +
swoosh in `global-bottom.vue` with `position: fixed`, set
`.slidev-layout { background: transparent !important; }`.

### 2 · Echo polygon for transition trail

A single morphing polygon set fades visibly when slides change. The fix is two identical
polygon layers — main (4s transition, z-index -10) and **echo** (7s, z-index -11). The
slower echo is always behind, creating a "trail" that hides the visual gap.

### 3 · `presetWebFonts` must use `provider: 'none'` for self-hosted Selawik

Without it, UnoCSS tries to fetch Selawik from Google Fonts, fails silently, and the page
falls back to system fonts (San Francisco on Mac, Segoe UI on Windows — different metrics
on each). With `provider: 'none'`, UnoCSS only emits the family name and trusts your
`@font-face` declarations.

### 4 · `backdrop-filter` blur + `inset 0 1px 0 rgba(255,255,255,X)` = visible "lid"

At `blur(18px+)` combined with an inset white highlight on the top edge, glass cards
develop a visible white bar at the top edge on macOS. Fix: lower blur to `12px`,
remove the inset highlight, use a single `border` for the card edge instead.

### 5 · `v-click` adds tabindex → native focus ring

When you use `v-click` on a `<div>`, Vue/Slidev sets `tabindex` so it can be focused.
Browsers then show their native focus ring (a thick blue outline) on click. Fix:

```css
.card { outline: none; }
.card:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(var(--card-accent-rgb), 0.18), …;
}
```

Plus add a click handler in `global-bottom.vue` that `.blur()`s any `[tabindex]` after
80ms — keeps keyboard arrow navigation working.

### 6 · `layout: center` clips overflowing content

It vertically centers the slide content. If your content is taller than the slide,
**both top and bottom get clipped**. Use the default (top-anchored) layout for any
slide with multiple cards, chat mockups, or stacked sections.

### 7 · Server restart needed for `uno.config.ts` and `public/`

Slidev HMR re-evaluates `slides.md` and `style.css` (press `r` in the terminal — fast).
But changes to `uno.config.ts`, `package.json`, `global-*.vue`, or files in `public/`
require a **full restart** of the dev server. Use `./run.sh` (kills the port, relaunches).

### 8 · Single source of truth for card accent color

Don't duplicate the accent color across border / shadow / icon / left-bar — you'll fight
yourself when adding variants. Use CSS custom props:

```css
.card { --card-accent-rgb: 0, 120, 212; }
.card { border-color: rgba(var(--card-accent-rgb), 0.4); }
.card { box-shadow: 0 8px 24px rgba(var(--card-accent-rgb), 0.08); }
.card-purple { --card-accent-rgb: 113, 96, 232; }   /* one line per variant */
```

### 9 · Selawik has no italics or Black weight

Only 5 weights: 300, 350, 400, 600, 700. No italics. If your design needs italics, they
fall back to whatever the system has — usually fine, but verify on Windows where the
fallback is Segoe UI Italic.

### 10 · Carbon icon names that *seem* obvious aren't always available

`i-carbon:user-shield` doesn't exist; `i-carbon:password` does. Always test new icons
visually — if they don't render, swap them. Reliable fallbacks: `password`,
`fingerprint-recognition`, `user-avatar`, `network-3`, `plug`, `tool-kit`, `bot`,
`document`, `checkmark-outline`, `warning-alt`, `idea`, `arrows-horizontal`, `building`.

### 11 · Tailwind `text-*` utilities can't shrink `<h2>` / `<h3>` without `!important`

**Symptom**: you write `<h2 class="text-xl">My title</h2>` and it still renders huge.
You bump it to `text-base`, still huge. You add `!important` (`!text-xl`) and it finally
sticks — but you've started fighting the cascade.

**Cause**: this theme's `style.css` has a `.slidev-layout h2 { font-weight: 500 !important; … }`
block (and the global hero `<h1>` rule sets a large `font-size`). Tailwind utility classes
have lower specificity than `.slidev-layout h2`, so they lose the cascade fight.

**Fix**: don't use `<h2>` for content-slide titles. Use the `.ask-title` token instead:

```html
<!-- ❌ Fights the cascade, eventually needs ! -->
<h2 class="text-xl">Stack vertical</h2>

<!-- ✅ Bypasses the h2 rule entirely, no !important anywhere -->
<div class="ask-eyebrow">Sesión 02</div>
<div class="ask-title">Stack vertical</div>
```

Reserve `<h1>` and `<h2>` for hero / cover / section divider slides where you actually
*want* the big sizing. Everything else is a `<div class="ask-title">`.

### 12 · Cards inside `flex flex-col` columns get clipped at the bottom

**Symptom**: the last line of the longer card disappears (e.g. a `<code>` line at the
bottom of a card just *isn't there*), even though `bodyScrollHeight === bodyClientHeight`
when you inspect via DevTools — no apparent overflow.

**Cause**: `.card { overflow: hidden; height: 100% }` (the default in this theme) combined
with two cards inside a `<div class="flex flex-col gap-4">` parent that lives in one
column of a `grid grid-cols-3` — the grid row stretches to match the tallest column
(typically a wide table), and the flex children then *split* that height proportionally.
The longer card gets squeezed below its natural content height; `overflow: hidden` clips
the bottom and you see nothing.

When you inspect, the missing element's `getBoundingClientRect()` shows it sitting *below*
the card's bottom edge — the body element extends past the card's clip region.

**Fix**: replace the flex parent with margin-based stacking so each card sizes to its
own content:

```html
<!-- ❌ Cards fight for height, longer card clips -->
<div class="flex flex-col gap-4">
  <div class="card card-compact card-magenta">…long card…</div>
  <div class="card card-compact card-purple">…short card…</div>
</div>

<!-- ✅ Each card sizes to content, no clipping -->
<div class="space-y-4 self-start">
  <div class="card card-compact card-magenta">…long card…</div>
  <div class="card card-compact card-purple">…short card…</div>
</div>
```

`space-y-4` adds margin between siblings (no flex), and `self-start` keeps the column
from being stretched to match the table column's height. Use `card-compact` to reclaim
even more vertical space when the cards share a row with a wide table.

---

## Microsoft brand color quick-reference

| Token            | Hex       | Use for                                        |
|------------------|-----------|------------------------------------------------|
| `--ms-blue`      | `#0078D4` | Primary accent, links, "Microsoft" callouts    |
| `--ms-blue-deep` | `#004578` | Hover state for blue                           |
| `--ms-cyan`      | `#00A4EF` | Logo cyan, secondary accent                    |
| `--ms-purple`    | `#7160E8` | Partner / collab callouts (e.g. KPMG side)     |
| `--ms-magenta`   | `#E3008C` | Warnings, gaps, things that need attention     |
| `--ms-orange`    | `#F25022` | Logo orange, "code" / dev-tool accents         |
| `--ms-amber`     | `#FFB900` | Logo amber, idea / takeaway icons              |
| `--ms-green`     | `#7FBA00` | Logo green, "success" / "approved" tags        |
| `--ms-teal`      | `#008272` | Conversational / chat / customer-data accents  |
| `--ms-ink`       | `#201F1E` | Body copy, headings                            |
| `--ms-ink-soft`  | `#605E5C` | Captions, secondary text, eyebrows             |
| `--ms-line`      | `#E1DFDD` | Hairline borders on light surfaces             |

---

## Pairing this style with other features

- **Code blocks**: dark code (#1F1F1F) on light cards looks intentional and matches MS
  developer docs. Keep `slidev-code-background: #1F1F1F`.
- **Mermaid diagrams**: set `theme: 'neutral'` in mermaid block frontmatter to match.
- **Magic-move**: works fine; the dark code background pops against the light canvas.
- **Drawings (`C` key)**: use a light pen color like `#7160E8` (purple) — black is too
  harsh on the paper canvas.
- **Export to PDF**: works out of the box with `playwright-chromium`. The grain SVG and
  fixed-position swoosh render correctly per slide. Use
  `slidev export --with-clicks --per-slide --wait-until none` to capture click steps.
