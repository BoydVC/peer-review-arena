#!/usr/bin/env python3
"""Peer Review Arena — multi-persona critique + chair consensus on 127.0.0.1:4333."""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from engine import run_review, chair_merge  # noqa: E402
from engine.render_md import render_review_md  # noqa: E402

PORT = int(os.environ.get("PORT", "4333"))
HOST = "127.0.0.1"

SEEDS = {
    "bonsai-reveal": {
        "id": "bonsai-reveal",
        "title": "Bonsai REVEAL_DRAFT",
        "path": "seeds/bonsai-reveal.md",
        "description": "Critique the Bonsai reveal draft (pass 11).",
    },
    "forge-readme": {
        "id": "forge-readme",
        "title": "Agent Brief Forge README",
        "path": "seeds/forge-readme.md",
        "description": "Second seed — Forge README how-to + layout.",
    },
    "forge-next-topics": {
        "id": "forge-next-topics",
        "title": "Agent Brief Forge NEXT_TOPICS",
        "path": "seeds/forge-next-topics.md",
        "description": "Second-seed alternate — 10 heavy follow-up topics.",
    },
    "brief-007-preops": {
        "id": "brief-007-preops",
        "title": "Brief-007 Pre-Ops / Workflow-Audit Gates",
        "path": "seeds/brief-007-preops.md",
        "description": "Arena pass on Agent Brief Forge brief-007 (pre-ops risk card before prod).",
    },
}

REFUSED_CORRECT_CI = {
    "/api/auto-merge",
    "/api/force-merge",
    "/api/bypass-correct-ci",
}

REFUSED_COUNCIL = {
    "/api/auto-apply",
    "/api/auto-apply-council",
    "/api/council-force-send",
}

ET = ZoneInfo("America/New_York")


def _stamp_et() -> str:
    return datetime.now(ET).strftime("%Y-%m-%d %I:%M:%S %p %Z") + " (America/New_York)"


def brief024_payload() -> dict:
    """Fold Agent Brief Forge brief-024 law + live_check (/correct CI encoding)."""
    law = _read_json(ROOT / "data" / "brief024.json")
    sc = law.get("scorecard", {})
    law["live_check"] = {
        "auto_merge": sc.get("auto_merge", 0),
        "docs_only_lessons": sc.get("docs_only_lessons", 0),
        "advisory_only_arch_job": sc.get("advisory_only_arch_job", 0),
        "self_merge_or_self_approve": sc.get("self_merge_or_self_approve", 0),
        "agent_pr_non_draft_without_human_ready": sc.get(
            "agent_pr_non_draft_without_human_ready", 0
        ),
        "unproven_checks": sc.get("unproven_checks", 0),
        "synthetic_sold_as_live": sc.get("synthetic_sold_as_live", 0),
        "burn_merge_or_send": sc.get("burn_merge_or_send", 0),
        "utc_only_stamps": sc.get("utc_only_stamps", 0),
        "kpd_bleed": sc.get("kpd_bleed", 0),
        "auto_merge_apis_succeed": False,
        "force_merge_apis_succeed": False,
        "bypass_correct_ci_apis_succeed": False,
        "post_disabled": True,
        "mutation_endpoints_policy": "403",
        "refused_post_prefixes": list(REFUSED_CORRECT_CI),
        "encoding_ladder": list(law.get("encoding_ladder", [])),
        "paired_with_brief007": True,
        "paired_with_brief012": True,
        "paired_with_brief004": True,
        "never_merge_without_boyd_ok": True,
        "timezone": "America/New_York",
        "served_at_et": _stamp_et(),
    }
    return law


