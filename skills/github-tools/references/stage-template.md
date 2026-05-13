# STAGE.md — v4.4 Contract Format (Self-Consistent Edition)

**library_version**: v4.4-dynamic
**generated_at**: [AUTO-POPULATED]
**active_repo**: kywrn7z4ww-glitch/ChaosEngine-Grok-OS
**working_branch**: skills-prototype
**read_only_branch**: main

**Self-Consistency Rubric Score** (must be 5/5 or document is invalid):
1. Tool Mapping: [Yes/No]
2. Parameter Completeness: [Yes/No]
3. Rollback Path: [Yes/No]
4. Future-Proofing: [Yes/No]
5. Zero-Context Execution: [Yes/No]

**Justification** (required if any "No"): [ ]

**Connector Library Compliance Declaration**:
This document was generated while strictly following the v4.4 Connector Library and 5-question rubric. All actions use only discoverable `github___*` tools. No curl. No external assumptions.

**Current Session**:
[Auto summary]

## Completed (Pushed via Connectors)
- [Item] — verified with get_file_contents + secret scan

## Staged (Local Ready for Push)
- [File] — will use create_or_update_file with SHA from get_file_contents

## Next Actions
1. Push using exact connector call from library
2. Run validate-stage after changes
3. self-update-stage with library hash

**Migration Notes**: v4.4 format. Run `github-tools migrate-stage` on older files.

**All changes ready for targeted connector push.**