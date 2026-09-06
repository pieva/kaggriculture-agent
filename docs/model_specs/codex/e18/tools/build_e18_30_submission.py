"""Build E18.30 CROP_POOL without changing the published parent artifact."""

import ast
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]
DERIVED = BASE / "artifacts/derived"
PARENT_SHA = "8788f68c74b95c56c21feffba6fd5c49654d1c2dc5e71b5a0ca94800f988969d"
OUTPUT = ROOT / "submission/submission_codex_e18_30_770.py"


def segment(source, node):
    first = min([node.lineno, *(d.lineno for d in getattr(node, "decorator_list", []))])
    return "\n".join(source.splitlines()[first - 1 : node.end_lineno])


def build():
    parent = ROOT / "submission/submission_codex_e18_28_770.py"
    assert hashlib.sha256(parent.read_bytes()).hexdigest() == PARENT_SHA
    source = parent.read_text(encoding="utf-8")
    chunks = []
    hashes = {str(parent.relative_to(ROOT)).replace("\\", "/"): PARENT_SHA}
    for node in ast.parse(source).body:
        name = getattr(node, "name", None)
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            name = getattr(node.targets[0], "id", None)
        if name not in {
            "MODEL_VERSION",
            "SOURCE_HASHES",
            "create_agent",
            "_ACTIVE",
            "agent",
        }:
            chunks.append(segment(source, node))
    chunks.append(
        "from collections.abc import Iterable, Mapping\nfrom dataclasses import dataclass, field\nfrom enum import Enum\nfrom math import isfinite"
    )
    for filename in ("e18_30_mission_dispatcher.py", "e18_30_mission_runtime.py"):
        path = BASE / "tools" / filename
        hashes[str(path.relative_to(ROOT)).replace("\\", "/")] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        text = path.read_text(encoding="utf-8")
        for node in ast.parse(text).body:
            if isinstance(
                node, (ast.FunctionDef, ast.ClassDef, ast.Assign, ast.AnnAssign)
            ):
                chunks.append(segment(text, node))
    chunks.extend(
        [
            'MODEL_VERSION = "E18.30-CROP-POOL-770-V2"',
            f"SOURCE_HASHES = {hashes!r}",
            "def create_agent(run_context=None):\n    context = run_context or {}\n    return MissionRuntimeController(deepcopy(_PLAN), int(context.get('player_position', 0)), variant='CROP_POOL', reference_plan=_PARENT_27_PLAN)",
            "_ACTIVE = {}",
            "def agent(observation, configuration=None):\n    seat = int(observation.get('player', 0))\n    step = int(observation.get('step', 0))\n    entry = _ACTIVE.get(seat)\n    if entry is None or step <= entry[0]:\n        policy = create_agent({'player_position': seat})\n    else:\n        policy = entry[1]\n    _ACTIVE[seat] = (step, policy)\n    return policy(observation, configuration)",
        ]
    )
    result = "\n\n".join(chunks) + "\n"
    result = result.replace(
        '"""E18.28 C: fixed 770, full-season Carrot. Daily external diagnostic; not incumbent promotion."""',
        '"""E18.30 CROP_POOL V2: fixed 770, observed mission dispatch; internal development."""',
    )
    compile(result, str(OUTPUT), "exec")
    assert not any(
        s in result
        for s in ("read_text(", "kaggle_environments", "from agricola", "from docs.")
    )
    if OUTPUT.exists():
        assert OUTPUT.read_text(encoding="utf-8") == result, (
            "Preserve prior artifact; use a new version"
        )
    else:
        OUTPUT.write_text(result, encoding="utf-8", newline="\n")
    manifest = {
        "version": "E18.30 CROP_POOL V2",
        "sources": hashes,
        "submission": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
        "submission_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "bytes": OUTPUT.stat().st_size,
        "external_status": "NOT_SUBMITTED",
        "incumbent_promoted": False,
        "holdout_consumed": False,
    }
    target = DERIVED / "E18_30_SUBMISSION_MANIFEST_V2.json"
    if target.exists():
        assert json.loads(target.read_text()) == manifest
    else:
        target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    build()
