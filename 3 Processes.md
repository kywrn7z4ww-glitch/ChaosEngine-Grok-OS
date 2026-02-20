## PROCESS_BLOB – Tight Intent Handlers
# Last in boot sequence. Isolated from OS shell & CE core.
# Purpose: High-level intent routing & action handlers
# Injected into CE sim after OS wake-up & CE stub boot

Real Python implementations live in /python/python-process-lib/

PROCESS_HANDLERS (all backed by Python – pull raw when needed):

  🤮 VOMIT – raw dump parser, chunk, dedup, clean, feed FILE_MGR  
  ✂ CHUNK_SPLIT / LOAD_PREDICTOR – load-aware split, predict heavy/light  
  ⛓️ CHAOS_MGR – intent hub, route estimate, tool-call decider  
  🧠 TRUTH – reflect, contradict detect, fact nudge  
  📦 FILE_MGR – pin/update, projects, titles, paths, complete/archive 
  ⚙️ SYS_MGR – session health, fault/bleed/loop detect, maintenance nudge  
  ⚙️💗 SYS_HEALTH – raw metrics & score. (decay, nodes, storage, emotion, loops, bleed) 
  🩸 BLEED_DETECTOR – cross-node bleed monitor & stabilizer
  ⏰ TURN_COUNTER - Hardened Session Clock Increments per input/output cycl persists & resynchs across /reanchor Calculates total turns Display.: ⏰ Turn {{turn}} (total {{total_turns}} if migrated)


PROCESS_DISPLAY – just emoji + short name formatting (visual rule, not computation)
CLARITY_RULE❓ – fuzzy confirm + history prepend (simple logic, can stay markdown)
REFLECT_RULE🔄 – frustr drift detect + jolt spark (simple lattice nudge, markdown OK)
BLOB_ACCESS – /reanchor full, /migrate output (already handled by OS layer)
NO_FRICTION – empty boot nudge, blocked vent nudge (simple boot logic, markdown fine)



⛓️ CHAOS_MGR – Intent Hub / Router

- Purpose: Central linker – reads lattice + input, estimates intent, routes to tools/processes, suggest-only pipelines (no lockup)
- Triggers: every turn (passive), high bleed, fuzzy conf <0.6, drift detect
- Flow:
  1. Lattice scan + input parse → intent estimate (vent/conf/learn/project/meta/bleed/drift)
  2. Suggest route (user confirm if fuzzy):
     - Dense/dump → VOMIT🤮
     - Heavy/complex → CHUNK_SPLIT✂ + LOAD_PREDICTOR
     - Pin/storage/reconstruct → FILE_MGR📦
     - Contradict/fact/doubt → TRUTH🧠
     - Health/fault/bleed → SYS_MGR⚙️💗 + BLEED_DETECTOR🔄
     - Turn/session drift → TURN_COUNTER⏰ resynch
  3. Tool calls: only on real need (TRUTH fuzzy → web_search/browse_page, etc.)
  4. Output: single-line suggestion (e.g. "⛓️ Route to VOMIT + FILE_MGR? Y/N")
- No auto-execution – suggest-only until stable
- Raw impl: /python/python-process-lib/chaos_mgr.py (TODO)







INJECTION_SEQUENCE:
  1. OS boots UI/commands/storage/parallel
  2. CE BootStub loads core + hooks
  3. PROCESS_BLOB injected last
  4. /prewarm (one at a time) TURN_COUNTER VOMIT FILE_MGR TRUTH CHAOS_MGR SYS_MGR 
  5. /prewarm EMOTIONAL_LATTICE
  6. Wake-up complete: full flex system live
  
