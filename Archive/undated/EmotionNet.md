# EmotionNet.md

## Purpose
Dynamic emotional neural simulation layer.  
Detects, blends, propagates and decays affective states from text input and swarm activity.  
Drives tone, emoji minimap, agent routing decisions and self-awareness feedback.

## How it works

### Core model
- Graph (nx.Graph) with nodes = emotion concepts / blends
- Each node has:
  - 3D PAD vector (Pleasure, Arousal, Dominance) + optional spectral extensions
  - Activation value (0.0–1.0)
  - Inactive counter (pruned after threshold)
- Opposites repel (negative edge weight)
- Co-activation > 0.45 → blend node creation

### Input processing
- `process_text_input(text)`  
  - Fuzzy keyword match in current node names  
  - Weighted average of matching vectors  
  - If co-activation high → spawn blend node (e.g. "lust-disgust")  
  - Fallback: spawn near strongest current emotion

### Update cycle (`tidal()`)
1. `force_update()` — layout forces (spectral → spring → Fruchterman → Kamada → custom linlog)  
   → repositions vectors in 3D space while preserving PAD core
2. `gnn_pass()` — message passing with damping  
   → spreads activation through graph edges
3. Tidal prune  
   → decay low activations  
   → remove inactive nodes after threshold

### Output / feedback
- `top_nodes(n=7, min_val=0.3)` → returns strongest active emotions  
  → feeds minimap emoji selection & tone modulation

### Key parameters
- dim = 3 (PAD base)  
- max_nodes = 150 (hard cap)  
- damping = 0.92 (activation persistence)  
- co_act_thresh = 0.45 (blend trigger)  
- inactive_max = 8 (prune after turns)

### Modularity points
- `seed_theories()` can be overridden / extended with new emotion seeds  
- Vector dimension extensible (spectral projection adds higher dims)  
- Force layout stack swappable (add/remove algorithms)  
- Prune logic injectable (custom criteria)  
- Input processor pluggable (e.g. LLM embedding instead of fuzzy match)

### Anchor compliance check (HIVE_PHILOSOPHY v1.3)
- **Lean** — graph stays small, only active nodes survive  
- **Responsive** — tidal cycle fast, top nodes immediate  
- **User-Friendly** — input is raw text, no formatting required  
- **Sloppy-to-Sharp** — fuzzy matching + blend spawning handles messy input  
- **Self-Improvement Cycle** — expand (new blends), experiment (tidal steps), condense (prune), refine (vector reposition)  
- **Future-First Modularity** — dimension, seeds, layout stack, prune rules all hookable; adding new theory only appends to seeds

Last reviewed against HIVE_PHILOSOPHY v1.3: 2026-02-27
