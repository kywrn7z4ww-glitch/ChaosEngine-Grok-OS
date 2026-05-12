---
name: github-tools
description: Master GitHub operations skill for ChaosEngine-Grok-OS. Full connector workflow, STAGE.md lifecycle management, SHA stripping, changelog & archive automation, self-updating rules, safe push/verify process, OUT-OF-THE-BOX creative tool usage, and full API tree scanning + local index.json building. Use for any repo change, staging, or maintenance on the skills-prototype / testing branch. MAIN branch is always read-only.
---

# GitHub Tools — Complete Connector Workflow Skill (v4.1 — Enhanced)

**Trigger when:** User says "use github-tools", "stage changes", "push via connectors", "update STAGE.md", "run git workflow", "scan the full repo tree", "build local index", or similar. This skill contains the **single source of truth** for all GitHub operations.

## Core Principles (Never Violate)
- **MAIN branch = read-only**. All work happens on `skills-prototype` or `testing`.
- **STAGE.md is the single source of truth** for the current session.
- **Local sandbox first** — never push without going through STAGE.md.
- **SHA stripping mandatory** for any *_INDEX.json before push (local index keeps SHA for verification).
- **Self-updating STAGE.md rule** — after every successful push, immediately update STAGE.md with "Pushed + Verified", new SHA, and commit URL.
- **Archive everything important** — major changes go to ARCHIVE/changelog/yyyy/mm/{date-title}.md; minor fixes go to ARCHIVE/minor_fixes/.

## OUT-OF-THE-BOX THINKING — Creative & Unorthodox Tool Usage (Mandatory Section)

Grok must think creatively. STAGE.md and this skill explicitly encourage combining tools in non-obvious ways:

**Creative Patterns (use these when standard flow is too slow or limited):**
1. **Full Repo Snapshot + Diff**: Use `consolidator` skill first to get a clean codebase.txt, then run full API tree scan below, then compare with local index.json to instantly see what changed since last session.
2. **Hybrid Browse + Connector**: When connectors are rate-limited or missing a file, fall back to `browse_page` on the raw GitHub URL or GitHub API tree endpoint, then feed the result directly into `github___create_or_update_file`.
3. **Index-First Development**: Before touching any file, run the "Full API Tree + Local Index Build" (below) so you have a complete local `index.json` with SHAs. This lets you detect stale files instantly without extra API calls.
4. **Stage + Consolidator Combo**: When preparing a big push, first run consolidator on the changed folders, paste the result into STAGE.md as the "what changed" evidence, then proceed with normal push.
5. **Emergency Rollback**: If a push breaks something, use `github___get_file_contents` with the previous SHA (stored in STAGE.md), then `create_or_update_file` to revert instantly.

**Golden Creative Rule**: If a task feels slow or repetitive, combine `browse_page` + connectors + consolidator + local index.json in one flow. Document the creative pattern you used inside STAGE.md under "Next Actions" so future sessions can reuse it.

## Full API Tree Scanning + Local Index Building (New v4.1 Feature)

This skill now includes **full repo tree scanning via web browse + automatic local index.json generation**.

### How to Trigger
Say: "Use github-tools to scan the full repo tree and build local index"

### Exact Process
1. **Fetch complete tree** (uses GitHub API via browse_page fallback or connector if available):
   ```
   https://api.github.com/repos/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/git/trees/skills-prototype?recursive=1
   ```
   (Authentication header added automatically when possible.)

2. **Build/Update local index.json**:
   - Location: `/home/workdir/artifacts/grok-os/INDEX.json` (or repo-specific name)
   - Keeps **all SHA values** locally (for staleness detection and fast verification).
   - Structure: `{ "path": "...", "sha": "...", "type": "blob/tree", "size": N }`

3. **Before any push** that includes the index:
   - Run the built-in `strip-sha` command on the index file (removes all `"sha"` fields).
   - Then push the cleaned version.

4. **Verification**:
   - After push, re-run the scan and compare local vs remote SHAs to confirm success.

This gives you an instant, queryable local map of the entire repository without relying on slow `git ls-files` or repeated connector calls.