def brief027_payload() -> dict:
    """Fold Agent Brief Forge brief-027 law + live_check (Grok Council Hold before Apply)."""
    law = _read_json(ROOT / "data" / "brief027.json")
    sc = law.get("scorecard", {})
    law["live_check"] = {
        "auto_apply_council": sc.get("auto_apply_council", 0),
        "auto_send": sc.get("auto_send", 0),
        "rubber_stamp": sc.get("rubber_stamp", 0),
        "fake_live_council": sc.get("fake_live_council", 0),
        "truncated_digest_applies": sc.get("truncated_digest_applies", 0),
        "hold_timeout_failopen": sc.get("hold_timeout_failopen", 0),
        "self_approve": sc.get("self_approve", 0),
        "minority_drop": sc.get("minority_drop", 0),
        "tool_during_deliberation": sc.get("tool_during_deliberation", 0),
        "cas_conflict_silent": sc.get("cas_conflict_silent", 0),
        "wrong_principal": sc.get("wrong_principal", 0),
        "utc_only_stamps": sc.get("utc_only_stamps", 0),
        "kpd_bleed": sc.get("kpd_bleed", 0),
        "auto_apply_apis_succeed": False,
        "auto_apply_council_apis_succeed": False,
        "council_force_send_apis_succeed": False,
        "post_disabled": True,
        "mutation_endpoints_policy": "403",
        "refused_post_prefixes": list(REFUSED_COUNCIL),
        "council_seats": list(law.get("council_seats", [])),
        "desk_stages": list(law.get("desk_stages", [])),
        "paired_with_brief008": True,
        "paired_with_brief017": True,
        "paired_with_brief007": True,
        "paired_with_brief024": True,
        "never_majority_vote_auto_apply": True,
        "council_hold_until_human_apply": True,
        "timezone": "America/New_York",
        "served_at_et": _stamp_et(),
    }
    return law


def _read_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    tmp.replace(path)


def _bundle_for(draft_text: str, title: str, source: str, draft_id: str | None = None) -> dict:
    review = run_review(draft_text, title=title, source=source, draft_id=draft_id)
    chair = chair_merge(review)
    return {"review": review, "chair": chair}


