"""Reviewer personas — fixed cast of ≥4 angles for every draft."""
from __future__ import annotations

PERSONAS = [
    {
        "id": "skeptic",
        "name": "Skeptic",
        "role": "Adversarial truth-seeker",
        "lens": "Overclaims, missing evidence, demo theater vs product truth, honesty gaps.",
        "color": "#f97316",
    },
    {
        "id": "security",
        "name": "Security",
        "role": "Blast-radius & trust boundary reviewer",
        "lens": "Irreversible actions, synthetic vs real data, path guards, publish/send gates.",
        "color": "#ef4444",
    },
    {
        "id": "ux_delight",
        "name": "UX Delight",
        "role": "Operator experience & reveal polish",
        "lens": "Cognitive load, spoken-script length, demo friction, glossary clarity, delight.",
        "color": "#a855f7",
    },
    {
        "id": "operator",
        "name": "Operator / On-call",
        "role": "Day-2 operability",
        "lens": "Runbooks, ports, reset/recover, failure modes, preflight checklists.",
        "color": "#22c55e",
    },
    {
        "id": "product",
        "name": "Product Strategist",
        "role": "Fit & narrative ownership",
        "lens": "Why this exists for Boyd, bookmark lineage, fleet placement, next-ask clarity.",
        "color": "#38bdf8",
    },
]

PERSONA_IDS = [p["id"] for p in PERSONAS]
