"""Focused tests for the single-lever V7.3 Q1 cadence iteration."""

from __future__ import annotations

from typing import Any

from agricola.strategy.codex_dual_q1_cadence import (
    CADENCE_MODEL_SPEC_VERSION,
    CodexDualQ1CadenceAgent,
    load_cadence_config,
)


def test_cadence_config_freezes_feed_q0_and_geometry():
    config = load_cadence_config()
    agent = CodexDualQ1CadenceAgent(config)

    assert agent.model_spec_version == CADENCE_MODEL_SPEC_VERSION
    assert len(agent.crop_positions) == 36
    assert len(agent.pasture_positions) == 12
    assert config["q1_activation_cash"] == 2800
    assert config["q1_cadence_relief"] == {
        "worker_role": "FERTILIZER_LOGISTICS_Q1",
        "eligible_tasks": ["ANIMAL_COLLECTION", "CARE"],
        "feed_ownership_unchanged": True,
        "q0_ownership_unchanged": True,
    }


def test_local_relief_only_adds_q1_collection_and_care(monkeypatch):
    agent = CodexDualQ1CadenceAgent(load_cadence_config())
    hard_crop = {"kind": "WATER", "target": (0, 0)}
    tasks: dict[str, list[dict[str, Any]]] = {
        "COW": [
            {"kind": "FEED", "target": (5, 3), "value": 160},
            {"kind": "CARE", "target": (6, 3), "value": 80},
        ],
        "SHEEP": [
            {"kind": "ANIMAL_COLLECTION", "target": (5, 2), "value": 200},
            {"kind": "FERTILIZER_COLLECTION", "target": (6, 2), "value": 100},
        ],
    }

    monkeypatch.setattr(
        agent,
        "_module_animal_tasks",
        lambda snapshot, module, species: tasks[species],
    )
    monkeypatch.setattr(
        CodexDualQ1CadenceAgent.__mro__[1],
        "_fertilizer_role_candidates",
        lambda self, snapshot, role, hard_crop_tasks: hard_crop_tasks,
    )
    candidates = agent._fertilizer_role_candidates(
        object(), "FERTILIZER_LOGISTICS_Q1", [hard_crop]  # type: ignore[arg-type]
    )

    assert candidates == [
        hard_crop,
        {**tasks["COW"][1], "value": 130},
        tasks["SHEEP"][0],
    ]
    assert all(task["kind"] not in {"FEED", "FERTILIZER_COLLECTION"} for task in candidates)
