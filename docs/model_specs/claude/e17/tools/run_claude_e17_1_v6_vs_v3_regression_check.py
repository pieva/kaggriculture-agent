"""Regression check: Claude V6 vs Claude V3, own-family, all 7 dev seeds.

The E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3 report found V5's worst collapses
specifically in direct Claude V5 vs Claude V3 play (money as low as `78`,
3Q reached only `28/42`), not in the V-vs-Codex black-box benchmark this
agent otherwise uses (`run_claude_e17_1_vN_dev_benchmark_vs_codex.py`).
V6's fix (MODEL_SPEC V6: workforce-gated clustering) was designed and
verified against one reproduced case from that report (seed `26090102`,
seat 1: money `78` -> `15,743`). This tool re-checks the fix across all 7
development seeds and both seat orientations before trusting it more
broadly -- both agents are this project's own Claude policy versions, so
no cross-agent black-box restriction applies.

Seeds are restricted programmatically to the development set; holdout and
final-confirmation seeds raise before the engine is invoked.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import kaggle_environments

from agricola.strategy.claude.e17_reactive_3q_v3 import create_claude_e17_agent_v3
from agricola.strategy.claude.e17_reactive_3q_v6 import create_claude_e17_agent_v6

DEVELOPMENT_SEEDS = (
    26090101,
    26090102,
    26090103,
    1838889274,
    1619968655,
    710418712,
    562040596,
)
_HOLDOUT_AND_FINAL_SEEDS = frozenset(
    {
        207899150,
        1866713870,
        1953344146,
        412628772,
        157353689,
        352254289,
        1182799305,
        1144076852,
        1172855418,
        1075728698,
    }
)
EPISODE_STEPS = 720
COLLAPSE_MONEY_FLOOR = 5000.0


class HoldoutSeedGuardError(Exception):
    pass


def _guarded_seed(seed: int) -> int:
    if seed not in DEVELOPMENT_SEEDS or seed in _HOLDOUT_AND_FINAL_SEEDS:
        raise HoldoutSeedGuardError(f"seed {seed} is not an authorized development seed")
    return seed


def _tile_counts(tiles: list[Any]) -> tuple[int, int, int]:
    plant = sum(1 for row in tiles for t in row if isinstance(t, dict) and t.get("kind") == "PLANT")
    weed = sum(1 for row in tiles for t in row if isinstance(t, dict) and t.get("kind") == "WEED")
    animal = sum(1 for row in tiles for t in row if isinstance(t, dict) and "animal" in t)
    return plant, weed, animal


def _run_match(seed: int, seat: int) -> dict[str, Any]:
    seed = _guarded_seed(seed)
    v6 = create_claude_e17_agent_v6()
    v3 = create_claude_e17_agent_v3()
    agents = [v3, v3]
    agents[seat] = v6
    env = kaggle_environments.make(
        "kaggriculture", configuration={"episodeSteps": EPISODE_STEPS, "seed": seed}
    )
    env.run(agents)
    terminal = env.steps[-1]
    own = terminal[seat]
    opp = terminal[1 - seat]
    final_obs = own.get("observation", {}) or {}
    farms = final_obs.get("farms") or [{}, {}]
    own_farm = farms[seat] if len(farms) > seat else {}
    own_plant, own_weed, own_animal = _tile_counts(own_farm.get("tiles", []) or [])
    own_money = float(own.get("reward") or 0.0)
    opp_money = float(opp.get("reward") or 0.0)
    outcome = "W" if own_money > opp_money else ("L" if own_money < opp_money else "T")
    return {
        "seed": seed,
        "seat": seat,
        "v6_final_money": own_money,
        "v3_final_money": opp_money,
        "outcome": outcome,
        "v6_technical_errors": v6.technical_errors,
        "unlocked_quadrants": list(own_farm.get("unlocked_quadrants", []) or []),
        "reached_3q": len(own_farm.get("unlocked_quadrants", []) or []) >= 3,
        "crop_tiles_final": own_plant,
        "weed_tiles_final": own_weed,
        "animals_final": own_animal,
        "hands_final": len(own_farm.get("hands", []) or []),
    }


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    seeds = DEVELOPMENT_SEEDS if not argv else tuple(int(a) for a in argv)
    for seed in seeds:
        _guarded_seed(seed)

    results: list[dict[str, Any]] = []
    for seed in seeds:
        for seat in (0, 1):
            record = _run_match(seed, seat)
            results.append(record)
            print(
                f"seed={seed} seat={seat}: v6={record['v6_final_money']:.0f} "
                f"v3={record['v3_final_money']:.0f} outcome={record['outcome']} "
                f"3Q={record['unlocked_quadrants']} crop={record['crop_tiles_final']} "
                f"weed={record['weed_tiles_final']} animal={record['animals_final']} "
                f"hands={record['hands_final']}",
                flush=True,
            )

    money = [r["v6_final_money"] for r in results]
    wins = sum(1 for r in results if r["outcome"] == "W")
    ties = sum(1 for r in results if r["outcome"] == "T")
    losses = sum(1 for r in results if r["outcome"] == "L")
    reached_3q = sum(1 for r in results if r["reached_3q"])
    collapses = [r for r in results if r["v6_final_money"] < COLLAPSE_MONEY_FLOOR]
    print(f"\nMATCHES={len(results)} W-T-L={wins}-{ties}-{losses}")
    print(f"V6_MEAN_MONEY={mean(money):.2f}")
    print(f"V6_MIN_MONEY={min(money):.2f}")
    print(f"V6_REACHED_3Q={reached_3q}/{len(results)}")
    print(f"V6_COLLAPSES_BELOW_{COLLAPSE_MONEY_FLOOR:.0f}={len(collapses)}")
    for r in collapses:
        print(f"  COLLAPSE seed={r['seed']} seat={r['seat']} money={r['v6_final_money']:.0f}")
    print(f"TECH_ERRORS={sum(r['v6_technical_errors'] for r in results)}")

    out_path = (
        REPOSITORY_ROOT
        / "docs" / "model_specs" / "claude" / "e17" / "artifacts" / "derived"
        / "E17_1_V6_VS_V3_REGRESSION_CHECK.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "results": results,
                "mean_money": mean(money),
                "min_money": min(money),
                "reached_3q": reached_3q,
                "w_t_l": [wins, ties, losses],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"WRITTEN={out_path.relative_to(REPOSITORY_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
