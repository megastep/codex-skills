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
| 2026-02-25 | self | Used reserved Bash variable name `GROUPS` in installer and it collided with shell group IDs. | Avoid special Bash variable names (`GROUPS`, `RANDOM`, etc.) in scripts; use explicit names like `SELECTED_GROUPS`. |
| 2026-02-25 | self | Empty array handling with `set -u` broke loops on this shell. | Guard array reads with `${arr[*]-}` checks before iterating under nounset.
## Patterns That Work
- Installer ergonomics improve with both copy and symlink modes; symlink mode is best for active skill development loops.

| 2026-02-26 | self | Multi-agent docs were fetched but not wired into orchestrator SKILL.md guidance in first pass. | After importing skills, explicitly add Codex `spawn_agent` + `wait` role mapping (`explorer`/`worker`/`default`) in top-level orchestrators and README. |

| 2026-02-26 | user | User explicitly requested no delete operations in the repo. | Avoid delete commands in `/Users/megastep/src/codex-skills`; prefer additive/overwrite-safe edits only. |

| 2026-02-26 | self | Used Python for simple markdown edits where `apply_patch` was sufficient. | Prefer `apply_patch` for single-file textual edits; reserve scripting for bulk/generated transformations. |

| 2026-02-26 | self | Reintroduced Bash reserved var collision by naming a custom array `GROUPS` during installer refactor. | Never use `GROUPS`; standardize on `SKILL_GROUPS` for installer group metadata. |

| 2026-02-26 | self | Installer refactor tests initially failed due reserved variable collision before full validation. | Always run `./install-skills.sh --list` and at least one grouped `--dry-run` immediately after installer edits. |
