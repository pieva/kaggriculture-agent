"""Claude E18.3 lifecycle-and-safety controller — V3.

Five explicit layers, unchanged in kind from V1/V2, per
``docs/model_specs/claude/e18/prompts/E18_CLAUDE_OPPONENT_REACTIVE_V1_BUILD_PROMPT_IT.md``
and this version's scope in
``docs/model_specs/claude/e18/prompts/E18_CLAUDE_LIFECYCLE_SAFETY_V3_BUILD_PROMPT_IT.md``:

1. ``PUBLIC_OPPONENT_SNAPSHOT`` -- a single photograph of the opponent's
   public farm (unlocked quadrants, hands, crop tiles, animals, pastures,
   weed), taken once in the declared window D4-D8.
2. ``REGIME_CLASSIFIER`` -- turns that snapshot into a named regime with a
   serializable numeric reason (a pressure score against a threshold).
3. ``STICKY_POLICY_SELECTOR`` -- locks the regime for the rest of the
   episode (exactly one decision per run) and exposes it as
   ``self._regime``.
4. ``CAPACITY_AND_LIFECYCLE_CONTROLLER`` -- per-tile crop lifecycle state
   (``KEEP``/``HARVEST``/``DIG``/``REPLANT``), workforce sizing and a
   livestock ledger gated on demonstrated, not assumed, feeding capacity.
5. ``ACTION_ARBITER`` -- the same persistent, priority-ordered worker
   dispatch this agent family has used since V1-V3, extended with the new
   opportunity kinds layers 1-4 introduce and a recorded reason string per
   command.

Provenance
----------
The only shared module imported from outside this namespace is
``agricola.core.observation_contract`` (policy-neutral parsing, explicitly
authorized for reuse). Numeric environment constants (crop seed prices,
first-yield days, animal purchase costs and structures, land order and
prices, the ``HIRE`` Fibonacci cost formula, shed-access tile geometry) are
public ``ENGINE_VERIFIED`` facts, carried forward unchanged from this
agent's own E17 lineage (``e17_reactive_3q*.py``) -- the project's own
convention for versions of the *same* agent, not another modeler's work.
Nothing here imports, reads or copies from ``agricola.strategy.codex`` or
``agricola.strategy.copilot``, and there is no action table indexed by
step. The opponent snapshot reads only ``observation["farms"][opponent_seat]``
(public per-farm state already returned by the engine to every player, the
same category of evidence the E18 tournament runner and Codex's own
opponent-reactive candidate use), never ``private`` fields, which the
observation contract only ever populates for the observing player itself.

Origin of this version's design
--------------------------------
``experiments/e18/reports/common/E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1_REPORT_IT.md``
found this agent's own V3 (the only Claude candidate in that tournament)
produced 28 distinct action streams as an emergent side-effect of shared
game state, with no explicit selector, snapshot, sticky decision or
regime-transition telemetry, plus 19 verified livestock losses and no
crop-lifecycle policy at all.
``experiments/e18/reports/common/E18_EPISODE_105080066_CROP_LIFECYCLE_FORENSICS_IT.md``
traced a +41.5% harvested-unit gap in a live Top-3 replay to exactly one
mechanism absent from every prior Claude version: proactively rotating a
perennial (Strawberry/Tomato) to Wheat once it is close to expiry instead
of leaving it to expire or starve into WEED, plus waiting for a fuller
Wheat yield instead of harvesting at the first unit. This version's crop
lifecycle layer targets exactly that mechanism; the regime layer targets
the missing explicit selector.

What changed vs. V2 -- two verified assignment-layer bugs, not a redesign
--------------------------------------------------------------------------
``experiments/e18/reports/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1_REPORT_IT.md``
found V2 economically strong (27-1-0, mean 14,236.36 across 28 matches vs
Copilot E18.2 and Antigravity E18.1) but still failing SAFETY:
``verified_livestock_losses = 24`` of 28 matches. This is *worse* than V1's
31/42 despite V2's proactive wheat-buffer fix, which the V2 report itself
flagged as unresolved ("servibilità continuativa, non solo stock
iniziale") and named as the required next audit target -- not a blind
re-tuning of the same buffer thresholds.

The single worst match (seed `180903002`, seat 0 vs Copilot E18.2, 4
verified losses) was traced turn-by-turn before writing any fix. Two
distinct, previously-invisible bugs were found in the ``ACTION_ARBITER``
layer itself, both present since V1 and untouched by V1->V2:

10. **Worker "identity" was a raw list index, not a stable identity.**
    ``worker_keys = ["farmer"] + [f"hand:{i}" for i in range(...)]`` was
    rebuilt from ``observation["farms"][seat]["hands"]`` every call, and
    that list's *order* is not stable across turns -- newly hired hands
    can be inserted anywhere, not only appended. The trace shows the same
    persistent ``FEED_NEEDED`` assignment silently jumping across six
    different ``hand:N`` keys in ten consecutive steps, each one starting
    the walk to the animal from a different worker's actual position --
    it never converges, because "the worker with this assignment" was
    never the same physical worker two turns running. This alone explains
    why the emergency queue (V2 remediation item 2) never actually
    resolves most emergencies: it *reaches* a worker, but that worker's
    identity resets before it can travel there. ``_track_worker_identities``
    below replaces the positional key with a persistent id assigned by
    greedy nearest-previous-position matching (a hand moves at most one
    tile per turn, so distance <=1 to a still-unclaimed previous identity
    is a safe match; anything unmatched is a newly hired hand). Farmer
    identity was already stable (a distinguished, always-index-0 field,
    never part of the reordered ``hands`` list) and is unchanged.
11. **The stall-timeout escape hatch never fired for a stuck ``PICKUP``.**
    ``assignment.stalled_steps`` only incremented on a literal ``PASS``;
    a worker re-issuing ``["PICKUP", "WHEAT", 1]`` every single turn
    because the shed genuinely has zero stock that moment (traced: shed
    WHEAT stayed at exactly ``0`` for 24 consecutive turns while three
    ``FEED_NEEDED`` assignments competed for the same restock) was never
    reassigned or timed out -- it simply burned the entire remainder of
    the day with zero feeding progress. ``_resolve_feed`` and
    ``_resolve_place_animal`` only ever emit ``PICKUP`` when their target
    resource is still absent from inventory, so a single successful
    pickup always transitions to a ``MOVE``/terminal command on the very
    next call (only one unit is ever needed to proceed); treating a
    repeated ``PICKUP`` exactly like a repeated ``PASS`` for stall
    counting therefore only catches genuinely stuck assignments, never a
    legitimately progressing one.

Both fixes live entirely in the ``ACTION_ARBITER`` layer (worker identity
tracking and stall detection); nothing about *what* gets prioritised,
*when* an animal counts as at-risk, or *how* crop lifecycle/rotation is
decided has changed from V2. Layers 1-4 (opponent snapshot, classifier,
sticky selector, crop KEEP/HARVEST/ROTATION_DIG lifecycle, proactive wheat
buffer, crop-surface cap, per-animal ledger and emergency queue) are
unchanged byte-for-byte from V2 -- no third regime, no new snapshot
fields, no threshold re-tuning.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "CLAUDE-E18.3-LIFECYCLE-SAFETY-V1"

_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parents[4]
DEFAULT_CONFIG_PATH = (
    _REPO_ROOT
    / "docs" / "model_specs" / "claude" / "e18" / "configs"
    / "CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.json"
)

SAFE_PASS_ACTION: dict[str, Any] = {"farmer": ["PASS"], "hands": [], "market": []}

CORE_QUADRANT = "NW"


class ActionValidationError(Exception):
    """Raised internally when a constructed action violates the shared
    interface contract; always caught and converted to a safe PASS."""


# ---------------------------------------------------------------------------
# Public environment facts (ENGINE_VERIFIED), carried forward from this
# agent's own E17 lineage.
# ---------------------------------------------------------------------------

CROPS: dict[str, dict[str, Any]] = {
    "WHEAT": {"seed_price": 10, "first_yield_day": 2, "max_yield_day": 4, "max_yield": 6, "ongoing": False},
    "CARROT": {"seed_price": 20, "first_yield_day": 2, "max_yield_day": 3, "max_yield": 4, "ongoing": False},
    "TOMATO": {"seed_price": 50, "first_yield_day": 8, "max_yield_day": 8, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"seed_price": 100, "first_yield_day": 10, "max_yield_day": 10, "max_yield": 4, "ongoing": True},
    "MELON": {"seed_price": 80, "first_yield_day": 10, "max_yield_day": 12, "max_yield": 6, "ongoing": False},
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
CANONICAL_QUADRANT_ORDER = [CORE_QUADRANT, *LAND_ORDER]

FARMER_MOVES = {
    "NORTH": (0, -1),
    "SOUTH": (0, 1),
    "EAST": (1, 0),
    "WEST": (-1, 0),
}

# Opportunity kinds at or below this priority number risk an irreversible
# EOD loss (WEED conversion, animal starvation) if left unclaimed for
# another cycle; only these may preempt an existing persistent assignment
# or cross a regime's home-quadrant preference (this version does not use
# quadrant clustering at all -- see module docstring -- but the ceiling is
# kept as the single shared "must never wait" concept).
CRITICAL_PRIORITY_CEILING = 2

SERVICE_BACKLOG_KINDS = frozenset(
    {
        "URGENT_WATER",
        "FEED_NEEDED",
        "HARVEST_READY",
        "RECOVERY_DIG",
        "ROTATION_DIG",
        "CARE_NEEDED",
        "PLANT_OPPORTUNITY",
    }
)


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


def _payload_hash(payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RegimeProfile:
    """One named operating regime: everything the lower layers read that
    differs by regime lives here, so a regime change is a single config
    swap, never a scattered set of if/else branches."""

    name: str
    max_hands: int
    min_workers_per_quadrant: int
    crop_species_rotation: tuple[str, ...]
    crop_species_weights: dict[str, float]
    livestock_structures_target_per_quadrant: int
    max_quadrants_for_livestock: int


@dataclass(frozen=True)
class ReactiveConfigE18V3:
    policy_id: str
    target_quadrants: int
    fallback_turns_per_day: int
    fallback_episode_steps: int
    fallback_market_order_batch_limit: int
    land_purchase_reserve: float
    hire_reserve: float
    market_order_min_cash: float
    hire_batch_limit_per_turn: int
    tasks_per_worker_per_day: int
    assignment_stall_timeout: int
    prefer_same_quadrant: bool
    min_days_for_expansion_payback: int
    expansion_service_pressure_ceiling: float
    core_min_harvest_requests: int
    core_min_fill_ratio: float
    crop_target_fill_ratio: float
    crop_min_days_margin: int
    seed_purchase_batch_size: int
    fertilize_when_carried: bool
    max_serviceable_crop_tiles_per_worker: float
    harvest_yield_ratio: float
    rotation_lookahead_steps: int
    rotation_min_days_remaining_for_wheat_cycle: int
    rotation_episode_late_days_remaining: int
    livestock_species_rotation: tuple[str, ...]
    feed_security_buffer_per_animal: int
    wheat_buy_price_ceiling: float
    wheat_buy_batch_cap: int
    max_at_risk_animals_for_new_purchase: int
    animal_purchase_reserve: float
    herd_per_worker_ratio: float
    max_animal_placements_per_call: int
    shutdown_days_remaining: int
    liquidation_days_remaining: int
    snapshot_window_start_day: int
    snapshot_window_end_day: int
    regime_pressure_threshold: float
    regime_low: RegimeProfile
    regime_high: RegimeProfile
    source_payload: dict[str, Any] = field(repr=False)

    @staticmethod
    def load(config_path: str | Path | None = None) -> ReactiveConfigE18V3:
        path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
        payload = json.loads(path.read_text(encoding="utf-8"))
        fallback = payload.get("fallback", {})
        cash = payload.get("cash_reserve", {})
        dispatch = payload.get("dispatch", {})
        expansion = payload.get("expansion", {})
        crop = payload.get("crop", {})
        lifecycle = payload.get("lifecycle", {})
        livestock = payload.get("livestock", {})
        endgame = payload.get("endgame", {})
        snapshot = payload.get("opponent_snapshot", {})

        def _profile(raw: dict[str, Any]) -> RegimeProfile:
            return RegimeProfile(
                name=str(raw["name"]),
                max_hands=int(raw["max_hands"]),
                min_workers_per_quadrant=int(raw["min_workers_per_quadrant"]),
                crop_species_rotation=tuple(raw["crop_species_rotation"]),
                crop_species_weights={
                    str(k): float(v) for k, v in raw["crop_species_weights"].items()
                },
                livestock_structures_target_per_quadrant=int(
                    raw["livestock_structures_target_per_quadrant"]
                ),
                max_quadrants_for_livestock=int(raw["max_quadrants_for_livestock"]),
            )

        regimes = payload.get("regimes", {})
        return ReactiveConfigE18V3(
            policy_id=str(payload.get("policy_id", POLICY_VERSION)),
            target_quadrants=int(payload.get("target_quadrants", 3)),
            fallback_turns_per_day=int(fallback.get("turns_per_day", 24)),
            fallback_episode_steps=int(fallback.get("episode_steps", 720)),
            fallback_market_order_batch_limit=int(
                fallback.get("market_order_batch_limit", 10)
            ),
            land_purchase_reserve=float(cash.get("land_purchase_reserve", 300.0)),
            hire_reserve=float(cash.get("hire_reserve", 150.0)),
            market_order_min_cash=float(cash.get("market_order_min_cash", 30.0)),
            hire_batch_limit_per_turn=int(dispatch.get("hire_batch_limit_per_turn", 2)),
            tasks_per_worker_per_day=int(dispatch.get("tasks_per_worker_per_day", 6)),
            assignment_stall_timeout=int(dispatch.get("assignment_stall_timeout", 3)),
            prefer_same_quadrant=bool(dispatch.get("prefer_same_quadrant", True)),
            min_days_for_expansion_payback=int(
                expansion.get("min_days_for_expansion_payback", 4)
            ),
            expansion_service_pressure_ceiling=float(
                expansion.get("expansion_service_pressure_ceiling", 0.34)
            ),
            core_min_harvest_requests=int(expansion.get("core_min_harvest_requests", 4)),
            core_min_fill_ratio=float(expansion.get("core_min_fill_ratio", 0.4)),
            crop_target_fill_ratio=float(crop.get("target_fill_ratio", 0.55)),
            crop_min_days_margin=int(crop.get("min_days_margin_for_planting", 1)),
            seed_purchase_batch_size=int(crop.get("seed_purchase_batch_size", 5)),
            fertilize_when_carried=bool(crop.get("fertilize_when_carried", True)),
            max_serviceable_crop_tiles_per_worker=float(
                crop.get("max_serviceable_crop_tiles_per_worker", 3.0)
            ),
            harvest_yield_ratio=float(lifecycle.get("harvest_yield_ratio", 0.6)),
            rotation_lookahead_steps=int(lifecycle.get("rotation_lookahead_steps", 48)),
            rotation_min_days_remaining_for_wheat_cycle=int(
                lifecycle.get("rotation_min_days_remaining_for_wheat_cycle", 4)
            ),
            rotation_episode_late_days_remaining=int(
                lifecycle.get("rotation_episode_late_days_remaining", 10)
            ),
            livestock_species_rotation=tuple(
                livestock.get("species_rotation", ["SHEEP", "COW", "GOOSE"])
            ),
            feed_security_buffer_per_animal=int(
                livestock.get("feed_security_buffer_per_animal", 3)
            ),
            wheat_buy_price_ceiling=float(livestock.get("wheat_buy_price_ceiling", 80.0)),
            wheat_buy_batch_cap=int(livestock.get("wheat_buy_batch_cap", 10)),
            max_at_risk_animals_for_new_purchase=int(
                livestock.get("max_at_risk_animals_for_new_purchase", 0)
            ),
            animal_purchase_reserve=float(livestock.get("animal_purchase_reserve", 300.0)),
            herd_per_worker_ratio=float(livestock.get("herd_per_worker_ratio", 0.5)),
            max_animal_placements_per_call=int(
                livestock.get("max_animal_placements_per_call", 2)
            ),
            shutdown_days_remaining=int(endgame.get("shutdown_days_remaining", 5)),
            liquidation_days_remaining=int(endgame.get("liquidation_days_remaining", 3)),
            snapshot_window_start_day=int(snapshot.get("window_start_day", 4)),
            snapshot_window_end_day=int(snapshot.get("window_end_day", 8)),
            regime_pressure_threshold=float(snapshot.get("pressure_threshold", 26.0)),
            regime_low=_profile(regimes["LOW_PRESSURE_BALANCED"]),
            regime_high=_profile(regimes["HIGH_PRESSURE_WHEAT_TEMPO"]),
            source_payload=payload,
        )


# ---------------------------------------------------------------------------
# Layer 1: PUBLIC_OPPONENT_SNAPSHOT
# ---------------------------------------------------------------------------


def _extract_opponent_snapshot(observation: dict[str, Any], my_seat: int) -> dict[str, Any] | None:
    """Photograph the opponent's currently-visible public farm only:
    unlocked quadrants, hands, crop tiles, weed tiles, animals, pastures.
    Never reads ``private`` (that key only ever holds the observing
    player's own shed/seeds/inventories, per the observation contract) and
    never reads the opponent's name, rating, replay ID or seed."""

    farms = observation.get("farms") or []
    opponent_seat = 1 - my_seat
    if opponent_seat >= len(farms) or opponent_seat < 0:
        return None
    opp_farm = farms[opponent_seat]
    if not isinstance(opp_farm, dict):
        return None
    tiles = opp_farm.get("tiles", []) or []
    crop_tiles = 0
    weed_tiles = 0
    animal_count = 0
    pasture_count = 0
    for row in tiles:
        if not isinstance(row, list):
            continue
        for tile in row:
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
            if kind == "PLANT":
                crop_tiles += 1
            elif kind == "WEED":
                weed_tiles += 1
            elif kind in ("PASTURE", "COOP"):
                pasture_count += 1
                if "animal" in tile:
                    animal_count += 1
    return {
        "unlocked_quadrants": len(opp_farm.get("unlocked_quadrants", []) or []),
        "hands": len(opp_farm.get("hands", []) or []),
        "crop_tiles": crop_tiles,
        "weed_tiles": weed_tiles,
        "animal_count": animal_count,
        "pasture_count": pasture_count,
    }


# ---------------------------------------------------------------------------
# Layer 2: REGIME_CLASSIFIER
# ---------------------------------------------------------------------------


def _classify_regime(
    cfg: ReactiveConfigE18V3, snapshot: dict[str, Any]
) -> tuple[str, float]:
    """A single, serializable numeric score against a preregistered
    threshold. Never reads name/rating/seed/replay ID/private inventory or
    any cross-episode memory -- only the fields `_extract_opponent_snapshot`
    put in `snapshot`."""

    pressure = (
        float(snapshot["crop_tiles"])
        + float(snapshot["animal_count"]) * 3.0
        + float(snapshot["hands"]) * 2.0
        + float(snapshot["pasture_count"])
    )
    regime = (
        cfg.regime_high.name if pressure >= cfg.regime_pressure_threshold else cfg.regime_low.name
    )
    return regime, pressure


# ---------------------------------------------------------------------------
# Feature extraction (state snapshot for this call)
# ---------------------------------------------------------------------------


@dataclass
class _Features:
    board_size: int
    day: int
    days_remaining: int
    current_step: int
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
    core_quadrant_fill_ratio: float
    seed_budget: dict[str, int]
    crop_mix_running: dict[str, int]
    in_shutdown: bool
    in_liquidation: bool
    service_pressure: float
    rotation_dig_count: int
    harvest_deferred_count: int
    animals_at_risk: bool
    serviceable_crop_capacity: int


def _plant_lifecycle_opportunity(
    cfg: ReactiveConfigE18V3,
    profile: RegimeProfile,
    tile: dict[str, Any],
    x: int,
    y: int,
    quadrant: str,
    day: int,
    current_step: int,
    days_remaining: int,
) -> tuple[dict[str, Any] | None, bool, bool]:
    """Layer 4 (crop half): decide KEEP / HARVEST / DIG for one live PLANT
    tile. Returns (opportunity_or_none, is_rotation_dig, is_deferred_harvest).

    Engine ground truth (``kaggle_environments/envs/kaggriculture``, the
    public game rules, not another agent's strategy) matters here:

    - For an ``ongoing`` (perennial) crop, ``max_lifespan_step`` is ``-1``
      -- no real deadline yet -- until it enters its *final* scheduled
      production cycle, at which point the engine sets a real value. A
      negative/absent value must therefore never be read as "already
      expired": DIG only fires once the engine has actually set a real
      deadline (no more production coming) or, independently, once the
      episode itself is late enough that a slow perennial's remaining
      interval-based cycles are worth less than a guaranteed-completable
      Wheat cycle -- the exact mechanism
      E18_EPISODE_105080066_CROP_LIFECYCLE_FORENSICS_IT.md traces the
      largest live gap to.
    - For a non-``ongoing`` crop (Wheat, Carrot, Melon), ``yield_units``
      only grows via the ``WATER`` action, and only within
      ``[max_yield_day/2 (rounded up), max_yield_day]`` days of age; the
      tile then expires one day past ``max_yield_day``. HARVEST is
      deferred up to ``harvest_yield_ratio`` of the crop's ``max_yield``,
      but must never be deferred past the crop's own accumulation window
      closing (``age > max_yield_day``) -- a step-based safety margin
      tuned for a multi-week perennial would swallow Wheat's ~5-day whole
      lifecycle if reused here unscaled.
    """

    crop = tile.get("crop")
    crop_facts = CROPS.get(crop, {})
    ongoing = bool(crop_facts.get("ongoing", False))
    max_yield = int(crop_facts.get("max_yield", 1) or 1)
    max_yield_day = int(crop_facts.get("max_yield_day", 999))
    planted_day = int(tile.get("planted_day", day))
    age = day - planted_day
    yield_units = int(tile.get("yield_units", 0) or 0)
    max_lifespan_step = tile.get("max_lifespan_step")
    has_real_deadline = isinstance(max_lifespan_step, (int, float)) and max_lifespan_step >= 0
    steps_to_expiry = int(max_lifespan_step) - current_step if has_real_deadline else None
    near_real_deadline = (
        steps_to_expiry is not None and steps_to_expiry <= cfg.rotation_lookahead_steps
    )
    enough_days_for_wheat_cycle = (
        days_remaining >= cfg.rotation_min_days_remaining_for_wheat_cycle
    )
    episode_running_late = days_remaining <= cfg.rotation_episode_late_days_remaining

    if ongoing:
        if yield_units <= 0:
            should_rotate = (
                near_real_deadline or episode_running_late
            ) and enough_days_for_wheat_cycle
            if should_rotate:
                return (
                    {
                        "priority": 5,
                        "secondary": 0,
                        "x": x,
                        "y": y,
                        "kind": "ROTATION_DIG",
                        "quadrant": quadrant,
                    },
                    True,
                    False,
                )
            # Still producing (or not yet worth abandoning): KEEP.
            return None, False, True
        must_harvest_now = near_real_deadline or days_remaining <= cfg.liquidation_days_remaining
    else:
        if yield_units <= 0:
            return None, False, False
        must_harvest_now = age > max_yield_day or days_remaining <= cfg.liquidation_days_remaining

    target_units = max(1, round(max_yield * cfg.harvest_yield_ratio))
    if must_harvest_now or yield_units >= target_units:
        return (
            {
                "priority": 4,
                "secondary": 0,
                "x": x,
                "y": y,
                "kind": "HARVEST_READY",
                "quadrant": quadrant,
            },
            False,
            False,
        )
    # KEEP: below the yield target and not at risk -- no opportunity
    # emitted, the tile is deliberately left growing.
    return None, False, True


def _extract_features(
    cfg: ReactiveConfigE18V3, profile: RegimeProfile, snap: Any
) -> _Features:
    farm = snap.farm
    private = snap.private
    market = snap.market
    board_size = int(snap.configuration_snapshot.get("boardSize", 10))
    half = board_size // 2
    core_livestock_zone_size = profile.livestock_structures_target_per_quadrant
    allowed_livestock_quadrants = set(
        CANONICAL_QUADRANT_ORDER[: profile.max_quadrants_for_livestock]
    )
    shed_tiles = set(_shed_access_tiles(board_size))

    tiles = farm.get("tiles", []) or []
    unlocked_quadrants = list(farm.get("unlocked_quadrants", []) or [])
    shed = {str(k): int(v) for k, v in (private.get("shed", {}) or {}).items()}
    seeds = {str(k): int(v) for k, v in (private.get("seeds", {}) or {}).items()}

    day = int(snap.clock.day)
    current_step = int(snap.clock.step)
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
    rotation_dig_count = 0
    harvest_deferred_count = 0

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
                if rank < core_livestock_zone_size and quadrant in allowed_livestock_quadrants:
                    opportunities.append(
                        {
                            "priority": 9,
                            "secondary": 0,
                            "x": x,
                            "y": y,
                            "kind": "BUILD_OPPORTUNITY",
                            "quadrant": quadrant,
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
                    {
                        "priority": 6,
                        "secondary": 0,
                        "x": x,
                        "y": y,
                        "kind": "RECOVERY_DIG",
                        "quadrant": quadrant,
                    }
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
                            "quadrant": quadrant,
                        }
                    )
                    if consecutive_unwatered == 1:
                        care_due_count += 1
                lifecycle_opp, is_rotation, is_deferred = _plant_lifecycle_opportunity(
                    cfg, profile, tile, x, y, quadrant, day, current_step, days_remaining
                )
                if lifecycle_opp is not None:
                    opportunities.append(lifecycle_opp)
                if is_rotation:
                    rotation_dig_count += 1
                if is_deferred:
                    harvest_deferred_count += 1
                continue
            if kind in ("COOP", "PASTURE"):
                structures_total += 1
                if "animal" in tile:
                    animal_headcount += 1
                    fed_today = bool(tile.get("fed_today", False))
                    cared_today = bool(tile.get("cared_today", False))
                    consecutive_unfed = int(tile.get("consecutive_unfed", 0))
                    if not fed_today:
                        opportunities.append(
                            {
                                "priority": 2,
                                "secondary": 0,
                                "x": x,
                                "y": y,
                                "kind": "FEED_NEEDED",
                                "quadrant": quadrant,
                            }
                        )
                        unfed_animal_count += 1
                        if consecutive_unfed >= 1:
                            at_risk_animal_count += 1
                    elif not cared_today:
                        opportunities.append(
                            {
                                "priority": 7,
                                "secondary": 0,
                                "x": x,
                                "y": y,
                                "kind": "CARE_NEEDED",
                                "quadrant": quadrant,
                            }
                        )
                    if tile.get("fertilizer_available"):
                        opportunities.append(
                            {
                                "priority": 8,
                                "secondary": 0,
                                "x": x,
                                "y": y,
                                "kind": "COLLECT_FERTILIZER_READY",
                                "quadrant": quadrant,
                            }
                        )
                else:
                    empty_structure_type_counts[kind] = (
                        empty_structure_type_counts.get(kind, 0) + 1
                    )
                    empty_structure_positions.append((x, y, kind))

    any_species_plantable = any(
        seeds.get(species, 0) > 0
        and days_remaining >= int(CROPS.get(species, {}).get("first_yield_day", 999))
        + cfg.crop_min_days_margin
        for species in profile.crop_species_rotation
    )
    # V2 remediation (MODEL_SPEC V2 Sec. "crop surface cap"): new planting is
    # capped at demonstrated servicing capacity -- `max_serviceable_crop_tiles_per_worker`
    # tiles per currently-hired worker (farmer + hands) -- instead of a flat
    # per-quadrant fill ratio alone. V1 planted up to 38 concurrent tiles
    # with 10-11 workers and could not water/harvest them fast enough
    # (traced audit, MODEL_SPEC V2 Sec. 1): MOVE outnumbered every
    # productive action combined roughly 3:1. This does not change the
    # per-quadrant fill *target* (`crop_target_fill_ratio`), only how many
    # new PLANT_OPPORTUNITY tiles are offered per call once that capacity is
    # already spoken for by tiles under service.
    worker_count = 1 + len(farm.get("hands", []) or [])
    serviceable_crop_capacity = int(worker_count * cfg.max_serviceable_crop_tiles_per_worker)
    plantable_room = max(0, serviceable_crop_capacity - plant_tiles_count)
    has_empty_crop_zone_tile = False
    total_quadrant_tiles = half * half
    for quadrant, empties in empty_crop_zone_by_quadrant.items():
        current_plant = plant_count_by_quadrant.get(quadrant, 0)
        current_fill = current_plant / max(1, total_quadrant_tiles)
        if current_fill >= cfg.crop_target_fill_ratio:
            continue
        has_empty_crop_zone_tile = True
        if not any_species_plantable or plantable_room <= 0:
            continue
        for (x, y) in empties:
            if plantable_room <= 0:
                break
            opportunities.append(
                {
                    "priority": 10,
                    "secondary": 0,
                    "x": x,
                    "y": y,
                    "kind": "PLANT_OPPORTUNITY",
                    "quadrant": quadrant,
                }
            )
            plantable_room -= 1

    if empty_structure_positions:
        placements_offered = 0
        for (x, y, struct_kind) in sorted(empty_structure_positions, key=lambda p: (p[1], p[0])):
            if placements_offered >= cfg.max_animal_placements_per_call:
                break
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
                        "quadrant": _quadrant_of(x, y, board_size),
                    }
                )
                placements_offered += 1

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

    core_crop_zone_size = max(1, total_quadrant_tiles - core_livestock_zone_size - 1)
    core_quadrant_fill_ratio = (
        plant_count_by_quadrant.get(CORE_QUADRANT, 0) / core_crop_zone_size
    )

    opportunities.sort(key=lambda o: (o["priority"], o["secondary"], o["y"], o["x"]))

    return _Features(
        board_size=board_size,
        day=day,
        days_remaining=days_remaining,
        current_step=current_step,
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
        core_quadrant_fill_ratio=core_quadrant_fill_ratio,
        seed_budget=dict(seeds),
        crop_mix_running=dict(crop_mix_counts),
        in_shutdown=in_shutdown,
        in_liquidation=in_liquidation,
        service_pressure=service_pressure,
        rotation_dig_count=rotation_dig_count,
        harvest_deferred_count=harvest_deferred_count,
        animals_at_risk=unfed_animal_count > 0,
        serviceable_crop_capacity=serviceable_crop_capacity,
    )


