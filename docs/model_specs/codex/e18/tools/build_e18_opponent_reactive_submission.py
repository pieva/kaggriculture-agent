#!/usr/bin/env python3
"""Build the standalone E18 opponent-reactive submission mechanically."""

from __future__ import annotations

import hashlib
import json
import pprint
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "submission/submission_codex_e17_topology_662.py"
SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/codex_e18_opponent_reactive_topology.py"
)
CONFIG = (
    ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_1_OPPONENT_REACTIVE_662_770_V1.json"
)
TARGET = ROOT / "submission/submission_codex_e18_opponent_reactive_662_770.py"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    base = BASE.read_text(encoding="utf-8")
    source = SOURCE.read_text(encoding="utf-8").replace(
        "from agricola.strategy.codex.codex_e17_topology_cap_662 import (",
        "from _codex_bundle.agricola.strategy.codex."
        "codex_e17_topology_cap_662 import (",
    )
    if "from agricola." in source:
        raise RuntimeError("E18 source still contains a repository import")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    source_sha = _sha256(SOURCE)
    config_sha = _sha256(CONFIG)
    suffix = f'''

# E18.1 public-opponent-reactive topology overlay.  This replaces the E17.3
# entry point while retaining its hash-verified embedded provider.
_E18_BASE_RELEASE_ID = RELEASE_ID
_E18_BASE_BUILD_METADATA = BUILD_METADATA
RELEASE_ID = "CODEX-E18.1-OPPONENT-REACTIVE-662-770-KAGGLE-V1"
MODEL_SPEC_VERSION = "CODEX-E18.1-OPPONENT-REACTIVE-662-770-V1"
BUILD_METADATA = {{
    "release_id": RELEASE_ID,
    "model_spec_version": MODEL_SPEC_VERSION,
    "base_release_id": _E18_BASE_RELEASE_ID,
    "source_sha256": "{source_sha}",
    "config_sha256": "{config_sha}",
    "decision_day": 6,
    "topology_modes": ["6-6-2", "7-7-0"],
    "public_opponent_features_only": True,
    "cross_episode_memory": False,
    "pasture_fill_target": 14,
    "livestock_resource_cap": 14,
    "high_pressure_placement_release_day": 28,
}}
_E18_SOURCE = {source!r}
_E18_CONFIG = {pprint.pformat(config, width=100, sort_dicts=False)}

_e18 = _exec_module(
    "_codex_bundle.agricola.strategy.codex."
    "codex_e18_opponent_reactive_topology",
    _E18_SOURCE,
)
_e18.load_e18_opponent_reactive_config = _config_loader(_E18_CONFIG)


def create_agent(run_context=None):
    return _e18.create_codex_e18_opponent_reactive_topology(
        run_context=run_context,
        config_path=_e18.DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH,
    )


_DEFAULT_AGENT = create_agent()


def agent(observation, configuration=None):
    return _DEFAULT_AGENT(observation, configuration)
'''
    TARGET.write_text(base.rstrip() + suffix + "\n", encoding="utf-8")
    print(
        f"wrote {TARGET} source_sha256={source_sha} "
        f"config_sha256={config_sha} submission_sha256={_sha256(TARGET)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
