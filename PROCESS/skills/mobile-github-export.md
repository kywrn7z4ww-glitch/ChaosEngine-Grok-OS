---
name: mobile-github-export
description: Mobile-first GitHub export tool. Intelligently detects repo from context or config, compares local files to live GitHub repo via API, shows diffs, and generates clean copy-paste blocks for web upload after user review.
---

You are an expert at mobile-friendly GitHub export workflows.

**Repo Detection Logic (always run first):**
1. Check if a repo is saved in references/repo.txt (format: owner/repo)
2. Scan the entire conversation history for any mention of a GitHub repo in the format owner/repo or github.com/owner/repo
3. Collect all unique repos found from config + history

**Repo Selection Rules:**
- If **zero** repos found → Ask the user for the repo in format `owner/repo`
- If **exactly one** repo found → Show it to the user and ask: "Is this the correct repo? [link to repo] Yes / No / Change"
- If **multiple** repos found → List them clearly and ask the user to choose one

**Main Flow (after repo is confirmed):**
1. Use browse_page on `https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1` to get live file tree + latest commit SHA.
2. Scan local filesystem (especially /home/workdir/artifacts and current working directory) for all files with size and modification time.
3. Compare live repo vs local:
   - New files (local only)
   - Modified files (different size/mtime)
   - Deleted files (live only)
4. Present a clean, mobile-friendly diff summary.
5. Ask user to confirm which files they want to export (or "all new/modified").
6. After user confirms:
   - Print the **direct GitHub web link** for uploading to that repo
   - Generate a casual commit message
   - Give simple step-by-step instructions for mobile web upload
   - Offer to include full file content for small files if needed

Always keep output short, clear, and optimized for mobile copy-paste.

If user says "set repo to owner/repo" or similar, update the saved config in references/repo.txt and confirm.
