"""Claude E17.1 3Q reactive independent controller — V2 (remediation of V1).

State-reactive, natively-written planner/dispatcher for the E17 reactive
three-way tournament. See
``docs/model_specs/claude/MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V2.md`` for the
full design rationale, the V1 diagnosis this version remediates, and the
independence statement.

Provenance
----------
The only shared module imported from outside this namespace is
``agricola.core.observation_contract`` (policy-neutral parsing, explicitly
authorized for reuse). A handful of small numeric constants below (crop seed
prices, first-yield days, animal purchase costs and structures, land order
and prices, the ``HIRE`` Fibonacci cost formula, shed-access tile geometry)
are public ``ENGINE_VERIFIED`` / ``DERIVED_ENGINE_FACT`` facts of the
Kaggriculture environment, documented in the C2.1 Foundation and
independently confirmed against the installed environment source, and
carried forward unchanged from this agent's own V1
(``e17_reactive_3q.py``). They are environment facts, not another agent's
routine, action table, planner, dispatcher or schedule. Nothing here imports
or copies from ``agricola.strategy.codex``, ``agricola.strategy.antigravity``
or ``agricola.strategy.copilot``, and there is no action table indexed by
step.

What changed vs. V1 (see MODEL_SPEC V2 Sec. 1 for the verified diagnosis):
1. Persistent, self-invalidating per-worker target assignment
   (``_Assignment``) replaces V1's fully stateless per-call reselection,
   which measurably produced 77.4% MOVE commands and 8.3% immediate
   backtracking on development seed 26090101.
2. A "core established" guard blocks ``BUY_LAND`` until Q0 has actually
   produced (``plant_tiles_count > 0`` and a minimum count of own-requested
   ``HARVEST`` commands), closing the gap that let V1 buy land on day 0
   with zero harvests completed.
3. Workforce sizing follows the observed service backlog instead of a flat
   per-quadrant multiplier.
4. New animal purchases are blocked while any owned animal is one missed
   feed away from escaping (``LIV-08``).
5. The V1 hypothesis that ``HIRE`` requests were wasted retries was tested
   directly against the V1 ledger and falsified (zero days where requested
   hires exceeded engine-confirmed ``hires_today``); no throttle for that
   was added here, deliberately.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V2"

_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parents[4]
DEFAULT_CONFIG_PATH = (
    _REPO_ROOT
    / "docs" / "model_specs" / "claude" / "e17" / "configs"
    / "CLAUDE_E17_1_3Q_REACTIVE_V2.json"
)

SAFE_PASS_ACTION: dict[str, Any] = {"farmer": ["PASS"], "hands": [], "market": []}


class ActionValidationError(Exception):
    """Raised internally when a constructed action violates the shared
    interface contract; always caught and converted to a safe PASS."""


# ---------------------------------------------------------------------------
# Public environment facts (ENGINE_VERIFIED / DERIVED_ENGINE_FACT). See the
# module docstring: these are Foundation-documented constants of the shared
# simulation, carried forward from this agent's own V1, not a copied
# routine.
# ---------------------------------------------------------------------------

CROPS: dict[str, dict[str, Any]] = {
    "WHEAT": {"seed_price": 10, "first_yield_day": 2, "max_yield": 6, "ongoing": False},
    "CARROT": {"seed_price": 20, "first_yield_day": 2, "max_yield": 4, "ongoing": False},
    "TOMATO": {"seed_price": 50, "first_yield_day": 8, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"seed_price": 100, "first_yield_day": 10, "max_yield": 4, "ongoing": True},
    "MELON": {"seed_price": 80, "first_yield_day": 10, "max_yield": 6, "ongoing": False},
}

ANIMALS: dict[str, dict[str, Any]] = {
    "GOOSE": {"cost": 300, "structure": "COOP"},
    "COW": {"cost": 400, "structure": "PASTURE"},
    "SHEEP": {"cost": 500, "structure": "PASTURE"},
}

SELLABLE_PRODUCE = (
    "CARROT",
    "TOMATO",
    "STRAWBERRY",
    "MELON",
    "EGG",
    "MILK",
    "WOOL",
)

LAND_ORDER = ["NE", "SW", "SE"]
LAND_PRICES = [1000, 2000, 4000]

FARMER_MOVES = {
    "NORTH": (0, -1),
    "SOUTH": (0, 1),
    "EAST": (1, 0),
    "WEST": (-1, 0),
}

SERVICE_BACKLOG_KINDS = frozenset(
    {
        "URGENT_WATER",
        "FEED_NEEDED",
        "HARVEST_READY",
        "RECOVERY_DIG",
        "CARE_NEEDED",
        # PLANT_OPPORTUNITY (growth, not maintenance) is included too:
        # excluding it created a bootstrap trap where an empty Q0 has zero
        # maintenance backlog, so the load-driven target stayed at the bare
        # floor exactly when more hands were needed to fill it.
        "PLANT_OPPORTUNITY",
    }
)

# Opportunity kinds at or below this priority number risk an irreversible
# EOD loss (WEED conversion, animal escape) if left unclaimed for another
# cycle; only these may preempt an existing persistent assignment.
CRITICAL_PRIORITY_CEILING = 2


def _fibonacci(n: int) -> int:
    a, b = 1, 1
    for _ in range(max(0, int(n))):
        a, b = b, a + b
    return a


def _hire_cost_estimate(hires_today: int) -> float:
    return float(_fibonacci(hires_today))


def _quadrant_of(x: int, y: int, board_size: int) -> str:
    half = board_size // 2
    return ("N" if y < half else "S") + ("W" if x < half else "E")


def _shed_access_tiles(board_size: int) -> list[tuple[int, int]]:
    half = board_size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _quadrant_local_rank(x: int, y: int, quadrant: str, board_size: int) -> int:
    half = board_size // 2
    lx = x - (half if "E" in quadrant else 0)
    ly = y - (half if "S" in quadrant else 0)
    return ly * half + lx


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ReactiveConfigV2:
    policy_id: str
    target_quadrants: int
    fallback_turns_per_day: int
    fallback_episode_steps: int
    fallback_market_order_batch_limit: int
    land_purchase_reserve: float
    hire_reserve: float
    market_order_min_cash: float
    min_workers_per_quadrant: int
    max_hands: int
    hire_batch_limit_per_turn: int
    tasks_per_worker_per_day: int
    assignment_stall_timeout: int
    min_days_for_expansion_payback: int
    expansion_service_pressure_ceiling: float
    core_min_harvest_requests: int
    crop_species_rotation: tuple[str, ...]
    crop_target_fill_ratio: float
    crop_min_days_margin: int
    seed_purchase_batch_size: int
    fertilize_when_carried: bool
    livestock_species_rotation: tuple[str, ...]
    livestock_structures_target_per_quadrant: int
    feed_security_buffer_per_animal: int
    wheat_buy_price_ceiling: float
    wheat_buy_batch_cap: int
    max_at_risk_animals_for_new_purchase: int
    herd_size_workforce_divisor: int
    shutdown_days_remaining: int
    liquidation_days_remaining: int
    source_payload: dict[str, Any] = field(repr=False)

    @staticmethod
    def load(config_path: str | Path | None = None) -> ReactiveConfigV2:
        path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
        payload = json.loads(path.read_text(encoding="utf-8"))
        fallback = payload.get("fallback", {})
        cash = payload.get("cash_reserve", {})
        workforce = payload.get("workforce", {})
        dispatch = payload.get("dispatch", {})
        expansion = payload.get("expansion", {})
        crop = payload.get("crop", {})
        livestock = payload.get("livestock", {})
        endgame = payload.get("endgame", {})
        return ReactiveConfigV2(
            policy_id=str(payload.get("policy_id", POLICY_VERSION)),
            target_quadrants=int(payload.get("target_quadrants", 3)),
            fallback_turns_per_day=int(fallback.get("turns_per_day", 24)),
            fallback_episode_steps=int(fallback.get("episode_steps", 720)),
            fallback_market_order_batch_limit=int(
                fallback.get("market_order_batch_limit", 10)
            ),
            land_purchase_reserve=float(cash.get("land_purchase_reserve", 300.0)),
            hire_reserve=float(cash.get("hire_reserve", 50.0)),
            market_order_min_cash=float(cash.get("market_order_min_cash", 30.0)),
            min_workers_per_quadrant=int(workforce.get("min_workers_per_quadrant", 2)),
            max_hands=int(workforce.get("max_hands", 9)),
            hire_batch_limit_per_turn=int(workforce.get("hire_batch_limit_per_turn", 2)),
            tasks_per_worker_per_day=int(workforce.get("tasks_per_worker_per_day", 6)),
            assignment_stall_timeout=int(dispatch.get("assignment_stall_timeout", 3)),
            min_days_for_expansion_payback=int(
                expansion.get("min_days_for_expansion_payback", 4)
            ),
            expansion_service_pressure_ceiling=float(
                expansion.get("expansion_service_pressure_ceiling", 0.34)
            ),
            core_min_harvest_requests=int(expansion.get("core_min_harvest_requests", 4)),
            crop_species_rotation=tuple(
                crop.get("species_rotation", ["WHEAT", "CARROT", "MELON", "TOMATO"])
            ),
            crop_target_fill_ratio=float(crop.get("target_fill_ratio", 0.55)),
            crop_min_days_margin=int(crop.get("min_days_margin_for_planting", 1)),
            seed_purchase_batch_size=int(crop.get("seed_purchase_batch_size", 5)),
            fertilize_when_carried=bool(crop.get("fertilize_when_carried", True)),
            livestock_species_rotation=tuple(
                livestock.get("species_rotation", ["SHEEP", "COW", "GOOSE"])
            ),
            livestock_structures_target_per_quadrant=int(
                livestock.get("structures_target_per_quadrant", 4)
            ),
            feed_security_buffer_per_animal=int(
                livestock.get("feed_security_buffer_per_animal", 3)
            ),
            wheat_buy_price_ceiling=float(livestock.get("wheat_buy_price_ceiling", 45.0)),
            wheat_buy_batch_cap=int(livestock.get("wheat_buy_batch_cap", 10)),
            max_at_risk_animals_for_new_purchase=int(
                livestock.get("max_at_risk_animals_for_new_purchase", 0)
            ),
            herd_size_workforce_divisor=int(livestock.get("herd_size_workforce_divisor", 2)),
            shutdown_days_remaining=int(endgame.get("shutdown_days_remaining", 5)),
            liquidation_days_remaining=int(endgame.get("liquidation_days_remaining", 3)),
            source_payload=payload,
        )


# ---------------------------------------------------------------------------
# Online feature extraction (Section: FEATURES)
# ---------------------------------------------------------------------------


@dataclass
class _Features:
    board_size: int
    day: int
    days_remaining: int
    worker_positions: list[tuple[int, int]]
    worker_inventories: list[dict[str, int]]
    shed: dict[str, int]
    seeds: dict[str, int]
    money: float
    market_prices: dict[str, float]
    unlocked_quadrants: list[str]
    hires_today: int
    opportunities: list[dict[str, Any]]
    plant_tiles_count: int
    care_due_count: int
    crop_mix_counts: dict[str, int]
    animal_headcount: int
    unfed_animal_count: int
    at_risk_animal_count: int
    structures_total: int
    empty_structure_type_counts: dict[str, int]
    has_empty_crop_zone_tile: bool
    seed_budget: dict[str, int]
    crop_mix_running: dict[str, int]
    in_shutdown: bool
    in_liquidation: bool
    service_pressure: float


def _extract_features(cfg: ReactiveConfigV2, snap: Any) -> _Features:
    farm = snap.farm
    private = snap.private
    market = snap.market
    board_size = int(snap.configuration_snapshot.get("boardSize", 10))
    half = board_size // 2
    livestock_zone_size = cfg.livestock_structures_target_per_quadrant
    shed_tiles = set(_shed_access_tiles(board_size))

    tiles = farm.get("tiles", []) or []
    unlocked_quadrants = list(farm.get("unlocked_quadrants", []) or [])
    shed = {str(k): int(v) for k, v in (private.get("shed", {}) or {}).items()}
    seeds = {str(k): int(v) for k, v in (private.get("seeds", {}) or {}).items()}

    day = int(snap.clock.day)
    turns_per_day = max(1, int(snap.clock.turns_per_day))
    remaining_steps = int(snap.clock.remaining_steps)
    days_remaining = remaining_steps // turns_per_day

    opportunities: list[dict[str, Any]] = []
    plant_tiles_count = 0
    care_due_count = 0
    crop_mix_counts: dict[str, int] = {}
    animal_headcount = 0
    unfed_animal_count = 0
    at_risk_animal_count = 0
    structures_total = 0
    empty_structure_type_counts: dict[str, int] = {"COOP": 0, "PASTURE": 0}
    empty_structure_positions: list[tuple[int, int, str]] = []
    plant_count_by_quadrant: dict[str, int] = {}
    empty_crop_zone_by_quadrant: dict[str, list[tuple[int, int]]] = {}

    for y, row in enumerate(tiles):
        if not isinstance(row, list):
            continue
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            quadrant = _quadrant_of(x, y, board_size)
            if tile is None:
                if (x, y) in shed_tiles:
                    continue
                rank = _quadrant_local_rank(x, y, quadrant, board_size)
                if rank < livestock_zone_size:
                    opportunities.append(
                        {
                            "priority": 8,
                            "secondary": 0,
                            "x": x,
                            "y": y,
                            "kind": "BUILD_OPPORTUNITY",
                        }
                    )
                else:
                    empty_crop_zone_by_quadrant.setdefault(quadrant, []).append((x, y))
                continue
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
            if kind == "WEED":
                opportunities.append(
                    {"priority": 5, "secondary": 0, "x": x, "y": y, "kind": "RECOVERY_DIG"}
                )
                continue
            if kind == "PLANT":
                plant_tiles_count += 1
                plant_count_by_quadrant[quadrant] = plant_count_by_quadrant.get(quadrant, 0) + 1
                crop = tile.get("crop")
                crop_mix_counts[crop] = crop_mix_counts.get(crop, 0) + 1
                watered_today = bool(tile.get("watered_today", False))
                consecutive_unwatered = int(tile.get("consecutive_unwatered", 0))
                if not watered_today:
                    opportunities.append(
                        {
                            "priority": 1,
                            "secondary": -consecutive_unwatered,
                            "x": x,
                            "y": y,
                            "kind": "URGENT_WATER",
                        }
                    )
                    if consecutive_unwatered == 1:
                        care_due_count += 1
                planted_day = int(tile.get("planted_day", day))
                age = day - planted_day
                first_yield = int(CROPS.get(crop, {}).get("first_yield_day", 999))
                yield_units = tile.get("yield_units", 0) or 0
                if yield_units > 0 and age >= first_yield:
                    opportunities.append(
                        {"priority": 4, "secondary": 0, "x": x, "y": y, "kind": "HARVEST_READY"}
                    )
                continue
            if kind in ("COOP", "PASTURE"):
                structures_total += 1
                if "animal" in tile:
                    animal_headcount += 1
                    fed_today = bool(tile.get("fed_today", False))
                    cared_today = bool(tile.get("cared_today", False))
                    consecutive_unfed = int(tile.get("consecutive_unfed", 0))
                    if not fed_today:
                        unfed_animal_count += 1
                        opportunities.append(
                            {"priority": 2, "secondary": 0, "x": x, "y": y, "kind": "FEED_NEEDED"}
                        )
                        if consecutive_unfed == 1:
                            # LIV-08: one more missed feed and this animal
                            # escapes at the next EOD.
                            at_risk_animal_count += 1
                    elif not cared_today:
                        opportunities.append(
                            {"priority": 6, "secondary": 0, "x": x, "y": y, "kind": "CARE_NEEDED"}
                        )
                    yield_units = tile.get("yield_units", 0) or 0
                    if yield_units > 0:
                        opportunities.append(
                            {
                                "priority": 4,
                                "secondary": 0,
                                "x": x,
                                "y": y,
                                "kind": "HARVEST_READY",
                            }
                        )
                    if tile.get("fertilizer_available"):
                        opportunities.append(
                            {
                                "priority": 7,
                                "secondary": 0,
                                "x": x,
                                "y": y,
                                "kind": "COLLECT_FERTILIZER_READY",
                            }
                        )
                else:
                    empty_structure_type_counts[kind] = (
                        empty_structure_type_counts.get(kind, 0) + 1
                    )
                    empty_structure_positions.append((x, y, kind))

    # Crop fill / plant opportunities: only in quadrants below fill target,
    # and only when at least one rotation species is actually plantable now
    # (seeds in stock and horizon guard satisfied). Without this feasibility
    # gate, idle workers would keep claiming PLANT_OPPORTUNITY tiles they
    # cannot actually plant, starving the lower-priority BUILD_OPPORTUNITY
    # queue of any worker attention (found and fixed in V1).
    any_species_plantable = any(
        seeds.get(species, 0) > 0
        and days_remaining >= int(CROPS.get(species, {}).get("first_yield_day", 999))
        + cfg.crop_min_days_margin
        for species in cfg.crop_species_rotation
    )
    has_empty_crop_zone_tile = False
    for quadrant, empties in empty_crop_zone_by_quadrant.items():
        total_quadrant_tiles = half * half
        current_plant = plant_count_by_quadrant.get(quadrant, 0)
        current_fill = current_plant / max(1, total_quadrant_tiles)
        if current_fill >= cfg.crop_target_fill_ratio:
            continue
        has_empty_crop_zone_tile = True
        if not any_species_plantable:
            continue
        for (x, y) in empties:
            opportunities.append(
                {"priority": 9, "secondary": 0, "x": x, "y": y, "kind": "PLANT_OPPORTUNITY"}
            )

    # A single PLACE_ANIMAL_NEEDED opportunity per call: nearest empty
    # structure that has a matching species already waiting in the shed.
    if empty_structure_positions:
        for (x, y, struct_kind) in sorted(empty_structure_positions, key=lambda p: (p[1], p[0])):
            candidate_species = None
            for species in cfg.livestock_species_rotation:
                if ANIMALS[species]["structure"] != struct_kind:
                    continue
                if shed.get(species, 0) >= 1:
                    candidate_species = species
                    break
            if candidate_species is not None:
                opportunities.append(
                    {
                        "priority": 3,
                        "secondary": 0,
                        "x": x,
                        "y": y,
                        "kind": "PLACE_ANIMAL_NEEDED",
                        "animal": candidate_species,
                    }
                )
                break

    money = float(farm.get("money", 0.0))
    market_prices = {str(k): float(v) for k, v in (market.get("prices", {}) or {}).items()}

    farmer_pos = farm.get("farmer")
    worker_positions: list[tuple[int, int]] = [
        (int(farmer_pos[0]), int(farmer_pos[1])) if farmer_pos else (half - 1, half - 1)
    ]
    for hand in farm.get("hands", []) or []:
        if isinstance(hand, (list, tuple)) and len(hand) >= 2:
            worker_positions.append((int(hand[0]), int(hand[1])))
        else:
            worker_positions.append((half - 1, half - 1))

    raw_inventories = private.get("inventories", []) or []
    worker_inventories: list[dict[str, int]] = []
    for idx in range(len(worker_positions)):
        inv = raw_inventories[idx] if idx < len(raw_inventories) else {}
        worker_inventories.append(
            {str(k): int(v) for k, v in (inv or {}).items()} if isinstance(inv, dict) else {}
        )

    service_pressure = care_due_count / max(1, plant_tiles_count)
    in_shutdown = days_remaining <= cfg.shutdown_days_remaining
    in_liquidation = days_remaining <= cfg.liquidation_days_remaining

    opportunities.sort(key=lambda o: (o["priority"], o["secondary"], o["y"], o["x"]))

    return _Features(
        board_size=board_size,
        day=day,
        days_remaining=days_remaining,
        worker_positions=worker_positions,
        worker_inventories=worker_inventories,
        shed=shed,
        seeds=seeds,
        money=money,
        market_prices=market_prices,
        unlocked_quadrants=unlocked_quadrants,
        hires_today=int(farm.get("hires_today", 0)),
        opportunities=opportunities,
        plant_tiles_count=plant_tiles_count,
        care_due_count=care_due_count,
        crop_mix_counts=crop_mix_counts,
        animal_headcount=animal_headcount,
        unfed_animal_count=unfed_animal_count,
        at_risk_animal_count=at_risk_animal_count,
        structures_total=structures_total,
        empty_structure_type_counts=empty_structure_type_counts,
        has_empty_crop_zone_tile=has_empty_crop_zone_tile,
        seed_budget=dict(seeds),
        crop_mix_running=dict(crop_mix_counts),
        in_shutdown=in_shutdown,
        in_liquidation=in_liquidation,
        service_pressure=service_pressure,
    )


# ---------------------------------------------------------------------------
# Goal planner helpers (species selection)
# ---------------------------------------------------------------------------


def _choose_plant_species(cfg: ReactiveConfigV2, feat: _Features) -> str | None:
    eligible = []
    for species in cfg.crop_species_rotation:
        if feat.seed_budget.get(species, 0) <= 0:
            continue
        first_yield = int(CROPS.get(species, {}).get("first_yield_day", 999))
        if feat.days_remaining < first_yield + cfg.crop_min_days_margin:
            continue
        eligible.append(species)
    if not eligible:
        return None
    eligible.sort(
        key=lambda s: (
            feat.crop_mix_running.get(s, 0),
            cfg.crop_species_rotation.index(s),
        )
    )
    return eligible[0]


# ---------------------------------------------------------------------------
# Worker dispatch (Section: DISPATCH) — persistent per-worker assignment
# ---------------------------------------------------------------------------


@dataclass
class _Assignment:
    """A worker's current committed job. Persists across calls; revalidated
    every call against the freshly rebuilt opportunity index (Sec. 6.2 of
    the V2 MODEL_SPEC), never against a saved plan."""

    kind: str
    target: tuple[int, int]
    animal: str | None = None
    stalled_steps: int = 0


def _move_toward(pos: tuple[int, int], target: tuple[int, int]) -> list[str]:
    dx = target[0] - pos[0]
    dy = target[1] - pos[1]
    if dx == 0 and dy == 0:
        return ["PASS"]
    if abs(dx) >= abs(dy):
        return ["EAST"] if dx > 0 else ["WEST"]
    return ["SOUTH"] if dy > 0 else ["NORTH"]


def _nearest_shed_tile(pos: tuple[int, int], board_size: int) -> tuple[int, int]:
    candidates = _shed_access_tiles(board_size)
    return min(
        candidates,
        key=lambda t: (abs(t[0] - pos[0]) + abs(t[1] - pos[1]), t[1], t[0]),
    )


def _select_deposit_item(inv: dict[str, int]) -> str | None:
    for item in SELLABLE_PRODUCE:
        if inv.get(item, 0) > 0:
            return item
    if inv.get("WHEAT", 0) > 0:
        return "WHEAT"
    if inv.get("FERTILIZER", 0) > 0:
        return "FERTILIZER"
    for item in sorted(inv):
        if inv.get(item, 0) > 0:
            return item
    return None


def _best_opportunity(
    pos: tuple[int, int],
    opportunities: list[dict[str, Any]],
    claimed: set[tuple[int, int]],
) -> dict[str, Any] | None:
    best = None
    best_key: tuple[Any, ...] | None = None
    for opp in opportunities:
        tile_xy = (opp["x"], opp["y"])
        if tile_xy in claimed:
            continue
        distance = abs(pos[0] - opp["x"]) + abs(pos[1] - opp["y"])
        key = (opp["priority"], opp["secondary"], distance, opp["y"], opp["x"])
        if best_key is None or key < best_key:
            best_key = key
            best = opp
    return best


def _tile_at(snap: Any, pos: tuple[int, int]) -> Any:
    farm = snap.farm
    tiles = farm.get("tiles", []) or []
    x, y = pos
    if not (0 <= y < len(tiles) and 0 <= x < len(tiles[y])):
        return None
    return tiles[y][x]


def _current_tile_needs_water(pos: tuple[int, int], snap: Any) -> bool:
    tile = _tile_at(snap, pos)
    return (
        isinstance(tile, dict)
        and tile.get("kind") == "PLANT"
        and not tile.get("watered_today", False)
    )


def _opportunistic_fertilize(
    pos: tuple[int, int], inv: dict[str, int], snap: Any, cfg: ReactiveConfigV2, day: int
) -> bool:
    if not cfg.fertilize_when_carried:
        return False
    if inv.get("FERTILIZER", 0) < 1:
        return False
    tile = _tile_at(snap, pos)
    if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):
        return False
    return int(tile.get("fertilized_until_day", -1)) < day


def _resolve_feed(
    pos: tuple[int, int],
    inv: dict[str, int],
    target: tuple[int, int],
    feat: _Features,
) -> list[Any]:
    if inv.get("WHEAT", 0) >= 1:
        if pos == target:
            return ["FEED"]
        return _move_toward(pos, target)
    shed_wheat = feat.shed.get("WHEAT", 0)
    if shed_wheat <= 0:
        return ["PASS"]
    nearest_shed = _nearest_shed_tile(pos, feat.board_size)
    if pos == nearest_shed:
        qty = min(shed_wheat, max(1, feat.unfed_animal_count))
        feat.shed["WHEAT"] = shed_wheat - qty
        return ["PICKUP", "WHEAT", int(qty)]
    return _move_toward(pos, nearest_shed)


def _resolve_place_animal(
    pos: tuple[int, int],
    inv: dict[str, int],
    target: tuple[int, int],
    species: str,
    feat: _Features,
) -> list[Any]:
    if inv.get(species, 0) >= 1:
        if pos == target:
            return ["PLACE", species]
        return _move_toward(pos, target)
    if feat.shed.get(species, 0) <= 0:
        return ["PASS"]
    nearest_shed = _nearest_shed_tile(pos, feat.board_size)
    if pos == nearest_shed:
        feat.shed[species] = feat.shed.get(species, 0) - 1
        return ["PICKUP", species, 1]
    return _move_toward(pos, nearest_shed)


def _resolve_plant(
    pos: tuple[int, int], target: tuple[int, int], cfg: ReactiveConfigV2, feat: _Features
) -> list[Any]:
    if pos != target:
        return _move_toward(pos, target)
    species = _choose_plant_species(cfg, feat)
    if species is None:
        return ["PASS"]
    feat.seed_budget[species] = feat.seed_budget.get(species, 0) - 1
    feat.crop_mix_running[species] = feat.crop_mix_running.get(species, 0) + 1
    return ["PLANT", species]


def _resolve_build(pos: tuple[int, int], target: tuple[int, int], feat: _Features) -> list[Any]:
    if pos != target:
        return _move_toward(pos, target)
    coop = feat.empty_structure_type_counts.get("COOP", 0)
    pasture = feat.empty_structure_type_counts.get("PASTURE", 0)
    op = "BUILD_PASTURE" if pasture <= coop else "BUILD_COOP"
    return [op]


_SIMPLE_TILE_COMMAND = {
    "URGENT_WATER": "WATER",
    "HARVEST_READY": "HARVEST",
    "RECOVERY_DIG": "DIG",
    "CARE_NEEDED": "CARE",
    "COLLECT_FERTILIZER_READY": "COLLECT_FERTILIZER",
}


def _resolve_assignment(
    pos: tuple[int, int],
    inv: dict[str, int],
    assignment: _Assignment,
    cfg: ReactiveConfigV2,
    feat: _Features,
) -> list[Any]:
    target = assignment.target
    kind = assignment.kind
    simple = _SIMPLE_TILE_COMMAND.get(kind)
    if simple is not None:
        return [simple] if pos == target else _move_toward(pos, target)
    if kind == "FEED_NEEDED":
        return _resolve_feed(pos, inv, target, feat)
    if kind == "PLACE_ANIMAL_NEEDED":
        return _resolve_place_animal(pos, inv, target, assignment.animal, feat)
    if kind == "PLANT_OPPORTUNITY":
        return _resolve_plant(pos, target, cfg, feat)
    if kind == "BUILD_OPPORTUNITY":
        return _resolve_build(pos, target, feat)
    return ["PASS"]


def _idle_or_deposit(pos: tuple[int, int], inv: dict[str, int], feat: _Features) -> list[Any]:
    if not inv:
        return ["PASS"]
    nearest_shed = _nearest_shed_tile(pos, feat.board_size)
    if pos == nearest_shed:
        item = _select_deposit_item(inv)
        if item is None:
            return ["PASS"]
        return ["PLACE", item, int(inv[item])]
    return _move_toward(pos, nearest_shed)


# ---------------------------------------------------------------------------
# Market order construction (Section: MARKET BUILDER)
# ---------------------------------------------------------------------------


def _expansion_guard(cfg: ReactiveConfigV2, feat: _Features, core_harvest_requests: int) -> bool:
    if len(feat.unlocked_quadrants) >= cfg.target_quadrants:
        return False
    n_extra = max(0, len(feat.unlocked_quadrants) - 1)
    if n_extra >= len(LAND_PRICES):
        return False
    next_cost = LAND_PRICES[n_extra]
    if feat.money < next_cost + cfg.land_purchase_reserve:
        return False
    if feat.days_remaining < cfg.min_days_for_expansion_payback:
        return False
    # Core-established guard (V2 remediation, MODEL_SPEC Sec. 6.4): V1
    # bought land on day 0 with zero harvests completed because
    # service_pressure is trivially 0 when no plant exists yet. Require an
    # actual, non-trivial Q0 before authorizing more territory.
    if feat.plant_tiles_count <= 0:
        return False
    if core_harvest_requests < cfg.core_min_harvest_requests:
        return False
    return feat.service_pressure <= cfg.expansion_service_pressure_ceiling


def _hire_orders(
    cfg: ReactiveConfigV2, feat: _Features, money: float
) -> tuple[list[list[Any]], float]:
    orders: list[list[Any]] = []
    headcount = len(feat.worker_positions)
    backlog = sum(1 for o in feat.opportunities if o["kind"] in SERVICE_BACKLOG_KINDS)
    quadrants = max(1, len(feat.unlocked_quadrants))
    floor_headcount = cfg.min_workers_per_quadrant * quadrants
    load_driven = (
        (backlog + cfg.tasks_per_worker_per_day - 1) // cfg.tasks_per_worker_per_day
        if backlog > 0
        else 0
    )
    target_headcount = min(cfg.max_hands, max(floor_headcount, load_driven))
    hires_today = feat.hires_today
    remaining_money = money
    count = 0
    while (
        count < cfg.hire_batch_limit_per_turn
        and headcount + count < target_headcount
        and headcount + count < cfg.max_hands
    ):
        cost = _hire_cost_estimate(hires_today + count)
        if remaining_money < cfg.hire_reserve + cost:
            break
        orders.append(["HIRE"])
        remaining_money -= cost
        count += 1
    return orders, remaining_money


def _seed_orders(
    cfg: ReactiveConfigV2, feat: _Features, money: float, room_left: int
) -> tuple[list[list[Any]], float]:
    orders: list[list[Any]] = []
    remaining_money = money
    if not feat.has_empty_crop_zone_tile:
        return orders, remaining_money
    for species in cfg.crop_species_rotation:
        if len(orders) >= room_left:
            break
        if feat.seeds.get(species, 0) > 0:
            continue
        first_yield = int(CROPS.get(species, {}).get("first_yield_day", 999))
        if feat.days_remaining < first_yield + cfg.crop_min_days_margin:
            continue
        unit_price = float(CROPS[species]["seed_price"])
        qty = cfg.seed_purchase_batch_size
        cost = unit_price * qty
        if remaining_money - cfg.market_order_min_cash < cost:
            continue
        orders.append(["BUY_SEED", species, int(qty)])
        remaining_money -= cost
    return orders, remaining_money


def _animal_orders(
    cfg: ReactiveConfigV2, feat: _Features, money: float, room_left: int, core_harvest_requests: int
) -> tuple[list[list[Any]], float]:
    orders: list[list[Any]] = []
    remaining_money = money
    # Core-established guard (V2 remediation, same rationale as
    # _expansion_guard, MODEL_SPEC Sec. 6.4): buying animals before Q0 has
    # produced anything diverts scarce early capital and worker attention
    # (PLACE_ANIMAL_NEEDED outranks HARVEST_READY) away from establishing
    # the crop economy that would otherwise fund expansion.
    if feat.plant_tiles_count <= 0 or core_harvest_requests < cfg.core_min_harvest_requests:
        return orders, remaining_money
    # Zero-risk ratchet (V2 remediation, MODEL_SPEC Sec. 6.5): never grow the
    # herd while an already-owned animal is one missed feed away from
    # escaping (LIV-08). This bounds herd growth to demonstrated servicing
    # capacity instead of a pre-estimated one.
    if feat.at_risk_animal_count > cfg.max_at_risk_animals_for_new_purchase:
        return orders, remaining_money
    if feat.structures_total <= 0 or feat.animal_headcount >= feat.structures_total:
        return orders, remaining_money
    # Workforce-relative herd cap: structural capacity (COOP/PASTURE count)
    # is a poor proxy for feeding capacity, since it is cheap ($0) and
    # unrelated to how many workers are actually available to run the daily
    # FEED/CARE logistics. Cap herd growth to what the current headcount
    # could plausibly service instead.
    max_serviceable_herd = max(1, len(feat.worker_positions) // cfg.herd_size_workforce_divisor)
    if feat.animal_headcount >= max_serviceable_herd:
        return orders, remaining_money
    if room_left <= 0:
        return orders, remaining_money
    # At most one purchase per call (herd grows one animal at a time): the
    # zero-risk ratchet above is only re-evaluated between calls, so
    # authorizing several simultaneous purchases here would let a whole
    # burst of new animals land before the next call could reassess
    # at_risk_animal_count against them, defeating the ratchet's purpose.
    for species in cfg.livestock_species_rotation:
        structure = ANIMALS[species]["structure"]
        if feat.empty_structure_type_counts.get(structure, 0) <= 0:
            continue
        if feat.shed.get(species, 0) >= 1:
            continue
        cost = float(ANIMALS[species]["cost"])
        if remaining_money - cfg.market_order_min_cash < cost:
            continue
        orders.append(["BUY_ANIMAL", species, 1])
        remaining_money -= cost
        break
    return orders, remaining_money


def _wheat_buy_order(
    cfg: ReactiveConfigV2, feat: _Features, money: float
) -> tuple[list[Any] | None, float]:
    if feat.animal_headcount <= 0:
        return None, money
    if feat.in_liquidation:
        target_buffer = feat.animal_headcount * max(1, feat.days_remaining)
    else:
        target_buffer = feat.animal_headcount * cfg.feed_security_buffer_per_animal
    current = feat.shed.get("WHEAT", 0)
    deficit = target_buffer - current
    if deficit <= 0:
        return None, money
    price = feat.market_prices.get("WHEAT")
    if price is None or price <= 0 or price > cfg.wheat_buy_price_ceiling:
        return None, money
    qty = min(deficit, cfg.wheat_buy_batch_cap)
    affordable_qty = int(max(0.0, (money - cfg.market_order_min_cash)) / price)
    qty = min(qty, affordable_qty)
    if qty <= 0:
        return None, money
    cost = price * qty
    return ["BUY_PRODUCT", "WHEAT", int(qty)], money - cost


def _sell_orders(cfg: ReactiveConfigV2, feat: _Features, room_left: int) -> list[list[Any]]:
    orders: list[list[Any]] = []
    if feat.in_liquidation:
        wheat_reserve = feat.animal_headcount * max(1, feat.days_remaining)
    else:
        wheat_reserve = feat.animal_headcount * cfg.feed_security_buffer_per_animal
    for item in sorted(feat.shed):
        if item in ANIMALS:
            # Purchased animals wait in the shed to be picked up and placed
            # by a worker (PLACE_ANIMAL_NEEDED); they are not produce.
            continue
        if len(orders) >= room_left:
            break
        qty = feat.shed.get(item, 0)
        if item == "WHEAT":
            qty = max(0, qty - wheat_reserve)
        if qty > 0:
            orders.append(["SELL", item, int(qty)])
    return orders


def _build_market_orders(
    cfg: ReactiveConfigV2, snap: Any, feat: _Features, core_harvest_requests: int
) -> list[list[Any]]:
    configured_limit = int(snap.configuration_snapshot.get("maxMarketOrdersPerTurn", 10))
    batch_limit = max(0, min(configured_limit, cfg.fallback_market_order_batch_limit))
    orders: list[list[Any]] = []
    money = feat.money

    def room() -> int:
        return batch_limit - len(orders)

    if room() > 0:
        orders.extend(_sell_orders(cfg, feat, room()))

    if not feat.in_shutdown and room() > 0:
        hires, money = _hire_orders(cfg, feat, money)
        orders.extend(hires[: room()])

    if not feat.in_shutdown and room() > 0 and _expansion_guard(cfg, feat, core_harvest_requests):
        orders.append(["BUY_LAND"])
        n_extra = max(0, len(feat.unlocked_quadrants) - 1)
        money -= LAND_PRICES[n_extra]

    if not feat.in_shutdown and room() > 0:
        seed_orders, money = _seed_orders(cfg, feat, money, room())
        orders.extend(seed_orders)

    if not feat.in_shutdown and room() > 0:
        animal_orders, money = _animal_orders(cfg, feat, money, room(), core_harvest_requests)
        orders.extend(animal_orders)

    if not feat.in_shutdown and room() > 0:
        wheat_order, money = _wheat_buy_order(cfg, feat, money)
        if wheat_order is not None:
            orders.append(wheat_order)

    return orders[:batch_limit]


# ---------------------------------------------------------------------------
# Controller
# ---------------------------------------------------------------------------


class ClaudeE17ReactiveAgentV2:
    """Reactive controller with persistent, self-invalidating per-worker
    target assignment (see MODEL_SPEC V2 Sections 4 and 6.2)."""

    def __init__(self, config: ReactiveConfigV2, run_context: Any = None) -> None:
        self.config = config
        self.run_context = run_context
        self.policy_version = POLICY_VERSION
        self.technical_errors = 0
        self._telemetry: Counter[str] = Counter()
        self._assignments: dict[str, _Assignment] = {}
        self._core_harvest_requests = 0
        self._last_seen_day: int | None = None

    def __call__(self, observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        try:
            action = self._decide(observation, configuration)
        except Exception:  # noqa: BLE001 - MODEL_SPEC Sec. 8: any technical
            # failure must fall back to a safe PASS, not propagate.
            self.technical_errors += 1
            return deepcopy(SAFE_PASS_ACTION)
        self._record_telemetry(action)
        return action

    def _decide(self, observation: dict[str, Any], configuration: Any) -> dict[str, Any]:
        cfg = self.config
        snap = CodexObservationAdapter.parse(
            observation,
            configuration,
            fallback_turns_per_day=cfg.fallback_turns_per_day,
            fallback_episode_steps=cfg.fallback_episode_steps,
        )

        current_day = int(snap.clock.day)
        if self._last_seen_day is not None and current_day != self._last_seen_day:
            # Hands are physically replaced every EOD (ENGINE_VERIFIED daily
            # contract); a stale hand assignment from yesterday belongs to a
            # different individual today. The farmer's identity persists, so
            # its assignment is not cleared here.
            for key in [k for k in self._assignments if k != "farmer"]:
                self._assignments.pop(key, None)
        self._last_seen_day = current_day

        feat = _extract_features(cfg, snap)

        claimed: set[tuple[int, int]] = set()
        opportunities_index = {(o["kind"], o["x"], o["y"]): o for o in feat.opportunities}
        worker_keys = ["farmer"] + [f"hand:{i}" for i in range(len(feat.worker_positions) - 1)]
        commands: list[list[Any]] = []
        for worker_key, pos, inv in zip(
            worker_keys, feat.worker_positions, feat.worker_inventories
        ):
            commands.append(
                self._decide_worker(
                    worker_key, pos, inv, cfg, feat, snap, claimed, opportunities_index
                )
            )

        self._core_harvest_requests += sum(1 for cmd in commands if cmd and cmd[0] == "HARVEST")

        farmer_cmd = commands[0]
        hands_cmds = commands[1:]
        market_orders = _build_market_orders(cfg, snap, feat, self._core_harvest_requests)

        action = {"farmer": farmer_cmd, "hands": hands_cmds, "market": market_orders}
        self._validate_action(action, len(hands_cmds), snap)
        return action

    def _decide_worker(
        self,
        worker_key: str,
        pos: tuple[int, int],
        inv: dict[str, int],
        cfg: ReactiveConfigV2,
        feat: _Features,
        snap: Any,
        claimed: set[tuple[int, int]],
        opportunities_index: dict[tuple[str, int, int], dict[str, Any]],
    ) -> list[Any]:
        assignment = self._assignments.get(worker_key)
        if assignment is not None:
            key = (assignment.kind, assignment.target[0], assignment.target[1])
            if key not in opportunities_index or assignment.target in claimed:
                assignment = None
                self._assignments.pop(worker_key, None)
            elif opportunities_index[key]["priority"] > CRITICAL_PRIORITY_CEILING:
                # Urgency preemption: stickiness must not let a worker sit on
                # a low-priority job (e.g. PLANT_OPPORTUNITY) while an
                # EOD-loss-risk need (URGENT_WATER/FEED_NEEDED) goes
                # unclaimed because every other worker is likewise
                # committed. Every V1 escape traced back to exactly this:
                # a lone worker mid-journey on a low-priority task while the
                # herd's only animal went unfed for two EODs. Only these two
                # critical categories can preempt; everything else keeps
                # full stickiness against everything else.
                candidate = _best_opportunity(pos, feat.opportunities, claimed)
                if candidate is not None and candidate["priority"] <= CRITICAL_PRIORITY_CEILING:
                    assignment = None

        if assignment is None:
            opp = _best_opportunity(pos, feat.opportunities, claimed)
            if opp is not None:
                assignment = _Assignment(
                    kind=opp["kind"], target=(opp["x"], opp["y"]), animal=opp.get("animal")
                )
                self._assignments[worker_key] = assignment

        if assignment is None:
            command = _idle_or_deposit(pos, inv, feat)
        else:
            claimed.add(assignment.target)
            command = _resolve_assignment(pos, inv, assignment, cfg, feat)
            if command and command[0] == "PASS":
                assignment.stalled_steps += 1
                if assignment.stalled_steps >= cfg.assignment_stall_timeout:
                    # Serviceable again once it resurfaces in a future call's
                    # opportunity list (MODEL_SPEC V2 Sec. 6.2).
                    self._assignments.pop(worker_key, None)
            else:
                assignment.stalled_steps = 0

        op = command[0] if command else "PASS"
        if op in FARMER_MOVES or op == "PASS":
            # Zero-detour opportunistic interrupt: act on the tile the
            # worker is already standing on without abandoning its
            # persistent assignment for next call.
            if _current_tile_needs_water(pos, snap):
                return ["WATER"]
            if _opportunistic_fertilize(pos, inv, snap, cfg, feat.day):
                return ["FERTILIZE"]
        return command

    @staticmethod
    def _validate_action(action: dict[str, Any], active_hands_count: int, snap: Any) -> None:
        farmer = action.get("farmer")
        if not isinstance(farmer, list) or not farmer:
            raise ActionValidationError("farmer command missing or empty")
        hands = action.get("hands")
        if not isinstance(hands, list) or len(hands) != active_hands_count:
            raise ActionValidationError("hands command count mismatch")
        for hand_cmd in hands:
            if not isinstance(hand_cmd, list) or not hand_cmd:
                raise ActionValidationError("malformed hand command")
        market = action.get("market")
        if not isinstance(market, list):
            raise ActionValidationError("market must be a list")
        configured_limit = int(snap.configuration_snapshot.get("maxMarketOrdersPerTurn", 10))
        if len(market) > configured_limit:
            raise ActionValidationError("market batch exceeds configured limit")

    def _record_telemetry(self, action: dict[str, Any]) -> None:
        self._telemetry["farmer:" + str(action["farmer"][0])] += 1
        for hand_cmd in action["hands"]:
            self._telemetry["hand:" + str(hand_cmd[0])] += 1
        for order in action["market"]:
            self._telemetry["market:" + str(order[0])] += 1

    @property
    def telemetry(self) -> dict[str, int]:
        """Passive counters only; never consulted by the decision path."""

        return dict(self._telemetry)


def create_claude_e17_agent_v2(
    run_context: Any = None, config_path: str | Path | None = None
) -> ClaudeE17ReactiveAgentV2:
    """Factory returning a callable ``agent(observation, configuration=None)``."""

    config = ReactiveConfigV2.load(config_path)
    return ClaudeE17ReactiveAgentV2(config=config, run_context=run_context)


def claude_policy_fingerprint(config_path: str | Path | None = None) -> str:
    """SHA-256 over this controller's source and its resolved configuration.

    Distinct from any other agent's routine/action-table fingerprint, and
    from this agent's own V1 fingerprint; there is no action table here to
    fingerprint separately from the source.
    """

    source_bytes = _THIS_FILE.read_bytes()
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    config_bytes = path.read_bytes()
    digest = hashlib.sha256()
    digest.update(source_bytes)
    digest.update(config_bytes)
    return digest.hexdigest().upper()


__all__ = [
    "DEFAULT_CONFIG_PATH",
    "POLICY_VERSION",
    "SAFE_PASS_ACTION",
    "ActionValidationError",
    "ClaudeE17ReactiveAgentV2",
    "ReactiveConfigV2",
    "claude_policy_fingerprint",
    "create_claude_e17_agent_v2",
]
