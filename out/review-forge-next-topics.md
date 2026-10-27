# Peer Review — Agent Brief Forge NEXT_TOPICS

- **Draft id:** `forge-next-topics`
- **Source:** seed:forge-next-topics
- **Kind:** `forge_pack`
- **Reviewed at:** 2026-10-27T00:38:34-04:00 (America/New_York box clock)
- **Stats:** 14 lines · 267 words · 0 urls
- **Chair verdict:** **hold** (risk=29, adjusted=29)

Chair merges 10 findings from 5 personas → verdict=hold, must-fix=2, nice-to-haves=8, disagreements=1.

## Must-fix before ship

### [HIGH] run.sh + smoke_test.sh are the contract — brief ≥200 lines and ≥5 citations
- **Persona:** operator · **id:** `ope-fd8f91cfc0`
- **Evidence:** ./smoke_test.sh  # health + brief ≥200 lines
- **Fix:** CI-less burn: always run smoke after regenerating brief-001.

### [HIGH] Local-only bind 127.0.0.1:4330 — good; no firm/client topics in NEXT_TOPICS
- **Persona:** security · **id:** `sec-3670baf615`
- **Evidence:** h sports logistics. Not collections / law firm.  1. **Grok Bot fleet token-pool discipline** — When weekly Grok Bot burn vs Cursor Model
- **Fix:** Keep topic filter in POST /api/topics; reject kpdlawgroup-shaped strings.

## Nice-to-haves

- **[medium]** pkill by script path can race if two forges start together — _Prefer PORT env + flock or health-check before pkill in future._ (`ope-3bf5dda823`)
- **[medium]** Hold/Apply brief topic maps cleanly onto Bonsai + Draft Day adjacency — _Cross-link Arena reviews of Bonsai reveal ↔ Forge brief in burn notes._ (`pro-88b2a58e65`)
- **[medium]** POST /api/topics appends without rate limit — fine for local burn, not public — _Document local-only; never expose beyond loopback._ (`sec-c4feab30d1`)
- **[medium]** Seed brief claims live WebSearch/WebFetch citations — peer must spot-check URLs still resolve — _Smoke should assert ≥5 unique http citations and sample-fetch 2 URLs._ (`ske-fff1fc6a04`)
- **[medium]** 2-minute how-to is crisp; home should surface brief line count + citation count — _Dashboard hero: lines / citations / peer-review verdict at a glance._ (`ux_-872fce1d89`)
- **[low]** NEXT_TOPICS intentionally skip law firm — aligns with burn rules — _Keep exclusion list in DESIGN when topics regenerate._ (`pro-8097af8ef2`)
- **[low]** Pipeline stages are simulated peer review, not a live multi-model debate — _Label UI as 'simulated stages' so Boyd doesn't expect live LLM round-trips._ (`ske-669d1f4015`)
- **[low]** Ten NEXT_TOPICS are heavy follow-ups — good burn fuel, dense for a first glance — _UI: show top 3 topics + '7 more' expander._ (`ux_-721ac9dbca`)

## Consensus table

| Topic | Worst | Personas | Headline |
|---|---|---|---|
| `scope` | high | 2 (product, security) | Local-only bind 127.0.0.1:4330 — good; no firm/client topics in NEXT_TOPICS |
| `smoke` | high | 1 (operator) | run.sh + smoke_test.sh are the contract — brief ≥200 lines and ≥5 citations |
| `citations` | medium | 1 (skeptic) | Seed brief claims live WebSearch/WebFetch citations — peer must spot-check URLs still resolve |
| `exposure` | medium | 1 (security) | POST /api/topics appends without rate limit — fine for local burn, not public |
| `dashboard` | medium | 1 (ux_delight) | 2-minute how-to is crisp; home should surface brief line count + citation count |
| `ports` | medium | 1 (operator) | pkill by script path can race if two forges start together |
| `fleet_fit` | medium | 1 (product) | Hold/Apply brief topic maps cleanly onto Bonsai + Draft Day adjacency |
| `honesty` | low | 1 (skeptic) | Pipeline stages are simulated peer review, not a live multi-model debate |
| `density` | low | 1 (ux_delight) | Ten NEXT_TOPICS are heavy follow-ups — good burn fuel, dense for a first glance |

## Disagreements

- **scope**: Personas disagree on urgency for 'scope': high, low

## Per-persona scoreboard

| Persona | Findings | Blocker | High | Med | Low | Nit | Risk |
|---|---:|---:|---:|---:|---:|---:|---:|
| Skeptic | 2 | 0 | 0 | 1 | 1 | 0 | 5 |
| Security | 2 | 0 | 1 | 1 | 0 | 0 | 7 |
| UX Delight | 2 | 0 | 0 | 1 | 1 | 0 | 5 |
| Operator / On-call | 2 | 0 | 1 | 1 | 0 | 0 | 7 |
| Product Strategist | 2 | 0 | 0 | 1 | 1 | 0 | 5 |

