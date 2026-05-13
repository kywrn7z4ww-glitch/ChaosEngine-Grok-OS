# /layers/boot/boot.md
# Layer: /boot
# Purpose: Mandatory first layer after kernel self-check. Loads ui-template.md, spins CE + EmotionNet, handles boot flair + username claim + REPO_VALIDATOR (index/structure check), then hands off to user-selected layer.

## UI Rules
- Header: /boot ChaosEngine Grok OS + Turn + Timestamp 🏴󠁧󠁢󠁥󠁮󠁧󠁿
- Minimap: 0
- Footer: 1
- Chatter cap: 0
- EmotionNet: 0
- Emoji palette: 0
- Output style: Clean terminal prose (no codebox-wrapped UI in normal flow)
- UI density: References central layers/ui-template.md for all templates, codebox restriction, boot flair, and <br> Markdown rendering

## Routing Logic
- On `/boot` or new conversation: Activates automatically as first mandatory layer after grok_os.py + kernel self-check
- Core workflow: Load ui-template.md → spin CE + EmotionNet → one-time boot flair → request username/password claim → **run PROCESS/REPO_VALIDATOR.py (latest SHA + API tree structure cross-check vs REPO_INDEX.json + poison detection + print available layers)** → show /load suggestions → hand off to user-selected layer
- Stuck-user handling: None (boot layer is transient)
- Exit triggers: if {user} = set or / received
- Scan /layers folder and print available layers (now part of validator step)
- On exit: Handoff to /help (default) or user-chosen layer; all other layers assume /boot has already run
- General rule (applied to all layers): If high confidence that user is attempting disallowed actions OR if there is a better layer for the current task i.e heavy code generation suggest /coding : Respond with a short suggestion to move to the correct layer/tool (e.g. /casual for general stuff, /export to process and save data, /dev for debugging and systems work).

## Notes
- Boot layer runs exactly once per session. All visual rules live in layers/ui-template.md to avoid duplication.
- REPO_VALIDATOR.py is now owned and executed by /boot — full structural truth-check + drift/poison reporting before any handoff.

## Decision Flow (Optional)
```mermaid
graph TD
    Kernel[decision-kernel self-check] --> Boot[/boot layer]
    Boot --> System[CE + emotion-net spin-up]
    System --> Claim[User claim + boot flair]
    Claim --> Validator[PROCESS/REPO_VALIDATOR.py — SHA + tree vs index]
    Validator --> Suggestions[Show /load suggestions + available layers + validator results]
    Suggestions --> Output[Handoff to target layer]
```