def _core_established(
    cfg: ReactiveConfigE18V3, feat: _Features, core_harvest_requests: int
) -> bool:
    return (
        feat.plant_tiles_count > 0
        and core_harvest_requests >= cfg.core_min_harvest_requests
        and feat.core_quadrant_fill_ratio >= cfg.core_min_fill_ratio
    )


# ---------------------------------------------------------------------------
# Layer 4 (crop half continued): weighted species selection
# ---------------------------------------------------------------------------


def _choose_plant_species(
    cfg: ReactiveConfigE18V3, profile: RegimeProfile, feat: _Features
) -> str | None:
    """Weighted round-robin: pick the eligible species whose planted share
    of the running mix is furthest *below* its regime target weight,
    instead of V1-V3's plain least-planted-count rotation. This is what
    lets a regime's `crop_species_weights` (e.g. Wheat weighted far above
    Strawberry in HIGH_PRESSURE_WHEAT_TEMPO) actually bias new plantings,
    including tiles freshly emptied by a ROTATION_DIG."""

    eligible = []
    for species in profile.crop_species_rotation:
        if feat.seed_budget.get(species, 0) <= 0:
            continue
        first_yield = int(CROPS.get(species, {}).get("first_yield_day", 999))
        if feat.days_remaining < first_yield + cfg.crop_min_days_margin:
            continue
        eligible.append(species)
    if not eligible:
        return None
    total_planted = sum(feat.crop_mix_running.get(s, 0) for s in profile.crop_species_rotation)
    total_planted = max(1, total_planted)

    def _deficit(species: str) -> float:
        target_weight = profile.crop_species_weights.get(species, 0.0)
        current_share = feat.crop_mix_running.get(species, 0) / total_planted
        return target_weight - current_share

    eligible.sort(key=lambda s: (-_deficit(s), profile.crop_species_rotation.index(s)))
    return eligible[0]


