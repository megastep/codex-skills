# Skill Format (Codex)

## Minimal Skill

```text
<skill-name>/
├── SKILL.md
└── agents/
    └── openai.yaml
```

## `SKILL.md` Template

```markdown
---
name: my-skill
description: >
  One to three sentences explaining what this skill does, when to trigger it,
  and expected output.
---

# My Skill

## Trigger

Describe the user intents that should activate this skill.

## Inputs

List required and optional inputs.

## Process

1. Step one.
2. Step two.
3. Step three.

## Outputs

Define exact output shape or report sections.

## Constraints

Include safety limits, timeouts, hard stops, and non-goals.
```

## `agents/openai.yaml` Template

```yaml
interface:
  display_name: "My Skill"
  short_description: "Help with <domain> tasks and workflows"
  default_prompt: "Use $my-skill to handle this task and return <expected result>."
```

## Optional Package Content

- `assets/`: prompt fragments, templates, structured defaults
- `references/`: standards, threshold tables, domain guides
- `scripts/`: executable helpers called by the skill

## Style Guidelines

- Use imperative steps for workflows.
- Prefer concrete limits (`max pages: 500`, `timeout: 30s`).
- Keep sections scannable and deterministic.
- Avoid tool assumptions not available in the runtime.
