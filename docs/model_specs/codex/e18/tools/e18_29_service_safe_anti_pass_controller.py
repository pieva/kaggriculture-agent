"""B2: retain surplus missions, preempt optional boosts before deadline overrun."""

from docs.model_specs.codex.e18.tools.e18_29_anti_pass_controller import (
    AntiPassController,
    distance,
)


class ServiceSafeAntiPassController(AntiPassController):
    def __init__(self, plan, seat=0, reference_plan=None):
        super().__init__(plan, seat, "B", reference_plan)
        self.current_turn = 1

    def _earliest_route_finish(self, key, position):
        """Replay the remaining calendar and travel, assuming valid operations.

        Include spawn/position correction; do not assume one scheduled MOVE
        still corresponds to one actual step. This is a feasibility estimate,
        not a forecast of future stochastic tile changes or market fills.
        """
        turn = self.current_turn
        for row in self.routes[key][self.cursors[key] :]:
            if row["opcode"] == "PASS":
                continue
            turn = max(turn, int(row["turn"]))
            target = tuple(row["position"])
            turn += distance(position, target)
            if row["opcode"] not in {"NORTH", "SOUTH", "EAST", "WEST"}:
                turn += 1
            position = target
        return turn - 1

    def _worker_command(self, day, turn, worker, farm, private):
        self.current_turn = turn
        return super()._worker_command(day, turn, worker, farm, private)

    def _planned_or_recovery(self, row, farm, private, worker, key):
        if key[0] >= 7 and row["opcode"] == "FERTILIZE":
            position = self._position(farm, worker)
            limit = 23 if key[0] == 30 else 24
            if position is not None and self._inventory(private, worker).get(
                "FERTILIZER", 0
            ):
                finish = self._earliest_route_finish(key, position)
                if finish > limit:
                    self._advance(key)
                    self.anti_daily[key[0]]["optional_fertilize_preempted"] += 1
                    return ["PASS"], None
        return super()._planned_or_recovery(row, farm, private, worker, key)
