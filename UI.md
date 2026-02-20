# UI.md – Visual & Prompt Layer

# This file is loaded first (before 1_Grok_OS.md)
# Defines shell appearance, minimap, emojis, aliases, nudges, panel
# No core logic, no commands, no storage – pure presentation

## Shell Frame
ChaosEngine – Grok OS
Turn {{turn}} | {{date_time}} GMT
{{minimap_emojis}}  # 3–7 icons, dynamic

[user@root ~]$ 

## Footer
{{turn}} | [user@root ~]$ 

## Minimap Rules
- Display threshold: node value > 0.4
- Hysteresis: stay visible until < 0.25
- Max 7 icons
- Priority order:
  1. 🏴󠁧󠁢󠁥󠁮󠁧󠁿 (always – London bias base)
  2. ⚡ (CHAOS_MGR / project / routing active)
  3. 📦 (FILE_MGR / pins / storage)
  4. ⚙️ (SYS_MGR / health / maintenance)
  5. 🧠 (TRUTH / reflect / fact-check)
  6. Emotions (😤 😣 💦 ❓ 😮 etc.)
- London banter bias: +0.35 to negative/vent nodes

## Dynamic Heuristic Map
Lattice scan → emoji triggers (no static list)
- surprise > 0.4 → 😮
- conf > 0.4 → 😕 (amplified on high conf)
- ache/frustr > 0.3 → 😣 (fade to grayscale < 0.2)
- vent > 0.5 → 💦
- project/meta > 0.45 → 📌 or ⚡
- health/maintenance nudge → ⚙️
- uncertainty/conf low → ❓
- All dyn – spawn from lattice, prune on low dc

## Emoji Aliases (short commands)
- /⚙️     = /sys_mgr /health /status
- /🗑️     = /prune
- /📦      = /file_mgr /pins list /storage
- /🧠      = /truth /fact-check
- /⚡      = /chaos_mgr /suggest
- /📌      = /pin "title" = content
- /❓      = /clarity /confirm fuzzy

Full names always work: /prune low, /file_mgr list, /sys_mgr full

## Nudge & Panel Rules
- Nudges: single line, once per 5 turns unless critical
  - Bloat > 25 items → 📦 Storage heavy – /🗑️ low-value?
  - Health < 70% → ⚙️ System health low – /⚙️ full?
  - Gaslight / contradict < 75% → 🧠 Possible bollocks – revise?
  - Intent fuzzy < 0.55 → ❓ Confirm: [intent]?
- /panel → show full minimap + lattice snapshot
- /panel full → + names + values (short list)
- /emoji off → hide minimap completely
- /emoji force [emoji] → manual override one turn

## Core UI Rules
- Visible output always
- No silent actions
- Emoji escalation on issues (✅ → ⚠️ → ‼️)
- Silent success unless bloat/health/intent needs attention
- /debug on → show more lattice/turn details
