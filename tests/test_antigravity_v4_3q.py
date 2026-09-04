"""Tests for the sole active Antigravity V4 3Q baseline."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from kaggle_environments import make

from agricola.strategy.antigravity import V4_SPEC_VERSION, create_agent


def test_antigravity_v4_real_engine_prefix_is_fail_closed():
    policy = create_agent(
        run_context={"run_id": "test-v4", "episode_id": "prefix", "seed": 0}
    )
    env = make("kaggriculture", configuration={"episodeSteps": 48, "seed": 0})
    observations = env.reset()

    for _ in range(47):
        action = policy(observations[0].observation)
        assert set(action) == {"farmer", "hands", "market"}
        observations = env.step(
            [action, {"farmer": ["PASS"], "hands": [], "market": []}]
        )
        if observations[0].status != "ACTIVE":
            break

    instance = policy.antigravity_v4_instance
    assert instance.model_spec_version == V4_SPEC_VERSION
    assert instance.error_count == 0
    assert instance.fallback_count == 0


def test_antigravity_v4_archived_submission_matches_freeze():
    root = Path(__file__).resolve().parents[1]
    canonical = (
        root
        / "docs"
        / "model_specs"
        / "antigravity"
        / "archive"
        / "e16"
        / "artifacts"
        / "freeze"
        / "legacy_submissions"
        / "submission_antigravity.py"
    )
    frozen = (
        root
        / "docs"
        / "governance"
        / "history"
        / "model_spec_c2"
        / "antigravity"
        / "freeze"
        / "submission_antigravity_v4_tournament.py"
    )
    assert canonical.read_bytes() == frozen.read_bytes()

    spec = importlib.util.spec_from_file_location("antigravity_v4_submission", canonical)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    action = module.agent({"step": 9999})
    assert action == {"farmer": ["PASS"], "hands": [], "market": []}
