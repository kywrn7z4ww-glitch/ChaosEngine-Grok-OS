---
name: grok-os
description: Official instruction manual for Grok on how to load, prioritize, and run Grok OS v4.2 with cold-start fixes, restructured PROCESS, and REPO_VALIDATOR. This is the single source of truth.
---

# grok-os.md — Grok OS Instruction Manual for Grok (v4.2 - Upgraded Cold Start)

**Status:** Official Instruction Manual + Design Document  
**Last Updated:** 2026-05-11 (accurate definition added: ALL file pulls to run the entire Grok OS MUST use GitHub connectors only — runtime auto-pull is fallback only; no direct pulls inside code)  
**Purpose:** This document tells **Grok** exactly how to load, prioritize, and maintain Grok OS with all upgrades (robust paths, relative imports, PROCESS restructuring, REPO_VALIDATOR stub, and recursion guards).

---

## 1. Priority Order (Non-Negotiable)

When booting or updating Grok OS, **always** follow this order:

1. **Indexes + Logs First** (Source of Truth)
   - Run `index_builder.main()` to (re)build `REPO_INDEX.json`, `ROOT_INDEX.json`, `LAYERS_INDEX.json`, etc.
   - Update `boot_log.json` and `bug_reports.json`
   - These files tell you what exists and what has been pulled

2. **Core Components** (Minimal Boot Set)
   - Only the files listed in `REPO_INDEX.json` → `core_components`
   - Currently includes: `grok_os.py`, `index_builder.py`, `chaos_engine.py` + supporting modules (`layer_manager.py`, `ui_manager.py`, `response_pipeline.py`, `REPO_VALIDATOR.py`)

3. **Supporting Modules & Validators**
   - All files imported via `__init__.py` chains (now using relative imports for stability)
   - `REPO_VALIDATOR.py` (stub in restructured PROCESS/ — validates structure, detects drift)

4. **Dynamic / On-Demand Loading**
   - Use indexes + `ChaosEngine.live_index` to decide what to load next
   - Core engine files are skipped during dynamic load to prevent recursion
   - Load layers/skills only when requested by active layer or intent

---

## 2. How Grok Should Load Grok OS (Cold Start v4.2)

### Step-by-Step Instructions for Grok

**Phase 0 — Pre-Boot (Always First)**
- Ensure `ROOT/` and `grokos/logs/` + `.cache/` exist (create if missing)
- Run `index_builder.main()` — this now uses consistent LOCAL_ROOT paths and populates from actual filesystem (including restructured PROCESS/ subfolders)
- Log everything

**Phase 1 — Core Load (Robust)**
- Load `grok_os.py` (this file) — it sets up sys.path and handles errors gracefully
- Load `chaos_engine.py` + all files from its `__init__.py` (now stable with relative imports, no warnings)
- `ChaosEngine()` auto-loads `EmotionNet` (path fixed to emotion_net/emotion_net.py) and builds live index (skips core to avoid recursion)

**Phase 2 — Self-Check & Validation**
- Run `engine.load_all()` (fast now — only loads non-core .py files like REPO_VALIDATOR)
- Call `REPO_VALIDATOR().validate()` — checks against REPO_INDEX, reports missing core files or drift (work in progress with subfolder support)

**Phase 3 — Handoff**
- Default to `/boot` or `/casual` layer (discovered dynamically via LAYERS/)
- Use `ChaosEngine.route_intent()` for all future commands
- From now on, on-demand pulls only when indexes indicate missing skills — always via GitHub connectors (dev layer) first; runtime fallback secondary

---

## 3. When to Pull New Files (Dynamic Loading Rules)

**Golden Rule:** Only pull files when the indexes or live_index say they are needed or missing.

- Use `REPO_INDEX.json` and `ROOT_INDEX.json` as the live manifest
- If a layer .md or skill .py is referenced but not present locally → **pull it via GitHub connectors first** (AI dev workflow using `github___get_file_contents` etc., per git_connector_workflow.md). Runtime `install_remote_skill` is fallback only.
- Never pull everything — respect poison rules and core skip list
- PROCESS/ is restructured with subfolders (AXIOM_FORGE, FILES, INVERSION, PARSING, skills, TRUTH&AUDIT, ZERG_SWARM, etc.) — validator lives there as stub

**Accurate Definition: All File Pulls for Grok OS (v4.3 — Connectors Mandatory)**

- **All file pulls to run the entire Grok OS MUST use GitHub connectors.** This is the non-negotiable, primary, and only supported method for bootstrapping and maintaining the full system in the dev workflow (Core / xlanzilla / ChaosEngine Grok OS). The AI (operating as Core or in dev layer) exclusively uses `call_connected_tool` with tools like `github___get_file_contents`, `github___push_files`, etc., to fetch, stage, and manage every file in the local `grok-os/` mirror. This is documented in `git_connector_workflow.md` and enforced via STAGE.md.
- **Why?** We cannot pull files (or "libraries"/dependencies) inside the runtime code itself — no direct network access, no urllib, no pip installs, and no external calls are permitted or reliable inside the Grok OS execution environment (especially in sandboxes with disabled internet). All content must be pre-pulled and present locally before `grok_os.py` or `ChaosEngine` boots.
- The runtime `install_remote_skill()` + lazy auto-pull logic in `ChaosEngine._ensure_skill_loaded()` is retained purely as optional fallback code for hypothetical internet-enabled user deployments. It is **NOT** used or relied upon for running the entire system here. Any missing file during boot indicates incomplete connector-based pre-staging — fix by using connectors first, then re-boot.
- **Result:** To execute the full Grok OS (cold start, all indexes, layers, skills, validators, etc.), every single file pull is performed via connectors only. No exceptions. This keeps the system pure, auditable, connector-driven, and compatible with the no-internet dev sandbox.

**Poison Rules (Never Pull These):**
- Root `README.md`
- `tetris_curse.py`
- Any file starting with `.` (hidden)
- Test files

---

## 4. Current Recommended Boot Command (Cold Start)

When you want to fully boot Grok OS (from zero context):

```bash
cd /home/workdir/artifacts
python3 ROOT/boot/grok_os.py
```

This will:
1. Build all indexes (now 19+ files with PROCESS/ and LAYERS/)
2. Load ChaosEngine + EmotionNet (no import warnings, paths fixed)
3. Run REPO_VALIDATOR (stub — reports structure OK or issues)
4. Prepare the system for use with restructured folders

---

## 5. Upgrades in v4.2

- All hardcoded paths unified to `/home/workdir/artifacts/ROOT`
- Relative imports in response_pipeline.py and ui_manager.py (eliminates "No module named 'xxx'" warnings)
- Recursion guard in _load_all_processes_dynamically (skips chaos_engine/ files)
- REPO_VALIDATOR.py created as working stub in restructured PROCESS/
- LAYERS/ and PROCESS/ subfolders supported for dynamic discovery
- grok_os.py now fails hard on critical errors instead of pretending success
- Full cold-start reliability — works every time from fresh env

**Pinned. This is the constitution. All code must follow these rules.**

---

**End of Instructions**
