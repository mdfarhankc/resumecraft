# Styling

Customize the look of your resume with the `style` object. All options are optional and have sensible defaults.

```json
{
  "style": {
    "font": "garamond",
    "color": "navy",
    "spacing": "compact",
    "ats": false
  }
}
```

---

## Fonts

| Value | Font Name |
|---|---|
| `calibri` | Calibri **(default)** |
| `arial` | Arial |
| `times` | Times New Roman |
| `garamond` | Garamond |
| `georgia` | Georgia |
| `helvetica` | Helvetica |
| `cambria` | Cambria |

!!! tip
    **Calibri** and **Arial** are safe choices for maximum compatibility. **Garamond** and **Georgia** give a more traditional look. Make sure the font is installed on the system that opens the document.

---

## Color Themes

Each theme sets the color for section headings, tech stack lines, and hyperlinks.

| Value | Heading Color | Link Color | Best for |
|---|---|---|---|
| `black` | Black | Blue | Classic, safe for any industry **(default)** |
| `navy` | Dark blue | Dark blue | Corporate, finance, consulting |
| `forest` | Dark green | Dark green | Sustainability, nature, healthcare |
| `maroon` | Deep red | Deep red | Law, academia, traditional industries |
| `slate` | Dark gray | Dark gray | Subtle, modern, tech |
| `royal` | Deep purple | Deep purple | Creative, design, standout |

---

## Spacing Presets

| Value | Description | Use when |
|---|---|---|
| `compact` | Tight spacing (6pt between sections, 0pt between bullets) | You need to fit a lot of content on one page |
| `normal` | Balanced spacing (8pt between sections, 1pt between bullets) **(default)** | Most resumes |
| `relaxed` | Generous spacing (10pt between sections, 2pt between bullets) | Short resumes that need to fill the page |

### Fixed Dimensions

These are not configurable:

| Element | Size |
|---|---|
| Page margins | 0.5" top/bottom, 0.6" left/right |
| Name | 22pt |
| Section headings | 12pt bold |
| Company/institution | 10.5pt bold |
| Body text | 10pt |
| Contact / tech stack | 9.5pt |

---

## ATS Mode

Applicant Tracking Systems (ATS) often struggle with complex formatting. Set `"ats": true` to produce cleaner output:

```json
{
  "style": {
    "ats": true
  }
}
```

**What changes in ATS mode:**

| Feature | Normal | ATS |
|---|---|---|
| Date alignment | Right-aligned tab stops | Inline with `" - "` separator |
| Section headings | Underline border | Plain bold text |
| Tech stack | Italic, colored | Plain text with "Tech:" prefix |
| Photo | Rendered (if provided) | Skipped |

!!! note
    ATS mode only changes formatting. Your content, section order, and headings stay exactly the same.

---

## Photo

Add a profile photo to the header. When a photo is provided, the header switches from a centered layout to a two-column layout: photo on the left, name and contact info on the right.

```json
{
  "photo": "headshot.jpg"
}
```

### File Path or URL

```json
{ "photo": "photos/headshot.png" }
{ "photo": "/home/user/photos/headshot.jpg" }
{ "photo": "https://example.com/photo.jpg" }
```

URLs are fetched automatically (30-second timeout).

### Details

- Rendered at **1 inch square**
- Supported formats: **PNG, JPEG, GIF, BMP, TIFF**
- **Skipped in ATS mode** (ATS parsers can't process images)
- **Skipped when omitted** (header uses centered layout)
- Invalid paths or failed URL fetches produce a clear error message

!!! warning
    Photos are uncommon on resumes in the US, UK, and Canada. They are standard in Germany, France, and many Asian countries. Know your audience.

---

## Section Order

Control which sections appear and in what order:

```json
{
  "section_order": ["summary", "skills", "experience", "education"]
}
```

**Only listed sections are rendered.** This lets you hide sections by omitting them.

When `section_order` is omitted, all non-empty sections render in the default order:

```
summary, experience, projects, professional_projects, personal_projects,
skills, education, certifications, awards, languages
```

Duplicate entries are rejected at validation.

### Valid Section Names

```
summary          experience         projects
professional_projects                personal_projects
skills           education          certifications
awards           languages
```

---

## Custom Headings

Override any section's default heading text:

```json
{
  "headings": {
    "summary": "ABOUT ME",
    "experience": "CAREER HISTORY",
    "skills": "TECHNICAL SKILLS",
    "awards": "HONORS & RECOGNITION"
  }
}
```

Keys must be valid section names. Only sections you want to rename need to be included.

---

## Bold Keywords

List words that should be automatically bolded wherever they appear in bullet points:

```json
{
  "bold_keywords": ["Python", "FastAPI", "React", "PostgreSQL", "AWS"]
}
```

- Matching is **case-sensitive** and **exact**
- **Longer keywords match first** to avoid partial matches (`"REST API"` matches before `"API"`)
- **Special characters** like `C++` and `Node.js` are handled correctly
