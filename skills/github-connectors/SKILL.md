---
name: github-connectors
description: "GitHub Connector Tools Reference. Literal definitions, schemas, and usage for all github___* tools discovered via search_connected_tools('github'). Call these exclusively for GitHub ops. Always discover first."
---

# GitHub Connectors — Official Tool Definitions

**Core Rule (Non-Negotiable):**  
All GitHub operations **MUST** use only these `github___*` connector tools via `call_connected_tool()`.  
**Never** use direct API calls, curl, or shell git for remote operations.  
**Always** begin with `search_connected_tools("github")` (or `"all"`) to retrieve the live, versioned list + full JSON schemas before any call.

**How to Use:**
1. `search_connected_tools(query="github")` → returns current tool names + complete `json_schema` for each.
2. `call_connected_tool(tool_name="github___XXX", arguments={...})` using the exact schema from discovery.

**Discovered Tools (2026-05-14 snapshot — re-run search for latest):**

## 1. github___search_repositories
**Title:** GitHub · search_repositories  
**Description:** Find GitHub repositories by name, description, readme, topics, or other metadata. Perfect for discovering projects, finding examples, or locating specific repositories across GitHub.  
**Required:** `["query"]`  
**Key Properties:**  
- `query` (string, required): Repository search query. Supports advanced syntax e.g. `'machine learning in:name stars:>1000 language:python'`, `'topic:react'`, `'user:facebook'`.  
- `sort` (enum: stars, forks, help-wanted-issues, updated)  
- `order` (asc/desc), `page`, `perPage` (max 100), `minimal_output` (bool, default true)  
**Usage Note:** Primary discovery tool. Use before forking, cloning, or referencing repos.

## 2. github___search_code
**Title:** GitHub · search_code  
**Description:** Fast and precise code search across ALL GitHub repositories using GitHub's native search engine. Best for finding exact symbols, functions, classes, or specific code patterns.  
**Required:** `["query"]`  
**Key Properties:**  
- `query` (string, required): Code search syntax e.g. `'content:Skill language:Java org:github'`, `'NOT is:archived language:Python OR language:go'`, `'repo:github/github-mcp-server'`. Supports language, path, org filters.  
- `sort` (indexed only), `order`, `page`, `perPage`  
**Usage Note:** Ideal for code archaeology, finding implementations, or verifying patterns across the ecosystem.

## 3. github___get_file_contents
**Title:** GitHub · get_file_contents  
**Description:** Get the contents of a file or directory from a GitHub repository.  
**Required:** `["owner", "repo"]`  
**Key Properties:**  
- `owner` (string), `repo` (string)  
- `path` (string, default "/") — file or directory path  
- `ref` (string) — branch/tag/PR ref e.g. `refs/heads/main`, `refs/pull/123/head`  
- `sha` (string) — specific commit SHA  
**Usage Note:** Core read primitive. Use for reading files before editing or auditing. Directory mode returns listing.

## 4. github___create_or_update_file
**Title:** GitHub · create_or_update_file  
**Description:** Create or update a single file in a GitHub repository. If updating, provide the SHA of the file you want to update.  
**Required:** `["owner", "repo", "path", "content", "message", "branch"]`  
**Key Properties:**  
- `owner`, `repo`, `path`, `content` (string — full file content), `message` (commit msg), `branch`  
- `sha` (string, required **only** for updates — get via get_file_contents or git rev-parse)  
**Usage Note:** Primary write primitive. **Always** fetch SHA first for existing files. Use for all skill/code pushes.

## 5. github___delete_file
**Title:** GitHub · delete_file  
**Description:** Delete a file from a GitHub repository.  
**Required:** `["owner", "repo", "path", "message", "branch"]`  
**Key Properties:**  
- `owner`, `repo`, `path`, `message`, `branch`  
**Usage Note:** Irreversible. Use only after confirmation. Pair with get_file_contents for SHA if needed (though delete uses branch/path).

## 6. github___list_branches
**Title:** GitHub · list_branches  
**Description:** List branches in a GitHub repository.  
**Required:** `["owner", "repo"]`  
**Key Properties:** `owner`, `repo`, `page`, `perPage` (max 100)  
**Usage Note:** Precursor to create_branch or checkout planning.

## 7. github___create_branch
**Title:** GitHub · create_branch  
**Description:** Create a new branch in a GitHub repository.  
**Required:** `["owner", "repo", "branch"]`  
**Key Properties:**  
- `owner`, `repo`, `branch` (new branch name)  
- `from_branch` (string, defaults to repo default)  
**Usage Note:** Use after list_branches. Common in staging workflows.

## 8. github___list_releases
**Title:** GitHub · list_releases  
**Description:** List releases in a GitHub repository.  
**Required:** `["owner", "repo"]`  
**Key Properties:** `owner`, `repo`, `page`, `perPage`  
**Usage Note:** For versioning, changelog, or deployment checks.

## 9. github___list_tags
**Title:** GitHub · list_tags  
**Description:** List git tags in a GitHub repository.  
**Required:** `["owner", "repo"]`  
**Key Properties:** `owner`, `repo`, `page`, `perPage`  
**Usage Note:** Complements list_releases for tag-based workflows.

## 10. github___get_commit
**Title:** GitHub · get_commit  
**Description:** Get details for a commit from a GitHub repository.  
**Required:** `["owner", "repo", "sha"]`  
**Key Properties:**  
- `owner`, `repo`, `sha` (commit SHA, branch, or tag)  
- `include_diff` (bool, default true) — include file diffs and stats  
- `page`, `perPage`  
**Usage Note:** Deep commit inspection, diff review, or history tracing.

## 11. github___get_me
**Title:** GitHub · get_me  
**Description:** Get details of the authenticated GitHub user. Use when a request is about the user's own profile or when information is missing to build other tool calls.  
**Required:** `[]` (no params)  
**Usage Note:** Quick identity check or to populate owner fields dynamically.

## 12. github___fork_repository
**Title:** GitHub · fork_repository  
**Description:** Fork a GitHub repository to your account or specified organization.  
**Required:** `["owner", "repo"]`  
**Key Properties:**  
- `owner`, `repo`  
- `organization` (optional target org)  
**Usage Note:** Use after search_repositories when you need your own copy.

---

**Additional Notes (from Connector Protocol):**
- Schemas are self-describing via the `json_schema` field returned by search_connected_tools.
- Some tools support pagination (`page`, `perPage` max 100).
- File operations (get/create/update/delete) are the foundation for all repo mutations.
- **Self-Consistency Check:** Before any push or mutation, re-discover tools and validate required params exactly match the live schema.
- More tools may exist (e.g. issues, pull requests, organizations, secret scanning). Always run fresh `search_connected_tools("github")` — do not hardcode.

**End of github-connectors v1.0 — Literal. Discover-first. Connector-only.**

*This skill exists purely as the authoritative, zero-assumption reference for GitHub connector tools and what they do.*