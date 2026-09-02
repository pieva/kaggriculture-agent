#!/usr/bin/env python3
"""Build the frozen standalone Codex V9 tournament/Kaggle candidate."""

from __future__ import annotations

import pprint
from pathlib import Path

from agricola.strategy.codex.codex_v9_routine_data import ROUTINE_ACTIONS, ROUTINE_SHA256

ROOT = Path(__file__).resolve().parents[1]
TARGET = (
    ROOT
    / "docs"
    / "governance"
    / "history"
    / "model_spec_c2"
    / "codex"
    / "freeze"
    / "submission_codex_v9_tournament.py"
)


def build_submission_codex_v9(output_path: Path | str | None = None) -> Path:
    """Build V9 without ever defaulting to the canonical Kaggle path.

    Tests must pass a temporary ``output_path``.  Promotion to
    ``submission/submission_codex.py`` is an explicit copy step owned by the
    release workflow, not a side effect of this builder.
    """
    target = Path(output_path) if output_path is not None else TARGET
    body = f'''"""Standalone Codex V9.0 3Q mixed high-density candidate.

Frozen for local tournament before any Kaggle promotion.
"""

from copy import deepcopy

MODEL_SPEC_VERSION = "CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY"
ROUTINE_SHA256 = "{ROUTINE_SHA256}"
ROUTINE_ACTIONS = {pprint.pformat(ROUTINE_ACTIONS, width=100, sort_dicts=False)}
SAFE_PASS = {{"farmer": ["PASS"], "hands": [], "market": []}}


class CodexV9StandaloneAgent:
    def __call__(self, observation, configuration=None):
        del configuration
        step = int(observation.get("step", 0))
        action = (
            deepcopy(ROUTINE_ACTIONS[step])
            if 0 <= step < len(ROUTINE_ACTIONS)
            else deepcopy(SAFE_PASS)
        )
        if step == 195:
            for order in action.get("market", []) or []:
                if order[:2] == ["BUY_PRODUCT", "WHEAT"]:
                    order[2] = max(4, int(order[2]))
                    break
            action["market"] = [
                order
                for order in action.get("market", []) or []
                if order[:2] != ["BUY_ANIMAL", "COW"]
            ]
        return action


def create_agent(run_context=None):
    del run_context
    return CodexV9StandaloneAgent()


_DEFAULT_AGENT = create_agent()


def agent(observation, configuration=None):
    return _DEFAULT_AGENT(observation, configuration)
'''
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8", newline="\n")
    return target


def main() -> int:
    target = build_submission_codex_v9()
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
