# Grok Download Skill — v1.3 (API-First + Full ROOT Bootstrap)

**Status:** Production-ready. GitHub API via `browse_page` is the **primary and first** method. Pre-configured for full Grok OS ROOT download + self-bootstrap.

**Purpose:** A single, powerful, reusable skill that handles **all** URL-based downloads reliably — from single files to entire GitHub folders — with smart caching, exact content fidelity, optional safety filters, and clean connector logic for `.py` files. Serves as the foundation for your future network module.

**Design Goals:**
- 100% generic / blank-slate (no hard-coded repos) — but **baked-in defaults** for your ChaosEngine-Grok-OS repo
- Optional poison filtering (opt-in per request or profile)
- Local-first + SHA sidecar caching (configurable freshness)
- **GitHub API via browse_page is the FIRST and PRIMARY method** for SHA/commit checking (v1.3)
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
- Apply profile (default: `grok-os` for this repo)
- Collect optional flags: `--force`, `--freshness-days N`, `--no-sha`, `--filename NAME`, `--poison "file1,file2"`, `--retries N`, `--return-content`, etc.

### 1.2 API-First Freshness Check (v1.3 — Primary Method)

**This is now the FIRST and PRIMARY action for all GitHub URLs.**

1. **Call GitHub API via browse_page** (new in v1.3)
   - For folders: `https://api.github.com/repos/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/git/trees/main?recursive=1`
   - For files: `https://api.github.com/repos/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/commits?path={path}&per_page=1`
   - Extract the latest `sha` / `tree.sha`

2. **Compare with local `.meta.json`**
   - If no `.meta.json` exists → **Cold boot**: Always download everything (guarantees latest files).
   - If `.meta.json` exists → Compare `remote_sha` / `remote_commit` with API result.
   - If different → Download only changed files.
   - If same → Skip (fresh).

This replaces flaky web scraping with reliable API calls.

### 1.3 Prefer Raw URLs (Important)
When the input URL is a GitHub blob or tree URL, the skill **automatically converts it to the equivalent raw.githubusercontent.com URL** before fetching. This gives cleaner, exact content with no HTML wrapping.

Example conversion:
- Input: `https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/blob/main/ROOT/chaos-engine/chaos_engine.py`
- Used internally: `https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/main/ROOT/chaos-engine/chaos_engine.py`

### 1.4 Fetch Exact Content (Critical)
Always use this exact instruction when calling `browse_page`:

```
Return the COMPLETE, EXACT, UNMODIFIED content of this resource as plain text.
Do NOT summarize, truncate, rewrite, add explanations, HTML, or change even one character.
Output ONLY the raw original bytes as text. If the content is binary or too large, return base64 with a clear "BASE64:" prefix.
```

### 1.5 Save + Sidecars
- `mkdir -p` parent directories
- `write_file` with exact content
- Create/update:
  - `filename.sha256`
  - `filename.meta.json` (contains `remote_sha`, `remote_commit`, `last_checked`, `source_url`)

### 1.6 Error Handling & Reporting (Mandatory)
On any failure:
- Record: URL, error type, HTTP status if known, retry count
- Continue with remaining files
- Final report always includes:
  - Downloaded (count + bytes)
  - Skipped (fresh / SHA match)
  - Failed (with short reason)
  - Poisoned (if any)
  - Total time

---

## 2. Profiles (Choose Per Request)

| Profile     | Poison Filtering          | Strictness          | Best For                     |
|-------------|---------------------------|---------------------|------------------------------|
| `generic`   | None (default)            | Normal              | Everyday use, most projects  |
| `grok-os`   | Enabled (see section 3)   | High                | Your ChaosEngine-Grok-OS repo|
| `strict`    | User-supplied list only   | Very high           | Sensitive / untrusted sources|
| `custom`    | Via `--poison` flag       | As specified        | One-off needs                |

**Default profile for this skill: `grok-os`**

---

## 3. Optional Poison Filtering (Opt-in)

When profile is `grok-os` or `--poison` is supplied:
- Only **exact filename matches** are blocked (case-insensitive)
- Default grok-os poison list:
  - `README.md` (any case)
  - `tetris_curse.py`
  - `boot_shim.py`

---

## 4. Supported Download Modes

- **Single file** — any raw URL
- **Batch list** — comma or space separated URLs
- **GitHub folder / repo discovery**:
  - Uses GitHub API first (tree SHA comparison)
  - Only downloads changed files
- **Full ROOT bootstrap mode** (new in v1.3):
  - Trigger with: "grab core files for grok os" or "download entire ROOT folder"
  - Automatically targets: `https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/tree/main/ROOT`
  - Downloads **every single file** in all subfolders (`boot/`, `chaos-engine/`, `emotion-net/`, `layers/`, etc.)
  - Uses raw URLs + API-first SHA checking
  - Self-bootstrap: installs/updates the skill first if needed, then proceeds with full download

- **Return content only** (`--return-content`): for your future network module

---

## 5. Pluggable Connector Logic for .py Files & Network Module

Any `.py` file can declare:

```python
# === GROK-DOWNLOAD CONNECTOR v1.3 ===
# All network / URL operations in this file are handled by the grok-download skill.
download_url(url, target_path, profile="generic", freshness_days=7)
sync_github_folder(github_url, local_dir, profile="grok-os")
```

---

## 6. Configuration Flags (All Optional)

- `--target-dir /path`
- `--freshness-days 30`
- `--force`
- `--dry-run`
- `--offline`
- `--no-sha`
- `--filename custom.name`
- `--profile generic|grok-os|strict|custom`
- `--poison "file1,file2"`
- `--retries 3`
- `--return-content`

---

## 7. Cold Boot Guarantee (v1.3)

When there is no `.meta.json` cache (first run or after clearing cache), the skill **always** pulls the latest version of every file from the repository. No false "fresh" skips on cold boot.

---

**End of v1.3 spec.**
