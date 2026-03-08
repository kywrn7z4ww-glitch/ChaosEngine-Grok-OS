# ZERG_SWARM_Design.md

## Purpose
On-command internal swarm generator.  
Creates temporary, dynamic entities (mini-agents) that brainstorm, solve problems, or improve other system components.

One sentence:  
**Internal swarm factory — spawns disposable entities on demand to attack any task.**

## Why it exists
Sometimes a single agent or fixed pipeline is too slow, too narrow, or too rigid.  
This component lets the system instantly spin up a small, custom swarm of helpers tailored to the current problem (debugging, idea generation, component redesign, etc.).  
It keeps everything loose and adaptive — no fixed roster, no permanent agents, just temporary firepower when needed.

## General idea of what it does
- Triggered by explicit command or internal request  
- Takes a problem statement (or clarification)  
- Spawns a variable number of short-lived entities with loose roles (debug-style, idea-style, pattern-style, calm-style, etc.)  
- Entities think in parallel on the problem  
- Returns combined output + state summary  
- Everything is temporary — entities disappear after the task unless explicitly kept  

Definitions are deliberately loose and expected to change over time.  
No fixed number of entities, no locked roles, no permanent state.

## Interactions (high-level only)
- Receives command from ChaosEngine or user  
- Can pull context from lattice / MEMORY_WEAVER / FILE_MGR  
- Sends results back to output layer or pins cleaned output via FILE_MGR  
- Can be throttled by BLEED_DETECTOR or SYS_HEALTH if swarm grows too wild  

## Key invariants
- Always on-command only — never auto-spawns  
- Entities are temporary by default  
- Output is raw-ish but usable  
- No heavy persistence unless requested  
- Fully replaceable / rewritable at any time

Subject to complete redesign.  
Loose by design.  
Pure dynamic helper swarm utility.

Last sketched: 2026-02-27
Status: high-level design — intentionally fluid
