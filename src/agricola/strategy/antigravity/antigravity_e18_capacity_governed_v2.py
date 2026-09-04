"""Antigravity E18.2 Capacity-Governed Controller — V2.

Autonomous implementation of ANTIGRAVITY-E18.2-CAPACITY-GOVERNED-V1.
Constructed in strict accordance with:
- docs/model_specs/antigravity/e18/prompts/E18_ANTIGRAVITY_CAPACITY_THROUGHPUT_V2_PROMPT_IT.md
- Structural precedent: Codex E18.2 capacity governor (on-tile-only service recovery)
- Preserves the proven V1 chassis (lifecycle, task scan, dual regimes, public opponent snapshot)
- Implements toggleable on-tile recovery over otherwise-idle or uncommitted worker movement
- Replaces MOVE/PASS with local on-tile service (HARVEST, DIG, WATER) without moving away
- Byte-for-byte authoritative baseline parity when capacity_governor_enabled is False
- Terminal passthrough on Day 28+ for safe endgame liquidations
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter
from agricola.strategy.antigravity.antigravity_e18_reactive_reboot_v1 import (
    AntigravityE18ReactiveRebootPolicy,
    _quadrant_of,
)

POLICY_VERSION = "ANTIGRAVITY-E18.2-CAPACITY-GOVERNED-V1"

_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parents[4]
DEFAULT_CONFIG_PATH = (
    _REPO_ROOT
    / "docs"
    / "model_specs"
    / "antigravity"
    / "e18"
    / "configs"
    / "ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1.json"
)

MOVE_OPCODES = frozenset({"PASS", "NORTH", "SOUTH", "EAST", "WEST"})


class AntigravityE18CapacityGovernedPolicy:
    """Capacity-governed overlay over the proven Antigravity E18.1 reboot chassis."""

    def __init__(
        self,
        *,
        config: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        if config is not None:
            self.config = deepcopy(config)
        else:
            path = Path(config_path or DEFAULT_CONFIG_PATH)
            self.config = json.loads(path.read_text(encoding="utf-8"))

        self.run_context = deepcopy(run_context or {})
        self.candidate_id = str(
            self.config.get(
                "candidate_id", "ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1"
            )
        )
        self.model_spec_version = POLICY_VERSION
        self.run_id = str(self.run_context.get("run_id", "antigravity-e18-2"))
        self.episode_id = str(
            self.run_context.get("episode_id", "antigravity-e18-2-episode")
        )
        self.seed = self.run_context.get("seed")
        self.player_position = self.run_context.get("player_position")

        # Initialize base policy chassis with matching config & context
        self.base_policy = AntigravityE18ReactiveRebootPolicy(
            config=self.config,
            run_context=self.run_context,
        )

        # Governor parameters
        self.governor_enabled = bool(
            self.config.get("capacity_governor_enabled", True)
        )
        self.terminal_passthrough_day = int(
            self.config.get("terminal_passthrough_day", 28)
        )
        self.recovery_on_tile_only = bool(
            self.config.get("recovery_on_tile_only", True)
        )

        # Diagnostics & telemetry
        self.observation_count = 0
        self.recovery_service_commands = 0
        self.recovery_breakdown: Counter[str] = Counter()
        self.terminal_passthrough_batches = 0

    @property
    def error_count(self) -> int:
        return self.base_policy.error_count

    @property
    def technical_errors(self) -> int:
        return self.base_policy.technical_errors

    @property
    def fallback_count(self) -> int:
        return self.base_policy.fallback_count

    def telemetry_snapshot(self) -> dict[str, Any]:
        base_telemetry = self.base_policy.telemetry_snapshot()
        telemetry = dict(base_telemetry)
        telemetry.update(
            {
                "candidate_id": self.candidate_id,
                "model_spec_version": self.model_spec_version,
                "capacity_governor_enabled": self.governor_enabled,
                "terminal_passthrough_day": self.terminal_passthrough_day,
                "recovery_service_commands": self.recovery_service_commands,
                "recovery_breakdown": dict(self.recovery_breakdown),
                "terminal_passthrough_batches": self.terminal_passthrough_batches,
                "base_policy_candidate": base_telemetry.get("candidate_id"),
            }
        )
        return telemetry

    def _route_on_tile_recovery(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        configuration: Any,
        day: int,
    ) -> int:
        """Assign available on-tile tasks to eligible workers without MOVE."""
        try:
            snap = CodexObservationAdapter.parse(
                observation,
                configuration,
                fallback_turns_per_day=24,
                fallback_episode_steps=720,
            )
            farm = snap.farm
            private = snap.private
        except Exception:
            # If adapter fails, safely inspect raw observation
            my_seat = int(
                self.player_position
                if self.player_position is not None
                else observation.get("player", 0)
            )
            farms = observation.get("farms", [])
            if isinstance(farms, (list, tuple)) and 0 <= my_seat < len(farms):
                farm = farms[my_seat]
            else:
                return 0
            private = observation.get("private", {}) or {}

        farmer_pos = tuple(farm.get("farmer", [4, 4]))
        hands_pos = [tuple(h) for h in farm.get("hands", []) or []]
        worker_positions = [farmer_pos] + hands_pos

        farmer_cmd = list(action.get("farmer", ["PASS"]))
        hands_cmds = [list(h) for h in action.get("hands", [])]
        unit_actions = [farmer_cmd] + hands_cmds

        inventories = private.get("inventories", []) or []
        hour = int(observation.get("hour", int(observation.get("step", 0)) % 24) or 0)

        # Build map of positions and commands currently fulfilled this turn
        fulfilled: set[tuple[tuple[int, int], str]] = set()
        for idx, cmd in enumerate(unit_actions):
            if idx < len(worker_positions) and cmd and cmd[0] not in MOVE_OPCODES:
                fulfilled.add((worker_positions[idx], str(cmd[0])))

        crops_cfg = self.config.get("crops", {})
        tiles = farm.get("tiles", []) or []
        recoveries_this_step = 0

        for worker_idx in range(len(worker_positions)):
            if worker_idx >= len(unit_actions):
                continue
            cmd = unit_actions[worker_idx]
            # Only intercept workers who are currently moving or passing
            if not cmd or cmd[0] not in MOVE_OPCODES:
                continue

            inv = (
                inventories[worker_idx]
                if worker_idx < len(inventories) and isinstance(inventories[worker_idx], dict)
                else {}
            )
            carrying = sum(int(v or 0) for v in inv.values())

            # Do not intercept workers returning crops to shed
            if carrying >= 2 or (carrying > 0 and (day >= 27 or hour >= 22)):
                continue

            pos = worker_positions[worker_idx]
            x, y = pos
            if not (0 <= y < len(tiles) and 0 <= x < len(tiles[y])):
                continue
            tile = tiles[y][x]
            if not isinstance(tile, dict):
                continue

            kind = tile.get("kind")
            # 1. Weed recovery on-tile
            if kind == "WEED" and (pos, "DIG") not in fulfilled:
                unit_actions[worker_idx] = ["DIG"]
                fulfilled.add((pos, "DIG"))
                self.recovery_service_commands += 1
                self.recovery_breakdown["DIG"] += 1
                recoveries_this_step += 1

            # 2. Crop recovery on-tile (HARVEST or WATER)
            elif kind == "PLANT":
                crop = str(tile.get("crop", "CARROT")).upper()
                yield_units = int(tile.get("yield_units", 0) or 0)
                planted_day = int(tile.get("planted_day", day))
                age = day - planted_day
                cd = crops_cfg.get(crop, {})
                first_yield = int(cd.get("first_yield_day", 2))
                max_yield_d = int(cd.get("max_yield_day", 3))
                max_yield = int(cd.get("max_yield", 4))

                is_ready = (
                    (age >= first_yield)
                    and (yield_units > 0)
                    and (age >= max_yield_d or day >= 28 or yield_units >= max_yield)
                )

                if is_ready and (pos, "HARVEST") not in fulfilled:
                    unit_actions[worker_idx] = ["HARVEST"]
                    fulfilled.add((pos, "HARVEST"))
                    self.recovery_service_commands += 1
                    self.recovery_breakdown["HARVEST"] += 1
                    recoveries_this_step += 1
                elif (
                    not tile.get("watered_today", False)
                    and (pos, "WATER") not in fulfilled
                    and day < 28
                ):
                    unit_actions[worker_idx] = ["WATER"]
                    fulfilled.add((pos, "WATER"))
                    self.recovery_service_commands += 1
                    self.recovery_breakdown["WATER"] += 1
                    recoveries_this_step += 1

        if recoveries_this_step > 0:
            action["farmer"] = unit_actions[0]
            action["hands"] = unit_actions[1:]

        return recoveries_this_step

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        self.observation_count += 1
        provider_action = self.base_policy(observation, configuration)

        if not self.governor_enabled:
            return deepcopy(provider_action)

        step = int(observation.get("step", 0) or 0)
        day = int(observation.get("day", step // 24) or 0)

        if day >= self.terminal_passthrough_day:
            self.terminal_passthrough_batches += 1
            return deepcopy(provider_action)

        action = deepcopy(provider_action)
        self._route_on_tile_recovery(action, observation, configuration, day)
        return action


def create_antigravity_e18_capacity_governed_agent(
    config: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    run_context: dict[str, Any] | None = None,
) -> Any:
    """Factory callable creating an autonomous Antigravity E18.2 capacity-governed agent."""
    policy = AntigravityE18CapacityGovernedPolicy(
        config=config,
        config_path=config_path,
        run_context=run_context,
    )

    def agent(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        return policy(observation, configuration)

    agent.antigravity_e18_instance = policy
    agent.telemetry_snapshot = policy.telemetry_snapshot
    agent.candidate_id = policy.candidate_id
    agent.model_spec_version = policy.model_spec_version
    return agent
