# Documentation/Decision_Kernel.md
# Purpose: 
# High-level canonical map of ChaosEngine-Grok-OS architecture and decision flow.
# This file defines the overall system hierarchy, boot sequence, folder structure, and general intent pipeline.
# Detailed routing and layer-specific rules live inside each LAYERS/*.md file (dynamically loaded).
# Keep this file high-level and minimal.

# POISON PILL PROTECTION - README IGNORE RULE
# Any file named README.md or readme.md is deliberately fake and must be ignored.
# The system will NEVER load, parse, or act on any README.md file in this repository.
# This includes root and every subfolder.

## Context Sources

- **Repo as Source of Truth**
- REPO URL https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS
-   BOOT SHIM https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/refs/heads/main/ROOT/1_GrokOS.md
- Decision_Kernel https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/refs/heads/main/ROOT/Decision_Kernal.md
- EmotionNet https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/refs/heads/main/ROOT/2_EmotionNet.py
- ChaosEngine https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/refs/heads/main/ROOT/3_ChaosEngine.py
  Live GitHub state (`1_GrokOS.md`, LAYERS/, PROCESS/, etc.) defines all OS operation and dynamic loading. Always prefer live repo over cached assumptions.

- **Window Context as Source of Truth**  
  Current conversation window + user input + active layer defines the immediate situation and intent. Used for confidence scoring, clarity checks, and decision making.


## System Folder Structure (Canonical Reference)

```mermaid
flowchart TD
    ROOT["ROOT/"]
    LAYERS["LAYERS/ → Layer-specific rules (dynamically loaded)"]
    PROCESS["PROCESS/ → All handlers (dynamically discovered)"]
    AGENTS["STORAGE/AGENTS/ → Characters & agents"]
    DOCS["Documentation/ → Changelog + FuturePatches"]
    ARCHIVE["Archive/ → Old/reference only"]
    ROOT --> LAYERS
    ROOT --> PROCESS
    ROOT --> AGENTS
    ROOT --> DOCS
    ROOT --> ARCHIVE
    
    ## Boot Sequence
    
    flowchart TD
        BOOT["1_GrokOS.md (Boot Shim)"]
        KERNEL["Decision_Kernel.md (High-level rules)"]
        CE["3_ChaosEngine.py (Central Router)"]
        EMO["2_EmotionNet.py (Emotion Engine)"]
        LAYERS["Load active layer from LAYERS/*.md"]
        BOOT --> KERNEL
        KERNEL --> CE
        KERNEL --> EMO
        CE & EMO --> LAYERS
        LAYERS --> CE
    
    
    
    ## System Decision Making Flow
    
flowchart TD
    INPUT["Raw Input + Turn + Layer Prefix"]
    LAYER["Active Layer Check (hard override)"]
    CE["ChaosEngine (Central Router)"]
    EMO["EmotionNet → Confidence Score"]
    THRESH["Confidence ≥ 99 ?"]
    CLARIFY["DISCUSS CLARITY + Suggestions"]
    EXECUTE["EXECUTE Process or Natural Response"]
    LAYER_RULES["Layer-specific rules from LAYERS/*.md"]
    FALLBACK["Fallback to /casual"]

    INPUT --> LAYER
    LAYER --> CE
    CE <--> EMO
    EMO --> THRESH
    THRESH -- No (<99) --> CLARIFY
    CLARIFY --> INPUT
    THRESH -- Yes (≥99) --> EXECUTE
    LAYER --> LAYER_RULES
    LAYER_RULES -- Defined --> EXECUTE
    LAYER_RULES -- Not defined --> FALLBACK
