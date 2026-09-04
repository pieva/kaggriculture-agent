from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4D_CONFIG_PATH,
    create_codex_e17_batched_cluster_routing_v4,
    load_v4_config,
)
from agricola.strategy.codex.codex_e17_post_feed_capacity_routing_v5_d27 import (
    V5_D27_MODEL_SPEC_VERSION,
    create_codex_e17_post_feed_capacity_routing_v5_d27,
    load_v5_d27_config,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
REPLAY = REPO_ROOT / "data/replays/json/104498819.json"


def _observation(step: int) -> tuple[dict, dict]:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    return (
        deepcopy(replay["steps"][step][0]["observation"]),
        deepcopy(replay["configuration"]),
    )


def test_v5_d27_changes_only_activation_day_and_metadata() -> None:
    control = load_v4_config(DEFAULT_V4D_CONFIG_PATH)
    candidate = load_v5_d27_config()
    ignored = {
        "candidate_id",
        "schema_version",
        "model_spec_version",
        "base_policy",
        "causal_family",
        "activation_day",
    }
    assert candidate["model_spec_version"] == V5_D27_MODEL_SPEC_VERSION
    assert candidate["activation_day"] == 27
    assert control["activation_day"] == 28
    assert {key: value for key, value in candidate.items() if key not in ignored} == {
        key: value for key, value in control.items() if key not in ignored
    }


def test_v5_d27_matches_v4d_before_day_27() -> None:
    observation, configuration = _observation(647)
    candidate = create_codex_e17_post_feed_capacity_routing_v5_d27()
    control = create_codex_e17_batched_cluster_routing_v4(
        config_path=DEFAULT_V4D_CONFIG_PATH
    )
    assert candidate(deepcopy(observation), configuration) == control(
        deepcopy(observation), configuration
    )


def test_v5_d27_activates_routing_on_day_27() -> None:
    observation, configuration = _observation(648)
    candidate = create_codex_e17_post_feed_capacity_routing_v5_d27()
    candidate(deepcopy(observation), configuration)
    instance = candidate.codex_e17_batched_cluster_routing_instance
    assert instance.model_spec_version == V5_D27_MODEL_SPEC_VERSION
    assert len(instance.ledger_records) > 0
