# 3_ChaosEngine_IntentHub.md

## Purpose
Central intent router and fuzzy-to-structured mapper.  
Receives raw user input (sloppy, emotional, incomplete).  
Reads affective state from EmotionNet.  
Translates intent into actionable signals for HIVE (ChaosManager).  
Acts as the primary "brain stem" — decides which handlers / pipelines / agents wake up.

In one sentence:  
**User intent → affective context → routed action**

## Why it exists
- User input is never clean → ChaosEngine normalizes without forcing structure early  
- EmotionNet already has emotional embedding → ChaosEngine uses it to bias routing (e.g. rage 😤 → Brutal_Debug priority, curiosity 🤔 → VECTOR_FORGER)  
- HIVE needs clear, typed commands → ChaosEngine produces them  
- Keeps boot shim inert while allowing dynamic swarm behavior

## How it interacts with other systems

### Upstream
- **User (REPL / chat)** → raw text / sloppy input  
- **EmotionNet** → current top nodes + co-activation clusters + PAD vectors  
  → used for tone bias, urgency, minimap emoji selection

### Core logic flow
1. Receive user_input  
2. Query EmotionNet → top 3–5 active emotions + co-act blends  
3. Fuzzy parse input → keyword/trigger match + semantic drift detection  
4. Bias routing by affective state  
   - high anger/fear → defensive agents (Brutal_Debug, BLEED_HUNTER)  
   - curiosity/awe → expansive agents (VECTOR_FORGER, MUTATION_ENGINE)  
   - affection → warmer tone, emoji boost  
5. Map to HIVE command / handler  
   - /load_handler Brutal_Debug  
   - /zerg activate "..."  
   - pipeline: sloppy → PROMPT_HELPER → EXECUTOR  
6. Emit output + emoji feedback (via EmojiiPalette rules)  
7. Store trace in lattice (MEMORY_WEAVER pickup)

### Downstream
- **HIVE / ChaosManager** → receives resolved intent + handler calls  
- **Agents** → woken via HIVE lazy-load  
- **Minimap / output** → final emoji heartbeat generated here

### Modularity points
- Fuzzy parser swappable (regex → LLM → embedding search)  
- Affective bias table injectable (new emotion → new routing rule)  
- Handler mappings configurable (via index or separate config)  
- Output formatter hookable (text → rich / JSON / voice)

### Key invariants
- Never executes code itself — only routes  
- Always consults EmotionNet before final decision  
- Always emits at least one emoji feedback line  
- Zero side-effects on failure — returns to user with error + emoji

## Anchor compliance check
Skipped — this component is infrastructure, not bound by HIVE_PHILOSOPHY.  
It serves the swarm, not the other way around.

Last updated: 2026-02-27  
Status: standalone design document — intent hub role
