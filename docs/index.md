---
hide:
  - navigation
---

# ResumeCraft

**Generate professional resumes from JSON or YAML. Export to Word (.docx) or PDF.**

ResumeCraft takes a single data file and produces a polished, ATS-friendly resume. Use it from the command line, as a Python library, or inside a web framework like FastAPI, Flask, or Django.

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } **Get started in 30 seconds**

    ---

    Install with pip, generate a template, and build your resume.

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-language-python:{ .lg .middle } **Use as a Python library**

    ---

    Factory methods, byte exports, and streaming responses for any framework.

    [:octicons-arrow-right-24: Python Library](library.md)

-   :material-console:{ .lg .middle } **CLI tool**

    ---

    Build, validate, and watch your resume from the terminal.

    [:octicons-arrow-right-24: CLI Reference](cli.md)

-   :material-palette-outline:{ .lg .middle } **7 fonts, 6 colors, 3 spacings**

    ---

    Customize the look with style presets, or enable ATS mode for maximum compatibility.

    [:octicons-arrow-right-24: Styling](format/styling.md)

</div>

## Why ResumeCraft?

- **One file, version controlled** - Your resume lives in a single JSON or YAML file. Track changes with Git.
- **Strict validation** - Pydantic catches typos and missing fields before you build. `"experiance"` raises an error, not a silent pass.
- **Auto-bold keywords** - List your tech stack once, and every mention in your bullets is bolded automatically.
- **ATS-friendly** - Flip `ats: true` to strip formatting that confuses applicant tracking systems.
- **Web-ready** - Factory methods and byte exports plug directly into FastAPI, Flask, or Django.
- **Zero lock-in** - MIT licensed. Your data is plain JSON. Take it anywhere.

## Quick Example

=== "CLI"

    ```bash
    resumecraft init -o my-resume.json    # generate a template
    resumecraft build my-resume.json      # build .docx
    resumecraft build my-resume.json --pdf --open   # build PDF and open it
    ```

=== "Python"

    ```python
    from resumecraft import ResumeCraft

    rc = ResumeCraft.from_jsonfile("my-resume.json")
    rc.to_docx("resume.docx")
    rc.to_pdf("resume.pdf")              # requires resumecraft[pdf]
    ```

=== "FastAPI"

    ```python
    from fastapi import FastAPI
    from fastapi.responses import Response
    from resumecraft import ResumeCraft

    app = FastAPI()

    @app.post("/resume/pdf")
    def generate(data: dict):
        return Response(
            ResumeCraft.from_dict(data).to_pdf_bytes(),
            media_type="application/pdf",
        )
    ```
