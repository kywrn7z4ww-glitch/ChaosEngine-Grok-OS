# ROOT/

**Grok OS Core Repository**  
**Status:** Active Development — 4.3 Migration in Progress

---

## Purpose of This README

This file exists so that **any automated system** (including future versions of Grok) that enters this folder immediately knows:

- The current state of the project
- The **correct order** of operations
- How to handle failures gracefully
- The overall philosophy: **"Mirror first → Install second"**

Without this, systems make assumptions and cause breakages (as we have seen).

---

## Core Rule: Mirror First, Install Second

**Never** begin Grok OS installation until the **full local mirror** is complete.

### Phase 1 – Build Local Mirror (Required First)
1. Install `grok-download` skill (if not already present)
2. Use it to scan GitHub and fetch **all** files from:
   - `PROCESS/`
   - `STORAGE/AGENTS/`
   - Core `ROOT/` files (including `emotion-net.md`)
3. Handle 404s, missing files, and breakages using the rules below
4. Only proceed to Phase 2 when mirror is 100% complete

### Phase 2 – Grok OS Installation (Only After Mirror Complete)
1. Follow `/boot` layer as the single entry point
2. Install everything as a **full nested Grok OS skill**
3. Run final validation

---

## Fetch & Mirror Rules (grok-download behavior)

When fetching files:

- **Primary method**: GitHub API via `browse_page` (for SHA/commit checking)
- **Fallback**: Raw URL (`raw.githubusercontent.com`)
- **If both fail (404)**:
  - Create placeholder file with expected structure
  - Log clearly: "MISSING: [filepath] — created placeholder"
  - Continue with next file (never halt the entire process)
- **If file exists but is broken**:
  - Move to `BROKEN/` folder
  - Log reason
  - Continue

**Special Rule for `PROCESS/skills/`**:  
These must remain **flat** (not nested inside Grok OS skill) until nesting is fully tested.

---

## Current Status (2026-04-29)

- Most layer `.md` files synced
- Several skills installed from `PROCESS/skills/`
- Many `.py` files in `PROCESS/` subfolders still returning 404 (not yet pushed)
- `emotion-net.md` core ready for fetch

**Next Action**: Complete full mirror of `PROCESS/`, `STORAGE/AGENTS/`, and core `ROOT/` files using `grok-download` skill.

---

**Last Updated:** 2026-04-29

