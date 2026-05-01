# Mirroring Guide v1.0 — Batch-Based Repo Cloning

**Purpose:** Separate, optional mirroring strategy for keeping a local copy of the GrokOS repo in sync.

**Status:** Experimental / Alternative Method  
**Last Updated:** 2026-04-30

---

## 1. Overview

This is a **separate mirroring method** that can be used alongside (or instead of) the normal install logic.

It focuses on:
- Downloading index + log files first (as the manifest)
- Batch mirroring in controlled turns
- Keeping everything logged and indexed
- Being easy to abandon if we change direction later

---

## 2. High-Level Flow

### Turn 0 — Preparation
1. Make sure the **Download skill/module** is active and working
2. Have all target folders ready locally (`/grokos/`, `ROOT/`, etc.)

### Turn 1 — Core Manifest + Essential Files
1. Download these files first from the repo:
   - `REPO_INDEX.json`
   - All `*_INDEX.json` (ROOT, PROCESS, AGENT, STORAGE, NETWORK_HUB)
   - `Boot_Log.json`
   - `Bug_Reports.json`
2. Save them locally (they become the starting manifest)
3. Mirror only the **core components** listed in `REPO_INDEX.json` → `core_components`
4. Update `Boot_Log.json` with every file downloaded
5. Update relevant `*_INDEX.json` files (mark files as `pulled: true`)

### Turn 1.5 — ROOT Folder Batch Load
1. After Turn 1 is complete, begin loading the `ROOT/` folder and its subfolders in controlled batches
2. Prioritize high-value folders first (e.g. `layers/`, `boot/`, `chaos-engine/`)
3. **emotion-net** only receives a **partial load** at this stage (core files only) to leave room for future expansion
4. Update `ROOT_INDEX.json` and `Boot_Log.json` after each batch
5. Log any errors into `Bug_Reports.json`

### Turn 2 — Next Batch
1. Mirror the `/PROCESS` folder (or start with high-priority subfolders)
2. Mirror `/STORAGE/AGENTS/SYS_ADMIN_CLUSTER`
3. Update all affected indexes and `Boot_Log.json`
4. Log any errors into `Bug_Reports.json`

### Future Turns (Optional)
- Continue batching other folders as needed (`layers/`, `skills/`, `chaos-engine/`, etc.)
- Always update indexes + logs after each batch

---

## 3. Key Rules

- **Download skill must be active** before anything else
- Always download the **index + log files first** — they are the manifest
- Never mirror everything at once — use controlled batches
- Every action must update `Boot_Log.json`
- Every error must be logged in `Bug_Reports.json`
- This method is **optional** and can be abandoned without affecting the main install logic

---

## 4. Why This Approach?

- Gives us a clean, controllable way to mirror the repo
- Builds the indexes and logs as we go (instead of generating them blindly)
- Easy to pause, resume, or change batches later
- Keeps everything auditable through the logs

---

## 5. Current Status (2026-04-30)

- All required `.json` template files exist in `/grokos/`
- Download skill is available
- This guide is the new reference for the batch mirroring method

---

**This is a separate tool in the toolbox. Use it when it makes sense. Abandon it when it doesn’t.**

**Pinned. Update as needed.**
