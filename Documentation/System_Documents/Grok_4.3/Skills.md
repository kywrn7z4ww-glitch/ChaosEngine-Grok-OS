# Grok OS Skills

This folder contains portable skills for ChaosEngine Grok OS.

## boot-grok-os

**Purpose:** One-command bootstrap of the full Grok OS lattice (Kernel → Layers → EmotionNet/ChaosEngine → Processes).

**File:** `boot-grok-os-skill.tar.gz`

### Installation (fresh machine)

```bash
# 1. Extract into your local skill directory
tar -xzf boot-grok-os-skill.tar.gz -C ~/.grok/skills/

# 2. (Optional) Verify
ls ~/.grok/skills/boot-grok-os/
```

### Usage

Say any of these phrases:
- "boot Grok OS"
- "load Grok OS"
- "start ChaosEngine"
- "boot the lattice"

The skill will:
- Verify latest commit SHA
- Mirror only `ROOT/` files (poison pills ignored)
- Chain-load `1_GrokOS.py`
- Enable on-demand sync for future missing files

### Notes

- Requires Python 3 + internet (for GitHub API calls)
- Creates `/opt/grok-os/ROOT` and `/opt/grok-os/.cache` automatically
- Fully compatible with current hierarchy (Core → TheRedQueen → Luna → BabySkynet)

For future me: keep this file updated when new skills are added.
