#!/usr/bin/env python3
"""Build the standalone E18.2 capacity-governed V4D submission."""

from __future__ import annotations

import hashlib
import json
import pprint
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "submission/submission_codex_e18_opponent_reactive_662_770.py"
SOURCE = (
    ROOT
    / "src/agricola/strategy/codex/codex_e18_capacity_governed_v4d.py"
)
CONFIG = (
    ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1.json"
)
TARGET = ROOT / "submission/submission_codex_e18_2_capacity_governed_v4d.py"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    base = BASE.read_text(encoding="utf-8")
    source = SOURCE.read_text(encoding="utf-8").replace(
        "from agricola.", "from _codex_bundle.agricola."
    )
    if "from agricola." in source:
        raise RuntimeError("E18.2 source still contains a repository import")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    source_sha = _sha256(SOURCE)
    config_sha = _sha256(CONFIG)
    suffix = f'''

# E18.2 capacity governor.  The embedded V4D provider and E18 helper modules
# remain hash-addressed; this final entry point replaces the rejected E18.1
# topology controller with a topology-preserving, on-tile recovery overlay.
_E18_2_BASE_RELEASE_ID = RELEASE_ID
_E18_2_BASE_BUILD_METADATA = BUILD_METADATA
RELEASE_ID = "CODEX-E18.2-CAPACITY-GOVERNED-V4D-KAGGLE-V1"
MODEL_SPEC_VERSION = "CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1"
BUILD_METADATA = {{
    "release_id": RELEASE_ID,
    "model_spec_version": MODEL_SPEC_VERSION,
    "base_release_id": _E18_2_BASE_RELEASE_ID,
    "source_sha256": "{source_sha}",
    "config_sha256": "{config_sha}",
    "base_policy": "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28",
    "topology": "7-7-5 preserved",
    "topology_reclaim_enabled": False,
    "recovery_scope": "otherwise-PASS worker already on service tile",
    "terminal_passthrough_day": 28,
    "public_opponent_features_only": True,
    "cross_episode_memory": False,
    "holdout_consumed": False,
    "final_confirmation_consumed": False,
}}
_E18_2_SOURCE = {source!r}
_E18_2_CONFIG = {pprint.pformat(config, width=100, sort_dicts=False)}

_e18_2 = _exec_module(
    "_codex_bundle.agricola.strategy.codex."
    "codex_e18_capacity_governed_v4d",
    _E18_2_SOURCE,
)
_e18_2.load_e18_capacity_governed_config = _config_loader(_E18_2_CONFIG)


def create_agent(run_context=None):
    return _e18_2.create_codex_e18_capacity_governed_v4d(
        run_context=run_context,
        config_path=_e18_2.DEFAULT_E18_CAPACITY_GOVERNED_CONFIG_PATH,
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