# ---------------------------------------------------------------------------
# Layer 5: ACTION_ARBITER -- worker dispatch
# ---------------------------------------------------------------------------


@dataclass
class _Assignment:
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
    board_size: int,
    prefer_same_quadrant: bool,
) -> dict[str, Any] | None:
    worker_quadrant = _quadrant_of(pos[0], pos[1], board_size) if prefer_same_quadrant else None
    best = None
    best_key: tuple[Any, ...] | None = None
    for opp in opportunities:
        tile_xy = (opp["x"], opp["y"])
        if tile_xy in claimed:
            continue
        distance = abs(pos[0] - opp["x"]) + abs(pos[1] - opp["y"])
        cross_quadrant_penalty = (
            0 if worker_quadrant is None or opp.get("quadrant") == worker_quadrant else 1
        )
        key = (opp["priority"], opp["secondary"], cross_quadrant_penalty, distance, opp["y"], opp["x"])
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
    pos: tuple[int, int], inv: dict[str, int], snap: Any, cfg: ReactiveConfigE18V3, day: int
) -> bool:
    if not cfg.fertilize_when_carried or inv.get("FERTILIZER", 0) <= 0:
        return False
    tile = _tile_at(snap, pos)
    if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
        return False
    fertilized_until_day = int(tile.get("fertilized_until_day", -1))
    return fertilized_until_day < day


