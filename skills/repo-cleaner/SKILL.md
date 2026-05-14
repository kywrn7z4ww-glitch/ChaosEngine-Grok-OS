---
name: repo-cleaner
description: "Safe Repo Hygiene Tool v1.1. Suggests cleanup actions first, always creates backup branch before any changes. Now includes skill archiving, deprecation, and manifest cleanup. Trigger with: 'clean repo', 'repo cleaner', 'repo hygiene', 'archive skill', 'deprecate skill'. Use when your repo is getting messy and you want safe, guided cleanup."
---

# Repo Cleaner — Safe Hygiene Tool v1.1

**Core Philosophy:**
**"Suggest First. Backup Always. Clean Safely. Archive Before Delete."**

This skill helps keep repositories healthy by suggesting cleanup actions **before** doing anything. It always creates a backup branch first, respects files that "look useless but might be important", and focuses especially on **commit history cleaning** and **skill lifecycle management** (archiving, deprecation, manifest cleanup).

**Non-Negotiable Rules:**
1. **Suggest First** — Never auto-execute. Always show proposed actions first.
2. **Backup Branch Always** — Create a backup branch (e.g. `backup-before-clean-YYYYMMDD`) before any destructive action.
3. **Respect "Looks Useless" Files** — Flag files that might actually be important and ask for confirmation.
4. **Commit Cleaning Focus** — Prioritize cleaning commit history (squash, rewrite messages, remove noise).
5. **Archive Before Delete** — Never delete important files. Always move to `skills/archive/` first.
6. **Limited Self-Improvement** — Only logs patterns. Never aggressively changes behavior without strong justification.
7. **User Must Approve Everything** — No auto-cleaning ever.

---

**New Commands (v1.1)**

| Command                    | What It Does |
|---------------------------|--------------|
| `archive skill [name]`    | Moves skill folder to `skills/archive/[name]/` and updates manifest |
| `deprecate skill [name]`  | Marks skill as deprecated in manifest + suggests archiving |
| `clean manifest archives` | Removes all skills marked as "archived" from the manifest |
| `clean repo`              | General repo hygiene (original behavior) |

---

**Execution Flow (General)**

**Phase 0 — Analysis**
- Scan the repository
- Identify potential hygiene issues:
  - Messy commit history
  - Old/unused branches
  - Duplicate or broken files
  - Deprecated/archived skills that can be cleaned from manifest

**Phase 1 — Backup Branch Creation**
- Always create a backup branch before suggesting any changes
- Show the branch name to the user

**Phase 2 — Suggestion Generation**
- Generate clear, prioritized list of suggested actions
- For each action: show what will change + risk level

**Phase 3 — User Review & Approval**
- User selects which actions to approve
- Final confirmation before execution

**Phase 4 — Execution (Only Approved Actions)**
- Execute only what user approved
- Keep detailed log of changes

**Phase 5 — Post-Clean Verification**
- Show summary of what was cleaned
- Remind user they can delete the backup branch if everything is fine

---

**Current Capabilities (v1.1)**
- Commit history analysis + suggestions
- File hygiene suggestions (with safety warnings)
- Automatic backup branch creation
- Clear suggestion + approval flow
- **Skill archiving** (`archive skill [name]`)
- **Skill deprecation** (`deprecate skill [name]`)
- **Manifest cleanup** (`clean manifest archives`)
- Limited pattern logging (light self-improvement)

**Recommended Future Upgrades**
- Better commit message suggestions using AI
- Large file detection in history
- Branch cleanup suggestions
- Integration with `skills-backup` for full hygiene + backup workflows
- More aggressive cleaning options (with extra warnings)
- Auto-detect deprecated skills from manifest

---

**Trigger Phrases**
- clean repo
- repo cleaner
- repo hygiene
- archive skill [name]
- deprecate skill [name]
- clean manifest archives

**End of repo-cleaner v1.1 — Suggest first. Backup always. Archive before delete. Safe skill lifecycle management.**