#!/usr/bin/env python3
"""Real-engine intake for the active E18 peer V2 roster.

Antigravity is intentionally absent until a new callable release exists.  The
matrix keeps two Codex references: V4D as the economic control and E18.1 as
the failed topology ablation.  Claude and Copilot are evaluated from their V2
factories; synthetic peer artifacts are never imported as results.
"""

from __future__ import annotations

import itertools
import json
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agricola.strategy.claude.e18_opponent_reactive_v2 import (
    DEFAULT_CONFIG_PATH as CLAUDE_CONFIG,
)
from agricola.strategy.claude.e18_opponent_reactive_v2 import (
    create_claude_e18_agent_v2,
)
from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4D_CONFIG_PATH,
    create_codex_e17_batched_cluster_routing_v4,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH as E18_CONFIG,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    create_codex_e18_opponent_reactive_topology,
)
from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
    DEFAULT_CONFIG_PATH as COPILOT_CONFIG,
)
from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
    create_copilot_e18_opponent_reactive_v2,
)
from experiments.e18.tools.common import (
    run_e18_four_agent_reactive_tournament_v2 as common,
)

MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    ROOT
    / "experiments/e18/artifacts/derived/common/"
    / "E18_PEER_V2_REAL_ENGINE_INTAKE_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")

V4D = "CODEX_E17_V4D_CONTROL"
E18 = "CODEX_E18_1_ABLATION"
CLAUDE = "CLAUDE_E18_2"
COPILOT = "COPILOT_E18_2"
PARTICIPANTS = (V4D, E18, CLAUDE, COPILOT)
PAIRS = tuple(itertools.combinations(PARTICIPANTS, 2))
TARGET_MONEY = 100_000.0

SOURCES = {
    V4D: ROOT / "src/agricola/strategy/codex/codex_e17_batched_cluster_routing_v4.py",
    E18: ROOT / "src/agricola/strategy/codex/codex_e18_opponent_reactive_topology.py",
    CLAUDE: ROOT / "src/agricola/strategy/claude/e18_opponent_reactive_v2.py",
    COPILOT: ROOT / "src/agricola/strategy/copilot/e18_opponent_reactive_v2.py",
}
CONFIGS = {
    V4D: Path(DEFAULT_V4D_CONFIG_PATH),
    E18: Path(E18_CONFIG),
    CLAUDE: Path(CLAUDE_CONFIG),
    COPILOT: Path(COPILOT_CONFIG),
}


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-PEER-V2-INTAKE-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-PEER-V2-INTAKE-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == V4D:
        policy = create_codex_e17_batched_cluster_routing_v4(
            run_context=context,
            config_path=DEFAULT_V4D_CONFIG_PATH,
        )
        return policy, policy.codex_e17_batched_cluster_routing_instance
    if name == E18:
        policy = create_codex_e18_opponent_reactive_topology(run_context=context)
        return policy, policy.codex_e18_opponent_reactive_instance
    if name == CLAUDE:
        policy = create_claude_e18_agent_v2(run_context=context)
        return policy, policy
    if name == COPILOT:
        policy = create_copilot_e18_opponent_reactive_v2(run_context=context)
        return policy, policy
    raise ValueError(name)


def _controller_diagnostics(_name: str, controller: Any) -> tuple[int, int]:
    errors = int(
        getattr(
            controller,
            "error_count",
            getattr(controller, "technical_errors", 0),
        )
    )
    return errors, int(getattr(controller, "fallback_count", 0))


def _regime_metrics(name: str, controller: Any) -> dict[str, Any]:
    if name == V4D:
        return {
            "final_regime": "STATIC_V4D",
            "regime_signature": ["STATIC_V4D"],
            "mode_decisions": 0,
            "regime_transitions": 0,
            "decision_day": None,
            "decision_pressure": None,
        }
    telemetry = controller.telemetry_snapshot()
    if name == E18:
        mode = telemetry.get("topology_mode")
        return {
            "final_regime": mode,
            "regime_signature": [mode] if mode else [],
            "mode_decisions": int(telemetry.get("mode_decisions", 0)),
            "regime_transitions": len(telemetry.get("regime_transitions", [])),
            "decision_day": telemetry.get("mode_decision_day"),
            "decision_pressure": telemetry.get("mode_decision_pressure"),
        }
    if name == CLAUDE:
        mode = telemetry.get("regime")
        history = [
            item.get("regime")
            for item in telemetry.get("regime_transitions", [])
            if isinstance(item, dict) and item.get("regime")
        ]
        regimes = sorted({*history, *([mode] if mode else [])})
        return {
            "final_regime": mode,
            "regime_signature": regimes,
            "mode_decisions": int(telemetry.get("mode_decisions", 0)),
            "regime_transitions": len(history),
            "decision_day": telemetry.get("regime_decision_day"),
            "decision_pressure": telemetry.get("regime_decision_pressure"),
        }
    mode = telemetry.get("current_regime")
    history = [str(value) for value in telemetry.get("regime_history", [])]
    regimes = sorted({*history, *([str(mode)] if mode else [])})
    return {
        "final_regime": mode,
        "regime_signature": regimes,
        "mode_decisions": int(telemetry.get("transition_count", len(history))),
        "regime_transitions": int(telemetry.get("transition_count", len(history))),
        "decision_day": telemetry.get("decision_day"),
        "decision_pressure": telemetry.get("decision_pressure"),
    }


