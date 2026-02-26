#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_DEST_DEFAULT="${CODEX_HOME:-$HOME/.codex}/skills"
AGENTS_DEST_DEFAULT="$HOME/.agents/skills"
DEST_DEFAULT="$CODEX_DEST_DEFAULT"
DEST="$DEST_DEFAULT"
TARGET="codex"
FORCE=0
DRY_RUN=0
LIST_ONLY=0
INSTALL_ALL=0
SYMLINK=0

declare -a SELECTED_GROUPS=()
declare -a SKILLS=()
declare -a AVAILABLE_SKILLS=()

declare -a SKILL_GROUPS=(
  "experts"
  "quality"
  "planning"
  "platform"
  "marketing"
  "frontend"
  "languages"
  "seo"
  "ads"
  "blog"
  "devops"
  "fullstack"
  "database"
  "kotlin"
  "typescript"
  "code"
  "vue"
  "react"
  "prompt"
  "test"
  "feature"
  "swift"
  "axiom"
)

load_available_skills() {
  local skill
  AVAILABLE_SKILLS=()
  while IFS= read -r skill; do
    [[ -n "$skill" ]] || continue
    AVAILABLE_SKILLS+=("$skill")
  done < <(find "$REPO_ROOT" -mindepth 1 -maxdepth 1 -type d \
    ! -name '.git' \
    ! -name '.claude' \
    ! -name 'docs' \
    -exec test -f '{}/SKILL.md' ';' -print \
    | xargs -n1 basename \
    | sort)
}

group_names_csv() {
  local IFS=", "
  echo "${SKILL_GROUPS[*]}"
}

emit_if_available() {
  local target="$1"
  local skill
  for skill in "${AVAILABLE_SKILLS[@]}"; do
    if [[ "$skill" == "$target" ]]; then
      echo "$skill"
      return
    fi
  done
}

collect_by_prefix() {
  local prefix="$1"
  local skill
  for skill in "${AVAILABLE_SKILLS[@]}"; do
    if [[ "$skill" == "$prefix" || "$skill" == "$prefix"-* ]]; then
      echo "$skill"
    fi
  done
}

print_usage() {
  cat <<USAGE
Usage: ./install-skills.sh [options]

Install Codex skills from this repository into your local Codex skills directory.

Options:
  --all                  Install all skills (default when no filters are set)
  --group <name>         Install a skill group: $(group_names_csv) (repeatable)
  --skill <name>         Install a specific skill directory name (repeatable)
  --target <name>        Install target: codex or agents (default: codex)
  --agents               Shortcut for --target agents
  --dest <path>          Destination skills directory (default: $DEST_DEFAULT)
  --force                Overwrite existing installed skills
  --symlink              Symlink skills to this repo instead of copying
  --dry-run              Show what would be installed without copying
  --list                 List available groups and skills
  -h, --help             Show this help message

Examples:
  ./install-skills.sh --all
  ./install-skills.sh --target agents --all
  ./install-skills.sh --agents --group seo
  ./install-skills.sh --group seo
  ./install-skills.sh --group ads --group blog
  ./install-skills.sh --skill seo --skill ads-google
  ./install-skills.sh --group seo --force
  ./install-skills.sh --group blog --symlink
USAGE
}

print_list() {
  local group
  local skill
  local group_skills_text

  echo "Groups and skills:"
  for group in "${SKILL_GROUPS[@]}"; do
    echo "$group:"
    group_skills_text="$(collect_group_skills "$group")"
    if [[ -z "$group_skills_text" ]]; then
      echo "  (none)"
      continue
    fi
    while IFS= read -r skill; do
      [[ -n "$skill" ]] || continue
      echo "  - $skill"
    done <<< "$group_skills_text"
  done
}

collect_group_skills() {
  local group="$1"
  case "$group" in
    experts)
      emit_if_available "react-expert"
      emit_if_available "vue-expert"
      emit_if_available "swift-expert"
      emit_if_available "kotlin-specialist"
      emit_if_available "typescript-pro"
      emit_if_available "prompt-engineer"
      ;;
    quality)
      emit_if_available "code-reviewer"
      emit_if_available "code-documenter"
      emit_if_available "test-master"
      ;;
    planning)
      emit_if_available "feature-forge"
      emit_if_available "fullstack-guardian"
      ;;
    platform)
      emit_if_available "devops-engineer"
      emit_if_available "database-optimizer"
      ;;
    marketing)
      collect_by_prefix "seo"
      collect_by_prefix "ads"
      collect_by_prefix "blog"
      ;;
    frontend)
      emit_if_available "react-expert"
      emit_if_available "vue-expert"
      ;;
    languages)
      emit_if_available "kotlin-specialist"
      emit_if_available "swift-expert"
      emit_if_available "typescript-pro"
      ;;
    seo|ads|blog|devops|fullstack|database|kotlin|typescript|code|vue|react|prompt|test|feature|swift|axiom)
      collect_by_prefix "$group"
      ;;
    *)
      echo "Error: unknown group '$group' (valid: $(group_names_csv))" >&2
      exit 1
      ;;
  esac
}

