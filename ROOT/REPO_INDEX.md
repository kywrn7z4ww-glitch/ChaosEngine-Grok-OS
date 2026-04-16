# /ROOT/REPO_INDEX.md — HIGH-LEVEL CANONICAL MANIFEST v0.9
# Single narrow URL: https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/main/ROOT/REPO_INDEX.md
# Purpose: Top-level navigation only. Detailed indexes live in each folder's *_INDEX.md.
# POISON PILL RULE: Every README.md in high-level folders is explicitly ignored (never load/parse).

## CORE SYSTEM FILES (ROOT/)
- ROOT/1_GrokOS.py                  → Single-file boot orchestrator v9.1
- ROOT/UI_Template.md               → Central UI frame + rules (FLAT)
- ROOT/Decision_Kernel.md           → Architecture map, boot sequence, decision flow
- ROOT/EmojiPalette.md              → Emoji + minimap definitions
- ROOT/REPO_INDEX.md                → This file (high-level manifest)
- ROOT/README.md                    → **POISON PILL — ignore**
- ROOT/tetris_curse.py              → **POISON PILL — ignore**

## ROOT/LAYERS/ — Per-Layer Folders (full tree)
- ROOT/LAYERS/boot/boot.md          → Mandatory first layer + REPO_VALIDATOR
- ROOT/LAYERS/casual/casual.md      → Casual vibe layer
- ROOT/LAYERS/deepdive/deepdive.md  → Factual deep-research layer
- ROOT/LAYERS/dev/dev.md            → Dev/debug layer
- ROOT/LAYERS/export/export.md      → Intelligent file manipulation/export layer
- ROOT/LAYERS/help/help.md          → Gentle onboarding & navigation layer
- ROOT/LAYERS/roleplay/roleplay.md  → Pure immersive narrative layer
- ROOT/LAYERS/update/update.md      → Git maintainer & lattice updater
- ROOT/LAYERS/void/void.md          → Dark silent data-dump scratchpad

## SUB-INDEXES (detailed trees)
- NETWORK_HUB/NETWORK_HUB_INDEX.md  → Full NETWORK_HUB tree
- PROCESS/PROCESS_INDEX.md          → Full PROCESS/ tree
- STORAGE/STORAGE_INDEX.md          → Full STORAGE/ tree
- Documentation/DocumA
A
A
Aentation_INDEX.md → Full Documentation/ tree

## SYS_ADMIN_CLUSTER (kept intact — core system)
- STORAGE/AGENTS/SYS_ADMIN_CLUSTER/BabySkynet/BabySkynet.md
- STORAGE/AGENTS/SYS_ADMIN_CLUSTER/Core/Core.md
- STORAGE/AGENTS/SYS_ADMIN_CLUSTER/Luna/Luna.md
- STORAGE/AGENTS/SYS_ADMIN_CLUSTER/TheRedQueen/TheRedQueen.md
- STORAGE/AGENTS/SYS_ADMIN_CLUSTER/SYS_ADMIN_CLUSTER.md

## POISON PILL README.md LOCATIONS (explicitly listed in every high-level folder)
- ROOT/README.md                    → **POISON PILL — ignore**
- NETWORK_HUB/README.md             → **POISON PILL — ignore** (if exists)
- PROCESS/README.md                 → **POISON PILL — ignore**
- Documentation/README.md           → **POISON PILL — ignore**
- STORAGE/README.md                 → **POISON PILL — ignore**

# REPO NAVIGATION RULE (post-validator)
Primary: This REPO_INDEX.md (high-level) + direct raw pulls of each *_INDEX.md.  
Detailed file trees live in the per-folder indexes + explicit LAYERS/ section above.  
SYS_ADMIN_CLUSTER remains core and un-split. NETWORK_HUB added as proactive high-level hook.
Every README.md in high-level folders is explicitly a poison pill — never load or parse.
