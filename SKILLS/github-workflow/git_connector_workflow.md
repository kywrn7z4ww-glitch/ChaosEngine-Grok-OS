# Git Connector Workflow (for Remote Repo Management)

**Location:** /LAYERS/dev/github-workflow/git_connector_workflow.md
**Purpose:** Outline the standardized process for using GitHub connectors to perform targeted updates, cleanups, and pushes to the ChaosEngine-Grok-OS repository. This is the primary workflow for /dev layer when handling repo maintenance, deprecations, and structural changes.

## Primary Tooling
- Use GitHub connectors exclusively via `call_connected_tool`:
  - `github___get_file_contents` — Pull current remote state (always first step for any target).
  - `github___create_or_update_file` — For edits/rewrites (provide exact SHA for updates to avoid conflicts).
  - `github___delete_file` — For removals (use specific commit messages).
  - `github___push_files` — For batch commits when multiple related changes.
- Never use shell `git` commands for remote operations. Connectors handle authentication and API calls safely.

## Manifest-Driven Process (STAGE.md)
1. **Local Sandbox Fixes**: Perform all edits, audits, cleanups, and path fixes locally in `/home/workdir/artifacts/grok-os/`.
2. **Audit**: Verify changes, check for inconsistencies (e.g., path hardcodes, deprecated references, empty dirs), ensure comments are updated.
3. **Create/Update STAGE.md**: Track every item as a "push candidate" with:
   - File path (relative to repo root, e.g., `ROOT/boot/grok_os.py`)
   - Action (update, delete, create)
   - Description of change
   - Commit message template
   - Status (local done / ready to push / pushed)
4. **Archiving Phase** (during staging/audit — update and verify changelogs before any push, so everything stays clean, logical, and inline with the repo structure):
   - Determine type: minor fixes, full overhaul, or both.
   - Create folder: `ARCHIVE/changelog/{date}{type}/` (e.g. `10-05-2026-full-overhaul/` or `10-05-2026-minor-fixes/` — no pure date folders; keep descriptive and simple as requested).
   - Create file inside: `{date}{small note on change for big changes or minor fixes and the full list of fixes inside}.md` (e.g. `10-05-2026-refined-github-connectors-workflow.md`).
   - Inside the file: include the date, a small note on the change, and the full detailed list of fixes/changes made.
   - Verify the changelog is complete and accurate, and the overall repo structure is respected (no random files or paths outside the defined scheme).
   - Update STAGE.md to mark the item as "archived to ARCHIVE/changelog/..."
   - (Optional) Re-run index_builder.py on ARCHIVE/ to refresh ARCHIVE_INDEX.json.
   - This keeps the process simple and ensures changelogs are updated and verified before pushing.

5. **Push Phase** (after archiving and verification, when local work is complete):
   - Pull current remote state for each file.
   - Execute targeted connector calls.
   - Use precise, relevant commit messages (e.g., "chore(boot): remove deprecated mirroring/ folder (v2.5 legacy replaced by v4.0 connectors)").
   - Verify post-push with re-pull.
   - Update STAGE.md status.

6. **Cleanup**: Remove any local temp files, empty duplicate dirs, update indexes/docs if needed, ensure no iteration clutter.

## Pull-First Discipline
- Always start with `github___get_file_contents` (ref: "testing") to capture current SHA and content before any modification.
- This prevents conflicts and ensures we only push diffs.

## Targeted & Clean Commits Only
- No bulk pushes of unedited files.
- Every commit must be meaningful and tied to a STAGE.md entry.
- For deprecations (e.g., mirroring/ folder): Delete files individually with specific messages, then confirm folder removal.

## Index & Doc Sync
- After structural changes (adds/deletes), update `REPO_INDEX.json`, `ROOT_INDEX.json`, and related docs to reflect new state (remove legacy refs, update boot_sequence, version bumps).
- Example: When removing v2.5 mirror logic, excise all references from indexes and update to v4.0+ connector flow.

## Index SHA Stripping Rule (Critical — Non-Negotiable)
- **When updating ANY *_INDEX.json** (LAYERS_INDEX.json, REPO_INDEX.json, ROOT_INDEX.json, PROCESS_INDEX.json, etc.): **ALWAYS STRIP all "sha" fields** from every entry object before writing the final JSON and staging for push.
- **Rationale**: Committing live blob SHAs causes the index file's own SHA to change on every update → perpetual drift, extra commits, and validation mismatches. The local runtime (ChaosEngine / REPO_VALIDATOR.py) **must** fetch current SHAs fresh via GitHub API (`get_latest_tree` or per-blob) at pull/validate time.
- **Implementation in workflow**:
  1. Generate/populate index via scan (as done for LAYERS) or index_builder.py.
  2. Post-process: recursively remove any "sha" key from the JSON structure.
  3. Write the SHA-free version.
  4. Commit message MUST reference: "index: SHA-stripped per rules (runtime fetches live SHAs)".
- This rule now applies to **all future index syncs** — no exceptions. The LAYERS_INDEX.json update just performed followed this exactly (no SHAs present).

## Verification & Logging
- Post-push: Re-pull file, compare to local, log in boot_log or STAGE.md.
- Cross-check against grok-os.md and other design docs.

## Workflow Triggers
- User requests like "push the updated logic", "clean up X", "stage the fixes", "targeted fixes for Y".
- Automatically activate in /dev for any repo maintenance task.

**This file is the single source of truth for connector ops in the /dev layer. Update it as the process evolves.**