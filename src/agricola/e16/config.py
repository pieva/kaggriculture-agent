"""Fail-closed loading and validation for the frozen E16 protocol."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
LEGACY_CONFIG_PATH = REPO_ROOT / "configs" / "e16" / "E16_FROZEN_CONFIG.json"
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "e16" / "E16_R1_FROZEN_CONFIG.json"
MANIPULATED_FIELDS = frozenset(
    {
        "watering_dispatch_priority",
        "crop_working_set_target",
        "livestock_headcount_target",
        "pasture_allocation_target",
    }
)
EXPECTED_SEEDS = (1802163452, 1678077158)
EXPECTED_SEATS = (0, 1)
EXPECTED_STAGE_A = {
    "A01": (0.20, 10),
    "A02": (0.70, 10),
    "A03": (0.20, 25),
    "A04": (0.70, 25),
    "A05": (0.45, 17),
    "A06": (0.45, 25),
    "A07": (0.70, 17),
}
EXPECTED_STAGE_B = {
    "B01": (4, 5),
    "B02": (4, 18),
    "B03": (10, 11),
    "B04": (10, 18),
    "B05": (17, 18),
}
EXPECTED_OPPONENT_SHA256 = (
    "604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb"
)
EXPECTED_LEGACY_CONFIG_SHA256 = (
    "4c6ca43025d5a95acd6b2c8c5eb51a17a4bc4cadd672146055c317d54864ec92"
)
EXPECTED_LEGACY_TREATMENT_SHA256 = (
    "8a897209ca331f9be21e430107b2452bb5b26df9e8d5b88c015b052a5185355e"
)


class ConfigError(RuntimeError):
    """The requested run is not identical to the frozen protocol."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def _resolve_repo_path(value: str) -> Path:
    path = (REPO_ROOT / value).resolve()
    try:
        path.relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise ConfigError(f"path escapes repository: {value}") from exc
    return path


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ConfigError(message)


def _validate_cell_controls(config: dict[str, Any], cells: dict[str, Any]) -> None:
    controls = config["controls"]
    for cell_id, cell in cells.items():
        unknown = set(cell) - MANIPULATED_FIELDS
        _require(
            not unknown, f"{cell_id} contains non-allowlisted fields: {sorted(unknown)}"
        )
        merged = {**controls, **cell}
        for field, expected in controls.items():
            if field not in MANIPULATED_FIELDS:
                _require(
                    merged[field] == expected,
                    f"{cell_id} changes frozen control {field}",
                )


def validate_frozen_config(
    config: dict[str, Any], *, verify_files: bool = True
) -> None:
    """Validate every protocol identity that can be checked before a run."""

    _require(config.get("design_id") == "E16_TRAINING", "unexpected design_id")
    _require(
        config.get("evidence_role") == "TRAINING", "E16 evidence_role must be TRAINING"
    )
    _require(config.get("quadrants_owned") == 2, "quadrants_owned must equal 2")
    _require(
        tuple(config.get("seed_list", ())) == EXPECTED_SEEDS,
        "seed list differs from frozen protocol",
    )
    _require(
        tuple(config.get("seat_protocol", {}).get("treatment_seats", ()))
        == EXPECTED_SEATS,
        "seat swap is incomplete",
    )
    _require(
        config.get("seat_protocol", {}).get("mandatory") is True,
        "seat swap must be mandatory",
    )
    _require(
        config.get("opponent_sha256") == EXPECTED_OPPONENT_SHA256,
        "unexpected opponent hash in config",
    )
    schema_version = config.get("schema_version")
    if schema_version == "e16.config.v1":
        _require(
            config.get("telemetry_schema_version") == "e16.telemetry.v1",
            "unexpected legacy telemetry schema",
        )
    elif schema_version == "e16.config.r1.v1":
        _require(
            config.get("telemetry_schema_version") == "e16.telemetry.v2",
            "unexpected repaired telemetry schema",
        )
        _require(
            config.get("watering_semantic_version")
            == "e16.watering_dispatch_precedence.v1",
            "unexpected watering semantic version",
        )
        _require(config.get("replication_id") == "E16-A-R1", "unexpected repair id")
        _require(
            config.get("predecessor_config_sha256") == EXPECTED_LEGACY_CONFIG_SHA256,
            "legacy config provenance mismatch",
        )
        _require(
            config.get("predecessor_treatment_build_sha256")
            == EXPECTED_LEGACY_TREATMENT_SHA256,
            "legacy treatment provenance mismatch",
        )
        _require(
            config.get("repair_reasons")
            == [
                "semantic clarification",
                "implementation repair",
                "telemetry repair",
            ],
            "repair reasons differ",
        )
    else:
        raise ConfigError(f"unexpected config schema: {schema_version}")
    _require(
        config.get("manipulated_field_allowlist") == sorted(MANIPULATED_FIELDS),
        "manipulated allowlist differs",
    )

    stage_a = config.get("stage_a_cells", {})
    _require(
        set(stage_a) == set(EXPECTED_STAGE_A), "Stage A must contain exactly A01-A07"
    )
    for cell_id, (watering, crops) in EXPECTED_STAGE_A.items():
        cell = stage_a[cell_id]
        _require(
            cell.get("watering_dispatch_priority") == watering,
            f"{cell_id} watering value differs",
        )
        _require(
            cell.get("crop_working_set_target") == crops,
            f"{cell_id} crop target differs",
        )
        _require(
            cell.get("livestock_headcount_target") == 4,
            f"{cell_id} herd control differs",
        )
        _require(
            cell.get("pasture_allocation_target") == 5,
            f"{cell_id} pasture control differs",
        )

    stage_b = config.get("stage_b_cells", {})
    _require(
        set(stage_b) == set(EXPECTED_STAGE_B), "Stage B must contain exactly B01-B05"
    )
    for cell_id, (herd, pasture) in EXPECTED_STAGE_B.items():
        cell = stage_b[cell_id]
        _require(
            cell.get("livestock_headcount_target") == herd,
            f"{cell_id} herd value differs",
        )
        _require(
            cell.get("pasture_allocation_target") == pasture,
            f"{cell_id} pasture value differs",
        )
        _require(
            set(cell) == {"livestock_headcount_target", "pasture_allocation_target"},
            f"{cell_id} changes a Stage B control",
        )

    _validate_cell_controls(config, stage_a)
    _validate_cell_controls(config, stage_b)

    gate = config.get("stage_b_gate", {})
    _require(
        gate.get("eligible_cell_ids") == ["A02", "A07", "A04"],
        "capacity ladder differs",
    )
    _require(
        "final_money" not in json.dumps(gate).lower(),
        "final_money is forbidden in Stage B gate",
    )
    _require(
        gate.get("selection") == "largest_eligible_crop_target",
        "gate selection differs",
    )

    if verify_files:
        opponent = _resolve_repo_path(config["opponent_path"])
        treatment = _resolve_repo_path(config["treatment_build_path"])
        design = _resolve_repo_path(config["frozen_design_path"])
        _require(opponent.is_file(), f"missing opponent: {opponent}")
        _require(treatment.is_file(), f"missing treatment build: {treatment}")
        _require(design.is_file(), f"missing frozen design: {design}")
        _require(
            sha256_file(opponent) == config["opponent_sha256"],
            "opponent SHA256 mismatch",
        )
        _require(
            sha256_file(treatment) == config["treatment_build_sha256"],
            "treatment build SHA256 mismatch",
        )
        _require(
            sha256_file(design) == config["frozen_design_sha256"],
            "frozen design SHA256 mismatch",
        )
        if schema_version == "e16.config.r1.v1":
            clarification = _resolve_repo_path(config["semantic_clarification_path"])
            predecessor_config = _resolve_repo_path(config["predecessor_config_path"])
            predecessor_treatment = _resolve_repo_path(
                config["predecessor_treatment_build_path"]
            )
            _require(clarification.is_file(), "missing semantic clarification")
            _require(
                sha256_file(clarification) == config["semantic_clarification_sha256"],
                "semantic clarification SHA256 mismatch",
            )
            _require(
                sha256_file(predecessor_config) == EXPECTED_LEGACY_CONFIG_SHA256,
                "legacy config artifact changed",
            )
            _require(
                sha256_file(predecessor_treatment) == EXPECTED_LEGACY_TREATMENT_SHA256,
                "legacy treatment artifact changed",
            )


