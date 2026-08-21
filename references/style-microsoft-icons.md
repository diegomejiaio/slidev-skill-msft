---
name: microsoft-icons
description: Use official Microsoft and Azure icons in Slidev decks — Fluent UI System Icons (open source, via Iconify), Azure Architecture Icons (custom UnoCSS collection from Microsoft's official ZIP), and Microsoft brand logos.
---

# Official Microsoft & Azure Icons for Slidev

Three official icon sources from Microsoft, each with different licensing and a different
integration path. Pick the one(s) you need:

| Source | License | What it gives you | Best for |
|---|---|---|---|
| **Fluent UI System Icons** | MIT — fully open | ~9,000 generic UI icons (home, settings, person, calendar, document, …) in 6 sizes × 2 styles | General UI, navigation, content metaphors |
| **Azure Architecture Icons** | Microsoft license — Azure architecture diagrams only, no redistribution | ~700 official Azure service icons (Storage Accounts, App Service, Cosmos DB, Functions, AKS, …) | Azure architecture diagrams, service callouts |
| **Microsoft brand logos** | Microsoft brand guidelines — accurate use only | Microsoft, Azure, Teams, Outlook, Windows, Office app marks | Title slides, "powered by" callouts, brand bar |

You can mix all three in the same deck.

---

## 1 · Fluent UI System Icons (the easy one)

Microsoft's open-source UI icon library. Available as a regular NPM package via Iconify
— no manual file management, no licensing hoops.

### Install

```bash
pnpm add -D @iconify-json/fluent
```

Already wired if your `uno.config.ts` uses `presetIcons({ prefix: 'i-' })` — Iconify
auto-discovers any `@iconify-json/*` package you've installed.

### Naming pattern

```
i-fluent:<icon-name>-<size>-<style>
       │            │       │
       │            │       └─  regular | filled
       │            └────────  16 | 20 | 24 | 28 | 32 | 48
       └─────────────────────  kebab-case of the Fluent icon name
```

### Examples

```html
<div class="i-fluent:home-24-regular text-2xl" />
<div class="i-fluent:document-multiple-32-filled text-3xl" style="color: var(--ms-blue)" />
<div class="i-fluent:cloud-arrow-up-24-regular" />
<div class="i-fluent:person-tag-20-filled" />
<div class="i-fluent:shield-checkmark-24-regular" />
<div class="i-fluent:bot-24-filled" />
<div class="i-fluent:flash-24-regular" />
```

### Browse the catalog

- Search UI: <https://react.fluentui.dev/?path=/docs/icons-catalog--docs>
- GitHub source: <https://github.com/microsoft/fluentui-system-icons>
- Iconify search (filter "fluent"): <https://icon-sets.iconify.design/fluent/>

### Tip · prefer `regular` for body, `filled` for emphasis

Fluent's design system uses **regular** for default and inactive states, **filled** for
selected, primary, or highlighted elements. Keep that hierarchy in your slides too —
helps the deck feel native to Microsoft design.

---

## 2 · Azure Architecture Icons (manual download + UnoCSS custom collection)

The official set Microsoft ships for Azure architecture diagrams. **Cannot be
redistributed** — there's no NPM package and no Iconify collection. You download the
ZIP from Microsoft, drop the SVGs in your repo, and register a UnoCSS custom collection
that exposes them as `i-azure:<service>`.

### Step 1 · Download the official ZIP

```
https://learn.microsoft.com/en-us/azure/architecture/icons/
```

Click **"Download SVG icons"**. You'll get a ZIP (~50MB) of ~700 SVG files named like:

```
00017-icon-service-Subscriptions.svg
10001-icon-service-Storage-Accounts.svg
10006-icon-service-Function-Apps.svg
```

### Step 2 · Stage them into your project

```bash
# from the repo root, after unzipping the download to ~/Downloads/AzureIcons/
mkdir -p public/icons/azure
# copy and clean up the names: drop the numeric prefix and "-icon-service-" infix
for f in ~/Downloads/AzureIcons/Azure_Public_Service_Icons/Icons/**/*.svg; do
  base="$(basename "$f" .svg)"
  clean="$(echo "$base" | sed -E 's/^[0-9]+-icon-service-//; s/^[0-9]+-icon-//' | tr '[:upper:]' '[:lower:]')"
  cp "$f" "public/icons/azure/${clean}.svg"
done
ls public/icons/azure/ | head
# →  storage-accounts.svg, function-apps.svg, app-services.svg, …
```

> ⚠️ **Do not commit the icons to a public repo.** Microsoft's terms restrict
> redistribution. Add `public/icons/azure/` to `.gitignore` and document the download
> step in your README so collaborators bring their own copy.

### Step 3 · Register them as a UnoCSS collection

Add to `uno.config.ts`:

```ts
import { presetIcons } from 'unocss'
import { FileSystemIconLoader } from '@iconify/utils/lib/loader/node-loaders'

// ...inside presets: [...]
presetIcons({
  prefix: 'i-',
  collections: {
    // Azure architecture icons live in public/icons/azure/<service>.svg.
    // The loader strips fill/stroke="..." so you can re-color via currentColor
    // and CSS — useful for hover states and dark/light themes.
    azure: FileSystemIconLoader(
      './public/icons/azure',
      svg => svg
        .replace(/fill="[^"]*"/g, 'fill="currentColor"')
        .replace(/stroke="[^"]*"/g, 'stroke="currentColor"'),
    ),
  },
  extraProperties: { display: 'inline-block', 'vertical-align': 'middle' },
}),
```

You'll need to add `@iconify/utils` if it's not already a dep:

```bash
pnpm add -D @iconify/utils
```

> 💡 If you'd rather **keep Microsoft's original colors** (the official Azure brand cyan
> per service), drop the two `.replace(...)` calls — the SVGs render with their built-in
> colors and ignore CSS color.

### Step 4 · Restart Slidev

```bash
./run.sh        # custom collections need a full server restart, not HMR
```

### Step 5 · Use them

```html
<!-- Monochrome (currentColor — picks up CSS color) -->
<div class="i-azure:storage-accounts text-3xl" style="color: var(--ms-blue)" />
<div class="i-azure:function-apps text-2xl" style="color: var(--ms-orange)" />

<!-- Native Azure colors (if you removed the .replace() calls in step 3) -->
<div class="i-azure:cosmos-db text-4xl" />
<div class="i-azure:app-services text-4xl" />
```

### Discovery

Inspect the cleaned filenames in `public/icons/azure/` — the icon name in the class is
the filename without `.svg`:

```bash
ls public/icons/azure/ | sed 's/\.svg$//' | grep -i storage
# → storage-accounts, storage-queues, storage-explorer, …
```

---

## 3 · Microsoft brand logos (already on Iconify)

For the brand marks themselves — Microsoft, Azure, Teams, Outlook, Windows, Office apps —
two collections cover almost everything:

### `@iconify-json/logos` (color brand marks)

```bash
pnpm add -D @iconify-json/logos
```

```html
<div class="i-logos:microsoft-icon text-4xl" />        <!-- 4-square logo -->
<div class="i-logos:microsoft-azure text-4xl" />        <!-- Azure cube -->
<div class="i-logos:microsoft-teams text-4xl" />
<div class="i-logos:microsoft-windows-icon text-4xl" />
<div class="i-logos:microsoft-outlook text-4xl" />
<div class="i-logos:microsoft-onedrive text-4xl" />
<div class="i-logos:visual-studio-code text-4xl" />
<div class="i-logos:github-icon text-4xl" />
```

### `@iconify-json/simple-icons` (monochrome brand marks)

```bash
pnpm add -D @iconify-json/simple-icons
```

```html
<!-- Single-color, color via CSS — useful when the brand mark must follow theme color -->
<div class="i-simple-icons:microsoftazure" style="color: var(--ms-ink)" />
<div class="i-simple-icons:microsoft365" style="color: var(--ms-blue)" />
```

### Inline SVG (the most accurate for Microsoft 4-square)

For the canonical 4-color Microsoft logo (e.g. in `global-top.vue` chrome) the Iconify
version is fine, but inline SVG gives you exact pixel control:

```html
<svg viewBox="0 0 23 23" width="22" height="22">
  <rect x="1"  y="1"  width="10" height="10" fill="#F25022" />
  <rect x="12" y="1"  width="10" height="10" fill="#7FBA00" />
  <rect x="1"  y="12" width="10" height="10" fill="#00A4EF" />
  <rect x="12" y="12" width="10" height="10" fill="#FFB900" />
</svg>
```

---

## Combining all three in one deck

A typical Microsoft customer deck uses all three:

```html
<!-- Top chrome: brand logo (option 3 — inline SVG) -->
<div class="ms-logo">
  <svg viewBox="0 0 23 23" width="22" height="22"> … </svg>
  <span>Microsoft</span>
</div>

<!-- Card header: Fluent generic icon (option 1) -->
<div class="card card-blue">
  <div class="card-header">
    <div class="i-fluent:document-multiple-24-regular card-icon" />
    Documentation
  </div>
</div>

<!-- Architecture diagram: Azure service icons (option 2) -->
<div class="flex items-center gap-6">
  <div class="i-azure:azure-active-directory text-5xl" />
  <div class="i-carbon:arrow-right text-2xl" style="color: var(--ms-ink-soft)" />
  <div class="i-azure:api-management-services text-5xl" />
  <div class="i-carbon:arrow-right text-2xl" style="color: var(--ms-ink-soft)" />
  <div class="i-azure:function-apps text-5xl" />
</div>
```

---

## Recommended `uno.config.ts` (all three packs)

```ts
// @ts-expect-error - missing types for the slidev uno config export
import config from '@slidev/client/uno.config'
import {
  mergeConfigs, presetAttributify, presetIcons, presetWebFonts, presetWind3,
} from 'unocss'
import { FileSystemIconLoader } from '@iconify/utils/lib/loader/node-loaders'

export default mergeConfigs([
  config,
  {
    presets: [
      presetWind3({ dark: 'class' }),
      presetAttributify(),
      presetIcons({
        prefix: 'i-',
        extraProperties: { display: 'inline-block', 'vertical-align': 'middle' },
        warn: true,
        collections: {
          // Custom Azure architecture icons (downloaded ZIP, see step 1-3 above)
          azure: FileSystemIconLoader(
            './public/icons/azure',
            svg => svg
              .replace(/fill="[^"]*"/g, 'fill="currentColor"')
              .replace(/stroke="[^"]*"/g, 'stroke="currentColor"'),
          ),
        },
      }),
      presetWebFonts({ /* ... */ }),
    ],
    // No special safelist needed — Iconify icons are tree-shaken on usage.
  },
])
```

With `@iconify-json/fluent`, `@iconify-json/logos` and `@iconify-json/simple-icons`
installed, the four prefixes you'll use are:

| Prefix | Source | Use for |
|---|---|---|
| `i-fluent:` | `@iconify-json/fluent` (auto-discovered) | Generic UI icons, content metaphors |
| `i-azure:` | Custom `FileSystemIconLoader` | Azure service icons in architecture diagrams |
| `i-logos:` | `@iconify-json/logos` (auto-discovered) | Color brand logos |
| `i-simple-icons:` | `@iconify-json/simple-icons` (auto-discovered) | Monochrome brand logos |
| `i-carbon:` | `@iconify-json/carbon` (auto-discovered) | Generic UI fallback (always reliable, simple geometry) |

---

## Gotchas

### Restart required when adding icon collections

Adding a new `@iconify-json/*` package or editing the `collections:` config in
`uno.config.ts` requires a **full Slidev restart** — HMR doesn't pick up icon registry
changes. Use `./run.sh` (the kill-and-relaunch helper).

### Azure icons render too large with `text-2xl`

Azure SVGs have larger native viewboxes than UI icons. Start with `text-4xl` or
`text-5xl` for service icons, not `text-2xl`. Or use `width: 48px` / `height: 48px`
inline.

### `currentColor` only works if you stripped the fills

The `FileSystemIconLoader` `.replace()` calls in step 3 are what make `style="color: …"`
work on Azure icons. Without them, the SVGs render with their built-in fills and
**ignore your CSS color**. Either:

- Keep the `.replace()` → monochrome icons, color follows CSS `color:`. Best for
  consistent themes (e.g. all icons in `--ms-blue`).
- Remove the `.replace()` → original full-color Azure icons. Best when accuracy of
  the Azure brand color per service matters (architecture diagrams for customers).

### Don't commit Azure icons to public repos

Microsoft's license restricts redistribution. Always:
1. Add `public/icons/azure/` to `.gitignore`
2. Document the download step in your repo README so collaborators can BYO

### Fluent has 12 variants per icon — be consistent

Each Fluent icon comes in 6 sizes × 2 styles = 12 versions. Don't mix sizes in the same
visual cluster. Pick a size for body (e.g. `24-regular`), a size for emphasis (e.g.
`32-filled`), and stick with that throughout the deck.

### Filled icons + dark theme can blow out

Fluent `filled` icons are dense — at large sizes on a dark background they can dominate
the slide. If you're on a dark theme, prefer `regular` and bump weight via `font-weight`
or color saturation rather than switching to `filled`.

---

## Reference URLs

- Fluent UI System Icons (browse): <https://react.fluentui.dev/?path=/docs/icons-catalog--docs>
- Fluent UI System Icons (source): <https://github.com/microsoft/fluentui-system-icons>
- Azure architecture icons (download): <https://learn.microsoft.com/en-us/azure/architecture/icons/>
- Microsoft brand center: <https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks>
- Iconify catalog (search any prefix): <https://icon-sets.iconify.design/>
- UnoCSS preset-icons docs: <https://unocss.dev/presets/icons>

---

## When the 3 main sources don't have what you need

The Fluent + Azure + brand-logos combo covers maybe 80% of what you'll reach for in a
Microsoft customer deck. Here's where to find the other 20%, organized by what you're
looking for.

### Decision tree

```
Need an icon and Fluent / Azure / logos don't have it?
│
├─ Is it a Microsoft product?
│   ├─ M365 apps (Word, Excel, Teams, Outlook…) ───► Iconify  i-logos:microsoft-<app>
│   ├─ Microsoft Fabric service icons ─────────────► Manual download (see §A)
│   ├─ Power Platform service icons ───────────────► Manual download (see §B)
│   ├─ Defender / Sentinel / Purview / Entra ID ───► Already in Azure ZIP (see §C)
│   └─ Dynamics 365 ───────────────────────────────► simple-icons / brand center (§D)
│
├─ Is it a developer / GitHub / dev-tools icon?
│   ├─ GitHub product (Copilot, Actions, …) ───────► @iconify-json/octicon
│   ├─ VS Code / file types ───────────────────────► @iconify-json/vscode-icons
│   └─ Programming languages, frameworks ──────────► @iconify-json/devicon, logos
│
├─ Is it a partner / customer logo (KPMG, etc.)?
│   └─────────────────────────────────────────────► Manual from their brand kit (§E)
│
├─ Is it a 3D illustrated keynote-style icon?
│   └─────────────────────────────────────────────► design.microsoft.com (§F)
│
└─ None of the above
    └─────────────────────────────────────────────► Search icon-sets.iconify.design,
                                                     fall back to i-carbon:* (§G)
```

### §A · Microsoft Fabric icons

Microsoft Fabric ships its own icon set (Lakehouse, Warehouse, KQL DB, Eventhouse,
Notebook, Pipeline, Real-Time Dashboard, Semantic Model, OneLake, …). Same model as
Azure: official ZIP, restricted license, register as a UnoCSS custom collection.

**Download**: <https://learn.microsoft.com/en-us/fabric/get-started/icons>
(look for the "Download Microsoft Fabric icons" link).

```bash
mkdir -p public/icons/fabric
# adjust the source path to wherever you unzipped it
for f in ~/Downloads/MicrosoftFabricIcons/**/*.svg; do
  base="$(basename "$f" .svg)"
  clean="$(echo "$base" | sed -E 's/^[0-9]+-//; s/-icon-service-//' | tr '[:upper:]' '[:lower:]')"
  cp "$f" "public/icons/fabric/${clean}.svg"
done
```

Add to `presetIcons({ collections: { … } })`:

```ts
fabric: FileSystemIconLoader(
  './public/icons/fabric',
  svg => svg
    .replace(/fill="[^"]*"/g, 'fill="currentColor"')
    .replace(/stroke="[^"]*"/g, 'stroke="currentColor"'),
),
```

Use:

```html
<div class="i-fabric:lakehouse text-4xl" style="color: var(--ms-teal)" />
<div class="i-fabric:warehouse text-4xl" />
<div class="i-fabric:kql-database text-4xl" />
<div class="i-fabric:notebook text-4xl" />
```

Same `.gitignore` discipline applies — `public/icons/fabric/` should not ship to a
public repo.

### §B · Power Platform service icons

For service-level icons of Power BI / Power Apps / Power Automate / Power Pages /
Copilot Studio / Dataverse subcomponents (not just the brand marks).

**Download**: <https://learn.microsoft.com/en-us/power-platform/guidance/icons>

Same workflow as Fabric — drop into `public/icons/powerplatform/`, register as a custom
collection, use as `i-powerplatform:<service>`.

For just the **brand marks** (Power BI yellow tile, Power Apps purple, etc.) Iconify
already has them and you don't need the manual download:

```html
<div class="i-logos:microsoft-power-bi" />
<div class="i-logos:microsoft-power-apps" />
<div class="i-logos:microsoft-power-automate" />
```

### §C · Security / Identity icons (Defender, Sentinel, Purview, Entra ID, Intune)

These ship **inside the Azure architecture icons ZIP** — they're not a separate download.
After unzipping, look in subfolders like:

```
Identity/                        →  Microsoft Entra ID, Conditional Access, …
Security/                        →  Defender, Sentinel, Purview, Key Vault, …
Management + governance/         →  Intune, Defender for Cloud, …
```

Once you've staged them into `public/icons/azure/`, they're just regular `i-azure:*`
icons:

```html
<div class="i-azure:microsoft-entra-id text-4xl" />
<div class="i-azure:microsoft-defender-for-cloud text-4xl" />
<div class="i-azure:microsoft-sentinel text-4xl" />
<div class="i-azure:microsoft-purview text-4xl" />
```

> 💡 If you only want the security stuff (not the whole 700-icon Azure set), unzip
> into a temp folder, copy only the security/identity subfolders, and you'll keep
> the bundle small.

### §D · Dynamics 365 and other Microsoft brand marks

Most are in `simple-icons` (monochrome, theme-color via CSS):

```html
<div class="i-simple-icons:microsoftdynamics365" style="color: var(--ms-blue)" />
<div class="i-simple-icons:microsoftbing" />
<div class="i-simple-icons:microsoftedge" />
<div class="i-simple-icons:microsoftexcel" />
```

For the canonical color version, **Microsoft Brand Central**
(<https://brandcentral.microsoft.com/>) is the source — but it requires Microsoft
sign-in. Once you have an SVG, drop it in `public/icons/brand/` and register as a
custom collection.

### §E · Partner / customer logos (KPMG, Accenture, BBVA, etc.)

Iconify won't have most of these. The right path:

1. **Find the customer's brand kit** — usually `<customer>.com/press`, `/media`,
   `/brand-guidelines`, `/about/brand` or `/newsroom`. Most enterprises publish
   approved SVGs.
2. **Pick the version that fits your background** — most kits ship full-color, mono
   white (for dark backgrounds), and mono black (for light). For the MS Modern theme
   (light canvas), use the full-color or mono-black version.
3. **Drop into `public/icons/partners/`** and register a custom collection:

```ts
partners: FileSystemIconLoader('./public/icons/partners'),  // keep original colors
```

```html
<div class="i-partners:kpmg" style="height: 32px" />
```

> ⚠️ **Brand guidelines vary**. Some companies require minimum clear space, specific
> color values, or written permission for use. Skim the customer's brand guidelines PDF
> before shipping — especially for external/customer-facing decks. When in doubt, ask
> the customer's marketing contact for the latest approved SVG.

### §F · Microsoft 3D illustrated icons (keynote-style)

The fluffy 3D-rendered illustrations you see in MS Build / Ignite keynotes ("a 3D
purple cloud", "a 3D Copilot orb"). These come from Microsoft Design's published
collections at <https://design.microsoft.com/>. They are **PNG/illustration assets**,
not SVG vector — so they don't go through UnoCSS.

Workflow:
1. Download the PNG (usually 1024px, transparent background) from the published
   collection or Microsoft Design's GitHub repos.
2. Drop into `public/illustrations/`.
3. Use as a regular image:

```html
<img src="/illustrations/copilot-orb.png" class="h-32" alt="Copilot" />
```

Common collection: <https://github.com/microsoft/cloud-native-icons> (Microsoft's
3D cloud-native icon set, MIT licensed).

### §G · Last resort: search Iconify and fall back to Carbon

Before giving up, search the full Iconify catalog — it has 200+ collections covering
over 200,000 icons:

<https://icon-sets.iconify.design/>

Useful general collections beyond the Microsoft world:

| Pack | Install | Strength |
|---|---|---|
| `mdi` (Material Design Icons) | `pnpm add -D @iconify-json/mdi` | Huge coverage of generic + many brands (`mdi:microsoft-azure`, `mdi:slack`, `mdi:aws`) |
| `tabler` | `pnpm add -D @iconify-json/tabler` | Modern thin-line aesthetic, ~5,000 icons |
| `lucide` | `pnpm add -D @iconify-json/lucide` | Clean, consistent, popular React/Vue choice |
| `heroicons` | `pnpm add -D @iconify-json/heroicons` | Tailwind-aligned, regular + solid |
| `ph` (Phosphor) | `pnpm add -D @iconify-json/ph` | Multiple weights (thin, light, regular, bold, fill) |

**The reliable fallback**: `i-carbon:*` (IBM's Carbon Design System). Already in your
deps, predictable simple geometry, never out of place on a corporate slide. When you
can't find anything else, Carbon almost always has *something* close.

---

## Quick "I need an icon for X" cheat sheet

| You need… | Try this first |
|---|---|
| A user / person | `i-fluent:person-24-regular` |
| A document / file | `i-fluent:document-24-regular` |
| A chat / conversation | `i-fluent:chat-24-regular` |
| A bot / agent | `i-fluent:bot-24-regular` |
| A cloud (generic) | `i-fluent:cloud-24-regular` |
| Microsoft Azure (brand) | `i-logos:microsoft-azure` |
| An Azure service | `i-azure:<service>` (after Azure ZIP setup) |
| A Microsoft 365 app | `i-logos:microsoft-<app>` |
| GitHub Copilot | `i-octicon:copilot-24` |
| A code editor / IDE | `i-logos:visual-studio-code` |
| A programming language | `i-logos:<language>` or `i-devicon:<language>` |
| A partner / customer logo | Manual — from their brand kit, into `public/icons/partners/` |
| Generic UI catch-all | `i-carbon:<name>` (always reliable) |
