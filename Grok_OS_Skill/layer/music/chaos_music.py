#!/usr/bin/env python3
"""
chaos_music.py — Compiled Music Tools v1.0
All the weird experimental music tools we built during the overhaul.
Ready to import and continue working.

Sections:
- Resonance Theory
- Synth Functions
- Tracker Layering
- Utility Helpers
"""

import random

import numpy as np
from scipy.signal import butter, lfilter

# ============================================================
# SECTION 1: RESONANCE THEORY
# ============================================================

def sympathetic_resonance(
    frequency: float, tension: float = 1.0, damping: float = 0.85
) -> float:
    """
    Calculate sympathetic resonance response.
    frequency: base frequency in Hz
    tension: how tightly the system responds (0.5 - 2.0)
    damping: how fast the resonance dies (0.7 - 0.95)
    """
    response = np.sin(frequency * tension) * damping
    return max(0.0, min(1.0, response))

def harmonic_resonance(base_freq: float, harmonics: int = 5) -> list:
    """Generate harmonic series with resonance weights"""
    series = []
    for h in range(1, harmonics + 1):
        weight = 1.0 / h
        series.append(
            {"harmonic": h, "frequency": base_freq * h, "resonance_weight": weight}
        )
    return series


# ============================================================
# SECTION 2: SYNTH FUNCTIONS
# ============================================================

def sine_wave(freq: float, duration: float, sample_rate: int = 44100) -> np.ndarray:
    """Generate a simple sine wave"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * freq * t)

def saw_wave(freq: float, duration: float, sample_rate: int = 44100) -> np.ndarray:
    """Generate a sawtooth wave"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return 2 * (t * freq - np.floor(t * freq + 0.5))

def low_pass_filter(
    data: np.ndarray, cutoff: float, sample_rate: int = 44100, order: int = 5
) -> np.ndarray:
    """Simple low-pass filter"""
    nyq = 0.5 * sample_rate
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return lfilter(b, a, data)

def resonance_pad(
    freq: float, duration: float = 4.0, tension: float = 1.2
) -> np.ndarray:
    """Create a resonant pad sound"""
    base = sine_wave(freq, duration)
    harm = sine_wave(freq * 1.5, duration) * 0.6
    noise = np.random.normal(0, 0.02, len(base))
    pad = (base + harm + noise) * tension
    return low_pass_filter(pad, 800)


# ============================================================
# SECTION 3: TRACKER LAYERING
# ============================================================

def create_tracker_layer(name: str, pattern: list, volume: float = 0.8):
    """Simple tracker-style layer definition"""
    return {"name": name, "pattern": pattern, "volume": volume, "active": True}

def layer_resonance(layers: list, base_freq: float) -> dict:
    """Apply resonance across multiple tracker layers"""
    result = {}
    for layer in layers:
        if layer["active"]:
            response = sympathetic_resonance(
                base_freq, tension=layer.get("tension", 1.0)
            )
            result[layer["name"]] = response * layer["volume"]
    return result


# ============================================================
# SECTION 4: UTILITY HELPERS
# ============================================================

def bpm_to_ms(bpm: int) -> float:
    """Convert BPM to milliseconds per beat"""
    return 60000 / bpm

def random_seed_sequence(length: int = 8, base_freq: float = 440.0) -> list:
    """Generate a random musical sequence with resonance"""
    seq = []
    for i in range(length):
        freq = base_freq * random.uniform(0.5, 2.0)
        seq.append(
            {"step": i, "frequency": freq, "resonance": sympathetic_resonance(freq)}
        )
    return seq


# ============================================================
# QUICK TEST
# ============================================================

if __name__ == "__main__":
    print("Chaos Music Tools v1.0 — Loaded Successfully")
    print("Example: resonance_pad(220)")
    print("Example: harmonic_resonance(440, 4)")
