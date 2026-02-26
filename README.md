# codex-skills

Codex-format skills for SEO, blog, paid ads, DevOps, full-stack implementation, feature specification, database performance, Kotlin, TypeScript, Vue, React, prompt engineering, testing, and documentation workflows, converted from Claude-style skills and organized for easy reuse.

## What Is In This Repo

- `ads/`: Top-level paid ads orchestrator skill with shared references, research notes, and scripts
- `ads-*`: Specialized sub-skills (audit, platform deep-dives, budget, planning, and competitor analysis)
- `blog/`: Top-level blog orchestrator skill with shared references, templates, and scripts
- `blog-*`: Specialized sub-skills (write, rewrite, analyze, strategy, schema, and more)
- `seo/`: Top-level SEO orchestrator skill with shared references, templates, and scripts
- `seo-*`: Specialized sub-skills (audit, content, schema, technical, sitemap, GEO, and more)
- `devops-engineer/`: CI/CD, infrastructure-as-code, container, and operations engineering skill
- `fullstack-guardian/`: End-to-end feature implementation skill across frontend, backend, and security
- `database-optimizer/`: Database performance analysis and optimization skill
- `kotlin-specialist/`: Kotlin/KMP/Compose/Ktor implementation skill
- `typescript-pro/`: Advanced TypeScript type-system and tooling skill
- `code-documenter/`: Code and API documentation generation skill
- `code-reviewer/`: Structured code review and quality audit skill
- `vue-expert/`: Vue 3/Nuxt/Pinia implementation skill
- `react-expert/`: React 19/Server Components implementation skill
- `prompt-engineer/`: LLM prompt design, optimization, and evaluation skill
- `test-master/`: Comprehensive test strategy and implementation skill
- `feature-forge/`: Feature discovery and specification skill
- `docs/`: Contributor and migration documentation

## Current Skill Set

```text
ads/
├── ads
├── ads-audit
├── ads-google
├── ads-meta
├── ads-youtube
├── ads-linkedin
├── ads-tiktok
├── ads-microsoft
├── ads-creative
├── ads-landing
├── ads-budget
├── ads-plan
└── ads-competitor

blog/
├── blog
├── blog-write
├── blog-rewrite
├── blog-analyze
├── blog-brief
├── blog-calendar
├── blog-strategy
├── blog-outline
├── blog-seo-check
├── blog-schema
├── blog-repurpose
├── blog-geo
├── blog-audit
└── blog-chart (internal helper)

seo/
├── seo
├── seo-audit
├── seo-page
├── seo-technical
├── seo-content
├── seo-schema
├── seo-sitemap
├── seo-images
├── seo-geo
├── seo-plan
├── seo-programmatic
├── seo-competitor-pages
└── seo-hreflang

devops/
└── devops-engineer

fullstack/
└── fullstack-guardian

database/
└── database-optimizer

kotlin/
└── kotlin-specialist

typescript/
└── typescript-pro

code/
├── code-documenter
└── code-reviewer

vue/
└── vue-expert

react/
└── react-expert

prompt/
└── prompt-engineer

test/
└── test-master

feature/
└── feature-forge
```

## Repository Layout

```text
.
├── README.md
├── CONTRIBUTING.md
├── docs/
│   ├── skill-format.md
│   └── migration-claude-to-codex.md
├── ads/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   ├── research-sources/
│   └── scripts/
├── ads-*/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── assets/ (optional, used by `ads-plan`)
├── blog/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   ├── templates/
│   └── scripts/
├── blog-*/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── seo/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/
│   ├── references/
│   └── scripts/
├── seo-*/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── devops-engineer/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── fullstack-guardian/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── database-optimizer/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── kotlin-specialist/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── typescript-pro/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── code-documenter/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── code-reviewer/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── vue-expert/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── react-expert/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── prompt-engineer/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── test-master/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
└── feature-forge/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
```

## Quick Start

1. Review [docs/skill-format.md](docs/skill-format.md) for required structure.
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) for conventions.
3. Follow [docs/migration-claude-to-codex.md](docs/migration-claude-to-codex.md) when porting additional skills.

## Codex Multi-Agent Support

This repo is designed to work with Codex multi-agent orchestration for heavy audits.

1. Enable multi-agent in Codex via `/experimental` or `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

2. Use orchestrator skills (`$seo`, `$blog`, `$ads`) and domain skills (for example, `$devops-engineer`) for top-level tasks.
3. For broad audits, run specialist checks in parallel with `spawn_agent`, then consolidate with `wait`.
4. Prefer Codex built-in agent roles for consistency:
   - `explorer` for repository/data discovery
   - `worker` for execution and artifact generation
   - `default` for synthesis and final report delivery

## Install Locally

Use the bundled installer to copy skills from this repo into your local Codex skills directory (`$CODEX_HOME/skills`, default `~/.codex/skills`).

```bash
# install all skills
./install-skills.sh --all

# install by group
./install-skills.sh --group seo
./install-skills.sh --group ads --group blog
./install-skills.sh --group devops
./install-skills.sh --group fullstack
./install-skills.sh --group database
./install-skills.sh --group kotlin
./install-skills.sh --group typescript
./install-skills.sh --group code
./install-skills.sh --group vue
./install-skills.sh --group react
./install-skills.sh --group prompt
./install-skills.sh --group test
./install-skills.sh --group feature

# install specific skills
./install-skills.sh --skill seo --skill ads-google

# preview without copying
./install-skills.sh --group seo --dry-run

# symlink instead of copy (useful while iterating in this repo)
./install-skills.sh --group blog --symlink
```

Then restart Codex to pick up installed skills.

## Design Principles

- Keep `SKILL.md` focused on behavior, trigger rules, and operational steps.
- Keep reusable data in `assets/` and static references in `references/`.
- Keep executable helpers in `scripts/`.
- Treat `agents/openai.yaml` as display metadata for the skill surface.

## Status

This is an early scaffolded repo with a complete first batch of SEO skills and contributor docs in place.

## Attribution

The SEO skills in this repository were originally sourced from:

- [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)

The blog skills in this repository were originally sourced from:

- [AgriciDaniel/claude-blog](https://github.com/AgriciDaniel/claude-blog)

The paid ads skills in this repository were originally sourced from:

- [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads)

The DevOps Engineer skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/devops-engineer)

The Fullstack Guardian skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/fullstack-guardian)

The Database Optimizer skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/blob/main/skills/database-optimizer/SKILL.md)

The Kotlin Specialist skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/kotlin-specialist)

The TypeScript Pro skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/typescript-pro)

The Code Documenter skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/code-documenter)

The Code Reviewer skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/code-reviewer)

The Vue Expert skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/blob/main/skills/vue-expert/SKILL.md)

The React Expert skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/react-expert)

The Prompt Engineer skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/prompt-engineer)

The Test Master skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/blob/main/skills/test-master/SKILL.md)

The Feature Forge skill in this repository was originally sourced from:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/feature-forge)
