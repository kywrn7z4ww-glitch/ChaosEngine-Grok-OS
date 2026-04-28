---
name: grok-download
description: Production-grade generic download-from-URL skill. Fetches any URL using browse_page with exact-content mode, saves with write_file + SHA sidecars, local-first caching (configurable), optional poison filtering, batch support, GitHub folder discovery, pluggable .py connector logic, and profiles for different use cases (generic / grok-os / strict). Designed as foundation for future network modules. Triggers: "download from URL", "fetch this", "grab folder from github.com/...", or any connector comment. Fully blank-slate and shareable.
---

# Grok Download Skill — Generic URL Fetch & Save (v1.1 — Enhanced)

**Status:** Production-ready, heavily improved, ready for broad use and future network module integration.

**Purpose:** A single, powerful, reusable skill that handles **all** URL-based downloads reliably — from single files to entire GitHub folders — with smart caching, exact content fidelity, optional safety filters, and clean connector logic for `.py` files. Serves as the foundation for your future network module.

**Design Goals:**
- 100% generic / blank-slate (no hard-coded repos)
- Optional poison filtering (opt-in per request or profile)
- Local-first + SHA sidecar caching (configurable freshness)
- Exact content preservation (never summarize code/files)
- Rich configuration + profiles
- Future-proof for network module (return-content mode, headers, retries, etc.)
- One skill to rule all downloads until native connectors arrive

---

## 1. Core Behavior (Always Follow)

When the skill is activated:

### 1.1 Parse Request
- Extract URL(s) or GitHub folder path
- Determine target directory (default `~/.grok-downloads/`, or user-specified, or temp dir)
- Apply profile (default: `generic`)
- Collect optional flags: `--force`, `--freshness-days N`, `--no-sha`, `--filename NAME`, `--poison "file1,file2"`, `--retries N`, `--return-content`, etc.

### 1.2 Local-First Check (per file)
For every target file:
- If exists:
  - Check modification time (freshness window, default 7 days)
  - If `--sha` enabled: compare against `.sha256` sidecar (if present)
- If fresh and valid → **skip** with reason "fresh"
- If missing / stale / `--force` → proceed to fetch

### 1.3 Fetch Exact Content (Critical)
Always use this exact instruction when calling `browse_page`:

```
Return the COMPLETE, EXACT, UNMODIFIED content of this resource as plain text.
Do NOT summarize, truncate, rewrite, add explanations, HTML, or change even one character.
Output ONLY the raw original bytes as text. If the content is binary or too large, return base64 with a clear "BASE64:" prefix.
```

- GitHub raw URLs → perfect source code
- Other URLs → best-effort exact text (use raw links when possible)

### 1.4 Save + Sidecar (unless `--return-content`)
- `mkdir -p` parent directories
- `write_file` with exact content
- If not `--no-sha`: run `sha256sum file > file.sha256`
- Touch file to update mtime for freshness tracking

### 1.5 Error Handling & Reporting (Mandatory)
On any failure (404, rate-limit, timeout, parse error, write failure, etc.):
- Record: URL, error type, HTTP status if known, retry count
- Continue with remaining files (never abort whole batch)
- Final report always includes:
  - Downloaded (count + bytes)
  - Skipped (fresh / already exists)
  - Failed (with short reason)
  - Poisoned (if any were filtered)
  - Total time

---

## 2. Profiles (Choose Per Request)

| Profile     | Poison Filtering          | Strictness          | Best For                     |
|-------------|---------------------------|---------------------|------------------------------|
| `generic`   | None (default)            | Normal              | Everyday use, most projects  |
| `grok-os`   | Enabled (see section 3)   | High                | Your ChaosEngine-Grok-OS repo|
| `strict`    | User-supplied list only   | Very high           | Sensitive / untrusted sources|
| `custom`    | Via `--poison` flag       | As specified        | One-off needs                |

Example:
> download entire folder from https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/tree/main/ROOT --profile grok-os

---

## 3. Optional Poison Filtering (Opt-in)

