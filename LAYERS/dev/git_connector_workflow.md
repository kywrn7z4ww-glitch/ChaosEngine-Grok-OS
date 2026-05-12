# Git Connector Workflow v3.0 (Master Document - Updated 2026-05-12)

## Purpose
This is the single source of truth for how to manage the Grok OS repository using GitHub connectors. It covers the complete lifecycle: staging → changelog → index editing → SHA stripping → push → verification.

**Core Rule:** MAIN branch = read-only. TESTING branch = full read-write.

---

## 1. Overall Workflow (The Actual Process)

### Phase 1: Local Work
- Do all development, testing, and debugging locally in `/home/workdir/artifacts/Grok OS/`
- Never push directly without going through `STAGE.md`

### Phase 2: Staging (Using STAGE.md)
1. Update `STAGE.md` with:
   - List of changes
   - Target files
   - Description of what each change does
   - How to amend each file

2. Create changelog entry in the correct nested structure:
   ```
   ARCHIVE/changelog/yyyy/mm/{date+filename}.md
   ```

### Phase 3: Index Editing + SHA Stripping (Critical)
Before pushing any index files (`*_INDEX.json`):
- Open the index file
- **Strip all `sha` fields** from file entries
- This prevents SHA conflicts during push
- Save the cleaned version

### Phase 4: Push via Connectors
Use these tools in order:
1. `github___get_file_contents` — Get current SHA of target file
2. `github___create_or_update_file` — Push the updated file using the SHA from step 1
3. Repeat for each file

### Phase 5: Verification
1. Confirm changes appear in repo
2. Run `runtime_index_scan("list")` or cold boot to verify
3. Update `STAGE.md` status to "Pushed + Verified"

---

## 2. How to Use Connectors to Emulate Real GitHub Work

### Reading Files
```python
github___get_file_contents(
    owner="kywrn7z4ww-glitch",
    repo="ChaosEngine-Grok-OS",
    path="ROOT/boot/index_builder.py",
    ref="testing"
)
```

### Updating Files (The Real Way)
```python
github___create_or_update_file(
    owner="kywrn7z4ww-glitch",
    repo="ChaosEngine-Grok-OS",
    path="ROOT/boot/index_builder.py",
    content=updated_content,
    sha=current_sha,           # ← Required for updates
    message="feat(index): add runtime_index_scan()",
    branch="testing"
)
```

### Deleting Files
```python
github___delete_file(
    owner="kywrn7z4ww-glitch",
    repo="ChaosEngine-Grok-OS",
    path="old_file.py",
    branch="testing",
    message="chore: remove deprecated file"
)
```

---

## 2.5. Self-Updating STAGE.md Rule (Mandatory)

After **every successful push**, Grok must immediately:

1. Open `STAGE.md`
2. Mark the pushed item as **"Pushed + Verified"**
3. Add the new SHA and commit URL
4. Update the final checklist

**This is now an official rule.** No push is considered complete until `STAGE.md` is updated.

---

## 3. Changelog Creation

Always create changelogs in this exact structure:

```
ARCHIVE/changelog/yyyy/mm/{date+filename}.md
```

**Example path:**
`ARCHIVE/changelog/2026/05/2026-05-12-resilient-boot-upgrades.md`

**Use the official template:** `LAYERS/dev/stage-template.md` (Section: Changelog)

---

## 4. Index Editing Rules (SHA Stripping)

**Golden Rule:** Never push an index file that still contains `sha` fields.

**Process:**
1. Before pushing any `*_INDEX.json` file:
   - Open the file
   - Remove or nullify every `"sha": "..."` entry
   - Save the cleaned file
2. This prevents "Update is not a fast forward" errors and SHA conflicts.

---

## 5. Quick Reference Commands

| Task                        | Tool                              | Notes |
|----------------------------|-----------------------------------|-------|
| Read file                  | `github___get_file_contents`      | Always get SHA first |
| Update file                | `github___create_or_update_file`  | Must include current SHA |
| Delete file                | `github___delete_file`            | Use with caution |
| List top-level folders     | `runtime_index_scan("list")`      | Local function |
| Scan specific folder       | `runtime_index_scan("FOLDER")`    | Updates index automatically |
| Full cold boot             | `boot_grok_os()`                  | Uses targeted indexing |

---

**This document now contains the complete, real workflow.**

*Last updated: 2026-05-12*