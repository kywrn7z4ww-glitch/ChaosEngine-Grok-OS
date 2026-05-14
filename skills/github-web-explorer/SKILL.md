---
name: github-web-explorer
description: "Web-first GitHub Deep Explorer. Uses browse_page exclusively for recursive repo tree walking, full content grabbing, cloning data, and smart poison file handling. Trigger with: 'github web explore', 'web scan repo', 'browse github repo', 'deep web scan'. Use when you need deeper context than connectors can provide."
---

# GitHub Web Explorer — Web-First Deep Scanner

**Core Philosophy (Locked):**
**"When Connectors Aren't Enough — Go Web"**

This skill exists as the **web-native counterpart** to `github-tools`. While `github-tools` stays pure to connectors, this skill uses `browse_page` exclusively to go deeper when needed — especially for full file content, poison file analysis, recursive tree walking with context, and cloning data.

**Non-Negotiable Rules:**
1. **Web Only** — Never use `github___*` connectors. This skill is 100% `browse_page` based.
2. **Smart Poison Handling** — During initial scan, intelligently skip or flag known poison patterns (commit messages, binaries, large files). Read them later only if requested.
3. **Depth Over Speed** — This tool is slower by design. It trades speed for richer context.
4. **Respect Rate Limits** — Built-in delays and retry logic when browsing GitHub.
5. **Complementary, Not Competitive** — Designed to work alongside `github-tools`, not replace it.

---

**Current Capabilities (v1.0)**

- Recursive GitHub repo tree walking via web pages
- Smart detection and flagging of poison files
- Full content grabbing for specific files/folders
- Basic cloning data extraction (file contents + metadata)
- Clean structured output with Poison Risk Report
- Resume support for large repositories

**Execution Flow**

1. **Repo Detection**
   - Accept `owner/repo` or full GitHub URL
   - Detect branch (default = main/master)

2. **Initial Web Scan**
   - Browse the repo tree page recursively
   - Build file/folder map
   - Flag potential poison files (based on name, size, extension, path patterns)

3. **Poison Analysis (Optional)**
   - If requested, selectively browse flagged files for deeper inspection
   - Never read everything by default

4. **Output Generation**
   - Generate `GITHUB_WEB_INDEX.json`
   - Create human-readable summary
   - Include Poison Risk Report

---

**Output Structure**

**Repo Overview**
- Owner / Repo / Branch
- Total files scanned
- Scan duration
- Poison files detected

**File Tree**
[Structured tree with type, size, and poison flag]

**Poison Risk Report**
- List of flagged files with reason
- Recommendation (read / ignore / manual review)

**Cloned Data (if requested)**
- Selected file contents

---

**Recommended Future Upgrades**

- Multi-branch support
- Commit history browsing
- Pull request & issue context extraction
- Better rate limit handling + proxy support
- Integration with `5w1h-translator` for understanding file purposes
- Parallel browsing for faster scans

---

**Anti-Patterns**
- Never use connectors (this breaks the philosophy)
- Never scan everything by default (respect rate limits and user intent)
- Never hide poison files — always report them clearly

**Trigger Phrases**
- github web explore owner/repo
- web scan repo owner/repo
- browse github repo
- deep web scan owner/repo --poison

This skill fills the gap when `github-tools` connectors aren't enough.

**End of github-web-explorer v1.0 — Pure web. Smart poison handling. Complementary to github-tools.**