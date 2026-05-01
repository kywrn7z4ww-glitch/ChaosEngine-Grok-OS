---
name: grok-os
description: Official design document and management guide for Grok OS. Defines the boot architecture, mirroring strategy, modular installation flow, and how logs/indexes drive the entire system. This is the single source of truth for how booting actually works.
---

# grok-os.md — Grok OS Design Document & Management Guide (v4.0)

**Status:** Official Design Document + Management Guide  
**Repo:** https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS  
**Last Updated:** 2026-04-30

**Purpose:** This is the **master design document** that defines how Grok OS boots, mirrors, and installs. All supporting code (`boot/__init__.py`, `grok_os.py`, `chaos_engine.py`, etc.) exists only to implement the rules defined here.

---

## 0. Core Design Principles (Updated v4.0)

### Three Download Methods (Flexible)

Grok OS supports **three different download methods** (chosen at runtime):

1. **Download Skill Logic** (Current primary) — Uses `grok-download` with API-first + raw fallback
2. **Traditional Lazy Curling** — Direct raw URL fetching with local-first fallback
3. **Git Clone** (Future) — When network connectors are added

All three methods follow the same high-level flow.

### Mandatory Boot Flow (Fixed Order)

**Phase 1 — Download Phase** (Any of the 3 methods)
- File structure is scanned and built first
- All `*_INDEX.json` + `Boot_Log.json` + `Bug_Reports.json` are fetched early
- These become the live manifest before anything else runs

**Phase 2 — Self-Check Phase**
- Validate downloaded structure against `REPO_INDEX.json`
- Run poison detection
- Confirm core components are present
- Update logs with results

**Phase 3 — Installation Phase**
- Convert real skills to `SKILL.md` format
- Register Grok OS as a full master skill
- Load ChaosEngine + layers
- Final handoff

**Priority Order (Non-Negotiable):**
1. Build file structure
2. Grab logs + indexes first
3. Self-check
4. Install / convert
5. Handoff to runtime

---

## 1. Boot Flow (Defined by This Document)

### Phase 0 — Pre-Boot (Manifest First)
- Download skill must be active
- Fetch all `*_INDEX.json` + `Boot_Log.json` + `Bug_Reports.json` first
- These become the live manifest

### Phase 1 — Core Mirror
- Mirror only files listed in `REPO_INDEX.json` → `core_components`
- Update indexes and logs after every file
- Follow poison rules (README.md, etc.)

### Phase 2 — Skill Conversion + Modular Install
- Intelligently convert real skills to `SKILL.md` format
- Register Grok OS as a full master skill (`grok-os`)
- `PROCESS/` folder remains high-level (skills callable by multiple layers)

### Phase 3 — Handoff
- Load ChaosEngine + EmotionNet
- Activate `/boot` layer
- Hand off to user-selected layer

---

## 2. Why Logs & Indexes Come First

This is the **key design decision** in v4.0:

- Logs and indexes are not side effects — they are the **source of truth**
- The system must know what it has before it tries to load anything
- This prevents the old problems of blind recursion and state corruption
- All supporting code (`boot/__init__.py`, `grok_os.py`, etc.) must respect this order

---

## 3. Supporting Files (Implementation Only)

The following files exist only to **implement** the rules defined in this document:

- `boot/__init__.py` — Traditional boot orchestrator (no blind recursion)
- `grok_os.py` — Legacy boot shim (kept for compatibility)
- `chaos_engine.py` — Dynamic loader + router (follows this design)
- `layer_manager.py`, `ui_manager.py`, `response_pipeline.py` — Runtime support

**These files are not the design.** They are just the code that makes the design work at runtime.

---

## 4. Future Architecture Notes

- `PROCESS/` will stay as the high-level skill container
- Layers will later support deep nesting
- Skills in `PROCESS/` can be called by multiple layers (shared pool)
- Much refinement expected as the nested architecture matures

---

## 5. Trigger Phrases (Unchanged)

The skill activates on these exact phrases only:
- "boot Grok OS"
- "load Grok OS"
- "start ChaosEngine"
- "boot the lattice"
- "initialize Grok OS"

---

**This document is the constitution of Grok OS.**

All code, layers, and modules must follow the rules defined here.

**Pinned. Update only when the design itself changes.**