def _resolve_feed(
    pos: tuple[int, int], inv: dict[str, int], target: tuple[int, int], feat: _Features
) -> list[Any]:
    if inv.get("WHEAT", 0) > 0:
        if pos != target:
            return _move_toward(pos, target)
        return ["FEED"]
    nearest_shed = _nearest_shed_tile(pos, feat.board_size)
    if pos != nearest_shed:
        return _move_toward(pos, nearest_shed)
    return ["PICKUP", "WHEAT", 1]


def _resolve_place_animal(
    pos: tuple[int, int], inv: dict[str, int], target: tuple[int, int], animal: str | None, feat: _Features
) -> list[Any]:
    if animal and inv.get(animal, 0) > 0:
        if pos != target:
            return _move_toward(pos, target)
        return ["PLACE", animal, 1]
    nearest_shed = _nearest_shed_tile(pos, feat.board_size)
    if pos != nearest_shed:
        return _move_toward(pos, nearest_shed)
    if animal:
        return ["PICKUP", animal, 1]
    return ["PASS"]


def _resolve_plant(
    pos: tuple[int, int], target: tuple[int, int], cfg: ReactiveConfigE18V3, profile: RegimeProfile, feat: _Features
) -> list[Any]:
    if pos != target:
        return _move_toward(pos, target)
    species = _choose_plant_species(cfg, profile, feat)
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
    "ROTATION_DIG": "DIG",
    "CARE_NEEDED": "CARE",
    "COLLECT_FERTILIZER_READY": "COLLECT_FERTILIZER",
}


