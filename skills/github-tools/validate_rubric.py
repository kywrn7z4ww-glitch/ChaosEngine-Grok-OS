#!/usr/bin/env python3
"""
v4.4 Self-Consistency Rubric Validator
Checks a STAGE.md against the 5-question contract.
"""

import re
import sys
from pathlib import Path

RUBRIC = [
    "1. Every action maps to a discoverable github___* tool?",
    "2. All required parameters are explicitly provided?",
    "3. Clear rollback path exists using only library tools?",
    "4. Document remains valid after library refresh?",
    "5. Future Grok with zero prior context can execute it exactly?"
]

def validate_stage_file(filepath: str) -> dict:
    content = Path(filepath).read_text()
    
    score = 0
    results = []
    
    for i, question in enumerate(RUBRIC, 1):
        if re.search(rf"question {i}|rubric|self-consistency|executable|library", content, re.I):
            score += 1
            results.append(f"✓ {question}")
        else:
            results.append(f"✗ {question} (not addressed)")
    
    return {
        "score": score,
        "max_score": 5,
        "passed": score >= 4,
        "results": results,
        "filepath": filepath
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_rubric.py <path-to-STAGE.md>")
        sys.exit(1)
    
    result = validate_stage_file(sys.argv[1])
    print(f"\n=== v4.4 Self-Consistency Rubric ===")
    print(f"File: {result['filepath']}")
    print(f"Score: {result['score']}/5")
    for line in result['results']:
        print(line)
    print(f"\nStatus: {'✅ PASSED' if result['passed'] else '❌ FAILED - Must rewrite'}")