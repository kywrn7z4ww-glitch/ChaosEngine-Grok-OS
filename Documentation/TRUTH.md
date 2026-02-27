# TRUTH_Design.md

## Purpose
Lightweight consistency & truth-consistency checker.  
Compares statements, outputs, assumptions, or retrieved facts against known ground-truth sources or internal coherence rules.

One sentence:  
**The system's bullshit detector — flags contradictions, hallucinations, or unsupported claims before they propagate.**

## Why it exists
LLM-style generation frequently produces plausible-sounding but factually wrong or internally inconsistent output.  
TRUTH.py exists to catch that early — especially in long sessions where context drifts or agents start agreeing on wrong premises.

## General idea of what it does
- Receives candidate output / claim / retrieved snippet  
- Cross-checks against:  
  - pinned / indexed ground-truth documents  
  - previous turns' agreed facts (via lattice memory)  
  - internal rule set (e.g. "cannot contradict HIVE_PHILOSOPHY v1.3")  
  - basic coherence heuristics (self-contradiction, impossible timelines, logical fallacies)  
- Returns pass/fail + explanation delta (what's wrong, confidence score)  
- Does **not** auto-correct — only flags and suggests revision

## Interactions (high-level)
- Called by ChaosEngine before final output routing  
- Pulls from lattice memory / pinned docs / index  
- Can be triggered by SYSTEM_CRITIC or THE_QUESTIONER  
- Feeds back to output layer (warning emoji / minimap shift on fail)

## Key invariants
- No generative capability — pure checking  
- No side-effects on pass  
- Always produces structured feedback (pass/fail + reason)  
- Lightweight — fast enough to run on every major response  
- Configurable thresholds (strict vs lenient mode)

Subject to change / replacement / tuning.  
No tie to overarching philosophy — pure verification utility.

Last sketched: 2026-02-27
Status: high-level design — abstract & flexible
