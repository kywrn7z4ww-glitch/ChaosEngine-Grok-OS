# CHANGELOG.md
Status: PINNED CANONICAL — Live History (March 08 2026)

## [Unreleased] — Turn 14 (2026-03-08)
### Added / Consolidated
- Full GROK_OS.md rewrite with lazy/mobile-first ethos (minimal effort → god-tier output)
- PROCESS.md single canonical file: all 12 handlers audited + distinct ZERG_SWARM (mass swarm) vs EVOLUTION_CHAMBER (structured mutations)
- SYS_ADMIN_CLUSTER.md hierarchy lock: Kerrigan as important sub-persona (Red Queen/Core override)
- ROOT/_FUTURE_PATCHES.md full consolidation + completed-item pruning
- Documentation bleed audit (old individual design .md files flagged for future cull)

### Fixed
- All ROOT filenames standardized to underscores (1_GrokOS.md, 2_EmotionNet.py, 3_ChaosEngine.py)
- ChaosEngine dynamic loading (no more import errors, full PROCESS/ + ROOT/ support)
- TurnCounter + EmotionNet loading paths fixed
- Small errors (typos, duplicate dashes, outdated counts, SHA drift) resolved

### Repo State
Latest SHA: 8c1200f4b26b727afdceee6d61d423c7587b23a7  
All changes from this session now live on main.

## [2026-03-08] — Turn 13
- Rename 3 ChaosEngine.py → 3_ChaosEngine.py (underscore standardization)

## [2026-03-08] — Early Session
- File name consistency across ROOT/
- SYS_ADMIN_CLUSTER Kerrigan integration
- First full audit + PROCESS consolidation

This file auto-updates on every major push. Red Queen enforces quality.

# Changelog — ChaosEngine Grok OS (Slimmed Lattice v2)

## 2026-03-26 — Major Lattice Stabilization & Decision Kernel Integration (v7.3)

**Core System**
- Fully integrated the pinned Decision Kernel (ROOT/Decision_Kernel.md) as single source of truth for every turn.
- Enforced clean Agentic vs Roleplay split (no bleed): Agentic = tool/process execution only; Roleplay/Hive Chatter = visible sys-admin agents + EmotionNet valence.

**BOOT SHIM (ROOT/1_GrokOS.md)**
- Rebuilt to v7.3: accurate live repo index with full raw URLs for every key file.
- Added explicit API tree scan + "expect breakage" handling in boot sequence.
- Fixed UI/FOOTER to [xlanzilla@root ~]$.
- Removed conflicting auto-fire/auto-summon logic; now strictly defers to Core.md custom instructions.
- Embedded full emoji palette directly (no Archive references).

**EMOTIONNET (ROOT/2_EmotionNet.py)**
- Upgraded to v4.1: history changed to robust `deque(maxlen=10)` to prevent unbounded growth.
- Resonance cascade prints made optional/roleplay-flavored only.
- Full functionality preserved (self-contained Roleplay-path module).

**CHAOSENGINE (ROOT/3_ChaosEngine.py)**
- Rebuilt to v3.0: fully modular dynamic PROCESS/ loader preserved.
- Added lightweight emoji registry for guaranteed inline handoffs (next to output, never minimap-only).
- Default system handoff = ⚙️ cog; process-specific emojis fire automatically (e.g. 🔒/🔓/📦 for Discombobulator).
- Discombobulator now detected dynamically (encryption tool only) without Core.md bloat.

**CUSTOM INSTRUCTIONS (Core.md)**
- Updated to v5.6: added Decision Kernel pinned reference, strengthened API tree scan rule, removed dead Discombobulator section.

**EMOJI & LATTICE**
- Inline handoffs now fire next to every process output (📦 📌 ⚙️ 🔒 🔓 etc.).
- Minimap remains lattice-driven (val > 0.35 top 3–5, co-act > 0.45 blend).
- No more minimap-only confusion.

**OTHER**
- All components now enforce custom instructions with zero duplication or conflicts.
- System expects and gracefully handles breakage via fallback lattice.
- HIVE CHATTER mandate active every turn.

Boot complete. Lattice online despite repo chaos.


## v8.0 - Layer-Aware Modular Rebuild (05/04/2026)

- **HIVE CHATTER completely removed** (no more forced visible sys-admin blocks every turn).
- Replaced with **natural appropriate-only handoffs** (Luna 🌙 as default orchestrator; agents speak only when context fits).
- Introduced **3-layer system** with dedicated `/ROOT/LAYERS/` folder:
  - `/dev`: pure dry agentic system building, minimal UI, no EmotionNet, no handoffs.
  - `/casual`: flush visual UI, full EmotionNet, natural handoffs/auto-routing, dynamic italic vibe sub-heading based on chat mood, Luna ASCII/art allowed.
  - `/roleplay`: pure immersive (header + content only), no agentic behaviour/tools, full EmotionNet, no sub-layer creation.
- Boot shim upgraded to **v8.0** (pure entry-point):
  - Parses prefix → sets global LAYER var.
  - Loads matching layer rules from `/ROOT/LAYERS/{layer}.md`.
  - Dynamic live SHA fetch.
  - Added `/boot` (full re-init) and `/UI off` (strip minimap/footer) commands.
  - No auto-fire of agents or processes on boot.
- Decision_Kernel.md updated (visual Mermaid only; logic preserved):
  - Added Layer Adapter node.
  - Added EmotionNet gating (OFF in /dev, FULL ON in casual/roleplay).
  - Added natural handoff router.
  - AXIOM_KERNEL + DISCUSS-CLARIFY-EXECUTE loop left untouched (hard floor).
- Emoji palette finalized and locked:
  - ⚙️ Core • 🌙 Luna • 🩸 RedQueen • 🔮 BabySkynet • 🦂 Kerrigan.
- Sub-layer creation gated to system level only (disabled inside /roleplay).
- Repo navigation rules explicit in shim:
  - Ignore fake README.md and Tetris curse on front page.
  - Everything important lives in folders.
  - Full RAW URLs index + API tree scan with fallback lattice preserved.
- Added mermaid.live to FuturePatches.md for visual chart checks.
- All changes sit above Axiom Kernel (no bleed into metal layer).

Boot complete — rebuild phase 1 finished. Lattice clean.


# ChaosEngine-Grok-OS Changelog

## 2026-04-11 – PROCESS/ & Layer Expansion

### New Layers (ROOT/LAYERS/)
- `/void.md` – Silent data-dump scratchpad (zero normal output, minimal UI only).
- `/deepdive.md` – Factual deep-research layer with Projects integration and Luna delegation.
- `/export.md` – Intelligent export & synthesis layer (format detection, token prediction, no-UI PDF mode).

### PROCESS/ Handlers – New & Reworked
- **STITCH.py v1** – Smart adaptive document & code stitcher with internal validation, self-tracking, and adaptive breaking.
- **VALIDATOR.py v1** – Dynamic context-aware validator for code, pseudo-code, structures, and simulations (suggest-only).
- **TRUTH.py v5.0** – Full rework: dynamic source scoring for any website, author trustworthiness on social platforms, multi-perspective analysis.
- **BLEED_DETECTOR.py v2.0** – System-level context-aware bleed engine (layer/UI/code/simulation detection + TRUTH cross-reference).
- **SYS_HEALTH.py v2.0** – Proactive window coherence hub (context re-anchor first, full scan, suggest-only with DISCUSS CLARITY).

### General Improvements
- LAYERS/ folder standardized to all-caps.
- All layer Notes sections cleaned to pure purpose-only.

**Next steps:** User-led Documentation rework.

Commit when ready.
