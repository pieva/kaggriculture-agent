"""Development benchmark: Claude E17.1 V6 vs Codex V9/reactive, black-box.

Same harness as the V3 benchmark tool
(``run_claude_e17_1_v3_dev_benchmark_vs_codex.py``), pointed at V6
(MODEL_SPEC V6: workforce-gated home-quadrant clustering, fixing the
collapse pattern the E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3 report found in
V5) instead. Authorized by
``experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md``
(authorization is for the black-box benchmark method against these Codex
factories, not scoped to a single Claude version).
Imports only the public factory entry points of the frozen Codex candidates
to instantiate them as opponent callables for ``kaggle_environments.run``.
This is execution infrastructure, not a strategy dependency: nothing here is
imported by, or copied into, the Claude policy module
(``agricola.strategy.claude.e17_reactive_3q_v6``). No Codex source, config or
MODEL_SPEC is read or summarized by this tool or by the session that wrote
it; only the public factory names (obtained from the import lines of
``experiments/e17/tools/common/run_e17_reactive_three_way_development_exhibition.py``,
never Codex's own source) and observable match results are used.

Seeds are restricted programmatically to the development set; holdout and
final-confirmation seeds raise before the engine is invoked.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import kaggle_environments

from agricola.strategy.claude.e17_reactive_3q_v6 import create_claude_e17_agent_v6
from agricola.strategy.codex.codex_3q_mixed_high_density import create_v9_agent
from agricola.strategy.codex.codex_e17_reactive_guarded import (
    create_codex_e17_reactive_agent,
)

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

OPPONENT_FACTORIES = {
    "CODEX_V9": create_v9_agent,
    "CODEX_REACTIVE": create_codex_e17_reactive_agent,
}


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


def _run_match(seed: int, seat: int, opponent_id: str) -> dict[str, Any]:
    seed = _guarded_seed(seed)
    claude = create_claude_e17_agent_v6()
    opponent = OPPONENT_FACTORIES[opponent_id]()
    agents = [opponent, opponent]
    agents[seat] = claude
    env = kaggle_environments.make(
        "kaggriculture", configuration={"episodeSteps": EPISODE_STEPS, "seed": seed}
    )
    env.run(agents)
    terminal = env.steps[-1]
    own = terminal[seat]
    opp = terminal[1 - seat]
    final_obs = own.get("observation", {}) or {}
    # Shared public game state from Claude's own observation: farms is a
    # two-element list indexed by player, so farms[1-seat] is the
    # opponent's own observable board (tiles/hands/unlocked_quadrants),
    # not Codex source or routine. Authorized by
    # E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md
    # ("azioni finali eseguite... stato tile, quadranti sbloccati,
    # animali, timing").
    farms = final_obs.get("farms") or [{}, {}]
    own_farm = farms[seat] if len(farms) > seat else {}
    opp_farm = farms[1 - seat] if len(farms) > (1 - seat) else {}
    own_plant, own_weed, own_animal = _tile_counts(own_farm.get("tiles", []) or [])
    opp_plant, opp_weed, opp_animal = _tile_counts(opp_farm.get("tiles", []) or [])
    own_money = float(own.get("reward") or 0.0)
    opp_money = float(opp.get("reward") or 0.0)
    outcome = "W" if own_money > opp_money else ("L" if own_money < opp_money else "T")
    return {
        "seed": seed,
        "seat": seat,
        "opponent_id": opponent_id,
        "status": own.get("status"),
        "opponent_status": opp.get("status"),
        "claude_final_money": own_money,
        "opponent_final_money": opp_money,
        "outcome": outcome,
        "claude_technical_errors": claude.technical_errors,
        "unlocked_quadrants": list(own_farm.get("unlocked_quadrants", []) or []),
        "crop_tiles_final": own_plant,
        "weed_tiles_final": own_weed,
        "animals_final": own_animal,
        "hands_final": len(own_farm.get("hands", []) or []),
        "opponent_unlocked_quadrants": list(opp_farm.get("unlocked_quadrants", []) or []),
        "opponent_crop_tiles_final": opp_plant,
        "opponent_weed_tiles_final": opp_weed,
        "opponent_animals_final": opp_animal,
        "opponent_hands_final": len(opp_farm.get("hands", []) or []),
    }


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    seeds = DEVELOPMENT_SEEDS if not argv else tuple(int(a) for a in argv)
    for seed in seeds:
        _guarded_seed(seed)

    results: list[dict[str, Any]] = []
    for opponent_id in OPPONENT_FACTORIES:
        for seed in seeds:
            for seat in (0, 1):
                record = _run_match(seed, seat, opponent_id)
                results.append(record)
                print(
                    f"{opponent_id} seed={seed} seat={seat}: "
                    f"claude={record['claude_final_money']:.0f} "
                    f"opponent={record['opponent_final_money']:.0f} "
                    f"outcome={record['outcome']} "
                    f"3Q={record['unlocked_quadrants']} "
                    f"crop={record['crop_tiles_final']} weed={record['weed_tiles_final']} "
                    f"animal={record['animals_final']} hands={record['hands_final']} | "
                    f"opp_3Q={record['opponent_unlocked_quadrants']} "
                    f"opp_crop={record['opponent_crop_tiles_final']} "
                    f"opp_weed={record['opponent_weed_tiles_final']} "
                    f"opp_animal={record['opponent_animals_final']} "
                    f"opp_hands={record['opponent_hands_final']}",
                    flush=True,
                )

    money = [r["claude_final_money"] for r in results]
    opp_money = [r["opponent_final_money"] for r in results]
    wins = sum(1 for r in results if r["outcome"] == "W")
    ties = sum(1 for r in results if r["outcome"] == "T")
    losses = sum(1 for r in results if r["outcome"] == "L")
    print(f"\nMATCHES={len(results)} W-T-L={wins}-{ties}-{losses}")
    print(f"CLAUDE_MEAN_MONEY={mean(money):.2f}")
    print(f"OPPONENT_MEAN_MONEY={mean(opp_money):.2f}")
    print(f"CLAUDE_MEAN_HANDS_FINAL={mean(r['hands_final'] for r in results):.2f}")
    print(f"OPPONENT_MEAN_HANDS_FINAL={mean(r['opponent_hands_final'] for r in results):.2f}")
    print(f"CLAUDE_MEAN_CROP_TILES_FINAL={mean(r['crop_tiles_final'] for r in results):.2f}")
    print(f"OPPONENT_MEAN_CROP_TILES_FINAL={mean(r['opponent_crop_tiles_final'] for r in results):.2f}")
    print(f"CLAUDE_MEAN_ANIMALS_FINAL={mean(r['animals_final'] for r in results):.2f}")
    print(f"OPPONENT_MEAN_ANIMALS_FINAL={mean(r['opponent_animals_final'] for r in results):.2f}")
    print(f"TECH_ERRORS={sum(r['claude_technical_errors'] for r in results)}")

    out_path = (
        REPOSITORY_ROOT
        / "experiments"
        / "e17"
        / "artifacts"
        / "derived"
        / "claude"
        / "E17_1_V6_DEV_BENCHMARK_VS_CODEX.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "results": results,
                "mean_money": mean(money),
                "opponent_mean_money": mean(opp_money),
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