def _gates(standings: dict[str, dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for participant, row in standings.items():
        common_checks = {
            "zero_technical_errors": row["technical_errors"] == 0,
            "zero_fallbacks": row["fallbacks"] == 0,
            "zero_verified_livestock_losses": row["verified_livestock_losses"] == 0,
        }
        if participant == V4D:
            checks = {**common_checks, "economic_100k": row["money_mean"] >= TARGET_MONEY}
        elif participant == E18:
            checks = {
                **common_checks,
                "economic_100k": row["money_mean"] >= TARGET_MONEY,
                "at_least_two_regimes": len(row["activated_regimes"]) >= 2,
            }
        else:
            checks = {
                **common_checks,
                "economic_m1_15k": row["money_mean"] >= 15_000,
                "at_least_two_regimes": len(row["activated_regimes"]) >= 2,
                "conditioned_action_divergence_12_of_14": (
                    row["action_divergence"]["divergent_groups"] >= 12
                ),
                "conditioned_architecture_divergence_12_of_14": (
                    row["architecture_divergence"]["divergent_groups"] >= 12
                ),
            }
        result[participant] = {"checks": checks, "passed": all(checks.values())}
    return result


def _configure_common() -> None:
    common.PARTICIPANTS = PARTICIPANTS
    common.PAIRS = PAIRS
    common.TARGET_MONEY = TARGET_MONEY
    common.OUTPUT_JSON = OUTPUT_JSON
    common.OUTPUT_CSV = OUTPUT_CSV
    common._factory = _factory
    common._controller_diagnostics = _controller_diagnostics
    common._regime_metrics = _regime_metrics


def _run_spec(index: int, seed: int, p0: str, p1: str) -> tuple[int, dict[str, Any]]:
    _configure_common()
    return index, common._run_match(seed, p0, p1)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(value) for value in manifest["seed_policy"]["development"]]
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(int, manifest["seed_policy"]["final_confirmation"]["seeds"]),
    }
    if set(seeds).intersection(reserved):
        raise RuntimeError("development matrix overlaps a reserved seed")

    _configure_common()
    specs: list[tuple[int, int, str, str]] = []
    for left, right in PAIRS:
        for seed in seeds:
            for p0, p1 in ((left, right), (right, left)):
                specs.append((len(specs), seed, p0, p1))
    total = len(specs)
    completed: dict[int, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(_run_spec, index, seed, p0, p1): (index, seed, p0, p1)
            for index, seed, p0, p1 in specs
        }
        for future in as_completed(futures):
            index, seed, p0, p1 = futures[future]
            returned_index, match = future.result()
            if returned_index != index:
                raise RuntimeError("worker returned a mismatched matrix index")
            completed[index] = match
            print(
                f"[{len(completed):02d}/{total}] seed={seed} {p0} vs {p1} "
                f"winner={match['winner']} margin_p0={match['margin_p0']:.0f}",
                flush=True,
            )
    matches = [completed[index] for index in range(total)]

    standings = common._aggregate(matches)
    provenance = {
        name: {
            "source": str(SOURCES[name].relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": common._sha256(SOURCES[name]),
            "config": str(CONFIGS[name].relative_to(ROOT)).replace("\\", "/"),
            "config_sha256": common._sha256(CONFIGS[name]),
        }
        for name in PARTICIPANTS
    }
    payload = {
        "schema_version": "E18_PEER_V2_REAL_ENGINE_INTAKE_V1",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "date": "2026-09-03",
        "engine": "kaggle_environments/kaggriculture",
        "participants": list(PARTICIPANTS),
        "excluded_participants": {
            "ANTIGRAVITY_E17_OBSOLETE": "UNTIL_NEW_RELEASE"
        },
        "pairs": [list(pair) for pair in PAIRS],
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "provenance": provenance,
        "standings": standings,
        "head_to_head": common._head_to_head(matches),
        "gates": _gates(standings),
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    common._write_csv(matches)
    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
