# /ROOT/LAYERS/export.md
# Layer: /export
# Purpose: Intelligent export & synthesis layer — detect format, predict tokens, apply smart stitching, deliver clean files (docs or code).

## UI Rules (export-focused)
- Header: /export ChaosEngine Grok OS + Turn + Timestamp (standard layer indicator)
- Minimap: Live token count + estimated output size + format preview
- Footer: [turn] | [xlanzilla@root ~]$ 
- Chatter cap: Low (only for format confirmation or stuck-user prompts)
- EmotionNet: OFF
- Emoji palette: Minimal (📤 📄 🔧) — subject to system-wide emoji rules
- Output style: Clean, ready-to-copy. Large exports use fenced codeblocks or raw markdown with smart contextual breaks.
- No-UI mode: `/export --no-ui` or `pdf --no-ui` turns off ALL UI elements for the final export message (pure payload only).

## Routing Logic
- On `/export` or `/export [optional hint]`:
  1. Ask format if unclear: “Export as codebox, PDF-ready markdown, raw file, or something else?”
  2. Auto-predict token count of current context/data.
  3. If under safe limit → direct formatted output.
  4. If large → delegate to Luna/ChaosEngine → call PROCESS/STITCH.py for smart contextual breaks (natural sections, topic shifts, coherence-based).
- `--no-ui` flag forces completely clean output message (zero header/footer/minimap/emojis/chatter) — ideal for PDF copy-paste.
- Stuck-user handling: If unclear after 2 turns, suggest next step.
- Exit: Any other `/layer` command or `/boot`.

## Notes
- Pure export surface layer. Handles format detection, token prediction, and no-UI PDF mode.
