#!/usr/bin/env python3
"""Build the immutable E18.26 Jesse BoostD10 plan artifact."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[5]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docs.model_specs.codex.e18.tools.e18_26_jesse_boost_d10_controller import (
    build_candidate_plan,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/derived/E18_26_770_JESSE_BOOST_D10_PLAN_V1.json"


def main() -> int:
    plan = build_candidate_plan()
    OUTPUT.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "gate_0a_passed": plan["gate_0a_passed"],
                "plan_sha256": plan["plan_sha256"],
                "shadow_crop_output": plan["totals"]["shadow_crop_output"],
                "failed_checks": [
                    key for key, passed in plan["gate_0a_checks"].items() if not passed
                ],
            },
            indent=2,
        )
    )
    return 0 if plan["gate_0a_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
