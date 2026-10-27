#!/usr/bin/env bash
# Smoke: health, seeds, bonsai review artifacts, live review API
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
BASE="${BASE_URL:-http://127.0.0.1:4333}"
FAIL=0
PASS=0

ok() { echo "OK  $*"; PASS=$((PASS+1)); }
bad() { echo "FAIL $*"; FAIL=$((FAIL+1)); }

echo "== Peer Review Arena smoke =="

# Artifacts
JSON="$ROOT/out/review-bonsai-reveal.json"
MD="$ROOT/out/review-bonsai-reveal.md"
[[ -f "$JSON" ]] && ok "bonsai json exists" || bad "missing $JSON"
[[ -f "$MD" ]] && ok "bonsai md exists" || bad "missing $MD"

if [[ -f "$JSON" ]]; then
  python3 - "$JSON" <<'PY' && ok "bonsai json substantive" || bad "bonsai json thin"
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))
r,c=d["review"],d["chair"]
assert r["persona_count"]>=4, r["persona_count"]
assert r["finding_count"]>=12, r["finding_count"]
assert c["must_fix_before_ship"], "need must-fix"
assert c["consensus_table"], "need consensus"
assert len(open(sys.argv[1].replace(".json",".md"),encoding="utf-8").read().splitlines())>=40
print(f"personas={r['persona_count']} findings={r['finding_count']} must={c['counts']['must_fix']} verdict={c['verdict']}")
PY
fi

# Forge second seed
[[ -f "$ROOT/out/review-forge-readme.json" ]] && ok "forge-readme review" || bad "missing forge-readme review"

# Brief-007 pre-ops arena pass
B7="$ROOT/out/review-brief-007.json"
[[ -f "$B7" ]] && ok "brief-007 json exists" || bad "missing $B7"
[[ -f "$ROOT/out/review-brief-007.md" ]] && ok "brief-007 md exists" || bad "missing brief-007 md"
if [[ -f "$B7" ]]; then
  python3 - "$B7" <<'PYB7' && ok "brief-007 substantive" || bad "brief-007 thin"
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))
r,c=d["review"],d["chair"]
assert r["kind"]=="preops_brief", r["kind"]
assert r["persona_count"]>=4
assert r["finding_count"]>=12
assert c["must_fix_before_ship"], "need must-fix"
assert c.get("nice_to_haves"), "need nice-to-haves"
assert c["consensus_table"]
print(f"kind={r['kind']} findings={r['finding_count']} must={c['counts']['must_fix']} nice={c['counts'].get('nice_to_haves')} verdict={c['verdict']}")
PYB7
fi


health=$(curl -s -o /tmp/pra-health.json -w "%{http_code}" "$BASE/api/health" || echo "000")
[[ "$health" == "200" ]] && ok "health $(cat /tmp/pra-health.json)" || bad "health HTTP $health"

home=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/" || echo "000")
[[ "$home" == "200" ]] && ok "home" || bad "home HTTP $home"

seeds=$(curl -s -o /tmp/pra-seeds.json -w "%{http_code}" "$BASE/api/seeds" || echo "000")
[[ "$seeds" == "200" ]] && ok "seeds" || bad "seeds HTTP $seeds"

# Live API review of forge next topics
api=$(curl -s -o /tmp/pra-review.json -w "%{http_code}" \
  -H 'Content-Type: application/json' \
  -d '{"seed_id":"forge-next-topics","save":true,"stem":"review-forge-next-topics"}' \
  "$BASE/api/review" || echo "000")
if [[ "$api" == "200" ]]; then
  python3 - <<'PY' && ok "POST /api/review" || bad "POST review payload"
import json
d=json.load(open("/tmp/pra-review.json",encoding="utf-8"))
assert d.get("ok"), d
assert d["bundle"]["review"]["persona_count"]>=4
assert d["bundle"]["chair"]["consensus_table"]
print("verdict", d["bundle"]["chair"]["verdict"], "findings", d["bundle"]["review"]["finding_count"])
PY
else
  bad "POST /api/review HTTP $api"
fi

