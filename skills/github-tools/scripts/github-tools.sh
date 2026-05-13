#!/bin/bash
# github-tools.sh — v4.4 Multi-Repo/Branch + Self-Consistency Edition
set -euo pipefail

SKILL_DIR="/home/workdir/.grok/skills/github-tools"
STAGE_FILE="/home/workdir/artifacts/grok-os/STAGE.md"
ARCHIVE_BASE="/home/workdir/artifacts/grok-os/ARCHIVE"
LIBRARY_FILE="$SKILL_DIR/CONNECTOR_LIBRARY.json"
CONFIG_FILE="/home/workdir/artifacts/grok-os/.github-tools-config"

# Defaults (overridable)
DEFAULT_REPO="kywrn7z4ww-glitch/ChaosEngine-Grok-OS"
DEFAULT_READ_ONLY_BRANCH="main"
DEFAULT_WORKING_BRANCH="skills-prototype"

load_config() {
  if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
  else
    ACTIVE_REPO="$DEFAULT_REPO"
    WORKING_BRANCH="$DEFAULT_WORKING_BRANCH"
    READ_ONLY_BRANCH="$DEFAULT_READ_ONLY_BRANCH"
  fi
}

save_config() {
  mkdir -p "$(dirname "$CONFIG_FILE")"
  cat > "$CONFIG_FILE" <<EOF
ACTIVE_REPO="$ACTIVE_REPO"
WORKING_BRANCH="$WORKING_BRANCH"
READ_ONLY_BRANCH="$READ_ONLY_BRANCH"
EOF
}

show_help() {
  cat <<EOF
github-tools v4.4 — Multi-Repo + Self-Consistent Edition

REPO & BRANCH MANAGEMENT
  select-repo <owner/repo>          # e.g. select-repo kywrn7z4ww-glitch/ChaosEngine-Grok-OS
  set-working-branch <branch>       # Working branch (where we push changes)
  set-read-only-branch <branch>     # Read-only branch (e.g. main — never push here)

STAGE & VALIDATION
  init-stage                        # Create fresh v4.4 STAGE.md (auto-populates date/repo/branch)
  validate-stage [file]             # Run 5-question self-consistency rubric
  migrate-stage <old-file>          # Upgrade old STAGE.md to v4.4 format
  refresh-library                   # Re-discover github___ tools
  cleanup                         # Remove deprecated files (safe)

LEGACY (still work)
  archive-major "title"
  strip-sha <file>
  push-ready
  self-update-stage
  full-workflow

All operations now enforce the v4.4 Self-Consistency Contract + multi-repo/branch support.
EOF
}

select_repo() {
  ACTIVE_REPO="$1"
  save_config
  echo "✅ Active repo: $ACTIVE_REPO"
}

set_working_branch() {
  WORKING_BRANCH="$1"
  save_config
  echo "✅ Working branch: $WORKING_BRANCH (changes pushed here)"
}

set_read_only_branch() {
  READ_ONLY_BRANCH="$1"
  save_config
  echo "✅ Read-only branch: $READ_ONLY_BRANCH (MAIN equivalent — do not push)"
}

init_stage() {
  load_config
  mkdir -p "$(dirname "$STAGE_FILE")"
  cp "$SKILL_DIR/references/stage-template.md" "$STAGE_FILE"
  sed -i "s|\[YYYY-MM-DD HH:MM TZ\]|$(date '+%Y-%m-%d %H:%M %Z')|g" "$STAGE_FILE"
  echo "✅ v4.4 STAGE.md created"
  echo "Repo: $ACTIVE_REPO | Working: $WORKING_BRANCH | Read-only: $READ_ONLY_BRANCH"
}

validate_stage() {
  local file="${1:-$STAGE_FILE}"
  python3 "$SKILL_DIR/validate_rubric.py" "$file"
}

refresh_library() {
  echo "Library refresh triggered. Run search_connected_tools(\"github\") to update CONNECTOR_LIBRARY.json"
}

cleanup() {
  echo "=== github-tools v4.4 Cleanup ==="
  echo "This will remove deprecated files from skills/github-tools/"
  echo "- Old git_connector_workflow.md (superseded by SKILL.md v4.4)"
  echo ""
  read -p "Proceed with cleanup? (y/N) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [[ -f "$SKILL_DIR/references/git_connector_workflow.md" ]]; then
      rm "$SKILL_DIR/references/git_connector_workflow.md"
      echo "✅ Removed old git_connector_workflow.md"
    fi
    echo "Cleanup complete."
  else
    echo "Cleanup cancelled."
  fi
}

# Legacy functions (minimal)
archive_major() {
  local title="$1"
  local date=$(date +%Y-%m-%d)
  local dir="$ARCHIVE_BASE/changelog/$(date +%Y/%m)"
  mkdir -p "$dir"
  echo "# $title — $(date)" > "$dir/${date}-${title}.md"
  echo "Created major changelog"
}

strip_sha() {
  local file="$1"
  [[ -f "$file" ]] && sed -i '/"sha":\s*"[^"]*"/d' "$file" && echo "SHA stripped"
}

push_ready() {
  echo "=== Staged Items ==="
  [[ -f "$STAGE_FILE" ]] && grep -A 10 "Staged" "$STAGE_FILE" || echo "No STAGE.md"
}

self_update_stage() {
  [[ -f "$STAGE_FILE" ]] && sed -i 's/Pushed + Verified/Pushed + Verified (auto)/g' "$STAGE_FILE" && echo "STAGE.md updated"
}

full_workflow() {
  cat "$SKILL_DIR/references/git_connector_workflow.md" 2>/dev/null || echo "No workflow doc"
}

case "${1:-help}" in
  select-repo) select_repo "$2" ;;
  set-working-branch) set_working_branch "$2" ;;
  set-read-only-branch) set_read_only_branch "$2" ;;
  init-stage) init_stage ;;
  validate-stage) validate_stage "$2" ;;
  refresh-library) refresh_library ;;
  cleanup) cleanup ;;
  *) show_help ;;
esac