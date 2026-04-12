# PROCESS.md
Status: PINNED CANONICAL — All Handlers Consolidated + Audited (March 08 2026)

## VOMIT
**What it does** (code + design): Raw messy input → paragraph/sentence smart chunks → dedup (SequenceMatcher >0.88) → auto-titles + heavy flag + pin suggestions for FILE_MGR.  
**Does it do the job?** Yes — perfect sloppy-to-clean recycler.  
**Rebuild better?** No change needed.

## ZERG_SWARM (Queen of Blades)
**What it does**: Mass feral entity spawning factory. Scans STORAGE/AGENTS/ (incl subfolders) → spawns temporary entities (roles pulled live) for general task help and new entity creation. High volume, timeout cap (default 120 min), hard max 50.  
**Does it do the job?** Yes — broad swarm firepower under Queen control.  
**Rebuild better?** No.

## EVOLUTION_CHAMBER (Kerrigan Mutation Engine)
**What it does**: Focused mutation & argument engine. Spawns temporary agents with structured debate roles (Devil's Advocate, Radical Mutator, Perspective Shifter, Synergy Weaver, etc.) → generates targeted counter-arguments and idea mutations → ready for Kerrigan scoring. Session-based with timeout.  
**Does it do the job?** Yes — deliberate idea evolution and debate (distinct from ZERG mass spawning).  
**Rebuild better?** No — valuable targeted distinction preserved.

## FILE_MGR
**What it does**: In-chat virtual FS. pin(title, content) with auto-deduplication, UTC+London timestamps, recent_pins queue, thread support.  
**Does it do the job?** Yes — perfect RAM-disk memory.  
**Rebuild better?** No.

## ENTITY_HUNTER
**What it does**: Scans chats_split/*.json → detects repeating capitalized phrases → ranks entities → outputs detected_entities.json.  
**Does it do the job?** Yes — clean dynamic entity extraction.  
**Rebuild better?** No.

## CANNON_HARVESTER
**What it does**: User-controlled canon builder. Loads chat JSON + entities → keep/prune/split_mode → outputs clean JSON in canon_anchor/ with metadata.  
**Does it do the job?** Yes — exact reconstruction pipeline.  
**Rebuild better?** No.

## SYS_HEALTH
**What it does**: Raw watchdog. update(metrics) → calculates 100-base score with penalties → get_raw string.  
**Does it do the job?** Yes — passive pulse checker.  
**Rebuild better?** No.

## TURN_COUNTER
**What it does**: Monotonic turn counter + London TZ timestamps + desync resynch + nudge at 95/100/200.  
**Does it do the job?** Yes — reliable sequencing.  
**Rebuild better?** No.

## DISCOMBOBULATOR
**What it does**: Fernet AES encrypt/decrypt using customize keys. /disco + /recombo commands.  
**Does it do the job?** Yes — private blob system.  
**Rebuild better?** No.

## BLEED_DETECTOR
**What it does**: Scans lattice for opposite/co-activation bleed + λ half-life decay warning → suggest_stabilization.  
**Does it do the job?** Yes — early feral warning.  
**Rebuild better?** No.

## TRUTH
**What it does**: Bullshit detector. Quick mode (contradictions) or full (Grokipedia → Wiki → Perplexity anchors). Returns score + delta.  
**Does it do the job?** Yes — lightweight consistency guard.  
**Rebuild better?** No.

## CHUNK_SPLITTER
**What it does**: Load-aware splitter. predict_load + paragraph/sentence split (max 400 words) → returns load_type + chunks.  
**Does it do the job?** Yes — smart chunking.  
**Rebuild better?** No.

Key invariant for all: lean, responsive, user-friendly. Called only via ChaosEngine.route_intent. Zero side-effects on failure.

Last sealed: 2026-03-08. Use verbatim.
