import json
from importlib.metadata import version as pkg_version
from pathlib import Path

import typer
from pydantic import ValidationError

from resumecraft.builder import DocxBuilder
from resumecraft.models import Resume


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"resumecraft {pkg_version('resumecraft')}")
        raise typer.Exit()


app = typer.Typer(
    name="resumecraft",
    help="Generate professionally formatted .docx resumes from JSON data.",
    invoke_without_command=True,
    no_args_is_help=True,
)


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version and exit.",
        callback=_version_callback, is_eager=True,
    ),
) -> None:
    """Generate professionally formatted .docx resumes from JSON data."""


def _load_resume(path: Path) -> Resume:
    """Load and validate a resume JSON file with user-friendly error messages."""
    if not path.exists():
        typer.echo(f"Error: {path} not found.", err=True)
        raise typer.Exit(1)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        typer.echo(f"Error: Invalid JSON in {path}", err=True)
        typer.echo(f"  {e.msg} (line {e.lineno}, column {e.colno})", err=True)
        raise typer.Exit(1)

    try:
        return Resume(**data)
    except ValidationError as e:
        typer.echo(f"Error: Invalid resume data in {path}", err=True)
        for err in e.errors():
            loc = " → ".join(str(l) for l in err["loc"])
            typer.echo(f"  {loc}: {err['msg']}", err=True)
        raise typer.Exit(1)


def _convert_to_pdf(docx_path: Path, pdf_path: Path) -> Path:
    """Convert a .docx file to PDF using docx2pdf."""
    try:
        from docx2pdf import convert
    except ImportError:
        typer.echo(
            "Error: PDF output requires 'docx2pdf'. Install it with:",
            err=True,
        )
        typer.echo("  pip install docx2pdf", err=True)
        raise typer.Exit(1)

    convert(str(docx_path), str(pdf_path))
    return pdf_path


@app.command(no_args_is_help=True)
def build(
    input_file: Path = typer.Argument(...,
                                      help="Path to the resume JSON file."),
    output: Path = typer.Option(
        "output/resume.docx", "-o", "--output",
        help="Output file path (.docx or .pdf)."),
) -> None:
    """Build a .docx resume from a JSON file."""
    resume = _load_resume(input_file)
    builder = DocxBuilder(resume)

    if output.suffix.lower() == ".pdf":
        docx_tmp = output.with_suffix(".docx")
        builder.save(docx_tmp)
        _convert_to_pdf(docx_tmp, output)
        docx_tmp.unlink()
        typer.echo(f"Resume saved to {output}")
    else:
        saved = builder.save(output)
        typer.echo(f"Resume saved to {saved}")


@app.command(no_args_is_help=True)
def validate(
    input_file: Path = typer.Argument(...,
                                      help="Path to the resume JSON file."),
) -> None:
    """Validate a resume JSON file without building."""
    _load_resume(input_file)
    typer.echo(f"Valid: {input_file}")


@app.command()
def init(
    output: Path = typer.Option(
        "resume-template.json", "-o", "--output",
        help="Output JSON template path."),
) -> None:
    """Generate a blank resume JSON template."""
    template = {
        "name": "Your Name",
        "contact": {
            "location": "City, State, Country",
            "email": "your@email.com",
            "phone": "+1-234-567-8900",
            "links": [
                {"label": "LinkedIn", "url": "https://linkedin.com/in/yourprofile"},
                {"label": "GitHub", "url": "https://github.com/yourusername"},
            ],
        },
        "summary": "A brief professional summary about yourself.",
        "bold_keywords": ["Python", "React", "FastAPI", "PostgreSQL", "Docker"],
        "experience": [
            {
                "company": "Company Name",
                "location": "City, Country",
                "title": "Your Title",
                "duration": "JAN 2023 - PRESENT",
                "bullets": [
                    "Describe what you did and the impact it had.",
                    "Use action verbs and quantify results where possible.",
                ],
            }
        ],
        "professional_projects": [
            {
                "name": "Project Name",
                "subtitle": "| Location | Type",
                "tech_stack": "FastAPI, React, PostgreSQL",
                "link": None,
                "bullets": ["Describe the project and your contributions."],
            }
        ],
        "personal_projects": [
            {
                "name": "Side Project",
                "subtitle": "| Personal Project",
                "tech_stack": None,
                "link": {"label": "GitHub", "url": "https://github.com/you/project"},
                "bullets": ["Describe what you built and why."],
            }
        ],
        "skills": [
            {"category": "Backend", "items": "Python (FastAPI, Django), Node.js"},
            {"category": "Frontend", "items": "React, TypeScript"},
            {"category": "Databases", "items": "PostgreSQL, Redis, MongoDB"},
        ],
        "education": [
            {
                "institution": "University Name",
                "degree": "Bachelor of Science in Computer Science",
                "duration": "2019 - 2023",
            }
        ],
        "languages": "English - Native  |  Spanish - Professional Working Proficiency",
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(template, indent=2, ensure_ascii=False), encoding="utf-8")
    typer.echo(f"Template saved to {output}")


if __name__ == "__main__":
    app()
