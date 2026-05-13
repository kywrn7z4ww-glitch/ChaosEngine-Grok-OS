# STAGE.md — Grok OS Targeted Push Manifest (v4.0 Workflow)

**Purpose**: Tracks all local fixes, audits, and items to push via GitHub connectors. STAGE.md is built and maintained **live on the local side** (in `/home/workdir/artifacts/grok-os/`) as the single source of truth for the current session's push queue, status, and history. Follows: Local Sandbox Fixes > Audit > Stage > Push > Archiving (before cleanup, to capture deprecated snapshots) > Cleanup (comments + final tidy).

**Last Updated**: [YYYY-MM-DD HH:MM TZ]

**Current Session**: [Brief summary of what this session accomplished, e.g. "All changes staged for push. Updated X, Y, Z. Minor fixes logged to ARCHIVE/minor_fixes/.... "]

**Archiving Policy (for reference)**: Major overhauls, deprecations (old versions for rollback), structural refactors, or significant feature additions get full dated archive folders (ARCHIVE/changelog/DD-MM-YYYY-short-title/) with snapshots + changelog entry. Minor fixes (typos, small comments, wording tweaks) are logged in archive for sure but shoved into a single minor_fixes/DD-MM-YYYY.md file for that date (avoids tonnes of tiny files). Commit messages still capture the details too. Git history + this keeps it clean.

## Completed (Pushed via Connectors)
- **[Item 1]** (description; folder confirmed gone on remote)
- **[Item 2]** (description)

## Staged (Local Ready for Push)
- **[File/Path]** (description of change; will be archived to ... upon push — ready for targeted connector push)
- **[File/Path]** (description; ready for push to LAYERS/dev/github-workflow/)

## Next Actions
1. Push [key file] with commit: "[type(scope): description]"
2. [Other actions...]
3. Final verification: re-pull key files, confirm no legacy refs, update any docs if needed
4. Create dated archive folder or minor_fixes entry for this session's changes and mark complete in STAGE.md

**All pushes use connectors only. No unedited bulk. Comments/cleanup included in commits.**

**All changes staged and ready for next targeted push!**