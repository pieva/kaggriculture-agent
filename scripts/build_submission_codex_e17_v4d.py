#!/usr/bin/env python3
"""Build the standalone Codex E17.2 V4D D28 Kaggle candidate."""

from __future__ import annotations

import hashlib
import json
import pprint
from pathlib import Path
from typing import Any

from agricola.core.state import CROPS
from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4D_CONFIG_PATH,
    V4D_MODEL_SPEC_VERSION,
    load_v4_config,
)
from agricola.strategy.codex.codex_v9_routine_data import (
    ROUTINE_ACTIONS,
    ROUTINE_SHA256,
)

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "submission" / "submission_codex_e17_v4d.py"
RELEASE_ID = "CODEX-E17.2-V4D-D28-KAGGLE-CANDIDATE-V1"

SOURCE_PATHS = {
    "observation_contract": ROOT / "src/agricola/core/observation_contract.py",
    "v9": ROOT / "src/agricola/strategy/codex/codex_3q_mixed_high_density.py",
    "guarded": ROOT / "src/agricola/strategy/codex/codex_e17_reactive_guarded.py",
    "true_reactive": ROOT
    / "src/agricola/strategy/codex/codex_e17_true_reactive.py",
    "routing_core": ROOT
    / "src/agricola/strategy/codex/codex_e17_reactive_service_routing_core.py",
    "routing_v3": ROOT
    / "src/agricola/strategy/codex/codex_e17_reactive_service_routing_v3.py",
    "routing_v4": ROOT
    / "src/agricola/strategy/codex/codex_e17_batched_cluster_routing_v4.py",
    "routine_data": ROOT
    / "src/agricola/strategy/codex/codex_v9_routine_data.py",
}
CONFIG_PATHS = {
    "v9": ROOT
    / "docs/model_specs/codex/configs/"
    / "CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY_CONFIG.json",
    "guarded": ROOT
    / "experiments/e17/configs/codex/"
    / "CODEX_E17_1_3Q_REACTIVE_GUARDED_V1.json",
    "true_reactive": ROOT
    / "experiments/e17/configs/codex/"
    / "CODEX_E17_1_TRUE_REACTIVE_V2.json",
    "routing_core": ROOT
    / "experiments/e17/configs/codex/"
    / "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V2.json",
    "routing_v3": ROOT
    / "experiments/e17/configs/codex/"
    / "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V3_D28.json",
    "routing_v4": DEFAULT_V4D_CONFIG_PATH,
}
EXPECTED_SOURCE_HASHES = {
    "observation_contract": "3E7509888B09103C79B86FD058984651337CBFC32AB60CD934E6351A4F2A81A9",
    "v9": "4D99C919B59DAE9B307C403FCF3198763B08FB9D15324AB8C937C4FC2B32090E",
    "guarded": "4B9F1FE9BD839F284D25030B39292CEF77F9195C6CA29711CF908EE5D2968607",
    "true_reactive": "9CD72CA9512B62DB6354CC998EDBCF55AF697989ED92C6806D51EBE329F4B07E",
    "routing_core": "DDF736DF8E40ADC5CE3F6983CCD516F97AE72E5A385A58A2200A816AD314AEDB",
    "routing_v3": "80D909104402473503E1945A6F9EE200DF1CEA5ABA9C66B43C5F6A8AA61A6E91",
    "routing_v4": "9350F8B327B972C703136EB6411F03C74B2A80F6A75A9D99C3E4CA614A60B2A4",
    "routine_data": "AC5819014EBB85ED86BA5D25D4F01DE46F9E4760465B7188DF11E69C8812F774",
}
EXPECTED_CONFIG_HASHES = {
    "v9": "44DD0EC2F33C9EEEE74AE5676580DC833325AB969D8A9D262EC870FEAAAC6C99",
    "guarded": "5B4D4B24C4791E42A08937F9CCD7F7BCE5B4B05BA960E7FE8F066DA4C6BED5A0",
    "true_reactive": "2CC7F1900AFEBC09F971E76FCC0CCC801FF1F54CE65CECB2E979B95456EB42ED",
    "routing_core": "43FFD984C17F61F21932AB08433DB652DB07E09BFC9AA781FC961D0AC8D48749",
    "routing_v3": "AD2A79602A610D35C2D44F200AEA36B9949F41D1EA67EC43EAB873B007A2EF8D",
    "routing_v4": "CA7A6E13CF991185E823325D8220E0682388AC18EB446BB206C0A30ACAB45595",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _verify_inputs() -> None:
    actual_sources = {key: _sha256(path) for key, path in SOURCE_PATHS.items()}
    actual_configs = {key: _sha256(path) for key, path in CONFIG_PATHS.items()}
    if actual_sources != EXPECTED_SOURCE_HASHES:
        raise RuntimeError(
            f"source freeze mismatch: expected={EXPECTED_SOURCE_HASHES}, "
            f"actual={actual_sources}"
        )
    if actual_configs != EXPECTED_CONFIG_HASHES:
        raise RuntimeError(
            f"config freeze mismatch: expected={EXPECTED_CONFIG_HASHES}, "
            f"actual={actual_configs}"
        )


def _embedded_sources() -> dict[str, str]:
    return {
        key: path.read_text(encoding="utf-8").replace(
            "from agricola.", "from _codex_bundle.agricola."
        )
        for key, path in SOURCE_PATHS.items()
        if key != "routine_data"
    }


def _embedded_configs() -> dict[str, dict[str, Any]]:
    configs = {
        key: json.loads(path.read_text(encoding="utf-8"))
        for key, path in CONFIG_PATHS.items()
    }
    configs["routing_v4"] = load_v4_config(DEFAULT_V4D_CONFIG_PATH)
    return configs


def _build_body() -> str:
    sources = _embedded_sources()
    configs = _embedded_configs()
    metadata = {
        "release_id": RELEASE_ID,
        "model_spec_version": V4D_MODEL_SPEC_VERSION,
        "routine_sha256": ROUTINE_SHA256,
        "source_sha256": EXPECTED_SOURCE_HASHES,
        "config_sha256": EXPECTED_CONFIG_HASHES,
    }
    return f'''"""Standalone Codex E17.2 V4D D28 Kaggle candidate.

Generated from hash-verified sources.  The embedded private module namespace
keeps the complete source policy behavior without repository dependencies.
"""

import sys as _sys
import types as _types
from copy import deepcopy as _deepcopy

RELEASE_ID = {RELEASE_ID!r}
MODEL_SPEC_VERSION = {V4D_MODEL_SPEC_VERSION!r}
ROUTINE_SHA256 = {ROUTINE_SHA256!r}
BUILD_METADATA = {pprint.pformat(metadata, width=100, sort_dicts=False)}
_SOURCES = {pprint.pformat(sources, width=120, sort_dicts=False)}
_CONFIGS = {pprint.pformat(configs, width=120, sort_dicts=False)}
_ROUTINE_ACTIONS = {pprint.pformat(ROUTINE_ACTIONS, width=120, sort_dicts=False)}
_CROPS = {pprint.pformat(CROPS, width=120, sort_dicts=False)}


def _package(name):
    module = _types.ModuleType(name)
    module.__package__ = name
    module.__path__ = []
    _sys.modules[name] = module
    return module


def _plain_module(name):
    module = _types.ModuleType(name)
    module.__package__ = name.rpartition(".")[0]
    module.__file__ = "/kaggle/working/codex_bundle/" + name.replace(".", "/") + ".py"
    _sys.modules[name] = module
    return module


def _exec_module(name, source):
    module = _plain_module(name)
    exec(compile(source, module.__file__, "exec"), module.__dict__)
    return module


def _config_loader(config):
    frozen = _deepcopy(config)

    def load(path=None):
        del path
        return _deepcopy(frozen)

    return load


for _name in (
    "_codex_bundle",
    "_codex_bundle.agricola",
    "_codex_bundle.agricola.core",
    "_codex_bundle.agricola.strategy",
    "_codex_bundle.agricola.strategy.codex",
):
    _package(_name)

_state = _plain_module("_codex_bundle.agricola.core.state")
_state.CROPS = _deepcopy(_CROPS)

_routine = _plain_module(
    "_codex_bundle.agricola.strategy.codex.codex_v9_routine_data"
)
_routine.ROUTINE_ACTIONS = _ROUTINE_ACTIONS
_routine.ROUTINE_SHA256 = ROUTINE_SHA256

_observation = _exec_module(
    "_codex_bundle.agricola.core.observation_contract",
    _SOURCES["observation_contract"],
)
_v9 = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_3q_mixed_high_density",
    _SOURCES["v9"],
)
_v9.load_v9_config = _config_loader(_CONFIGS["v9"])
_guarded = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_reactive_guarded",
    _SOURCES["guarded"],
)
_guarded.load_reactive_config = _config_loader(_CONFIGS["guarded"])
_true_reactive = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_true_reactive",
    _SOURCES["true_reactive"],
)
_true_reactive.load_true_reactive_config = _config_loader(_CONFIGS["true_reactive"])
_routing_core = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_reactive_service_routing_core",
    _SOURCES["routing_core"],
)
_routing_core.load_core_config = _config_loader(_CONFIGS["routing_core"])
_routing_v3 = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_reactive_service_routing_v3",
    _SOURCES["routing_v3"],
)
_routing_v3.load_v3_config = _config_loader(_CONFIGS["routing_v3"])
_routing_v4 = _exec_module(
    "_codex_bundle.agricola.strategy.codex.codex_e17_batched_cluster_routing_v4",
    _SOURCES["routing_v4"],
)
_routing_v4.load_v4_config = _config_loader(_CONFIGS["routing_v4"])


def create_agent(run_context=None):
    return _routing_v4.create_codex_e17_batched_cluster_routing_v4(
        run_context=run_context,
        config_path=_routing_v4.DEFAULT_V4D_CONFIG_PATH,
    )


_DEFAULT_AGENT = create_agent()


def agent(observation, configuration=None):
    return _DEFAULT_AGENT(observation, configuration)
'''


def build_submission_codex_e17_v4d(output_path: Path | str | None = None) -> Path:
    """Build V4D to a separate explicit Kaggle candidate path."""

    _verify_inputs()
    target = Path(output_path) if output_path is not None else TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_build_body(), encoding="utf-8", newline="\n")
    return target


def main() -> int:
    target = build_submission_codex_e17_v4d()
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
