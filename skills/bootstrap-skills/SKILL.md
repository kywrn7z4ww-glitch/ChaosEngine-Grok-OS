---
name: bootstrap-skills
description: "Clean Skills Bootstrap Installer v2.1 — Hard-locked safety edition with real uninstall. Fully explicit, manifest-tracked, zero risk to pre-existing skills. Supports actual deletion of manifest-listed skills only. Batched fetching via github-connectors. Trigger with: 'bootstrap skills', 'install skills', 'setup skills', 'bootstrap from repo', 'bootstrap uninstall'."
---

# Bootstrap Skills v2.1 — Hard-Locked Safe Installer + Real Uninstall

**Core Philosophy (Locked Forever):**  
**"Explicit. Safe. Manifest-Tracked. Real Uninstall for Manifest Skills Only. Pre-Existing Data Is Sacred."**

This is the **only** approved way to install or remove skills. Everything is explicit. No silent automation. No risk to your pre-existing work.

**Non-Negotiable Hard Locks (Never Violate):**
1. **100% Explicit Confirmation** — Every single action requires clear user approval.
2. **Manifest-Tracked Operations** — All installed skills are recorded in `skills-manifest.json`.
3. **Real Uninstall for Manifest Skills** — Skills listed in the manifest **can be fully deleted** (folders + manifest entry).
4. **Pre-Existing Data Protection** — Skills **not** in the manifest are **never shown or touched**.
5. **Batched & Safe Fetching** — All repo operations happen in small, user-approved batches.
6. **Full Audit Log** — Every action is logged with timestamps and confirmations.

---

## 1. Skills Manifest (Single Source of Truth)

**Location:** `/home/workdir/.grok/skills/skills-manifest.json`

The manifest tracks **only** the skills that were installed via bootstrap. Pre-existing skills are never added to it.

---

## 2. Pre-Bootstrap Safety Scan (Mandatory First Step)

Before anything happens:
1. Scan `/home/workdir/.grok/skills/`
2. Load `skills-manifest.json`
3. Clearly separate:
   - Skills **in manifest** (can be uninstalled)
   - Skills **not in manifest** (pre-existing — never touched)
4. Show safety summary and ask for confirmation to continue.

---

## 3. Installation / Update Flow (Batched + Explicit)

**Phase 0 — Mode Selection**
- Choose: (1) Install/Update from repo, (2) Uninstall mode

**Phase 1 — Batched Fetching (github-connectors only)**
- Propose logical batches
- Confirm per batch or per skill
- Fetch + write only after explicit approval
- Register in manifest after successful write

**Phase 2 — Post-Install Verification**
- Validate new skills
- Show clean report

---

## 4. Uninstall Mode — Real Deletion (Manifest-Listed Skills Only)

**Trigger:** "bootstrap uninstall" or choose mode 2.

**Flow:**

1. Load `skills-manifest.json`
2. Show **only** the skills currently listed in the manifest (with install dates)
3. "Select skills to **fully uninstall** (delete folders + remove from manifest). Skills not in the manifest will never be touched."
4. User selects skills (comma-separated or "all")
5. **Double Confirmation:**
   - First: "You are about to **permanently delete** these skill folders. This cannot be undone. Type 'YES DELETE' to continue."
   - Second: Final list + "Type the exact names of the skills you want to delete to confirm."
6. For each selected skill:
   - Delete the folder `/home/workdir/.grok/skills/[skill-name]/`
   - Remove entry from manifest
7. Save updated manifest + write detailed log
8. "Uninstall complete. X skills fully removed. Pre-existing skills untouched."

**Safety Guarantees:**
- Only skills **listed in the manifest** can be selected for deletion
- Pre-existing skills (not in manifest) are **never shown or deletable** through this tool
- Every deletion requires multiple explicit confirmations
- Full log is always created

---

## 5. Automated Fetching Logic (github-connectors)

Uses only `github___get_file_contents` and `github___create_or_update_file` via `call_connected_tool`.

All operations are:
- Batched
- User-confirmed
- Logged
- Reversible via manifest

---

## 6. Full Safety & Logging

- Every run creates a timestamped log in `/home/workdir/.grok/skills/logs/`
- Log contains: all user confirmations, files written/deleted, manifest changes, pre-existing skills list
- Zero risk to skills not managed by bootstrap

---

**Current Status (v2.1 — Real Uninstall Edition)**  
- Fully explicit at every step  
- Manifest-tracked install + **real deletion** for manifest-listed skills  
- Pre-existing skills completely protected  
- Batched repo fetching via github-connectors  
- Ready for production use

**Trigger Phrases**  
- bootstrap skills  
- install skills  
- setup skills  
- bootstrap from repo  
- bootstrap uninstall  
- bootstrap safe mode

**End of bootstrap-skills v2.1 — Explicit. Manifest-tracked. Real uninstall for installed skills. Pre-existing data sacred.**