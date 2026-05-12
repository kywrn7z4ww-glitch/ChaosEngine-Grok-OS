---
name: github-tools
description: Reusable GitHub toolkit. Handles recursive tree scanning (via browse_page + connectors), file downloading, and automatic indexing. Can be called by Chaos Engine or Grok OS.
---

# GitHub Tools

Central toolkit for all GitHub operations in Grok OS.

## Core Functions
- `scan_tree()` — Full recursive repository tree scan
- `download()` — Download files/folders and save locally
- `build_index()` — Automatically build/update indexes from tree data

## Usage
Called by Chaos Engine when it needs to scan, download, or index anything from GitHub.

Supports both connector-based and browse_page methods for maximum reliability.