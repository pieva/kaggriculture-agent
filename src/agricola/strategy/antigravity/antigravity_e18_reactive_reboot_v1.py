"""Antigravity E18.1 Opponent-Reactive Controller — Reboot V1.

Autonomous implementation of ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1.
Constructed in full compliance with:
- docs/model_specs/antigravity/e18/prompts/E18_ANTIGRAVITY_REACTIVE_V1_REBOOT_PROMPT_IT.md
- Policy-neutral observation contract (CodexObservationAdapter)
- Explicit crop lifecycle and task management
- Backlog-governed workforce sizing (Fibonacci HIRE at hour 0)
- Capital protection (seed reserve prioritized before land expansion)
- One-time D4-D8 public opponent farm snapshot and sticky regime selection
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1"

_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parents[4]
DEFAULT_CONFIG_PATH = (
    _REPO_ROOT
    / "docs"
    / "model_specs"
    / "antigravity"
    / "e18"
    / "configs"
    / "ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1.json"
)

SAFE_PASS: dict[str, Any] = {"farmer": ["PASS"], "hands": [], "market": []}
MOVE_OPCODES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})
PRODUCTIVE_OPCODES = frozenset({"DIG", "PLANT", "WATER", "HARVEST"})

# Fibonacci sequence for HIRE cost
_FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]


def _hire_cost(hires_today: int) -> int:
    if hires_today < len(_FIB):
        return _FIB[hires_today]
    return _FIB[-1]


def _quadrant_of(x: int, y: int) -> str:
    if x < 5 and y < 5:
        return "Q0"
    if x >= 5 and y < 5:
        return "Q1"
    if x < 5 and y >= 5:
        return "Q2"
    return "Q3"


def _manhattan_step(origin: tuple[int, int], target: tuple[int, int]) -> str:
    ox, oy = origin
    tx, ty = target
    if ox < tx:
        return "EAST"
    if ox > tx:
        return "WEST"
    if oy < ty:
        return "SOUTH"
    if oy > ty:
        return "NORTH"
    return "PASS"


class AntigravityE18ReactiveRebootPolicy:
    """Opponent-reactive controller with lifecycle planning and workforce governance."""

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
        self.candidate_id = str(self.config.get("candidate_id", "ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1"))
        self.model_spec_version = POLICY_VERSION
        self.run_id = str(self.run_context.get("run_id", "antigravity-e18-1"))
        self.episode_id = str(self.run_context.get("episode_id", "antigravity-e18-1-episode"))
        self.seed = self.run_context.get("seed")
        self.player_position = self.run_context.get("player_position")

        # Telemetry and state
        self.technical_errors = 0
        self.error_count = 0  # alias for tournament runner compatibility
        self.fallback_count = 0
        self.last_exception: str | None = None

        self.final_money = 0.0
        self.max_hands = 0
        self.max_quadrants = 1
        self.max_active_animals = 0
        self.max_active_crops = 0
        self.peak_crops = 0
        self.peak_hands = 0
        self.peak_animals = 0
        self.final_crops = 0
        self.final_weeds = 0
        self.backlog = 0

        self.action_counts: Counter[str] = Counter()
        self.sale_requests: Counter[str] = Counter()
        self.purchase_requests: Counter[str] = Counter()

        # Regime & Snapshot state
        self.current_regime = "BALANCED_SERVICE"
        self.regime_signature = ["BALANCED_SERVICE"]
        self.regime_transitions = 0
        self.mode_decisions = 0
        self.decision_day: int | None = None
        self.decision_pressure: float | None = None
        self._snapshot_taken = False

        # Daily tracking
        self._last_day: int | None = None
        self._hires_today = 0

        # Persistent worker target memory: worker_index -> (target_pos, verb, crop)
        self._worker_assignments: dict[int, tuple[tuple[int, int], str, str]] = {}

    def _observe_state(self, observation: dict[str, Any], configuration: Any) -> Any:
        return CodexObservationAdapter.parse(
            observation,
            configuration,
            fallback_turns_per_day=int(self.config.get("turns_per_day", 24)),
            fallback_episode_steps=int(self.config.get("episode_steps", 720)),
        )

    def _public_opponent_snapshot(self, observation: dict[str, Any], my_seat: int) -> dict[str, Any]:
        farms = observation.get("farms", []) or []
        opp_seat = 1 - my_seat if len(farms) > 1 else 0
        opp = farms[opp_seat] if 0 <= opp_seat < len(farms) and isinstance(farms[opp_seat], dict) else {}
        tiles = opp.get("tiles", []) or []
        hands = opp.get("hands", []) or []

        crop_tiles = 0
        weed_tiles = 0
        animal_tiles = 0
        for row in tiles:
            if not isinstance(row, list):
                continue
            for tile in row:
                if isinstance(tile, dict):
                    if tile.get("kind") == "PLANT":
                        crop_tiles += 1
                    elif tile.get("kind") == "WEED":
                        weed_tiles += 1
                    if tile.get("animal") is not None:
                        animal_tiles += 1

        pressure_score = float(crop_tiles * 2 + weed_tiles * 3 + len(hands) * 3 + animal_tiles * 2)
        return {
            "crop_tiles": crop_tiles,
            "weed_tiles": weed_tiles,
            "animal_tiles": animal_tiles,
            "hands": len(hands),
            "unlocked_quadrants": opp.get("unlocked_quadrants", []),
            "money": float(opp.get("money", 0.0) or 0.0),
            "pressure_score": pressure_score,
        }

    def _classify_and_select_regime(self, day: int, hour: int, snapshot: dict[str, Any]) -> None:
        start_day = int(self.config.get("snapshot_day_start", 4))
        end_day = int(self.config.get("snapshot_day_end", 8))
        target_day = int(self.config.get("default_snapshot_day", 6))

        if not self._snapshot_taken and (day >= target_day or (day >= start_day and hour == 0)):
            score = snapshot["pressure_score"]
            threshold = float(self.config.get("pressure_threshold", 20.0))
            if score >= threshold:
                chosen = "EXPANSION_TEMPO"
            else:
                chosen = "BALANCED_SERVICE"

            self.current_regime = chosen
            self.regime_signature = [chosen]
            self.mode_decisions = 1
            self.decision_day = day
            self.decision_pressure = score
            self.regime_transitions += 1
            self._snapshot_taken = True

    def _active_regime_config(self) -> dict[str, Any]:
        regimes = self.config.get("regimes", {})
        return regimes.get(self.current_regime, regimes.get("BALANCED_SERVICE", {}))

    def _owned_quadrants(self, farm: dict[str, Any]) -> set[str]:
        unlocked = farm.get("unlocked_quadrants", []) or []
        names: set[str] = set()
        for entry in unlocked:
            val = str(entry).upper()
            if val in {"NW", "Q0"}:
                names.add("Q0")
            elif val in {"NE", "Q1"}:
                names.add("Q1")
            elif val in {"SW", "Q2"}:
                names.add("Q2")
            elif val in {"SE", "Q3"}:
                names.add("Q3")
        if not names:
            names.add("Q0")
        return names

    def _tile_is_in_allowed_quadrant(self, x: int, y: int, owned: set[str], allowed: list[str]) -> bool:
        q = _quadrant_of(x, y)
        return (q in owned) and (q in allowed)

    def _generate_tasks(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        day: int,
        owned_quadrants: set[str],
        regime_cfg: dict[str, Any],
    ) -> list[tuple[int, tuple[int, int], str, str]]:
        """Generate tasks with priority: HARVEST (0), WATER (1), DIG (2), PLANT (3)."""
        tasks: list[tuple[int, tuple[int, int], str, str]] = []
        tiles = farm.get("tiles", []) or []
        seeds = private.get("seeds", {}) or {}
        allowed = regime_cfg.get("allowed_quadrants", ["Q0", "Q1"])
        crops_cfg = self.config.get("crops", {})

        seed_stock = dict(seeds)

        for y, row in enumerate(tiles):
            if not isinstance(row, list):
                continue
            for x, tile in enumerate(row):
                if not self._tile_is_in_allowed_quadrant(x, y, owned_quadrants, allowed):
                    continue

                if isinstance(tile, dict) and tile.get("kind") == "WEED":
                    # Clear weeds
                    tasks.append((2, (x, y), "DIG", ""))
                elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    crop = str(tile.get("crop", "CARROT")).upper()
                    yield_units = int(tile.get("yield_units", 0) or 0)
                    planted_day = int(tile.get("planted_day", day))
                    age = day - planted_day
                    cd = crops_cfg.get(crop, {})
                    first_yield = int(cd.get("first_yield_day", 2))
                    max_yield_d = int(cd.get("max_yield_day", 3))

                    # Can only be harvested if age >= first_yield_day
                    is_ready_to_harvest = (age >= first_yield) and (yield_units > 0) and (age >= max_yield_d or day >= 28 or yield_units >= int(cd.get("max_yield", 4)))

                    if is_ready_to_harvest:
                        # Priority 0: Ready to harvest
                        tasks.append((0, (x, y), "HARVEST", crop))
                    elif not tile.get("watered_today", False):
                        # Priority 1: Water growing plant
                        tasks.append((1, (x, y), "WATER", crop))
                    elif age >= first_yield and yield_units > 0:
                        # Priority 0: Harvest if mature
                        tasks.append((0, (x, y), "HARVEST", crop))
                elif tile is None:
                    # Empty tile: plant if we have seeds
                    quad = _quadrant_of(x, y)
                    chosen_crop = "CARROT" if quad == "Q0" else "WHEAT"
                    if int(seed_stock.get(chosen_crop, 0)) > 0 and day < 27:
                        seed_stock[chosen_crop] -= 1
                        tasks.append((3, (x, y), "PLANT", chosen_crop))

        return tasks

    def _allocate_workers(
        self,
        worker_positions: list[tuple[int, int]],
        tasks: list[tuple[int, tuple[int, int], str, str]],
        private: dict[str, Any],
        day: int,
        hour: int,
    ) -> list[list[str]]:
        """Assign tasks to workers and return action opcode lists."""
        actions: list[list[str]] = [["PASS"] for _ in worker_positions]
        if not worker_positions:
            return actions

        inventories = private.get("inventories", []) or []
        shed_tile = (4, 4)

        # Sort tasks by priority
        sorted_tasks = sorted(tasks, key=lambda t: (t[0], t[1][1], t[1][0]))
        assigned_tasks: set[tuple[int, int]] = set()

        for worker_idx, wpos in enumerate(worker_positions):
            inv = inventories[worker_idx] if worker_idx < len(inventories) and isinstance(inventories[worker_idx], dict) else {}
            carrying = sum(inv.values())

            # If carrying crops, drop off at shed
            if carrying >= 2 or (carrying > 0 and (day >= 27 or hour >= 22)):
                if wpos == shed_tile:
                    actions[worker_idx] = ["DROP"]
                    self._worker_assignments.pop(worker_idx, None)
                else:
                    actions[worker_idx] = [_manhattan_step(wpos, shed_tile)]
                continue

            # Check existing assignment if still valid
            current_target = self._worker_assignments.get(worker_idx)
            task_found = None

            # First, see if worker is directly on an available task
            for t in sorted_tasks:
                if t[1] not in assigned_tasks and t[1] == wpos:
                    task_found = t
                    break

            # Next, keep existing assignment if still valid
            if task_found is None and current_target is not None:
                tpos, verb, crop = current_target
                for t in sorted_tasks:
                    if t[1] not in assigned_tasks and t[1] == tpos:
                        task_found = t
                        break

            # Otherwise, pick nearest task
            if task_found is None:
                candidates = [t for t in sorted_tasks if t[1] not in assigned_tasks]
                if candidates:
                    task_found = min(
                        candidates,
                        key=lambda t: (
                            t[0],
                            abs(t[1][0] - wpos[0]) + abs(t[1][1] - wpos[1]),
                        ),
                    )

            if task_found is not None:
                prio, tpos, verb, crop = task_found
                assigned_tasks.add(tpos)
                self._worker_assignments[worker_idx] = (tpos, verb, crop)

                if wpos == tpos:
                    if verb == "PLANT":
                        actions[worker_idx] = ["PLANT", crop]
                    else:
                        actions[worker_idx] = [verb]
                    # Task completed this turn; remove assignment
                    self._worker_assignments.pop(worker_idx, None)
                else:
                    step = _manhattan_step(wpos, tpos)
                    actions[worker_idx] = [step]
            else:
                self._worker_assignments.pop(worker_idx, None)
                # If carrying anything, head to shed
                if carrying > 0:
                    if wpos == shed_tile:
                        actions[worker_idx] = ["DROP"]
                    else:
                        actions[worker_idx] = [_manhattan_step(wpos, shed_tile)]
                else:
                    actions[worker_idx] = ["PASS"]

        return actions

    def _market_orders(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        day: int,
        hour: int,
        owned_quadrants: set[str],
        regime_cfg: dict[str, Any],
        backlog: int,
    ) -> list[list[Any]]:
        orders: list[list[Any]] = []
        money = float(farm.get("money", 0.0) or 0.0)
        shed = private.get("shed", {}) or {}
        seeds = private.get("seeds", {}) or {}

        # 1. SELL produce from shed (cash generation)
        sell_thresh = int(regime_cfg.get("sell_threshold", 2))
        for item, qty in shed.items():
            qty_int = int(qty or 0)
            if qty_int <= 0:
                continue
            if qty_int >= sell_thresh or day >= 25 or money < 300:
                orders.append(["SELL", item, qty_int])
                self.sale_requests[item] += qty_int

        # 2. HIRE hands at hour 0
        if hour == 0:
            if day != self._last_day:
                self._last_day = day
                self._hires_today = 0

            target_hands = int(regime_cfg.get("target_hands", 4))
            max_hands = int(regime_cfg.get("max_hands", 6))
            current_hands = len(farm.get("hands", []) or [])

            # Desired hands scales with backlog and day
            desired = min(max_hands, max(target_hands, min(max_hands, 1 + backlog // 4)))
            if day == 0:
                desired = min(2, desired)  # Day 0 start conservative

            while current_hands < desired:
                cost = _hire_cost(self._hires_today)
                # Keep a $150 seed reserve
                if money - cost >= 150.0:
                    orders.append(["HIRE"])
                    money -= cost
                    self._hires_today += 1
                    current_hands += 1
                    self.purchase_requests["HIRE"] += 1
                else:
                    break

        # 3. BUY_SEED if below target
        seed_targets = regime_cfg.get("seed_target", {"CARROT": 6, "WHEAT": 6})
        crops_cfg = self.config.get("crops", {})
        for crop, target in seed_targets.items():
            curr = int(seeds.get(crop, 0) or 0)
            price = float(crops_cfg.get(crop, {}).get("seed_price", 20))
            if curr < target and day < 28:
                needed = target - curr
                cost = price * needed
                if money - cost >= 100.0:
                    orders.append(["BUY_SEED", crop, needed])
                    money -= cost
                    self.purchase_requests[f"SEED_{crop}"] += needed
                elif money >= price:
                    can_buy = int(money // price)
                    if can_buy > 0:
                        orders.append(["BUY_SEED", crop, can_buy])
                        money -= price * can_buy
                        self.purchase_requests[f"SEED_{crop}"] += can_buy

        # 4. BUY_LAND (Capital-protected quadrant expansion)
        if "Q1" not in owned_quadrants and "Q1" in regime_cfg.get("allowed_quadrants", []):
            q1_day = int(regime_cfg.get("q1_unlock_day", 5))
            q1_cash = float(regime_cfg.get("q1_min_cash", 1400.0))
            if day >= q1_day and money >= q1_cash:
                orders.append(["BUY_LAND"])
                money -= 1000.0
                self.purchase_requests["LAND_Q1"] += 1

        if "Q2" not in owned_quadrants and "Q2" in regime_cfg.get("allowed_quadrants", []):
            q2_day = int(regime_cfg.get("q2_unlock_day", 10))
            q2_cash = float(regime_cfg.get("q2_min_cash", 2400.0))
            if day >= q2_day and money >= q2_cash:
                orders.append(["BUY_LAND"])
                money -= 2000.0
                self.purchase_requests["LAND_Q2"] += 1

        return orders[:8]

    def __call__(self, observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        snapshot = self._observe_state(observation, configuration)
        clock = snapshot.clock
        farm = snapshot.farm
        private = snapshot.private
        day = clock.day
        hour = clock.hour
        my_seat = snapshot.player

        # Update opponent public telemetry & regime
        opp_snap = self._public_opponent_snapshot(observation, my_seat)
        self._classify_and_select_regime(day, hour, opp_snap)
        regime_cfg = self._active_regime_config()

        # Update metrics
        hands_count = len(farm.get("hands", []) or [])
        unlocked = self._owned_quadrants(farm)
        self.final_money = float(farm.get("money", 0.0) or 0.0)
        self.max_hands = max(self.max_hands, hands_count)
        self.peak_hands = self.max_hands
        self.max_quadrants = max(self.max_quadrants, len(unlocked))

        # Count crops & weeds
        active_crops = 0
        active_weeds = 0
        tiles = farm.get("tiles", []) or []
        for row in tiles:
            if not isinstance(row, list):
                continue
            for tile in row:
                if isinstance(tile, dict):
                    if tile.get("kind") == "PLANT":
                        active_crops += 1
                    elif tile.get("kind") == "WEED":
                        active_weeds += 1

        self.max_active_crops = max(self.max_active_crops, active_crops)
        self.peak_crops = self.max_active_crops
        self.final_crops = active_crops
        self.final_weeds = active_weeds

        # 1. Generate tasks
        tasks = self._generate_tasks(farm, private, day, unlocked, regime_cfg)
        self.backlog = len(tasks)

        # 2. Worker positions: farmer first, then hands
        farmer_pos = tuple(farm.get("farmer", [4, 4]))
        worker_positions = [farmer_pos]
        for h in farm.get("hands", []) or []:
            worker_positions.append(tuple(h))

        # 3. Worker action allocation
        unit_actions = self._allocate_workers(worker_positions, tasks, private, day, hour)
        farmer_action = unit_actions[0] if unit_actions else ["PASS"]
        hands_actions = unit_actions[1:] if len(unit_actions) > 1 else []

        # 4. Market orders
        market_orders = self._market_orders(farm, private, day, hour, unlocked, regime_cfg, self.backlog)

        action = {
            "farmer": farmer_action,
            "hands": hands_actions,
            "market": market_orders,
        }

        # Track action counts
        f_op = farmer_action[0] if farmer_action else "PASS"
        self.action_counts[f_op] += 1
        for h_act in hands_actions:
            h_op = h_act[0] if h_act else "PASS"
            self.action_counts[h_op] += 1

        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        productive = sum(self.action_counts[op] for op in PRODUCTIVE_OPCODES)
        moves = sum(self.action_counts[op] for op in MOVE_OPCODES)
        passes = int(self.action_counts["PASS"])

        return {
            "agent_version": self.model_spec_version,
            "final_regime": self.current_regime,
            "regime_signature": list(self.regime_signature),
            "mode_decisions": self.mode_decisions,
            "regime_transitions": self.regime_transitions,
            "decision_day": self.decision_day,
            "decision_pressure": self.decision_pressure,
            "final_money": self.final_money,
            "money": self.final_money,
            "peak_hands": self.peak_hands,
            "max_hands": self.peak_hands,
            "peak_crops": self.peak_crops,
            "max_active_crops": self.peak_crops,
            "peak_animals": 0,
            "final_crops": self.final_crops,
            "final_weeds": self.final_weeds,
            "backlog": self.backlog,
            "productive_actions": productive,
            "move_actions": moves,
            "pass_actions": passes,
            "move_per_productive": moves / productive if productive > 0 else 0.0,
            "verified_livestock_losses": 0,
            "animal_escapes": 0,
            "technical_errors": self.technical_errors,
            "error_count": self.error_count,
            "fallbacks": self.fallback_count,
            "fallback_count": self.fallback_count,
            "action_counts": dict(self.action_counts),
            "sale_requests": dict(self.sale_requests),
            "purchase_requests": dict(self.purchase_requests),
        }


def create_antigravity_e18_agent(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    instance = AntigravityE18ReactiveRebootPolicy(
        run_context=run_context,
        config_path=config_path,
    )

    def policy(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.antigravity_e18_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001
            instance.technical_errors += 1
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.antigravity_e18_last_error = instance.last_exception
            return deepcopy(SAFE_PASS)

    policy.antigravity_instance = instance
    policy.antigravity_e18_instance = instance
    policy.antigravity_e18_last_error = None
    policy.__name__ = "antigravity_e18_reactive_reboot_policy"
    return policy


__all__ = [
    "AntigravityE18ReactiveRebootPolicy",
    "DEFAULT_CONFIG_PATH",
    "POLICY_VERSION",
    "create_antigravity_e18_agent",
]
