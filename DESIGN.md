# DESIGN.md — Peer Review Arena

## Spark

Jim · Interests burn snapshot + Boyd bookmarks on multi-agent peer review / @EXM7777-shaped critique loops. Runner-up build: **multi-agent critique loop before merge**.

## Job to be done

Before a reveal, PR description, or agent plan ships, fan out **independent reviewer personas**, collect structured findings, and let a **Chair** produce:

1. Consensus table (by topic)
2. Disagreements (severity spreads)
3. Must-fix-before-ship list
4. A triage verdict (`ship_ready` → `hold`)

## Personas (fixed cast of 5)

| Id | Name | Lens |
|---|---|---|
| `skeptic` | Skeptic | Overclaims, honesty gaps, demo theater |
| `security` | Security | Send/publish gates, SYNTHETIC boundary, blast radius |
| `ux_delight` | UX Delight | Script length, demo friction, glossary |
| `operator` | Operator / On-call | Ports, preflight, failure modes |
| `product` | Product Strategist | Bookmark lineage, CTA, fleet fit |

## Finding schema

```json
{
  "id": "ske-…",
  "persona_id": "skeptic",
  "severity": "blocker|high|medium|low|nit",
  "claim": "…",
  "evidence": "quote or path from draft",
  "suggested_fix": "…",
  "topic": "send_gate"
}
```

## Chair rules

- Independent first pass (no mid-review score sharing).
- Risk = sum of severity weights; nits lightly discounted for verdict.
- Must-fix = all `blocker` + `high`.
- Disagreement = topic with ≥2 personas and ≥2 distinct severities.
- Chair never auto-sends or auto-merges.

## Seeds

1. **Bonsai REVEAL_DRAFT** (primary) → `out/review-bonsai-reveal.{json,md}`
2. **Agent Brief Forge README** / **NEXT_TOPICS** (second option)
3. **Brief-007 Pre-Ops / Workflow-Audit Gates** → `out/review-brief-007.{json,md}`

## Non-goals (v1)

- Live multi-round LLM debate
- Cursor cloud agents / on-demand
- kpdlawgroup or client drafts
- Messaging Boyd from this app

## Stack

Python 3 stdlib only · `ThreadingHTTPServer` · `127.0.0.1:4333` · static UI
