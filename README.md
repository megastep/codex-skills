# codex-skills

Codex-format skills for SEO, blog, and paid ads workflows, converted from Claude-style skills and organized for easy reuse.

## What Is In This Repo

- `ads/`: Top-level paid ads orchestrator skill with shared references, research notes, and scripts
- `ads-*`: Specialized sub-skills (audit, platform deep-dives, budget, planning, and competitor analysis)
- `blog/`: Top-level blog orchestrator skill with shared references, templates, and scripts
- `blog-*`: Specialized sub-skills (write, rewrite, analyze, strategy, schema, and more)
- `seo/`: Top-level SEO orchestrator skill with shared references, templates, and scripts
- `seo-*`: Specialized sub-skills (audit, content, schema, technical, sitemap, GEO, and more)
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
└── seo-*/
    ├── SKILL.md
    └── agents/openai.yaml
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

2. Use orchestrator skills (`$seo`, `$blog`, `$ads`) for top-level tasks.
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
