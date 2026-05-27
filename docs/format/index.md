# Resume Format

ResumeCraft accepts JSON or YAML input files. Both formats use the same structure and fields.

## Minimal Resume

Only three fields are required:

=== "JSON"

    ```json
    {
      "name": "Jane Doe",
      "contact": {
        "location": "New York, NY",
        "email": "jane@example.com",
        "phone": "+1-234-567-8900"
      },
      "summary": "Full-stack developer with 5 years of experience."
    }
    ```

=== "YAML"

    ```yaml
    name: Jane Doe
    contact:
      location: New York, NY
      email: jane@example.com
      phone: "+1-234-567-8900"
    summary: Full-stack developer with 5 years of experience.
    ```

Everything else is optional and has sensible defaults.

## How It Works

1. **Validation** - Your data is validated against Pydantic models with strict mode. Unknown fields (typos) raise errors instead of being silently ignored.
2. **Section ordering** - Sections render in the order specified by `section_order`. If omitted, all non-empty sections render in the default order.
3. **Empty sections** - Sections with no data are automatically skipped. You don't need to remove empty arrays.
4. **Styling** - Font, color, and spacing are resolved from the `style` object. Defaults to Calibri, black, normal spacing.
5. **Rendering** - Each section is rendered to the Word document with proper formatting, tab stops, hyperlinks, and page break protection.

## Available Sections

| Section | Default Heading | Description |
|---|---|---|
| `summary` | PROFESSIONAL SUMMARY | A paragraph about your background |
| `experience` | WORK EXPERIENCE | Jobs with company, title, duration, and bullets |
| `projects` | PROJECTS | Unified projects section |
| `professional_projects` | PROFESSIONAL PROJECTS | Work-related projects |
| `personal_projects` | PERSONAL & OPEN SOURCE PROJECTS | Side projects and open source |
| `skills` | SKILLS | Categorized skill lists |
| `education` | EDUCATION | Degrees and institutions |
| `certifications` | CERTIFICATIONS | Professional certifications |
| `awards` | AWARDS & ACHIEVEMENTS | Awards and honors |
| `languages` | LANGUAGES | Language proficiencies |

!!! tip "Projects: unified vs. split"
    Use `projects` for a single section, **or** `professional_projects` + `personal_projects` for two separate sections. Don't mix both approaches.

## Next Steps

- [Field Reference](fields.md) - Every field, type, and default
- [Styling](styling.md) - Fonts, colors, spacing, photos, and ATS mode
- [Examples](examples.md) - Complete JSON and YAML examples
