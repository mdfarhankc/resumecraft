# Examples

## Sample resume

[`sample_resume.json`](sample_resume.json) is a complete example showing every feature: work experience, projects with multiple links, skills, education, certifications, awards, and a navy color theme.

Generated output:
- [`output/sample_resume.docx`](output/sample_resume.docx)
- [`output/sample_resume.pdf`](output/sample_resume.pdf)

To regenerate:

```bash
resumecraft build examples/sample_resume.json -o examples/output/sample_resume.docx
```

## Code examples

- [`basic.py`](basic.py) - Minimal usage: load sample, customize, build
- [`from_json.py`](from_json.py) - Build from an existing JSON file
- [`styled.py`](styled.py) - Custom fonts, colors, spacing
- [`fastapi_app.py`](fastapi_app.py) - REST API with FastAPI
- [`flask_app.py`](flask_app.py) - REST API with Flask
- [`django_view.py`](django_view.py) - Django views for docx/pdf generation