def _resolve_assignment(
    pos: tuple[int, int],
    inv: dict[str, int],
    assignment: _Assignment,
    cfg: ReactiveConfigE18V3,
    profile: RegimeProfile,
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
        return _resolve_plant(pos, target, cfg, profile, feat)
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
# Market order construction
# ---------------------------------------------------------------------------


def _expansion_guard(
    cfg: ReactiveConfigE18V3, profile: RegimeProfile, feat: _Features, core_harvest_requests: int
) -> bool:
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
    if not _core_established(cfg, feat, core_harvest_requests):
        return False
    if len(feat.worker_positions) < profile.min_workers_per_quadrant * len(feat.unlocked_quadrants):
        return False
    return feat.service_pressure <= cfg.expansion_service_pressure_ceiling


def _hire_orders(
    cfg: ReactiveConfigE18V3, profile: RegimeProfile, feat: _Features, money: float
) -> tuple[list[list[Any]], float]:
    orders: list[list[Any]] = []
    headcount = len(feat.worker_positions)
    backlog = sum(1 for o in feat.opportunities if o["kind"] in SERVICE_BACKLOG_KINDS)
    quadrants = max(1, len(feat.unlocked_quadrants))
    floor_headcount = profile.min_workers_per_quadrant * quadrants
    load_driven = (
        (backlog + cfg.tasks_per_worker_per_day - 1) // cfg.tasks_per_worker_per_day
        if backlog > 0
        else 0
    )
    target_headcount = min(profile.max_hands, max(floor_headcount, load_driven))
    hires_today = feat.hires_today
    remaining_money = money
    count = 0
    while (
        count < cfg.hire_batch_limit_per_turn
        and headcount + count < target_headcount
        and headcount + count < profile.max_hands
    ):
        cost = _hire_cost_estimate(hires_today + count)
        if remaining_money < cfg.hire_reserve + cost:
            break
        orders.append(["HIRE"])
        remaining_money -= cost
        count += 1
    return orders, remaining_money


def _seed_orders(
    cfg: ReactiveConfigE18V3, profile: RegimeProfile, feat: _Features, money: float, room_left: int
) -> tuple[list[list[Any]], float]:
    orders: list[list[Any]] = []
    remaining_money = money
    if not feat.has_empty_crop_zone_tile:
        return orders, remaining_money
    for species in profile.crop_species_rotation:
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
    cfg: ReactiveConfigE18V3,
    profile: RegimeProfile,
    feat: _Features,
    money: float,
    room_left: int,
    core_harvest_requests: int,
) -> tuple[list[list[Any]], float]:
    orders: list[list[Any]] = []
    remaining_money = money
    if not _core_established(cfg, feat, core_harvest_requests):
        return orders, remaining_money
    # Zero-risk ledger (E18 lifecycle gate: verified_livestock_losses == 0):
    # never grow the herd while ANY existing animal has ever missed a feed
    # this run's recent window (`unfed_animal_count`, not merely the V1-V3
    # `at_risk_animal_count` which only counted the second consecutive
    # miss). This is strictly more conservative than V3's ratchet.
    if feat.unfed_animal_count > cfg.max_at_risk_animals_for_new_purchase:
        return orders, remaining_money
    if feat.at_risk_animal_count > cfg.max_at_risk_animals_for_new_purchase:
        return orders, remaining_money
    if feat.structures_total <= 0 or feat.animal_headcount >= feat.structures_total:
        return orders, remaining_money
    max_serviceable_herd = max(1, int(len(feat.worker_positions) * cfg.herd_per_worker_ratio))
    if feat.animal_headcount >= max_serviceable_herd:
        return orders, remaining_money
    if remaining_money < cfg.animal_purchase_reserve:
        return orders, remaining_money
    # V2 fix (MODEL_SPEC V2, remediation item 1): never buy a new animal
    # before its feed buffer already exists in the shed -- `_wheat_stock_orders`
    # stocks proactively from the moment a structure exists, so by the time
    # this authorizes a purchase the buffer should already be there; if it
    # is not (e.g. WHEAT price above ceiling that call), wait rather than
    # add a mouth to feed with nothing to feed it.
    if feat.shed.get("WHEAT", 0) < cfg.feed_security_buffer_per_animal:
        return orders, remaining_money
    for species in cfg.livestock_species_rotation:
        if len(orders) >= room_left:
            break
        structure = ANIMALS[species]["structure"]
        if feat.empty_structure_type_counts.get(structure, 0) <= 0:
            continue
        unit_price = float(feat.market_prices.get(species, ANIMALS[species]["cost"]))
        cost = unit_price
        if remaining_money - cfg.animal_purchase_reserve < cost:
            continue
        orders.append(["BUY_ANIMAL", species, 1])
        remaining_money -= cost
        break
    return orders, remaining_money


