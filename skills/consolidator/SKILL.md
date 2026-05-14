---
name: consolidator
description: "Smart Consolidator. Consolidates, condenses, and compresses files in an intelligent manner while preserving original intent, clarity, and fidelity. Use when you need to analyze, share, review, or feed a full codebase to an LLM without losing context."
---

# Consolidator — Smart Context-Preserving Compressor

**Core Philosophy (Locked):**
**"Consolidate Smart. Compress Intelligently. Never Lose Intent, Clarity, or Fidelity."**

This skill exists to **consolidate, condense, and compress** entire projects or codebases in a smart, context-aware way. It is designed for situations where you need to feed large amounts of code/context to an LLM (or human) while keeping the original meaning, structure, and intent intact.

**Non-Negotiable Rules:**
1. **Preserve Intent First** — Never summarize or compress in a way that changes or loses the original purpose of the code.
2. **Maintain Clarity** — Output must remain readable and well-structured.
3. **Protect Fidelity** — Key logic, comments, architecture, and relationships must be preserved.
4. **Smart Compression Only** — Use intelligent selection, hierarchical organization, and smart summarization where safe. Never blindly truncate.
5. **Context is Sacred** — When in doubt, keep more context rather than less.

---

**Primary Use Cases**
- Feeding large codebases to LLMs for analysis, refactoring, or review
- Creating clean, condensed project overviews
- Preparing context for long-running agent tasks
- Sharing project snapshots without losing critical details

---

**Execution Approach (Flexible & Smart)**

The consolidator can use multiple strategies depending on the request:

**Strategy 1: Smart Hierarchical Consolidation (Default)**
- Organize by directory structure
- Keep high-level architecture + key files in full
- Use smart summarization only for repetitive/low-value sections
- Preserve all critical logic and intent

**Strategy 2: Context-Preserving Compression**
- Identify and keep core files (entry points, main logic, config, architecture)
- Condense repetitive modules while preserving their purpose
- Maintain relationships and data flow

**Strategy 3: Full + Intelligent Filtering**
- Include everything important
- Apply smart filtering for size (skip generated files, node_modules, build artifacts, etc.)
- Add clear structure and navigation

---

**Output Format (Recommended)**
- Clean Markdown with proper language fences
- Hierarchical structure (directories → files → content)
- Header with: project name, total files, lines, git commit, timestamp
- Clear separation between architecture overview and detailed code

---

**Anti-Patterns (Hard Rules)**
- Never blindly truncate important logic
- Never lose the "why" behind code decisions
- Never remove comments that explain intent
- Never assume something is "unimportant" without strong justification
- Never sacrifice clarity for smaller file size

**Trigger Phrases**
- consolidate the project
- condense the codebase
- compress the repo smartly
- create context for LLM
- full project overview with intent preserved
- smart consolidate

This skill turns large, messy codebases into **clean, intelligent, context-rich** representations — perfect for analysis and LLM consumption.

**End of consolidator v2.0 — Smart. Context-aware. Fidelity-first.**