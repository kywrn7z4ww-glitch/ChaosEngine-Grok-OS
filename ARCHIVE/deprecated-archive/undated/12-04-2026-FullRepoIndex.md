# 5_FullRepoIndex_Design.md

## Purpose
Single source of truth for every important path in the entire fucking repo.  
One file. One place. You change a path → update here → everything else finds it without breaking.  
That's literally it.

## Why it exists
Because without it every other component has to hard-code URLs / paths / filenames like a moron.  
And when you rename something (which you will) the whole system turns into 404 spaghetti.  
This file stops that cancer before it starts.

It is **not** philosophy.  
It is **not** code.  
It is **not** documentation.  
It is a lookup table so dumb components don't have to guess where shit lives.

## How it works
- Plain markdown table  
- Columns: Component | Path / URL | Purpose | Notes / Last Reviewed  
- Every agent, handler, doc, pipeline, boot file, whatever — gets one row  
- ChaosEngine, HIVE, warm-boot loader, docs renderer — all read this file first  
- Format stays stupid simple so even a caveman can edit it with nano/vi/notepad

## Interactions
- **Upstream**: nothing — humans edit it manually  
- **Downstream**:  
  - ChaosEngine reads it for routing hints  
  - HIVE / ChaosManager uses it for lazy-load paths  
  - Warm-boot shim (2_SwarmBoot) pulls core paths from here  
  - Any future "scan repo" / auto-discovery logic starts here

## Why people still fuck it up
- They think it's "just another readme" → ignore it  
- They add new files → forget to add row → breakage  
- They rename shit → don't update index → everything dies  
- They expect magic auto-discovery → there is none  

Deal with it.  
One file. One truth.  
Update it or suffer.

## Key invariants
- Never executed as code  
- Never contains logic  
- Never depends on EmotionNet / philosophy / agents  
- Human edited only  
- Always raw.githubusercontent.com links for remote fetch  
- No emojis, no minimap, no feedback — just cold facts

Last updated: 2026-02-27  
Status: dumbest but most important file in the repo — change at your own risk
