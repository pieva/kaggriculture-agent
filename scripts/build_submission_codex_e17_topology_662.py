#!/usr/bin/env python3
"""Build the standalone productive Codex E17.3 6-6-2 candidate."""

from __future__ import annotations

import hashlib
import json
import pprint
from pathlib import Path

from agricola.core.repository_paths import expected_current_sha256
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    DEFAULT_TOPOLOGY_662_CONFIG_PATH,
    TOPOLOGY_662_MODEL_SPEC_VERSION,
)

try:
    from scripts.build_submission_codex_e17_v4d import RELEASE_ID as V4D_RELEASE_ID
    from scripts.build_submission_codex_e17_v4d import _build_body as _build_v4d_body
    from scripts.build_submission_codex_e17_v4d import (
        _verify_inputs as _verify_v4d_inputs,
    )
except ModuleNotFoundError:  # Direct ``python scripts/<builder>.py`` execution.
    from build_submission_codex_e17_v4d import (  # type: ignore[no-redef]
        RELEASE_ID as V4D_RELEASE_ID,
    )
    from build_submission_codex_e17_v4d import (  # type: ignore[no-redef]
        _build_body as _build_v4d_body,
    )
    from build_submission_codex_e17_v4d import (  # type: ignore[no-redef]
        _verify_inputs as _verify_v4d_inputs,
    )

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "submission/submission_codex_e17_topology_662.py"
RELEASE_ID = "CODEX-E17.3-TOPOLOGY-FILL-662-KAGGLE-CANDIDATE-V2"
SOURCE_PATH = (
    ROOT / "src/agricola/strategy/codex/codex_e17_topology_cap_662.py"
)
CONFIG_PATH = DEFAULT_TOPOLOGY_662_CONFIG_PATH
SOURCE_SHA256_AT_FREEZE = (
    "3B7A49FB29187D2E03F58F74E48A0D9A114C2C0E7112EB19908C303826D6315C"
)
EXPECTED_SOURCE_SHA256 = expected_current_sha256(
    SOURCE_PATH.relative_to(ROOT).as_posix(), SOURCE_SHA256_AT_FREEZE
)
EXPECTED_CONFIG_SHA256 = (
    "0288AB878C7C9224A56B71E84158BDDDFDBE0CECC6D8EAE0F30093F985CEF50C"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _verify_inputs() -> None:
    _verify_v4d_inputs()
    actual_source = _sha256(SOURCE_PATH)
    actual_config = _sha256(CONFIG_PATH)
    if actual_source != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(
            "topology source freeze mismatch: "
            f"expected={EXPECTED_SOURCE_SHA256} actual={actual_source}"
        )
    if actual_config != EXPECTED_CONFIG_SHA256:
        raise RuntimeError(
            "topology config freeze mismatch: "
            f"expected={EXPECTED_CONFIG_SHA256} actual={actual_config}"
        )


def _build_body() -> str:
    base = _build_v4d_body()
    source = SOURCE_PATH.read_text(encoding="utf-8").replace(
        "from agricola.", "from _codex_bundle.agricola."
    )
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    metadata = {
        "release_id": RELEASE_ID,
        "model_spec_version": TOPOLOGY_662_MODEL_SPEC_VERSION,
        "base_release_id": V4D_RELEASE_ID,
        "topology_source_sha256": EXPECTED_SOURCE_SHA256,
        "topology_source_sha256_at_freeze": SOURCE_SHA256_AT_FREEZE,
        "topology_config_sha256": EXPECTED_CONFIG_SHA256,
        "pasture_targets_by_quadrant": {"Q0": 6, "Q1": 6, "Q2": 2},
        "q2_pasture_cap": 2,
        "pasture_fill_target": 14,
        "livestock_resource_cap": 15,
        "livestock_in_transit_buffer": 1,
        "reclaimed_crop_targets": 5,
        "q2_reclaimed_crop_targets": 3,
        "pasture_fill_control": True,
    }
    overlay = f'''

# E17.3 productive 6-6-2 topology overlay.  This intentionally replaces the
# default V4D entry point while retaining the hash-verified embedded provider.
_BASE_RELEASE_ID = RELEASE_ID
_BASE_BUILD_METADATA = BUILD_METADATA
RELEASE_ID = {RELEASE_ID!r}
MODEL_SPEC_VERSION = {TOPOLOGY_662_MODEL_SPEC_VERSION!r}
BUILD_METADATA = {pprint.pformat(metadata, width=100, sort_dicts=False)}
_TOPOLOGY_662_SOURCE = {source!r}
_TOPOLOGY_662_CONFIG = {pprint.pformat(config, width=100, sort_dicts=False)}

_topology_662 = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_topology_cap_662",
    _TOPOLOGY_662_SOURCE,
)
_topology_662.load_topology_662_config = _config_loader(_TOPOLOGY_662_CONFIG)


def create_agent(run_context=None):
    return _topology_662.create_codex_e17_topology_cap_662(
        run_context=run_context,
        config_path=_topology_662.DEFAULT_TOPOLOGY_662_CONFIG_PATH,
    )


_DEFAULT_AGENT = create_agent()


def agent(observation, configuration=None):
    return _DEFAULT_AGENT(observation, configuration)
'''
    return base + overlay


def build_submission_codex_e17_topology_662(
    output_path: Path | str | None = None,
) -> Path:
    """Build the productive 6-6-2 candidate to a Kaggle submission file."""

    _verify_inputs()
    target = Path(output_path) if output_path is not None else TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_build_body(), encoding="utf-8", newline="\n")
    return target


def main() -> int:
    target = build_submission_codex_e17_topology_662()
    print(f"wrote {target}")
    print(f"sha256={_sha256(target)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
