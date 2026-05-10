# Git MV: Renaming Files and Folders to Change Filepaths

## Key Principle
**Yes — renaming a file or folder changes its filepath.** The name is part of the path, so a name change directly updates the full path in the repository.

This works on GitHub repos whether done locally or via the web UI / API connectors.

## Recommended Method: Local Git (Preserves History)

```bash
# Rename a file
git mv old/path/old-name.md new/path/new-name.md

# Rename a folder (moves everything inside)
git mv old-folder-name/ new-folder-name/

# Commit and push
git commit -m "chore: rename file/folder to update path"
git push origin testing
```

Git automatically detects this as a rename (not delete + add), so blame, history, and diffs stay clean.

## GitHub Web UI Method

1. Browse to the file in the repo
2. Click the ✏️ (edit) icon
3. In the filename box at the top, edit the name and/or path
4. Add a commit message
5. Commit changes

GitHub handles it as a rename commit.

## Using GitHub Connectors (Automation / No Local Clone)

Since we have `github___delete_file` and `github___create_or_update_file`:

1. Read the current content of the old path (use `github___get_file_contents`)
2. Delete the old path (`github___delete_file`)
3. Create the new path with the same content (`github___create_or_update_file`)

**Note:** This is technically a delete + create, not a tracked rename. Use local `git mv` when possible for better history.

## Why This Matters in Our Workflow

- Keeps repo structure clean and logical
- Enables the exact paths we document in indexes and STAGE.md
- Works for both files and entire folders
- All changes go through the normal commit + push flow on the `testing` branch

## Example in This Repo

Current workflow docs live at:
`LAYERS/dev/github-workflow/`

Renaming or moving files here (e.g., `git-mv.md` → `git-rename.md`) is done exactly as described above.

---
*Saved per user request. This logic is now part of the github-workflow documentation.*