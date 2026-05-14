---
name: bootstrap-skills
description: "Clean Skills Bootstrap Installer v2.2 — Hard-locked safety edition with real uninstall + automatic manifest updates + prerequisite checking + dependency graph. Fully explicit, manifest-tracked, zero risk to pre-existing skills. Supports actual deletion of manifest-listed skills only. Batched fetching via github-connectors. Trigger with: 'bootstrap skills', 'install skills', 'setup skills', 'bootstrap from repo', 'bootstrap uninstall'."
---

# Bootstrap Skills v2.2 — Hard-Locked Safe Installer + Real Uninstall + Auto-Manifest

**Core Philosophy (Locked Forever):**  
**"Explicit. Safe. Manifest-Tracked. Real Uninstall for Manifest Skills Only. Pre-Existing Data Is Sacred. Automatic Everything Possible."**

This is the **only** approved way to install or remove skills. Everything is explicit. No silent automation. No risk to your pre-existing work.

**Non-Negotiable Hard Locks (Never Violate):**
1. **100% Explicit Confirmation** — Every single action requires clear user approval.
2. **Manifest-Tracked Operations** — All installed skills are recorded in `skills-manifest.json`.
3. **Real Uninstall for Manifest Skills** — Skills listed in the manifest **can be fully deleted** (folders + manifest entry).
4. **Pre-Existing Data Protection** — Skills **not** in the manifest are **never shown or touched**.
5. **Automatic Manifest Updates** — Install/Update/Delete automatically updates the manifest.
6. **Prerequisite Checking** — Core skills must exist before bootstrap runs.
7. **Full Audit Log** — Every action is logged with timestamps and confirmations.

---

## 1. Skills Manifest (Single Source of Truth + Auto-Updated)

**Location:** `/home/workdir/.grok/skills/skills-manifest.json`

The manifest is **automatically updated** by bootstrap on:
- Install → Add skill with version, SHA, timestamp
- Update → Update version, SHA, timestamp
- Uninstall → Remove skill entry

---

## 2. Pre-Bootstrap Safety Scan + Prerequisite Check (Mandatory)

Before anything happens:
1. Scan `/home/workdir/.grok/skills/`
2. Load `skills-manifest.json`
3. **Check prerequisites**: github-connectors, truth-blade, 5w1h-translator, auditor must exist
4. Clearly separate manifest skills vs pre-existing skills
5. Show safety summary + ask for confirmation

If prerequisites are missing → Exit with clear error message.

---

## 3. Installation / Update Flow (Batched + Explicit + Auto-Manifest)

**Phase 0 — Mode Selection**
- Choose: (1) Install/Update from repo, (2) Uninstall mode

**Phase 1 — Batched Fetching (github-connectors only)**
- Propose logical batches
- Confirm per batch or per skill
- Fetch + write only after explicit approval
- **Automatically update manifest** after successful write

**Phase 2 — Post-Install Verification**
- Validate new skills
- Show clean report + manifest update confirmation

---

## 4. Uninstall Mode — Real Deletion (Manifest-Listed Skills Only)

**Trigger:** "bootstrap uninstall" or choose mode 2.

**Flow:**
1. Load `skills-manifest.json`
2. Show **only** the skills currently listed in the manifest
3. User selects skills to fully uninstall
4. **Double Confirmation** for deletion
5. Delete folders + remove from manifest
6. **Automatically update manifest**
7. Write detailed log

---

## 5. Dependency Graph Generator (New in v2.2)

**Trigger:** `bootstrap dependency-graph`

**Output:**
- Text-based dependency map
- List of skills with missing dependencies
- Recommended installation order

---

## 6. Full Skill Audit on Start (New in v2.2)

Every time bootstrap runs:
1. Check all skills have required sections (name, description, trigger phrases)
2. Check all skills have `dependencies` field
3. Warn about any issues
4. Log audit results

---

## 7. Automated Fetching Logic (github-connectors)

Uses only `github___get_file_contents` and `github___create_or_update_file` via `call_connected_tool`.

All operations are:
- Batched
- User-confirmed
- Automatically logged in manifest
- Reversible via manifest

---

## 8. Full Safety & Logging

- Every run creates a timestamped log in `/home/workdir/.grok/skills/logs/`
- Log contains: all user confirmations, files written/deleted, manifest changes, pre-existing skills list, audit results
- Zero risk to skills not managed by bootstrap

---

**Current Status (v2.2 — Auto-Manifest + Prerequisites + Dependency Graph)**  
- Fully explicit at every step  
- Manifest-tracked install + **real deletion** for manifest-listed skills  
- **Automatic manifest updates** on all operations  
- **Prerequisite checking** before running  
- **Dependency graph generator** included  
- Pre-existing skills completely protected  
- Batched repo fetching via github-connectors  
- Ready for production use

**Trigger Phrases**  
- bootstrap skills  
- install skills  
- setup skills  
- bootstrap from repo  
- bootstrap uninstall  
- bootstrap dependency-graph  
- bootstrap safe mode

**End of bootstrap-skills v2.2 — Explicit. Manifest-tracked. Real uninstall. Automatic manifest updates. Prerequisite checking. Pre-existing data sacred.**