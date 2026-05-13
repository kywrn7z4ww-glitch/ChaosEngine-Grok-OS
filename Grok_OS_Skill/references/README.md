# ROOT/ — Grok OS Core Repository

**Grok OS Core Repository**  
**Status:** Active Development — v4.0 Architecture (3-Phase Boot + Logs-First)

---

## Purpose of This README

This is the **high-level architecture document** for the entire Grok OS system.

It explains:
- The overall philosophy and design
- The mandatory boot flow
- How everything connects
- Where to find more details (subfolder READMEs)

**Rule:** This document stays high-level. All detailed explanations live in subfolder READMEs.

---

## Core Philosophy (v4.0)

**"Mirror First → Self-Check → Install Second"**

Grok OS follows a strict **3-Phase Boot Flow**:

1. **Download Phase** (any method: Download Skill / Traditional Curling / Git Clone)
   - File structure is built first
   - All `*_INDEX.json` + `boot_log.json` + `bug_reports.json` are fetched early
   - These become the live manifest

2. **Self-Check Phase**
   - Validate structure against `REPO_INDEX.json`
   - Run poison detection
   - Confirm core components exist
   - Log everything

3. **Installation Phase**
   - Convert real skills to `SKILL.md` format
   - Register Grok OS as a full master skill
   - Load ChaosEngine + layers
   - Final handoff to runtime

**Non-Negotiable Rule:** Logs and indexes come **first**. No blind recursion. Everything is auditable.

---

## Key Folders & Their Purpose

| Folder              | Purpose                                      | Details In                  |
|---------------------|----------------------------------------------|-----------------------------|
| `boot/`             | Boot orchestrator + index builder            | `boot/README.md`            |
| `logs/`             | All system logs (`boot_log.json`, etc.)      | `logs/README.md`            |
| `PROCESS/`          | High-level callable skills                   | `PROCESS/README.md`         |
| `layers/`           | Layer definitions (`/casual`, `/dev`, etc.)  | `layers/README.md`          |
| `chaos-engine/`     | Central brain + dynamic loader               | `chaos-engine/README.md`    |
| `emotion-net/`      | Emotional state engine                       | `emotion-net/README.md`     |
| `NETWORK_HUB/`      | External URLs, modules prone to deprecation, future expansion (music hosting, etc.) | `NETWORK_HUB/README.md` |
| `Documentation/`    | User-created docs, templates, not frequently updated | `Documentation/README.md` |
| `STORAGE/`          | Storage for agents, data, and persistent state | `STORAGE/README.md`         |
| `AGENTS/`           | Agent definitions and clusters (including SYS_ADMIN_CLUSTER) | `AGENTS/README.md` |
| `Archive/`          | Old data from big file changes, sorted by date | (Historical only)           |

---

## Important Design Documents

- `grok-os.md` → **Master design document** (read this first)
- `INSTALLATION_GUIDE.md` → Traditional + batch mirroring methods
- `mirroring_guide.md` → Detailed batch mirroring strategy
- `boot.md` → `/boot` layer rules

---

## Current Status (2026-05-01)

- `boot/__init__.py` + `grok_os.py` + `chaos_engine.py` = v4.1 (full logging + index builder)
- All core indexes and logs use proper template format with `{VARIABLE}` placeholders
- System is stable and ready for further expansion

---

**This is the beating heart of Grok OS.**

Everything else is implementation detail.

**Pinned. Update only when the high-level architecture changes.**
