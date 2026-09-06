"""E18.30 online adapter on the immutable E18.28 C economy/trajectory.

RESCUE redistributes already-planned WATER at risk of missing the day deadline.
POOL adds an isolated surplus-fertilizer treatment in genuine idle windows.
CROP_POOL also transfers endangered planned PLANT->WATER as a complete mission.
OFF delegates directly to the parent, for action-by-action parity checks.
The engine permits movement over every in-bounds tile (including LOCKED), so
the shortest orthogonal path is exact here; locked service targets are rejected.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from docs.model_specs.codex.e18.tools.e18_28_full_season_controller import (
    SHED_ACCESS,
    FullSeasonController,
)
from docs.model_specs.codex.e18.tools.e18_30_mission_dispatcher import (
    Mission,
    MissionDispatcher,
    RouteOffer,
    Status,
)

MOVES = {"EAST": (1, 0), "WEST": (-1, 0), "SOUTH": (0, 1), "NORTH": (0, -1)}


def route(start, target, size=10):
    """Legal shortest path under the inspected engine's movement contract."""
    if any(not 0 <= c < size for p in (start, target) for c in p):
        raise ValueError("Route endpoint outside board")
    x, y = start
    tx, ty = target
    return [["EAST" if tx > x else "WEST"]] * abs(tx - x) + [
        ["SOUTH" if ty > y else "NORTH"]
    ] * abs(ty - y)


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class MissionRuntimeController(FullSeasonController):
    def __init__(self, plan, seat=0, variant="RESCUE", reference_plan=None):
        super().__init__(plan, seat, reference_plan)
        if variant not in {"OFF", "RESCUE", "POOL", "CROP_POOL"}:
            raise ValueError(variant)
        self.runtime_variant = variant
        self.pool = MissionDispatcher()
        self.pool_day = 0
        self.jobs = {}
        self.active = {}
        self.runtime_daily = defaultdict(Counter)
        self.mission_log = []
        self.prepared = None
        self.selected = []
        self.shed_capacity = 100
        self._confirmed = set()
        self._cancelled = set()
        self._last_roster_size = 0
        self.plant_confirmed = set()

    @staticmethod
    def worker_id(day, slot):
        # Hands only append intraday, and ALL hands disappear at daily refresh.
        # Therefore identity is (day, slot), not slot across the whole episode.
        return (day - 1) * 13 + slot

    def _planned_or_recovery(self, row, farm, private, worker, key):
        if self.runtime_variant == "CROP_POOL" and row["opcode"] in {"PLANT", "WATER"}:
            target = tuple(row["position"])
            if row["opcode"] == "PLANT" and (key[0], target) in self.plant_confirmed:
                tile = self._tile(farm, target)
                if (
                    isinstance(tile, dict)
                    and tile.get("kind") == "PLANT"
                    and tile.get("crop") == row["arguments"].get("crop")
                    and tile.get("planted_day") == key[0] - 1
                ):
                    self._advance(key)
                    self.runtime_daily[key[0]]["donor_plant_acknowledged"] += 1
                    return ["PASS"], None
            for job in self.active.values():
                if (
                    job["day"] == key[0]
                    and job["op"] == "PLANT_WATER"
                    and job["target"] == target
                    and job["phase"] != "RETURN"
                ):
                    self.runtime_daily[key[0]]["donor_wait_for_crop_ack"] += 1
                    return ["PASS"], None
        if self.runtime_variant != "OFF" and row["opcode"] == "WATER":
            for job in self.active.values():
                if (
                    job["day"] == key[0]
                    and job["op"] == "WATER"
                    and tuple(row["position"]) == job["target"]
                    and job["phase"] in {"OUT", "SERVICE_ACK"}
                ):
                    # Retain the original task until observed WATER confirms it;
                    # do not destroy the donor's task on mere assignment/emission.
                    self.runtime_daily[key[0]]["donor_wait_for_water_ack"] += 1
                    return ["PASS"], None
        return super()._planned_or_recovery(row, farm, private, worker, key)

    def _worker_command(self, day, turn, worker, farm, private):
        if self.runtime_variant != "OFF" and self.prepared == (day, turn):
            return self.selected[worker]
        return super()._worker_command(day, turn, worker, farm, private)

    def _remaining_rows(self, day, worker):
        key = (day, worker)
        return [
            r
            for r in self.routes.get(key, [])[self.cursors[key] :]
            if r["opcode"] != "PASS"
        ]

    def _pending_requirements(self, day, requirement_kind):
        needed = super()._pending_requirements(day, requirement_kind)
        if self.runtime_variant == "CROP_POOL" and requirement_kind != "pickup":
            for d, owner in self.routes:
                if d != day:
                    continue
                for row in self._remaining_rows(day, owner):
                    if (
                        row["opcode"] == "PLANT"
                        and (day, tuple(row["position"])) in self.plant_confirmed
                    ):
                        needed[row["arguments"]["crop"]] -= int(
                            row["arguments"].get("units", 1)
                        )
        return +needed

    def _water_eta(self, day, turn, owner, target, farm, baseline=None):
        pos = self._position(farm, owner)
        if pos is None:
            return 10**6
        tick = turn
        if baseline is not None and owner < len(baseline):
            command = baseline[owner][0]
            if command[0] in MOVES:
                dx, dy = MOVES[command[0]]
                pos = (pos[0] + dx, pos[1] + dy)
            # Cursors have already consumed the selected command. Continue
            # from its post-batch position/time, not the previous observation.
            tick += 1
        for row in self._remaining_rows(day, owner):
            tick = max(tick, int(row["turn"]))
            dest = tuple(row["position"])
            tick += distance(pos, dest)
            if row["opcode"] not in MOVES:
                tick += 1
            pos = dest
            if row["opcode"] == "WATER" and dest == target:
                return tick - 1
        return 10**6

    def _new_day(self, day):
        if day == self.pool_day:
            return
        for job in self.active.values():
            self.runtime_daily[job["day"]]["unfinished_at_day_refresh"] += 1
            job["phase"] = "EXPIRED"
        self.pool_day = day
        self.pool = MissionDispatcher()
        self.jobs, self.active = {}, {}
        self._confirmed = set()
        self._cancelled = set()
        self._last_roster_size = 0

    def _observe(self, day, turn, farm, private):
        self._confirmed = set()
        self._cancelled = set()
        for key, job in list(self.active.items()):
            slot = job["worker"]
            pos = self._position(farm, slot)
            if pos is None:
                self.runtime_daily[day]["unexpected_worker_loss"] += 1
                continue
            inv = self._inventory(private, slot)
            tile = self._tile(farm, job["target"])
            if job["op"] == "PLANT_WATER":
                expected = (
                    isinstance(tile, dict)
                    and tile.get("kind") == "PLANT"
                    and tile.get("crop") == job["crop"]
                    and tile.get("planted_day") == day - 1
                )
                if job["phase"] == "PLANT_ACK":
                    if expected:
                        self.plant_confirmed.add((day, job["target"]))
                        self.runtime_daily[day]["ack_PLANT"] += 1
                        job["phase"] = "INITIAL_WATER"
                    else:
                        self.runtime_daily[day]["plant_unacknowledged"] += 1
                        job["phase"] = "OUT"
                if job["phase"] == "INITIAL_WATER" and not expected:
                    job["phase"], job["cancelled_target"] = "RETURN", True
                if job["phase"] == "OUT":
                    job["needs_dig"] = (
                        isinstance(tile, dict) and tile.get("kind") == "WEED"
                    )
            if job["phase"] == "SERVICE_ACK":
                observed = (
                    (isinstance(tile, dict) and tile.get("watered_today"))
                    if job["op"] in {"WATER", "PLANT_WATER"}
                    else inv.get("FERTILIZER", 0) > job["before_units"]
                )
                if observed:
                    self.runtime_daily[day]["ack_" + job["op"]] += 1
                    job["phase"] = (
                        "DELIVER" if job["op"] == "COLLECT_FERTILIZER" else "RETURN"
                    )
                else:
                    self.runtime_daily[day]["service_unacknowledged"] += 1
                    job["phase"] = (
                        "INITIAL_WATER" if job["op"] == "PLANT_WATER" else "OUT"
                    )
            if job["phase"] == "DROP_ACK":
                if not inv and job.get("drop_capacity_verified"):
                    # Capacity and slot-order were checked before emission;
                    # the gate separately verifies actual delivered units in engine.
                    self.runtime_daily[day]["drop_ack_units"] += job["drop_units"]
                    job["phase"] = "RETURN"
                else:
                    self.runtime_daily[day]["drop_unacknowledged"] += 1
                    job["phase"] = "DELIVER"
            if job["phase"] == "OUT":
                valid = (
                    (
                        tile is None
                        or (isinstance(tile, dict) and tile.get("kind") == "WEED")
                    )
                    if job["op"] == "PLANT_WATER"
                    else (
                        (
                            isinstance(tile, dict)
                            and tile.get("kind") == "PLANT"
                            and not tile.get("watered_today")
                        )
                        if job["op"] == "WATER"
                        else (
                            isinstance(tile, dict)
                            and tile.get("animal")
                            and tile.get("fertilizer_available")
                        )
                    )
                )
                if not valid:
                    job["phase"] = "RETURN"
                    job["cancelled_target"] = True
                    self.runtime_daily[day]["target_changed"] += 1
            if job["phase"] == "RETURN" and (
                job["origin"] is None or pos == job["origin"]
            ):
                job["phase"], job["ack_turn"] = "DONE", turn
                (
                    self._cancelled if job.get("cancelled_target") else self._confirmed
                ).add(key)
                del self.active[key]
                self.runtime_daily[day][
                    "missions_cancelled"
                    if job.get("cancelled_target")
                    else "missions_completed"
                ] += 1

    def _steps(self, job, pos):
        phase = job["phase"]
        origin = job["origin"]
        if phase == "RETURN":
            return route(pos, origin) if origin is not None else []
        if phase == "DELIVER":
            return (
                route(pos, job["shed"])
                + [["DROP"]]
                + (route(job["shed"], origin) if origin is not None else [])
            )
        if phase == "INITIAL_WATER":
            return (
                route(pos, job["target"])
                + [["WATER"]]
                + (route(job["target"], origin) if origin is not None else [])
            )
        if phase != "OUT":
            return []
        service = (
            ([["DIG"]] if job.get("needs_dig") else [])
            + [["PLANT", job["crop"]], ["WATER"]]
            if job["op"] == "PLANT_WATER"
            else [[job["op"]]]
        )
        steps = route(pos, job["target"]) + service
        end = job["target"]
        if job["op"] == "COLLECT_FERTILIZER":
            steps += route(end, job["shed"]) + [["DROP"]]
            end = job["shed"]
        if origin is not None:
            steps += route(end, origin)
        return steps

    def _candidate_jobs(self, day, turn, farm, private, baseline, snapshot):
        pending_fert = set()
        water = {}
        crops = {}
        for (d, owner), rows in self.routes.items():
            if d != day:
                continue
            remaining = rows[self.cursors[(d, owner)] :]
            for index, row in enumerate(remaining):
                coord = tuple(row["position"])
                if row["opcode"] == "COLLECT_FERTILIZER":
                    pending_fert.add(coord)
                if self.runtime_variant == "CROP_POOL" and row["opcode"] == "PLANT":
                    tile = self._tile(farm, coord)
                    crop = row["arguments"]["crop"]
                    following = next(
                        (
                            r
                            for r in remaining[index + 1 :]
                            if r["opcode"] not in {*MOVES, "PASS"}
                        ),
                        None,
                    )
                    if (
                        following is not None
                        and following["opcode"] == "WATER"
                        and tuple(following["position"]) == coord
                        and (
                            tile is None
                            or (isinstance(tile, dict) and tile.get("kind") == "WEED")
                        )
                        and private.get("seeds", {}).get(crop, 0) > 0
                        and self._water_eta(day, turn, owner, coord, farm, baseline)
                        > (23 if day == 30 else 24)
                    ):
                        crops.setdefault(coord, (owner, crop))
                if row["opcode"] != "WATER" or int(row["turn"]) > turn:
                    continue
                tile = self._tile(farm, coord)
                if not (
                    isinstance(tile, dict)
                    and tile.get("kind") == "PLANT"
                    and not tile.get("watered_today")
                ):
                    continue
                eta = self._water_eta(
                    day,
                    turn,
                    owner,
                    coord,
                    farm,
                    baseline if self.runtime_variant == "CROP_POOL" else None,
                )
                if eta > (23 if day == 30 else 24):
                    water.setdefault(coord, owner)
        emitting = defaultdict(set)
        for slot, (command, _) in enumerate(baseline):
            emitting[command[0]].add(self._position(farm, slot))
        candidates = [
            ("WATER", coord, owner)
            for coord, owner in water.items()
            if coord not in emitting["WATER"]
            and not any(
                j["op"] == "PLANT_WATER" and j["target"] == coord
                for j in self.active.values()
            )
        ]
        candidates += [
            ("PLANT_WATER", coord, owner)
            for coord, (owner, _) in crops.items()
            if coord not in emitting["PLANT"]
        ]
        if self.runtime_variant in {"POOL", "CROP_POOL"}:
            for y, row in enumerate(farm["tiles"]):
                for x, tile in enumerate(row):
                    coord = (x, y)
                    if (
                        isinstance(tile, dict)
                        and tile.get("animal")
                        and tile.get("fertilizer_available")
                        and coord not in pending_fert
                        and coord not in emitting["COLLECT_FERTILIZER"]
                    ):
                        candidates.append(("COLLECT_FERTILIZER", coord, None))
        for op, target, donor in candidates:
            key = f"{day}:{op}:{target[0]},{target[1]}"
            if key not in self.jobs:
                self.jobs[key] = {
                    "key": key,
                    "day": day,
                    "op": op,
                    "target": target,
                    "donor": donor,
                }
                if op == "PLANT_WATER":
                    self.jobs[key]["crop"] = crops[target][1]
                self.pool.submit(
                    Mission(
                        key,
                        snapshot,
                        (day - 1) * 24 + 22,
                        1.0,
                        safety=op in {"WATER", "PLANT_WATER"},
                    )
                )

    def _prepare(self, observation, configuration):
        day, turn = int(observation["day"]) + 1, int(observation["hour"]) + 1
        snapshot = (day - 1) * 24 + turn - 1
        farm, private = observation["farms"][self.seat], observation["private"]
        self.shed_capacity = int((configuration or {}).get("shedCapacity", 100))
        self._new_day(day)
        if len(farm["hands"]) < self._last_roster_size:
            raise ValueError("Unexpected intraday roster shrink; identity not safe")
        self._last_roster_size = len(farm["hands"])
        self._observe(day, turn, farm, private)
        active_slots = {j["worker"] for j in self.active.values()}
        baseline = [
            (["PASS"], None)
            if w in active_slots
            else super(MissionRuntimeController, self)._worker_command(
                day, turn, w, farm, private
            )
            for w in range(len(farm["hands"]) + 1)
        ]
        self.selected = baseline
        self.prepared = (day, turn)
        if day < 7 or turn < 3 or turn > 23:
            return
        self._candidate_jobs(day, turn, farm, private, baseline, snapshot)
        incoming = sum(
            sum(self._inventory(private, w).values())
            for w, (cmd, _) in enumerate(baseline)
            if cmd[0] == "DROP" and self._position(farm, w) in SHED_ACCESS
        )
        room = max(0, self.shed_capacity - sum(private["shed"].values()) - incoming)
        capacities = {"shed_room": room, "new_shed_room": max(0, room - 10)}
        if self.runtime_variant == "CROP_POOL":
            emitted_seeds = Counter(c[1] for c, _ in baseline if c[0] == "PLANT")
            capacities.update(
                {
                    "seed:" + crop: max(0, units - emitted_seeds[crop])
                    for crop, units in private.get("seeds", {}).items()
                }
            )
        offers, bindings = [], {}
        for key, descriptor in self.jobs.items():
            record = self.pool.records[key]
            if (
                record.status in {Status.DONE, Status.EXPIRED, Status.CANCELLED}
                or key in self._confirmed
                or key in self._cancelled
            ):
                continue
            running = self.active.get(key)
            for slot, (cmd, _) in enumerate(baseline):
                pos = self._position(farm, slot)
                if running is not None:
                    if slot != running["worker"]:
                        continue
                    job = running
                else:
                    tile = self._tile(farm, descriptor["target"])
                    valid = (
                        (
                            tile is None
                            or (isinstance(tile, dict) and tile.get("kind") == "WEED")
                        )
                        if descriptor["op"] == "PLANT_WATER"
                        else (
                            isinstance(tile, dict)
                            and tile.get("kind") == "PLANT"
                            and not tile.get("watered_today")
                        )
                        if descriptor["op"] == "WATER"
                        else (
                            isinstance(tile, dict)
                            and tile.get("animal")
                            and tile.get("fertilizer_available")
                        )
                    )
                    if not valid or any(
                        c[0]
                        == (
                            "PLANT"
                            if descriptor["op"] == "PLANT_WATER"
                            else descriptor["op"]
                        )
                        and self._position(farm, w) == descriptor["target"]
                        for w, (c, _) in enumerate(baseline)
                    ):
                        continue
                    if (
                        slot in active_slots
                        or cmd[0] != "PASS"
                        or self._inventory(private, slot)
                    ):
                        continue
                    pending = self._remaining_rows(day, slot)
                    # Only borrow a known future calendar gap, never a blocked
                    # currently-due task that could become executable next batch.
                    if pending and int(pending[0]["turn"]) <= turn:
                        continue
                    origin = pos if pending else None
                    fence = min(23, int(pending[0]["turn"]) - 1) if pending else 23
                    job = dict(
                        descriptor,
                        worker=slot,
                        origin=origin,
                        phase="OUT",
                        start_turn=turn,
                        fence=fence,
                        needs_dig=isinstance(tile, dict) and tile.get("kind") == "WEED",
                    )
                    if descriptor["op"] == "COLLECT_FERTILIZER":
                        job["shed"] = min(
                            SHED_ACCESS,
                            key=lambda s: (
                                distance(job["target"], s)
                                + (distance(s, origin) if origin is not None else 0),
                                s,
                            ),
                        )
                steps = self._steps(job, pos)
                if not steps:
                    continue
                if turn + len(steps) - 1 > job["fence"]:
                    if running is not None:
                        self.runtime_daily[day]["active_route_deadline_blocked"] += 1
                    continue
                claims = []
                if job["phase"] in {"OUT", "INITIAL_WATER"}:
                    resource = "tile:" + key
                    if self.runtime_variant == "CROP_POOL" and job["op"] in {
                        "WATER",
                        "PLANT_WATER",
                    }:
                        resource = f"tile:{day}:water:{job['target']}"
                    capacities[resource] = 1
                    claims.append((resource, 1))
                if job["op"] == "PLANT_WATER" and job["phase"] == "OUT":
                    claims.append(("seed:" + job["crop"], 1))
                if job["op"] == "COLLECT_FERTILIZER" and job["phase"] != "RETURN":
                    claims.append(("shed_room", 1))
                    if running is None:
                        claims.append(("new_shed_room", 1))
                identity = self.worker_id(day, slot)
                offers.append(
                    RouteOffer(key, identity, snapshot, len(steps), tuple(claims))
                )
                bindings[(identity, key)] = job
        roster = [self.worker_id(day, s) for s in range(len(baseline))]
        decision = self.pool.tick(
            snapshot,
            roster,
            offers,
            capacities=capacities,
            confirmed=self._confirmed,
            invalidated=self._cancelled,
        )
        self.runtime_daily[day].update(
            {"reject_" + k: v for k, v in decision.rejected_offers.items()}
        )
        for identity, key in decision.assignments.items():
            job = bindings[(identity, key)]
            if key not in self.active:
                self.active[key] = job
                self.mission_log.append(job)
                self.runtime_daily[day]["missions_started"] += 1
            slot = job["worker"]
            command = self._steps(job, self._position(farm, slot))[0]
            row = None
            if job["op"] == "PLANT_WATER" and command[0] in {"PLANT", "WATER"}:
                job["phase"] = "PLANT_ACK" if command[0] == "PLANT" else "SERVICE_ACK"
            elif command[0] == job["op"]:
                job["before_units"] = self._inventory(private, slot).get(
                    "FERTILIZER", 0
                )
                job["phase"] = "SERVICE_ACK"
            elif command[0] == "DROP":
                inventory = self._inventory(private, slot)
                # Reserve every baseline DROP regardless of ordering, plus all
                # new pool DROP units, before accepting an overflow-sensitive DROP.
                amount = sum(inventory.values())
                if amount > room:
                    self.runtime_daily[day]["delivery_capacity_wait"] += 1
                    continue
                room -= amount
                job.update(
                    phase="DROP_ACK", drop_units=amount, drop_capacity_verified=True
                )
                row = {
                    "opcode": "DROP",
                    "position": list(self._position(farm, slot)),
                    "arguments": {"expected_items": dict(inventory)},
                }
            self.selected[slot] = (command, row)
            self.runtime_daily[day]["extra_" + command[0]] += 1

    def __call__(self, observation, configuration=None):
        if self.runtime_variant == "OFF":
            return super().__call__(observation, configuration)
        try:
            self._prepare(observation, configuration)
            return super().__call__(observation, configuration)
        except Exception as exc:  # noqa: BLE001 - fail closed, explicit gate failure
            self.error_count += 1
            self.last_error = f"{type(exc).__name__}: {exc}"
            return {"farmer": ["PASS"], "hands": [], "market": []}

    def acknowledge_terminal(self, observation):
        if self.runtime_variant == "OFF":
            return
        day, turn = observation["day"] + 1, observation["hour"] + 1
        self._observe(
            day, turn, observation["farms"][self.seat], observation["private"]
        )

    @property
    def incomplete_missions(self):
        return len(self.active) + sum(
            d.get("unfinished_at_day_refresh", 0) for d in self.runtime_daily.values()
        )
