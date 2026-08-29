"""Verify the X1.12 Kaggle submission candidate against canonical source."""

import importlib.util
import json
from pathlib import Path
from typing import Any, Callable, Dict

from kaggle_environments import make

from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import (
    ProductiveMassConfig,
    ProductiveMassROIAgent,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SUBMISSION_PATH = PROJECT_ROOT / "submission" / "submission.py"
RESULT_PATH = PROJECT_ROOT / "results" / "e12" / "x112" / "submission_candidate_verification.json"
SEEDS = (0, 421521921)
EXPECTED_FINALS = {0: 42491.0, 421521921: 48313.0}


def _load_submission_agent(seed: int) -> Callable[[Dict[str, Any], Any], Dict[str, Any]]:
    spec = importlib.util.spec_from_file_location(f"x112_submission_{seed}", SUBMISSION_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load submission module from {SUBMISSION_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.agent


def _run_agent(agent: Callable[[Dict[str, Any], Any], Dict[str, Any]], seed: int) -> Dict[str, Any]:
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
    env.run([agent, "pass"])
    final_step = env.steps[-1][0]
    observation = final_step.get("observation", {})
    farm = observation.get("farms", [{}])[0]
    livestock = {"COW": 0, "SHEEP": 0}
    for row in farm.get("tiles", []):
        for tile in row:
            if not isinstance(tile, dict):
                continue
            animal = tile.get("animal")
            if animal in livestock:
                livestock[animal] += 1
    private = observation.get("private", {}) if isinstance(observation, dict) else {}
    shed = private.get("shed", {}) if isinstance(private, dict) else {}
    inventories = private.get("inventories", []) if isinstance(private, dict) else []
    for animal in livestock:
        livestock[animal] += shed.get(animal, 0) if isinstance(shed, dict) else 0
        for inventory in inventories if isinstance(inventories, list) else []:
            if isinstance(inventory, dict):
                livestock[animal] += inventory.get(animal, 0)
    unlocked = farm.get("unlocked_quadrants", [])
    owned_quadrants = len(unlocked) if isinstance(unlocked, list) else int(unlocked or 0)
    return {
        "final_money": float(final_step.get("reward", 0.0) or 0.0),
        "status": final_step.get("status", "UNKNOWN"),
        "owned_quadrants": owned_quadrants,
        "livestock": livestock,
    }


def _source_agent() -> Callable[[Dict[str, Any], Any], Dict[str, Any]]:
    config = ProductiveMassConfig(
        productive_core_mode="E12_TRUEBELIEF_ENGINE_X112",
        enable_land_expansion=True,
        target_cows=7,
        target_sheep=4,
        max_workers=6,
        stop_hire_day=1,
    )
    instance = ProductiveMassROIAgent(config=config)

    def agent(observation: Dict[str, Any], configuration: Any = None) -> Dict[str, Any]:
        return instance.act(GameState(observation))

    return agent


def main() -> int:
    if not SUBMISSION_PATH.exists():
        raise FileNotFoundError(SUBMISSION_PATH)

    results: Dict[str, Any] = {
        "mode": "E12_TRUEBELIEF_ENGINE_X112",
        "submission": str(SUBMISSION_PATH),
        "seeds": {},
    }
    ok = True

    for seed in SEEDS:
        source = _run_agent(_source_agent(), seed)
        submission = _run_agent(_load_submission_agent(seed), seed)
        expected = EXPECTED_FINALS[seed]
        seed_ok = (
            source == submission
            and submission["final_money"] == expected
            and submission["owned_quadrants"] == 2
            and submission["livestock"] == {"COW": 7, "SHEEP": 4}
        )
        ok = ok and seed_ok
        results["seeds"][str(seed)] = {
            "source": source,
            "submission": submission,
            "expected_final_money": expected,
            "pass": seed_ok,
        }

    results["pass"] = ok
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
