#!/usr/bin/env python3
"""Generate seed review artifacts for Bonsai reveal + Forge pack + brief-007."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from engine import run_review, chair_merge
from engine.render_md import render_review_md
from server import _save_bundle, _bundle_for, SEEDS


def main() -> None:
    # Required primary seed
    text = (ROOT / "seeds/bonsai-reveal.md").read_text(encoding="utf-8")
    bundle = _bundle_for(text, title="Bonsai REVEAL_DRAFT", source="seed:bonsai-reveal", draft_id="bonsai-reveal")
    info = _save_bundle(bundle, "review-bonsai-reveal")
    print("bonsai:", info)

    # Second seed options
    for seed_id, stem in (
        ("forge-readme", "review-forge-readme"),
        ("forge-next-topics", "review-forge-next-topics"),
    ):
        meta = SEEDS[seed_id]
        text = (ROOT / meta["path"]).read_text(encoding="utf-8")
        bundle = _bundle_for(text, title=meta["title"], source=f"seed:{seed_id}", draft_id=seed_id)
        info = _save_bundle(bundle, stem)
        print(seed_id + ":", info)

    # Brief-007 pre-ops / workflow-audit (weekly burn)
    meta = SEEDS["brief-007-preops"]
    text = (ROOT / meta["path"]).read_text(encoding="utf-8")
    bundle = _bundle_for(
        text,
        title=meta["title"],
        source="seed:brief-007-preops",
        draft_id="brief-007-preops",
    )
    info = _save_bundle(bundle, "review-brief-007")
    print("brief-007-preops:", info)


if __name__ == "__main__":
    main()