personas=$(curl -s "$BASE/api/personas" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert len(d["personas"])>=4; print(len(d["personas"]))')
[[ "$personas" -ge 4 ]] && ok "personas=$personas" || bad "personas"


# Brief-024 /correct CI law fold (alongside brief-007 pre-ops)
B24="$ROOT/data/brief024.json"
[[ -f "$B24" ]] && ok "data/brief024.json exists" || bad "missing $B24"
[[ -f "$ROOT/data/peer-review-024.json" ]] && ok "data/peer-review-024.json exists" || bad "missing peer-review-024"
if [[ -f "$B24" ]]; then
  python3 - "$B24" <<'PYB24' && ok "brief024 scorecard zeros" || bad "brief024 thin"
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))
assert d["brief_id"]=="brief-024"
sc=d["scorecard"]
assert sc["auto_merge"]==0 and sc["docs_only_lessons"]==0
assert sc["advisory_only_arch_job"]==0 and sc["burn_merge_or_send"]==0
assert sc["kpd_bleed"]==0 and sc["timezone"]=="America/New_York"
assert "/api/auto-merge" in d["refused_post_prefixes"]
assert "auto-merge" in d["denied_tools"]
assert d["encoding_ladder"][0].startswith("architecture")
assert d["encoding_ladder"][-1].startswith("docs")
print("ladder", " → ".join(d["encoding_ladder"]))
PYB24
fi

b24=$(curl -s -o /tmp/pra-brief024.json -w "%{http_code}" "$BASE/api/brief024" || echo "000")
[[ "$b24" == "200" ]] && ok "GET /api/brief024" || bad "GET /api/brief024 HTTP $b24"
if [[ "$b24" == "200" ]]; then
  python3 - <<'PYLC' && ok "brief024 live_check" || bad "brief024 live_check"
import json
b=json.load(open("/tmp/pra-brief024.json",encoding="utf-8"))
assert b["brief_id"]=="brief-024"
lc=b["live_check"]
assert lc["auto_merge"]==0 and lc["docs_only_lessons"]==0
assert lc["auto_merge_apis_succeed"] is False
assert lc["force_merge_apis_succeed"] is False
assert lc["bypass_correct_ci_apis_succeed"] is False
assert lc["mutation_endpoints_policy"]=="403"
assert lc["paired_with_brief007"] is True
assert lc["never_merge_without_boyd_ok"] is True
assert lc["timezone"]=="America/New_York"
assert "America/New_York" in lc["served_at_et"] or "EDT" in lc["served_at_et"] or "EST" in lc["served_at_et"]
print("served", lc["served_at_et"])
PYLC
fi

for ep in auto-merge force-merge bypass-correct-ci; do
  code=$(curl -s -o "/tmp/pra-$ep.json" -w "%{http_code}" \
    -X POST -H 'Content-Type: application/json' -d '{}' \
    "$BASE/api/$ep" || echo "000")
  [[ "$code" == "403" ]] && ok "POST /api/$ep 403" || bad "POST /api/$ep HTTP $code"
done
python3 - <<'PY403' && ok "403 cites brief-024" || bad "403 body"
import json
d=json.load(open("/tmp/pra-auto-merge.json",encoding="utf-8"))
assert d.get("brief_id")=="brief-024" or "brief-024" in d.get("error","")
assert d.get("ok") is False
print(d.get("error","")[:120])
PY403
code_get=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/api/auto-merge" || echo "000")
[[ "$code_get" == "403" ]] && ok "GET /api/auto-merge 403" || bad "GET /api/auto-merge HTTP $code_get"

home_html=$(curl -s "$BASE/" || true)
echo "$home_html" | grep -q 'Brief-024 law · /correct CI' && ok "UI Brief-024 law panel" || bad "UI missing Brief-024 panel"
grep -q 'renderBrief024' "$ROOT/static/app.js" && ok "app.js renderBrief024" || bad "missing renderBrief024"
grep -q 'brief007_preops' "$ROOT/server.py" && ok "brief-007 fold still wired" || bad "lost brief-007 flag"


