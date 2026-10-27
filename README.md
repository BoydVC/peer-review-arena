# Peer Review Arena

Local web app: **3–5 reviewer personas** critique a draft (spec, PR description, or agent plan), then a **Chair** merges findings into a consensus scorecard with disagreements and a must-fix-before-ship list.

Inspired by multi-subagent review patterns and Jim’s “critique loop before merge” runner-up. TokenMax / Grok Bot weekly burn — not Cursor Models.

## 2-minute how-to

```bash
cd /workspace/tokenmax/peer-review-arena
./run.sh                 # rebuilds seeds + serves http://127.0.0.1:4333/
./smoke_test.sh          # artifacts + health + live POST /api/review
```

Open the UI → **Load Bonsai reveal** / **Load Brief-007 pre-ops** (or paste a draft) → **Run review**. Chair panel shows verdict, must-fix, consensus table, disagreements. Full transcript saves under `out/`.

**Brief-024 fold:** portable `/correct` CI law panel (`Brief-024 law · /correct CI`) with scorecard `auto_merge=0` / `docs_only_lessons=0`, alongside the existing brief-007 pre-ops seed. `GET /api/brief024` + `live_check`; POST `/api/auto-merge`, `/api/force-merge`, `/api/bypass-correct-ci` → **403**. Never merge without Boyd OK.

**Brief-027 fold:** portable Grok Council law panel (`Brief-027 law · Grok Council`) with scorecard `auto_apply_council=0` / `auto_send=0`, alongside brief-007 + brief-024. `GET /api/brief027` + `live_check`; POST `/api/auto-apply`, `/api/auto-apply-council`, `/api/council-force-send` → **403**. Council Hold until human Apply; never majority-vote auto-apply. Pairs brief-008 + brief-017.

## Layout

| Path | What |
|------|------|
| `server.py` | stdlib server on `127.0.0.1:4333` |
| `engine/` | personas, review, chair, markdown render |
| `seeds/` | bonsai reveal + forge README / NEXT_TOPICS |
| `out/review-bonsai-reveal.json` | primary multi-review transcript |
| `out/review-bonsai-reveal.md` | readable chair report |
| `out/review-brief-007.{json,md}` | Arena pass on Forge brief-007 (pre-ops / workflow-audit) |
| `data/brief024.json` | Folded `/correct` CI law + scorecard zeros (brief-024) |
| `data/peer-review-024.json` | Forge peer review for brief-024 |
| `data/brief027.json` | Folded Grok Council law + scorecard zeros (brief-027) |
| `data/peer-review-027.json` | Forge peer review for brief-027 |
| `static/` | draft + chair UI + Brief-024 / Brief-027 law panels |
| `RESEARCH.md` | cited multi-agent / LLM-as-judge desk |
| `DESIGN.md` | product rules |
| `smoke_test.sh` | automated smoke |

## API

- `GET /api/health`
- `GET /api/personas` · `GET /api/seeds` · `GET /api/seeds/:id/raw`
- `GET /api/reviews` · `GET /api/reviews/:file`
- `POST /api/review` — `{ "seed_id" }` or `{ "draft", "title" }`; optional `stem`, `save`
- `GET /api/brief024` — `/correct` CI law + `live_check` (paired with brief-007 / brief-012)
- `POST /api/auto-merge` · `/api/force-merge` · `/api/bypass-correct-ci` → **403** (`auto_merge=0`)

## Notes

- Python 3 stdlib only (no pip deps).
- Seed critiques are deterministic + evidence-quoting so burns replay cleanly.
- RESEARCH.md cites Du et al., ChatDev, MetaGPT, adversarial persuasion, role-asymmetry MAD, Zheng MT-Bench, Many-Minds bias.
- Brief-024 encodes pstack `/correct` ladder (arch→types→lint/CI→tests→docs); docs_only_lessons=0; America/New_York; no KPD; no burn merge/outbound.
- Brief-027 encodes Grok Council desk (digest→seats→refute→recommend→Hold→human Apply); auto_apply_council=0 / auto_send=0; America/New_York; no KPD; no burn outbound.
