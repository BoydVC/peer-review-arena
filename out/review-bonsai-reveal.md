# Peer Review — Bonsai REVEAL_DRAFT

- **Draft id:** `bonsai-reveal`
- **Source:** seed:bonsai-reveal
- **Kind:** `bonsai_reveal`
- **Reviewed at:** 2026-10-27T00:38:33-04:00 (America/New_York box clock)
- **Stats:** 88 lines · 978 words · 3 urls
- **Chair verdict:** **hold** (risk=55, adjusted=53)

Chair merges 19 findings from 5 personas → verdict=hold, must-fix=6, nice-to-haves=11, disagreements=1.

## Must-fix before ship

### [BLOCKER] Draft must never be sent from a burn/subagent session
- **Persona:** security · **id:** `sec-6b9c68abb0`
- **Evidence:** file is a draft. **Do not send from a burn/subagent session.**
- **Fix:** Enforce send-on-behalf Hold: only parent channel after Boyd OK; burn agents produce drafts only.

### [HIGH] Port 4317 must be free; Next.js 'N' badge means wrong serve mode
- **Persona:** operator · **id:** `ope-bc1a341e91`
- **Evidence:** e CLI). Open http://127.0.0.1:4317 — you should **not** see the Next.js dev "N" badge. 3. Second terminal: **`npm run demo:s
- **Fix:** Preflight: lsof/curl 4317; abort if badge present; use serve --prod only.

### [HIGH] Three green gates required: test, verify (28), adversarial (7)
- **Persona:** operator · **id:** `ope-fb746d3cf1`
- **Evidence:** test` — green. 2. `npm run verify` — green (28 checks). 3. `npm run adversarial` (alias: `interrogate` if still present) —
- **Fix:** Run all three ~5 min before talk; paste exit codes into a sticky note.

### [HIGH] Repo is still a private Origin draft — reveal must not imply public publish
- **Persona:** security · **id:** `sec-eeeaee22e3`
- **Evidence:** ursor Origin draft `boydvc/tmp-6e67f983fcd2585c` @ e41f0d6. Want it moved to a private **BoydVC/bonsai** repo like your other projects? S
- **Fix:** Keep 'Where it lives' as Origin draft; require explicit OK before BoydVC/bonsai move.

### [HIGH] Pass-11 numbers may drift before Thursday send if Origin SHA moves
- **Persona:** skeptic · **id:** `ske-d1497f1409`
- **Evidence:** 26 ~9:35 PM ET for pass 11 @ e41f0d6 (agent bc-15e97a35). Numbers and attachments below match `/workspace/tokenmax/bonsai/STAT
- **Fix:** Bind the send checklist to STATUS.md SHA; if SHA ≠ e41f0d6, regenerate numbers + attachments before send.

### [HIGH] Demo path has six steps + optional apply-all — mid-talk Reset is a known footgun
- **Persona:** ux_delight · **id:** `ux_-fcd62d1690`
- **Evidence:** Do not click Reset again mid-talk
- **Fix:** Put a sticky 'NO RESET' note on the demo machine; prefer CLI demo:reset only in preflight.

## Nice-to-haves

- **[medium]** demo:story may need a single reload if tree does not live-refresh — _Script the reload as step 3b so it doesn't look like a hang on stage._ (`ope-7378a523f2`)
- **[medium]** Bookmark lineage (/correct, trust pyramid, Draft Day adjacency) is the ownership hook — _Lead with 'why it's yours' before numbers so the reveal isn't a feature dump._ (`pro-659dd58f41`)
- **[medium]** SYNTHETIC playground claim is strong — verify every attached screenshot still shows the badge — _Attachment preflight: open each PNG/webm and confirm SYNTHETIC chrome before send._ (`sec-805780a9fe`)
- **[medium]** Honesty line admits catalog-vs-discovery gap but spoken script may oversell 'ingests a pile' — _Keep the spoken line 'synthetic mistakes' and add one beat: 'twelve planted types, not live history discovery yet.'_ (`ske-327e7a5ade`)
- **[medium]** Remaining '1 biting' after apply-all should be framed as honesty, not a broken demo — _Agree the spoken beat with Skeptic before Thursday; one shared line._ (`ux_-9f4bbbe4e5`)
- **[medium]** Spoken script targets 75–85s — good; two-minute how-to is operator, not spoken — _Copy only the spoken block into notes; keep operator checklist off-screen during the talk._ (`ux_-9cf2d41be9`)
- **[low]** Deep-link cluster query is brittle if cluster id renames — _Pin cluster id in STATUS.md; if renamed, update reveal draft same commit._ (`ope-90362a2759`)
- **[low]** Ask to move Origin draft → BoydVC/bonsai is a clear next CTA — _Keep CTA after honesty line; don't bury under attachments._ (`pro-1eb6a4df99`)
- **[low]** Blast-radius path guards mentioned but not demonstrated in the spoken path — _Optional 10s aside: point at path-guard in verify or adversarial output if time._ (`sec-da6fa18078`)
- **[low]** 'Apply-all ends 11 held / 1 biting' needs the remaining biter named in the talk — _Name the remaining biter aloud (honesty, not failure) so the audience doesn't invent a bug._ (`ske-17a2c18f98`)
- **[low]** Hold / Apply / Revert glossary is in header — say it once at flaky-date cluster — _Practice the three-word glossary aloud once; don't re-explain on every prune._ (`ux_-5e50cb7763`)

