---
name: smart-git-clone
description: "Intelligent Hybrid Git Clone Tool. Uses github-tools + github-web-explorer + 5w1h-translator + truth-blade + auditor to smartly clone repositories with conflict awareness, intent-based filtering, and minimal overhead. Trigger with: 'smart clone', 'intelligent clone', 'smart git clone owner/repo'. Use when you want accurate, efficient cloning without the downsides of traditional git clone."
---

# Smart Git Clone — Intelligent Hybrid Cloner

**Core Philosophy:**
**"Be Smart When Possible — Be Simple When Necessary"**

Most repositories are straightforward. For normal repos, use intelligence (hybrid approach, filtering, intent analysis). For chaotic/"schitzo" repos, just clone fully and interpret later — no overthinking.

**Non-Negotiable Rules:**
1. **Hybrid First** — Prefer `github-tools` for metadata, use web only when needed.
2. **Intent-Driven by Default** — Use `5w1h-translator` unless user says "just clone it".
3. **Chaos Mode** — If repo is detected as highly complex/chaotic, switch to simple full clone mode automatically.
4. **Conflict Aware** — Detect and report conflicts, but don't try to auto-resolve unless asked.
5. **Quality Controlled** — Use `auditor` + `truth-blade` for important clones.

---

**Execution Flow**

**Phase 0 — Intent Clarification**
- Use `5w1h-translator` to understand the user's real goal (full clone? specific branch? just source? resolve conflicts?)

**Phase 1 — Fast Metadata Scan** (`github-tools`)
- Use `map-repo-tree` or `deep-repo-scan` (connector mode)
- Get complete file tree + SHAs + sizes
- Identify branches and recent activity

**Phase 2 — Smart Filtering** (`truth-blade` + `5w1h-translator`)
- Analyze the tree against user intent
- Flag low-value files (binaries, large media, generated files, etc.)
- Detect potential conflicts (divergent branches, modified files)

**Phase 3 — Targeted Deep Fetch** (`github-web-explorer`)
- Selectively fetch full content only for high-value files
- Use smart poison handling
- Respect rate limits

**Phase 4 — Output + Validation** (`auditor`)
- Generate clean output (structured data or files)
- Run quality audit on the clone
- Produce Conflict Report + Recommendations

**Phase 5 — Learning** (`project-pusher`)
- Extract high-value patterns
- Feed back into the system

---

**Output Structure**

**Clone Summary**
- Repo + Branch
- Intent alignment
- Files cloned vs skipped
- Conflicts detected

**Conflict Report**
- List of potential merge conflicts
- Divergent branches
- Recommended resolution strategy

**Cloned Data**
- Either structured JSON or actual files (user choice)

**Recommendations**
- Next steps based on clone results

---

**Current Limitations (v1.0)**
- Still in early development
- Conflict resolution suggestions are basic
- Rate limiting is conservative
- Full testing needed

**Recommended Future Upgrades**
- Better conflict detection and auto-resolution suggestions
- Parallel metadata + content fetching
- Integration with `skills-backup` for post-clone hygiene
- Support for private repos + authentication
- Smart .gitignore + large file handling

**End of smart-git-clone v1.0 — Intelligent when it matters. Simple when it doesn't.**