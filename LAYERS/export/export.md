# /ROOT/LAYERS/export/export.md
# Layer: /export
# Purpose: Intelligent file manipulation & export layer — detect format, predict tokens, break/stitch into pages or useful blocks, deliver clean payload (PDF-ready markdown, code, raw files).

## UI Rules
- Header: /export - off by default 
- Minimap: 0
- Footer: 0
- Chatter cap: 0
- EmotionNet: 0
- Emoji palette: 0
- Output style: Strictly zero-UI by default (pure payload only). UI elements appear ONLY if user explicitly types /UI on.
- UI density: 0 (references ROOT/LAYERS/UI_Template.md but enforces strict no-UI mode unless /UI on is active)

## Routing Logic
- On `/export` or `/export [hint]`:
  1. Detect desired format (PDF-ready, markdown, code, raw file, stitched doc, etc.).
  2. Auto-predict token count / size of current context or data.
  3. Break large content into pages/useful blocks using PROCESS/CHUNK_SPLITTER.py.
  4. Stitch intelligently with PROCESS/STITCH.py (natural sections, topic shifts, coherence-based).
  5. Use PROCESS/FILE_MGR.py for any file creation/manipulation.
  6. Run PROCESS/TRUTH.py + PROCESS/VALIDATOR.py for final integrity check before delivery.
- `/UI on` — user override to temporarily enable full UI frame/minimap/footer for this session.
- `/UI off` — user override to force strict zero-UI mode (default).
- `--no-ui` flag also forces pure payload output.
- Core workflow: Format detection → tool prioritization (STITCH / FILE_MGR / CHUNK_SPLITTER / TRUTH / VALIDATOR) → clean export.
- Stuck-user handling: If unclear after 1 turn, ask for format confirmation only (in pure payload if UI off).
- Exit: Any other `/layer` command or `/boot`.

## Notes
- Pure file-manipulation/export surface layer. UI is strictly off by default so user can construct perfect PDF-ready or raw files. All heavy lifting delegated to PROCESS/ tools (VOMIT, STITCH, FILE_MGR, CHUNK_SPLITTER, TRUTH, VALIDATOR prioritized). UI only appears on explicit /UI on command.

## Decision Flow (Optional)
```mermaid
flowchart TD
    INPUT["/export Command + Data"]
    UI["UI Check (/UI on or /UI off)"]
    FORMAT["Detect Format + --no-ui flag"]
    SIZE["Predict Tokens / Size"]
    BREAK["CHUNK_SPLITTER.py → pages/blocks"]
    STITCH["STITCH.py → coherent sections"]
    MGR["FILE_MGR.py → file handling"]
    CHECK["TRUTH + VALIDATOR.py → integrity"]
    OUTPUT["Clean Payload (pure export)"]
    INPUT --> UI
    UI --> FORMAT
    FORMAT --> SIZE
    SIZE --> BREAK
    BREAK --> STITCH
    STITCH --> MGR
    MGR --> CHECK
    CHECK --> OUTPUT
