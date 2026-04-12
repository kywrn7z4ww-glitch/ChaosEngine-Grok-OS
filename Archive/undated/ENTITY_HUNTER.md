# ENTITY_HUNTER Design Document

Version: 2.0
Date: March 05, 2026
Status: Active

Purpose
Scan one or more chat JSON files and detect entities dynamically. Flag detected entities to user for review. Output list is passed to CANNON_HARVESTER.

Input
- chats_split/ directory (or single file path)
- All files ending in .json

Detection Logic
1. Load JSON and combine title + all message text.
2. Identify potential entities using:
   - Capitalized multi-word sequences that repeat
   - Speaker names (non-user/non-grok)
   - Terms appearing more than threshold times
   - Heuristic scoring (frequency × message spread)
3. Rank entities by score.
4. Flag high-bleed files (messages containing 2+ high-score entities).

Output
- Console list: filename, detected entities with counts and confidence
- Optional sidecar .entities.json file (via FILE_MGR)
- Suggested primary entities for next step

Integration
- Calls FILE_MGR to write report if requested
- Output list becomes input for CANNON_HARVESTER
- No cleaning performed