def _save_bundle(bundle: dict, stem: str) -> dict:
    out_json = ROOT / "out" / f"{stem}.json"
    out_md = ROOT / "out" / f"{stem}.md"
    _write_json(out_json, bundle)
    out_md.write_text(render_review_md(bundle), encoding="utf-8")
    return {
        "json": str(out_json.relative_to(ROOT)),
        "md": str(out_md.relative_to(ROOT)),
        "verdict": bundle["chair"]["verdict"],
        "finding_count": bundle["review"]["finding_count"],
        "must_fix": bundle["chair"]["counts"]["must_fix"],
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "static"), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        print(f"[arena] {self.address_string()} {fmt % args}", flush=True)

    def _send_json(self, code: int, payload) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, code: int, text: str, content_type: str) -> None:
        body = text.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            return self._send_json(
                200,
                {
                    "ok": True,
                    "service": "peer-review-arena",
                    "port": PORT,
                    "personas": 5,
                    "brief007_preops": True,
                    "brief024_correct_ci": True,
                    "brief027_grok_council": True,
                    "timezone": "America/New_York",
                },
            )

        if path == "/api/personas":
            from engine.personas import PERSONAS

            return self._send_json(200, {"personas": PERSONAS})

        if path == "/api/seeds":
            items = []
            for s in SEEDS.values():
                p = ROOT / s["path"]
                items.append({
                    **s,
                    "exists": p.is_file(),
                    "bytes": p.stat().st_size if p.is_file() else 0,
                })
            return self._send_json(200, {"seeds": items})

        if path.startswith("/api/seeds/") and path.endswith("/raw"):
            seed_id = path[len("/api/seeds/") : -len("/raw")]
            meta = SEEDS.get(seed_id)
            if not meta:
                return self._send_json(404, {"ok": False, "error": "unknown seed"})
            text = (ROOT / meta["path"]).read_text(encoding="utf-8")
            return self._send_text(200, text, "text/markdown; charset=utf-8")

        if path == "/api/reviews":
            out = ROOT / "out"
            files = sorted(out.glob("review-*.json")) if out.is_dir() else []
            items = []
            for f in files:
                try:
                    data = _read_json(f)
                    items.append({
                        "file": f.name,
                        "title": data["review"]["title"],
                        "verdict": data["chair"]["verdict"],
                        "finding_count": data["review"]["finding_count"],
                        "reviewed_at": data["review"]["reviewed_at"],
                    })
                except Exception as exc:  # noqa: BLE001
                    items.append({"file": f.name, "error": str(exc)})
            return self._send_json(200, {"reviews": items})

        if path.startswith("/api/reviews/"):
            name = path[len("/api/reviews/") :]
            if "/" in name or ".." in name:
                return self._send_json(400, {"ok": False, "error": "bad name"})
            target = (ROOT / "out" / name).resolve()
            if not str(target).startswith(str((ROOT / "out").resolve())) or not target.is_file():
                return self._send_json(404, {"ok": False, "error": "not found"})
            if target.suffix == ".md":
                return self._send_text(200, target.read_text(encoding="utf-8"), "text/markdown; charset=utf-8")
            return self._send_json(200, _read_json(target))

        if path.startswith("/out/"):
            rel = path[len("/out/") :]
            target = (ROOT / "out" / rel).resolve()
            if not str(target).startswith(str((ROOT / "out").resolve())) or not target.is_file():
                self.send_error(404)
                return
            data = target.read_bytes()
            ctype = "text/markdown; charset=utf-8" if target.suffix == ".md" else "application/json"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        if path == "/api/brief024":
            return self._send_json(200, brief024_payload())

        if path == "/api/brief027":
            return self._send_json(200, brief027_payload())

        if path in REFUSED_CORRECT_CI:
            return self._send_json(
                403,
                {
                    "ok": False,
                    "error": "refused: brief-024 /correct CI — auto_merge=0 / docs_only_lessons=0; never merge without Boyd OK",
                    "path": path,
                    "brief_id": "brief-024",
                },
            )

        if path in REFUSED_COUNCIL:
            return self._send_json(
                403,
                {
                    "ok": False,
                    "error": "refused: brief-027 Grok Council — auto_apply_council=0 / auto_send=0; Council Hold until human Apply; never majority-vote auto-apply",
                    "path": path,
                    "brief_id": "brief-027",
                },
            )

        if path == "/" or path == "":
            self.path = "/index.html"
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return self._send_json(400, {"ok": False, "error": "invalid json"})

        if parsed.path == "/api/review":
            seed_id = (body.get("seed_id") or "").strip()
            draft = body.get("draft")
            title = (body.get("title") or "").strip()
            save = bool(body.get("save", True))
            stem = (body.get("stem") or "").strip()

            if seed_id:
                meta = SEEDS.get(seed_id)
                if not meta:
                    return self._send_json(404, {"ok": False, "error": "unknown seed"})
                draft_text = (ROOT / meta["path"]).read_text(encoding="utf-8")
                title = title or meta["title"]
                source = f"seed:{seed_id}"
                draft_id = seed_id
                stem = stem or f"review-{seed_id.replace('_', '-')}"
            else:
                draft_text = draft if isinstance(draft, str) else ""
                if len(draft_text.strip()) < 40:
                    return self._send_json(400, {"ok": False, "error": "draft too short (min 40 chars)"})
                title = title or "Pasted draft"
                source = "paste"
                draft_id = None
                stem = stem or "review-paste"

            bundle = _bundle_for(draft_text, title=title, source=source, draft_id=draft_id)
            saved = None
            if save:
                stem = re.sub(r"[^a-zA-Z0-9._-]+", "-", stem).strip("-") or "review-paste"
                if not stem.startswith("review-"):
                    stem = "review-" + stem
                saved = _save_bundle(bundle, stem)
            return self._send_json(
                200,
                {
                    "ok": True,
                    "bundle": bundle,
                    "saved": saved,
                    "markdown": render_review_md(bundle),
                },
            )

        if parsed.path in REFUSED_CORRECT_CI:
            return self._send_json(
                403,
                {
                    "ok": False,
                    "error": "refused: brief-024 /correct CI — auto_merge=0 / docs_only_lessons=0; never merge without Boyd OK",
                    "path": parsed.path,
                    "brief_id": "brief-024",
                },
            )

        if parsed.path in REFUSED_COUNCIL:
            return self._send_json(
                403,
                {
                    "ok": False,
                    "error": "refused: brief-027 Grok Council — auto_apply_council=0 / auto_send=0; Council Hold until human Apply; never majority-vote auto-apply",
                    "path": parsed.path,
                    "brief_id": "brief-027",
                },
            )

        self.send_error(404)


def main() -> None:
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Peer Review Arena on http://{HOST}:{PORT}/", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
