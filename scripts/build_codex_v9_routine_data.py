#!/usr/bin/env python3
"""Generate the standalone Codex V9 routine table from replay 104498819."""

from __future__ import annotations

import hashlib
import json
import pprint
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "benchmark" / "104498819.json"
TARGET = ROOT / "src" / "agricola" / "strategy" / "codex_v9_routine_data.py"
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def main() -> int:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    steps = payload["steps"]
    actions = tuple(
        steps[index + 1][0].get("action") or SAFE_PASS
        for index in range(len(steps) - 1)
    )
    if len(actions) != 719:
        raise RuntimeError(f"expected 719 actions, observed {len(actions)}")
    canonical = json.dumps(actions, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()
    body = (
        '"""Generated action routine distilled from public replay 104498819.\n\n'
        "Do not edit manually; regenerate with scripts/build_codex_v9_routine_data.py.\n"
        '"""\n\n'
        f'ROUTINE_SHA256 = "{digest}"\n'
        f"ROUTINE_ACTIONS = {pprint.pformat(actions, width=100, sort_dicts=False)}\n"
    )
    TARGET.write_text(body, encoding="utf-8", newline="\n")
    print(f"wrote {TARGET}")
    print(f"actions={len(actions)} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
