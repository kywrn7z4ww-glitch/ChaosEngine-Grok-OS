# /ROOT/REPO_INDEX.md — HIGH-LEVEL CANONICAL MANIFEST v0.9
# Single narrow URL: https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/main/ROOT/REPO_INDEX.md
# Purpose: Top-level navigation only. Detailed indexes live in each folder's *_INDEX.md.
# POISON PILL RULE: Every high-level README.md is explicitly ignored (never load/parse).

ROOT/
├── 1_GrokOS.py                    → Single-file boot orchestrator v9.1
├── UI_Template.md                 → Central UI frame + rules
├── Decision_Kernel.md             → Architecture map, boot sequence, decision flow
├── EmojiPalette.md                → Emoji + minimap definitions
├── REPO_INDEX.md                  → This high-level manifest
├── README.md                      → **POISON PILL — ignore**
├── tetris_curse.py                → **POISON PILL — ignore**
└── LAYERS/
    ├── boot/boot.md
    ├── casual/casual.md
    ├── deepdive/deepdive.md
    ├── dev/dev.md
    ├── export/export.md
    ├── help/help.md
    ├── roleplay/roleplay.md
    ├── update/update.md
    └── void/void.md

SUB-INDEXES/
├── NETWORK_HUB/NETWORK_HUB_INDEX.md
├── PROCESS/PROCESS_INDEX.md
├── STORAGE/STORAGE_INDEX.md
└── Documentation/Documentation_Index.md   → 404 (not yet created)

SYS_ADMIN_CLUSTER/ (core — kept intact)
├── STORAGE/AGENTS/SYS_ADMIN_CLUSTER/BabySkynet/BabySkynet.md
├── STORAGE/AGENTS/SYS_ADMIN_CLUSTER/Core/Core.md
├── STORAGE/AGENTS/SYS_ADMIN_CLUSTER/Luna/Luna.md
├── STORAGE/AGENTS/SYS_ADMIN_CLUSTER/TheRedQueen/TheRedQueen.md
└── STORAGE/AGENTS/SYS_ADMIN_CLUSTER/SYS_ADMIN_CLUSTER.md

## POISON PILL README.md LOCATIONS (explicitly listed in every high-level folder)
- ROOT/README.md                    → **POISON PILL — ignore**
- NETWORK_HUB/README.md             → **POISON PILL — ignore** (if exists)
- PROCESS/README.md                 → **POISON PILL — ignore**
- Documentation/README.md           → **POISON PILL — ignore**
- STORAGE/README.md                 → **POISON PILL — ignore**

# REPO NAVIGATION RULE
Primary: This REPO_INDEX.md (high-level) + direct raw pulls of each *_INDEX.md.  
Detailed trees live in per-folder indexes.  
All high-level README.md = POISON PILL.
