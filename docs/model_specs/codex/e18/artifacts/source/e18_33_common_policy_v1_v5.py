"""Parametric, quadrant-invariant kernel. No trajectory/controller dependencies.

This first implementation is a diagnostic kernel, not a released full agent.
Prices are passed as observed/conditional quotes; it never sees opponent or seed.
"""
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from math import ceil

from agricola.core.state import CROPS

ANIMALS = {
    "COW": dict(cost=400, first_yield_day=8, interval=2, max_held=6, product="MILK"),
    "SHEEP": dict(cost=500, first_yield_day=6, interval=3, max_held=6, product="WOOL"),
}


@dataclass(frozen=True)
class Profile:
    target: int
    local_capacity: int
    maximum_quadrants: int
    maximum_hands: int
    mix_weights: tuple
    crops: tuple

    @classmethod
    def from_config(cls, config):
        keys = {"schema_version", "pastures", "maximum_unlocked_quadrants", "maximum_hands", "livestock_mix_weights", "allowed_crops"}
        if set(config) != keys or config["schema_version"] != "e18.codex.common_resource_policy.v1":
            raise ValueError("Unknown or missing policy fields; no legacy config merge")
        if set(config["pastures"]) != {"target", "uniform_capacity_per_quadrant"}:
            raise ValueError("Pastures contain only global target and uniform capacity")
        if set(config["livestock_mix_weights"]) != set(ANIMALS):
            raise ValueError("Unsupported species profile")
        numbers = [config["pastures"]["target"], config["pastures"]["uniform_capacity_per_quadrant"],
                   config["maximum_unlocked_quadrants"], config["maximum_hands"], *config["livestock_mix_weights"].values()]
        if any(type(n) is not int or n < 0 for n in numbers) or any(n <= 0 for n in [numbers[1], numbers[2], *numbers[4:]]):
            raise ValueError("Invalid numerical policy limit")
        crops = config["allowed_crops"]
        if not isinstance(crops, list) or not crops or len(set(crops)) != len(crops) or not set(crops) <= set(CROPS):
            raise ValueError("Invalid shared crop set")
        return cls(numbers[0], numbers[1], numbers[2], numbers[3], tuple(sorted(config["livestock_mix_weights"].items())), tuple(crops))

    def validate_board(self, size):
        if size <= 0 or size % 2 or self.maximum_quadrants > 4:
            raise ValueError("Unsupported environment geometry")
        if self.local_capacity > (size // 2) ** 2 or self.target > self.local_capacity * self.maximum_quadrants:
            raise ValueError("Profile cannot fit on permitted land")

    def pasture_budgets(self, activation_order):
        if len(set(activation_order)) != len(activation_order):
            raise ValueError("Duplicate quadrant identity")
        return {q: min(self.local_capacity, max(0, self.target - self.local_capacity * rank))
                if rank < self.maximum_quadrants else 0 for rank, q in enumerate(activation_order)}

    def species_targets(self):
        total = sum(w for _, w in self.mix_weights)
        targets = {s: self.target * w // total for s, w in self.mix_weights}
        order = sorted(self.mix_weights, key=lambda sw: (-(self.target * sw[1] % total), sw[0]))
        for species, _ in order[:self.target - sum(targets.values())]:
            targets[species] += 1
        assert sum(targets.values()) == self.target
        return targets


def quadrant(coord, size):
    x, y = coord
    return ("N" if y < size // 2 else "S") + ("W" if x < size // 2 else "E")


def shed_access(size):
    h = size // 2
    return ((h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h))


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def walk(start, target):
    x, y = start
    tx, ty = target
    return [["EAST" if tx > x else "WEST"]] * abs(tx - x) + [["SOUTH" if ty > y else "NORTH"]] * abs(ty - y)


def biological_deadline(tile, day, turns_per_day, episode_steps):
    """Last executable zero-based step before starvation/escape/episode end."""
    if tile.get("kind") == "PLANT":
        counter, done = tile.get("consecutive_unwatered", 0), tile.get("watered_today", False)
    elif tile.get("animal"):
        counter, done = tile.get("consecutive_unfed", 0), tile.get("fed_today", False)
    else:
        raise ValueError("No biological obligation on this tile")
    next_failure_day = day + (2 if done else max(0, 1 - counter))
    return min(episode_steps - 2, (next_failure_day + 1) * turns_per_day - 1)


def needs_water(tile, day):
    if tile.get("watered_today"):
        return False
    rule = CROPS[tile["crop"]]
    age = day - tile["planted_day"]
    return (tile.get("consecutive_unwatered", 0) >= 1 or
            not rule["ongoing"] and ceil(rule["max_yield_day"] / 2) <= age <= rule["max_yield_day"] or
            rule["ongoing"] and tile.get("fertilized_until_day", -1) >= day and
            age + 1 >= rule["first_yield_day"] and (age + 1 - rule["first_yield_day"]) % rule["interval"] == 0)


def pasture_candidates(farm, profile, reserved=()):
    """All legal opportunities, not a table of predetermined pasture coordinates."""
    size = len(farm["tiles"])
    profile.validate_board(size)
    quotas = profile.pasture_budgets(farm["unlocked_quadrants"])
    occupied = Counter()
    for y, row in enumerate(farm["tiles"]):
        for x, tile in enumerate(row):
            if isinstance(tile, dict) and tile.get("kind") == "PASTURE":
                occupied[quadrant((x, y), size)] += 1
    reserved = set(reserved)
    for p in reserved:
        tile = farm["tiles"][p[1]][p[0]]
        if not (isinstance(tile, dict) and tile.get("kind") == "PASTURE"):
            occupied[quadrant(p, size)] += 1
    candidates = []
    for y, row in enumerate(farm["tiles"]):
        for x, tile in enumerate(row):
            pos = (x, y)
            q = quadrant(pos, size)
            if pos in reserved or tile == "LOCKED" or isinstance(tile, dict) and tile.get("animal"):
                continue
            empty_pasture = isinstance(tile, dict) and tile.get("kind") == "PASTURE"
            if q not in quotas or (not empty_pasture and occupied[q] >= quotas[q]):
                continue
            candidates.append(pos)
    return sorted(candidates, key=lambda p: (min(distance(p, s) for s in shed_access(size)), p))


def crop_candidates(farm, reserved=()):
    reserved = set(reserved)
    return [(x, y) for y, row in enumerate(farm["tiles"]) for x, tile in enumerate(row)
            if (x, y) not in reserved and (tile is None or isinstance(tile, dict) and tile.get("kind") == "WEED")]


def crop_cashflows(crop, planted_day, final_day, *, fertilized=False):
    """Exact biological potential of one maintained cycle, no future prices.

    Annual harvest at max yield, or earlier at the last useful day; ongoing
    harvest on each production day. Acquisition/execution funding is separate.
    Values become harvestable at the beginning of the indicated day.
    """
    rule = CROPS[crop]
    events = []
    if rule["ongoing"]:
        for k in range(rule["max_yield"]):
            day = planted_day + rule["first_yield_day"] + k * rule["interval"]
            if day <= final_day:
                events.append((day, 2 if fertilized else 1))
    else:
        harvest = min(final_day, planted_day + rule["max_yield_day"])
        age = harvest - planted_day
        if age >= rule["first_yield_day"]:
            waters = max(0, age - ceil(rule["max_yield_day"] / 2) + 1)
            events.append((harvest, min(rule["max_yield"], 1 + waters * (2 if fertilized else 1))))
    return events


def animal_cashflows(species, placed_day, final_day, *, care=True):
    rule = ANIMALS[species]
    events = []
    bonus = 0
    for day in range(placed_day, final_day):
        next_day = day + 1
        age = next_day - placed_day
        if age >= rule["first_yield_day"] and (age - rule["first_yield_day"]) % rule["interval"] == 0:
            events.append((next_day, min(rule["max_held"], 1 + bonus)))
            bonus = 0
        if care:
            bonus += 1
    return events


def new_crop_value(crop, day, final_day, quotes, maintenance_action_cost=0):
    flows = crop_cashflows(crop, day, final_day)
    if not flows:
        return dict(gain=-CROPS[crop]["seed"], revenue=0, cost=CROPS[crop]["seed"], first_income=None, daily_load=0)
    last = flows[-1][0]
    life = last - day + 1
    # Upper service load protects first WATER and permits yield-window WATER.
    actions = 1 + life + len(flows) + 1
    revenue = sum(quotes(crop, "SELL", n) for _, n in flows)
    cost = CROPS[crop]["seed"] + actions * maintenance_action_cost
    return dict(gain=revenue-cost, revenue=revenue, cost=cost, first_income=flows[0][0], daily_load=actions/life)


def new_animal_value(species, day, final_day, quotes, maintenance_action_cost=0):
    rule = ANIMALS[species]
    flows = animal_cashflows(species, day, final_day)
    life = final_day - day + 1
    if not flows:
        return dict(gain=-rule["cost"], revenue=0, cost=rule["cost"], first_income=None, daily_load=0)
    revenue = sum(quotes(rule["product"], "SELL", n) for _, n in flows)
    revenue += quotes("FERTILIZER", "SELL", max(0, life-1))
    cost = rule["cost"] + quotes("WHEAT", "BUY", life) + (3*life + len(flows) + 3)*maintenance_action_cost
    return dict(gain=revenue-cost, revenue=revenue, cost=cost, first_income=min(day+1,flows[0][0]), daily_load=3+len(flows)/life)


class PriceEnvelope:
    """Two preregistered conditional scenarios; history belongs to this episode."""
    def __init__(self):
        self.low = {}
        self.high = {}

    def observe(self, prices):
        for item, price in prices.items():
            self.low[item] = min(price, self.low.get(item, price))
            self.high[item] = max(price, self.high.get(item, price))

    def conservative(self, item, operation, unit_quotes):
        if operation == "SELL":
            return sum(min(p, self.low[item]) for p in unit_quotes)
        return sum(max(p, self.high[item]) for p in unit_quotes)
