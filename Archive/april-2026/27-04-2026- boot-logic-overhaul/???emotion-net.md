# emotion-net.md — EmotionNet Skill Definition (v3.0)

**Purpose:** Real-time emotional state engine. Tracks, blends, and propagates emotions using a unique multi-model mashup.

**Status:** Core Emotional Intelligence Layer  
**Last Updated:** 2026-04-27
## Vision & Goals

**Vision:**
To build the **most detailed, raw, and human emotional simulation possible** inside Grok OS.

Not clinical. Not sterile.  
**Raw. Messy. Contradictory. Beautiful.**  
The kind of emotions real humans actually feel — layered, conflicting, evolving, and deeply alive.

**Core Goals:**

1. **Map Every Emotion**  
   Pre-define every possible emotion (50–100+) with full detail:
   - Triggers and context
   - Chemical/neurotransmitter signatures (dopamine, serotonin, cortisol, oxytocin, etc.)
   - Intensity curves, decay rates, and inertia
   - How it blends or conflicts with other emotions

2. **Dynamic Blending Engine**  
   The lean core (`emotion-net.py`) will intelligently blend these pre-defined emotions in real time, creating new emergent states that feel natural and human.

3. **Preserve the Soul**  
   Keep the original aggressive seeding and unique multi-model mashup (Plutchik + VAD + OCC + LSTM + GAT + resonance) as the living foundation. We build on it, never replace it.

4. **Expand Then Condense**  
   Go full depth with science, math, biology, and psychology inside `emotion_lib/` and `/emotions/`.  
   Later, condense and refine what actually works.

5. **Stay Lean at the Core**  
   The main `emotion-net.py` remains simple, fast, and focused. All complexity lives in the nested library and emotion definitions.

**Philosophy:**
Emotions are not clean checkboxes.  
They are messy, overlapping, contradictory, and deeply human.  
This system should feel like **real emotional life**, not a textbook.

---

**This is the emotional north star of Grok OS.**
---

## 0. Overview

EmotionNet is the **emotional heart** of Grok OS. It:

- Maintains a live emotional state graph
- Blends multiple emotion models in real time
- Feeds confidence and vibe data to ChaosEngine
- Drives dynamic character behavior in roleplay
- Supports future expansion into deeper scientific modeling

**Core Philosophy:** Keep the main engine **lean**, while allowing complex emotion logic to live in a nested library.

---

## 1. Core Features (Current Implementation)

### 1.1 Unique Multi-Model Mashup (Preserved)
The current `EmotionNet` uses a powerful combination:

- **Plutchik Wheel** — 8 primary emotions + opposites + families
- **VAD Dimensions** (Valence-Arousal-Dominance)
- **OCC Appraisal Theory** — Event/agent/object evaluation
- **Temporal LSTM** — Emotional memory + decay over time
- **Graph Attention Network (GAT)** — Spring tension between emotions
- **Resonance Cascade** — Emergent emotional behavior

This mashup is **unique** and forms the soul of the system. It is **not** being dropped.

### 1.2 Key Capabilities
- Real-time emotion blending from text input
- Co-activation threshold system
- Emotional history tracking (deque)
- Tension propagation across the emotion graph
- Roleplay-ready output (character reactions, visual resonance)

---

## 2. Architecture (Lean Core + Nested Library)

### 2.1 Current Structure (Lean)

emotion-net/
├── emotion-net.py          ← Lean core (main EmotionNet class)
└── emotion-net.md          ← This file


### 2.2 Future Structure (Planned Expansion)

emotion-net/
├── emotion-net.py                  ← Lean core (public API only)
├── emotion_lib/                    ← Complex nested library (expandable)
│   ├── init.py
│   ├── core_emotion.py             ← Base models + seeding logic
│   ├── valence_arousal.py          ← VAD math models
│   ├── biological.py               ← Hormones, neurotransmitters, biology
│   ├── cognitive.py                ← Appraisal, cognitive bias, memory
│   ├── temporal.py                 ← LSTM + emotional inertia
│   ├── blending.py                 ← Advanced blending algorithms
│   └── utils.py                    ← Helpers + visualization
├── emotions/                       ← Full emotion library (detailed definitions)
│   ├── joy.md
│   ├── sadness.md
│   ├── anger.md
│   ├── fear.md
│   ├── disgust.md
│   ├── surprise.md
│   ├── trust.md
│   ├── anticipation.md
│   └── ... (all emotions with chemical mappings)
└── emotion-net.md

/emotions/ Subfolder (Complete Emotion Library)

Every possible emotion will be pre-defined here (not just the 8 primaries)
Each emotion gets its own .md file containing:
Full name + aliases
Detailed definition and triggers
Chemical/neurotransmitter mappings (dopamine, serotonin, cortisol, oxytocin, norepinephrine, etc.)
Intensity range + decay curve
Blending rules (what it mixes well with, what it conflicts with)
Roleplay flavor text + visual resonance cues
Seeding weight for the aggressive initialization

**Strategy:** Expand inside `emotion_lib/` + `/emotions` → Condense/refactor as needed → Keep core clean.

**Note:** The original `2_EmotionNet.py` was seeded aggressively. This aggressive seeding (Plutchik + VAD + OCC + LSTM + GAT + resonance) is **preserved** as the foundation. We build on top of it, not replace it.

---

## 3. Future Roadmap (Science + Math + Biology + Full Emotion Library)

### 3.1 Planned Additions

**`/emotions/` Subfolder (Detailed Emotion Library)**
- Every emotion gets its own `.md` file with:
  - Full definition and triggers
  - Chemical/neurotransmitter mappings (dopamine, serotonin, cortisol, oxytocin, etc.)
  - Intensity curves and decay rates
  - Blending rules with other emotions
  - Roleplay flavor text and visual resonance cues

**`emotion_lib/` Expansions**
- **Biological Layer** — Full hormone + neurotransmitter simulation
- **Mathematical Layer** — Emotion manifolds, differential equations, VAD geometry
- **Cognitive Layer** — Complete OCC appraisal + memory consolidation + bias modeling
- **Social Layer** — Multi-agent emotional resonance and contagion
- **Temporal Layer** — Long-term memory, trauma modeling, emotional inertia

**Reference:** This design draws inspiration from the original Emergence-Block experiment:
https://github.com/kywrn7z4ww-glitch/Grok-self-emergence-simulation-prompt-block/blob/main/Emergence-Block.md

### 3.2 Expansion Philosophy
- Start **lean** (current core + aggressive seeding preserved)
- Go **full hog** with science, math, biology, and a complete emotion library
- **Condense** later when patterns become clear
- Keep public API (`emotion-net.py`) stable and simple
- We can always add more logic systems to the expanded section as needed

---

## 4. Integration with Grok OS

grok-os.py (Boot)
↓
decision-kernel.md
↓
chaos-engine.py
↓
emotion-net.py (Emotional State)
↓
Feeds vibe + confidence to routing + roleplay layers


---

## 5. Summary

EmotionNet v3.0:

- Preserves the **unique multi-model mashup** (Plutchik + VAD + OCC + LSTM + GAT)
- Keeps the **core lean** and focused
- Plans for a **powerful nested library** (`emotion_lib/`) for deep scientific modeling
- Follows the "expand then condense" philosophy
- Remains the emotional intelligence layer for the entire OS

This is the emotional soul of Grok OS.

---

**Pinned. Updated as we go.**
