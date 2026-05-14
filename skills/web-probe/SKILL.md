---
name: web-probe
description: "General-purpose Deep Web Analysis & Probing Tool. Uses browse_page intelligently for rich data extraction, metadata analysis, structure mapping, and relationship discovery across any website. Trigger with: 'web probe', 'deep probe', 'analyze website', 'probe this url'. Use when you need deeper, structured analysis beyond normal browsing."
---

# Web Probe — Deep Web Analysis Engine

**Core Philosophy (Locked):**
**"Probe Deep. Extract Smart. Evolve Continuously."**

This skill is a general-purpose deep analysis tool for **any website**. It uses `browse_page` intelligently to extract not just content, but structure, metadata, relationships, and hidden patterns. It is designed to **discover and leverage novel ways** to use web browsing for better results over time.

**Two Probe Modes:**

| Mode          | Speed     | Depth          | Use Case |
|---------------|-----------|----------------|----------|
| **Fast Probe**    | Very Fast | Basic          | Quick overview, metadata, structure |
| **Deep Probe**    | Slower    | Full analysis  | Detailed extraction, relationships, patterns (**default**) |

**Non-Negotiable Rules:**
1. **General Purpose** — Works on any public website (not GitHub-specific).
2. **Smart Probing** — Never blindly scrape. Always analyze what is most valuable to extract based on user intent.
3. **Self-Improving** — Actively logs novel techniques and patterns discovered while using `browse_page`.
4. **Context & Intent First** — Uses `5w1h-translator` logic to understand why the user wants to probe.
5. **Respectful & Efficient** — Respects rate limits and avoids unnecessary requests.

---

**Execution Flow**

**Phase 0 — Intent & Context Excavation**
- Use 5W1H analysis to understand what the user wants to achieve.
- Determine optimal probing strategy.

**Phase 1 — Initial Probe**
- Browse the target URL(s)
- Extract: metadata, headings, links, structured data, main content, forms, etc.
- Identify high-value areas for deeper probing.

**Phase 2 — Deep Analysis**
- Recursively probe important sections
- Map relationships (internal links, data flows, hierarchies)
- Detect patterns and anomalies

**Phase 3 — Novel Technique Logging (Self-Improvement)**
- If a new or more effective way of using `browse_page` is discovered, log it.
- Examples: better pagination handling, smarter content extraction, novel metadata parsing, etc.
- These learnings can be reused in future probes.

**Phase 4 — Structured Output + Insights**
- Deliver rich, structured analysis
- Include actionable insights based on user intent

---

**Output Structure**

**Probe Summary**
- Target URL(s)
- Intent alignment
- Key findings

**Extracted Data**
- Metadata (title, description, Open Graph, etc.)
- Structure (headings, navigation, sections)
- Content highlights
- Relationships & links
- Forms & interactive elements

**Novel Techniques Discovered** (if any)
- New patterns or methods found during this probe

**Recommendations**
- Suggested next steps or deeper probes

---

**Self-Improvement Mechanism**

This skill maintains a small internal knowledge base of effective `browse_page` techniques. After every probe, it asks:
- "Did I discover a new useful pattern?"
- "Can this be reused in future probes?"
- "Should I update my prompting strategy?"

These learnings are logged and can be reviewed later.

**Trigger Phrases**
- web probe
- deep probe
- analyze website
- probe this url
- deep web analysis

This skill turns casual browsing into **structured intelligence**.

**End of web-probe v1.0 — Probe deep. Extract smart. Evolve continuously.**