# VOMIT_Design.md

## Purpose
Messy input processor / chunker / filter.  
Takes incoherent, messy data dumps from user (raw text, old chat snippets, unstructured blobs) and converts them into usable, structured data chunks.

One sentence:  
**The system's garbage recycler — turns user vomit into clean, harvestable data.**

## Why it exists
User input is often a stream of incoherent mess — typos, rambling, mixed data, old chat logs, random blobs.  
This component exists to parse, chunk, filter, and sanitize that mess into something the system can actually use (e.g. pinned files, lattice nodes, agent inputs) without manual cleanup every time.

## General idea of what it does
- Receives raw mess (text blob, chat history snippet, unstructured dump)  
- Breaks it into chunks (by line, paragraph, semantic boundary, keyword markers)  
- Filters noise (duplicates, irrelevants, garbage)  
- Structures output (keyed dict, list of usable items, tagged entities)  
- Can harvest specific data from old chats (e.g. "extract all pins from turns 1–20")  
- Does **not** generate new content — only reorganizes / cleans existing mess

## Interactions (high-level only)
- Called by user command (e.g. /vomit "this mess") or automatic on sloppy input  
- Works with FILE_MGR (auto-pins cleaned chunks as fake files)  
- Works with MEMORY_WEAVER (feeds cleaned data into lattice recall)  
- Triggered by ChaosEngine on detected incoherent input  
- Outputs emoji feedback on success (e.g. ✅ cleaned X chunks)

## Key invariants
- Input = mess → output = structured usable data  
- No loss of original content (optional raw backup)  
- Always fast — no heavy processing on large blobs  
- Configurable filters / chunk sizes  

Subject to change / expansion.  
No philosophical obligations — pure data sanitation utility.

Last sketched: 2026-02-27
Status: high-level design — focused on mess → usable