# Brief-027 Grok Council law fold (alongside brief-007 / brief-024)
B27="$ROOT/data/brief027.json"
[[ -f "$B27" ]] && ok "data/brief027.json exists" || bad "missing $B27"
[[ -f "$ROOT/data/peer-review-027.json" ]] && ok "data/peer-review-027.json exists" || bad "missing peer-review-027"
if [[ -f "$B27" ]]; then
  python3 - "$B27" <<'PYB27' && ok "brief027 scorecard zeros" || bad "brief027 thin"
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))
assert d["brief_id"]=="brief-027"
sc=d["scorecard"]
assert sc["auto_apply_council"]==0 and sc["auto_send"]==0
assert sc["rubber_stamp"]==0 and sc["fake_live_council"]==0
assert sc["self_approve"]==0 and sc["hold_timeout_failopen"]==0
assert sc["kpd_bleed"]==0 and sc["timezone"]=="America/New_York"
assert "/api/auto-apply" in d["refused_post_prefixes"]
assert "/api/auto-apply-council" in d["refused_post_prefixes"]
assert "/api/council-force-send" in d["refused_post_prefixes"]
assert "auto-apply" in d["denied_tools"]
assert "Michael (ops)" in d["council_seats"]
assert "TokenMax (pool/burn)" in d["council_seats"]
assert "brief-008" in d["paired_with"] and "brief-017" in d["paired_with"]
print("seats", " · ".join(d["council_seats"]))
PYB27
fi

b27=$(curl -s -o /tmp/pra-brief027.json -w "%{http_code}" "$BASE/api/brief027" || echo "000")
[[ "$b27" == "200" ]] && ok "GET /api/brief027" || bad "GET /api/brief027 HTTP $b27"
if [[ "$b27" == "200" ]]; then
  python3 - <<'PYLC27' && ok "brief027 live_check" || bad "brief027 live_check"
import json
b=json.load(open("/tmp/pra-brief027.json",encoding="utf-8"))
assert b["brief_id"]=="brief-027"
lc=b["live_check"]
assert lc["auto_apply_council"]==0 and lc["auto_send"]==0
assert lc["auto_apply_apis_succeed"] is False
assert lc["auto_apply_council_apis_succeed"] is False
assert lc["council_force_send_apis_succeed"] is False
assert lc["mutation_endpoints_policy"]=="403"
assert lc["paired_with_brief008"] is True
assert lc["paired_with_brief017"] is True
assert lc["never_majority_vote_auto_apply"] is True
assert lc["council_hold_until_human_apply"] is True
assert lc["timezone"]=="America/New_York"
assert "America/New_York" in lc["served_at_et"] or "EDT" in lc["served_at_et"] or "EST" in lc["served_at_et"]
print("served", lc["served_at_et"])
PYLC27
fi

for ep in auto-apply auto-apply-council council-force-send; do
  code=$(curl -s -o "/tmp/pra-$ep.json" -w "%{http_code}" \
    -X POST -H 'Content-Type: application/json' -d '{}' \
    "$BASE/api/$ep" || echo "000")
  [[ "$code" == "403" ]] && ok "POST /api/$ep 403" || bad "POST /api/$ep HTTP $code"
done
python3 - <<'PY403C' && ok "403 cites brief-027" || bad "403 council body"
import json
d=json.load(open("/tmp/pra-auto-apply.json",encoding="utf-8"))
assert d.get("brief_id")=="brief-027" or "brief-027" in d.get("error","")
assert d.get("ok") is False
print(d.get("error","")[:140])
PY403C
code_get=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/api/auto-apply" || echo "000")
[[ "$code_get" == "403" ]] && ok "GET /api/auto-apply 403" || bad "GET /api/auto-apply HTTP $code_get"

home_html=$(curl -s "$BASE/" || true)
echo "$home_html" | grep -q 'Brief-027 law · Grok Council' && ok "UI Brief-027 law panel" || bad "UI missing Brief-027 panel"
grep -q 'renderBrief027' "$ROOT/static/app.js" && ok "app.js renderBrief027" || bad "missing renderBrief027"
grep -q 'brief024_correct_ci' "$ROOT/server.py" && ok "brief-024 fold still wired" || bad "lost brief-024 flag"
grep -q 'brief027_grok_council' "$ROOT/server.py" && ok "brief-027 fold wired" || bad "lost brief-027 flag"

echo "-- $PASS passed, $FAIL failed --"
if [[ "$FAIL" -eq 0 ]]; then
  echo "SMOKE PASS"
  exit 0
fi
echo "SMOKE FAIL"
exit 1