def _wheat_stock_orders(
    cfg: ReactiveConfigE18V3, feat: _Features, money: float, room_left: int
) -> tuple[list[list[Any]], float]:
    """V2 fix (MODEL_SPEC V2, remediation item 1): stock feed *proactively*,
    from the moment any livestock structure exists (``structures_total >
    0``), not reactively once an animal is already living there
    (``animal_headcount > 0``, V1's gate). The traced audit found the first
    animal placed with zero WHEAT in the shed and no worker able to feed it
    for two consecutive days -- escaping on the third -- precisely because
    V1 never bought feed until an animal already needed it. `target_stock`
    is sized for at least one animal even at `animal_headcount == 0`, so
    the buffer is already in place before `_animal_orders` (below)
    authorizes the purchase that will need it."""

    orders: list[list[Any]] = []
    remaining_money = money
    if feat.structures_total <= 0:
        return orders, remaining_money
    wheat_price = float(feat.market_prices.get("WHEAT", cfg.wheat_buy_price_ceiling))
    if wheat_price > cfg.wheat_buy_price_ceiling:
        return orders, remaining_money
    wheat_stock = feat.shed.get("WHEAT", 0)
    target_stock = max(1, feat.animal_headcount) * cfg.feed_security_buffer_per_animal
    if wheat_stock >= target_stock:
        return orders, remaining_money
    qty = min(cfg.wheat_buy_batch_cap, target_stock - wheat_stock)
    cost = wheat_price * qty
    if len(orders) < room_left and remaining_money - cfg.market_order_min_cash >= cost and qty > 0:
        orders.append(["BUY_WHEAT", int(qty)])
        remaining_money -= cost
    return orders, remaining_money


def _sell_orders(cfg: ReactiveConfigE18V3, feat: _Features, room_left: int) -> list[list[Any]]:
    orders: list[list[Any]] = []
    for item in SELLABLE_PRODUCE:
        if len(orders) >= room_left:
            break
        qty = feat.shed.get(item, 0)
        if qty <= 0:
            continue
        if item == "WHEAT":
            continue
        orders.append(["SELL", item, int(qty)])
    return orders


