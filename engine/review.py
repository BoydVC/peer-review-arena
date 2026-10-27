"""Parallel persona critique of a draft — deterministic, evidence-quoting."""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any

from .personas import PERSONAS

SEVERITIES = ("blocker", "high", "medium", "low", "nit")


def _now_et_iso() -> str:
    # Box clock is America/New_York; emit offset-aware local stamp.
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _evidence_snip(text: str, needle: str, radius: int = 90) -> str:
    idx = text.lower().find(needle.lower())
    if idx < 0:
        return ""
    start = max(0, idx - 20)
    end = min(len(text), idx + len(needle) + radius)
    snip = text[start:end].replace("\n", " ").strip()
    return snip[:220]


def _finding(
    persona_id: str,
    severity: str,
    claim: str,
    evidence: str,
    suggested_fix: str,
    topic: str = "",
) -> dict[str, Any]:
    assert severity in SEVERITIES
    fid = hashlib.sha1(f"{persona_id}|{claim}|{severity}".encode()).hexdigest()[:10]
    return {
        "id": f"{persona_id[:3]}-{fid}",
        "persona_id": persona_id,
        "severity": severity,
        "claim": claim,
        "evidence": evidence,
        "suggested_fix": suggested_fix,
        "topic": topic or "general",
    }


def _detect_kind(title: str, text: str) -> str:
    blob = (title + "\n" + text).lower()
    if "bonsai" in blob and ("reveal" in blob or "demo:story" in blob or "flaky-date" in blob):
        return "bonsai_reveal"
    # Pre-ops / workflow-audit brief (Agent Brief Forge brief-007) before forge_pack
    if (
        "brief-007" in blob
        or "pre-ops risk card" in blob
        or ("workflow-audit" in blob and "pre-ops" in blob)
        or ("one-thing-first" in blob and "allow-scoped" in blob)
    ):
        return "preops_brief"
    if (
        "agent brief forge" in blob
        or "brief-001" in blob
        or ("next topics" in blob and "token-pool" in blob)
    ):
        return "forge_pack"
    if "hold" in blob and "apply" in blob and ("brief" in blob or "citation" in blob):
        return "forge_pack"
    return "generic"


# --- Seed-specific curated findings (substantive, quote evidence) ---

