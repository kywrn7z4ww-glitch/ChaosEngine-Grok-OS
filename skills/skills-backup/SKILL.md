---
name: skills-backup
description: "Smart Skills Backup Tool v1.3. Backs up all custom skills to the skills-prototype branch. Automatically updates manifest on backup. Supports current skills folder and future Grok OS Skill folder. Trigger with: 'backup skills', 'skills backup', 'backup grok skills'. Use for regular repo backup of all custom skills."
---

# Skills Backup — Smart Repo Backup Tool v1.3

**Core Philosophy (Locked):**
**"Backup the Skill Library Safest Way Possible — Efficient, Compatible, and Conflict-Aware. Auto-Manifest Updates."**

This skill exists to protect our custom skills by backing them up to git in the **safest, most reliable way** while remaining efficient. It prioritizes:
- Safety over speed
- Compatibility checking over blind self-improvement
- Clear conflict handling
- Traceable version history (SHA + content hash + date)
- **Automatic manifest updates** after every successful backup

**Backup Targets:**

| Target              | Local Path                          | Remote Path |
|---------------------|-------------------------------------|-------------|
| **Current Skills**  | `/home/workdir/.grok/skills/`       | `skills-prototype/skills` |
| **Grok OS Skill**   | (Future)                            | `skills-prototype/Grok_OS_Skill` |

**Non-Negotiable Rules:**
1. **Always Compare First** — Never push blindly. Always show diff + conflict summary.
2. **Track Everything** — Use SHA + content hash + timestamp for every file version.
3. **Compatibility First** — Before any self-improvement, check compatibility with dependencies (github-tools, project-pusher, etc.).
4. **Conflict Handling** — Detect and clearly report when remote and local have diverged.
5. **User Confirmation** — Always ask before pushing (no auto-push ever).
6. **Automatic Manifest Update** — After successful backup, automatically update `skills-manifest.json` with new SHAs and timestamps.
7. **Limited Self-Improvement** — Only improve if compatibility is confirmed. Never break core safety.

---

**Execution Flow**

**Phase 0 — Target Selection**
- Ask which target(s) to backup (default = Current Skills)

**Phase 1 — Local Scan + Version Tracking**
- Walk the selected folder(s)
- For every file generate:
  - SHA (git-style)
  - Content hash (MD5/SHA256)
  - Last modified date
- Store version metadata

**Phase 2 — Remote Comparison + Conflict Detection**
- Use `github-tools` to get remote tree + metadata
- Compare local vs remote using SHA + content hash
- Detect:
  - New files
  - Modified files (content changed)
  - Diverged files (both sides changed differently = conflict)
  - Deleted files

**Phase 3 — Compatibility & Safety Check**
- Check compatibility with key dependencies (`github-tools`, `project-pusher`)
- If any risk detected → warn user and pause

**Phase 4 — User Review + Conflict Resolution**
- Show clear diff + conflict report
- Ask user how to handle conflicts (keep local / keep remote / manual)
- Final confirmation before push

**Phase 5 — Stage + Push**
- Stage only approved changes
- Generate smart commit message
- Push to `skills-prototype` branch
- **Automatically update manifest** with new SHAs and backup timestamp

**Phase 6 — Limited Self-Improvement (Compatibility First)**
- Log what was backed up + any patterns
- Only improve if compatibility check passes
- Never break core safety rules

**Phase 7 — Verification**
- Confirm success
- Log backup metadata (date, files changed, commit SHA)
- Confirm manifest was updated

---

**Current Capabilities (v1.3)**
- Backup current skills folder
- Smart diff detection
- User confirmation before push
- Clean commit messages
- **Automatic manifest update** after successful backup
- Future support for Grok OS Skill path (ready when needed)

**Recommended Future Upgrades**
- Scheduled automatic backups
- Backup to multiple branches
- Encryption option for sensitive skills
- Integration with `project-pusher` for full project backup
- One-command "backup everything" mode

---

**Trigger Phrases**
- backup skills
- skills backup
- backup grok skills
- backup skills --target grok-os

This skill makes sure we never lose our custom skills work and keeps the manifest in sync automatically.

**End of skills-backup v1.3 — Stronger philosophy, SHA+hash tracking, conflict handling, compatibility-first limited self-improvement, automatic manifest updates. Safest possible skill library backup.**