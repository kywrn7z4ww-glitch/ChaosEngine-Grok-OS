# /STORAGE/AGENTS/AGENTS_INDEX.md — CANONICAL AGENTS MANIFEST
# Purpose: Dedicated index for all agents and personas in the Grok OS cluster.
# This file is the single source of truth for agent discovery and structure.

AGENTS/
├── AGENT_LOADER.py                    ← Dynamic loader (scans all subfolders)
├── Echo/Echo.md
├── Kerrigan/Kerrigan.md
├── SYS_ADMIN_CLUSTER/                 ← SYSTEM CRITICAL
│   ├── SYS_ADMIN_CLUSTER.md           ← Central hub & summoning logic
│   ├── BabySkynet/BabySkynet.md
│   ├── Core/Core.md
│   ├── Luna/Luna.md
│   └── TheRedQueen/TheRedQueen.md
└── System_Design_Team/
    ├── Logistics_Manager.md
    ├── Scared_Engineer.md
    ├── The_Planner.md
    └── The_Secretary.md

# AGENT NAVIGATION RULE
- Use AGENT_LOADER.py to dynamically load any agent by name.
- SYS_ADMIN_CLUSTER agents are system-critical and should be loaded early.
- Other agents (System_Design_Team, Kerrigan, Echo, etc.) are modular and can be added/removed as needed.
- All agents support future .py upgrades via AGENT_LOADER.
