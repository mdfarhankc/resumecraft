# Examples

## Sample resume

Two versions built from the same content, showing the difference between a styled resume and an ATS-friendly one.

### Styled (navy theme)

[`sample_resume.json`](sample_resume.json) - uses `style: { font: "calibri", color: "navy" }`.

- [`output/sample_resume.docx`](output/sample_resume.docx)
- [`output/sample_resume.pdf`](output/sample_resume.pdf)

### ATS-friendly

[`sample_resume_ats.json`](sample_resume_ats.json) - same content with `style: { font: "arial", color: "black", ats: true }`. Strips tab stops, heading borders, and colored tech lines for cleaner ATS parsing.

- [`output/sample_resume_ats.docx`](output/sample_resume_ats.docx)
- [`output/sample_resume_ats.pdf`](output/sample_resume_ats.pdf)

To regenerate:

```bash
resumecraft build examples/sample_resume.json -o examples/output/sample_resume.docx
resumecraft build examples/sample_resume_ats.json -o examples/output/sample_resume_ats.docx
```

## Code examples

- [`basic.py`](basic.py) - Minimal usage: load sample, customize, build
- [`from_json.py`](from_json.py) - Build from an existing JSON file
- [`styled.py`](styled.py) - Custom fonts, colors, spacing
- [`fastapi_app.py`](fastapi_app.py) - REST API with FastAPI
- [`flask_app.py`](flask_app.py) - REST API with Flask
- [`django_view.py`](django_view.py) - Django views for docx/pdf generation
