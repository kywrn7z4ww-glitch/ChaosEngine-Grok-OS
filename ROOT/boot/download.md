# Grok Download Skill — v1.2 (SHA + Commit Aware)

**Status:** Production-ready with proper remote freshness checking.

**Purpose:** A single, powerful, reusable skill that handles **all** URL-based downloads reliably — from single files to entire GitHub folders — with smart caching, exact content fidelity, optional safety filters, and clean connector logic for `.py` files. Serves as the foundation for your future network module.

**Design Goals:**
- 100% generic / blank-slate (no hard-coded repos)
- Optional poison filtering (opt-in per request or profile)
- Local-first + SHA sidecar caching (configurable freshness)
- **Proper remote SHA + commit checking** (new in v1.2)
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

### 1.2 Local-First + Remote SHA Check (v1.2)

For every target file:

1. **Check for local cache** (`.meta.json`)
   - If no `.meta.json` exists → **Cold boot**: Always download (guarantees latest files).

2. **Remote freshness check** (via GitHub API)
   - Fetch current blob SHA or tree SHA from GitHub.
   - Compare against stored `remote_sha` / `remote_commit` in `.meta.json`.

3. **Decision**
   - If remote SHA matches → **Skip** (fresh)
   - If different or no cache → Download + update `.sha256` + `.meta.json`

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

### 1.4 Save + Sidecars
- `mkdir -p` parent directories
- `write_file` with exact content
- Create/update:
  - `filename.sha256`
  - `filename.meta.json` (contains `remote_sha`, `remote_commit`, `last_checked`, `source_url`)

### 1.5 Error Handling & Reporting (Mandatory)
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
  - Uses GitHub API to get tree SHA
  - Compares tree SHA first (very fast skip if unchanged)
  - Then only downloads changed files
- **Return content only** (`--return-content`): for your future network module

---

## 5. Pluggable Connector Logic for .py Files & Network Module

Any `.py` file can declare:

```python
# === GROK-DOWNLOAD CONNECTOR v1.2 ===
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

## 7. Cold Boot Guarantee (v1.2)

When there is no `.meta.json` cache (first run or after clearing cache), the skill **always** pulls the latest version of every file from the repository. No false "fresh" skips on cold boot.

---

**End of v1.2 spec.**
