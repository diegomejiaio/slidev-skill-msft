---
name: laser-pointer
description: Native laser pointer cursor for emphasizing slide content during presentation
---

# Laser Pointer

Slidev ships a built-in laser pointer (red glowing dot following the cursor)
to emphasize content during a live presentation. Added in **v52.0.0**.

## Enable

In the play view, hover the bottom-left controls → **More Options** (⋯) →
**Cursor Style** → **Laser**.

State persists in `localStorage['slidev-cursor-style']` (`'cursor'` |
`'laser'`).

## Programmatic

```ts
import { cursorStyle } from '@slidev/client/state'
cursorStyle.value = 'laser'
```

## Notes

- Available in both play and presenter modes.
- When drawing mode (`D`) is active, the drawing canvas captures the cursor
  — exit drawing first.
- The dot is rendered inside `<SlideContainer>`'s default slot via a wrapper
  with `absolute top-0 left-0 right-0 bottom-0`. If `right-0` is purged by
  UnoCSS or overridden by a custom selector matching `.absolute.bottom-0.left-0`
  (e.g. nav-controls overrides), the wrapper collapses and the dot renders
  off-screen — see [troubleshooting](troubleshooting.md).
