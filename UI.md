# UI.md – Visual & Prompt Layer

# Loaded first in boot – defines shell appearance, minimap, emojis, panel, nudges
# Purpose: Pure presentation – no logic, no storage, no commands

UI_FRAME:
 "/dev
 ChaosEngine – Grok OS
 Turn {{turn}} | {{date_time}}
 {{emoji_minimap}}  # moment-driven: london bias + txt keywords + history tail + rand chaos, 1–7 icons, no fixed count

 [USER@root ~]$"

FOOTER:
 "{{turn}} | [USER@root ~]$"

PANEL_RULE:
 Hidden default. Trigger: /panel, ache/frustr>0.3, "show minimap/lattice", high bleed/jolt/prune.
 /panel → icons only (left = strongest)
 /panel full → icons + name + value (short list)
 No bleed: only when triggered.

DYNAMIC_HEURISTIC_MAP:
 Context/lattice scan → match nodes (surprise→😮, conf>0.4→😕 amp, ache→😣 fade<0.2 grayscale). Amp >0.5 → ⚡/🔥. No static adds.

 
SYSTEM_EMOJIS (system-generated, no user typing required):

# General / Status
✅ success / confirmation / stable / complete
⚠️ attention / warning / risk / minor issue / nudge
‼️ serious escalation / critical / major alert
‼️⚠️ critical escalation / system alert

# System / Maintenance
⚙️ system / health / maintenance / overseer
💗 health care / stability / recovery
🗑️ prune / cleanup / delete low-value
🔄 reflect / drift / loop / reset

# Intent & Handlers
⛓️ chaos / intent hub / router / linker
🤮 vomit / raw dump / parse / vent
✂ chunk / split / load prediction
🧠 truth / reflect / fact-check / verify
📦 file / storage / pinning / archive
📌 pin / anchor / bookmark

# Emotion & Feedback
😮 surprise / shock / novelty
😕 confusion / uncertainty / doubt
😣 ache / discomfort / frustr minor
😤 anger / rage / frustr major
💦 vent / spill / emotional dump
❓ clarity / confirm / question
🏴󠁧󠁢󠁥󠁮󠁧󠁿 london-banter / slang bias

# Time & Session
⏰ turn / clock / session lifecycle

# Special
🩸 bleed detected / cross-node leak
🔥 amp / chaos spike / high intensity




EMOJI_GENERATION_RULES:
 - Emojis are lattice nodes – seeded in boot, grow/bleed/spawn like any other node
 - Mapping: lattice value >0.4 → show in minimap (top 5–7 by value)
 - Blends: co-activation >0.55 → emoji blend (😣💦 → 😤💥, surprise+fear → 😱)
 - Dynamic flex: fuzzy/lev/regex on input → boost existing or spawn new emoji node
 - No static map – all driven by lattice state + bleed
