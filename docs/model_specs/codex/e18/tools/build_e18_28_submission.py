"""Build the verified C treatment as a stdlib-only, self-contained agent."""

import ast
import base64
import hashlib
import json
import zlib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]
DERIVED = BASE / "artifacts/derived"
PARTS = (
    (
        "run_e18_18_770_capacity_trajectory_gate_0b.py",
        (
            "PRODUCTS",
            "SAFE_PASS",
            "SEED_COSTS",
            "ANIMAL_COSTS",
            "LAND_COSTS",
            "_farm",
            "Gate0BController",
        ),
    ),
    (
        "e18_19_retrying_trajectory_controller.py",
        ("MOVES", "RetryingTrajectoryController"),
    ),
    ("e18_20_wheat_market_netting_controller.py", ("WheatMarketNettingController",)),
    (
        "e18_21_wheat_obligation_ledger_controller.py",
        ("WheatObligationLedgerController",),
    ),
    ("e18_22_wheat_jit_d1_controller.py", ("WheatJitD1Controller",)),
    ("e18_26_jesse_boost_d10_controller.py", ("JesseBoostD10Controller",)),
    ("e18_27_d10_d15_cashflow_controller.py", ("D10D15CashflowController",)),
    ("e18_28_full_season_controller.py", ("FullSeasonController",)),
)
PLANS = {
    "_PLAN": "E18_28_FULL_SEASON_C_PLAN_V1.json",
    "_PARENT_27_PLAN": "E18_27_770_D10_D15_CASHFLOW_PLAN_V3.json",
    "_PARENT_26_PLAN": "E18_26_770_JESSE_BOOST_D10_PLAN_V1.json",
}


def build():
    hashes = {}
    chunks = [
        '"""E18.28 C: fixed 770, full-season Carrot. Daily external diagnostic; not incumbent promotion."""',
        "from __future__ import annotations",
        "import base64\nimport json\nimport zlib\nfrom collections import Counter, defaultdict\nfrom copy import deepcopy\nfrom typing import Any",
        "SHED_ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))",
    ]
    for filename, names in PARTS:
        path = BASE / "tools" / filename
        hashes[str(path.relative_to(ROOT)).replace("\\", "/")] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        source = path.read_text(encoding="utf-8")
        found = set()
        for node in ast.parse(source).body:
            name = getattr(node, "name", None)
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                name = getattr(node.targets[0], "id", None)
            if isinstance(node, ast.AnnAssign):
                name = getattr(node.target, "id", None)
            if name in names:
                segment = ast.get_source_segment(source, node)
                segment = segment.replace(
                    "json.loads(PARENT_PLAN.read_text())", "deepcopy(_PARENT_26_PLAN)"
                )
                segment = segment.replace(
                    "json.loads(PARENT.read_text())", "deepcopy(_PARENT_27_PLAN)"
                )
                chunks.append(segment)
                found.add(name)
        assert found == set(names), (filename, found)
    for symbol, filename in PLANS.items():
        path = DERIVED / filename
        hashes[str(path.relative_to(ROOT)).replace("\\", "/")] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        original = json.loads(path.read_text())
        minimal = {
            k: original[k]
            for k in ("trajectory", "daily", "treatment_config", "max_hires_per_turn")
            if k in original
        }
        minimal["daily"] = [
            {"day": r["day"], "planned_hands": r["planned_hands"]}
            for r in original["daily"]
        ]
        blob = base64.b85encode(
            zlib.compress(json.dumps(minimal, separators=(",", ":")).encode(), 9)
        ).decode()
        chunks.append(
            f"{symbol} = json.loads(zlib.decompress(base64.b85decode({blob!r})))"
        )
    chunks.extend(
        [
            'MODEL_VERSION = "E18.28-C-770-FULL-SEASON-V1"',
            f"SOURCE_HASHES = {hashes!r}",
            "def create_agent(run_context=None):\n    context = run_context or {}\n    return FullSeasonController(deepcopy(_PLAN), int(context.get('player_position', 0)), reference_plan=_PARENT_27_PLAN)",
            "_ACTIVE = {}",
            "def agent(observation, configuration=None):\n    seat = int(observation.get('player', 0))\n    step = int(observation.get('step', 0))\n    entry = _ACTIVE.get(seat)\n    if entry is None or step <= entry[0]:\n        policy = create_agent({'player_position': seat})\n    else:\n        policy = entry[1]\n    _ACTIVE[seat] = (step, policy)\n    return policy(observation, configuration)",
        ]
    )
    result = "\n\n".join(chunks) + "\n"
    compile(result, "submission_codex_e18_28_770.py", "exec")
    assert not any(
        x in result
        for x in ("read_text(", "kaggle_environments", "from agricola", "from docs.")
    )
    output = ROOT / "submission/submission_codex_e18_28_770.py"
    manifest_path = DERIVED / "E18_28_DAILY_SUBMISSION_MANIFEST.json"
    if manifest_path.exists():
        saved = json.loads(manifest_path.read_text())
        if saved.get("submission_id"):
            assert output.read_text(encoding="utf-8") == result, (
                "Published artifact is immutable; create a new version for changed sources."
            )
            assert (
                hashlib.sha256(output.read_bytes()).hexdigest()
                == saved["submission_sha256"]
            )
            assert saved["sources"] == hashes
            print(
                json.dumps(
                    {
                        "published_artifact_preserved": True,
                        "submission_id": saved["submission_id"],
                    }
                )
            )
            return
    output.write_text(result, encoding="utf-8")
    manifest = {
        "version": "E18.28 C",
        "variant": "C",
        "submission": str(output.relative_to(ROOT)).replace("\\", "/"),
        "submission_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "bytes": output.stat().st_size,
        "sources": hashes,
        "external_status": "NOT_SUBMITTED",
        "incumbent_promoted": False,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    build()
