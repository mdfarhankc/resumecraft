# Field Reference

Complete reference for every field in the resume data format. All models use strict validation (`extra="forbid"`) - unknown field names raise an error.

---

## Resume (top-level)

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | **Yes** | | Full name at the top of the resume |
| `contact` | [Contact](#contact) | **Yes** | | Location, email, phone, and links |
| `summary` | string | **Yes** | | Professional summary paragraph |
| `photo` | string | No | `null` | Path or URL to a profile photo ([details](styling.md#photo)) |
| `bold_keywords` | string[] | No | `[]` | Words auto-bolded in all bullet points |
| `experience` | [Experience](#experience)[] | No | `[]` | Work experience entries |
| `projects` | [Project](#project)[] | No | `[]` | Unified projects section |
| `professional_projects` | [Project](#project)[] | No | `[]` | Professional/client projects |
| `personal_projects` | [Project](#project)[] | No | `[]` | Side projects and open source |
| `skills` | [Skill](#skill)[] | No | `[]` | Categorized skill lists |
| `education` | [Education](#education)[] | No | `[]` | Degrees and institutions |
| `certifications` | [Certification](#certification)[] | No | `[]` | Certifications with optional links |
| `awards` | [Award](#award)[] | No | `[]` | Awards with optional description |
| `languages` | string | No | `""` | Language proficiencies (free text) |
| `section_order` | string[] | No | `null` | Controls which sections appear and in what order |
| `headings` | object | No | `{}` | Override default section heading text |
| `style` | [StyleOptions](#styleoptions) | No | `{}` | Font, color, spacing, and ATS settings |
| `$schema` | string | No | | Editor autocomplete hint (ignored at runtime) |
| `_version` | string | No | | ResumeCraft version (ignored at runtime) |

---

## Contact

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `location` | string | **Yes** | | City, state/country |
| `email` | string | **Yes** | | Email address (rendered as a `mailto:` link) |
| `phone` | string | **Yes** | | Phone number |
| `links` | [Link](#link)[] | No | `[]` | Additional links (LinkedIn, GitHub, portfolio) |

All required fields must be non-empty (minimum 1 character).

---

## Link

| Field | Type | Required | Description |
|---|---|---|---|
| `label` | string | **Yes** | Display text (e.g., "LinkedIn", "GitHub") |
| `url` | string | **Yes** | Full URL |

Used in `contact.links`, `project.links`, and `certification.links`.

---

## Experience

| Field | Type | Required | Description |
|---|---|---|---|
| `company` | string | **Yes** | Company name |
| `location` | string | **Yes** | City, country or "Remote" |
| `title` | string | **Yes** | Job title |
| `duration` | string | **Yes** | Time period (e.g., `"JAN 2022 - PRESENT"`) |
| `bullets` | string[] | **Yes** | Accomplishments and responsibilities |

```json
{
  "company": "Acme Corp",
  "location": "New York, NY",
  "title": "Senior Software Engineer",
  "duration": "JAN 2022 - PRESENT",
  "bullets": [
    "Designed a microservice handling 10K requests/sec.",
    "Reduced deploy times by 60% through CI/CD improvements."
  ]
}
```

---

## Project

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | **Yes** | | Project name |
| `subtitle` | string | **Yes** | | Short description (e.g., `"\| Open Source"`) |
| `tech_stack` | string | No | `null` | Technologies used (rendered in italic) |
| `links` | [Link](#link)[] | No | `[]` | Project links (GitHub, live demo, docs) |
| `bullets` | string[] | **Yes** | | What you built and the impact |

```json
{
  "name": "DataPipeline",
  "subtitle": "| Open Source",
  "tech_stack": "Python, Apache Kafka, PostgreSQL",
  "links": [
    { "label": "GitHub", "url": "https://github.com/you/datapipeline" },
    { "label": "Docs", "url": "https://datapipeline.dev" }
  ],
  "bullets": [
    "Built a real-time data pipeline processing 1M events/day."
  ]
}
```

---

## Skill

| Field | Type | Required | Description |
|---|---|---|---|
| `category` | string | **Yes** | Skill group name (e.g., "Backend", "DevOps") |
| `items` | string | **Yes** | Comma-separated skills |

```json
{ "category": "Backend", "items": "Python (FastAPI, Django), Node.js, Go" }
```

---

## Education

| Field | Type | Required | Description |
|---|---|---|---|
| `institution` | string | **Yes** | University or school name |
| `degree` | string | **Yes** | Degree and field of study |
| `duration` | string | **Yes** | Time period (e.g., `"2016 - 2020"`) |

---

## Certification

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | **Yes** | | Certification name |
| `issuer` | string | **Yes** | | Issuing organization |
| `date` | string | **Yes** | | Year or date obtained |
| `links` | [Link](#link)[] | No | `[]` | Verification or credential links |

---

## Award

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `title` | string | **Yes** | | Award name |
| `issuer` | string | **Yes** | | Awarding organization |
| `date` | string | **Yes** | | Year received |
| `description` | string | No | `null` | Brief description |

---

## StyleOptions

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `font` | string | No | `"calibri"` | Font family |
| `color` | string | No | `"black"` | Color theme |
| `spacing` | string | No | `"normal"` | Spacing preset |
| `ats` | boolean | No | `false` | ATS-friendly mode |

See [Styling](styling.md) for all available values and what they look like.

---

## Valid Section Names

Used in `section_order` and `headings`:

```
summary, experience, projects, professional_projects, personal_projects,
skills, education, certifications, awards, languages
```