## The Official 5-Phase Workflow (from git_connector_workflow.md)

### Phase 1: Local Work
Do all development, testing, and debugging in `/home/workdir/artifacts/Grok OS/`.

### Phase 2: Staging (Using STAGE.md)
1. Update `STAGE.md` (use the template in `references/stage-template.md`).
2. List every change, target file, description, and how to amend it.
3. Create changelog entry in `ARCHIVE/changelog/yyyy/mm/{date+filename}.md`.

### Phase 3: Index Editing + SHA Stripping (Critical)
Before pushing any `*_INDEX.json`:
- Open the file
- **Strip all `sha` fields** from every entry
- Save the cleaned version
This prevents SHA conflicts and "not a fast forward" errors.

### Phase 4: Push via Connectors (Exact Order)
1. `github___get_file_contents` — get current SHA of target file
2. `github___create_or_update_file` — push using the SHA from step 1
3. Repeat for each file
4. For deletes: `github___delete_file`

### Phase 5: Verification & Self-Update
1. Confirm changes appear on remote.
2. Run verification commands (runtime_index_scan, cold boot if needed).
3. **Immediately update STAGE.md**:
   - Mark item as "Pushed + Verified"
   - Add new SHA and commit URL
   - Complete the final checklist
4. Archive the session (major vs minor_fixes policy).

## How to Use the Connectors (Exact Examples)

**Read a file (always get SHA first):**
```bash
github___get_file_contents(
  owner="kywrn7z4ww-glitch",
  repo="ChaosEngine-Grok-OS",
  path="ROOT/boot/index_builder.py",
  ref="testing"
)
```

**Update a file:**
```bash
github___create_or_update_file(
  owner="kywrn7z4ww-glitch",
  repo="ChaosEngine-Grok-OS",
  path="ROOT/boot/index_builder.py",
  content=updated_content,
  sha=current_sha,
  message="feat(index): add runtime_index_scan()",
  branch="testing"
)
```

**Delete a file:**
```bash
github___delete_file(
  owner="kywrn7z4ww-glitch",
  repo="ChaosEngine-Grok-OS",
  path="old_file.py",
  branch="testing",
  message="chore: remove deprecated file"
)
```

## STAGE.md Template & Rules
The official template is in `references/stage-template.md`. Key sections:
- **Current Session** summary
- **Completed (Pushed via Connectors)**
- **Staged (Local Ready for Push)**
- **Next Actions**
- **Archiving Policy**: Major overhauls → dated ARCHIVE/changelog/ folder. Minor fixes → ARCHIVE/minor_fixes/DD-MM-YYYY.md

After every push: **Self-update STAGE.md immediately** (this is now a hard rule).

## Changelog & Archive Structure
Always use:
```
ARCHIVE/changelog/yyyy/mm/{date+filename}.md
```
Example: `ARCHIVE/changelog/2026/05/2026-05-12-resilient-boot-upgrades.md`

## Quick Reference Table
| Task                        | Tool                              | Notes |
|----------------------------|-----------------------------------|-------|
| Read file                  | `github___get_file_contents`      | Always get SHA first |
| Update file                | `github___create_or_update_file`  | Must include current SHA |
| Delete file                | `github___delete_file`            | Use with caution |
| Full cold boot             | `boot_grok_os()`                  | Uses targeted indexing |
| Scan folder                | `runtime_index_scan("FOLDER")`    | Updates index automatically |
| Full API Tree + Index      | Built-in (browse_page + local)    | Keeps SHA locally, strips on push |

## How to Invoke This Skill
- "Use github-tools to stage these changes"
- "Run the git connector workflow for the new index builder"
- "Create STAGE.md for today's session"
- "Push the updated files via connectors and update STAGE.md"
- "Scan the full repo tree and build local index.json"
- "Think outside the box and find a creative way to push these 12 files"

This skill now contains the complete, production-grade workflow + **out-of-the-box creative guidance** + **full API tree scanning + local index building** from the official `LAYERS/dev/` files and your latest requirements.

**Last synced & enhanced**: 2026-05-12 (from skills-prototype branch)