## Full findings by persona

### Skeptic — Adversarial truth-seeker

_Skeptic filed 2 finding(s) via Overclaims, missing evidence, demo theater vs product truth, honesty gaps._

#### [medium] Seed brief claims live WebSearch/WebFetch citations — peer must spot-check URLs still resolve
- **Topic:** `citations` · **id:** `ske-fff1fc6a04`
- **Evidence:** Research for brief-001 was fetched live
- **Suggested fix:** Smoke should assert ≥5 unique http citations and sample-fetch 2 URLs.

#### [low] Pipeline stages are simulated peer review, not a live multi-model debate
- **Topic:** `honesty` · **id:** `ske-669d1f4015`
- **Evidence:** searcher → synthesizer → simulated peer reviewer
- **Suggested fix:** Label UI as 'simulated stages' so Boyd doesn't expect live LLM round-trips.

### Security — Blast-radius & trust boundary reviewer

_Security filed 2 finding(s) via Irreversible actions, synthetic vs real data, path guards, publish/send gates._

#### [high] Local-only bind 127.0.0.1:4330 — good; no firm/client topics in NEXT_TOPICS
- **Topic:** `scope` · **id:** `sec-3670baf615`
- **Evidence:** h sports logistics. Not collections / law firm.  1. **Grok Bot fleet token-pool discipline** — When weekly Grok Bot burn vs Cursor Model
- **Suggested fix:** Keep topic filter in POST /api/topics; reject kpdlawgroup-shaped strings.

#### [medium] POST /api/topics appends without rate limit — fine for local burn, not public
- **Topic:** `exposure` · **id:** `sec-c4feab30d1`
- **Evidence:** use Run next topic to append
- **Suggested fix:** Document local-only; never expose beyond loopback.

### UX Delight — Operator experience & reveal polish

_UX Delight filed 2 finding(s) via Cognitive load, spoken-script length, demo friction, glossary clarity, delight._

#### [medium] 2-minute how-to is crisp; home should surface brief line count + citation count
- **Topic:** `dashboard` · **id:** `ux_-872fce1d89`
- **Evidence:** ## 2-minute how-to
- **Suggested fix:** Dashboard hero: lines / citations / peer-review verdict at a glance.

#### [low] Ten NEXT_TOPICS are heavy follow-ups — good burn fuel, dense for a first glance
- **Topic:** `density` · **id:** `ux_-721ac9dbca`
- **Evidence:** s / law firm.  1. **Grok Bot fleet token-pool discipline** — When weekly Grok Bot burn vs Cursor Models diverge: metering, routine unde
- **Suggested fix:** UI: show top 3 topics + '7 more' expander.

### Operator / On-call — Day-2 operability

_Operator / On-call filed 2 finding(s) via Runbooks, ports, reset/recover, failure modes, preflight checklists._

#### [high] run.sh + smoke_test.sh are the contract — brief ≥200 lines and ≥5 citations
- **Topic:** `smoke` · **id:** `ope-fd8f91cfc0`
- **Evidence:** ./smoke_test.sh  # health + brief ≥200 lines
- **Suggested fix:** CI-less burn: always run smoke after regenerating brief-001.

#### [medium] pkill by script path can race if two forges start together
- **Topic:** `ports` · **id:** `ope-3bf5dda823`
- **Evidence:** starts http://127.0.0.1:4330/
- **Suggested fix:** Prefer PORT env + flock or health-check before pkill in future.

### Product Strategist — Fit & narrative ownership

_Product Strategist filed 2 finding(s) via Why this exists for Boyd, bookmark lineage, fleet placement, next-ask clarity._

#### [medium] Hold/Apply brief topic maps cleanly onto Bonsai + Draft Day adjacency
- **Topic:** `fleet_fit` · **id:** `pro-88b2a58e65`
- **Evidence:** Hold vs Apply, CAS, verification gates
- **Suggested fix:** Cross-link Arena reviews of Bonsai reveal ↔ Forge brief in burn notes.

#### [low] NEXT_TOPICS intentionally skip law firm — aligns with burn rules
- **Topic:** `scope` · **id:** `pro-8097af8ef2`
- **Evidence:** h sports logistics. Not collections / law firm.  1. **Grok Bot fleet token-pool discipline** — When weekly Grok Bot burn vs Cursor Model
- **Suggested fix:** Keep exclusion list in DESIGN when topics regenerate.

---
_Generated by Peer Review Arena (TokenMax / Grok Bot weekly burn)._
