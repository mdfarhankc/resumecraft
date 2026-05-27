# Quick Start

## 1. Generate a Template

```bash
resumecraft init -o my-resume.json
```

This creates a JSON file with every available field pre-filled with placeholder data.

## 2. Edit Your Resume

Open `my-resume.json` in your editor. Only three fields are required:

```json
{
  "name": "Your Name",
  "contact": {
    "location": "City, Country",
    "email": "your@email.com",
    "phone": "+1-234-567-8900"
  },
  "summary": "A brief professional summary about yourself."
}
```

Add experience, projects, skills, and other sections as needed. See the [Field Reference](../format/fields.md) for all available fields.

!!! tip "Editor autocomplete"
    Add a `$schema` line at the top of your JSON for autocomplete and validation in VS Code, IntelliJ, and other editors:

    ```json
    {
      "$schema": "https://raw.githubusercontent.com/mdfarhankc/resumecraft/main/schema.json",
      "name": "Your Name"
    }
    ```

## 3. Build Your Resume

```bash
# Build a .docx file (timestamped filename)
resumecraft build my-resume.json

# Build a PDF
resumecraft build my-resume.json --pdf

# Build and open immediately
resumecraft build my-resume.json --pdf --open
```

## 4. Validate Without Building

```bash
resumecraft validate my-resume.json
```

If there are errors, you'll see exactly what's wrong:

```
Error: Invalid resume data in my-resume.json
  contact.email: String should have at least 1 character
  experience.0.bullets: Field required
```

## 5. Watch Mode

Rebuild automatically every time you save the file:

```bash
resumecraft watch my-resume.json --open
```

This outputs a PDF by default and opens it on first build. Most PDF viewers reload automatically, so you get a live preview as you edit. Press `Ctrl+C` to stop.

Requires `pip install resumecraft[watch]`.

## Next Steps

- [CLI Reference](../cli.md) - All commands and options
- [Python Library](../library.md) - Use ResumeCraft in your code
- [Resume Format](../format/index.md) - Full data format documentation
- [Styling](../format/styling.md) - Fonts, colors, spacing, and ATS mode
