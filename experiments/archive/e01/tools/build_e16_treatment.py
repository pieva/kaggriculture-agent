"""Build the versioned E16-A-R1 treatment and config artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "agricola" / "e16" / "policy.py"
OUTPUT = ROOT / "results" / "e16" / "manifests" / "E16_TREATMENT_BUILD_R1.py"
LEGACY_TREATMENT = ROOT / "results" / "e16" / "manifests" / "E16_TREATMENT_BUILD.py"
LEGACY_CONFIG = ROOT / "configs" / "e16" / "E16_FROZEN_CONFIG.json"
OUTPUT_CONFIG = ROOT / "configs" / "e16" / "E16_R1_FROZEN_CONFIG.json"
SEMANTIC_CLARIFICATION = (
    ROOT
    / "docs"
    / "experiment_designs"
    / "e16"
    / "E16_WATERING_SEMANTICS_CLARIFICATION.md"
)
OLD_TREATMENT_SHA256 = (
    "8a897209ca331f9be21e430107b2452bb5b26df9e8d5b88c015b052a5185355e"
)
OLD_CONFIG_SHA256 = "4c6ca43025d5a95acd6b2c8c5eb51a17a4bc4cadd672146055c317d54864ec92"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    payload = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    if "from agricola" in payload or "import agricola" in payload:
        raise RuntimeError("treatment source is not self-contained")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(payload, encoding="utf-8", newline="\n")
    treatment_digest = sha256(OUTPUT)
    if sha256(LEGACY_TREATMENT) != OLD_TREATMENT_SHA256:
        raise RuntimeError("legacy treatment artifact changed")
    if sha256(LEGACY_CONFIG) != OLD_CONFIG_SHA256:
        raise RuntimeError("legacy config artifact changed")

    config = json.loads(LEGACY_CONFIG.read_text(encoding="utf-8"))
    config.update(
        {
            "schema_version": "e16.config.r1.v1",
            "telemetry_schema_version": "e16.telemetry.v2",
            "watering_semantic_version": "e16.watering_dispatch_precedence.v1",
            "semantic_clarification_path": str(
                SEMANTIC_CLARIFICATION.relative_to(ROOT)
            ).replace("\\", "/"),
            "semantic_clarification_sha256": sha256(SEMANTIC_CLARIFICATION),
            "treatment_build_path": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
            "treatment_build_sha256": treatment_digest,
            "predecessor_config_path": str(LEGACY_CONFIG.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "predecessor_config_sha256": OLD_CONFIG_SHA256,
            "predecessor_treatment_build_path": str(
                LEGACY_TREATMENT.relative_to(ROOT)
            ).replace("\\", "/"),
            "predecessor_treatment_build_sha256": OLD_TREATMENT_SHA256,
            "repair_reasons": [
                "semantic clarification",
                "implementation repair",
                "telemetry repair",
            ],
            "replication_id": "E16-A-R1",
            "corrected_stage_a_results_path": "results/e16/stage_a_r1",
        }
    )
    OUTPUT_CONFIG.write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    config_digest = sha256(OUTPUT_CONFIG)
    print(f"{OUTPUT.relative_to(ROOT)} sha256={treatment_digest}")
    print(f"{OUTPUT_CONFIG.relative_to(ROOT)} sha256={config_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
