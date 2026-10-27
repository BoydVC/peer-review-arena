# Agent Brief Forge

Local web app that runs a multi-stage research pipeline (**searcher → synthesizer → simulated peer reviewer → citation checker**) and serves long cited briefs on practical agent-tooling questions. Inspired by agentusecases.ai-style “produce cited research briefs with simulated peer review.”

Seed brief: **How to make agent apply/revert safe** (Hold vs Apply, CAS, verification gates, pstack `/correct`).

## 2-minute how-to

```bash
cd /workspace/tokenmax/agent-brief-forge
./run.sh                 # starts http://127.0.0.1:4330/
./smoke_test.sh          # health + brief ≥200 lines + ≥5 http citations
```

Open the UI, skim pipeline stages / brief / citations / peer-review findings, then use **Run next topic** to append to `data/topics.json`.

## Layout

| Path | What |
|------|------|
| `server.py` | stdlib `ThreadingHTTPServer` on `127.0.0.1:4330` |
| `static/` | home UI |
| `data/pipeline.json` | stage statuses + current brief pointer |
| `data/topics.json` | queued + completed topics |
| `out/brief-001.md` | seed brief (≥200 lines, real URLs) |
| `out/peer-review-001.json` | simulated peer review |
| `out/citations-001.json` | citation checker output |
| `NEXT_TOPICS.md` | 10 heavy follow-up topics |
| `smoke_test.sh` | automated smoke |

## API

- `GET /api/health`
- `GET /api/pipeline`
- `GET /api/brief` · `GET /api/brief/raw`
- `GET /api/citations` · `GET /api/peer-review`
- `GET/POST /api/topics`

## Notes

- Python 3 stdlib only (no pip deps).
- Research for brief-001 was fetched live in the forge session (WebSearch/WebFetch).
- Screenshots land in `screenshots/` when Chrome headless is available.
