# GitHub Connectors Guide for ChaosEngine-Grok-OS

## Purpose

This guide explains how to use the GitHub connectors (tools) to manage the repository efficiently. It serves as a permanent reference so we don't have to repeat the process every time.

## What are Connectors?

Connectors are remote tools that allow direct interaction with the GitHub repo (kywrn7z4ww-glitch/ChaosEngine-Grok-OS) using API calls via `call_connected_tool`. They replace the need for local git operations in this environment.

## Key Connectors and What They Do

- **github___get_file_contents**: Fetches the content of a file or lists contents of a directory. **Always use this first** before editing to get the current `sha` (for conflict prevention) and content.

- **github___create_or_update_file**: Creates a new file or update an existing one. For updates, provide the `sha` from get_file_contents. Supports any path - folders are created automatically.

- **github___delete_file**: Deletes a file (or empty folder). Requires the current `sha`.

- **github___push_files**: Pushes multiple files in one commit. Useful for batch operations. Each file has `path` and `content`.

- Other useful: github___list_branches, github___create_branch, github___create_pull_request, etc.

## How to Use Connectors

Use this exact format:

call tool call_connected_tool with tool_name is github___get_file_contents arguments is {"owner": "kywrn7z4ww-glitch", "repo": "ChaosEngine-Grok-OS", "path": "LAYERS/dev/github-workflow/GITHUB_CONNECTORS_GUIDE.md", "ref": "testing"}

**Important Notes**:
- `owner` and `repo` are always "kywrn7z4ww-glitch" and "ChaosEngine-Grok-OS"
- `branch` or `ref` is usually "testing"
- For JSON in arguments, use proper JSON syntax (no escaping needed in the call).
- Always include descriptive `message` for commits.

## Efficiently Moving and Editing Files/Folders

### General Workflow (Always Follow This Order)
1. **Pull current state**: Use get_file_contents on the target path to get latest sha and content.
2. **Plan the change**: Document in STAGE.md or a temp plan if complex.
3. **Make the change**: Use create_or_update or delete.
4. **Verify**: Get contents again to confirm.
5. **Update tracking**: Update STAGE.md, indexes, and docs if paths changed.
6. **Commit message best practices**: Use conventional commits like "refactor(archive): move legacy Archive to deprecated-archive/ for cleaner structure"

### Moving a Single File
1. Get content + sha from old_path.
2. Create_or_update_file at new_path with the content (no sha needed if new).
3. Delete_file at old_path using old sha.

Example move:
- Old: Archive/oldfile.md
- New: ARCHIVE/deprecated-archive/oldfile.md

### Moving Folders (Complex - Use This Order)
Since GitHub API doesn't have native folder move:
- Recursively list all files in the source folder using get_file_contents (it returns tree).
- For each file, perform the move as above (get, create new, delete old).
- For efficiency with many files: Use github___push_files to batch create the new paths first (copy), then batch delete the old ones.
- If too many, do in stages (e.g. one subdir at a time).
- After move, delete the now-empty source folder if needed.
- Update any references in README.md, indexes, or other docs.

### Creating New Structure
- Just create files in the desired path (e.g. ARCHIVE/changelog/2026-05-10-overview.md) - folders appear automatically.
- For empty folders, create a .gitkeep file inside.

### Editing Files
- Always get current version first.
- Modify the content locally in your mind or use tools.
- Use create_or_update with new content and old sha.

### Tips to Avoid Reminders/Errors
- Never edit without pulling sha first.
- Use "testing" branch for all dev work.
- Keep STAGE.md updated with current session changes.
- For big refactors like archive cleanup, create a PLAN.md first with numbered steps.
- Parallelize independent operations (multiple unrelated moves at once).
- After restructure, run any index builders or validators if applicable.

## Current Session: Archive Restructure Plan

To address the old Archive folder:

**Target Structure**:
ARCHIVE/
├── changelog/          (for new dated entries)
├── deprecated-archive/ (for old legacy folders)
│   └── Archive/        (or directly the subfolders)
├── minor_fixes/
└── README.md

**Order of Operations** (to be executed after this guide is created):
1. Create ARCHIVE/deprecated-archive/ with a README explaining it's for legacy pre-restructure content.
2. Move all subfolders from Archive/ (01-05-2026, 05-05-2026, etc.) and README.md into ARCHIVE/deprecated-archive/Archive/ or flat under deprecated-archive/.
3. Delete the old empty Archive/ folder.
4. Update any references (e.g. in ROOT/REPO_INDEX.json if it points to Archive).
5. Commit with message "refactor(archive): relocate legacy Archive contents to ARCHIVE/deprecated-archive/ for v4.0 structure"

This guide ensures future operations are self-documenting.
