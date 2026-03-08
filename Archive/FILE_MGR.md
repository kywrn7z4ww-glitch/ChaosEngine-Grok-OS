# FILE_MGR_Design.md

## Purpose
Virtual in-chat filesystem manager.  
Automatically creates, pins, updates, deduplicates and recalls "fake files" (text blobs, pinned content, thread memories) that live only inside the lattice/chat session.

One sentence:  
**The hive's RAM disk — tracks everything the user pins, calls, or works on without ever touching real disk.**

## Why it exists
Chat is stateless and forgetful.  
User drops blobs, pins ideas, references old turns, uploads concepts — all of it disappears the moment the session ends or context shifts.  
FILE_MGR gives persistent, searchable, auto-managed fake files inside the conversation so nothing gets lost and everything stays callable by title or thread.

## General idea of what it does
- User says "pin this code" or "pin that idea" → auto-saves as titled fake file with timestamp (UTC + London)  
- Detects near-duplicate content automatically and updates instead of creating duplicates  
- Organizes by thread (/user, /thread/main, custom threads)  
- Keeps recent pins queue for quick recall  
- Allows listing, searching, completing, archiving fake files  
- Returns clean feedback emoji + status every time something is pinned/called/updated  

No real files. No disk writes. Pure in-memory lattice storage that feels like a filesystem inside the chat.

## Interactions (loose)
- Receives pin/recall commands from user or other agents (via HIVE dispatch)  
- Stores content + metadata in shared lattice  
- Feeds MEMORY_WEAVER for cross-turn recall  
- Can be triggered by ChaosEngine on sloppy input ("remember that thing from earlier")  
- Outputs emoji feedback on every operation  

## Modularity notes
- Storage backend swappable (in-memory → vector store → external later)  
- Deduplication similarity threshold adjustable  
- Timestamp format / timezone configurable  
- Threading model extensible (add /project/X etc.)

Subject to complete change.  
No philosophy tie-in.  
Pure utility component for managing fake in-chat files.

Last sketched: 2026-02-27  
Status: high-level design — matches current implementation direction