def load_frozen_config(
    path: Path | str = DEFAULT_CONFIG_PATH, *, verify_files: bool = True
) -> dict[str, Any]:
    """Load a private immutable-by-convention copy of the validated config."""

    config_path = Path(path).resolve()
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    validate_frozen_config(config, verify_files=verify_files)
    config["configuration_sha256"] = sha256_file(config_path)
    config["configuration_path"] = str(config_path.relative_to(REPO_ROOT)).replace(
        "\\", "/"
    )
    return deepcopy(config)


def resolve_cell(
    config: dict[str, Any], stage: str, cell_id: str, c_star: int | None = None
) -> dict[str, Any]:
    """Resolve one cell while allowing only the frozen manipulated fields."""

    stage_key = stage.lower()
    if stage_key == "stage_a":
        cells = config["stage_a_cells"]
    elif stage_key == "stage_b":
        if c_star not in {10, 17, 25}:
            raise ConfigError("Stage B requires a positive frozen capacity gate")
        cells = config["stage_b_cells"]
    else:
        raise ConfigError(f"unknown stage: {stage}")
    if cell_id not in cells:
        raise ConfigError(f"unknown {stage} cell: {cell_id}")

    resolved = deepcopy(config["controls"])
    resolved.update(deepcopy(cells[cell_id]))
    if stage_key == "stage_b":
        resolved["watering_dispatch_priority"] = 0.70
        resolved["crop_working_set_target"] = c_star
    resolved["quadrants_owned"] = 2
    resolved["cell_id"] = cell_id
    resolved["stage"] = stage_key
    return resolved


def validate_run_identity(
    config: dict[str, Any], *, seed: int, treatment_seat: int
) -> None:
    if seed not in config["seed_list"]:
        raise ConfigError(f"seed {seed} is not frozen")
    if treatment_seat not in config["seat_protocol"]["treatment_seats"]:
        raise ConfigError(f"seat {treatment_seat} is not frozen")


def build_run_matrix(
    config: dict[str, Any], stage: str, *, c_star: int | None = None
) -> list[dict[str, Any]]:
    stage_key = stage.lower()
    cells = (
        config["stage_a_cells"] if stage_key == "stage_a" else config["stage_b_cells"]
    )
    rows: list[dict[str, Any]] = []
    for cell_id in cells:
        cell = resolve_cell(config, stage_key, cell_id, c_star)
        for seed in config["seed_list"]:
            for seat in config["seat_protocol"]["treatment_seats"]:
                prefix = (
                    config.get("replication_id", "E16")
                    if stage_key == "stage_a"
                    else "E16"
                )
                rows.append(
                    {
                        "episode_id": f"{prefix}-{cell_id}-S{seed}-P{seat}",
                        "stage": stage_key,
                        "cell_id": cell_id,
                        "seed": seed,
                        "treatment_seat": seat,
                        "cell_config": cell,
                        "status": "PLANNED",
                    }
                )
    return rows