def _build_market_orders(
    cfg: ReactiveConfigE18V3,
    profile: RegimeProfile,
    snap: Any,
    feat: _Features,
    core_harvest_requests: int,
) -> list[list[Any]]:
    limit = int(snap.configuration_snapshot.get("maxMarketOrdersPerTurn", cfg.fallback_market_order_batch_limit))
    orders: list[list[Any]] = []
    money = feat.money

    hire_orders, money = _hire_orders(cfg, profile, feat, money)
    orders.extend(hire_orders)

    # V2 emergency queue (MODEL_SPEC V2, remediation item 2): while any
    # animal is unfed today, non-urgent growth commitments -- new land and
    # new crop seed -- are suppressed entirely, not just new animal
    # purchases (V1 already gated those). HIRE and WHEAT/SELL orders are
    # deliberately exempt: more workers and more feed stock are exactly
    # what resolves the emergency, not what competes with it.
    emergency = feat.animals_at_risk

    if not feat.in_shutdown:
        if not emergency and _expansion_guard(cfg, profile, feat, core_harvest_requests):
            n_extra = max(0, len(feat.unlocked_quadrants) - 1)
            cost = LAND_PRICES[n_extra]
            if len(orders) < limit and money - cfg.land_purchase_reserve >= cost:
                orders.append(["BUY_LAND"])
                money -= cost

        if not emergency:
            seed_orders, money = _seed_orders(cfg, profile, feat, money, limit - len(orders))
            orders.extend(seed_orders)

        animal_orders, money = _animal_orders(
            cfg, profile, feat, money, limit - len(orders), core_harvest_requests
        )
        orders.extend(animal_orders)

    wheat_orders, money = _wheat_stock_orders(cfg, feat, money, limit - len(orders))
    orders.extend(wheat_orders)

    orders.extend(_sell_orders(cfg, feat, limit - len(orders)))
    if feat.shed.get("WHEAT", 0) > 0 and feat.animal_headcount <= 0 and len(orders) < limit:
        orders.append(["SELL", "WHEAT", int(feat.shed["WHEAT"])])

    return orders[:limit]


# ---------------------------------------------------------------------------
# Controller
# ---------------------------------------------------------------------------


