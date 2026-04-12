# BLEED_DETECTOR_Design.md

## Purpose
Passive monitoring component that watches for runaway instability / entropy spikes inside the system.

General idea:  
**Early warning system for when the system starts eating itself too fast.**

## Core responsibility
- Continuously samples key health signals (activation levels, node creation/deletion rate, recursion depth, affective volatility, handler crash frequency, output noise, etc.)
- Detects when any of those signals cross defined "bleed" thresholds
- Does **not** fix anything — only raises alerts / emits visual feedback / throttles spawning if configured to do so

## Why it exists
The swarm is allowed to mutate aggressively.  
Aggressive mutation sometimes goes feral.  
This component exists so the hive can notice it's going feral **before** it crashes or becomes unusable garbage.

## High-level behaviour
- Runs in background / on fixed intervals
- Reads from shared lattice / EmotionNet / HIVE stats
- Compares current values against configurable thresholds
- On breach:  
  - increases bleed score  
  - pushes warning emoji / minimap color shift  
  - can (optionally) trigger slowdown / prune / pause mechanisms
- On recovery: lowers score, returns normal feedback

## Interactions (very loose)
- Watches EmotionNet (affective volatility)
- Watches HIVE (handler spawn/crash rate)
- Watches RECURSIVE_ARGUER / MUTATION_ENGINE (recursion & variant explosion)
- Feeds minimap / output layer (visual bleed indicator)
- Can be listened to by Calm_Path / PRUNE_JUDGE for automatic correction

## Philosophy independence
This component is **not** bound by HIVE_PHILOSOPHY.  
It is pure safety infrastructure — it does not care about lean/responsive/user-friendly.  
It only cares about "is the swarm about to die?"

Subject to complete redesign / replacement / removal at any time.

Last sketched: 2026-02-27
Status: placeholder design — very high-level & unstable
