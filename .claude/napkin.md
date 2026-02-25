# Napkin

## Corrections
| Date | Source | What Went Wrong | What To Do Instead |
|------|--------|----------------|-------------------|
| 2026-02-25 | self | Started repo exploration before confirming napkin file existed. | Always check/create `.claude/napkin.md` immediately at session start in this repo. |

## User Preferences
- Keep scaffolding pragmatic and lightweight.

## Patterns That Work
- Skill packages in this repo follow a consistent layout: `SKILL.md`, optional `agents/`, `assets/`, `references/`, `scripts/`.
- Using `rg --files` quickly reveals repo structure and coverage gaps.

## Patterns That Don't Work
- Assuming global docs exist in fresh skill repos.

## Domain Notes
- This repo contains Codex-format skills, primarily SEO-related modules.
- Immediate value comes from contributor docs and reusable templates for adding new skills.
| 2026-02-25 | self | Needed repo-wide contributor context but there was no root docs scaffold. | Create lightweight root docs (`README.md`, `CONTRIBUTING.md`, `docs/*`) before deeper refactors. |

## Patterns That Work
- A short `migration-claude-to-codex.md` checklist speeds consistent skill ports.
- Capture upstream source attribution in root docs early when migrating third-party skill packs.
| 2026-02-25 | self | Used `in` as an `awk` variable name and hit syntax errors on BSD awk. | Avoid reserved words in awk (`in`); use neutral names like `in_fm`. |

## Patterns That Work
- For imported skill packs with shared resources, keep one shared orchestrator directory (e.g., `blog/`) and patch sub-skill paths to `../blog/...`.
| 2026-02-25 | self | Initial multi-hunk patch failed due context mismatch. | Re-open target files and apply precise replacements in smaller steps when imported files drift from expected context. |
| 2026-02-25 | self | Imported ads scripts had unguarded URL navigation/fetch behavior. | Apply shared URL/public-host validation + redirect/resource guard pattern to every new network script during import. |

## Patterns That Work
- During skill imports, run security hardening as part of conversion rather than as a separate cleanup pass.