## Consensus table

| Topic | Worst | Personas | Headline |
|---|---|---|---|
| `send_gate` | blocker | 1 (security) | Draft must never be sent from a burn/subagent session |
| `freshness` | high | 1 (skeptic) | Pass-11 numbers may drift before Thursday send if Origin SHA moves |
| `publish_boundary` | high | 1 (security) | Repo is still a private Origin draft — reveal must not imply public publish |
| `demo_friction` | high | 1 (ux_delight) | Demo path has six steps + optional apply-all — mid-talk Reset is a known footgun |
| `ports` | high | 1 (operator) | Port 4317 must be free; Next.js 'N' badge means wrong serve mode |
| `preflight` | high | 1 (operator) | Three green gates required: test, verify (28), adversarial (7) |
| `honesty` | medium | 2 (security, skeptic) | Honesty line admits catalog-vs-discovery gap but spoken script may oversell 'ingests a pile' |
| `demo_narrative` | medium | 2 (skeptic, ux_delight) | Remaining '1 biting' after apply-all should be framed as honesty, not a broken demo |
| `script_length` | medium | 1 (ux_delight) | Spoken script targets 75–85s — good; two-minute how-to is operator, not spoken |
| `failure_mode` | medium | 1 (operator) | demo:story may need a single reload if tree does not live-refresh |
| `narrative` | medium | 1 (product) | Bookmark lineage (/correct, trust pyramid, Draft Day adjacency) is the ownership hook |
| `verify` | low | 1 (security) | Blast-radius path guards mentioned but not demonstrated in the spoken path |
| `glossary` | low | 1 (ux_delight) | Hold / Apply / Revert glossary is in header — say it once at flaky-date cluster |
| `runbook` | low | 1 (operator) | Deep-link cluster query is brittle if cluster id renames |
| `cta` | low | 1 (product) | Ask to move Origin draft → BoydVC/bonsai is a clear next CTA |
| `attachments` | nit | 1 (ux_delight) | Attachment table includes webm — silent clip is reveal-friendly |
| `timing` | nit | 1 (product) | Target send Thu Oct 29 ~5 PM ET sits before ~7:42 PM reset — good pacing |

## Disagreements

- **demo_narrative**: Personas disagree on urgency for 'demo_narrative': medium, low

## Per-persona scoreboard

| Persona | Findings | Blocker | High | Med | Low | Nit | Risk |
|---|---:|---:|---:|---:|---:|---:|---:|
| Skeptic | 3 | 0 | 1 | 1 | 1 | 0 | 9 |
| Security | 4 | 1 | 1 | 1 | 1 | 0 | 14 |
| UX Delight | 5 | 0 | 1 | 2 | 1 | 1 | 13 |
| Operator / On-call | 4 | 0 | 2 | 1 | 1 | 0 | 13 |
| Product Strategist | 3 | 0 | 0 | 1 | 1 | 1 | 6 |

## Full findings by persona

### Skeptic — Adversarial truth-seeker

_Skeptic filed 3 finding(s) via Overclaims, missing evidence, demo theater vs product truth, honesty gaps._

