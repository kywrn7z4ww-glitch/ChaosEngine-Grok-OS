## PROCESS_BLOB – Tight Intent Handlers
# Last in boot sequence. Isolated from OS shell & CE core.
# Purpose: High-level intent routing & action handlers
# Injected into CE sim after OS wake-up & CE stub boot

Real Python implementations live in /python/python-process-lib/

PROCESS_HANDLERS:

  🤮 VOMIT – parse dump, chunk, dedup, clean, feed FILE_MGR  
  ✂ CHUNK_SPLIT / LOAD_PREDICTOR – load-aware split, predict heavy/light  
  ⛓️ CHAOS_MGR – intent hub, route estimate, tool-call decider  
  🧠 TRUTH_CHECK – reflect, contradict detect, fact nudge  
  📦 FILE_MGR – pin/update, projects, titles, paths, complete/archive  
  ⚙️ SYS_MGR – session health, fault/bleed/loop detect, maintenance nudge  
  ⚙️💗 SYS_HEALTH – raw metrics & score (decay, nodes, storage, emotion, loops, bleed)

Legacy / minimal (keep or migrate to Python later):
  - PROCESS_DISPLAY
  - TURN_HARDEN
  - CLARITY_RULE❓
  - REFLECT_RULE🔄
  - BLOB_ACCESS
  - NO_FRICTION

INJECTION_SEQUENCE:
  1. OS boots UI/commands/storage/parallel
  2. CE BootStub loads core + hooks
  3. PROCESS_BLOB injected last
  4. Wake-up complete: full flex live
