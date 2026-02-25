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

- `ads`
- `ads-audit`
- `ads-google`
- `ads-meta`
- `ads-youtube`
- `ads-linkedin`
- `ads-tiktok`
- `ads-microsoft`
- `ads-creative`
- `ads-landing`
- `ads-budget`
- `ads-plan`
- `ads-competitor`
- `blog`
- `blog-write`
- `blog-rewrite`
- `blog-analyze`
- `blog-brief`
- `blog-calendar`
- `blog-strategy`
- `blog-outline`
- `blog-seo-check`
- `blog-schema`
- `blog-repurpose`
- `blog-geo`
- `blog-audit`
- `blog-chart` (internal helper)
- `seo`
- `seo-audit`
- `seo-page`
- `seo-technical`
- `seo-content`
- `seo-schema`
- `seo-sitemap`
- `seo-images`
- `seo-geo`
- `seo-plan`
- `seo-programmatic`
- `seo-competitor-pages`
- `seo-hreflang`

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
