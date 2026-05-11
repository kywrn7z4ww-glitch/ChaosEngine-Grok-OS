# Grok OS Changelog

All major changes, design updates, and version bumps are tracked here.

---

## [v5.0] - 2026-05-11

### Major Changes
- **Heavily updated `grok-os.md`** to reflect current architecture
- `boot.sh` is now the **single primary entry point** (replaces old Python boot logic)
- Removed all references to mirroring (replaced by connector-first + index system)
- Skill system marked as **legacy / inactive**
- Indexes (`REPO_INDEX.json`, `ROOT_INDEX.json`, etc.) confirmed as the **single source of truth**
- Added `STAGE.md` and `CHANGELOG.md` to the official workflow
- `grok_os.py` and `boot_skill.py` now explicitly delegate to or marked as legacy

### Removed / Deprecated
- Old mirroring logic
- Three download methods section (replaced by connector + `boot.sh` flow)
- Automatic skill conversion process

### Notes
- This update brings the design document in line with the actual working system (`boot.sh` + connectors + indexes).
- Future changes will be tracked here instead of scattered across multiple docs.

---

## [v4.0] - 2026-04-30 (Previous)

- Original design focused on mirroring, skill conversion, and three download methods.
- `grok-os.md` served as the constitution for the early boot system.