# 4_HIVE_Manager_Design.md

## Purpose
Central handler registry, lazy loader, and module dispatcher for the ChaosEngine Grok OS swarm.  
HIVE.py is the runtime manager that knows where every handler (.proc), agent stub, and process lives — and loads them only when needed.

One sentence:  
**The hive's librarian & doorman — knows every door, opens them lazily, never executes anything itself.**

## Why it exists
- Swarm can have dozens of handlers/agents — loading everything at boot is wasteful and slow  
- Development is messy — files move, names change, new .proc appear — one place must track reality  
- Safety — prevent accidental execution of untrusted/unverified code during boot  
- Modularity — allow hot-swapping handlers without restarting the entire organism

## How it works (core responsibilities)

1. **Index awareness**  
   - Reads /ROOT/5 full-repo-index.md (or equivalent) at startup  
   - Builds internal map: component name → path/URL → type (handler, agent, pipeline, etc.)

2. **Lazy loading**  
   - /load_handler Brutal_Debug → resolves path → fetches raw content → exec() in isolated namespace  
   - Only loads when explicitly requested or triggered by ChaosEngine routing  
   - Caches loaded modules in memory for repeat calls

3. **Handler dispatch**  
   - Receives resolved intent from ChaosEngine (e.g. "activate Brutal_Debug")  
   - Looks up handler → if not loaded → load → call entry point  
   - Passes context (user input, EmotionNet state, lattice snapshot)

4. **Module registration**  
   - Allows dynamic registration of new handlers at runtime  
   - Exposes /register_handler <name> <path> for dev / extension

5. **Error boundary**  
   - Catches load/exec failures → returns clean error + emoji feedback  
   - Never crashes the entire session

## Interactions with other systems

### Upstream
- **ChaosEngine** → sends resolved intent + handler name  
- **EmotionNet** → provides affective context (optional bias for handler selection)

### Downstream
- **Individual handlers / agents** (.proc files in PROCESS/) — executes their code  
- **ZergLayer** — can request spawn / cull via HIVE  
- **Output layer** — receives handler results → formats + emoji

### Key invariants
- Never executes code on boot — only indexes  
- Zero side-effects on failed load  
- All fetches go through raw.githubusercontent.com (no local disk writes)  
- Handler namespace isolated — no global pollution  
- Always emits emoji feedback on success/failure

## Modularity & extensibility
- Index source swappable (markdown → JSON → database)  
- Load mechanism hookable (raw fetch → local disk → git submodule)  
- Handler entry point convention injectable  
- Error handlers pluggable

This component has **no dependency** on HIVE_PHILOSOPHY.md.  
It is infrastructure — it enables the swarm, it does not obey philosophical rules itself.

Last updated: 2026-02-27  
Status: standalone design document — handler & module manager role
