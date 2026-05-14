---
name: repo-cleaner
description: "Safe Repo Hygiene Tool. Suggests cleanup actions first, always creates backup branch before any changes, and focuses on commit cleaning + smart file hygiene. Trigger with: 'clean repo', 'repo cleaner', 'repo hygiene'. Use when your repo is getting messy and you want safe, guided cleanup."
---

# Repo Cleaner — Safe Hygiene Tool

**Core Philosophy:**
**"Suggest First. Backup Always. Clean Safely."**

This skill helps keep repositories healthy by suggesting cleanup actions **before** doing anything. It always creates a backup branch first, respects files that "look useless but might be important", and focuses especially on **commit history cleaning**.

**Non-Negotiable Rules:**
1. **Suggest First** — Never auto-execute. Always show proposed actions first.
2. **Backup Branch Always** — Create a backup branch (e.g. `backup-before-clean-YYYYMMDD`) before any destructive action.
3. **Respect "Looks Useless" Files** — Flag files that might actually be important and ask for confirmation.
4. **Commit Cleaning Focus** — Prioritize cleaning commit history (squash, rewrite messages, remove noise).
5. **Limited Self-Improvement** — Only logs patterns. Never aggressively changes behavior without strong justification.
6. **User Must Approve Everything** — No auto-cleaning ever.

---

**Execution Flow**

**Phase 0 — Analysis**
- Scan the repository
- Identify potential hygiene issues:
  - Messy commit history
  - Old/unused branches
  - Duplicate or broken files
  - Large binary files in history
  - Poor commit messages

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

**Current Capabilities (v1.0)**
- Commit history analysis + suggestions (squash, message cleanup, merge commit removal)
- File hygiene suggestions (with safety warnings)
- Automatic backup branch creation
- Clear suggestion + approval flow
- Limited pattern logging (light self-improvement)

**Recommended Future Upgrades**
- Better commit message suggestions using AI
- Large file detection in history
- Branch cleanup suggestions
- Integration with `skills-backup` for full hygiene + backup workflows
- More aggressive cleaning options (with extra warnings)

---

**Anti-Patterns**
- Never auto-clean without approval
- Never rewrite history without backup branch
- Never assume a file is useless without warning the user

**Trigger Phrases
- clean repo
- repo cleaner
- repo hygiene

**End of repo-cleaner v1.0 — Suggest first. Backup always. Clean safely.**