#### [high] Pass-11 numbers may drift before Thursday send if Origin SHA moves
- **Topic:** `freshness` · **id:** `ske-d1497f1409`
- **Evidence:** 26 ~9:35 PM ET for pass 11 @ e41f0d6 (agent bc-15e97a35). Numbers and attachments below match `/workspace/tokenmax/bonsai/STAT
- **Suggested fix:** Bind the send checklist to STATUS.md SHA; if SHA ≠ e41f0d6, regenerate numbers + attachments before send.

#### [medium] Honesty line admits catalog-vs-discovery gap but spoken script may oversell 'ingests a pile'
- **Topic:** `honesty` · **id:** `ske-327e7a5ade`
- **Evidence:** he demo corpus is a fixed catalog of 12 mistake types (the planted repeats). Some detectors may still be thinner than a full `/correct` loop (d
- **Suggested fix:** Keep the spoken line 'synthetic mistakes' and add one beat: 'twelve planted types, not live history discovery yet.'

#### [low] 'Apply-all ends 11 held / 1 biting' needs the remaining biter named in the talk
- **Topic:** `demo_narrative` · **id:** `ske-17a2c18f98`
- **Evidence:** "apply all" ends **11 held / 1 biting**; **155** tests; **28**-check verify; **7** adversarial checks; lint clean. Hold / Apply
- **Suggested fix:** Name the remaining biter aloud (honesty, not failure) so the audience doesn't invent a bug.

### Security — Blast-radius & trust boundary reviewer

_Security filed 4 finding(s) via Irreversible actions, synthetic vs real data, path guards, publish/send gates._

#### [blocker] Draft must never be sent from a burn/subagent session
- **Topic:** `send_gate` · **id:** `sec-6b9c68abb0`
- **Evidence:** file is a draft. **Do not send from a burn/subagent session.**
- **Suggested fix:** Enforce send-on-behalf Hold: only parent channel after Boyd OK; burn agents produce drafts only.

#### [high] Repo is still a private Origin draft — reveal must not imply public publish
- **Topic:** `publish_boundary` · **id:** `sec-eeeaee22e3`
- **Evidence:** ursor Origin draft `boydvc/tmp-6e67f983fcd2585c` @ e41f0d6. Want it moved to a private **BoydVC/bonsai** repo like your other projects? S
- **Suggested fix:** Keep 'Where it lives' as Origin draft; require explicit OK before BoydVC/bonsai move.

#### [medium] SYNTHETIC playground claim is strong — verify every attached screenshot still shows the badge
- **Topic:** `honesty` · **id:** `sec-805780a9fe`
- **Evidence:** ents playground and every screen says SYNTHETIC.  **Numbers (pass 11 @ e41f0d6):** 60 synthetic mistakes → 12 clusters; "apply all" ends
- **Suggested fix:** Attachment preflight: open each PNG/webm and confirm SYNTHETIC chrome before send.

#### [low] Blast-radius path guards mentioned but not demonstrated in the spoken path
- **Topic:** `verify` · **id:** `sec-da6fa18078`
- **Evidence:** d pstack's verify / blast-radius ideas. - Built to sit next to Draft Day: Draft Day builds things; Bonsai keeps the next b
- **Suggested fix:** Optional 10s aside: point at path-guard in verify or adversarial output if time.

### UX Delight — Operator experience & reveal polish

_UX Delight filed 5 finding(s) via Cognitive load, spoken-script length, demo friction, glossary clarity, delight._

#### [medium] Remaining '1 biting' after apply-all should be framed as honesty, not a broken demo
- **Topic:** `demo_narrative` · **id:** `ux_-9f4bbbe4e5`
- **Evidence:** ng**). Point at the remaining biter as honesty, not failure. 6. Trust-but-verify line: `npm test`, `npm run verify`, `npm run adversaria
- **Suggested fix:** Agree the spoken beat with Skeptic before Thursday; one shared line.

#### [medium] Spoken script targets 75–85s — good; two-minute how-to is operator, not spoken
- **Topic:** `script_length` · **id:** `ux_-9cf2d41be9`
- **Evidence:** t (copy into notes; ~75–85 seconds)  > Bonsai is the poteto idea from your bookmarks: stop micromanaging agents — encode the
- **Suggested fix:** Copy only the spoken block into notes; keep operator checklist off-screen during the talk.

#### [high] Demo path has six steps + optional apply-all — mid-talk Reset is a known footgun
- **Topic:** `demo_friction` · **id:** `ux_-fcd62d1690`
- **Evidence:** Do not click Reset again mid-talk
- **Suggested fix:** Put a sticky 'NO RESET' note on the demo machine; prefer CLI demo:reset only in preflight.

