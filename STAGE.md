# STAGE.md — Targeted Fixes (2026-05-11)

**Status:** In Progress
**Workflow:** /LAYERS/dev/github-workflow/git_connector_workflow.md

## Planned Changes (Amend-Only, No Stubs)

### 1. Spelling Correction
- File: `ROOT/evoloution-engine` → `ROOT/evolution-engine`
- Reason: Obvious typo in folder name
- Action: Amend references in code + folder rename via git-mv if possible

### 2. Path & Naming Consistency (to what actually exists on testing)
- Use `chaos_engine` (underscore) — matches current testing structure
- Fix all hardcoded paths in:
  - `ROOT/boot/grok_os.py`
  - `ROOT/chaos_engine/chaos_engine.py`
- Change from old `grok-os` / `grokos` to consistent `Grok OS` (per style) where it affects local runtime

### 3. Files to Amend (Pull-First + SHA)
1. `ROOT/boot/grok_os.py` — update paths
2. `ROOT/chaos_engine/chaos_engine.py` — update paths + fix spelling references
3. Update `STAGE.md` and archive changelog

## Status
- [ ] Pull current SHAs
- [ ] Amend files with exact SHA
- [ ] Create ARCHIVE/changelog entry
- [ ] Update indexes (SHA-stripped)

**Last Updated:** 2026-05-11 21:55 BST
