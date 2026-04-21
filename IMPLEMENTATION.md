# v1.0 Plan

Design notes for the v1 rewrite. Not built yet; this is the target.

## Goals

1. Keep the JSON API working exactly as it does today. No breaking changes for existing users.
2. Add a Python widget API for devs who want to build layouts in code.
3. Allow creative layouts (sidebars, two-column, colored panels) without forcing them on people who need ATS mode.

## Why widgets

The current builder hardcodes one layout in `DocxBuilder.build()`. Users who want something different have to subclass and override methods, which gets messy.

A widget tree lets developers compose the resume the same way they compose React/Flutter UIs. Each widget renders itself into the docx stream.

## Architecture

```
  JSON file                       Python code
      |                                |
      v                                v
  parse JSON  --->  widget tree  <---  user composes widgets
                        |
                        v
                  DocxRenderer
                        |
                        v
                     .docx file
```

- `Resume` Pydantic model becomes a thin layer that builds a default widget tree from JSON.
- `DocxBuilder` is replaced by `DocxRenderer`, which walks the tree and produces the document.
- Widgets are plain dataclasses with a `render(ctx)` method.

## Widget categories

Two groups. They are labeled in docstrings so IDEs hint correctly.

### Flow widgets (ATS-safe)

Render as vertical paragraphs. No tables. Compatible with ATS mode.

```
Resume          # root, holds a list of children
Header          # name + contact block
Section         # bold heading + bottom border + children
Experience      # company / title / duration / bullets
Project         # name / subtitle / tech / links / bullets
SkillGroup      # category: items
Education       # institution / degree / duration
Certification   # name / issuer / date / link
Award           # title / issuer / date / description
Bullet          # single bullet with bold-keyword handling
Paragraph       # free-form paragraph
Link            # inline hyperlink run
```

### Layout widgets (NOT ATS-safe)

Produce tables under the hood. Warned in docstrings. Refused or flattened in ATS mode.

```
Row             # side-by-side children (table row)
Column          # single column (table cell), optional width
Sidebar         # Column subclass with background color
Spacer          # fixed vertical space
Divider         # horizontal line
```

### Style primitives

```
Text            # run-level text with font/color/size overrides
Bold / Italic   # inline decorators
Pill            # small rounded label (1-cell table)
```

## Example

```python
from resumecraft.widgets import (
    Resume, Header, Section, Experience, Bullet,
    Row, Column, Sidebar, SkillGroup,
)

resume = Resume([
    Row([
        Sidebar(width=0.33, background="#1F2937", [
            Header(name="Jane Doe", email="jane@example.com"),
            Section("SKILLS", [
                SkillGroup("Backend", "Python, FastAPI"),
                SkillGroup("Frontend", "React, TypeScript"),
            ]),
        ]),
        Column(width=0.67, [
            Section("EXPERIENCE", [
                Experience(
                    company="Acme", title="Engineer",
                    duration="2022 - PRESENT",
                    bullets=[Bullet("Shipped things."), Bullet("Fixed others.")],
                ),
            ]),
        ]),
    ]),
])

resume.to_docx("out.docx")
```

## ATS safety

The `style.ats` flag already exists. In v1 it does one of:

1. *Refuse*: raise `AtsError("Row/Sidebar are not ATS-safe; remove layout widgets or disable ats mode")`
2. *Flatten*: walk the tree and replace `Row(children=[A, B])` with `A + B` stacked vertically

Default is *refuse* so users don't silently ship broken resumes. An opt-in `ats_flatten=True` on the renderer enables flatten mode.

## Rendering pipeline

```python
class RenderContext:
    doc: Document
    style: ResolvedStyle
    ats: bool
    bold_pattern: re.Pattern | None

class Widget(Protocol):
    def render(self, ctx: RenderContext) -> None: ...
    def is_ats_safe(self) -> bool: ...
```

Renderer:

1. Resolve `style` once
2. Walk the tree top-down
3. For layout widgets, create a docx table and recurse into cells
4. For flow widgets, append paragraphs to `ctx.doc` directly

## JSON backward compatibility

`Resume.from_json` stays identical. Internally it builds a default widget tree:

```python
def _default_tree(data: ResumeData) -> Widget:
    return Resume([
        Header(...),
        *[Section(heading, children) for name, ... in data.sections],
    ])
```

So `resumecraft build resume.json` still works, produces the same output, and existing JSON files need no changes.

## File layout

```
src/resumecraft/
    widgets/
        __init__.py       # exports
        base.py           # Widget protocol, RenderContext
        flow.py           # Section, Experience, Bullet, etc.
        layout.py         # Row, Column, Sidebar, Spacer
        style.py          # Text, Bold, Italic, Pill
    renderer.py           # DocxRenderer, replaces builder.py
    models.py             # Pydantic models (unchanged)
    loader.py             # JSON to widget tree
    cli.py                # unchanged
    craft.py              # ResumeCraft facade, updated to use renderer
```

## Migration path

- v0.x users on the JSON API: no changes needed.
- v0.x users who subclassed `DocxBuilder`: `DocxBuilder` stays as a deprecated shim wrapping the renderer. One minor version of warnings, then remove.
- New v1 features (widgets, layout) are additive.

## Open questions

1. Widget serialization: should widgets be dumpable back to JSON? If yes, the widget API becomes round-trippable.
2. Theming scope: per-widget `style=` overrides or keep styling global?
3. Inline rich text: how much formatting inside `Bullet(...)`? Markdown? A list of `Text`/`Bold`/`Link` runs? Pick one.
4. Table fidelity: docx tables with invisible borders render inconsistently across Word/LibreOffice/Google Docs. Needs testing before committing.
5. Width units: percentages of page width (current plan), explicit inches, or both?

## Phasing

- Phase 1: internal refactor. `DocxBuilder` rewritten on top of an internal widget tree. No public widget API yet. Output byte-identical to today. Ships as v0.x.
- Phase 2: public `resumecraft.widgets` exports. Flow widgets first. Layout widgets and ATS-refuse behavior. Ships as v1.0.0-beta.
- Phase 3: docs, migration guide, examples. Stable v1.0.0.

## Non-goals for v1

- HTML / markdown export
- Real-time preview
- GUI / web editor
- Replacing the JSON API