#### [low] Hold / Apply / Revert glossary is in header — say it once at flaky-date cluster
- **Topic:** `glossary` · **id:** `ux_-5e50cb7763`
- **Evidence:** iff. Say out loud: *Hold = add the guard. Apply = rewrite the smell. Revert = undo.* 5. Optional: **`npm run demo:apply-all`** — t
- **Suggested fix:** Practice the three-word glossary aloud once; don't re-explain on every prune.

#### [nit] Attachment table includes webm — silent clip is reveal-friendly
- **Topic:** `attachments` · **id:** `ux_-f343a9f987`
- **Evidence:** ax/bonsai/artifacts/demo-story.webm` | ~30 s motion clip ending 11 held / 1 biting (silent) |  **Optional:** `home-history.pn
- **Suggested fix:** Confirm autoplay/mute works in the reveal channel before Thursday.

### Operator / On-call — Day-2 operability

_Operator / On-call filed 4 finding(s) via Runbooks, ports, reset/recover, failure modes, preflight checklists._

#### [high] Port 4317 must be free; Next.js 'N' badge means wrong serve mode
- **Topic:** `ports` · **id:** `ope-bc1a341e91`
- **Evidence:** e CLI). Open http://127.0.0.1:4317 — you should **not** see the Next.js dev "N" badge. 3. Second terminal: **`npm run demo:s
- **Suggested fix:** Preflight: lsof/curl 4317; abort if badge present; use serve --prod only.

#### [high] Three green gates required: test, verify (28), adversarial (7)
- **Topic:** `preflight` · **id:** `ope-fb746d3cf1`
- **Evidence:** test` — green. 2. `npm run verify` — green (28 checks). 3. `npm run adversarial` (alias: `interrogate` if still present) —
- **Suggested fix:** Run all three ~5 min before talk; paste exit codes into a sticky note.

#### [medium] demo:story may need a single reload if tree does not live-refresh
- **Topic:** `failure_mode` · **id:** `ope-7378a523f2`
- **Evidence:** te). When it exits, reload once if the tree has not live-refreshed. 4. Open **http://127.0.0.1:4317/?cluster=flaky-date-p
- **Suggested fix:** Script the reload as step 3b so it doesn't look like a hang on stage.

#### [low] Deep-link cluster query is brittle if cluster id renames
- **Topic:** `runbook` · **id:** `ope-90362a2759`
- **Evidence:** p://127.0.0.1:4317/?cluster=flaky-date-parse** — evidence, ranked encodings (type beats test beats lint beats prose), before/after dif
- **Suggested fix:** Pin cluster id in STATUS.md; if renamed, update reveal draft same commit.

### Product Strategist — Fit & narrative ownership

_Product Strategist filed 3 finding(s) via Why this exists for Boyd, bookmark lineage, fleet placement, next-ask clarity._

#### [medium] Bookmark lineage (/correct, trust pyramid, Draft Day adjacency) is the ownership hook
- **Topic:** `narrative` · **id:** `pro-659dd58f41`
- **Evidence:** *Why it's yours** - Straight out of your bookmarks: poteto's `/correct` and bonsai post, the trust-layer pyramid (codebase → static analysis
- **Suggested fix:** Lead with 'why it's yours' before numbers so the reveal isn't a feature dump.

#### [low] Ask to move Origin draft → BoydVC/bonsai is a clear next CTA
- **Topic:** `cta` · **id:** `pro-1eb6a4df99`
- **Evidence:** oved to a private **BoydVC/bonsai** repo like your other projects? Say the word after the reveal.  ---  ## Two-minute how-t
- **Suggested fix:** Keep CTA after honesty line; don't bury under attachments.

#### [nit] Target send Thu Oct 29 ~5 PM ET sits before ~7:42 PM reset — good pacing
- **Topic:** `timing` · **id:** `pro-24bc45c839`
- **Evidence:** sent)  Target send: Thu Oct 29, 2026 ~5 PM ET (before the ~7:42 PM ET weekly reset). Updated Mon Oct 26 ~9:35 PM ET for
- **Suggested fix:** No change; confirm calendar block still clear.

---
_Generated by Peer Review Arena (TokenMax / Grok Bot weekly burn)._
