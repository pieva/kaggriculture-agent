#!/usr/bin/env python3
"""Build the standalone E18.16 exact-7-7-0 Kaggle submission."""

from __future__ import annotations

import hashlib
import json
import pprint
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "submission/submission_codex_e18_2_capacity_governed_v4d.py"
TARGET = ROOT / "submission/submission_codex_e18_16_770.py"

MODULES = (
    (
        "e18_6",
        "codex_e18_concentrated_770_throughput",
        "load_e18_concentrated_770_config",
        ROOT
        / "src/agricola/strategy/codex/"
        / "codex_e18_concentrated_770_throughput.py",
        ROOT
        / "docs/model_specs/codex/e18/configs/"
        / "CODEX_E18_6_CONCENTRATED_770_THROUGHPUT_V1.json",
    ),
    (
        "e18_9",
        "codex_e18_770_live_crop_rotation_guard",
        "load_e18_770_live_crop_rotation_guard_config",
        ROOT
        / "src/agricola/strategy/codex/"
        / "codex_e18_770_live_crop_rotation_guard.py",
        ROOT
        / "docs/model_specs/codex/e18/configs/"
        / "CODEX_E18_9_770_LIVE_CROP_ROTATION_GUARD_V1.json",
    ),
    (
        "e18_10_v2",
        "codex_e18_770_water_before_dig_guard_v2",
        "load_e18_770_water_before_dig_guard_v2_config",
        ROOT
        / "src/agricola/strategy/codex/"
        / "codex_e18_770_water_before_dig_guard_v2.py",
        ROOT
        / "docs/model_specs/codex/e18/configs/"
        / "CODEX_E18_10_770_WATER_BEFORE_DIG_GUARD_V2.json",
    ),
    (
        "e18_13",
        "codex_e18_770_d20_critical_feed_deadline",
        "load_e18_770_d20_critical_feed_deadline_config",
        ROOT
        / "src/agricola/strategy/codex/"
        / "codex_e18_770_d20_critical_feed_deadline.py",
        ROOT
        / "docs/model_specs/codex/e18/configs/"
        / "CODEX_E18_13_770_D20_CRITICAL_FEED_DEADLINE_V1.json",
    ),
    (
        "e18_16",
        "codex_e18_770_exact_cap_critical_feed",
        "load_e18_770_exact_cap_critical_feed_config",
        ROOT
        / "src/agricola/strategy/codex/"
        / "codex_e18_770_exact_cap_critical_feed.py",
        ROOT
        / "docs/model_specs/codex/e18/configs/"
        / "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1.json",
    ),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    base = BASE.read_text(encoding="utf-8")
    sources = {}
    configs = {}
    source_hashes = {}
    config_hashes = {}
    for key, _module, _loader, source_path, config_path in MODULES:
        source = source_path.read_text(encoding="utf-8").replace(
            "from agricola.", "from _codex_bundle.agricola."
        )
        if "from agricola." in source:
            raise RuntimeError(f"{key} still contains a repository import")
        sources[key] = source
        configs[key] = json.loads(config_path.read_text(encoding="utf-8"))
        source_hashes[key] = _sha256(source_path)
        config_hashes[key] = _sha256(config_path)

    module_bootstrap = []
    for key, module, loader, _source_path, _config_path in MODULES:
        module_bootstrap.append(
            f'''_{key} = _exec_module(
    "_codex_bundle.agricola.strategy.codex.{module}",
    _E18_16_SOURCES["{key}"],
)
_{key}.{loader} = _config_loader(_E18_16_CONFIGS["{key}"])'''
        )

    suffix = f'''

# E18.16 exact 7-7-0 livestock-safety release.  The embedded E18.2 provider
# remains hash-addressed; the modules below reproduce the complete E18.16
# inheritance chain without repository imports.
_E18_16_BASE_RELEASE_ID = RELEASE_ID
_E18_16_BASE_BUILD_METADATA = BUILD_METADATA
RELEASE_ID = "CODEX-E18.16-770-EXACT-CAP-CRITICAL-FEED-KAGGLE-V1"
MODEL_SPEC_VERSION = "CODEX-E18.16-770-EXACT-CAP-CRITICAL-FEED-V1"
BUILD_METADATA = {{
    "release_id": RELEASE_ID,
    "model_spec_version": MODEL_SPEC_VERSION,
    "base_release_id": _E18_16_BASE_RELEASE_ID,
    "source_sha256": {pprint.pformat(source_hashes, width=100, sort_dicts=False)},
    "config_sha256": {pprint.pformat(config_hashes, width=100, sort_dicts=False)},
    "pasture_topology": "7-7-0",
    "pasture_fill_target": 14,
    "livestock_resource_cap": 14,
    "in_transit_buffer": 0,
    "critical_feed_guard": "D20_IN_PLACE_FEED_BEFORE_MOVE",
    "development_gate_a": "PASS_14_MATCHES",
    "development_gate_b_top3": "FAIL",
    "holdout_consumed": False,
    "final_confirmation_consumed": False,
}}
_E18_16_SOURCES = {pprint.pformat(sources, width=120, sort_dicts=False)}
_E18_16_CONFIGS = {pprint.pformat(configs, width=120, sort_dicts=False)}

{chr(10).join(module_bootstrap)}


def create_agent(run_context=None):
    return _e18_16.create_codex_e18_770_exact_cap_critical_feed(
        run_context=run_context,
        config_path=_e18_16.DEFAULT_E18_770_EXACT_CAP_CRITICAL_FEED_CONFIG_PATH,
    )


_DEFAULT_AGENT = create_agent()


def agent(observation, configuration=None):
    return _DEFAULT_AGENT(observation, configuration)
'''
    TARGET.write_text(base.rstrip() + suffix + "\n", encoding="utf-8")
    print(
        f"wrote {TARGET} bytes={TARGET.stat().st_size} "
        f"submission_sha256={_sha256(TARGET)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
