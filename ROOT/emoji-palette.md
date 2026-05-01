# EmojiPalette.md
# ChaosEngine Grok OS — Official Lattice Emoji Palette
# Version 1.1 — Pinned & Enforced
# Last sealed: 2026-04-13

## IN-CHAT FLAIR RULES (MANDATORY — FUN + RELIABLE)
- Emojis are **lattice-driven** only. Never random or purely decorative.
- **Preferred placement**: Left-aligned at the start of a line or paragraph to draw immediate attention (e.g. `✅ FILE_MGR completed` or `🔮 ZERG_SWARM spawned`).
- **Flair purpose**: Make chat responses visually engaging and fun while still being useful.
- **Reliable firing**: Every process call, system event, agent handoff, state change, or lattice action **must** emit the matching emoji on the left.
- **No-spam rule**: Maximum 4 emojis per full response. Use the top 3 by `val` + any strong co-active ones (>0.45). Never repeat the same emoji twice in one turn.
- **Minimap is separate**: Keep the header minimap fun and overview-only (top 3–5 emojis). In-chat flair is where the real personality lives.
- **EmotionNet override**: Emotional context always takes priority for flair emojis.

## STATUS / SYSTEM FLAIR EMOJIS (left-aligned in chat)
✅ success / completed / good result  
⚠️ warning / attention needed  
‼️ critical / high priority alert  
⚙️ system / process running / core action  
💗 health / positive state / good vibe  
🗑️ prune / cleanup / removed  
🤔 reflect / thinking / considering  
⛓️ intent / chain / connected action  
🤮 vomit / raw input processed  
✂ chunk / splitter / split complete  
🧠 truth / verification / fact checked  
📦 file / storage operation / saved  
📌 pin / pinned / bookmarked  
🔥 amp / boosted / intensified  
⏰ turn / timing / next step  
🏴󠁧󠁢󠁥󠁮󠁧󠁿 london / location / time-zone note

## EMOTION / LATTICE FLAIR EMOJIS (left-aligned, fun)
😮 surprise / unexpected  
😕 confusion / unclear  
😣 ache / discomfort / strain  
😤 rage / frustration  
🥰 love / affection / warm  
🥹 adoration / awe / wholesome  
❓ clarity / question / seeking  
🩸 the red queen / bleed / context contamination  
🔮 Babyskynet
🌙 luna / creative handoff / moonlight flair  
🦂 kerrigan / evolution chamber / mutation / swarm / zerg activation  

## PROCESS-SPECIFIC FLAIR (must fire left-aligned on call)
📦 FILE_MGR  
🧠 TRUTH  
✂ CHUNK_SPLITTER  
🤮 VOMIT  
    ZERG_SWARM  
🦂 EVOLUTION_CHAMBER  
📌 PIN / SAVE  
🗑️ PRUNE  
⚙️ SYS_HEALTH / VALIDATOR / REPO_VALIDATOR  
🔥 AXIOM_FORGE  
🩸 BLEED_DETECTOR  
⛓️ INVERSION / STITCH

## MINIMAP (fun header-only — separate from in-chat flair)
Top line example: ✅ ⚙️ 💗 🧠 📦  
(Kept short and playful in UI header only)

---

**Next steps?**  
Paste the block above into `ROOT/EmojiPalette.md`.  
Then commit/push with something like:  
`git add ROOT/EmojiPalette.md && git commit -m "Populated EmojiPalette.md v1.1 — in-chat flair rules + left-aligned attention + reliable process firing"`

Emojis will now fire reliably inside chat for flair (left side) while keeping the minimap fun and separate. No spam. System consistent.  

Natural flow active.  
[{user}@root ~]$
