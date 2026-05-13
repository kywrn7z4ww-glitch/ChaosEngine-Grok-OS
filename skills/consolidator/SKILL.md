---
name: consolidator
description: Consolidates an entire project into one clean, optimized text file. Git-aware, supports 30+ languages, automatic .gitignore respect, size protection, and stats. Use whenever the user wants to analyze, share, review, or feed a full codebase to an LLM.
---

# Consolidator

**Trigger when:** User asks to "consolidate the project", "dump the whole codebase", "put everything in one file", "analyze the full repo", or similar.

## Instructions

Always use this skill for project consolidation tasks. It is faster, safer, and more consistent than manual commands.

### Steps
1. Change directory to the project root (where `.git` or main source files live).
2. Execute the consolidator script with desired options.
3. Review the output file (default: `codebase.txt` or custom name).

### Script location
`scripts/consolidator.sh` (executable, self-contained).

### Recommended usage
```bash
./scripts/consolidator.sh --md
```

This produces clean Markdown with language-aware code blocks — ideal for pasting into chats or LLMs.

### Full option reference
- `-o FILE` / `--output FILE` — Output filename (default: codebase.txt)
- `--md` — Markdown mode with ```language fences
- `--max-size KB` — Skip files larger than this (default: 2048)
- `-e DIRS` / `--exclude DIRS` — Comma-separated extra paths to skip
- `--no-git` — Force classic find mode (ignore .gitignore)
- `-v` / `--verbose` — Show skipped files in output
- `-h` / `--help` — Show usage

### Examples
```bash
# Best default for most projects
./scripts/consolidator.sh --md

# Custom output + size limit
./scripts/consolidator.sh -o review.txt --max-size 1024

# Non-git or legacy project
./scripts/consolidator.sh --no-git -o full-dump.txt -v
```

The script automatically:
- Uses `git ls-files` when available (respects .gitignore)
- Falls back to smart `find` otherwise
- Skips binaries, images, node_modules, dist, build, __pycache__, minified files, etc.
- Adds header with git commit, file count, and total lines
- Sorts output deterministically

**Last synced**: 2026-05-12