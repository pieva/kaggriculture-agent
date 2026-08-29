"""Frozen protocol identity tests for E16."""

from __future__ import annotations

from copy import deepcopy

import pytest

from agricola.e16.config import (
    EXPECTED_LEGACY_CONFIG_SHA256,
    EXPECTED_LEGACY_TREATMENT_SHA256,
    EXPECTED_OPPONENT_SHA256,
    LEGACY_CONFIG_PATH,
    MANIPULATED_FIELDS,
    REPO_ROOT,
    ConfigError,
    build_run_matrix,
    load_frozen_config,
    resolve_cell,
    sha256_file,
    validate_frozen_config,
    validate_run_identity,
)


@pytest.fixture(scope="module")
def frozen_config():
    return load_frozen_config()


def test_e16_opponent_path_and_hash(frozen_config):
    path = REPO_ROOT / frozen_config["opponent_path"]
    assert path.is_file()
    assert (
        sha256_file(path)
        == EXPECTED_OPPONENT_SHA256
        == frozen_config["opponent_sha256"]
    )


def test_e16_exact_cell_counts(frozen_config):
    assert len(frozen_config["stage_a_cells"]) == 7
    assert len(frozen_config["stage_b_cells"]) == 5


def test_e16_exact_stage_a_values(frozen_config):
    values = {
        cell_id: (cell["watering_dispatch_priority"], cell["crop_working_set_target"])
        for cell_id, cell in frozen_config["stage_a_cells"].items()
    }
    assert values == {
        "A01": (0.20, 10),
        "A02": (0.70, 10),
        "A03": (0.20, 25),
        "A04": (0.70, 25),
        "A05": (0.45, 17),
        "A06": (0.45, 25),
        "A07": (0.70, 17),
    }


def test_e16_exact_stage_b_values(frozen_config):
    values = {
        cell_id: (cell["livestock_headcount_target"], cell["pasture_allocation_target"])
        for cell_id, cell in frozen_config["stage_b_cells"].items()
    }
    assert values == {
        "B01": (4, 5),
        "B02": (4, 18),
        "B03": (10, 11),
        "B04": (10, 18),
        "B05": (17, 18),
    }


def test_e16_exact_seeds(frozen_config):
    assert frozen_config["seed_list"] == [1802163452, 1678077158]
    with pytest.raises(ConfigError):
        validate_run_identity(frozen_config, seed=1, treatment_seat=0)


def test_e16_seat_swap_completeness(frozen_config):
    matrix = build_run_matrix(frozen_config, "stage_a")
    assert all(
        {row["treatment_seat"] for row in matrix if row["cell_id"] == cell} == {0, 1}
        for cell in frozen_config["stage_a_cells"]
    )


def test_e16_quadrants_owned_is_exactly_two(frozen_config):
    assert frozen_config["quadrants_owned"] == 2
    assert all(
        row["cell_config"]["quadrants_owned"] == 2
        for row in build_run_matrix(frozen_config, "stage_a")
    )


def test_e16_stage_b_blocked_without_gate(frozen_config):
    with pytest.raises(ConfigError):
        resolve_cell(frozen_config, "stage_b", "B01")


def test_e16_manipulated_allowlist_exact(frozen_config):
    assert set(frozen_config["manipulated_field_allowlist"]) == MANIPULATED_FIELDS
    tampered = deepcopy(frozen_config)
    tampered.pop("configuration_sha256")
    tampered["stage_a_cells"]["A01"]["routing_module"] = "post_hoc_change"
    with pytest.raises(ConfigError):
        validate_frozen_config(tampered, verify_files=False)


def test_e16_controls_identical_outside_allowlist(frozen_config):
    resolved = [
        resolve_cell(frozen_config, "stage_a", cell)
        for cell in frozen_config["stage_a_cells"]
    ]
    controls = set(frozen_config["controls"]) - MANIPULATED_FIELDS
    for field in controls:
        assert len({repr(cell[field]) for cell in resolved}) == 1


def test_e16_hash_fail_closed(frozen_config):
    tampered = deepcopy(frozen_config)
    tampered.pop("configuration_sha256")
    tampered["opponent_sha256"] = "0" * 64
    with pytest.raises(ConfigError):
        validate_frozen_config(tampered, verify_files=False)


def test_e16_matrix_episode_totals_and_no_replacements(frozen_config):
    stage_a = build_run_matrix(frozen_config, "stage_a")
    stage_b = build_run_matrix(frozen_config, "stage_b", c_star=17)
    assert len(stage_a) == 28
    assert len(stage_a) + len(stage_b) == 48
    assert len({row["episode_id"] for row in stage_a}) == 28
    assert all(row["episode_id"].startswith("E16-A-R1-") for row in stage_a)
    assert all(row["status"] == "PLANNED" for row in stage_a)


def test_e16_r1_semantic_and_hash_provenance(frozen_config):
    assert frozen_config["schema_version"] == "e16.config.r1.v1"
    assert (
        frozen_config["watering_semantic_version"]
        == "e16.watering_dispatch_precedence.v1"
    )
    assert frozen_config["replication_id"] == "E16-A-R1"
    assert frozen_config["predecessor_config_sha256"] == EXPECTED_LEGACY_CONFIG_SHA256
    assert (
        frozen_config["predecessor_treatment_build_sha256"]
        == EXPECTED_LEGACY_TREATMENT_SHA256
    )
    assert frozen_config["treatment_build_sha256"] != EXPECTED_LEGACY_TREATMENT_SHA256
    assert (
        sha256_file(REPO_ROOT / frozen_config["treatment_build_path"])
        == (frozen_config["treatment_build_sha256"])
    )


def test_e16_legacy_artifacts_remain_loadable_and_unchanged():
    legacy = load_frozen_config(LEGACY_CONFIG_PATH)
    assert legacy["configuration_sha256"] == EXPECTED_LEGACY_CONFIG_SHA256
    assert legacy["treatment_build_sha256"] == EXPECTED_LEGACY_TREATMENT_SHA256
    assert sha256_file(REPO_ROOT / legacy["treatment_build_path"]) == (
        EXPECTED_LEGACY_TREATMENT_SHA256
    )
