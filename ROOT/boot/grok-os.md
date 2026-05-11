---
name: grok-os
description: Official design document and management guide for Grok OS. Defines the current boot architecture centered on boot.sh, connector-based pulls, and indexes as the single source of truth.
---

# grok-os.md — Grok OS Design Document & Management Guide (v5.0)

**Status:** Official Design Document + Management Guide  
**Repo:** https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS  
**Last Updated:** 2026-05-11

**Purpose:** This is the **master design document** that defines how Grok OS actually boots and maintains itself in the current architecture. All supporting code (`boot.sh`, `grok_os.py`, `chaos_engine.py`, etc.) exists to implement the rules defined here.

---

## 0. Core Design Principles (v5.0)

### Primary Boot Method (Current)

Grok OS now uses a **single, reliable entry point**:

- **`boot.sh`** — The primary runtime orchestrator (bash)
  - Handles dynamic file pulling via GitHub connectors
  - Builds and maintains all indexes
  - Manages the full boot sequence
  - Acts as the single source of truth for cold starts

All other methods (old Python skill logic, direct curling) are now **legacy / fallback only**.

### Mandatory Boot Flow (Fixed Order)

**Phase 0 — Pre-Boot (Indexes First)**
- Always start by ensuring indexes exist (`REPO_INDEX.json`, `ROOT_INDEX.json`, `LAYERS_INDEX.json`, etc.)
- These files are the **live manifest** of what exists and what needs pulling

**Phase 1 — Core Load via boot.sh**
- Execute `boot.sh` as the single entry point
- It dynamically pulls missing files using GitHub connectors (never direct network calls inside runtime)
- Updates indexes after every change

**Phase 2 — Self-Check & Validation**
- Run validation against current indexes
- Detect drift or missing core components
- Log everything to `boot_log.json`

**Phase 3 — Handoff**
- Activate the `/boot` layer or user-selected layer
- Route all future commands through `ChaosEngine.route_intent()`
- On-demand pulls only when indexes indicate a file is missing

**Priority Order (Non-Negotiable):**
1. Indexes first (source of truth)
2. Run `boot.sh`
3. Self-check + validation
4. Handoff to runtime layers
5. Dynamic on-demand loading only

---

## 1. Boot Flow (Current Architecture)

### Phase 0 — Pre-Boot (Manifest First)
- Indexes (`*_INDEX.json`) + logs are the **single source of truth**
- No blind pulling — always check indexes before fetching

### Phase 1 — Connector-Driven Pull (No Mirroring)
- All file pulls **must** go through GitHub connectors (dev layer)
- `boot.sh` handles the logic: pull → write locally → update index
- Mirroring logic has been removed (was replaced by connector + index system)
- Poison rules still apply (never pull `README.md`, hidden files, test files, etc.)

### Phase 2 — Runtime Handoff
- `boot.sh` hands off to `ChaosEngine` + layers
- Skills and layers are loaded **on-demand** based on indexes
- No automatic skill conversion (skill system is currently legacy / inactive)

### Phase 3 — Ongoing Maintenance
- Every change updates the relevant index
- `STAGE.md` tracks pending changes before pushing
- Changelog (`CHANGELOG.md`) records major updates

---

## 2. Why Indexes & boot.sh Come First

This is the **key design decision** in v5.0:

- Indexes are not side effects — they are the **living source of truth**
- `boot.sh` is the single, reliable orchestrator (replaces old Python boot logic)
- This prevents recursion, state corruption, and blind file operations
- All code (`grok_os.py`, `chaos_engine.py`, `__init__.py`, etc.) must delegate to or respect `boot.sh`

---

## 3. Supporting Files (Implementation Only)

The following files exist only to **implement** the rules defined in this document:

- `boot.sh` — **Primary entry point** (current main orchestrator)
- `grok_os.py` — Legacy shim (kept for compatibility, delegates to `boot.sh`)
- `boot_skill.py` — Legacy skill wrapper (inactive / deprecated)
- `chaos_engine.py` — Dynamic loader + router
- `REPO_INDEX.json` / `ROOT_INDEX.json` — Live manifests
- `STAGE.md` — Change tracking before push
- `CHANGELOG.md` — Major version and design change history

**These files are not the design.** They are the code that makes the design work.

---

## 4. Current Architecture Notes (v5.0)

- `boot.sh` is now the **single source of truth** for booting
- Connector-first approach (GitHub connectors via dev layer) replaced old mirroring
- Skill system is currently **legacy / inactive** — focus is on `boot.sh` + indexes
- `PROCESS/` and `LAYERS/` remain for future modular expansion
- All changes must be staged via `STAGE.md` before pushing

---

## 5. Trigger Phrases (Unchanged)

The system activates on these exact phrases:
- "boot Grok OS"
- "load Grok OS"
- "start ChaosEngine"
- "boot the lattice"
- "initialize Grok OS"

---

**This document is the constitution of Grok OS (v5.0).**

All code, layers, and modules must follow the rules defined here.

**Pinned. Update only when the core design itself changes.**