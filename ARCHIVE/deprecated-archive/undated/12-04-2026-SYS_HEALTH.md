# SYS_HEALTH_Design.md

## Purpose
Passive background watchdog that monitors overall system stability and vital signs of the running hive.

One sentence:  
**The hive's pulse checker – watches if the whole organism is still breathing or starting to flatline.**

## Why it exists
Swarm can get chaotic fast (mutations, recursion spikes, handler crashes, bleed overflow, memory pressure).  
Someone has to notice when things are quietly going wrong before the user screams or the session dies.  
SYS_HEALTH is that someone – low-profile, always running, never sleeps.

## General idea of what it does
- Periodically samples key metrics (node count, activation averages, bleed score, handler load success/failure rate, recursion depth, exception count, output noise, latency spikes, etc.)
- Compares against soft & hard thresholds
- On warning level → subtle feedback (emoji shift, minimap tint, quiet log)
- On critical level → louder alert (prominent emoji, possible auto-throttle / pause suggestion)
- Does **not** auto-fix anything — only observes & reports

## Interactions (high-level only)
- Pulls stats from EmotionNet (affective volatility)
- Pulls stats from HIVE (handler health)
- Pulls stats from RECURSIVE_ARGUER / MUTATION_ENGINE (loop explosion risk)
- Pushes alerts to minimap / output layer
- Can be polled by Calm_Path / BLEED_DETECTOR for coordinated response

## Key invariants
- Runs quietly in background – never blocks user intent
- Zero side-effects on normal operation
- No execution of user code
- Always produces visual feedback (emoji / minimap change) on state change
- Can be muted / tuned / replaced at any time

Subject to complete redesign / removal / replacement.  
No tie to HIVE_PHILOSOPHY.  
Pure infrastructure / safety component.

Last sketched: 2026-02-27
Status: high-level design placeholder – very abstract
