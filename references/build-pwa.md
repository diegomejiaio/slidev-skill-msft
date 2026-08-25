---
name: pwa
description: Offline support via service worker precaching of all deck assets
---

# PWA / Offline Support

Precaches every built asset — JS, CSS, HTML, images, video, audio — so a served
deck runs entirely from cache with no network. Solves the real failure mode:
presenting on an unfamiliar machine over conference WiFi.

Requires Slidev **v52.17.0+**.

## Usage

Headmatter of the first slide:

```yaml
---
pwa: true
---
```

| Value | Service worker active |
|---|---|
| `false` *(default)* | never |
| `true` | dev + build |
| `'build'` | built output only — **usually what you want** |
| `'dev'` | dev server only |

Off by default because precaching every asset is heavy. Enable it deliberately,
paired with [`build-pdf`](build-pdf.md) / [`core-hosting`](core-hosting.md) for a
self-hosted deck.

## Install the plugin

Powered by `vite-plugin-pwa`, shipped as an **optional peer dependency** — not
installed unless you opt in. The CLI prompts on first use:

```
? The "pwa" option requires the "vite-plugin-pwa" package, which is not installed
  in your project. Install it now? › (Y/n)
```

CI can't show the prompt, so install ahead of time:

```bash
npm i -D vite-plugin-pwa
```

## Behavior

- Serving the built deck triggers background precaching; a bottom-right
  indicator shows `Caching for offline…` then `Ready offline`.
- After that, disconnect the network and reload — everything serves from cache.
- Complete no-op when disabled: client registration and indicator are
  tree-shaken out, so there's no cost unless you opt in.

## Gotchas

- **Only built assets are precached.** Remote/CDN assets stay unavailable
  offline. Combine with
  [`build-remote-assets`](build-remote-assets.md) to download them into the
  build first — otherwise your offline deck still has holes where the remote
  images were.
- **No manifest icons.** The generated web app manifest intentionally ships no
  icons, since a deck's `favicon` may itself be a remote URL and an offline
  feature must not depend on one. Still a valid manifest.
- **Large media is handled.** Workbox's `maximumFileSizeToCacheInBytes` is
  raised to 100 MB and the precache glob covers common image/video/audio
  extensions, so big files aren't silently skipped.
- **Video seeking may fail offline.** Precached media is served as a full cached
  response — playing from the start works, but scrubbing/seeking needs
  additional range-request handling.

## Pre-flight for an offline talk

1. `pwa: 'build'` in headmatter
2. `npm i -D vite-plugin-pwa`
3. Bundle remote images ([`build-remote-assets`](build-remote-assets.md))
4. `slidev build`, serve it, load once, wait for `Ready offline`
5. Turn off WiFi and reload — verify before you're on stage
