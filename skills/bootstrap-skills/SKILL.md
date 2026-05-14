---
name: bootstrap-skills
description: "Clean Skills Bootstrap Installer v2.0 — Hard-locked safety edition. Fully explicit, manifest-only, zero automation on destructive actions. Includes batched automated fetching from repo using github-connectors. Pre-existing data is sacred and never touched without explicit confirmation. Trigger with: 'bootstrap skills', 'install skills', 'setup skills', 'bootstrap from repo', 'bootstrap uninstall'."
---

# Bootstrap Skills v2.0 — Hard-Locked Safe Installer + Manifest System

**Core Philosophy (Locked Forever):**  
**"Explicit. Safe. Manifest-Only. User in Total Control. Pre-Existing Data Is Sacred."**

This is the **only** approved way to install or remove skills. Everything is explicit. No silent automation. No data loss. Ever.

**Non-Negotiable Hard Locks (Never Violate):**
1. **100% Explicit Confirmation** — Every single action that could affect anything requires a clear "y/n" from the user.
2. **Manifest-Only Operations** — Install = add to manifest + fetch files. Uninstall = remove from manifest **only**. No file deletion, no overwrite of user data.
3. **Pre-Existing Data Safeguard** — Full scan before any action. Existing skills/files are **never** touched or listed for removal unless user explicitly requests manifest cleanup.
4. **Zero Destructive Automation** — No auto-delete, no auto-overwrite, no silent changes. All destructive-looking steps are replaced with manifest edits + user prompts.
5. **Batched & Safe Fetching** — All repo fetches happen in small, user-approved batches using `github-connectors`.
6. **Full Audit Log** — Every run writes a timestamped log of exactly what was confirmed and changed.

---

## 1. Skills Manifest (Single Source of Truth)

**Location:** `/home/workdir/.grok/skills/skills-manifest.json`

**Format (example):**
```json
{
  "version": "2.0",
  "last_updated": "2026-05-14T02:36:00Z",
  "installed_skills": [
    {
      "name": "github-connectors",
      "installed_at": "2026-05-14T02:30:00Z",
      "source": "repo:skills-prototype/skills/github-connectors"
    },
    {
      "name": "truth-blade",
      "installed_at": "...",
      "source": "..."
    }
  ],
  "pre_existing_skills_at_bootstrap": ["list of skills that existed before this bootstrap run"]
}
```

**Rules:**
- Bootstrap **only appends** to `installed_skills`.
- Uninstaller **only removes** from `installed_skills`.
- Never touches actual skill folders/files unless user explicitly says "yes, overwrite this specific file".

---

## 2. Pre-Bootstrap Safety Scan (Mandatory First Step — Always)

Before **anything** happens:
1. Scan `/home/workdir/.grok/skills/` for existing skill folders.
2. Load or create `skills-manifest.json`.
3. Output:
   ```
   SAFETY SCAN COMPLETE
   - Existing skills found: X
   - Skills already in manifest: Y
   - Pre-existing data that will NEVER be touched: [list]
   - Any conflicts? None / list them
   ```
4. Ask: **"Pre-existing skills and data are 100% safe and will not be modified. Continue with bootstrap? (y/n)"**

If user says no → exit immediately. No changes made.

---

## 3. Installation Flow (Fully Explicit + Batched Fetching)

**Phase 0 — Mode Selection**
- "Bootstrap mode: (1) Fresh install from repo (2) Update existing (3) Uninstall mode"
- User chooses.

**Phase 1 — Fetch Latest Skill List from Repo (Batched, Explicit)**

Uses `github-connectors` exclusively:
- `search_connected_tools("github")` → confirm tools available.
- Then `github___search_repositories` or direct `github___get_file_contents` on the skills folder in `skills-prototype` branch.

**Batched Fetching (Hard-Locked):**
- Batch 1: Core reasoning skills (truth-blade, auditor, project-pusher, 5w1h-translator, github-connectors)
- Batch 2: GitHub & tools (github-tools, github-web-explorer, smart-git-clone)
- Batch 3: Utility & safety (skills-backup, repo-cleaner, tool-recovery, consolidator)
- Batch 4: Creative & others (imagine-kitchen, web-probe, etc.)

