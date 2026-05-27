# Examples

Complete resume examples in JSON and YAML.

---

## Full JSON Example

```json
{
  "$schema": "https://raw.githubusercontent.com/mdfarhankc/resumecraft/main/schema.json",
  "name": "Jane Doe",
  "contact": {
    "location": "New York, NY",
    "email": "jane@example.com",
    "phone": "+1-234-567-8900",
    "links": [
      { "label": "LinkedIn", "url": "https://linkedin.com/in/janedoe" },
      { "label": "GitHub", "url": "https://github.com/janedoe" },
      { "label": "Portfolio", "url": "https://janedoe.dev" }
    ]
  },
  "summary": "Full-stack developer with 5 years of experience building scalable web applications and distributed systems. Passionate about developer experience and open source.",
  "bold_keywords": ["Python", "FastAPI", "React", "PostgreSQL", "AWS", "Docker", "Kubernetes"],
  "experience": [
    {
      "company": "Acme Corp",
      "location": "New York, NY",
      "title": "Senior Software Engineer",
      "duration": "JAN 2022 - PRESENT",
      "bullets": [
        "Designed and deployed a FastAPI microservice handling 10K requests/sec with 99.9% uptime.",
        "Led migration from monolith to microservices, reducing deploy times by 60%.",
        "Mentored 3 junior developers through code reviews and pair programming.",
        "Built a real-time analytics dashboard using React and WebSockets."
      ]
    },
    {
      "company": "StartUp Inc",
      "location": "Remote",
      "title": "Software Engineer",
      "duration": "JUN 2020 - DEC 2021",
      "bullets": [
        "Developed Python microservices processing 500K events/day via Apache Kafka.",
        "Implemented CI/CD pipelines with GitHub Actions, cutting release cycles from weekly to daily.",
        "Designed PostgreSQL schema supporting multi-tenant SaaS architecture."
      ]
    }
  ],
  "projects": [
    {
      "name": "DataPipeline",
      "subtitle": "| Open Source",
      "tech_stack": "Python, Apache Kafka, PostgreSQL",
      "links": [
        { "label": "GitHub", "url": "https://github.com/janedoe/datapipeline" },
        { "label": "Docs", "url": "https://datapipeline.dev" }
      ],
      "bullets": [
        "Built a real-time data pipeline framework processing 1M events/day.",
        "Published as open source with 500+ GitHub stars and 20 contributors."
      ]
    },
    {
      "name": "DevDash",
      "subtitle": "| Side Project",
      "tech_stack": "React, TypeScript, D3.js",
      "links": [
        { "label": "Live Demo", "url": "https://devdash.janedoe.dev" }
      ],
      "bullets": [
        "Created a developer productivity dashboard aggregating GitHub, Jira, and Slack data.",
        "Implemented interactive charts with D3.js rendering 100K+ data points."
      ]
    }
  ],
  "skills": [
    { "category": "Languages", "items": "Python, TypeScript, Go, SQL" },
    { "category": "Backend", "items": "FastAPI, Django, Node.js, gRPC" },
    { "category": "Frontend", "items": "React, Next.js, Tailwind CSS" },
    { "category": "Data", "items": "PostgreSQL, Redis, Apache Kafka, Elasticsearch" },
    { "category": "Infrastructure", "items": "AWS, Docker, Kubernetes, Terraform, GitHub Actions" }
  ],
  "education": [
    {
      "institution": "Massachusetts Institute of Technology",
      "degree": "B.S. Computer Science",
      "duration": "2016 - 2020"
    }
  ],
  "certifications": [
    {
      "name": "AWS Solutions Architect - Associate",
      "issuer": "Amazon Web Services",
      "date": "2024",
      "links": [
        { "label": "Verify", "url": "https://aws.amazon.com/verify/12345" }
      ]
    },
    {
      "name": "Certified Kubernetes Administrator",
      "issuer": "Cloud Native Computing Foundation",
      "date": "2023"
    }
  ],
  "awards": [
    {
      "title": "Hack the Future - 1st Place",
      "issuer": "TechCrunch Disrupt",
      "date": "2023",
      "description": "Won first place for building an AI-powered accessibility tool in 48 hours."
    }
  ],
  "languages": "English - Native  |  Spanish - Professional  |  French - Conversational",
  "style": {
    "font": "calibri",
    "color": "navy",
    "spacing": "normal"
  },
  "section_order": [
    "summary",
    "experience",
    "projects",
    "skills",
    "education",
    "certifications",
    "awards",
    "languages"
  ],
  "headings": {
    "summary": "ABOUT ME"
  }
}
```

---

