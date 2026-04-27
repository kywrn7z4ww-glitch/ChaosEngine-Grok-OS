# chaos-engine.md — ChaosEngine Skill Definition (v3.0)

**Purpose:** Full skill and process manager. Handles loading, routing, remote installation, chaining, and dynamic discovery.

**Status:** Core Brain of Grok OS  
**Last Updated:** 2026-04-27

---

## 0. Overview

ChaosEngine is the **central brain** of Grok OS. It:

- Loads and manages all skills and processes
- Routes user intent intelligently
- Supports **remote skill installation** (auto-trusts our repo)
- Supports **skill chaining/nesting**
- Dynamically scans folders and subfolders
- Maintains a **live index** of all available skills/processes
- Enforces the **≥99% confidence gate**

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

## 2. New Features (v3.0)

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

---

## 3. Security Model

- **Auto-trust** our official repo only
- Unknown sources require explicit user confirmation
- All remote code is fetched via raw GitHub URLs (no git clone)
- Poison pill protection (ignores all `README.md`)
- Respects the global **280-second execution ceiling**

---

## 4. How It Integrates
grok-os.py (Boot Shim)
↓
Loads core files + decision-kernel.md
↓
Hands off to chaos-engine.py
↓
ChaosEngine becomes the active brain:

Scans for all skills/processes
Builds live index
Routes user commands
Installs new skills on demand
Chains skills together when needed


---

## 5. Summary

ChaosEngine v3.0 is a **full-featured skill and process manager** that:

- Keeps all original powerful features
- Adds remote installation with smart trust model
- Supports skill chaining and nesting
- Dynamically scans subfolders and maintains a live index
- Remains lean, safe, and true to the "Be Amiga" philosophy

This is the beating heart of Grok OS.

---

**Pinned. Updated as we go.**
