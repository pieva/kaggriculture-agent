"""B3: match the two fresh late hires to complete routes that fit their spawn."""

from docs.model_specs.codex.e18.tools.e18_29_anti_pass_controller import (
    AntiPassController,
    distance,
)


class SpawnMatchedAntiPassController(AntiPassController):
    def __init__(self, plan, seat=0, reference_plan=None):
        super().__init__(plan, seat, "B", reference_plan)
        self.assignment_checked = set()
        self.reassignments = []

    @staticmethod
    def route_finish(rows, position, turn):
        for row in rows:
            if row["opcode"] == "PASS":
                continue
            turn = max(turn, int(row["turn"]))
            target = tuple(row["position"])
            turn += distance(position, target)
            if row["opcode"] not in {"NORTH", "SOUTH", "EAST", "WEST"}:
                turn += 1
            position = target
        return turn - 1

    def _assign_fresh_workers(self, day, turn, farm, private):
        if day < 7 or day in self.assignment_checked or len(farm.get("hands", [])) < 12:
            return
        self.assignment_checked.add(day)
        workers = (11, 12)
        keys = [(day, w) for w in workers]
        if any(
            self.cursors[key] or self._inventory(private, w)
            for key, w in zip(keys, workers)
        ):
            return
        if any(key not in self.routes for key in keys):
            return
        rows = [self.routes[key] for key in keys]
        positions = [self._position(farm, w) for w in workers]
        original = [self.route_finish(rows[i], positions[i], turn) for i in (0, 1)]
        swapped = [self.route_finish(rows[1 - i], positions[i], turn) for i in (0, 1)]
        deadline = 23 if day == 30 else 24
        # Do not optimize identity/order when both assignments already fit.
        if max(original) > deadline and max(swapped) <= deadline:
            self.routes[keys[0]], self.routes[keys[1]] = rows[1], rows[0]
            self.anti_daily[day]["fresh_worker_route_swap"] += 1
            self.reassignments.append(
                dict(
                    day=day,
                    turn=turn,
                    workers=workers,
                    positions=positions,
                    original_finish=original,
                    swapped_finish=swapped,
                )
            )

    def _worker_command(self, day, turn, worker, farm, private):
        if worker == 0:
            self._assign_fresh_workers(day, turn, farm, private)
        return super()._worker_command(day, turn, worker, farm, private)
