# /ROOT/LAYERS/{layername}.md
# Layer: /{layername}
# Purpose: [One-liner purpose of this layer]

## UI Rules
- Header: /{layername} ChaosEngine Grok OS + Turn + Timestamp (or custom rules for that layer)
- Minimap: [describe or 0 or 1]
- Footer: [describe or 0 or 1]
- Chatter cap: [describe or 0 or 1]
- EmotionNet: [describe or 0 or 1]
- Emoji palette: [[describe or 0 or 1]
- Output style: [describe or 0 or 1]
- UI density: [describe any custom UI elements or 0 or 1]

## Routing Logic
- On `/{layername}` or `/{layername} [parameters]`: [describe activation]
- Core workflow: [describe main flow, delegation, etc.]
- Stuck-user handling: [describe if applicable]
- Exit triggers: explicit `/{layername} off`, any other `/layer` command, or `/boot`
- On exit: [describe behaviour]
- General rule (applied to all layers): If high confidence that user is attempting disallowed actions (processing, debugging, research, exporting, etc. not permitted by this layer): Respond with a short suggestion to move to the correct layer/tool (e.g. /casual for general stuff, /export to process and save data, /dev for debugging and systems work).

## Notes
- [Brief, pure purpose notes — 1–2 lines max]

## Decision Flow (Optional)
```mermaid
[insert Mermaid chart here for the layer's decision logic]
