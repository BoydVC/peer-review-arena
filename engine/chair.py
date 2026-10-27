"""Chair merges persona findings into consensus scorecard."""
from __future__ import annotations

from collections import defaultdict
from typing import Any

from .personas import PERSONAS

WEIGHT = {"blocker": 5, "high": 4, "medium": 3, "low": 2, "nit": 1}
LABEL = {
    range(0, 8): "ship_ready",
    range(8, 16): "ship_with_fixes",
    range(16, 28): "needs_revision",
    range(28, 999): "hold",
}


def _verdict(score: int) -> str:
    if score < 8:
        return "ship_ready"
    if score < 16:
        return "ship_with_fixes"
    if score < 28:
        return "needs_revision"
    return "hold"


def chair_merge(review: dict[str, Any]) -> dict[str, Any]:
    findings = list(review.get("findings") or [])
    by_topic: dict[str, list] = defaultdict(list)
    for f in findings:
        by_topic[f.get("topic") or "general"].append(f)

    # Consensus rows: one per topic, worst severity + agreeing personas
    consensus_table = []
    disagreements = []
    for topic, fl in sorted(by_topic.items(), key=lambda kv: -max(WEIGHT[x["severity"]] for x in kv[1])):
        severities = {f["severity"] for f in fl}
        personas = sorted({f["persona_id"] for f in fl})
        worst = max(fl, key=lambda f: WEIGHT[f["severity"]])
        row = {
            "topic": topic,
            "worst_severity": worst["severity"],
            "persona_count": len(personas),
            "personas": personas,
            "headline": worst["claim"],
            "suggested_fix": worst["suggested_fix"],
            "finding_ids": [f["id"] for f in fl],
        }
        consensus_table.append(row)
        if len(severities) >= 2 and len(personas) >= 2:
            disagreements.append({
                "topic": topic,
                "severity_spread": sorted(severities, key=lambda s: -WEIGHT[s]),
                "personas": personas,
                "notes": (
                    f"Personas disagree on urgency for '{topic}': "
                    + ", ".join(sorted(severities, key=lambda s: -WEIGHT[s]))
                ),
            })

    must_fix = [
        {
            "id": f["id"],
            "persona_id": f["persona_id"],
            "severity": f["severity"],
            "claim": f["claim"],
            "suggested_fix": f["suggested_fix"],
            "evidence": f.get("evidence") or "",
        }
        for f in findings
        if f["severity"] in ("blocker", "high")
    ]
    must_fix.sort(key=lambda x: (-WEIGHT[x["severity"]], x["persona_id"]))

    nice_to_haves = [
        {
            "id": f["id"],
            "persona_id": f["persona_id"],
            "severity": f["severity"],
            "claim": f["claim"],
            "suggested_fix": f["suggested_fix"],
            "evidence": f.get("evidence") or "",
        }
        for f in findings
        if f["severity"] in ("medium", "low")
    ]
    nice_to_haves.sort(key=lambda x: (-WEIGHT[x["severity"]], x["persona_id"]))

    risk_score = sum(WEIGHT[f["severity"]] for f in findings)
    # Normalize lightly by finding count so huge nit lists don't auto-hold
    adjusted = risk_score - sum(1 for f in findings if f["severity"] == "nit")
    verdict = _verdict(max(0, adjusted))

    per_persona = []
    for p in PERSONAS:
        fl = [f for f in findings if f["persona_id"] == p["id"]]
        per_persona.append({
            "id": p["id"],
            "name": p["name"],
            "color": p["color"],
            "finding_count": len(fl),
            "blocker": sum(1 for f in fl if f["severity"] == "blocker"),
            "high": sum(1 for f in fl if f["severity"] == "high"),
            "medium": sum(1 for f in fl if f["severity"] == "medium"),
            "low": sum(1 for f in fl if f["severity"] == "low"),
            "nit": sum(1 for f in fl if f["severity"] == "nit"),
            "risk_contribution": sum(WEIGHT[f["severity"]] for f in fl),
        })

    return {
        "chair": "Chair",
        "verdict": verdict,
        "risk_score": risk_score,
        "adjusted_score": adjusted,
        "summary": (
            f"Chair merges {len(findings)} findings from {review.get('persona_count', len(PERSONAS))} personas → "
            f"verdict={verdict}, must-fix={len(must_fix)}, nice-to-haves={len(nice_to_haves)}, disagreements={len(disagreements)}."
        ),
        "consensus_table": consensus_table,
        "disagreements": disagreements,
        "must_fix_before_ship": must_fix,
        "nice_to_haves": nice_to_haves,
        "per_persona": per_persona,
        "counts": {
            "findings": len(findings),
            "must_fix": len(must_fix),
            "nice_to_haves": len(nice_to_haves),
            "disagreements": len(disagreements),
            "topics": len(consensus_table),
            "blocker": sum(1 for f in findings if f["severity"] == "blocker"),
            "high": sum(1 for f in findings if f["severity"] == "high"),
            "medium": sum(1 for f in findings if f["severity"] == "medium"),
            "low": sum(1 for f in findings if f["severity"] == "low"),
            "nit": sum(1 for f in findings if f["severity"] == "nit"),
        },
    }
