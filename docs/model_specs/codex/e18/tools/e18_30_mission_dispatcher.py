"""E18.30 Gate 0: observation-driven mission allocation, not a game agent.

The adapter must provide persistent observed worker IDs, semantic mission IDs,
acknowledgements and fresh, feasible *complete remaining route* offers. Offers
include travel, service and delivery, not merely distance to the first action.
Resource capacities are the current gross shared quantities BEFORE this pool's
reservations; each offer claims only quantities still needed in this snapshot.
No orders are emitted here and no route/market feasibility is inferred here.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from enum import Enum
from math import isfinite


def _integer(value: int, minimum: int = 0) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


class Status(str, Enum):
    READY = "READY"
    ASSIGNED = "ASSIGNED"
    DONE = "DONE"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


@dataclass(frozen=True)
class Mission:
    key: str
    not_before: int
    deadline: int
    value: float
    safety: bool = False
    dependencies: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self):
        if (
            not isinstance(self.key, str)
            or not self.key
            or not _integer(self.not_before)
            or not _integer(self.deadline)
            or self.deadline < self.not_before
            or not isfinite(self.value)
            or self.value < 0
        ):
            raise ValueError("Invalid mission interval/value/key")
        if self.key in self.dependencies or not isinstance(
            self.dependencies, frozenset
        ):
            raise ValueError(
                "Dependencies must be an immutable set without self-reference"
            )
        if any(not isinstance(key, str) or not key for key in self.dependencies):
            raise ValueError("Dependency IDs must be nonempty strings")


@dataclass(frozen=True)
class RouteOffer:
    mission: str
    worker: int
    snapshot: int
    remaining_steps: int
    claims: tuple[tuple[str, int], ...] = ()
    prerequisites_met: bool = True

    def __post_init__(self):
        if (
            not isinstance(self.mission, str)
            or not self.mission
            or not _integer(self.worker)
            or not _integer(self.snapshot)
            or not _integer(self.remaining_steps, 1)
        ):
            raise ValueError("Invalid route offer")
        if not isinstance(self.prerequisites_met, bool):
            raise TypeError("Prerequisites must be explicitly boolean")
        if not isinstance(self.claims, tuple):
            raise TypeError("Claims must be immutable")
        keys = []
        for claim in self.claims:
            if (
                not isinstance(claim, tuple)
                or len(claim) != 2
                or not isinstance(claim[0], str)
                or not claim[0]
                or not _integer(claim[1], 1)
            ):
                raise ValueError("Claims must have positive integer quantities")
            keys.append(claim[0])
        if len(keys) != len(set(keys)):
            raise ValueError("Duplicate resource in an offer")


@dataclass
class Record:
    mission: Mission
    status: Status = Status.READY
    worker: int | None = None
    reason: str = "NEW"


@dataclass(frozen=True)
class Decision:
    assignments: dict[int, str]
    idle: dict[int, str]
    reserved: dict[str, int]
    rejected_offers: dict[str, int]


class MissionDispatcher:
    """Deterministic greedy allocator with non-preemptive fresh revalidation.

    Call once per increasing observation snapshot. Repeated emission is not
    acknowledgement. An active assignment survives only with a fresh feasible
    remaining-route offer, so consumed resources are not reserved twice.
    """

    def __init__(self):
        self.records: dict[str, Record] = {}
        self.last_snapshot = -1

    def submit(self, mission: Mission) -> None:
        old = self.records.get(mission.key)
        if old is not None:
            if old.mission != mission:
                raise ValueError(f"Conflicting semantic mission ID: {mission.key}")
            return
        self.records[mission.key] = Record(mission)

    def tick(
        self,
        snapshot: int,
        workers: Iterable[int],
        offers: Iterable[RouteOffer],
        *,
        capacities: Mapping[str, int] | None = None,
        confirmed: Iterable[str] = (),
        invalidated: Iterable[str] = (),
        blocked: Iterable[str] = (),
        retry: Iterable[str] = (),
    ) -> Decision:
        workers = tuple(workers)
        roster = set(workers)
        offers = tuple(offers)
        capacities = dict(capacities or {})
        confirmed, invalidated, blocked, retry = map(
            set, (confirmed, invalidated, blocked, retry)
        )
        events = confirmed | invalidated | blocked | retry
        if not _integer(snapshot) or snapshot <= self.last_snapshot:
            raise ValueError("One call per increasing observation snapshot required")
        if (
            len(roster) != len(workers)
            or len(roster) > 13
            or any(not _integer(w) for w in roster)
        ):
            raise ValueError("Observed roster must contain at most farmer + 12 hands")
        if any(
            not isinstance(k, str) or not k or not _integer(v)
            for k, v in capacities.items()
        ):
            raise ValueError("Resource capacities must be non-negative integers")
        if events - self.records.keys() or confirmed & (invalidated | blocked | retry):
            raise ValueError("Unknown or contradictory acknowledgement")
        by_pair = {(o.worker, o.mission): o for o in offers}
        if len(by_pair) != len(offers) or any(
            o.mission not in self.records for o in offers
        ):
            raise ValueError("Unknown mission or ambiguous duplicate route offer")
        for key in confirmed:
            if self.records[key].status in (Status.CANCELLED, Status.EXPIRED):
                raise ValueError("Terminal mission cannot be resurrected")

        self.last_snapshot = snapshot
        for key, record in self.records.items():
            if key in confirmed:
                record.status, record.worker, record.reason = (
                    Status.DONE,
                    None,
                    "OBSERVED_DONE",
                )
            if record.status in (Status.DONE, Status.CANCELLED, Status.EXPIRED):
                continue
            if key in invalidated:
                record.status, record.worker, record.reason = (
                    Status.CANCELLED,
                    None,
                    "INVALIDATED",
                )
            elif snapshot > record.mission.deadline:
                record.status, record.worker, record.reason = (
                    Status.EXPIRED,
                    None,
                    "DEADLINE_EXPIRED",
                )
            elif (
                key in blocked
                or key in retry
                or (record.worker is not None and record.worker not in roster)
            ):
                reason = (
                    "PREREQUISITE_BLOCKED"
                    if key in blocked
                    else "RETRY_REQUESTED"
                    if key in retry
                    else "WORKER_ABSENT"
                )
                record.status, record.worker, record.reason = Status.READY, None, reason

        reserved: Counter[str] = Counter()
        rejected: Counter[str] = Counter()
        assigned: dict[int, str] = {}

        def eligible(offer: RouteOffer) -> str | None:
            record = self.records[offer.mission]
            mission = record.mission
            if offer.worker not in roster:
                return "WORKER_ABSENT"
            if offer.snapshot != snapshot:
                return "STALE_OFFER"
            if offer.mission in blocked or not offer.prerequisites_met:
                return "PREREQUISITE_BLOCKED"
            if any(
                d not in self.records or self.records[d].status != Status.DONE
                for d in mission.dependencies
            ):
                return "DEPENDENCY_UNCONFIRMED"
            if snapshot < mission.not_before:
                return "NOT_READY_YET"
            # The current batch consumes one of remaining_steps. Deadline is
            # the last executable batch, not a terminal observation index.
            if snapshot + offer.remaining_steps - 1 > mission.deadline:
                return "COMPLETE_ROUTE_MISSES_DEADLINE"
            if any(
                reserved[k] + units > capacities.get(k, 0) for k, units in offer.claims
            ):
                return "RESOURCE_CAPACITY"
            return None

        def take(offer: RouteOffer) -> None:
            record = self.records[offer.mission]
            record.status, record.worker, record.reason = (
                Status.ASSIGNED,
                offer.worker,
                "ASSIGNED",
            )
            assigned[offer.worker] = offer.mission
            reserved.update(dict(offer.claims))

        # Keep in-flight work when revalidated; do not steal a worker carrying
        # goods merely because a different mission has a better spot score.
        active = sorted(
            (r for r in self.records.values() if r.status == Status.ASSIGNED),
            key=lambda r: (not r.mission.safety, r.mission.deadline, r.mission.key),
        )
        for record in active:
            offer = by_pair.get((record.worker, record.mission.key))
            reason = eligible(offer) if offer is not None else "REVALIDATION_MISSING"
            if reason is None:
                take(offer)
            else:
                record.status, record.worker, record.reason = Status.READY, None, reason

        def rank(offer: RouteOffer):
            m = self.records[offer.mission].mission
            return (
                not m.safety,
                m.deadline,
                -m.value / offer.remaining_steps,
                offer.remaining_steps,
                m.key,
                offer.worker,
            )

        for offer in sorted(offers, key=rank):
            record = self.records[offer.mission]
            if record.status != Status.READY or offer.worker in assigned:
                continue
            reason = eligible(offer)
            if reason is None:
                take(offer)
            else:
                rejected[reason] += 1
                record.reason = reason
        return Decision(
            assigned,
            {w: "NO_ADMISSIBLE_MISSION" for w in sorted(roster - assigned.keys())},
            dict(reserved),
            dict(rejected),
        )
