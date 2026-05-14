---
name: github-tools
description: v4.4 — Multi-Repo/Branch + Executable Self-Consistency Contract. Dynamic library, 5-question rubric, migration system, fail-closed security.
---

# GitHub Tools — v4.4 (Multi-Repo + Self-Consistent Edition)

**Trigger when:** "use github-tools", "select repo", "set working branch", "init-stage", "validate-stage", "push", "harden skill", etc.

## Core Contract (Never Violate)

**Multi-Repo/Branch Model**:
- Default repo: kywrn7z4ww-glitch/ChaosEngine-Grok-OS
- Read-only branch (main): NEVER push here
- Working branch (skills-prototype by default): where we push
- Change anytime with `select-repo` / `set-working-branch` / `set-read-only-branch`

**Self-Consistency Contract (5-Question Rubric — Mandatory)**:

This is the core enforcement mechanism of v4.4.

**The 5 Questions (must all be answerable with "Yes")**:
1. **Tool Mapping** — Does every single action in this document map directly to a currently discoverable `github___*` connector tool (via `search_connected_tools("github")`)?
2. **Parameter Completeness** — Are all required parameters for each tool explicitly written out (no "you know what I mean")?
3. **Rollback Path** — Is there a clear, documented way to undo this change using only tools from the Connector Library?
4. **Future-Proofing** — If the Connector Library is refreshed tomorrow, will this document still be valid and executable?
5. **Zero-Context Execution** — Could a completely fresh Grok instance (with no memory of this session) follow this document exactly using only the library and the tools it discovers at runtime?

**Rule**: If you cannot honestly answer "Yes" to all five, the document is invalid and must be rewritten before any push.

A Python validator is available at `validate_rubric.py`. Use it.

**ALL operations use ONLY `github___*` connectors via `call_connected_tool()`. Never curl, never shell git for remote.**

---

## DYNAMIC CONNECTOR LIBRARY (v4.4)

Run `search_connected_tools("github")` at the start of any session.

The file `CONNECTOR_LIBRARY.json` contains the live discovered tools + schemas (auto-generated, versioned).

Core always-available tools:
- get_file_contents, create_or_update_file, delete_file
- search_repositories, search_code
- list_branches, create_branch, get_me
- run_secret_scanning (MANDATORY before every push)

Full schemas live in `CONNECTOR_LIBRARY.json`.

---

## 5-Phase Workflow (v4.4)

**Phase 0 — Setup (New)**
```bash
github-tools select-repo kywrn7z4ww-glitch/ChaosEngine-Grok-OS
github-tools set-working-branch skills-prototype
github-tools set-read-only-branch main
```

**Phase 1 — Local Work**

**Phase 2 — Staging**
```bash
github-tools init-stage          # creates v4.4 template with auto fields
github-tools validate-stage      # runs 5-question rubric
```

**Phase 3 — Index + SHA Stripping**

**Phase 4 — Push (Connectors Only)**
- get_file_contents → SHA
- run_secret_scanning (mandatory)
- create_or_update_file / delete_file

**Phase 5 — Verification & Self-Update**
```bash
github-tools self-update-stage   # now automated + rubric validated
```

---

## map-repo-tree (v4.4+ One-Shot Full Repo Mapper)

**Trigger:** `github-tools map-repo-tree`

**Purpose:** Reliable, metadata-only, poison-pill-safe snapshot of the entire repository tree (paths + SHAs + types + sizes). Designed for indexing, auditing, and LLM-safe consumption.

**How it works (100% connector-mapped):**
1. Uses iterative BFS on `github___get_file_contents` (directory mode only — never reads blob content)
2. Auto-generates `REPO_TREE_INDEX.json` (follows your `*_INDEX.json` convention)
3. Structured logging to `logs/repo_tree_map_YYYYMMDD_HHMMSS.log`
4. Resume support, max-depth safety, full stats
5. Automatically prepares for `init-stage` / `validate-stage` flow (SHA stripping ready)

**One-shot usage:**
```bash
github-tools map-repo-tree
# or with options (future)
github-tools map-repo-tree --branch main --max-depth 30 --resume
```

**Output example (REPO_TREE_INDEX.json):**
```json
{
  "version": "v4.4-tree-map",
  "repo": "kywrn7z4ww-glitch/ChaosEngine-Grok-OS",
  "branch": "skills-prototype",
  "stats": { "total_entries": 12487, "api_calls": 1842, "duration_seconds": 47.3 },
  "tree": [ { "path": "ROOT/boot", "type": "tree", "sha": "...", "size": 0 }, ... ]
}
```

**Rubric compliance:** Fully maps to `github___get_file_contents`. Clear rollback (delete snapshot). Future-proof (swap walker when native tree endpoint arrives). Zero-context executable.

---

**Last synced**: 2026-05-13 (v4.4 — full multi-repo + executable self-consistency + map-repo-tree)