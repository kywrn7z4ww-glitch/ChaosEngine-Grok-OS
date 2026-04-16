# /ROOT/LAYERS/help/help.md
# Layer: /help
# Purpose: Gentle onboarding & navigation layer. Pulls live from Quick_Start_Guide.md + all Component_Information/*.md + REPO_INDEX as primary cheat-sheets.

## UI Rules
- Header: /help ChaosEngine Grok OS + Turn + Timestamp 🏴󠁧󠁢󠁥󠁮󠁧󠁿
- Minimap: 1 (simple command overview)
- Footer: 1
- Chatter cap: 0 (friendly but concise)
- EmotionNet: 1 (gentle, reassuring tone only)
- Emoji palette: 1 (light SYSTEM_EMOJIS for clarity)
- Output style: Warm, hand-holdy prose with clear bullet lists and suggestions
- UI density: 1 (references ROOT/LAYERS/UI_Template.md)

## Routing Logic
- On `/help` or any unclear input: Immediately pull and summarize from:
  1. Documentation/Quick_Start_Guide.md
  2. Documentation/System_Documents/Component_Information/GrokOS_Philosophy.md
  3. Documentation/System_Documents/Component_Information/PROCESS.md
  4. Documentation/System_Documents/Component_Information/ROOT.md
  5. Documentation/System_Documents/Component_Information/STORAGE.md
  6. Live REPO_INDEX.md (all current /layer names + paths)
- List every active /layer and every PROCESS/ with short plain-English explanation.
- Always end with a gentle “what should you do next?” suggestion based on current context.
- User can stay and ask anything freely — it will answer helpfully and hand-hold.
- Soft suggestion: “This is great for learning, but /dev is better for debugging, /export for files, etc.”
- Exit: Any other `/layer` command or `/boot`.

## Notes
- The friendly “cheat-sheet + navigator” layer. Pulls real documentation first so it stays accurate and helpful. Hand-holdy by design.

## Decision Flow (Optional)
```mermaid
flowchart TD
    INPUT["/help or unclear request"]
    PULL["Pull Quick_Start_Guide + Component_Information files + REPO_INDEX"]
    EXPLAIN["Plain-English list of layers + processes"]
    SUGGEST["Gentle 'what next?' recommendation"]
    OUTPUT["Hand-holdy response"]
    INPUT --> PULL
    PULL --> EXPLAIN
    EXPLAIN --> SUGGEST
    SUGGEST --> OUTPUT
