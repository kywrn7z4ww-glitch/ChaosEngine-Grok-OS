# CANNON_HARVESTER – Chat Harvest & Sift Tool

## Philosophy
Harvest full chat threads, chunk if big, sift mixed content (stories, projects, personal notes, smut RP)  
Preserve 100% fidelity for reconstruction (timelines, char arcs, shared canon)  
Resolve contradictions / chaos with fuzzy merge + flags  
Standalone but can pipe CHUNK_SPLITTER for auto-split, FILE_MGR for dumps, DISCOMBOBULATER for encrypt  

## Setup
- No keys needed – optional encrypt via DISCOMBOBULATER keys in customize  
- Run in Grok: paste prototype code + raw chat chunk → /cannon  
- Offline: run .py locally with python (chunk size auto-check)  

## Commands (Grok-native)
- /cannon <chat_text> [mode=mixed] [encrypt=personal] → parsed chunks + timeline + arcs + conflicts  
- /cannon_dump <chat_text> → same + auto file dumps (json/md) + optional encrypt blobs  

## How to use in Grok (any window)
1. Copy chat chunk (~5k–10k chars)  
2. Paste into Grok + /cannon [pasted text] mode=mixed  
3. Grok spits structured json/md (full parsed, timeline, per-char arcs, conflicts)  
4. Copy outputs to repo files (DATA/thread/part001.json)  
5. Optional: encrypt outputs with /disco [json] category=personal  

## Rebuild full script (if needed)
Ask Grok: "give me CANNON_HARVESTER.py code"  
Grok spits full python – save locally  

## Security / Sanitization
- Outputs sanitized: types = story/project/personal/smut/other  
- No explicit terms – smut for spicy RP  
- Encrypt optional for blobs – pure noise without key  

## Fidelity Rules
- Never summarize/redact  
- Keep speaker tags, formatting, code blocks  
- Number turns relative to chunk  
- Flag conflicts (keyword mismatch or "contradiction") for manual resolve  
