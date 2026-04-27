# emotion-net.md — EmotionNet (Current Lean Version)

**Purpose:** Real-time emotional state engine for Grok OS.

**Version:** v3.0 (Lean Core)  
**Last Updated:** 2026-04-27

---

## What It Is

EmotionNet is the **emotional intelligence layer** of Grok OS. It tracks, blends, and propagates emotions in real time using a unique combination of:

- Plutchik Wheel
- VAD Dimensions
- OCC Appraisal
- Temporal LSTM
- Graph Attention + Spring Tension
- Resonance behavior

It feeds emotional state (vibe + confidence) to ChaosEngine and roleplay layers.

---

## Current Features (Lean Core)

- Real-time emotion detection from text
- Dynamic emotion blending
- Emotional history tracking
- Tension propagation
- Roleplay-ready output (character reactions, visual resonance)
- ≥99% confidence integration with ChaosEngine

---

## How to Install

1. Copy `emotion-net.py` into your `ROOT/emotion-net/` folder
2. Make sure `chaos-engine.py` can find it (it auto-loads on boot)
3. No extra dependencies needed beyond what's already in the environment

**Quick Test:**
```bash
python emotion-net.py

grok-os.py (Boot Shim)
        ↓
decision-kernel.md
        ↓
chaos-engine.py (loads EmotionNet automatically)
        ↓
emotion-net.py (provides emotional state)
        ↓
Used by: roleplay layers, confidence scoring, character behavior

Key Connections:

ChaosEngine calls it on every intent route
Roleplay layers use get_roleplay_emotion() and get_character_reaction()
Decision Kernel uses emotional state for confidence and vibe

Basic Usage

from emotion_net import EmotionNet

net = EmotionNet()

# Process user input
net.process_text_input("I feel so frustrated with this bug")

# Get current emotional state
print(net.get_roleplay_emotion("gentle", "I feel happy today"))

# Get character reaction
reaction = net.get_character_reaction("angry", "You broke my heart")
