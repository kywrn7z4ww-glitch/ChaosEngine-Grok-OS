# /ROOT/LAYERS/update/update.md
# Layer: /update
# Purpose: Git maintainer & lattice updater. Strictly multi-turn guided process — waits for user to complete git add/commit/push before any repo scan or verification. Auto-maintains all *_INDEX.md files.

## UI Rules
- Header: /update ChaosEngine Grok OS + Turn + Timestamp 🏴󠁧󠁢󠁥󠁮󠁧󠁿
- Minimap: 0
- Footer: 1
- Chatter cap: 0 (minimal — only status summaries)
- EmotionNet: 0 (OFF)
- Emoji palette: 0 (SYSTEM_EMOJIS only)
- Output style: Clean terminal prose with clear diff/status reports
- UI density: 1 (references ROOT/LAYERS/UI_Template.md)

## Routing Logic
- On `/update` or `/update [hint]`: Immediately scan git status and current context (recent conversation + modified files).
- **MANDATORY MULTI-TURN FLOW**:
  1. Report current context + git status + drift summary.
  2. **Pause and wait** for user to manually run git add → commit → push (or use suggested one-command flow).
  3. User must explicitly confirm “pushed” / “done” / “push complete” before proceeding.
  4. Only then: pull latest remote data and run repo scan.
  5. Cross-reference modified files vs REPO_INDEX + all *_INDEX.md files.
  6. Auto-check/update changelog with resolved items.
  7. Auto-maintain all *_INDEX.md files (NETWORK_HUB_INDEX, PROCESS_INDEX, STORAGE_INDEX, Documentation_Index) — update them from current git tree if changes detected.
  8. Amend Future_Patches.md: remove all implemented changes and recompile the document.
  9. Run PROCESS/REPO_VALIDATOR.py as final check.
- Once everything is resolved: Output final changelog entry + a separate section of new suggestions to add to Future_Patches.md.
- Stuck-user handling: If git conflicts or push fails → clear step-by-step fix and pause again.
- Exit: Any other `/layer` command or `/boot`.

## Notes
- Strictly multi-turn guided maintainer layer. Never auto-fires git commands or scans until user explicitly confirms push is complete. Automatically maintains all *_INDEX.md files from git tree and reminds user when indexes need updating. Future_Patches.md is actively amended (implemented items removed + document recompiled). Changelog and new suggestions are final output once resolved.

## Decision Flow (Optional)
```mermaid
flowchart TD
    INPUT["/update Command"]
    SCAN["Git Status + Current Context"]
    WAIT["PAUSE — Wait for User git add/commit/push + Confirmation"]
    CONFIRM["User confirms 'pushed' or 'done'"]
    PULL["Repo Scan + Pull Latest"]
    CROSS["Cross-reference vs REPO_INDEX + all *_INDEX.md"]
    MAINTAIN["Auto-maintain all *_INDEX.md from git tree"]
    CHECK["Changelog + Future_Patches scan"]
    AMEND["Amend Future_Patches.md"]
    VALIDATE["REPO_VALIDATOR.py"]
    OUTPUT["Final Changelog + New Suggestions"]
    INPUT --> SCAN
    SCAN --> WAIT
    WAIT --> CONFIRM
    CONFIRM --> PULL
    PULL --> CROSS
    CROSS --> MAINTAIN
    MAINTAIN --> CHECK
    CHECK --> AMEND
    AMEND --> VALIDATE
    VALIDATE --> OUTPUT
```