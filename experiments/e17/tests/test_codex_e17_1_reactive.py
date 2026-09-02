from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.strategy.codex.codex_3q_mixed_high_density import create_v9_agent
from agricola.strategy.codex.codex_e17_reactive_guarded import (
    REACTIVE_MODEL_SPEC_VERSION,
    create_codex_e17_reactive_agent,
    load_reactive_config,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
REPLAY = REPO_ROOT / "data/replays/reference/104498819.json"


def _observation(step: int = 195) -> tuple[dict, dict]:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    observation = deepcopy(replay["steps"][step][0]["observation"])
    configuration = deepcopy(replay["configuration"])
    return observation, configuration


def _set_wheat(private: dict, quantity: int) -> None:
    private.setdefault("shed", {})["WHEAT"] = quantity
    for inventory in private.get("inventories", []) or []:
        if isinstance(inventory, dict):
            inventory["WHEAT"] = 0


def test_config_is_bounded_to_one_causal_family() -> None:
    config = load_reactive_config()
    assert config["model_spec_version"] == REACTIVE_MODEL_SPEC_VERSION
    assert config["causal_family"] == "WHEAT_FEED_SERVICEABILITY"
    assert config["base_policy"] == "CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY"


def test_safe_state_preserves_v9_action_exactly() -> None:
    observation, configuration = _observation()
    _set_wheat(observation["private"], 100)
    baseline = create_v9_agent()(deepcopy(observation), configuration)
    candidate = create_codex_e17_reactive_agent()
    emitted = candidate(deepcopy(observation), configuration)
    assert emitted == baseline
    assert candidate.codex_e17_instance.override_count == 0


def test_unfilled_wheat_buy_changes_next_action() -> None:
    before, configuration = _observation(195)
    after, _ = _observation(196)
    _set_wheat(before["private"], 0)
    _set_wheat(after["private"], 0)
    stateful = create_codex_e17_reactive_agent()
    stateful(before, configuration)
    guarded_action = stateful(after, configuration)
    fresh_action = create_codex_e17_reactive_agent()(deepcopy(after), configuration)
    assert guarded_action != fresh_action
    assert stateful.codex_e17_instance.detected_unfilled_wheat_units > 0
    assert stateful.codex_e17_instance.override_count == 1


def test_same_step_critical_eod_hunger_can_override_worker_to_feed() -> None:
    observation, configuration = _observation(215)
    farm = observation["farms"][observation["player"]]
    private = observation["private"]
    target = None
    for row in farm["tiles"]:
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal"):
                tile["consecutive_unfed"] = 1
                tile["fed_today"] = False
                target = tile
                break
        if target is not None:
            break
    assert target is not None
    # Move the farmer onto that animal and give that unit WHEAT.
    for y, row in enumerate(farm["tiles"]):
        for x, tile in enumerate(row):
            if tile is target:
                farm["farmer"] = [x, y]
    private["inventories"][0]["WHEAT"] = 1
    candidate = create_codex_e17_reactive_agent()
    action = candidate(observation, configuration)
    assert action["farmer"] == ["FEED"]
    assert candidate.codex_e17_instance.override_reasons["CRITICAL_FEED_OVERRIDE"] == 1


def test_short_smoke_has_no_policy_errors() -> None:
    candidate = create_codex_e17_reactive_agent()
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 72, "seed": 26090101, "turnsPerDay": 24},
        debug=True,
    )
    env.run([candidate, inert_pass_policy])
    assert candidate.codex_e17_instance.error_count == 0
    assert candidate.codex_e17_instance.fallback_count == 0
