# Grok Download Skill — v1.4 (Full Scanning + Safe Poison Rules)

**Status:** Production-ready. GitHub API via `browse_page` is the **primary and first** method.

**Purpose:** Reliably download files and folders from GitHub with full tree scanning, SHA verification, raw URL fallback, and graceful handling of missing/broken files.

---

## Core Behavior

When activated:

### 1. Parse Request
- Extract URL or GitHub path
- Determine target directory
- Apply profile (default: `grok-os`)
- Collect flags (`--force`, `--freshness-days`, `--no-sha`, etc.)

### 2. API-First Freshness Check (Primary Method)
- Use GitHub API via `browse_page` to get latest commit SHA and tree
- Compare with local `.meta.json`
- Only download if newer or forced

### 3. Prefer Raw URLs
- Convert GitHub blob/tree URLs to `raw.githubusercontent.com`
- This gives clean content without HTML wrappers

### 4. Full Tree Scanning
- When given a folder path, recursively scan the entire tree
- Respect `.gitignore`-style patterns only if explicitly enabled
- Never skip high-level folders by default

### 5. Poison Filtering (Updated Rules v1.4)

**New Safe Rule:**
- **Only specific root-level files** are poisoned
- **All high-level folders** are considered safe by default

**Current Poison List (Root files only):**
- `README.md`
- `LICENSE`
- `tetris_curse.py`
- Any file starting with `.` (hidden files)
- Any file containing `test` or `example` in the name (optional, profile-dependent)

**High-level folders that are ALWAYS SAFE:**
- `PROCESS/`
- `layers/`
- `boot/`
- `chaos-engine/`
- `emotion-net/`
- `STORAGE/`
- `NETWORK_HUB/`
- `Documentation/`

### 6. Cold Boot Guarantee
- If no `.meta.json` exists → always download latest
- Create sidecars on every successful download:
  - `.sha256`
  - `.meta.json` (remote_sha, remote_commit, last_checked, profile)

### 7. Error Handling & Breakage Recovery
- On 404: Create placeholder + log
- On broken file: Move to `BROKEN/` + log
- Never halt the entire process on one failure
- Continue with next file/folder

### 8. Self-Bootstrap Mode
- Can install itself first if missing
- Then proceed to download full `ROOT/` structure

---

## Profiles

| Profile   | Poison Filtering          | Use Case                  |
|-----------|---------------------------|---------------------------|
| `generic` | Minimal                   | General use               |
| `grok-os` | Root files only (default) | Full Grok OS mirror       |
| `strict`  | Aggressive                | Clean/safe environments   |
| `custom`  | User-defined              | Advanced users            |

---

## Usage Examples

```bash
# Full Grok OS mirror (recommended)
grok-download --profile grok-os https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/tree/main/ROOT

# Single file with raw priority
grok-download https://raw.githubusercontent.com/.../file.py

# Force refresh
grok-download --force --freshness-days 0 [url]
```

---

**Last Updated:** 2026-04-29
**Version:** 1.4 (Safe Poison Rules + Full Tree Scanning)
