#!/bin/bash
# github-tools.sh — Executable helper for the github-tools skill
# Provides quick commands for the full connector workflow

set -euo pipefail

SKILL_DIR="/home/workdir/.grok/skills/github-tools"
STAGE_FILE="/home/workdir/artifacts/grok-os/STAGE.md"
ARCHIVE_BASE="/home/workdir/artifacts/grok-os/ARCHIVE"

show_help() {
  cat <<EOF
github-tools — ChaosEngine-Grok-OS GitHub Connector Workflow Helper

Usage:
  ./scripts/github-tools.sh init-stage          # Create fresh STAGE.md from template
  ./scripts/github-tools.sh show-stage          # Display current STAGE.md
  ./scripts/github-tools.sh archive-major "title"   # Create major changelog folder + entry
  ./scripts/github-tools.sh archive-minor "title"   # Append to today's minor_fixes file
  ./scripts/github-tools.sh strip-sha <file>    # Strip all sha fields from a *_INDEX.json
  ./scripts/github-tools.sh push-ready          # Show summary of what is ready to push
  ./scripts/github-tools.sh self-update-stage   # Mark last item Pushed + Verified (manual)
  ./scripts/github-tools.sh full-workflow       # Print the complete 5-phase workflow

All operations follow the official rules from references/git_connector_workflow.md
EOF
}

init_stage() {
  mkdir -p "$(dirname "$STAGE_FILE")"
  cp "$SKILL_DIR/references/stage-template.md" "$STAGE_FILE"
  echo "✅ Fresh STAGE.md created at $STAGE_FILE"
  echo "Edit it with your current session details, then run 'show-stage' to review."
}

show_stage() {
  if [[ -f "$STAGE_FILE" ]]; then
    cat "$STAGE_FILE"
  else
    echo "No STAGE.md found. Run 'init-stage' first."
  fi
}

archive_major() {
  local title="$1"
  local date=$(date +%Y-%m-%d)
  local dir="$ARCHIVE_BASE/changelog/$(date +%Y/%m)"
  mkdir -p "$dir"
  local file="$dir/${date}-${title}.md"
  echo "# $title — $(date)" > "$file"
  echo "Created major changelog: $file"
}

archive_minor() {
  local title="$1"
  local date=$(date +%Y-%m-%d)
  local file="$ARCHIVE_BASE/minor_fixes/${date}.md"
  mkdir -p "$(dirname "$file")"
  echo -e "\n## $title — $(date +%H:%M)\n" >> "$file"
  echo "Appended to minor_fixes: $file"
}

strip_sha() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo "File not found: $file"
    exit 1
  fi
  # Simple sed to remove "sha": "..." lines (works for most JSON index files)
  sed -i '/"sha":\s*"[^"]*"/d' "$file"
  echo "✅ SHA fields stripped from $file"
}

push_ready() {
  echo "=== Current Staged Items (from STAGE.md) ==="
  if [[ -f "$STAGE_FILE" ]]; then
    grep -A 5 "Staged (Local Ready for Push)" "$STAGE_FILE" || echo "No staged items section found."
  else
    echo "No STAGE.md found."
  fi
}

self_update_stage() {
  if [[ -f "$STAGE_FILE" ]]; then
    echo "Marking last item as Pushed + Verified..."
    sed -i 's/Pushed + Verified/Pushed + Verified (manual update)/g' "$STAGE_FILE" || true
    echo "✅ STAGE.md self-updated. Remember to add SHA and commit URL manually."
  else
    echo "No STAGE.md found."
  fi
}

full_workflow() {
  cat "$SKILL_DIR/references/git_connector_workflow.md"
}

case "${1:-help}" in
  init-stage) init_stage ;;
  show-stage) show_stage ;;
  archive-major) archive_major "${2:-untitled}" ;;
  archive-minor) archive_minor "${2:-untitled}" ;;
  strip-sha) strip_sha "$2" ;;
  push-ready) push_ready ;;
  self-update-stage) self_update_stage ;;
  full-workflow) full_workflow ;;
  *) show_help ;;
esac