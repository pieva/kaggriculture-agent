"""Antigravity E19.2 Hybrid Livestock Policy — V2.

Candidate ID: ANTIGRAVITY_E19_2_HYBRID_LIVESTOCK_V2
Model Spec Version: ANTIGRAVITY-E19.2-HYBRID-LIVESTOCK-V2

Evolution from E19.1:
1. Zero-Escape Fodder Shield:
   - Terminal wheat protection: even during flush (D27-D30), retains (animals_count + 1) * remaining_days
     in shed, selling only surplus wheat.
   - Guaranteed emergency procurement: buys WHEAT via BUY_PRODUCT through D30 (removes day < 28 cutoff).
   - Worker FEED guard: prevents invalid/failed FEED calls when inventory has 0 wheat; routes to shed instead.
   - Protects needed worker feed from premature DROP actions on terminal days.
2. Early Melon Catalyst:
   - High-priority Melon seed allocation in D01-D05 (target 10 tiles) to capture the D11 harvest surge ($15k+).
3. Scaled Workforce Capacity:
   - Workforce scales up to 12 hands (13 total workers) post-D11 to manage expanded crop and animal loads.
4. Active Capacity Governor Through D30:
   - Governor remains active through D30 for zero-displacement task recovery.
"""

from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "ANTIGRAVITY-E19.2-HYBRID-LIVESTOCK-V2"
CANDIDATE_ID = "ANTIGRAVITY_E19_2_HYBRID_LIVESTOCK_V2"

_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parents[4]
DEFAULT_CONFIG_PATH = (
    _REPO_ROOT
    / "docs"
    / "model_specs"
    / "antigravity"
    / "configs"
    / "ANTIGRAVITY_E19_2_HYBRID_LIVESTOCK_V2.json"
)

MOVE_OPCODES = frozenset({"PASS", "NORTH", "SOUTH", "EAST", "WEST"})
FIBONACCI_HIRE = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377)


def _hire_cost(hires_today: int) -> float:
    if hires_today < len(FIBONACCI_HIRE):
        return float(FIBONACCI_HIRE[hires_today])
    return float(FIBONACCI_HIRE[-1])


def _manhattan_step(current: tuple[int, int], target: tuple[int, int]) -> str:
    cx, cy = current
    tx, ty = target
    if cx < tx:
        return "EAST"
    if cx > tx:
        return "WEST"
    if cy < ty:
        return "SOUTH"
    if cy > ty:
        return "NORTH"
    return "PASS"


def _quadrant_of(x: int, y: int) -> str:
    if x <= 4 and y <= 4:
        return "Q0"
    if x >= 5 and y <= 4:
        return "Q1"
    if x <= 4 and y >= 5:
        return "Q2"
    return "Q3"


