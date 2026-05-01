# GrokOS Mirror Logic & Boot Guide v2.5

**Purpose:** Single source of truth for both the batch mirroring strategy and the overall boot/install process. Combines the previous separate guides into one cohesive reference.

**Status:** Master Reference Document  
**Last Updated:** 2026-05-01

---

## 0. Overview

GrokOS supports **two compatible methods** for getting the system running:

1. **Batch Mirroring** (this document) — Controlled, auditable, manifest-driven cloning using the custom Download Skill. Ideal when you want maximum control, logging, and the ability to pause/resume.
2. **Traditional Installation** — Full boot + skill conversion + module registration (still supported for redundancy).

Both methods follow the same high-level **"Boot Once + Lazy Runtime"** model:
- Do the heavy lifting **once** during boot (mirror + indexing)
- After boot, only load modules **on-demand** (lazy)
- Every significant action updates logs and indexes in real time

---

## 1. Master Boot Sequence (Authoritative)

The `REPO_INDEX.json` → `boot_sequence` is the single source of truth for the order of operations. The mirror logic **must** follow these phases:

### Phase 0 — Pre-Boot
- Activate Download Skill module first
- Fetch **ALL** `*_INDEX.json` + `boot_log.json` + `bug_reports.json` before anything else
- Call `index_builder.py` to populate local indexes from disk
- These files are the live manifest and source of truth

### Phase 1 — Core Mirror
- Pull **ONLY** the files listed in `REPO_INDEX.json` → `core_components`
- After each successful pull: update the relevant sub-index (`pulled: true` + timestamp) and append to `boot_log.json`
- Respect poison rules (skip `README.md`, `tetris_curse.py`, hidden files, tests)

### Phase 1.5 — ROOT Batch Load
- Controlled batch mirroring of `ROOT/` folder
- Priority order: `layers/` → `boot/` → `chaos-engine/`
- `emotion-net/` receives **partial load only** (core files) to leave room for future expansion
- Update `ROOT_INDEX.json` + `boot_log.json` after every batch
- Log errors to `bug_reports.json`

### Phase 2 — Next Batch
- Mirror `PROCESS/` (high-priority subfolders first)
- Mirror `STORAGE/AGENTS/SYS_ADMIN_CLUSTER`
- Update all affected indexes and `boot_log.json` after each batch

### Phase 3 — Handoff + Lazy Runtime
- Mark boot complete in `boot_log.json`
- Enable on-demand / lazy pulls for any missing files using the indexes
- Handoff to user-selected layer or ChaosEngine
- Future: when connectors are available, support `git clone` / full install on top of this mirror

---

## 2. Core Principles

1. **Everything is a Module**  
   The Download Skill, skill conversion, logging, and indexing are all just modules — not special external systems.

2. **Logs & Indexes are the Source of Truth**  
   `boot_log.json`, `bug_reports.json`, and all `*_INDEX.json` files must be updated in real time. They are not optional.

3. **Minimal Core Mirror First**  
   During Phase 1, only mirror the files listed in `core_components`. Everything else can be pulled on-demand later.

4. **Controlled Batches, Never Big Bang**  
   Never mirror everything at once. Use the phased approach so the system can be paused, resumed, or abandoned safely.

5. **Never Break the Modular System**  
   The existing recursive `__init__.py` loading and folder structure must be preserved. We enhance it, we do not replace it.

---

## 3. Download Skill (grok-download)

The Download Skill is the engine that powers mirroring. It must be active before any mirroring begins.

**Key Features:**
- Primary method: GitHub API via `browse_page` for SHA + tree scanning
- Fallback: raw.githubusercontent.com URLs
- Full recursive tree scanning for folders
- Poison filtering (root files only: `README.md`, `tetris_curse.py`, hidden files, tests)
- High-level folders (`PROCESS/`, `layers/`, `boot/`, `chaos-engine/`, `emotion-net/`, `STORAGE/`, `NETWORK_HUB/`) are always safe
- SHA verification + `.meta.json` / `.sha256` sidecars
- Graceful error handling (placeholders + `BROKEN/` folder on failure)
- Self-bootstrap capable

**Usage (when implemented):**
```bash
grok-download --profile grok-os https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/tree/main/ROOT
```

---

## 4. Logging Rules (Mandatory)

- **boot_log.json** must be updated on every major action:
  - Boot started
  - File downloaded
  - Index updated
  - Skill converted
  - Module loaded
  - Error occurred

- **bug_reports.json** must be updated on every error or warning (with full `data` object for rich debugging)

- Both logs must be updated **immediately** after the action completes.

---

## 5. Post-Mirror Steps (When Full Install is Desired)

After the core mirror is complete, the system can optionally perform:

1. **Module Fetching** — Scan all `.py` and `.md` files in `ROOT/` and `PROCESS/`
2. **Intelligent Skill Conversion** — Only files with proper YAML frontmatter (`name:` + `description:`) are converted to `SKILL.md` format
3. **Grok OS as Master Skill** — The entire system is registered as `grok-os`
4. **Module Updates** — Check for changes and re-register as needed

**Future Architecture Notes:**
- `PROCESS/` stays as the high-level skill container (callable by multiple layers)
- Layers will later support deep nesting
- Much refinement expected as the architecture matures

---

## 6. Current Status (2026-05-01)

- `REPO_INDEX.json` v2.5 with cleaned `core_components` and `boot_sequence` is live
- `mirror_logic.py` + `__init__.py` exist in `mirroring/` folder (workaround entry point)
- Download Skill spec (`grok-download.md`) is complete; Python implementation pending
- This `mirror-logic.md` is the single source of truth for the mirroring + boot flow

---

**This document is the single source of truth. All future changes should be made with reference to this guide.**

**Pinned. Update as we evolve.**
