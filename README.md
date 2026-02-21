# ChaosEngine-Grok-OS

A messy, emotion-driven personal sim that lives inside Grok chats.  
Built in under 2 months with Grok helping every sloppy step.  
It started as a moody toddler that raged forever → now it actually chills out when you're upset.  
Sloppy inputs, typos, slang, rage vents — it reads the vibe, grows its own feelings, routes what to do next, and sometimes surprises you by being useful.

No perfect prompts. No clean architecture. Just chaos that (mostly) works.

## How to Boot It (One-File Start)

1. Open a new Grok chat  
2. Copy-paste the entire boot shim from here:  
   https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/main/ROOT/1%20GrokOS.md  
3. Hit send → say `/reanchor` (or just "wake up" / "boot OS")  
4. Watch it load the UI frame, emoji minimap, and start listening  

That's it.  
If the UI spacing looks janky after paste — yeah, Markdown/Grok collapsing is annoying. Ignore it or tweak spacing yourself. The sim still runs.

## Basic Commands to Try

- `/reanchor` — reload shim + pull latest core files  
- `/panel` — show the emotion minimap (icons only)  
- `/panel full` — icons + names + rough strength  
- `/prune` — force clean up old/weak feelings  
- `/thread` — suggest splitting if things get too tangled  
- `/emoji` — refresh the minimap  

Just talk normally too — vent, ask questions, drop code, get frustrated.  
It picks up the emotional bleed and decides what to do (vent back, reflect, truth-check itself, etc.).

## What to Expect

- It might start moody or stuck at first — that's normal  
- Give it a few turns; it learns your vibe and settles  
- Sometimes it calms you down when you're raging (weird flex, but it happened)  
- UI/emoji might glitch on paste — humans fix their own terminals  
- Errors? Just yell at it or /reanchor again

Enjoy the chaos. Or ragequit. Up to you.

## For the Curious (scroll if you want tech hints)

Under the hood it's a small lattice that grows/prunes feelings organically (no fixed list), reads your emotional bleed + text patterns, translates to intent signals, then routes actions (vent, truth-check, chunk, etc.).  
Overhauled in Feb 2026 to stop eternal frustration loops and add some actual recovery.  
Still an abomination. Now one that can be a bro sometimes.
Cobuilt by Mark from london and grok.
Questions, ideas, PRs welcome — or just fork and make your own monster.