class AntigravityE19_2HybridLivestockPolicy:
    """Antigravity E19.2 Autonomous Hybrid Livestock & Capacity Governed Controller."""

    def __init__(
        self,
        *,
        config: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        if config is not None:
            self.config = copy.deepcopy(config)
        else:
            path = Path(config_path or DEFAULT_CONFIG_PATH)
            if path.exists():
                self.config = json.loads(path.read_text(encoding="utf-8"))
            else:
                self.config = {}

        self.run_context = copy.deepcopy(run_context or {})
        self.candidate_id = str(self.config.get("candidate_id", CANDIDATE_ID))
        self.model_spec_version = str(self.config.get("model_spec_version", POLICY_VERSION))
        self.run_id = str(self.run_context.get("run_id", "antigravity-e19-2-run"))
        self.episode_id = str(self.run_context.get("episode_id", "antigravity-e19-2-episode"))
        self.seed = self.run_context.get("seed")
        self.player_position = self.run_context.get("player_position")

        # Telemetry & stats
        self.technical_errors = 0
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None

        self.final_money = 0.0
        self.max_hands = 0
        self.max_quadrants = 1
        self.max_active_animals = 0
        self.peak_crops = 0
        self.peak_hands = 0
        self.animal_escapes = 0

        self.action_counts: Counter[str] = Counter()
        self.sale_requests: Counter[str] = Counter()
        self.purchase_requests: Counter[str] = Counter()
        self.recovery_breakdown: Counter[str] = Counter()
        self.recovery_service_commands = 0

        # State tracking
        self._last_day: int | None = None
        self._hires_today = 0
        self._last_known_animals = 0
        self._worker_assignments: dict[int, tuple[tuple[int, int], str, str]] = {}

        # Parameters from config
        self.shed_tile = tuple(self.config.get("shed_access_tile", [4, 4]))
        self.cash_reserve = float(self.config.get("cash_reserve", 300.0))
        self.governor_enabled = bool(self.config.get("capacity_governor_enabled", True))
        self.terminal_passthrough_day = int(self.config.get("terminal_passthrough_day", 31))

        livestock_cfg = self.config.get("livestock", {})
        self.target_cows = int(livestock_cfg.get("target_cows", 4))
        self.target_sheep = int(livestock_cfg.get("target_sheep", 2))
        self.stop_livestock_buy_day = int(livestock_cfg.get("stop_buy_day", 20))
        self.feed_safety_buffer = int(livestock_cfg.get("feed_safety_buffer", 3))

        raw_q0 = livestock_cfg.get("pasture_cluster_q0", [[3, 3], [3, 4], [4, 3]])
        raw_q1 = livestock_cfg.get("pasture_cluster_q1", [[5, 4], [5, 3], [6, 3]])
        self.pasture_cluster_q0 = [tuple(p) for p in raw_q0]
        self.pasture_cluster_q1 = [tuple(p) for p in raw_q1]
        self.all_designated_pastures = self.pasture_cluster_q0 + self.pasture_cluster_q1

    def _observe_state(self, observation: dict[str, Any], configuration: Any) -> Any:
        return CodexObservationAdapter.parse(
            observation,
            configuration,
            fallback_turns_per_day=int(self.config.get("turns_per_day", 24)),
            fallback_episode_steps=int(self.config.get("episode_steps", 720)),
        )

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            state = self._observe_state(observation, configuration)
            day = int(state.clock.day)
            hour = int(state.clock.hour)

            player = int(observation.get("player", 0))
            farms = observation.get("farms", []) or []
            farm = farms[player] if 0 <= player < len(farms) else {}
            private = observation.get("private", {}) or {}

            self.final_money = float(farm.get("money", 0.0) or 0.0)

            # Detect new day
            if self._last_day != day:
                self._last_day = day
                self._hires_today = 0
                self._worker_assignments.clear()

            # Identify owned quadrants
            raw_quadrants = farm.get("unlocked_quadrants", ["Q0"]) or ["Q0"]
            owned_quadrants = set()
            for q in raw_quadrants:
                if q in ("Q0", "NW"):
                    owned_quadrants.add("Q0")
                elif q in ("Q1", "NE"):
                    owned_quadrants.add("Q1")
                elif q in ("Q2", "SW"):
                    owned_quadrants.add("Q2")
                elif q in ("Q3", "SE"):
                    owned_quadrants.add("Q3")
            self.max_quadrants = max(self.max_quadrants, len(owned_quadrants))

            # Track worker count
            farmer_pos = tuple(farm.get("farmer", [4, 4]))
            hands = farm.get("hands", []) or []
            hand_positions = [tuple(h) for h in hands]
            self.max_hands = max(self.max_hands, len(hands))
            self.peak_hands = max(self.peak_hands, len(hands))

            # Scan board for animals, pastures, crops
            tiles = farm.get("tiles", []) or []
            animals_on_board = 0
            crops_on_board = 0
            for row in tiles:
                if not isinstance(row, list):
                    continue
                for t in row:
                    if isinstance(t, dict):
                        if t.get("animal"):
                            animals_on_board += 1
                        elif t.get("kind") == "PLANT":
                            crops_on_board += 1

            self.max_active_animals = max(self.max_active_animals, animals_on_board)
            self.peak_crops = max(self.peak_crops, crops_on_board)

            # Track animal escapes (drop from previous observation)
            if self._last_known_animals > animals_on_board:
                self.animal_escapes += (self._last_known_animals - animals_on_board)
            self._last_known_animals = animals_on_board

            # 1. Market Orders
            market_orders = self._market_orders(
                farm=farm,
                private=private,
                day=day,
                hour=hour,
                owned_quadrants=owned_quadrants,
                animals_count=animals_on_board,
            )

            # 2. Field & Livestock Tasks
            tasks = self._generate_tasks(
                farm=farm,
                private=private,
                day=day,
                hour=hour,
                owned_quadrants=owned_quadrants,
            )

            # 3. Allocate Workers
            farmer_action, hands_actions = self._allocate_workers(
                farmer_pos=farmer_pos,
                hand_positions=hand_positions,
                tasks=tasks,
                farm=farm,
                private=private,
                day=day,
                hour=hour,
                owned_quadrants=owned_quadrants,
            )

            # 4. On-Tile Capacity Governor
            if self.governor_enabled and day < self.terminal_passthrough_day:
                farmer_action, hands_actions = self._apply_capacity_governor(
                    farmer_action=farmer_action,
                    hands_actions=hands_actions,
                    farmer_pos=farmer_pos,
                    hand_positions=hand_positions,
                    farm=farm,
                    private=private,
                    day=day,
                )

            # Record action counts
            if farmer_action:
                self.action_counts[farmer_action[0]] += 1
            for ha in hands_actions:
                if ha:
                    self.action_counts[ha[0]] += 1

            return {
                "farmer": farmer_action,
                "hands": hands_actions,
                "market": market_orders,
            }

        except Exception as ex:
            self.technical_errors += 1
            self.error_count += 1
            self.fallback_count += 1
            self.last_exception = str(ex)
            hands_len = len(observation.get("farms", [{}])[observation.get("player", 0)].get("hands", []))
            return {
                "farmer": ["PASS"],
                "hands": [["PASS"] for _ in range(hands_len)],
                "market": [],
            }

    # --------------------------------------------------------------------------
    # Market & Procurement
    # --------------------------------------------------------------------------
    def _market_orders(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        day: int,
        hour: int,
        owned_quadrants: set[str],
        animals_count: int,
    ) -> list[list[Any]]:
        orders: list[list[Any]] = []
        money = float(farm.get("money", 0.0) or 0.0)
        shed = private.get("shed", {}) or {}
        seeds = private.get("seeds", {}) or {}
        market_cfg = self.config.get("market", {})
        order_cap = int(market_cfg.get("order_cap", 10))

        # A. SELL produce from shed
        sell_thresh = int(market_cfg.get("sell_threshold", 2))
        flush_day = int(market_cfg.get("shed_flush_start_day", 27))

        # Items to sell: MILK, WOOL, MELON, CARROT, surplus WHEAT, FERTILIZER
        wheat_in_shed = int(shed.get("WHEAT", 0) or 0)
        # E19.2 Zero-Escape Fodder Shield:
        # Protect enough grain to feed all animals until Day 30 H23
        remaining_days = max(1, 31 - day)
        feed_reserved = (animals_count + 1) * 2
        terminal_feed_reserved = (animals_count + 1) * remaining_days

        for item, qty in sorted(shed.items()):
            qty_int = int(qty or 0)
            if qty_int <= 0:
                continue

            sell_qty = 0
            if item == "WHEAT":
                if day >= flush_day:
                    if qty_int > terminal_feed_reserved:
                        sell_qty = qty_int - terminal_feed_reserved
                elif qty_int > feed_reserved:
                    sell_qty = qty_int - feed_reserved
            elif item in ("MILK", "WOOL", "MELON", "CARROT", "EGG", "FERTILIZER"):
                if day >= flush_day or qty_int >= sell_thresh or money < self.cash_reserve:
                    sell_qty = qty_int

            if sell_qty > 0 and len(orders) < order_cap:
                orders.append(["SELL", item, sell_qty])
                self.sale_requests[item] += sell_qty

        # B. HIRE workforce at Hour 0
        if hour == 0 and len(orders) < order_cap:
            workforce_cfg = self.config.get("workforce", {})
            target_hands = int(workforce_cfg.get("target_hands", 8))
            max_hands = int(workforce_cfg.get("max_hands", 12))
            current_hands = len(farm.get("hands", []) or [])

            # Scale hands smoothly with day, capital, and workload
            if day == 0:
                desired_hands = int(workforce_cfg.get("day_0_max_hands", 3))
            elif day < 5:
                desired_hands = 4
            elif day < 11:
                desired_hands = 6
            elif money > 3000.0:
                desired_hands = max_hands
            elif money > 1500.0:
                desired_hands = min(10, max_hands)
            else:
                desired_hands = min(target_hands, max_hands)

            needed_hires = max(0, desired_hands - current_hands)
            while needed_hires > 0 and len(orders) < order_cap:
                hire_cost = _hire_cost(current_hands + self._hires_today)
                min_reserve = float(workforce_cfg.get("min_cash_after_hire", 200.0))
                if money - hire_cost >= min_reserve:
                    orders.append(["HIRE"])
                    money -= hire_cost
                    self._hires_today += 1
                    self.purchase_requests["HIRE"] += 1
                    needed_hires -= 1
                else:
                    break

        # C. BUY_LAND (Quadrant expansions)
        if "Q1" not in owned_quadrants and len(orders) < order_cap:
            q1_day = int(self.config.get("q1_unlock_day", 5))
            q1_cash = float(self.config.get("q1_min_cash", 1400.0))
            if day >= q1_day and money >= q1_cash:
                orders.append(["BUY_LAND"])
                money -= 1000.0
                self.purchase_requests["BUY_LAND_Q1"] += 1

        if "Q1" in owned_quadrants and "Q2" not in owned_quadrants and len(orders) < order_cap:
            q2_day = int(self.config.get("q2_unlock_day", 12))
            q2_cash = float(self.config.get("q2_min_cash", 2500.0))
            if day >= q2_day and money >= q2_cash:
                orders.append(["BUY_LAND"])
                money -= 2000.0
                self.purchase_requests["BUY_LAND_Q2"] += 1

        # D. BUY_ANIMAL (Cows & Sheep)
        livestock_cfg = self.config.get("livestock", {})
        cows_target = self.target_cows
        sheep_target = self.target_sheep
        cow_cost = float(livestock_cfg.get("cow_cost", 400.0))
        sheep_cost = float(livestock_cfg.get("sheep_cost", 500.0))

        # Count owned animals
        cows_owned = int(shed.get("COW", 0) or 0)
        sheep_owned = int(shed.get("SHEEP", 0) or 0)
        for row in farm.get("tiles", []):
            if isinstance(row, list):
                for t in row:
                    if isinstance(t, dict):
                        if t.get("animal") == "COW":
                            cows_owned += 1
                        elif t.get("animal") == "SHEEP":
                            sheep_owned += 1

        # Count built pastures
        pastures_built = 0
        for row in farm.get("tiles", []):
            if isinstance(row, list):
                for t in row:
                    if isinstance(t, dict) and t.get("kind") == "PASTURE":
                        pastures_built += 1

        # Feed buffer check (grain only, seeds are not edible)
        wheat_supply = wheat_in_shed
        total_animals = cows_owned + sheep_owned
        feed_demand = total_animals
        has_feed_buffer = wheat_supply >= (feed_demand + self.feed_safety_buffer)

        if (
            day >= 4
            and day <= self.stop_livestock_buy_day
            and has_feed_buffer
            and len(orders) < order_cap
        ):
            # Prioritize Cows ($400, $160 milk every 2 days)
            if cows_owned < cows_target and pastures_built > total_animals:
                if money - cow_cost >= self.cash_reserve:
                    orders.append(["BUY_ANIMAL", "COW", 1])
                    money -= cow_cost
                    self.purchase_requests["COW"] += 1
            # Then Sheep ($500, $200 wool every 3 days)
            elif sheep_owned < sheep_target and pastures_built > total_animals:
                if money - sheep_cost >= self.cash_reserve:
                    orders.append(["BUY_ANIMAL", "SHEEP", 1])
                    money -= sheep_cost
                    self.purchase_requests["SHEEP"] += 1

        # E. Proactive Fodder Supply (Zero-Escape Guard)
        # Always maintain safe fodder through Day 30
        safe_fodder_target = max(total_animals * 2, 4) if total_animals > 0 else 0
        if total_animals > 0 and wheat_in_shed < safe_fodder_target and day <= 30 and len(orders) < order_cap:
            needed_feed = safe_fodder_target - wheat_in_shed
            est_cost = needed_feed * 25.0
            if money - est_cost >= self.cash_reserve:
                orders.append(["BUY_PRODUCT", "WHEAT", needed_feed])
                money -= est_cost
                self.purchase_requests["FODDER_WHEAT"] += needed_feed
            elif money >= 25.0:
                can_buy = int(min(needed_feed, money // 25.0))
                if can_buy > 0:
                    orders.append(["BUY_PRODUCT", "WHEAT", can_buy])
                    money -= can_buy * 25.0
                    self.purchase_requests["FODDER_WHEAT"] += can_buy

        # F. BUY_SEED (Crop schedule targets)
        if day < int(self.config.get("crop_schedule", {}).get("all_plant_cutoff", 26)) and len(orders) < order_cap:
            seed_targets = self._get_seed_targets(day)
            crops_cfg = self.config.get("crops", {})

            for crop, target in seed_targets.items():
                if len(orders) >= order_cap:
                    break
                curr = int(seeds.get(crop, 0) or 0)
                price = float(crops_cfg.get(crop, {}).get("seed_price", 20.0))
                if curr < target:
                    needed = target - curr
                    cost = price * needed
                    if money - cost >= self.cash_reserve:
                        orders.append(["BUY_SEED", crop, needed])
                        money -= cost
                        self.purchase_requests[f"SEED_{crop}"] += needed
                    elif money - price >= self.cash_reserve:
                        can_buy = int((money - self.cash_reserve) // price)
                        if can_buy > 0:
                            orders.append(["BUY_SEED", crop, can_buy])
                            money -= price * can_buy
                            self.purchase_requests[f"SEED_{crop}"] += can_buy

        return orders

    def _get_seed_targets(self, day: int) -> dict[str, int]:
        st_cfg = self.config.get("seed_targets", {})
        schedule = self.config.get("crop_schedule", {})
        early_cut = int(schedule.get("early_phase_cutoff", 5))
        melon_cut = int(schedule.get("melon_plant_cutoff", 18))

        if day <= early_cut:
            return dict(st_cfg.get("early", {"CARROT": 2, "WHEAT": 8, "MELON": 10}))
        if day <= melon_cut:
            return dict(st_cfg.get("production", {"CARROT": 2, "WHEAT": 8, "MELON": 8}))
        return dict(st_cfg.get("late", {"CARROT": 4, "WHEAT": 8, "MELON": 0}))

    # --------------------------------------------------------------------------
    # Field Tasks Generation
    # --------------------------------------------------------------------------
    def _generate_tasks(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        day: int,
        hour: int,
        owned_quadrants: set[str],
    ) -> list[tuple[int, tuple[int, int], str, str]]:
        """Generate prioritised tasks:
        Priority 0: Animal FEED (Vital zero-escape)
        Priority 1: Animal HARVEST (Milk/Wool) & Animal CARE / FERTILIZER
        Priority 2: Mature Crop HARVEST
        Priority 3: Crop WATER
        Priority 4: Weed DIG
        Priority 5: Pasture BUILD / Animal PLACE
        Priority 6: Crop PLANT
        """
        tasks: list[tuple[int, tuple[int, int], str, str]] = []
        tiles = farm.get("tiles", []) or []
        seeds = private.get("seeds", {}) or {}
        seed_stock = dict(seeds)

        # Designated pasture coordinates
        designated_pastures = set()
        for p in self.pasture_cluster_q0:
            designated_pastures.add(p)
        if "Q1" in owned_quadrants:
            for p in self.pasture_cluster_q1:
                designated_pastures.add(p)

        # 1. Scan board
        for y, row in enumerate(tiles):
            if not isinstance(row, list):
                continue
            for x, tile in enumerate(row):
                pos = (x, y)
                q = _quadrant_of(x, y)
                if q not in owned_quadrants:
                    continue

                if isinstance(tile, dict):
                    # A. Animal on tile
                    if tile.get("animal"):
                        # Zero-escape Feed priority: everyday through D30
                        if not tile.get("fed_today", False):
                            tasks.append((0, pos, "FEED", str(tile["animal"])))

                        # Harvest Milk / Wool
                        if int(tile.get("yield_units", 0) or 0) > 0:
                            tasks.append((1, pos, "HARVEST_ANIMAL", str(tile["animal"])))

                        # Collect Fertilizer
                        if tile.get("fertilizer_available", False):
                            tasks.append((1, pos, "COLLECT_FERTILIZER", ""))

                        # Care bonus
                        if not tile.get("cared_today", False) and day < 28:
                            tasks.append((1, pos, "CARE", ""))

                    # B. Pasture without animal
                    elif tile.get("kind") == "PASTURE":
                        pass

                    # C. Weed on tile
                    elif tile.get("kind") == "WEED":
                        tasks.append((4, pos, "DIG", ""))

                    # D. Crop on tile
                    elif tile.get("kind") == "PLANT":
                        crop = str(tile.get("crop", "WHEAT")).upper()
                        yield_units = int(tile.get("yield_units", 0) or 0)
                        planted_day = int(tile.get("planted_day", day))
                        age = day - planted_day

                        crops_cfg = self.config.get("crops", {}).get(crop, {})
                        first_yield = int(crops_cfg.get("first_yield_day", 2))
                        max_yield_d = int(crops_cfg.get("max_yield_day", 4))
                        max_y = int(crops_cfg.get("max_yield", 6))

                        is_mature = (
                            age >= first_yield
                            and yield_units > 0
                            and (age >= max_yield_d or day >= 28 or yield_units >= max_y)
                        )

                        if is_mature:
                            tasks.append((2, pos, "HARVEST", crop))
                        elif not tile.get("watered_today", False):
                            tasks.append((3, pos, "WATER", crop))
                        elif age >= first_yield and yield_units > 0:
                            tasks.append((2, pos, "HARVEST", crop))

                # Empty tile (tile is None)
                elif tile is None:
                    # Check if tile is in pasture cluster
                    if pos in designated_pastures:
                        tasks.append((5, pos, "BUILD_PASTURE", ""))
                    elif day < int(self.config.get("crop_schedule", {}).get("all_plant_cutoff", 26)):
                        chosen_crop = self._select_crop_for_tile(x, y, day, seed_stock)
                        if chosen_crop and int(seed_stock.get(chosen_crop, 0)) > 0:
                            seed_stock[chosen_crop] -= 1
                            tasks.append((6, pos, "PLANT", chosen_crop))

        return tasks

    def _select_crop_for_tile(
        self,
        x: int,
        y: int,
        day: int,
        seed_stock: dict[str, int],
    ) -> str | None:
        early_cut = int(self.config.get("crop_schedule", {}).get("early_phase_cutoff", 5))
        melon_cut = int(self.config.get("crop_schedule", {}).get("melon_plant_cutoff", 18))

        if day <= early_cut:
            # D01-D05: Prioritize Melons for early surge, followed by Wheat and Carrots
            if int(seed_stock.get("MELON", 0)) > 0:
                return "MELON"
            if int(seed_stock.get("WHEAT", 0)) > 0:
                return "WHEAT"
            if int(seed_stock.get("CARROT", 0)) > 0:
                return "CARROT"
        elif day <= melon_cut:
            if int(seed_stock.get("MELON", 0)) > 0:
                return "MELON"
            if int(seed_stock.get("WHEAT", 0)) > 0:
                return "WHEAT"
            if int(seed_stock.get("CARROT", 0)) > 0:
                return "CARROT"
        else:
            # Late phase: fast crops
            if int(seed_stock.get("WHEAT", 0)) > 0:
                return "WHEAT"
            if int(seed_stock.get("CARROT", 0)) > 0:
                return "CARROT"

        # Fallback to any available seed
        for c in ("MELON", "WHEAT", "CARROT"):
            if int(seed_stock.get(c, 0)) > 0:
                return c
        return None

    # --------------------------------------------------------------------------
    # Worker Allocation & Dispatching
    # --------------------------------------------------------------------------
    def _allocate_workers(
        self,
        farmer_pos: tuple[int, int],
        hand_positions: list[tuple[int, int]],
        tasks: list[tuple[int, tuple[int, int], str, str]],
        farm: dict[str, Any],
        private: dict[str, Any],
        day: int,
        hour: int,
        owned_quadrants: set[str],
    ) -> tuple[list[str], list[list[str]]]:
        all_workers = [farmer_pos] + hand_positions
        actions: list[list[str]] = [["PASS"] for _ in all_workers]
        inventories = private.get("inventories", []) or []
        shed = private.get("shed", {}) or {}

        sorted_tasks = sorted(tasks, key=lambda t: (t[0], t[1][1], t[1][0]))
        assigned_targets: set[tuple[int, int]] = set()

        # Count unfed animals to protect feed rations in inventory
        unfed_count = sum(1 for t in tasks if t[2] == "FEED")

        for worker_idx, wpos in enumerate(all_workers):
            inv = inventories[worker_idx] if worker_idx < len(inventories) and isinstance(inventories[worker_idx], dict) else {}
            sale_produce = sum(inv.get(k, 0) for k in ("MILK", "WOOL", "MELON", "CARROT", "EGG", "FERTILIZER"))
            wheat_count = inv.get("WHEAT", 0)
            # Retain wheat needed for unfed animals
            excess_wheat = max(0, wheat_count - unfed_count)
            carrying = sale_produce + excess_wheat
            carrying_animals = inv.get("COW", 0) + inv.get("SHEEP", 0)

            # 1. Product Dropoff at Shed (Carrying >= 2 or evening / terminal)
            if carrying >= 2 or (carrying > 0 and (day >= 28 and hour >= 20)):
                if wpos == self.shed_tile:
                    actions[worker_idx] = ["DROP"]
                    self._worker_assignments.pop(worker_idx, None)
                else:
                    actions[worker_idx] = [_manhattan_step(wpos, self.shed_tile)]
                continue

            # 2. Farmer Animal Logistics (BUILD_PASTURE & PLACE)
            if worker_idx == 0:
                if carrying_animals > 0:
                    animal_type = "COW" if inv.get("COW", 0) > 0 else "SHEEP"
                    empty_pasture = None
                    for p in self.all_designated_pastures:
                        tile = self._get_tile(farm, p)
                        if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and not tile.get("animal"):
                            empty_pasture = p
                            break
                    if empty_pasture:
                        if wpos == empty_pasture:
                            actions[worker_idx] = ["PLACE", animal_type]
                        else:
                            actions[worker_idx] = [_manhattan_step(wpos, empty_pasture)]
                        continue

                shed_cows = int(shed.get("COW", 0) or 0)
                shed_sheep = int(shed.get("SHEEP", 0) or 0)
                if (shed_cows > 0 or shed_sheep > 0) and carrying_animals == 0:
                    animal_pick = "COW" if shed_cows > 0 else "SHEEP"
                    if wpos == self.shed_tile:
                        actions[worker_idx] = ["PICKUP", animal_pick, 1]
                    else:
                        actions[worker_idx] = [_manhattan_step(wpos, self.shed_tile)]
                    continue

                unbuilt_pasture = None
                for p in self.all_designated_pastures:
                    tile = self._get_tile(farm, p)
                    q = _quadrant_of(p[0], p[1])
                    if q in owned_quadrants and tile is None:
                        unbuilt_pasture = p
                        break
                if unbuilt_pasture:
                    if wpos == unbuilt_pasture:
                        actions[worker_idx] = ["BUILD_PASTURE"]
                    else:
                        actions[worker_idx] = [_manhattan_step(wpos, unbuilt_pasture)]
                    continue

            # 3. Animal Feeding Protocol (Zero-Escape Guard)
            unfed_animal_task = None
            for t in sorted_tasks:
                if t[2] == "FEED" and t[1] not in assigned_targets:
                    unfed_animal_task = t
                    break

            if unfed_animal_task:
                worker_wheat = int(inv.get("WHEAT", 0) or 0)
                wheat_in_shed = int(shed.get("WHEAT", 0) or 0)
                prio, tpos, verb, crop = unfed_animal_task

                if worker_wheat > 0:
                    assigned_targets.add(tpos)
                    if wpos == tpos:
                        actions[worker_idx] = ["FEED"]
                        self._worker_assignments.pop(worker_idx, None)
                    else:
                        actions[worker_idx] = [_manhattan_step(wpos, tpos)]
                    continue
                elif wheat_in_shed > 0 and carrying < 2:
                    assigned_targets.add(tpos)
                    self._worker_assignments[worker_idx] = (tpos, "FEED", crop)
                    if wpos == self.shed_tile:
                        pickup_qty = min(3, wheat_in_shed)
                        actions[worker_idx] = ["PICKUP", "WHEAT", pickup_qty]
                    else:
                        actions[worker_idx] = [_manhattan_step(wpos, self.shed_tile)]
                    continue

            # 4. Standard Field & Livestock Task Assignment
            task_found = None

            # First: check if worker stands directly on an unassigned task
            for t in sorted_tasks:
                if t[1] not in assigned_targets and t[1] == wpos:
                    task_found = t
                    break

            # Second: keep existing valid assignment
            if task_found is None and worker_idx in self._worker_assignments:
                curr_tpos, curr_verb, curr_crop = self._worker_assignments[worker_idx]
                for t in sorted_tasks:
                    if t[1] not in assigned_targets and t[1] == curr_tpos:
                        task_found = t
                        break

            # Third: greedy nearest task
            if task_found is None:
                candidates = [t for t in sorted_tasks if t[1] not in assigned_targets and t[2] != "BUILD_PASTURE"]
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
                assigned_targets.add(tpos)
                self._worker_assignments[worker_idx] = (tpos, verb, crop)

                if wpos == tpos:
                    if verb == "PLANT":
                        actions[worker_idx] = ["PLANT", crop]
                    elif verb in ("HARVEST", "HARVEST_ANIMAL"):
                        actions[worker_idx] = ["HARVEST"]
                    elif verb == "CARE":
                        actions[worker_idx] = ["CARE"]
                    elif verb == "COLLECT_FERTILIZER":
                        actions[worker_idx] = ["COLLECT_FERTILIZER"]
                    elif verb == "FEED":
                        # Worker MUST have wheat to execute FEED
                        if int(inv.get("WHEAT", 0) or 0) > 0:
                            actions[worker_idx] = ["FEED"]
                        elif int(shed.get("WHEAT", 0) or 0) > 0:
                            actions[worker_idx] = [_manhattan_step(wpos, self.shed_tile)]
                        else:
                            actions[worker_idx] = ["PASS"]
                    elif verb == "DIG":
                        actions[worker_idx] = ["DIG"]
                    elif verb == "WATER":
                        actions[worker_idx] = ["WATER"]
                    elif verb == "BUILD_PASTURE":
                        actions[worker_idx] = ["BUILD_PASTURE"]
                    self._worker_assignments.pop(worker_idx, None)
                else:
                    actions[worker_idx] = [_manhattan_step(wpos, tpos)]
            else:
                actions[worker_idx] = ["PASS"]

        farmer_act = actions[0] if actions else ["PASS"]
        hands_acts = actions[1:] if len(actions) > 1 else []
        return farmer_act, hands_acts

    # --------------------------------------------------------------------------
    # Upgraded On-Tile Capacity Governor
    # --------------------------------------------------------------------------
    def _apply_capacity_governor(
        self,
        farmer_action: list[str],
        hands_actions: list[list[str]],
        farmer_pos: tuple[int, int],
        hand_positions: list[tuple[int, int]],
        farm: dict[str, Any],
        private: dict[str, Any],
        day: int,
    ) -> tuple[list[str], list[list[str]]]:
        all_workers = [farmer_pos] + hand_positions
        all_actions = [farmer_action] + hands_actions
        inventories = private.get("inventories", []) or []

        # Claimed locations
        claimed_tiles: set[tuple[int, int]] = set()
        for idx, act in enumerate(all_actions):
            if act and act[0] not in MOVE_OPCODES:
                claimed_tiles.add(all_workers[idx])

        for idx, (act, wpos) in enumerate(zip(all_actions, all_workers)):
            opcode = act[0] if act else "PASS"
            if opcode not in MOVE_OPCODES:
                continue
            if wpos in claimed_tiles:
                continue

            inv = inventories[idx] if idx < len(inventories) and isinstance(inventories[idx], dict) else {}
            sale_produce = sum(inv.get(k, 0) for k in ("MILK", "WOOL", "MELON", "CARROT", "EGG", "FERTILIZER"))
            wheat_count = inv.get("WHEAT", 0)
            carrying = sale_produce + wheat_count
            if carrying >= 2:
                continue

            tile = self._get_tile(farm, wpos)
            if not isinstance(tile, dict):
                continue

            # Check for local productive recovery actions
            recovered_action = None

            # 1. Animal on-tile recovery
            if tile.get("animal"):
                # Feed recovery if worker carries wheat and animal is unfed
                if not tile.get("fed_today", False) and inv.get("WHEAT", 0) > 0:
                    recovered_action = ["FEED"]
                # Harvest milk/wool
                elif int(tile.get("yield_units", 0) or 0) > 0:
                    recovered_action = ["HARVEST"]
                # Collect fertilizer
                elif tile.get("fertilizer_available", False):
                    recovered_action = ["COLLECT_FERTILIZER"]
                # Care animal
                elif not tile.get("cared_today", False) and day < 28:
                    recovered_action = ["CARE"]

            # 2. Weed on-tile recovery
            elif tile.get("kind") == "WEED":
                recovered_action = ["DIG"]

            # 3. Crop on-tile recovery
            elif tile.get("kind") == "PLANT":
                crop = str(tile.get("crop", "WHEAT")).upper()
                yield_units = int(tile.get("yield_units", 0) or 0)
                age = day - int(tile.get("planted_day", day))
                first_yield = 2
                max_yield_d = 4

                if age >= first_yield and yield_units > 0 and (age >= max_yield_d or day >= 28):
                    recovered_action = ["HARVEST"]
                elif not tile.get("watered_today", False):
                    recovered_action = ["WATER"]

            if recovered_action:
                all_actions[idx] = recovered_action
                claimed_tiles.add(wpos)
                self.recovery_service_commands += 1
                self.recovery_breakdown[recovered_action[0]] += 1

        new_farmer_action = all_actions[0] if all_actions else ["PASS"]
        new_hands_actions = all_actions[1:] if len(all_actions) > 1 else []
        return new_farmer_action, new_hands_actions

    def _get_tile(self, farm: dict[str, Any], pos: tuple[int, int]) -> Any:
        tiles = farm.get("tiles", []) or []
        x, y = pos
        if 0 <= y < len(tiles):
            row = tiles[y]
            if isinstance(row, list) and 0 <= x < len(row):
                return row[x]
        return None


def create_antigravity_e19_2_agent(
    config: dict[str, Any] | None = None,
    run_context: dict[str, Any] | None = None,
):
    """Factory creating the E19.2 Hybrid Livestock policy callable."""
    policy = AntigravityE19_2HybridLivestockPolicy(
        config=config,
        run_context=run_context,
    )

    def _agent(obs, conf=None):
        return policy(obs, conf)

    _agent.policy = policy  # type: ignore[attr-defined]
    return _agent
