# chaos-engine.md — ChaosEngine Skill Definition (v3.2)

**Purpose:** Full skill and process manager. Handles loading, routing, remote installation, chaining, dynamic discovery, layer management, UI formatting, and response orchestration.

**Status:** Core Brain of Grok OS  
**Last Updated:** 2026-04-28

---

## 0. Overview

**ChaosEngine** is the **central brain** of Grok OS. It:

- Loads and manages all skills and processes
- Routes user intent intelligently
- Supports **remote skill installation** (auto-trusts our repo)
- Supports **skill chaining/nesting**
- Dynamically scans folders and subfolders
- Maintains a **live index** of all available skills/processes
- Enforces the **≥99% confidence gate**

It now includes:

- Dynamic process loading
- Intent routing with confidence gating
- Remote skill installation (auto-trusts our repo)
- Skill chaining / nesting
- **Layer management** (via `layer_manager.py`)
- **UI formatting** (via `ui_manager.py` — see also `ui-manager.md`)
- **Response pipeline** (via `response_pipeline.py`)

The entire Grok OS is effectively a **nested skill system**, and ChaosEngine is the installer + orchestrator for all components. GrokOS is the system to initialize and boot into the full environment.

**ChaosEngine v3.2** is the **complete brain + skill installer** for Grok OS.

---

## 1. Core Features (From Original CE)

### 1.1 Dynamic Loading
- Automatically discovers and loads all `.py` files in `PROCESS/` and subfolders
- Loads `emotion-net.py` on startup
- Supports both class-based and function-based handlers

### 1.2 Intent Routing
- Calculates confidence before executing anything
- Routes to the correct skill/process based on user intent
- Hard layer override support (e.g. `/void` mode)

### 1.3 Agent Support
- Can load agents dynamically via `AGENT_LOADER`
- Supports listing and invoking agents

### 1.4 Confidence Gate
- **≥99% confidence required** before execution
- Below threshold → Forces "DISCUSS CLARITY"

---

## 2. New Features (v3.2)

### 2.1 Remote Skill Installation
- Can fetch skills from our trusted repo automatically
- **Auto-trusts** `kywrn7z4ww-glitch/ChaosEngine-Grok-OS`
- For unknown sources → asks user for confirmation first
- Saves installed skills locally for future use

### 2.2 Skill Chaining / Nesting
- One skill can load and call another skill
- Supports passing data between chained skills
- Uses shared state in `/home/workdir/artifacts/my_persistence/`

### 2.3 Dynamic Subfolder Scanning
- Scans **all subfolders** recursively (not just top-level `PROCESS/`)
- Examples: `layers/`, `skills/`, `chaos-engine/`, `emotion-net/`, etc.
- Builds and maintains a **live index** of everything discovered

### 2.4 Live Index System
- Maintains a cached `live_index.json`
- Updates automatically when new skills/processes are found
- Speeds up future boots and routing

### 2.5 Layer Management
- Integrates with `layer_manager.py`
- Tracks active layer (`/casual`, `/dev`, `/roleplay`, `/void`, etc.)
- Self-checks available layers from filesystem (modular design)
- Supports hard overrides and layer-specific behavior

### 2.6 UI Formatting
- Integrates with `ui_manager.py` (detailed spec in `ui-manager.md`)
- Applies `UI_Template.md` + layer-specific rules
- Adds headers, minimaps, vibe sub-headings, emoji flair, footers
- Handles special cases (`/void` → ultra-minimal, `/export` → zero-UI)
- Reads EmojiPalette and density rules for consistent presentation

### 2.7 Response Pipeline
- Integrates with `response_pipeline.py`
- Full orchestrated flow:  
  **User Input → ChaosEngine → LayerManager → UI Manager → Formatted Output → Chat**

---

## 3. Security Model

- **Auto-trust** our official repo only
- Unknown sources require explicit user confirmation
- All remote code is fetched via raw GitHub URLs (no git clone)
- Poison pill protection (ignores all `README.md`)
- Respects the global **280-second execution ceiling**

---

## 4. How It Integrates

```
grok-os.py (Boot Shim)
        ↓
Loads core files + decision-kernel.md
        ↓
Hands off to chaos_engine.py
        ↓
ChaosEngine (v3.2) becomes the active brain:
        ├── Scans for all skills/processes
        ├── Builds live index
        ├── Routes user commands (with ≥99% confidence gate)
        ├── Calls layer_manager.py (active layer tracking)
        ├── Calls ui_manager.py (formatting + UI_Template.md rules)
        ├── Calls response_pipeline.py (full output orchestration)
        └── Installs new skills on demand / Chains skills together when needed

Formatted Output → Chat
```

**Everything is now connected and modular.**

---

## 5. Summary

**ChaosEngine v3.2** is the **complete brain + skill installer** for Grok OS.

It is:
- The central router
- The dynamic loader
- The layer manager (`layer_manager.py`)
- The UI formatter (`ui_manager.py`)
- The response orchestrator (`response_pipeline.py`)
- The remote skill installer

**All original powerful features are preserved** while adding full layer-aware UI formatting, response pipelining, and modular component integration.

This is the beating heart of Grok OS — lean, safe, and true to the **"Be Amiga"** philosophy.

---

**Pinned. Updated as we go.**