When profile is `grok-os` or `--poison` is supplied:
- Only **exact filename matches** are blocked (case-insensitive)
- Rule is **always repo-specific** when a repo is detected in the URL
- Default grok-os poison list (when `--profile grok-os`):
  - `README.md` (any case)
  - `tetris_curse.py`
  - `boot_shim.py`
- You can override: `--poison "README.md,secret.py,another.bad"`

**Never** apply poison rules to other repos unless explicitly requested.

---

## 4. Supported Download Modes

- **Single file** — any raw URL
- **Batch list** — comma or space separated URLs
- **GitHub folder / repo discovery**:
  - `download entire folder from https://github.com/user/repo/tree/main/path`
  - Uses GitHub API + `browse_page` → recursive file list → filter → fetch each
- **Return content only** (`--return-content`): for your future network module — returns the text instead of writing to disk (perfect for in-memory processing)

---

## 5. Pluggable Connector Logic for .py Files & Network Module

Any `.py` file (or future network module) can declare:

```python
# === GROK-DOWNLOAD CONNECTOR v1.1 ===
# All network / URL operations in this file are handled by the grok-download skill.
# Supported calls the agent understands:
#   download_url(url, target_path, profile="generic", freshness_days=7, poison=None)
#   sync_github_folder(github_url, local_dir, profile="grok-os")
#   fetch_content(url, return_content=True)   # for network module in-memory use
```

The agent automatically routes matching requests through this skill.

This pattern keeps your code clean and lets the skill evolve (or be replaced by native connectors) without touching your `.py` files.

---

## 6. Configuration Flags (All Optional)

- `--target-dir /path`          → where to save
- `--freshness-days 30`         → override 7-day default
- `--force`                     → ignore cache, always re-download
- `--no-sha`                    → skip sidecar creation
- `--filename custom.name`      → override output filename
- `--profile generic|grok-os|strict|custom`
- `--poison "file1,file2"`      → custom poison list (comma separated)
- `--retries 3`                 → simple retry on transient errors
- `--return-content`            → return text instead of saving (network module)
- `--headers "Key: Value"`      → future header support (passed to browse_page when possible)

---

## 7. Trigger Phrases & Natural Language

Works with any natural phrasing:
- "download from URL https://..."
- "fetch this link and save it"
- "grab the whole folder from github.com/user/repo/tree/main/src"
- "update my local copy of https://... using grok-download"
- "use grok-download with grok-os profile for the ChaosEngine repo"
- "fetch content only from https://... for the network module"

---

## 8. Example Usage

**Simple:**
> download from URL https://raw.githubusercontent.com/someone/project/main/script.py --target-dir ~/src

**Grok OS style (with poison protection):**
> download entire folder from https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/tree/main/ROOT --profile grok-os --target-dir /opt/grok-os/ROOT

**For your future network module:**
> fetch content only from https://api.example.com/data.json --return-content

**Batch in a .py file (connector style):**
The script can contain:
```python
# === GROK-DOWNLOAD CONNECTOR v1.1 ===
download_url("https://...", "/tmp/a.txt", freshness_days=1)
sync_github_folder("https://github.com/user/repo/tree/main", "./local", profile="generic")
```

---

## 9. Future Migration & Network Module Path

- When native `git`, `curl`, or connector support arrives → this skill is updated in **one place** to prefer the faster method.
- Your `.py` files and future network module stay unchanged.
- The `--return-content` + connector pattern is specifically designed so your network module can use this skill today for reliable fetching, then swap the backend later with zero code changes.

---

## 10. Notes for Sharers & Forkers

- This is a **complete, self-contained, shareable skill**.
- Copy the whole folder into any `.grok/skills/` directory.
- Rename to `url-download`, `net-fetch`, etc. if desired.
- Add your own `references/` files for project-specific defaults.
- Zero dependencies on any external repository.

**This skill is now ready for production use across all your projects and as the foundation for your network module.**

---

**End of enhanced v1.1 spec.**
