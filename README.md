# Slidev Skill (MSFT fork)

Agent skill that helps AI coding assistants (GitHub Copilot, Claude Code, and other
agent runtimes that support the Agent Skills spec) understand and work with
[Slidev](https://sli.dev) presentations. This is a private fork of the upstream
`slidevjs/slidev` skill with added Microsoft-branded theme and icon pack support
(`style-microsoft-modern`, `style-microsoft-icons`).

## Installation

Clone this repo directly into your agent's skills directory so it's picked up as
a skill on any machine:

```bash
git clone https://github.com/diegomejiaio/slidev-skill-msft.git ~/.copilot/skills/slidev
```

## What's Included

The Slidev skill provides the agent with knowledge about:

- **Core Syntax** - Markdown syntax, slide separators, frontmatter
- **Animations** - Click animations, transitions, motion effects
- **Code Features** - Line highlighting, Monaco editor, code groups, magic-move
- **Diagrams** - Mermaid, PlantUML, LaTeX math
- **Layouts** - Built-in layouts, slots, global layers
- **Presenter Mode** - Recording, timer, remote access
- **Exporting** - PDF, PPTX, PNG, SPA hosting

## Usage

Once installed, the agent will automatically use Slidev knowledge when:

- Creating new presentations
- Adding slides with code examples
- Setting up animations and transitions
- Configuring themes and layouts
- Exporting presentations

### Example Prompts

```
Create a Slidev presentation about TypeScript generics with code examples
```

```
Add a two-column slide with code on the left and explanation on the right
```

```
Set up click animations to reveal bullet points one by one
```

```
Configure the presentation for PDF export with speaker notes
```

## Documentation

- [Slidev Documentation](https://sli.dev)
- [Theme Gallery](https://sli.dev/resources/theme-gallery)
- [Showcases](https://sli.dev/resources/showcases)

## License

MIT
