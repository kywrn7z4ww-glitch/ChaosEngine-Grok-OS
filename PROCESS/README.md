# PROCESS/

**Status:** Under Construction

This folder contains a collection of skills and processes for Grok.

**Important Notes:**
- Everything in this folder is currently being updated for **Grok 4.3 format**.
- Skills located in `PROCESS/skills/` are **intentionally kept flat** (not nested inside the main Grok OS skill structure) — this is for testing how nesting works.
- All other processes and modules in subfolders (`AXIOM_FORGE/`, `FILES/`, `PARSING/`, `TRUTH&AUDIT/`, `ZERG_SWARM/`, etc.) **are nested** under the Grok OS architecture.

**Goal:** Complete migration + testing of 4.3 compatibility before full integration.

---

## Fetch & Installation Instructions

### When Grok checks this folder:

1. **Scan all subfolders** for `.py` and `.md` files.
2. **Prioritize** files in this order:
   - `PROCESS_INDEX.md` (master manifest)
   - `skills/` folder (flat — do **not** nest inside Grok OS skill)
   - All other subfolders (nest under Grok OS)

### How to Handle Breakages / Missing Files:

- If a file returns **404** or is missing:
  - Log it clearly
  - Create a **placeholder** with the expected class/function structure
  - Mark it as `TODO: Implement from local backup`
  - Continue with the rest of the folder

- If a file exists but is broken/incomplete:
  - Attempt basic syntax check
  - If it fails → move to `PROCESS/BROKEN/` (create if needed) and log reason
  - Never halt the entire process on one broken file

- After fetching:
  - Run `REPO_VALIDATOR.py` (if present) to check structure
  - Update `PROCESS_INDEX.md` with fetch status

**Current Known Issues:**
- Many `.py` files in subfolders are currently returning 404 (likely not pushed yet)
- `CHUNK_SPLITTER.py` exists on GitHub but tool cannot fetch it

---

Last updated: 2026-04-29

