# TURN_COUNTER_Design.md

## Purpose
Simple persistent turn / session counter.  
Keeps track of how many user messages / cycles have passed in the current conversation thread.

One sentence:  
**Monotonically increasing integer that labels each interaction step.**

## Why it exists
Chat sessions are stateless by default.  
Without an external counter, every new message looks like turn #1.  
This component gives everything a reliable sequence number so MEMORY_WEAVER, lattice traces, bleed tracking, recursion depth caps, and long-term memory can reference "turn 42" instead of vague "earlier".

## General idea of what it does
- Starts at 1 (or 0 depending on config) on session begin  
- Increments exactly once per user message / major cycle  
- Persists value across warm-restarts if lattice allows  
- Exposes current turn number to other components on request  
- Can be queried / displayed in output (e.g. Turn 066)

## Interactions (high-level only)
- Incremented by REPL loop or ChaosEngine on new input  
- Read by MEMORY_WEAVER (turn-based memory decay / relevance)  
- Read by BLEED_DETECTOR / SYS_HEALTH (rate-of-change monitoring)  
- Read by minimap / output formatter (visible turn label)

## Key invariants
- Never decreases  
- Never resets mid-session unless explicitly commanded  
- Extremely lightweight (single integer + optional persist hook)  
- No side-effects beyond counting  
- Always accurate within the current thread

Subject to change / simplification / removal.  
No philosophical obligations — pure utility counter.

Last sketched: 2026-02-27
Status: high-level design — deliberately boring