## Full YAML Example

```yaml
name: Jane Doe
contact:
  location: New York, NY
  email: jane@example.com
  phone: "+1-234-567-8900"
  links:
    - label: LinkedIn
      url: https://linkedin.com/in/janedoe
    - label: GitHub
      url: https://github.com/janedoe
    - label: Portfolio
      url: https://janedoe.dev

summary: >-
  Full-stack developer with 5 years of experience building
  scalable web applications and distributed systems.
  Passionate about developer experience and open source.

bold_keywords:
  - Python
  - FastAPI
  - React
  - PostgreSQL
  - AWS
  - Docker
  - Kubernetes

experience:
  - company: Acme Corp
    location: New York, NY
    title: Senior Software Engineer
    duration: JAN 2022 - PRESENT
    bullets:
      - Designed and deployed a FastAPI microservice handling 10K requests/sec.
      - Led migration from monolith to microservices, reducing deploy times by 60%.
      - Mentored 3 junior developers through code reviews and pair programming.

  - company: StartUp Inc
    location: Remote
    title: Software Engineer
    duration: JUN 2020 - DEC 2021
    bullets:
      - Developed Python microservices processing 500K events/day via Apache Kafka.
      - Implemented CI/CD pipelines with GitHub Actions.

projects:
  - name: DataPipeline
    subtitle: "| Open Source"
    tech_stack: Python, Apache Kafka, PostgreSQL
    links:
      - label: GitHub
        url: https://github.com/janedoe/datapipeline
    bullets:
      - Built a real-time data pipeline framework processing 1M events/day.
      - Published as open source with 500+ GitHub stars.

skills:
  - category: Languages
    items: Python, TypeScript, Go, SQL
  - category: Backend
    items: FastAPI, Django, Node.js, gRPC
  - category: Infrastructure
    items: AWS, Docker, Kubernetes, Terraform

education:
  - institution: Massachusetts Institute of Technology
    degree: B.S. Computer Science
    duration: 2016 - 2020

certifications:
  - name: AWS Solutions Architect - Associate
    issuer: Amazon Web Services
    date: "2024"
    links:
      - label: Verify
        url: https://aws.amazon.com/verify/12345

awards:
  - title: Hack the Future - 1st Place
    issuer: TechCrunch Disrupt
    date: "2023"
    description: Won first place for building an AI-powered accessibility tool.

languages: English - Native  |  Spanish - Professional

style:
  font: garamond
  color: forest
  spacing: compact

section_order:
  - summary
  - experience
  - projects
  - skills
  - education
  - certifications
  - awards
  - languages

headings:
  summary: ABOUT ME
```

YAML requires `pip install resumecraft[yaml]`.

---

## Minimal Example

The smallest valid resume:

=== "JSON"

    ```json
    {
      "name": "Jane Doe",
      "contact": {
        "location": "New York, NY",
        "email": "jane@example.com",
        "phone": "+1-234-567-8900"
      },
      "summary": "Software engineer with 3 years of experience."
    }
    ```

=== "YAML"

    ```yaml
    name: Jane Doe
    contact:
      location: New York, NY
      email: jane@example.com
      phone: "+1-234-567-8900"
    summary: Software engineer with 3 years of experience.
    ```

---

## ATS-Optimized Example

A resume optimized for Applicant Tracking Systems:

```json
{
  "name": "Jane Doe",
  "contact": {
    "location": "New York, NY",
    "email": "jane@example.com",
    "phone": "+1-234-567-8900",
    "links": [
      { "label": "LinkedIn", "url": "https://linkedin.com/in/janedoe" }
    ]
  },
  "summary": "Senior software engineer with expertise in Python, cloud infrastructure, and distributed systems.",
  "bold_keywords": ["Python", "AWS", "Kubernetes"],
  "experience": [
    {
      "company": "Acme Corp",
      "location": "New York, NY",
      "title": "Senior Software Engineer",
      "duration": "JAN 2022 - PRESENT",
      "bullets": [
        "Designed microservices on AWS using Python and Kubernetes.",
        "Reduced infrastructure costs by 40% through optimization."
      ]
    }
  ],
  "skills": [
    { "category": "Languages", "items": "Python, Go, SQL" },
    { "category": "Cloud", "items": "AWS (EC2, Lambda, S3, RDS), Kubernetes, Terraform" }
  ],
  "education": [
    {
      "institution": "MIT",
      "degree": "B.S. Computer Science",
      "duration": "2016 - 2020"
    }
  ],
  "style": {
    "font": "calibri",
    "color": "black",
    "spacing": "normal",
    "ats": true
  }
}
```
