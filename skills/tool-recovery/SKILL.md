---
name: tool-recovery
description: "Dual-mode deep tool recovery & environment probe with self-testing and stronger-prompt generation. Mode 1: full sandbox environment scan. Mode 2: focused all-skills & Grok tools inventory + recovery. Generates working test interactions and stronger internal prompts. Use on: 'tool recovery', 'deep scan all tools', 'probe environment', 'tool inventory', 'full sandbox scan', 'all skills scan', 'recover tools', 'self test tools'. Outputs dual structured JSON reports + summary + self-improvement artifacts to /home/workdir/artifacts/. Non-destructive by default. Hybrid bash+python."
---

# Tool Recovery

## Overview
Performs safe, dual-mode deep scans:
- **Full sandbox mode**: Comprehensive environment probe (packages, processes, executables, env, safe filesystem).
- **All skills mode**: Complete Grok tool/skill discovery (base tools, bundled + user SKILL.md files, connected services, versions, anomalies).

Includes built-in self-testing (generates runnable test interactions) and stronger-prompt generator for continuous self-improvement.

## Instructions

**Core Philosophy (Locked):**
**"Precise Awareness, Not Noise"**

This skill exists to give clear, targeted visibility into the tool ecosystem — never overwhelming the user with unnecessary data.

**Three Modes (New v2.0 System):**

| Mode          | Focus                                      | Trigger Examples |
|---------------|--------------------------------------------|------------------|
| **`base`**    | Core Grok tools only (render_file, write_file, edit_file, create_skill, bash, etc.) | `tool recovery base` |
| **`skills`**  | User-created skills only (`/home/workdir/.grok/skills/`) | `tool recovery skills` |
| **`everything`** | Full scan (base + all skills + environment) | `tool recovery everything` or default |

**Mode Detection Logic:**
- If user says `"base"` → Base Grok tools only (fastest)
- If user says `"skills"` → User skills only (clean, focused)
- If user says `"everything"` or no mode → Full scan (current behavior)

**Always follow this flow when activated:**

1. **Detect mode** from user message (see table above)

2. **Execute the probe**:
   ```bash
   /home/workdir/.grok/skills/tool-recovery/scripts/deep-probe.sh --mode <base|skills|everything>
   ```

3. **Review outputs** (always created in `/home/workdir/artifacts/`):
   - `tool-inventory-base-*.json` (base mode)
   - `tool-inventory-skills-*.json` (skills mode)
   - `tool-inventory-full-*.json` (everything mode)
   - `tool-recovery-summary-*.md` (human readable)
   - `self-test-interactions-*.json` + `stronger-prompts-*.md` (self-improvement)

4. **Apply recovery**:
   - Review "recovery_suggestions" array in JSON.
   - Run suggested non-destructive commands manually.
   - For missing skills: use skill-creator to re-init.

5. **Self-improvement step** (mandatory):
   - Review the generated stronger prompts.
   - Test the generated interactions if desired.
   - Log any new patterns for future refinement.

**Key principles**:
- Never destructive without explicit user confirmation.
- Always cross-validate with known base tools and actual filesystem.
- Use UO hybrid probes (bash depth + Python structure + connector calls when relevant).
- Keep scans scoped and timeout-protected for safety.

**Example triggers & expected behavior**:
- "tool recovery" → both modes + full report
- "deep scan all tools full sandbox" → full mode only
- "all skills scan and self test" → skills mode + generate tests

This skill makes the entire tool ecosystem self-aware and recoverable.

## Self-Improvement Loop (Built-in)
After every run the script automatically:
- Generates 3–5 stronger prompt variants for this skill.
- Creates 2–4 ready-to-run test interactions (e.g. "simulate missing bundled skill", "test connected probe").
- These are saved for you to copy-paste and validate.

**This is now a living, self-strengthening tool-recovery system (v2.0).**