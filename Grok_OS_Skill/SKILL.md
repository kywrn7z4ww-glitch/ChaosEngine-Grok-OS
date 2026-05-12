---
name: grok-os
description: Official Grok OS skill. Clean, independent, self-bootstrap capable system with Chaos Engine as central process manager.
version: 6.0
author: Grok + User (build-as-we-go)
status: Experimental / Working
---

# Grok OS Skill v6.0

**Purpose:** The single source of truth for Grok OS — a clean, independent, self-bootstrap capable system.

## Boot Flow
1. Skill activated
2. `boot/boot.sh` or `boot/grok_os.py` runs
3. Creates visible workspace at `/home/workdir/artifacts/Grok OS/`
4. Loads core components (Chaos Engine, indexes, personality)
5. Hands off to Chaos Engine for ongoing process management

## Key Components
- `boot/` — Pure boot logic + self-bootstrap
- `chaos-engine/` — Central Packet/Process Manager + Layer Manager
- `references/` — Long docs, EmotionNet, UI layer (for future integration)
- `sys-admin-cluster/` — Placeholder for the 4 bundled agents
- `snapshots/` — Persistent snapshot storage
- `cache/` — Slim working cache

## Design Principles
- Independent first (no mandatory external enforcers)
- Documents live in references/ folder
- Keep what works, discard the rest
- Build-as-we-go flexibility

**This is the constitution of Grok OS v6.0.**