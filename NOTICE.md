# Third-Party Notices

This project is MIT-licensed (see [`LICENSE`](LICENSE)) and incorporates or
adapts material from the sources below. Each is credited here with its own
license terms.

---

## Slidev

Most reference files in `references/` derive from the official Slidev agent
skill and the Slidev documentation.

- Source: <https://github.com/slidevjs/slidev> (`skills/slidev`)
- Copyright (c) 2020-PRESENT Anthony Fu
- License: MIT

The upstream copyright is retained in [`LICENSE`](LICENSE) as required.

---

## bronto-community/ai-sre-talk

The rough.js patterns documented in
[`references/diagram-rough-sketch.md`](references/diagram-rough-sketch.md) are
adapted from this talk's components.

- Source: <https://github.com/bronto-community/ai-sre-talk>
- Copyright (c) 2026 Severin Neumann
- License: MIT (per the repository's `LICENSE-CODE`; slide *content* there is
  CC BY 4.0 and is **not** reused here)

---

## Referenced but not redistributed

The following are **documented** by this skill — installation steps, usage
patterns, licensing caveats — but no asset, font, or icon file from them is
vendored in this repository. Downstream users obtain them directly from their
respective sources under their own terms.

| Project | License | Referenced in |
|---|---|---|
| [Selawik](https://github.com/microsoft/Selawik) | SIL OFL 1.1 | `style-microsoft-modern.md` |
| [Fluent UI System Icons](https://github.com/microsoft/fluentui-system-icons) | MIT | `style-microsoft-icons.md` |
| [Azure Architecture Icons](https://learn.microsoft.com/azure/architecture/icons/) | Microsoft terms — Azure architecture diagrams only, **no redistribution** | `style-microsoft-icons.md` |
| Microsoft brand logos | Microsoft brand guidelines — accurate use only | `style-microsoft-modern.md`, `style-microsoft-icons.md` |
| [rough.js](https://github.com/rough-stuff/rough) | MIT | `diagram-rough-sketch.md` |
| [anime.js](https://github.com/juliangarnier/anime) | MIT | `animation-svg-anime.md` |

Note the Azure Architecture Icons terms in particular: they may be used in
Azure architecture diagrams and **may not be redistributed**. This repository
documents how to fetch them from Microsoft's official download; it does not
ship them.

---

## Trademarks

Microsoft, Azure, Fluent, Segoe, Windows, Teams, Outlook, and Office are
trademarks of the Microsoft group of companies. This project is an independent,
community-maintained work. It is **not affiliated with, endorsed by, or
sponsored by Microsoft**.

Use of Microsoft trademarks and brand assets in decks you build with this skill
is subject to Microsoft's
[Trademark and Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks).
You are responsible for ensuring your own usage complies.