install_one() {
  local skill="$1"
  local src="$REPO_ROOT/$skill"
  local dst="$DEST/$skill"

  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "Error: '$skill' is not a valid skill directory in this repo" >&2
    exit 1
  fi

  if [[ -d "$dst" && "$FORCE" -eq 0 ]]; then
    echo "Skip: $skill (already exists at $dst; use --force to overwrite)"
    return
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    if [[ -d "$dst" && "$FORCE" -eq 1 ]]; then
      if [[ "$SYMLINK" -eq 1 ]]; then
        echo "Would overwrite with symlink: $skill -> $dst -> $src"
      else
        echo "Would overwrite: $skill -> $dst"
      fi
    else
      if [[ "$SYMLINK" -eq 1 ]]; then
        echo "Would symlink: $skill -> $dst -> $src"
      else
        echo "Would install: $skill -> $dst"
      fi
    fi
    return
  fi

  if [[ -d "$dst" ]]; then
    rm -rf "$dst"
  fi

  if [[ "$SYMLINK" -eq 1 ]]; then
    ln -s "$src" "$dst"
    echo "Symlinked: $skill -> $dst -> $src"
  else
    cp -R "$src" "$dst"
    echo "Installed: $skill -> $dst"
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
      INSTALL_ALL=1
      shift
      ;;
    --group)
      [[ $# -ge 2 ]] || { echo "Error: --group requires a value" >&2; exit 1; }
      SELECTED_GROUPS+=("$2")
      shift 2
      ;;
    --skill)
      [[ $# -ge 2 ]] || { echo "Error: --skill requires a value" >&2; exit 1; }
      SKILLS+=("$2")
      shift 2
      ;;
    --target)
      [[ $# -ge 2 ]] || { echo "Error: --target requires a value" >&2; exit 1; }
      case "$2" in
        codex)
          TARGET="codex"
          DEST_DEFAULT="$CODEX_DEST_DEFAULT"
          DEST="$DEST_DEFAULT"
          ;;
        agents)
          TARGET="agents"
          DEST_DEFAULT="$AGENTS_DEST_DEFAULT"
          DEST="$DEST_DEFAULT"
          ;;
        *)
          echo "Error: invalid --target '$2' (valid: codex, agents)" >&2
          exit 1
          ;;
      esac
      shift 2
      ;;
    --agents)
      TARGET="agents"
      DEST_DEFAULT="$AGENTS_DEST_DEFAULT"
      DEST="$DEST_DEFAULT"
      shift
      ;;
    --dest)
      [[ $# -ge 2 ]] || { echo "Error: --dest requires a path" >&2; exit 1; }
      DEST="$2"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --symlink)
      SYMLINK=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --list)
      LIST_ONLY=1
      shift
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      echo "Error: unknown option '$1'" >&2
      print_usage
      exit 1
      ;;
  esac
done

load_available_skills

if [[ "$LIST_ONLY" -eq 1 ]]; then
  print_list
  exit 0
fi

mkdir -p "$DEST"

skills_file="$(mktemp)"
trap 'rm -f "$skills_file"' EXIT

if [[ "$INSTALL_ALL" -eq 1 || ( -z "${SELECTED_GROUPS[*]-}" && -z "${SKILLS[*]-}" ) ]]; then
  printf "%s\n" "${AVAILABLE_SKILLS[@]}" >> "$skills_file"
fi

if [[ -n "${SELECTED_GROUPS[*]-}" ]]; then
  for g in "${SELECTED_GROUPS[@]}"; do
    collect_group_skills "$g" >> "$skills_file"
  done
fi

if [[ -n "${SKILLS[*]-}" ]]; then
  for s in "${SKILLS[@]}"; do
    echo "$s" >> "$skills_file"
  done
fi

sort -u "$skills_file" -o "$skills_file"

if [[ ! -s "$skills_file" ]]; then
  echo "No skills selected for installation."
  exit 0
fi

echo "Destination: $DEST"
echo "Target: $TARGET"
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "Mode: dry-run"
fi
if [[ "$SYMLINK" -eq 1 ]]; then
  echo "Mode: symlink"
fi

while IFS= read -r skill; do
  [[ -n "$skill" ]] || continue
  install_one "$skill"
done < "$skills_file"

echo
echo "Done. Restart Codex to pick up installed skills."
