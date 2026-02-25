# Contributing

## Scope

This repository contains Codex-format skills. A skill package is a directory with:

- `SKILL.md` (required)
- `agents/openai.yaml` (recommended)
- Optional: `assets/`, `references/`, `scripts/`

## Authoring Rules

1. Keep each skill single-purpose.
2. Define clear trigger cues in the `description` frontmatter and body.
3. Prefer deterministic workflows over vague guidance.
4. Use relative file references inside each skill package.
5. Store large reusable prompts/templates in `assets/`.
6. Store factual guidance and standards in `references/`.
7. Keep scripts small and focused; document invocation in `SKILL.md`.

## Naming

- Use lowercase kebab-case for skill directory names.
- Match frontmatter `name` to the skill command name where possible.
- Use concise, behavior-oriented descriptions.

## Suggested Review Checklist

- Does the skill have a clear trigger and outcome?
- Are required files present and paths valid?
- Are referenced scripts/assets/references actually in the package?
- Are operations safe by default (timeouts, limits, constraints)?
- Is output format explicit enough for downstream use?

## Adding A New Skill

1. Create `<skill-name>/SKILL.md` with frontmatter + instructions.
2. Add `<skill-name>/agents/openai.yaml` metadata.
3. Add optional `assets/`, `references/`, and `scripts/` as needed.
4. Update the root `README.md` skill list.
5. If the skill is a migration, follow `docs/migration-claude-to-codex.md`.

## Pull Request Guidance

Include the following in your PR description:

- Skill(s) added or modified
- Trigger behavior and expected outputs
- New scripts/assets/references added
- Any known limitations or follow-up work
