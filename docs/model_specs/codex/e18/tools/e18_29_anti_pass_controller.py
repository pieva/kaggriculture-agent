"""Closed surplus-fertilizer missions after the immutable E18.28 daily queue."""

from collections import Counter, defaultdict

from docs.model_specs.codex.e18.tools.e18_28_full_season_controller import (
    SHED_ACCESS,
    FullSeasonController,
)


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class AntiPassController(FullSeasonController):
    def __init__(self, plan, seat=0, variant="B", reference_plan=None):
        super().__init__(plan, seat, reference_plan)
        assert variant in {"OFF", "A", "B"}
        self.anti_variant = variant
        self.missions = {}
        self.claims = set()
        self.emitted_collection = defaultdict(set)
        self.anti_daily = defaultdict(Counter)
        self.mission_log = []

    def _unfinished_productive(self, day, worker):
        key = (day, worker)
        return [
            r
            for r in self.routes.get(key, [])[self.cursors[key] :]
            if r["opcode"] != "PASS"
        ]

    def _planned_collection(self, day, turn):
        pending = set(self.emitted_collection[(day, turn)])
        for (route_day, worker), rows in self.routes.items():
            if route_day == day:
                pending.update(
                    tuple(r["position"])
                    for r in rows[self.cursors[(day, worker)] :]
                    if r["opcode"] == "COLLECT_FERTILIZER"
                )
        return pending

    def _admit(self, day, turn, worker, farm, private):
        pos = self._position(farm, worker)
        if pos is None or self._inventory(private, worker):
            return None
        # Capacity 100 in the frozen benchmark. Leave room for planned drops;
        # recheck at delivery because other workers can fill the shed meanwhile.
        if sum(private.get("shed", {}).values()) >= 90:
            return None
        pending = self._planned_collection(day, turn)
        candidates = []
        for y, row in enumerate(farm["tiles"]):
            for x, tile in enumerate(row):
                coord = (x, y)
                if not (
                    isinstance(tile, dict)
                    and tile.get("animal")
                    and tile.get("fertilizer_available")
                ):
                    continue
                if coord in pending or (day, coord) in self.claims:
                    continue
                shed = min(
                    SHED_ACCESS,
                    key=lambda s: (distance(coord, s) + distance(s, pos), s),
                )
                cost = (
                    distance(pos, coord)
                    + 1
                    + distance(coord, shed)
                    + 1
                    + distance(shed, pos)
                )
                if cost <= 24 - turn:  # last action H23, not terminal H24
                    candidates.append((cost, coord, shed))
        if not candidates:
            return None
        cost, target, shed = min(candidates)
        mission = dict(
            day=day,
            worker=worker,
            start_turn=turn,
            origin=pos,
            target=target,
            shed=shed,
            reserved_actions=cost,
            phase="OUTBOUND",
            collected=0,
        )
        self.claims.add((day, target))
        self.missions[(day, worker)] = mission
        self.anti_daily[day]["missions_started"] += 1
        self.mission_log.append(mission)
        return mission

    def _mission_command(self, day, turn, worker, farm, private, mission):
        pos = self._position(farm, worker)
        inv = self._inventory(private, worker)
        stats = self.anti_daily[day]
        phase = mission["phase"]
        if phase == "COLLECT_ACK":
            if inv.get("FERTILIZER", 0):
                mission["collected"] = inv["FERTILIZER"]
                stats["collection_ack_units"] += inv["FERTILIZER"]
                mission["phase"] = "DELIVER"
            else:
                stats["collection_failed"] += 1
                mission["phase"] = "RETURN"
        elif phase == "DROP_ACK":
            # DROP clears the inventory even when full. The engine-ledger gate
            # also checks delivered units, so empty inventory alone is not proof.
            stats["drop_inventory_cleared"] += int(not inv)
            mission["phase"] = "RETURN"
        phase = mission["phase"]
        if phase == "OUTBOUND":
            tile = self._tile(farm, mission["target"])
            if not (
                isinstance(tile, dict)
                and tile.get("animal")
                and tile.get("fertilizer_available")
            ):
                stats["target_cancelled"] += 1
                mission["phase"] = "RETURN"
            elif pos != mission["target"]:
                return self._move_toward(pos, mission["target"])[0], None
            else:
                mission["phase"] = "COLLECT_ACK"
                self.emitted_collection[(day, turn)].add(pos)
                return ["COLLECT_FERTILIZER"], None
        if mission["phase"] == "DELIVER":
            if pos != mission["shed"]:
                return self._move_toward(pos, mission["shed"])[0], None
            # Do not destroy inventory in a full shed. Abort the gate if this
            # deadline reserve is consumed; never silently label it completed.
            nearby_inventory = sum(
                sum(self._inventory(private, other).values())
                for other in range(1 + len(farm.get("hands", [])))
                if other != worker and self._position(farm, other) in SHED_ACCESS
            )
            if (
                sum(private.get("shed", {}).values())
                + sum(inv.values())
                + nearby_inventory
                > 100
            ):
                stats["delivery_capacity_wait"] += 1
                return ["PASS"], None
            mission["phase"] = "DROP_ACK"
            return ["DROP"], {
                "opcode": "DROP",
                "position": list(pos),
                "arguments": {"expected_items": dict(inv)},
            }
        if mission["phase"] == "RETURN":
            if pos != mission["origin"]:
                return self._move_toward(pos, mission["origin"])[0], None
            mission["phase"] = "DONE"
            mission["ack_turn"] = turn
            stats["missions_completed"] += 1
            del self.missions[(day, worker)]
        return ["PASS"], None

    def _worker_command(self, day, turn, worker, farm, private):
        stats = self.anti_daily[day]
        key = (day, worker)
        if key in self.missions:
            command, row = self._mission_command(
                day, turn, worker, farm, private, self.missions[key]
            )
            if command[0] != "PASS" or key in self.missions:
                stats["extra_" + command[0]] += 1
                return command, row
        command, row = super()._worker_command(day, turn, worker, farm, private)
        if command[0] == "COLLECT_FERTILIZER":
            self.emitted_collection[(day, turn)].add(self._position(farm, worker))
        if command[0] != "PASS":
            return command, row
        unfinished = self._unfinished_productive(day, worker)
        reason = (
            (
                "WAIT_FOR_SCHEDULED_TURN"
                if int(unfinished[0]["turn"]) > turn
                else "BLOCKED_DUE_TASK"
            )
            if unfinished
            else "NO_MORE_PRODUCTIVE_TASKS_TODAY"
        )
        stats["baseline_pass_" + reason] += 1
        if (
            unfinished
            or self.anti_variant == "OFF"
            or day < 7
            or (self.anti_variant == "A" and day > 12)
        ):
            return command, row
        mission = self._admit(day, turn, worker, farm, private)
        if mission is not None:
            command, row = self._mission_command(
                day, turn, worker, farm, private, mission
            )
            stats["extra_" + command[0]] += 1
        return command, row

    def acknowledge_terminal(self, observation):
        # D30's final observation acknowledges a mission ending on H23.
        # No command returned here is executed in the terminal observation.
        farm, private = observation["farms"][self.seat], observation["private"]
        for (day, worker), mission in list(self.missions.items()):
            if day == 30 and mission["phase"] in {"RETURN", "DROP_ACK"}:
                self._mission_command(30, 24, worker, farm, private, mission)