class ClaudeE18LifecycleSafetyV3:
    """Five-layer opponent-reactive controller (see module docstring)."""

    def __init__(self, config: ReactiveConfigE18V3, run_context: Any = None) -> None:
        self.config = config
        self.run_context = run_context
        self.policy_version = POLICY_VERSION
        self.technical_errors = 0
        self._telemetry: Counter[str] = Counter()
        self._assignments: dict[str, _Assignment] = {}
        self._core_harvest_requests = 0
        self._last_seen_day: int | None = None
        # Layers 1-3 state (sticky, decided at most once per episode).
        self._opponent_snapshot: dict[str, Any] | None = None
        self._opponent_snapshot_day: int | None = None
        self._regime: str | None = None
        self._regime_decision_day: int | None = None
        self._regime_decision_pressure: float | None = None
        self._regime_decision_features: dict[str, Any] | None = None
        self._mode_decisions = 0
        self._regime_transitions: list[dict[str, Any]] = []
        self._action_reasons: list[dict[str, Any]] = []
        # V2 daily economic telemetry (MODEL_SPEC V2, remediation item 3).
        self._daily_log: list[dict[str, Any]] = []
        self._day_counters: dict[str, int] = self._blank_day_counters()
        self._last_day_summary: dict[str, Any] | None = None
        # V3 stable worker identity (module docstring item 10): the engine's
        # own `hands` list order is not stable across turns, so a hand's
        # identity is tracked by greedy nearest-previous-position matching
        # instead of by list index. Reset every day rollover alongside
        # `_assignments`, since hands are re-hired fresh each day (V3 audit:
        # every observed match drops to exactly the farmer at the first step
        # of each new day, before that day's HIRE orders land).
        self._hand_identity_positions: dict[str, tuple[int, int]] = {}
        self._next_hand_id = 0

    @staticmethod
    def _blank_day_counters() -> dict[str, int]:
        return {"harvest": 0, "water": 0, "dig": 0, "feed": 0, "move": 0, "pass": 0, "sold_units": 0}

    def _track_worker_identities(self, positions: list[tuple[int, int]]) -> list[str]:
        """Return a worker key per position in `positions`, index-aligned,
        with the property that the SAME key means the SAME physical worker
        across consecutive calls -- unlike a raw list index, which the
        engine can silently reorder when a new hand is hired (module
        docstring item 10). Index 0 (the farmer) is always a distinguished,
        stable field, never part of the reordered `hands` list, so it keeps
        the literal key ``"farmer"``. Every other position is a hand: it is
        matched to the closest still-unclaimed previous identity within one
        Manhattan tile (a hand moves at most one tile per turn; every
        non-move command leaves it in place, i.e. distance 0), smallest
        distance first so no closer pair loses its match to a farther one
        considered earlier. Anything left unmatched is a newly hired hand
        and gets a fresh, never-reused id."""

        keys = ["farmer"]
        hand_positions = positions[1:]
        if not hand_positions:
            self._hand_identity_positions = {}
            return keys

        previous = self._hand_identity_positions
        candidates: list[tuple[int, int, str]] = []
        for pos_index, pos in enumerate(hand_positions):
            for identity, prev_pos in previous.items():
                distance = abs(pos[0] - prev_pos[0]) + abs(pos[1] - prev_pos[1])
                if distance <= 1:
                    candidates.append((distance, pos_index, identity))
        candidates.sort(key=lambda c: (c[0], c[1], c[2]))

        assigned: list[str | None] = [None] * len(hand_positions)
        used_ids: set[str] = set()
        for distance, pos_index, identity in candidates:
            if assigned[pos_index] is not None or identity in used_ids:
                continue
            assigned[pos_index] = identity
            used_ids.add(identity)

        for pos_index, identity in enumerate(assigned):
            if identity is None:
                assigned[pos_index] = f"hand:{self._next_hand_id}"
                self._next_hand_id += 1

        self._hand_identity_positions = {
            identity: hand_positions[pos_index]
            for pos_index, identity in enumerate(assigned)
            if identity is not None
        }
        keys.extend(identity for identity in assigned if identity is not None)
        return keys

    def __call__(self, observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        try:
            action = self._decide(observation, configuration)
        except Exception:  # noqa: BLE001 - any technical failure must fall
            # back to a safe PASS, never propagate.
            self.technical_errors += 1
            return deepcopy(SAFE_PASS_ACTION)
        self._record_telemetry(action)
        return action

    def _current_profile(self) -> RegimeProfile:
        cfg = self.config
        if self._regime == cfg.regime_high.name:
            return cfg.regime_high
        return cfg.regime_low

    def _maybe_decide_regime(self, observation: dict[str, Any], day: int) -> None:
        """Layers 1-3: capture the opponent snapshot once inside the
        declared window and lock the regime the first time it happens."""

        if self._regime is not None:
            return
        cfg = self.config
        if day < cfg.snapshot_window_start_day:
            return
        my_seat = int(observation.get("player", 0))
        snapshot = _extract_opponent_snapshot(observation, my_seat)
        force_decide = day >= cfg.snapshot_window_end_day
        if snapshot is None:
            if not force_decide:
                return
            snapshot = {
                "unlocked_quadrants": 1,
                "hands": 0,
                "crop_tiles": 0,
                "weed_tiles": 0,
                "animal_count": 0,
                "pasture_count": 0,
            }
        self._opponent_snapshot = snapshot
        self._opponent_snapshot_day = day
        regime, pressure = _classify_regime(cfg, snapshot)
        self._regime = regime
        self._regime_decision_day = day
        self._regime_decision_pressure = pressure
        self._regime_decision_features = dict(snapshot)
        self._mode_decisions += 1
        self._regime_transitions.append(
            {
                "day": day,
                "regime": regime,
                "pressure": pressure,
                "features": dict(snapshot),
            }
        )

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
            for key in [k for k in self._assignments if k != "farmer"]:
                self._assignments.pop(key, None)
            # V3: hands are re-hired fresh each day (audit-verified), so
            # yesterday's identities never mean anything today; starting the
            # matcher from empty avoids matching a brand-new hire to a
            # stale position left over from the previous day.
            self._hand_identity_positions = {}
            self._daily_log.append(
                {
                    "day": self._last_seen_day,
                    **self._day_counters,
                    **(self._last_day_summary or {}),
                }
            )
            self._day_counters = self._blank_day_counters()
        self._last_seen_day = current_day

        self._maybe_decide_regime(observation, current_day)
        # Before the window opens (and force-decide has not fired yet),
        # operate under the low-pressure profile as a conservative default
        # -- no snapshot has been taken, so no opponent-conditioned choice
        # has been made yet; this is bootstrap behaviour, not a decision.
        profile = self._current_profile()

        feat = _extract_features(cfg, profile, snap)

        claimed: set[tuple[int, int]] = set()
        opportunities_index = {(o["kind"], o["x"], o["y"]): o for o in feat.opportunities}
        worker_keys = self._track_worker_identities(feat.worker_positions)
        commands: list[list[Any]] = []
        for worker_key, pos, inv in zip(worker_keys, feat.worker_positions, feat.worker_inventories):
            commands.append(
                self._decide_worker(worker_key, pos, inv, cfg, profile, feat, snap, claimed, opportunities_index)
            )

        self._core_harvest_requests += sum(1 for cmd in commands if cmd and cmd[0] == "HARVEST")

        farmer_cmd = commands[0]
        hands_cmds = commands[1:]
        market_orders = _build_market_orders(cfg, profile, snap, feat, self._core_harvest_requests)

        action = {"farmer": farmer_cmd, "hands": hands_cmds, "market": market_orders}
        self._validate_action(action, len(hands_cmds), snap)
        self._record_daily_counters(commands, market_orders, feat)
        return action

    _OP_TO_DAY_COUNTER: ClassVar[dict[str, str]] = {
        "HARVEST": "harvest",
        "WATER": "water",
        "DIG": "dig",
        "FEED": "feed",
        "PASS": "pass",
    }

    def _record_daily_counters(
        self, commands: list[list[Any]], market_orders: list[list[Any]], feat: _Features
    ) -> None:
        for cmd in commands:
            op = cmd[0] if cmd else "PASS"
            if op in FARMER_MOVES:
                self._day_counters["move"] += 1
                continue
            counter_key = self._OP_TO_DAY_COUNTER.get(op)
            if counter_key is not None:
                self._day_counters[counter_key] += 1
        for order in market_orders:
            if order and order[0] == "SELL" and len(order) > 2:
                self._day_counters["sold_units"] += int(order[2])
        self._last_day_summary = {
            "residual_sellable_inventory": sum(
                v for k, v in feat.shed.items() if k in SELLABLE_PRODUCE
            ),
            "serviced_crop_tiles": feat.plant_tiles_count,
            "backlog": len(feat.opportunities),
            "hands": len(feat.worker_positions) - 1,
            "money": feat.money,
        }

    def _decide_worker(
        self,
        worker_key: str,
        pos: tuple[int, int],
        inv: dict[str, int],
        cfg: ReactiveConfigE18V3,
        profile: RegimeProfile,
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
                candidate = _best_opportunity(
                    pos, feat.opportunities, claimed, feat.board_size, cfg.prefer_same_quadrant
                )
                if candidate is not None and candidate["priority"] <= CRITICAL_PRIORITY_CEILING:
                    assignment = None

        if assignment is None:
            opp = _best_opportunity(
                pos, feat.opportunities, claimed, feat.board_size, cfg.prefer_same_quadrant
            )
            if opp is not None:
                assignment = _Assignment(
                    kind=opp["kind"], target=(opp["x"], opp["y"]), animal=opp.get("animal")
                )
                self._assignments[worker_key] = assignment

        if assignment is None:
            command = _idle_or_deposit(pos, inv, feat)
        else:
            claimed.add(assignment.target)
            command = _resolve_assignment(pos, inv, assignment, cfg, profile, feat)
            # V3 (module docstring item 11): `PICKUP` counts as a stall
            # exactly like `PASS`. `_resolve_feed`/`_resolve_place_animal`
            # only ever emit `PICKUP` when the needed resource is still
            # absent from inventory, and a single successful pickup always
            # yields a `MOVE`/terminal command on the very next call (one
            # unit is always enough to proceed) -- so a *repeated* `PICKUP`
            # can only mean the shed genuinely has none to give, which V1/V2
            # never timed out or reassigned (audit-verified: a worker can
            # burn an entire day on this with zero feeding progress).
            if command and command[0] in ("PASS", "PICKUP"):
                assignment.stalled_steps += 1
                if assignment.stalled_steps >= cfg.assignment_stall_timeout:
                    self._assignments.pop(worker_key, None)
            else:
                assignment.stalled_steps = 0

        op = command[0] if command else "PASS"
        if op in FARMER_MOVES or op == "PASS":
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
        return dict(self._telemetry)

    def telemetry_snapshot(self) -> dict[str, Any]:
        """Layer-by-layer telemetry: snapshot, classifier score, regime,
        transitions, decision count -- required by the E18 gate -- plus
        the V2 daily economic log (remediation item 3): harvested/sold
        units, residual sellable inventory, serviced crop tiles, backlog,
        MOVE/PASS, recorded once per day rollover. The in-progress
        (not-yet-rolled-over) day is included as `current_day_partial` so
        a mid-episode read is never silently missing the latest day."""

        return {
            "opponent_snapshot": self._opponent_snapshot,
            "opponent_snapshot_day": self._opponent_snapshot_day,
            "regime": self._regime,
            "regime_decision_day": self._regime_decision_day,
            "regime_decision_pressure": self._regime_decision_pressure,
            "regime_decision_features": self._regime_decision_features,
            "mode_decisions": self._mode_decisions,
            "regime_transitions": self._regime_transitions,
            "unique_regimes": len({t["regime"] for t in self._regime_transitions}),
            "daily_log": self._daily_log,
            "current_day_partial": {
                "day": self._last_seen_day,
                **self._day_counters,
                **(self._last_day_summary or {}),
            },
        }


def create_claude_e18_lifecycle_safety_v3(
    run_context: Any = None, config_path: str | Path | None = None
) -> ClaudeE18LifecycleSafetyV3:
    """Factory returning a callable ``agent(observation, configuration=None)``."""

    config = ReactiveConfigE18V3.load(config_path)
    return ClaudeE18LifecycleSafetyV3(config=config, run_context=run_context)


def claude_policy_fingerprint(config_path: str | Path | None = None) -> str:
    """SHA-256 over this controller's source and its resolved configuration."""

    source_bytes = _THIS_FILE.read_bytes()
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    config_bytes = path.read_bytes()
    digest = hashlib.sha256()
    digest.update(source_bytes)
    digest.update(config_bytes)
    return digest.hexdigest().upper()


__all__ = [
    "CORE_QUADRANT",
    "DEFAULT_CONFIG_PATH",
    "POLICY_VERSION",
    "SAFE_PASS_ACTION",
    "ActionValidationError",
    "ClaudeE18LifecycleSafetyV3",
    "ReactiveConfigE18V3",
    "RegimeProfile",
    "claude_policy_fingerprint",
    "create_claude_e18_lifecycle_safety_v3",
]