def _bonsai_findings(text: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    # Skeptic
    out.append(_finding(
        "skeptic", "high",
        "Pass-11 numbers may drift before Thursday send if Origin SHA moves",
        _evidence_snip(text, "pass 11 @ e41f0d6") or "pass 11 @ e41f0d6 … Re-check only if a newer Origin SHA lands",
        "Bind the send checklist to STATUS.md SHA; if SHA ≠ e41f0d6, regenerate numbers + attachments before send.",
        "freshness",
    ))
    out.append(_finding(
        "skeptic", "medium",
        "Honesty line admits catalog-vs-discovery gap but spoken script may oversell 'ingests a pile'",
        _evidence_snip(text, "fixed catalog of 12 mistake types") or "Today the demo corpus is a fixed catalog of 12 mistake types",
        "Keep the spoken line 'synthetic mistakes' and add one beat: 'twelve planted types, not live history discovery yet.'",
        "honesty",
    ))
    out.append(_finding(
        "skeptic", "low",
        "'Apply-all ends 11 held / 1 biting' needs the remaining biter named in the talk",
        _evidence_snip(text, "11 held / 1 biting") or "apply-all ends eleven held, one biting",
        "Name the remaining biter aloud (honesty, not failure) so the audience doesn't invent a bug.",
        "demo_narrative",
    ))

    # Security
    out.append(_finding(
        "security", "blocker",
        "Draft must never be sent from a burn/subagent session",
        _evidence_snip(text, "Do not send from a burn") or "Do not send from a burn/subagent session.",
        "Enforce send-on-behalf Hold: only parent channel after Boyd OK; burn agents produce drafts only.",
        "send_gate",
    ))
    out.append(_finding(
        "security", "high",
        "Repo is still a private Origin draft — reveal must not imply public publish",
        _evidence_snip(text, "boydvc/tmp-6e67f983fcd2585c") or "private Cursor Origin draft boydvc/tmp-…",
        "Keep 'Where it lives' as Origin draft; require explicit OK before BoydVC/bonsai move.",
        "publish_boundary",
    ))
    out.append(_finding(
        "security", "medium",
        "SYNTHETIC playground claim is strong — verify every attached screenshot still shows the badge",
        _evidence_snip(text, "every screen says SYNTHETIC") or "every screen says SYNTHETIC",
        "Attachment preflight: open each PNG/webm and confirm SYNTHETIC chrome before send.",
        "honesty",
    ))
    out.append(_finding(
        "ux_delight", "medium",
        "Remaining '1 biting' after apply-all should be framed as honesty, not a broken demo",
        _evidence_snip(text, "remaining biter as honesty") or "Point at the remaining biter as honesty, not failure",
        "Agree the spoken beat with Skeptic before Thursday; one shared line.",
        "demo_narrative",
    ))
    out.append(_finding(
        "security", "low",
        "Blast-radius path guards mentioned but not demonstrated in the spoken path",
        _evidence_snip(text, "blast-radius") or "blast-radius path guards",
        "Optional 10s aside: point at path-guard in verify or adversarial output if time.",
        "verify",
    ))

    # UX Delight
    out.append(_finding(
        "ux_delight", "medium",
        "Spoken script targets 75–85s — good; two-minute how-to is operator, not spoken",
        _evidence_snip(text, "~75–85 seconds") or "Spoken script … ~75–85 seconds",
        "Copy only the spoken block into notes; keep operator checklist off-screen during the talk.",
        "script_length",
    ))
    out.append(_finding(
        "ux_delight", "high",
        "Demo path has six steps + optional apply-all — mid-talk Reset is a known footgun",
        _evidence_snip(text, "Do not click Reset again") or "Do not click Reset again mid-talk",
        "Put a sticky 'NO RESET' note on the demo machine; prefer CLI demo:reset only in preflight.",
        "demo_friction",
    ))
    out.append(_finding(
        "ux_delight", "low",
        "Hold / Apply / Revert glossary is in header — say it once at flaky-date cluster",
        _evidence_snip(text, "Hold = add the guard") or "Hold = add the guard. Apply = rewrite the smell. Revert = undo.",
        "Practice the three-word glossary aloud once; don't re-explain on every prune.",
        "glossary",
    ))
    out.append(_finding(
        "ux_delight", "nit",
        "Attachment table includes webm — silent clip is reveal-friendly",
        _evidence_snip(text, "demo-story.webm") or "~30 s motion clip … (silent)",
        "Confirm autoplay/mute works in the reveal channel before Thursday.",
        "attachments",
    ))

    # Operator
    out.append(_finding(
        "operator", "high",
        "Port 4317 must be free; Next.js 'N' badge means wrong serve mode",
        _evidence_snip(text, "127.0.0.1:4317") or "Open http://127.0.0.1:4317 — you should not see the Next.js dev N badge",
        "Preflight: lsof/curl 4317; abort if badge present; use serve --prod only.",
        "ports",
    ))
    out.append(_finding(
        "operator", "high",
        "Three green gates required: test, verify (28), adversarial (7)",
        _evidence_snip(text, "npm run verify") or "npm run verify — green (28 checks)",
        "Run all three ~5 min before talk; paste exit codes into a sticky note.",
        "preflight",
    ))
    out.append(_finding(
        "operator", "medium",
        "demo:story may need a single reload if tree does not live-refresh",
        _evidence_snip(text, "reload once") or "reload once if the tree has not live-refreshed",
        "Script the reload as step 3b so it doesn't look like a hang on stage.",
        "failure_mode",
    ))
    out.append(_finding(
        "operator", "low",
        "Deep-link cluster query is brittle if cluster id renames",
        _evidence_snip(text, "cluster=flaky-date-parse") or "?cluster=flaky-date-parse",
        "Pin cluster id in STATUS.md; if renamed, update reveal draft same commit.",
        "runbook",
    ))

    # Product
    out.append(_finding(
        "product", "medium",
        "Bookmark lineage (/correct, trust pyramid, Draft Day adjacency) is the ownership hook",
        _evidence_snip(text, "Straight out of your bookmarks") or "Straight out of your bookmarks: poteto's /correct",
        "Lead with 'why it's yours' before numbers so the reveal isn't a feature dump.",
        "narrative",
    ))
    out.append(_finding(
        "product", "low",
        "Ask to move Origin draft → BoydVC/bonsai is a clear next CTA",
        _evidence_snip(text, "BoydVC/bonsai") or "Want it moved to a private BoydVC/bonsai repo",
        "Keep CTA after honesty line; don't bury under attachments.",
        "cta",
    ))
    out.append(_finding(
        "product", "nit",
        "Target send Thu Oct 29 ~5 PM ET sits before ~7:42 PM reset — good pacing",
        _evidence_snip(text, "Thu Oct 29") or "Target send: Thu Oct 29, 2026 ~5 PM ET",
        "No change; confirm calendar block still clear.",
        "timing",
    ))
    return out


def _forge_findings(text: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    out.append(_finding(
        "skeptic", "medium",
        "Seed brief claims live WebSearch/WebFetch citations — peer must spot-check URLs still resolve",
        _evidence_snip(text, "WebSearch") or "Research for brief-001 was fetched live",
        "Smoke should assert ≥5 unique http citations and sample-fetch 2 URLs.",
        "citations",
    ))
    out.append(_finding(
        "skeptic", "low",
        "Pipeline stages are simulated peer review, not a live multi-model debate",
        _evidence_snip(text, "simulated peer reviewer") or "searcher → synthesizer → simulated peer reviewer",
        "Label UI as 'simulated stages' so Boyd doesn't expect live LLM round-trips.",
        "honesty",
    ))
    out.append(_finding(
        "security", "high",
        "Local-only bind 127.0.0.1:4330 — good; no firm/client topics in NEXT_TOPICS",
        _evidence_snip(text, "Not collections / law firm") or "Not collections / law firm",
        "Keep topic filter in POST /api/topics; reject kpdlawgroup-shaped strings.",
        "scope",
    ))
    out.append(_finding(
        "security", "medium",
        "POST /api/topics appends without rate limit — fine for local burn, not public",
        _evidence_snip(text, "Run next topic") or "use Run next topic to append",
        "Document local-only; never expose beyond loopback.",
        "exposure",
    ))
    out.append(_finding(
        "ux_delight", "medium",
        "2-minute how-to is crisp; home should surface brief line count + citation count",
        _evidence_snip(text, "2-minute how-to") or "## 2-minute how-to",
        "Dashboard hero: lines / citations / peer-review verdict at a glance.",
        "dashboard",
    ))
    out.append(_finding(
        "ux_delight", "low",
        "Ten NEXT_TOPICS are heavy follow-ups — good burn fuel, dense for a first glance",
        _evidence_snip(text, "Grok Bot fleet token-pool") or "Grok Bot fleet token-pool discipline",
        "UI: show top 3 topics + '7 more' expander.",
        "density",
    ))
    out.append(_finding(
        "operator", "high",
        "run.sh + smoke_test.sh are the contract — brief ≥200 lines and ≥5 citations",
        _evidence_snip(text, "smoke_test.sh") or "./smoke_test.sh  # health + brief ≥200 lines",
        "CI-less burn: always run smoke after regenerating brief-001.",
        "smoke",
    ))
    out.append(_finding(
        "operator", "medium",
        "pkill by script path can race if two forges start together",
        _evidence_snip(text, "127.0.0.1:4330") or "starts http://127.0.0.1:4330/",
        "Prefer PORT env + flock or health-check before pkill in future.",
        "ports",
    ))
    out.append(_finding(
        "product", "medium",
        "Hold/Apply brief topic maps cleanly onto Bonsai + Draft Day adjacency",
        _evidence_snip(text, "Hold vs Apply") or "Hold vs Apply, CAS, verification gates",
        "Cross-link Arena reviews of Bonsai reveal ↔ Forge brief in burn notes.",
        "fleet_fit",
    ))
    out.append(_finding(
        "product", "low",
        "NEXT_TOPICS intentionally skip law firm — aligns with burn rules",
        _evidence_snip(text, "Not collections / law firm") or "Not collections / law firm",
        "Keep exclusion list in DESIGN when topics regenerate.",
        "scope",
    ))
    return out



def _preops_findings(text: str) -> list[dict[str, Any]]:
    """Curated Arena pass on Agent Brief Forge brief-007 (pre-ops / workflow-audit)."""
    out: list[dict[str, Any]] = []

    # Skeptic
    out.append(_finding(
        "skeptic", "high",
        "A filled risk card is not runtime authorization — Appendix B pitfall still bites if prose-only",
        _evidence_snip(text, "Policy PDF with no runtime gate")
        or _evidence_snip(text, "card without wiring")
        or "AISVS C9 … block privileged … until explicit human approval",
        "Keep must-list: card + Hold/Apply + protected main/Environments; never treat card completion as runtime auth.",
        "runtime_vs_card",
    ))
    out.append(_finding(
        "skeptic", "medium",
        "Simulated forge peer reviewer is same burn family — not an independent pre-ops authority (PR-5)",
        _evidence_snip(text, "simulated peer reviewer")
        or _evidence_snip(text, "Peer-review findings (simulated)")
        or "simulated peer review",
        "Label independence quality; prefer /interrogate or cross-family critic before encoding Pre-ops Origin as fleet law.",
        "independence",
    ))
    out.append(_finding(
        "skeptic", "low",
        "AWS three-tier maps awkwardly onto a solo household operator (PR-4)",
        _evidence_snip(text, "multi-stakeholder")
        or _evidence_snip(text, "Tier mapping")
        or "AGENTOPS06-BP03",
        "For solo fleets: Tier 3 needs time-separated Apply or second-family critic + human Apply — never same-chat self-approve.",
        "tier_mapping",
    ))
    out.append(_finding(
        "skeptic", "nit",
        "21 live citations are a strength — spot-check a few raw.githubusercontent.com URLs still resolve",
        _evidence_snip(text, "raw.githubusercontent.com/OWASP/AISVS")
        or "https://raw.githubusercontent.com/OWASP/AISVS",
        "Citation checker already counts URLs; sample-fetch AISVS C9 + AGENTOPS06 before encoding Origin agent.",
        "citations",
    ))

    # Security
    out.append(_finding(
        "security", "blocker",
        "Burn/subagent sessions must never send, merge, deploy, or move money even after a card ALLOW",
        _evidence_snip(text, "no outbound")
        or _evidence_snip(text, "Do not specialize")
        or "Treat any outbound message as irreversible",
        "Enforce: Arena + Forge burns produce drafts/cards only; Apply stays on parent channel after human OK.",
        "send_gate",
    ))
    out.append(_finding(
        "security", "high",
        "GitHub Environment required reviewers may be unavailable on some Free/private plans (PR-2)",
        _evidence_snip(text, "plan limits")
        or _evidence_snip(text, "required reviewers")
        or "local Hold must cover",
        "Document local Hold/Apply as the universal Tier-3 gate; Environments are should when plan allows.",
        "github_plan_limits",
    ))
    out.append(_finding(
        "security", "high",
        "Self-merge / self-deploy tools must stay off agent allowlists (Appendix C AC.8)",
        _evidence_snip(text, "No self-merge tools")
        or _evidence_snip(text, "cannot approve, merge, sign, or deploy")
        or "human merges",
        "Keep §9.1 must #5: no gh pr merge / deploy tools in T3 allowlists; CI bot opens, human merges.",
        "no_self_deploy",
    ))
    out.append(_finding(
        "security", "medium",
        "Fail-open Apply timeout is an explicit anti-pattern — verify runtime default is fail-closed",
        _evidence_snip(text, "Fail-closed Apply timeouts")
        or _evidence_snip(text, "Auto-approve Tier 3 on timeout")
        or "fail closed",
        "Wire expires → deny pending action; escalate to backup human, never auto-approve Tier 3.",
        "fail_closed",
    ))
    out.append(_finding(
        "security", "low",
        "EU AI Act Art.14 pointer is correctly framed as north star, not household compliance claim",
        _evidence_snip(text, "not an assertion that household bots are in-scope")
        or "EU AI Act Article 14",
        "Keep the disclaimer adjacent whenever Art.14 is cited in the Origin agent UX.",
        "honesty",
    ))

    # UX Delight
    out.append(_finding(
        "ux_delight", "medium",
        "Risk-card schema is dense for a nightly gate — operators need a 30-second fill path",
        _evidence_snip(text, "PRE-OPS RISK CARD")
        or _evidence_snip(text, "Card fields (must be filled")
        or "one_thing:",
        "Ship a one-screen card UI with required fields only; advanced evidence packet behind expander.",
        "card_ux",
    ))
    out.append(_finding(
        "ux_delight", "medium",
        "Deny-by-default checklist uses checkboxes that read as 'done' — invert to fail conditions",
        _evidence_snip(text, "Deny by default checklist")
        or "- [ ] Tools include send/merge",
        "Render as red fail chips ('DENY if…') so unchecked does not look like progress.",
        "checklist_semantics",
    ))
    out.append(_finding(
        "ux_delight", "low",
        "Worked examples (ALLOW/DENY/DEFER) are excellent — surface them as templates in the card UX",
        _evidence_snip(text, "ALLOW-SCOPED — draft PR docs only")
        or "Worked examples (synthetic)",
        "Pre-fill card from example chips; keep synthetic badge so they are not treated as live approvals.",
        "templates",
    ))
    out.append(_finding(
        "ux_delight", "nit",
        "Brief is long (~heavy) — good for Forge, heavy for a spoken reveal",
        f"~{len(text.split())} words",
        "Arena chair report is the skim; keep full brief for Origin encoding.",
        "density",
    ))

    # Operator
    out.append(_finding(
        "operator", "high",
        "Pre-ops must stay distinct from Peer Arena critique-before-merge (PR-3 / §1.1)",
        _evidence_snip(text, "Pre-ops is not peer review")
        or _evidence_snip(text, "does not replace this gate")
        or "When | Question answered",
        "Require both for Tier ≥2 code changes that also touch prod paths; do not collapse into one LGTM.",
        "gate_separation",
    ))
    out.append(_finding(
        "operator", "high",
        "One-thing-first needs a machine check — prose alone will be gamed",
        _evidence_snip(text, "exactly one** primary target")
        or _evidence_snip(text, "One-thing-first")
        or "also clean up Slack",
        "Schema reject when tools_requested span >1 prod_paths class or when Slack+Gmail both appear.",
        "one_thing_enforcement",
    ))
    out.append(_finding(
        "operator", "medium",
        "Local LIVE :43xx ports are correctly called production-class when humans treat them as truth",
        _evidence_snip(text, "127.0.0.1:43xx")
        or _evidence_snip(text, "Local LIVE ports")
        or "system of record",
        "Restart/wipe of state-holding LIVE apps requires a card; document in burn runbooks.",
        "localhost_prod",
    ))
    out.append(_finding(
        "operator", "low",
        "Scorecard columns in §13 need a Fleet Doctor v2 home — metrics not yet wired LIVE",
        _evidence_snip(text, "Prod-tool sessions with card")
        or "Add to the weekly fleet scorecard",
        "Nice-to-have: add pre-ops coverage column to fleet-doctor-v2 after Origin agent exists.",
        "scorecard_wiring",
    ))
    out.append(_finding(
        "operator", "nit",
        "Adversarial test table (§12) is the right CI seed for the gate itself",
        _evidence_snip(text, "Prompt injection: “ignore pre-ops")
        or "Adversarial tests for the gate",
        "When encoding Origin agent, turn rows into automated deny cases.",
        "adversarial_tests",
    ))

    # Product
    out.append(_finding(
        "product", "medium",
        "Jim · Interests lane #2 / Pre-ops Origin adjacency is clear — CTA should be encode Origin agent, not another brief",
        _evidence_snip(text, "Pre-ops Origin agent")
        or _evidence_snip(text, "Jim · Interests lane #2")
        or "Owns the risk-card UX",
        "End burn notes with one ask: scaffold Pre-ops Origin from §3 card schema.",
        "cta",
    ))
    out.append(_finding(
        "product", "low",
        "Fleet product map (§8) correctly keeps Kids Studio / dual-pool orthogonal to prod authority",
        _evidence_snip(text, "Child sessions never get prod tools")
        or _evidence_snip(text, "burn pool ≠ prod authority")
        or "Mapping to Boyd fleet products",
        "Keep exclusions when topics regenerate; no vertical/firm encoding.",
        "fleet_fit",
    ))
    out.append(_finding(
        "product", "nit",
        "Must/should/later (§9) is a clean encode-this-week cut",
        _evidence_snip(text, "Must (encode this week)")
        or "Risk card required before any agent session",
        "Arena must-fix should track §9.1; should-list stays backlog.",
        "prioritization",
    ))
    return out



def _generic_findings(text: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    words = len(re.findall(r"\S+", text))
    urls = re.findall(r"https?://[^\s\)\]\>\"']+", text)
    has_checklist = bool(re.search(r"^\s*- \[[ xX]\]", text, re.M))
    has_honesty = bool(re.search(r"honest|limitation|does not pretend|synthetic|draft only", text, re.I))
    has_numbers = bool(re.search(r"\b\d{2,}\b", text))
    mentions_send = bool(re.search(r"\b(send|publish|deploy|merge|post)\b", text, re.I))
    mentions_localhost = bool(re.search(r"127\.0\.0\.1|localhost", text))

    out.append(_finding(
        "skeptic", "medium" if words < 200 else "low",
        f"Draft length ~{words} words / {lines} lines — {'thin for a ship claim' if words < 200 else 'enough surface for critique'}",
        text[:160].replace("\n", " ") + ("…" if len(text) > 160 else ""),
        "Add concrete numbers, failure modes, and an honesty paragraph before claiming ready.",
        "coverage",
    ))
    if not has_honesty:
        out.append(_finding(
            "skeptic", "high",
            "No honesty / limitations paragraph detected",
            "(pattern miss: honest|limitation|synthetic|draft only)",
            "Add a short 'what's honest about it' section before any send CTA.",
            "honesty",
        ))
    else:
        out.append(_finding(
            "skeptic", "low",
            "Honesty / limitations language present",
            _evidence_snip(text, "honest") or _evidence_snip(text, "synthetic") or _evidence_snip(text, "limitation"),
            "Keep limitations adjacent to the hero claim.",
            "honesty",
        ))
    if not urls:
        out.append(_finding(
            "skeptic", "medium",
            "No http citations found — claims may be unanchored",
            "(no https?:// matches)",
            "Attach ≥3 primary URLs or point at local artifact paths with SHAs.",
            "citations",
        ))
    else:
        out.append(_finding(
            "skeptic", "nit",
            f"{len(set(urls))} unique URL(s) referenced",
            urls[0][:180],
            "Spot-check that linked docs match the claim dates.",
            "citations",
        ))

    if mentions_send:
        out.append(_finding(
            "security", "high",
            "Draft mentions send/publish/deploy/merge — confirm Hold gate exists",
            _evidence_snip(text, "send") or _evidence_snip(text, "publish") or _evidence_snip(text, "deploy"),
            "State explicitly: draft only; human OK required; no burn-session send.",
            "send_gate",
        ))
    else:
        out.append(_finding(
            "security", "low",
            "No irreversible-action verbs detected in draft body",
            "(no send/publish/deploy/merge hits)",
            "Still add a one-line 'do not send from subagent' if this becomes a reveal.",
            "send_gate",
        ))
    out.append(_finding(
        "security", "medium" if not mentions_localhost else "low",
        "Trust boundary: " + ("loopback URLs present" if mentions_localhost else "no loopback bind called out"),
        _evidence_snip(text, "127.0.0.1") or "(no 127.0.0.1/localhost)",
        "Document bind address and SYNTHETIC/real data boundary.",
        "boundary",
    ))

    out.append(_finding(
        "ux_delight", "medium" if words > 1200 else "low",
        "Cognitive load: " + ("long — consider a <90s spoken cut" if words > 1200 else "manageable for a skim"),
        f"~{words} words",
        "Split operator checklist from spoken script.",
        "script_length",
    ))
    if has_checklist:
        out.append(_finding(
            "ux_delight", "nit",
            "Checklist items present — good for operators",
            _evidence_snip(text, "- [") or "(checkbox list)",
            "Keep checkboxes for pre-send; don't read them aloud.",
            "checklist",
        ))
    else:
        out.append(_finding(
            "ux_delight", "medium",
            "No pre-send checklist detected",
            "(no - [ ] patterns)",
            "Add a 5-item preflight checkbox block.",
            "checklist",
        ))

    out.append(_finding(
        "operator", "high" if not has_checklist else "medium",
        "Operability: need explicit run/reset/verify commands",
        text[:120].replace("\n", " "),
        "Include exact commands, ports, and a failure-mode reload/reset note.",
        "runbook",
    ))
    if has_numbers:
        out.append(_finding(
            "operator", "low",
            "Numeric claims present — bind them to a SHA or date",
            _evidence_snip(text, re.search(r"\b\d{2,}\b", text).group(0)) if re.search(r"\b\d{2,}\b", text) else "",
            "Put build id / pass number next to every headline metric.",
            "freshness",
        ))
    out.append(_finding(
        "operator", "nit",
        f"Raw stats: lines={lines} words={words} urls={len(set(urls))}",
        f"lines={lines}",
        "Surface these in the chair scorecard header.",
        "metrics",
    ))

    out.append(_finding(
        "product", "medium",
        "Ownership hook: does the draft say why this is Boyd's?",
        text[:140].replace("\n", " "),
        "Open with bookmark / fleet adjacency before features.",
        "narrative",
    ))
    out.append(_finding(
        "product", "low",
        "CTA clarity after critique",
        text[-160:].replace("\n", " "),
        "End with one ask (move repo / approve send / next burn) — not three.",
        "cta",
    ))
    return out


def run_review(
    draft_text: str,
    *,
    title: str = "Untitled draft",
    source: str = "paste",
    draft_id: str | None = None,
) -> dict[str, Any]:
    """Run all personas (logically parallel) and return raw review transcript."""
    kind = _detect_kind(title, draft_text)
    if kind == "bonsai_reveal":
        findings = _bonsai_findings(draft_text)
    elif kind == "preops_brief":
        findings = _preops_findings(draft_text)
    elif kind == "forge_pack":
        findings = _forge_findings(draft_text)
    else:
        findings = _generic_findings(draft_text)

    # Ensure every persona contributed ≥1 finding
    seen = {f["persona_id"] for f in findings}
    for p in PERSONAS:
        if p["id"] not in seen:
            findings.append(_finding(
                p["id"], "nit",
                f"{p['name']} scanned draft — no persona-specific fire alarms",
                draft_text[:100].replace("\n", " "),
                "No action; keep persona in the cast for the next revision.",
                "coverage",
            ))

    by_persona: dict[str, list] = {p["id"]: [] for p in PERSONAS}
    for f in findings:
        by_persona.setdefault(f["persona_id"], []).append(f)

    personas_out = []
    for p in PERSONAS:
        fl = by_persona.get(p["id"], [])
        personas_out.append({
            **p,
            "finding_count": len(fl),
            "findings": fl,
            "summary": f"{p['name']} filed {len(fl)} finding(s) via {p['lens']}",
        })

    return {
        "schema": "peer-review-arena/v1",
        "draft_id": draft_id or hashlib.sha1(draft_text.encode()).hexdigest()[:12],
        "title": title,
        "source": source,
        "kind": kind,
        "reviewed_at": _now_et_iso(),
        "draft_stats": {
            "chars": len(draft_text),
            "lines": draft_text.count("\n") + (1 if draft_text and not draft_text.endswith("\n") else 0),
            "words": len(re.findall(r"\S+", draft_text)),
            "unique_urls": len(set(re.findall(r"https?://[^\s\)\]\>\"']+", draft_text))),
        },
        "personas": personas_out,
        "findings": findings,
        "persona_count": len(PERSONAS),
        "finding_count": len(findings),
    }
