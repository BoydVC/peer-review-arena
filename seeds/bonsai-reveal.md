# Bonsai — reveal draft (DRAFT ONLY, not sent)

Target send: Thu Oct 29, 2026 ~5 PM ET (before the ~7:42 PM ET weekly reset).
Updated Mon Oct 26 ~9:35 PM ET for pass 11 @ e41f0d6 (agent bc-15e97a35). Numbers and attachments below match `/workspace/tokenmax/bonsai/STATUS.md` and `artifacts/MANIFEST.json` / `NOTES.md`. Re-check only if a newer Origin SHA lands before Thursday.

---

## The message (draft) — tightened script (<90s spoken)

**Bonsai: the mistakes your agents keep making, pruned into structure**

Bonsai is the poteto idea from your bookmarks: stop micromanaging agents — encode the mistakes they keep making into the environment.

It ingests a pile of synthetic agent mistakes, clusters the repeats, and for each cluster proposes the highest fix that works: type, then test, then lint, then prose. **Hold** adds the guard. **Apply** rewrites the smell in a sandbox playground — with dry-run, undo, and history. The dashboard is a bonsai: biting clusters are branches; every hold prunes.

**Why it's yours**
- Straight out of your bookmarks: poteto's `/correct` and bonsai post, the trust-layer pyramid (codebase → static analysis → prose → human review), and pstack's verify / blast-radius ideas.
- Built to sit next to Draft Day: Draft Day builds things; Bonsai keeps the next build from repeating the last one's mistakes.
- **No firm code, no client data.** Everything is a synthetic payments playground and every screen says SYNTHETIC.

**Numbers (pass 11 @ e41f0d6):** 60 synthetic mistakes → 12 clusters; "apply all" ends **11 held / 1 biting**; **155** tests; **28**-check verify; **7** adversarial checks; lint clean. Hold / Apply (dry-run) / Apply (write) / Revert labels + header glossary.

**What's honest about it:** Today the demo corpus is a fixed catalog of 12 mistake types (the planted repeats). Some detectors may still be thinner than a full `/correct` loop (discovery from raw history, lint holds wired into ESLint, baseline-hash Apply). The product ships dry-run, revert, blast-radius path guards, and a real verify skill — and it does not pretend the loop is finished. Nothing merges, deploys, or publishes without your OK.

**Where it lives:** private Cursor Origin draft `boydvc/tmp-6e67f983fcd2585c` @ e41f0d6. Want it moved to a private **BoydVC/bonsai** repo like your other projects? Say the word after the reveal.

---

## Two-minute how-to (operator checklist)

Exact path for the live demo. Prefer a clean shell; nothing else on port 4317.

### Preflight (about 5 minutes before)
1. From the Bonsai repo root: `npm test` — green.
2. `npm run verify` — green (28 checks).
3. `npm run adversarial` (alias: `interrogate` if still present) — green.
4. Skim `artifacts/MANIFEST.json` so attachments match this build.

### Demo path
1. **`npm run demo:reset`** — clean tree, all 12 clusters biting. If a confirm dialog appears, accept it. Do **not** click Reset again mid-talk.
2. **`npm run serve --prod`** (or the README-equivalent prod flag: `next build` + `next start` via the CLI). Open http://127.0.0.1:4317 — you should **not** see the Next.js dev "N" badge.
3. Second terminal: **`npm run demo:story`** — ingests, holds, applies (includes flaky-date). When it exits, reload once if the tree has not live-refreshed.
4. Open **http://127.0.0.1:4317/?cluster=flaky-date-parse** — evidence, ranked encodings (type beats test beats lint beats prose), before/after diff. Say out loud: *Hold = add the guard. Apply = rewrite the smell. Revert = undo.*
5. Optional: **`npm run demo:apply-all`** — tree almost fully pruned (**11 held / 1 biting**). Point at the remaining biter as honesty, not failure.
6. Trust-but-verify line: `npm test`, `npm run verify`, `npm run adversarial` — synthetic playground only.

`Reset tree` in the UI wipes demo state. Prefer the CLI reset before the talk; avoid the button while presenting.

---

## Spoken script (copy into notes; ~75–85 seconds)

> Bonsai is the poteto idea from your bookmarks: stop micromanaging agents — encode the mistakes they keep making into the environment.
>
> It ingests a pile of synthetic agent mistakes, clusters the repeats, and for each cluster proposes the highest fix that works: type, then test, then lint, then prose. Hold adds the guard. Apply rewrites the smell in a sandbox playground — dry-run, undo, history. The dashboard is a bonsai: biting clusters are branches; every hold prunes.
>
> Why it's yours: straight from `/correct` and the trust pyramid you saved, built to sit next to Draft Day. No firm code, no client data — every screen says SYNTHETIC.
>
> Numbers on this build: sixty mistakes, twelve clusters; apply-all ends eleven held, one biting; one-fifty-five tests; verify twenty-eight; seven adversarial checks.
>
> Two minutes on your machine: reset, serve prod, run the story, open the flaky-date cluster. Watch a branch prune. Nothing merges or deploys without you.

---

## Attachments

**Attach (pass 11, prod capture):**
| File | Why |
|---|---|
| `/workspace/tokenmax/bonsai/artifacts/home-story.png` | Hero after story — cluster selected, Encode visible |
| `/workspace/tokenmax/bonsai/artifacts/home-apply-all.png` | Pruned tree, 11 held / 1 biting |
| `/workspace/tokenmax/bonsai/artifacts/home-eval.png` | Eval / verdict view |
| `/workspace/tokenmax/bonsai/artifacts/demo-story.webm` | ~30 s motion clip ending 11 held / 1 biting (silent) |

**Optional:** `home-history.png` only if it clearly shows newest history first and differs from apply-all.

**Do NOT attach:** anything under `artifacts/old/`, or any 48-mistakes / 10-cluster era shots.

**Capture notes (from NOTES.md):** `bonsai serve --prod` at http://127.0.0.1:4317; no Next dev badge; clocks are corpus time in Eastern Time; playground smells intentional; SYNTHETIC everywhere.

---

## Pre-send checklist (Thu, before ~5 PM ET)
- [ ] STATUS.md SHA still e41f0d6 (or update numbers if a newer pass landed).
- [ ] Attachments re-checked against `artifacts/MANIFEST.json`.
- [ ] Honesty line still matches what the code actually does (catalog vs discovery; Apply safety).
- [ ] "Where it lives" still Origin draft — do not publish or move without Boyd's OK.
- [ ] Parent sends via the approved channel only; this file is a draft. **Do not send from a burn/subagent session.**
