"""Run the seat-balanced Copilot, Antigravity, and Codex 3Q round robin."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agricola.strategy.antigravity.agent_c2_100k_central import (
    create_agent as create_antigravity,
)
from agricola.strategy.copilot.three_quadrant import CopilotThreeQAgent

DEFAULT_SEEDS = (26090101, 26090102, 26090103)


def _load_codex() -> Callable[[dict[str, Any], Any], dict[str, Any]]:
    import importlib.util

    path = ROOT / "submission" / "submission_codex.py"
    spec = importlib.util.spec_from_file_location("copilot_tournament_codex", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load Codex entrypoint from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.agent


def _new_agent(name: str, codex: Callable[[dict[str, Any], Any], dict[str, Any]]) -> Callable:
    if name == "copilot":
        return CopilotThreeQAgent()
    if name == "antigravity":
        return create_antigravity()
    if name == "codex":
        return codex
    raise ValueError(f"Unknown candidate: {name}")


def _run_match(
    seed: int,
    p0_name: str,
    p1_name: str,
    codex: Callable[[dict[str, Any], Any], dict[str, Any]],
) -> dict[str, Any]:
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
    )
    env.run([_new_agent(p0_name, codex), _new_agent(p1_name, codex)])
    p0_money = float(env.steps[-1][0]["observation"]["farms"][0]["money"])
    p1_money = float(env.steps[-1][1]["observation"]["farms"][1]["money"])
    return {
        "seed": seed,
        "p0": p0_name,
        "p1": p1_name,
        "p0_money": p0_money,
        "p1_money": p1_money,
        "winner": p0_name if p0_money > p1_money else p1_name if p1_money > p0_money else "tie",
    }


def run_tournament(seeds: tuple[int, ...], output: Path) -> dict[str, Any]:
    """Run every pair twice per seed, once in each seat."""
    codex = _load_codex()
    pairs = (("antigravity", "copilot"), ("codex", "copilot"), ("antigravity", "codex"))
    matches = [
        _run_match(seed, p0, p1, codex)
        for seed in seeds
        for first, second in pairs
        for p0, p1 in ((first, second), (second, first))
    ]
    standings: dict[str, dict[str, Any]] = {
        candidate: {"wins": 0, "losses": 0, "ties": 0, "money": []}
        for candidate in ("antigravity", "codex", "copilot")
    }
    for match in matches:
        for seat in ("p0", "p1"):
            candidate = match[seat]
            standings[candidate]["money"].append(match[f"{seat}_money"])
        if match["winner"] == "tie":
            standings[match["p0"]]["ties"] += 1
            standings[match["p1"]]["ties"] += 1
        else:
            loser = match["p1"] if match["winner"] == match["p0"] else match["p0"]
            standings[match["winner"]]["wins"] += 1
            standings[loser]["losses"] += 1
    for values in standings.values():
        values["mean_money"] = statistics.mean(values.pop("money"))

    result = {
        "protocol": "COPILOT_C2_3Q_TRIANGULAR_V1",
        "seeds": list(seeds),
        "seat_balanced": True,
        "matches": matches,
        "standings": standings,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=DEFAULT_SEEDS)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "model_spec_c2" / "copilot" / "COPILOT_3Q_TRIANGULAR_RESULTS.json",
    )
    args = parser.parse_args()
    result = run_tournament(tuple(args.seeds), args.output)
    for candidate, standing in result["standings"].items():
        print(
            f"{candidate}: {standing['wins']}W-{standing['losses']}L-{standing['ties']}T "
            f"mean ${standing['mean_money']:,.2f}"
        )