For each batch:
```
BATCH X — [Skill names]
This will fetch the latest SKILL.md + supporting files from the repo and register them in the manifest.
Your existing files will NOT be overwritten unless you explicitly approve per file.

Proceed with this batch? (y/n)
```

Only after "y" → automated fetch using:
- `github___get_file_contents` (owner, repo, path="skills/xxx/SKILL.md", ref="skills-prototype")
- Write locally to `/home/workdir/.grok/skills/xxx/SKILL.md` **only if** user confirms "yes, write this file" (or "yes to all in batch").

**Phase 2 — Register in Manifest**
After successful fetch + local write:
- Append to `installed_skills` array with timestamp + source.
- Save manifest.
- Explicit: "github-connectors has been added to manifest. Your previous skills are untouched. Continue? (y/n)"

**Phase 3 — Post-Install Verification**
- Run basic validation on each new skill (read SKILL.md, check for required sections).
- Print clean report: "X skills successfully registered. 0 files overwritten. Pre-existing data safe."

---

## 4. Uninstall Mode (Manifest-Only — Zero Data Loss)

**Trigger:** "bootstrap uninstall" or choose mode 3.

Flow:
1. Load `skills-manifest.json`.
2. Show list of installed skills (with install dates).
3. "Select skills to remove from manifest (comma-separated numbers or 'all'). This will ONLY remove the entry from the manifest. Your actual skill files and any user data remain 100% untouched."
4. User confirms selection.
5. **Final hard lock prompt:** "You are about to remove these from the manifest ONLY. No files will be deleted. Type 'YES I UNDERSTAND' to proceed."
6. Remove entries from `installed_skills`.
7. Save manifest + log the action.
8. "Uninstall complete. Skills removed from manifest only. Your files are safe."

This allows users to **try any skill** and cleanly remove the "package" reference without losing anything.

---

## 5. Automated Fetching Logic (Solid & Safe — Using github-connectors)

**Core Function (described for implementation):**
```python
# Pseudocode — actual implementation uses call_connected_tool
def fetch_skill_batch(batch_name, skill_list, ref="skills-prototype"):
    print(f"Fetching batch: {batch_name}")
    for skill in skill_list:
        # 1. User confirmation per skill or batch
        if not user_confirms(f"Fetch latest {skill} from repo?"):
            continue
        # 2. Get file contents via github___get_file_contents
        content = call_connected_tool(
            "github___get_file_contents",
            {"owner": "kywrn7z4ww-glitch", "repo": "ChaosEngine-Grok-OS", 
             "path": f"skills/{skill}/SKILL.md", "ref": ref}
        )
        # 3. Optional: fetch supporting files (scripts/, etc.) in same batch
        # 4. Write locally only after explicit "yes, write file"
        if user_confirms(f"Write {skill}/SKILL.md locally? (will not overwrite existing unless approved)"):
            write_file(f"/home/workdir/.grok/skills/{skill}/SKILL.md", content)
        # 5. Append to manifest
```

**Safety Features Built-In:**
- Every fetch requires confirmation.
- Never overwrites without per-file approval.
- All operations logged.
- Falls back to local copy if repo fetch fails.
- Uses only `github-connectors` tools (never direct git/curl).

---

## 6. Full Safety & Logging

- Every run creates `/home/workdir/.grok/skills/logs/bootstrap-YYYYMMDD-HHMMSS.log`
- Log contains: timestamp, user confirmations, files fetched/written, manifest changes, pre-existing data list.
- If any step fails or user aborts → zero changes, clean exit, log written.

---

**Current Status (v2.0 — Hard-Locked Safety Edition)**  
- Fully explicit at every step  
- Manifest-only install/uninstall  
- Batched automated fetching from repo via github-connectors  
- Pre-existing data never touched without explicit approval  
- Zero destructive automation  
- Ready for production use on any machine

**Trigger Phrases**  
- bootstrap skills  
- install skills  
- setup skills  
- bootstrap from repo  
- bootstrap uninstall  
- bootstrap safe mode

**End of bootstrap-skills v2.0 — The only safe way to manage skills. Explicit. Manifest-only. User-controlled. Pre-existing data sacred.**

*This skill now contains the complete hard-locked system you requested: explicit confirmations, manifest-only operations, batched repo fetching with github-connectors, and zero risk to existing data.*