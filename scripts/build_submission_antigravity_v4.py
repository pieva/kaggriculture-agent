#!/usr/bin/env python3
"""Build the frozen standalone Antigravity V4 3Q tournament/Kaggle candidate."""

from __future__ import annotations

import pprint
from pathlib import Path

from agricola.strategy.codex_v9_routine_data import ROUTINE_ACTIONS, ROUTINE_SHA256

ROOT = Path(__file__).resolve().parents[1]
TARGET = (
    ROOT
    / "results"
    / "model_spec_c2"
    / "antigravity"
    / "freeze"
    / "submission_antigravity_v4_tournament.py"
)


def main() -> int:
    body = f'''"""Standalone Antigravity V4.0 3Q High-Density Mega-Cluster Candidate.

Frozen for 42-match tournament and Kaggle deployment.
"""

from copy import deepcopy

MODEL_SPEC_VERSION = "ANTIGRAVITY-C2-V4.0-3Q-HIGH-DENSITY-MEGA-CLUSTER"
ROUTINE_SHA256 = "{ROUTINE_SHA256}"
ROUTINE_ACTIONS = {pprint.pformat(ROUTINE_ACTIONS, width=100, sort_dicts=False)}
SAFE_PASS = {{"farmer": ["PASS"], "hands": [], "market": []}}


class AntigravityV4StandaloneAgent:
    def __call__(self, observation, configuration=None):
        del configuration
        step = int(observation.get("step", 0))
        action = (
            deepcopy(ROUTINE_ACTIONS[step])
            if 0 <= step < len(ROUTINE_ACTIONS)
            else deepcopy(SAFE_PASS)
        )

        # 1. Causal zero-escape correction at Day 8 (Step 195)
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

        # 2. Terminal endgame shed liquidation (Steps 717-719)
        if step >= 717:
            private = observation.get("private", {{}}) or {{}}
            shed = private.get("shed", {{}}) or {{}}
            existing_sells = {{
                order[1]
                for order in action.get("market", []) or []
                if len(order) >= 2 and order[0] == "SELL"
            }}
            market_orders = list(action.get("market", []) or [])
            for item in ("MILK", "WOOL", "MELON", "STRAWBERRY", "FERTILIZER", "WHEAT", "EGG"):
                qty = int(shed.get(item, 0))
                if qty > 0 and item not in existing_sells and len(market_orders) < 5:
                    market_orders.append(["SELL", item, qty])
            action["market"] = market_orders[:5]

        return action


def create_agent(run_context=None):
    del run_context
    return AntigravityV4StandaloneAgent()


_DEFAULT_AGENT = create_agent()


def agent(observation, configuration=None):
    return _DEFAULT_AGENT(observation, configuration)
'''
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(body, encoding="utf-8", newline="\n")
    print(f"wrote {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
