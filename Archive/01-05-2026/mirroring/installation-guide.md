# GrokOS Installation & Boot Guide v2.1

**Purpose:** Master reference document that points to both installation methods for redundancy.

**Status:** Master Reference Document  
**Last Updated:** 2026-04-30

---

## 0. Two Available Methods

GrokOS supports **two separate but compatible** methods for getting the system running:

1. **Traditional Installation** (this document) — Full boot + skill conversion + module registration
2. **Batch Mirroring** (`mirroring_guide.md`) — Controlled, auditable, batch-based cloning using our custom download function

Both methods can be used. The batch mirroring method is especially useful when internet access is limited or when you want maximum control and logging.

**Future Support:** When internet becomes available, both methods will also support `git clone`, `curl`, and other standard tools.

---

## 1. Philosophy

GrokOS follows a **"Boot Once + Lazy Runtime"** model.

- Do the heavy lifting **once** during boot (mirror, conversion, initial indexing)
- After boot, only load modules **when they are actually needed** (lazy loading)
- Every significant action must update the logs and indexes so the system always knows its own state

This keeps the system lean, stable, and easy to debug in a turn-based AI environment.

---

## 2. Core Principles

1. **Everything is a Module**  
   The download skill, skill conversion, logging, and indexing are all just modules — not special external systems.

2. **Logs & Indexes are the Source of Truth**  
   `Boot_Log.json`, `Bug_Reports.json`, and all `*_INDEX.json` files must be updated in real time. They are not optional.

3. **Intelligent Conversion Only**  
   Only files that actually look like real skills (contain proper YAML frontmatter with `name:` and `description:`) should be converted to `SKILL.md` format. Do not blindly convert everything.

4. **Minimal Core Mirror**  
   During boot, only mirror the files listed in `core_components` + essential folders. Everything else can be pulled on-demand later.

5. **Never Break the Modular System**  
   The existing recursive `__init__.py` loading and folder structure must be preserved. We enhance it, we do not replace it.

---

## 3. Recommended Boot Order (Phase by Phase)

### Phase 0 — Pre-Boot (One-time setup)
- Create all required `.json` files if they don't exist:
  - `REPO_INDEX.json`
  - `ROOT_INDEX.json`, `PROCESS_INDEX.json`, `AGENT_INDEX.json`, `STORAGE_INDEX.json`, `NETWORK_HUB_INDEX.json`
  - `Boot_Log.json`
  - `Bug_Reports.json`

### Phase 1 — Boot Trigger (when user says "boot Grok OS")
1. Load the Download skill/module
2. Download all `*_INDEX.json` + log files first (they act as the manifest)
3. Populate/update the indexes with current state
4. Mirror only the core boot files listed in `REPO_INDEX.json` → `core_components`
5. Intelligently convert real skills to `SKILL.md` format (only where it makes sense)
6. Update `Boot_Log.json` with every major step
7. Update `Bug_Reports.json` if any errors occur

### Phase 2 — Post-Boot
- System is now considered "booted"
- All core indexes and logs are up to date
- No full recursive loading happens here

### Phase 3 — Runtime (Lazy + On-Demand)
- When a skill, layer, or command is actually called → load it then
- Use the indexes to check if it's already available
- If missing → trigger a light on-demand pull + update logs/indexes
- Never do full recursion on every turn

---

## 4. Post-Mirroring + Full Skill Installation

After the core mirror is complete, the system performs the following steps:

1. **Module Fetching**  
   All discovered `.py` and `.md` files in `ROOT/` and `PROCESS/` are scanned. Only files that match skill criteria (proper YAML frontmatter) are converted to `SKILL.md` format.

2. **Skill Conversion**  
   Real skills are converted and registered. The `PROCESS/` folder remains high-level — it contains callable skills that can be invoked by multiple layers.

3. **Grok OS as a Full Skill**  
   The entire GrokOS system is installed as one master skill (`grok-os`). This allows the system to be treated as a single installable unit while still exposing individual modules and layers.

4. **Module Updates**  
   Any existing modules are checked for updates. New or changed files are pulled and re-registered. Indexes and logs are updated after every change.

**Important Notes (Future Architecture):**
- `PROCESS/` folder will stay as the high-level skill container
- Layers (`/casual`, `/dev`, `/roleplay`, etc.) will later support nested sub-layers and deeper module organization
- Skills in `PROCESS/` can be called by multiple layers (shared skill pool)
- Much refinement is expected later as the nested layer + skill architecture matures

---

## 5. Logging Rules (Mandatory)

- **Boot_Log.json** must be updated on every major action:
  - Boot started
  - File downloaded
  - Index updated
  - Skill converted
  - Module loaded
  - Error occurred

- **Bug_Reports.json** must be updated on every error or warning (with full `data` object for rich debugging)

- Both logs should be updated **immediately** after the action completes (not at the end of boot).

---

## 5. How to Make Changes Strategically

When modifying the system:

1. **Always read this guide first**
2. Only touch the minimum files needed for the change
3. Update the relevant log/index immediately
4. Test the change in isolation before touching other parts
5. Never do a "big bang" rewrite — evolve the system in small, safe steps

---

## 6. Current State (as of 2026-04-30)

- All required `.json` template files have been created in `/grokos/`
- The old blind recursive loading system is still in place and needs to be enhanced
- The new "Boot Once + Lazy Runtime" model is the target architecture

---

**This document is the single source of truth. All future changes should be made with reference to this guide.**

**Pinned. Update as we evolve.**
