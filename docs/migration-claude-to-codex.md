# Migration Guide: Claude Skills -> Codex Skills

## Goal

Port a Claude-style skill into this Codex repository without losing intent, triggers, or operational safeguards.

## Source Attribution

Initial SEO skill conversions in this repo were sourced from:

- [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)

Initial blog skill conversions in this repo were sourced from:

- [AgriciDaniel/claude-blog](https://github.com/AgriciDaniel/claude-blog)

## Migration Checklist

1. Create a new skill directory in kebab-case.
2. Move core instructions into `SKILL.md` frontmatter + body.
3. Normalize trigger language for Codex-style invocation.
4. Move reusable prompt chunks into `assets/`.
5. Move static standards/checklists into `references/`.
6. Move executable logic into `scripts/`.
7. Add `agents/openai.yaml` interface metadata.
8. Validate all relative paths referenced by `SKILL.md`.
9. Add the skill to root `README.md`.

## Common Conversion Rules

- Replace provider-specific tool names with generic operational steps.
- Convert slash-command examples into intent labels (not required CLI syntax).
- Keep orchestration order explicit when multiple sub-skills are involved.
- Add hard limits for crawling/scraping/parallel operations.
- Keep output files/report sections concrete.

## Example Mapping

- Claude "agent prompt" -> Codex `SKILL.md` body sections
- Claude "sub-agent config" -> Codex `agents/openai.yaml`
- Claude embedded constants -> Codex `references/` or `assets/`
- Claude helper code snippets -> Codex `scripts/`

## Definition Of Done

A migrated skill is ready when:

- Trigger conditions are unambiguous
- Workflow steps are deterministic
- Safety constraints are explicit
- Referenced files exist and are scoped locally
- Outputs are concrete enough to evaluate
