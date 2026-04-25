import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path

import typer
from pydantic import ValidationError

from resumecraft import ResumeCraft, __version__
from resumecraft.builder import DocxBuilder
from resumecraft.models import Resume

SCHEMA_URL = "https://raw.githubusercontent.com/mdfarhankc/resumecraft/main/schema.json"


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"resumecraft {__version__}")
        raise typer.Exit()


app = typer.Typer(
    name="resumecraft",
    help="Generate professional resumes from JSON with DOCX/PDF export, custom styling, and web framework support.",
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
    """Generate professional resumes from JSON with DOCX/PDF export, custom styling, and web framework support."""


def _load_resume(path: Path) -> Resume:
    if not path.exists():
        typer.echo(f"Error: {path} not found.", err=True)
        raise typer.Exit(1)

    suffix = path.suffix.lower()
    if suffix not in {".json", ".yaml", ".yml"}:
        typer.echo(f"Error: {path} must be a .json, .yaml or .yml file.", err=True)
        typer.echo(f"  Got: {path.suffix}", err=True)
        raise typer.Exit(1)

    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as e:
        typer.echo(f"Error: {path} is not a valid UTF-8 text file.", err=True)
        typer.echo("  Make sure you're passing a text file, not a binary file.", err=True)
        raise typer.Exit(1) from e

    try:
        if suffix == ".json":
            data = json.loads(text)
        else:
            try:
                import yaml
            except ImportError as e:
                typer.echo("Error: YAML input requires pyyaml.", err=True)
                typer.echo("  pip install resumecraft[yaml]", err=True)
                raise typer.Exit(1) from e
            data = yaml.safe_load(text)
    except json.JSONDecodeError as e:
        typer.echo(f"Error: Invalid JSON in {path}", err=True)
        typer.echo(f"  {e.msg} (line {e.lineno}, column {e.colno})", err=True)
        raise typer.Exit(1) from e

    try:
        return Resume(**data)
    except ValidationError as e:
        typer.echo(f"Error: Invalid resume data in {path}", err=True)
        for err in e.errors():
            loc = ".".join(str(part) for part in err["loc"])
            typer.echo(f"  {loc}: {err['msg']}", err=True)
        raise typer.Exit(1) from e


def _convert_to_pdf(docx_path: Path, pdf_path: Path) -> Path:
    try:
        from docx2pdf import convert
    except ImportError as e:
        typer.echo("Error: PDF output requires docx2pdf.", err=True)
        typer.echo("  pip install resumecraft[pdf]", err=True)
        raise typer.Exit(1) from e

    convert(str(docx_path), str(pdf_path))
    return pdf_path


def _save_safely(builder: DocxBuilder, output: Path) -> Path:
    if output.is_dir():
        typer.echo(f"Error: {output} is a directory. Give a file path.", err=True)
        raise typer.Exit(1)
    try:
        return builder.save(output)
    except PermissionError as e:
        typer.echo(f"Error: Can't write to {output} (locked or read-only).", err=True)
        typer.echo("  Close the file in Word/another app and try again.", err=True)
        raise typer.Exit(1) from e
    except OSError as e:
        typer.echo(f"Error: Failed to save {output}: {e}", err=True)
        raise typer.Exit(1) from e


def _open_file(path: Path) -> None:
    system = platform.system()
    if system == "Windows":
        subprocess.Popen(["start", "", str(path)], shell=True)
    elif system == "Darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])


@app.command(no_args_is_help=True)
def build(
    input_file: Path = typer.Argument(...,
                                      help="Path to the resume JSON file."),
    output: Path = typer.Option(
        None, "-o", "--output",
        help="Output file path. Defaults to <input-name>_YYYY-MM-DD_HH-MMam/pm.docx"),
    pdf: bool = typer.Option(
        False, "--pdf",
        help="Shortcut for '-o <input-name>.pdf'. Ignored if -o is given."),
    open_file: bool = typer.Option(
        False, "--open", help="Open the file after building."),
) -> None:
    """Build a .docx (or .pdf) resume from a JSON file."""
    if output is None:
        if pdf:
            output = Path(f"{input_file.stem}.pdf")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M%p").lower()
            output = Path(f"{input_file.stem}_{timestamp}.docx")

    resume = _load_resume(input_file)
    builder = DocxBuilder(resume)

    if output.suffix.lower() == ".pdf":
        docx_tmp = output.with_suffix(".docx")
        _save_safely(builder, docx_tmp)
        try:
            _convert_to_pdf(docx_tmp, output)
        finally:
            docx_tmp.unlink(missing_ok=True)
        typer.echo(f"Resume saved to {output}")
    else:
        saved = _save_safely(builder, output)
        typer.echo(f"Resume saved to {saved}")

    if open_file:
        _open_file(output)


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
        "$schema": SCHEMA_URL,
        "_version": __version__,
        **ResumeCraft.sample(),
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(template, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    typer.echo(f"Template saved to {output}")


@app.command(no_args_is_help=True)
def watch(
    input_file: Path = typer.Argument(...,
                                      help="Path to the resume JSON file."),
    output: Path = typer.Option(
        None, "-o", "--output",
        help="Output file path (.docx or .pdf). Defaults to <input-name>.pdf"),
    open_file: bool = typer.Option(
        False, "--open", help="Open the file after first build."),
) -> None:
    """Watch a JSON file and rebuild on every save."""
    try:
        from watchfiles import watch as watch_files
    except ImportError as e:
        typer.echo(
            "Error: Watch mode requires 'watchfiles'. Install it with:",
            err=True,
        )
        typer.echo("  pip install resumecraft[watch]", err=True)
        raise typer.Exit(1) from e

    if not input_file.exists():
        typer.echo(f"Error: {input_file} not found.", err=True)
        raise typer.Exit(1)

    if output is None:
        output = input_file.with_suffix(".pdf")

    def _rebuild() -> None:
        ts = datetime.now().strftime("%I:%M:%S %p").lower()
        try:
            resume = _load_resume(input_file)
            builder = DocxBuilder(resume)
            if output.suffix.lower() == ".pdf":
                docx_tmp = output.with_suffix(".docx")
                builder.save(docx_tmp)
                try:
                    _convert_to_pdf(docx_tmp, output)
                finally:
                    docx_tmp.unlink(missing_ok=True)
            else:
                builder.save(output)
            typer.echo(f"[{ts}] Rebuilt -> {output}")
        except SystemExit:
            typer.echo(f"[{ts}] Build failed, waiting for next change.", err=True)
        except PermissionError:
            typer.echo(f"[{ts}] {output} is locked (close it in Word), will retry.", err=True)
        except OSError as e:
            typer.echo(f"[{ts}] Failed to save {output}: {e}", err=True)

    typer.echo(f"Watching {input_file} for changes... (Ctrl+C to stop)")
    _rebuild()

    if open_file:
        _open_file(output)

    for _ in watch_files(input_file.parent, watch_filter=lambda _, path: Path(path).name == input_file.name):
        _rebuild()


if __name__ == "__main__":
    app()
