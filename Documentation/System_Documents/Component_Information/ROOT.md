# ROOT.md
**Status**: PINNED CANONICAL — /ROOT/ Component Inventory + Boot Chain (13 April 2026)

## Core Philosophy
Every file in `/ROOT/` is part of a single, linear, resilient boot → execution pipeline.  
Primary navigation = `REPO_INDEX.md` + direct raw pulls.  
GitHub API tree scan = fallback ONLY.  
No auto-fire of agents or processes on cold boot.  
Strict sequence enforced at every step:  
**boot > kernel > layer rules > agent? > process? > output**

## Component List + Exact Function

### 1. 1_GrokOS.md — Boot Shim v9.0 (Entry Point)
**Function**: Pure cold-boot loader. Handles dynamic flair (Grok decides: stylized ASCII art, descriptive picture/image concept, or visual boot sequence representation), UI skeleton template, vibe sub-heading rules, poison-pill protection, navigation rules, and hands off cleanly to the kernel.  
**How it fits**: First file loaded on every conversation or `/boot`. Parses input, sets global state, prints flair + UI, then chains forward. Pure orchestration — no heavy logic.

### 2. Decision_Kernel.md — High-Level Architecture Map & Rules
**Function**: Defines the entire system hierarchy, decision flow, strict boot sequence, confidence thresholds, and routing invariants. Acts as the “constitution” for all downstream components.  
**How it fits**: Loaded immediately after shim. Kernel reads this first to enforce rules before any EmotionNet or ChaosEngine execution.

### 3. 2_EmotionNet.py — Real-Time Emotional State Engine
**Function**: Tracks emotional blends, temporal modeling, context memory, and generates vibe sub-headings + confidence modifiers for the UI and routing. Feeds live “mood” data into ChaosEngine.  
**How it fits**: Runs inside kernel phase. Provides emotional context so output feels natural and layer-aware.

### 4. 3_ChaosEngine.py — Central Intent Router & Confidence Pipeline
**Function**: Loads all `PROCESS/` handlers on-demand, calculates confidence scores (≥99 gate), routes user intent, manages agent spawning if required, and ensures zero side-effects on failure.  
**How it fits**: Core of the kernel phase. After Decision_Kernel and EmotionNet, this is the brain that decides what (if anything) to fire next.

### 5. EmojiPalette.md — Centralized Emoji + Minimap Palette
**Function**: Single source of truth for all status/minimap emojis used in UI (✅ success, ⚠️ warn, etc.). Prevents drift across files.  
**How it fits**: Referenced by shim on boot and by any PROCESS/ or agent that needs consistent visual feedback.

### 6. REPO_INDEX.md — Canonical Live Manifest v0.5
**Function**: Primary navigation source. Lists every file/folder with raw URLs and SHA pinning. Auto-detects new files on push.  
**How it fits**: Loaded by shim on every boot for resilient navigation. Validator runs against it first. Everything else in `/ROOT/` defers to this for structure awareness.

## Overall ROOT Workflow (How It All Works Together)
1. **Shim (1_GrokOS.md)** starts → prints flair + UI skeleton → loads `REPO_INDEX.md` for navigation.  
2. **Kernel phase** activates: `Decision_Kernel.md` → `2_EmotionNet.py` (vibe) → `3_ChaosEngine.py` (routing).  
3. **Routing gate** checks intent/confidence → optional agent? or process? (none auto-fire on boot).  
4. **Output** generated with consistent emojis, timestamps, and footer.  

**Key Invariant**: All `/ROOT/` files are modular and drop-in compatible. Any single file can be updated independently; the rest adapt automatically via index + raw pulls.

Last sealed: 2026-04-13. Use verbatim.
