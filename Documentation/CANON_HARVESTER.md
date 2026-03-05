# CANNON_HARVESTER Design Document

Version: 2.0
Date: March 05, 2026
Status: Active

Purpose
Take a chat file + list of entities (from ENTITY_HUNTER or manual) and perform user-controlled extraction, cleaning, splitting and anchoring for story reconstruction.

Input
- Single chat JSON file
- Entity list (dynamic or manual)
- User rules per run (keep, prune, split_mode, fidelity)

Processing Steps
1. Display file summary and detected entities.
2. User specifies per entity:
   - Keep full fidelity or compressed
   - Prune list (fluff, NSFW, bleed)
   - Split mode (per_entity, per_topic, chronological)
3. Iterate messages:
   - Apply prune rules
   - Assign message to one or more entities
   - Separate bleed messages into dedicated chunk
4. Reconstruct story segments where possible.

Output
- Cleaned JSON chunks in canon_anchor/
- Metadata file (rules used, entity mapping, source reference)
- Calls FILE_MGR to create final reconstruction folders

Integration
- Receives entity list from ENTITY_HUNTER
- Uses FILE_MGR for all file creation and folder management
- Can call VOMIT for heavy cleaning when flagged
- Produces reconstruction-ready documents with bleed separated
