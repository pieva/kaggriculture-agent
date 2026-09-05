"""Generic assignment failures; no Top770 or public replay/seed fitting."""

from dataclasses import replace
from random import Random

import pytest

from docs.model_specs.codex.e18.tools.e18_30_mission_dispatcher import (
    Mission,
    MissionDispatcher,
    RouteOffer,
    Status,
)


def pool(*missions):
    result = MissionDispatcher()
    for mission in missions:
        result.submit(mission)
    return result


def mission(key="water", **kwargs):
    return Mission(key, **({"not_before": 0, "deadline": 10, "value": 20} | kwargs))


def offer(key="water", worker=0, snapshot=0, **kwargs):
    return RouteOffer(key, worker, snapshot, **({"remaining_steps": 2} | kwargs))


def test_unconfirmed_hire_does_not_add_capacity():
    p = pool(mission())
    result = p.tick(0, [0, 1, 2, 3], [offer(worker=9)])
    assert result.assignments == {}
    assert result.rejected_offers == {"WORKER_ABSENT": 1}
    assert set(result.idle) == {0, 1, 2, 3}


def test_orphan_mission_reallocated_to_actual_worker():
    p = pool(mission())
    assert p.tick(0, [0, 9], [offer(worker=9)]).assignments == {9: "water"}
    assert p.tick(1, [0], [offer(snapshot=1)]).assignments == {0: "water"}
    assert p.records["water"].status == Status.ASSIGNED


def test_emitted_work_is_not_done_and_ack_releases_capacity():
    p = pool(mission(), mission("harvest", dependencies=frozenset({"water"})))
    assert p.tick(0, [0], [offer()]).assignments == {0: "water"}
    # No completion inference from time elapsed or empty legacy queue.
    assert p.tick(1, [0], []).assignments == {}
    assert p.records["water"].status == Status.READY
    assert p.tick(
        2, [0], [offer("harvest", snapshot=2)], confirmed={"water"}
    ).assignments == {0: "harvest"}
    assert p.records["water"].status == Status.DONE


def test_dependencies_require_observed_completion():
    p = pool(mission(), mission("harvest", dependencies=frozenset({"water"})))
    result = p.tick(0, [0, 1], [offer(), offer("harvest", 1)])
    assert result.assignments == {0: "water"}
    assert result.rejected_offers == {"DEPENDENCY_UNCONFIRMED": 1}


def test_fresh_revalidation_preserves_worker_without_thrashing():
    p = pool(mission(), mission("other", value=1000))
    p.tick(0, [0, 1], [offer()])
    result = p.tick(
        1,
        [0, 1],
        [offer(snapshot=1), offer(worker=1, snapshot=1), offer("other", 0, 1)],
    )
    assert result.assignments == {0: "water"}


def test_deduplication_and_different_semantics_rejected():
    m = mission()
    p = pool(m, m)
    assert len(p.records) == 1
    with pytest.raises(ValueError, match="Conflicting"):
        p.submit(replace(m, value=21))
    result = p.tick(0, [0, 1], [offer(), offer(worker=1)])
    assert len(result.assignments) == 1


def test_capacity_claims_prevent_double_spend_and_double_tile_service():
    p = pool(mission("feed"), mission("plant"))
    claims = (("shed:WHEAT", 2), ("tile:2,1", 1))
    result = p.tick(
        0,
        [0, 1],
        [offer("feed", claims=claims), offer("plant", 1, claims=claims)],
        capacities={"shed:WHEAT": 3, "tile:2,1": 1},
    )
    assert len(result.assignments) == 1
    assert result.reserved == {"shed:WHEAT": 2, "tile:2,1": 1}
    assert result.rejected_offers == {"RESOURCE_CAPACITY": 1}


def test_consumed_stock_is_not_reserved_twice_on_next_observation():
    p = pool(mission(), mission("other"))
    p.tick(0, [0], [offer(claims=(("stock", 2),))], capacities={"stock": 2})
    result = p.tick(
        1,
        [0, 1],
        [offer(snapshot=1, claims=()), offer("other", 1, 1, claims=(("stock", 1),))],
        capacities={"stock": 1},
    )
    assert len(result.assignments) == 2
    assert result.reserved == {"stock": 1}


def test_complete_delivery_deadline_not_just_arrival():
    p = pool(mission(deadline=2))
    assert p.tick(0, [0], [offer(remaining_steps=4)]).assignments == {}
    assert p.records["water"].reason == "COMPLETE_ROUTE_MISSES_DEADLINE"
    assert p.tick(1, [0], [offer(snapshot=1, remaining_steps=2)]).assignments == {
        0: "water"
    }


def test_expiration_and_invalidation_release_claims():
    p = pool(mission(deadline=0), mission("cancel"), mission("new"))
    p.tick(0, [0], [offer(remaining_steps=1)])
    result = p.tick(1, [0], [offer("new", snapshot=1)], invalidated={"cancel"})
    assert p.records["water"].status == Status.EXPIRED
    assert p.records["cancel"].status == Status.CANCELLED
    assert result.assignments == {0: "new"}


def test_stale_routes_or_missing_prerequisites_fail_closed():
    p = pool(mission(), mission("later", not_before=5), mission("blocked"))
    result = p.tick(
        1,
        [0, 1, 2],
        [
            offer(),
            offer("later", 1, 1),
            offer("blocked", 2, 1, prerequisites_met=False),
        ],
    )
    assert not result.assignments
    assert result.rejected_offers == {
        "STALE_OFFER": 1,
        "NOT_READY_YET": 1,
        "PREREQUISITE_BLOCKED": 1,
    }


def test_safety_before_discretionary_and_order_deterministic():
    missions = [mission("optional", value=999), mission("feed", safety=True)]
    offers = [offer("optional"), offer("feed")]
    a = pool(*missions).tick(0, [0], offers)
    b = pool(*reversed(missions)).tick(0, [0], reversed(offers))
    assert a == b
    assert a.assignments == {0: "feed"}


def test_blocked_active_work_returns_to_pool_without_losing_it():
    p = pool(mission())
    p.tick(0, [0], [offer()])
    assert not p.tick(1, [0], [offer(snapshot=1)], blocked={"water"}).assignments
    assert p.records["water"].status == Status.READY
    assert p.tick(2, [0], [offer(snapshot=2)]).assignments == {0: "water"}


@pytest.mark.parametrize(
    "kwargs",
    [
        {"remaining_steps": 0},
        {"remaining_steps": -1},
        {"claims": (("stock", -1),)},
        {"claims": (("stock", 1), ("stock", 1))},
    ],
)
def test_invalid_offers_rejected(kwargs):
    with pytest.raises(ValueError):
        offer(**kwargs)


def test_bad_event_does_not_partially_mutate_ledger():
    p = pool(mission())
    with pytest.raises(ValueError):
        p.tick(0, [0], [offer()], confirmed={"missing"})
    assert p.last_snapshot == -1
    assert p.records["water"].status == Status.READY
    assert p.tick(0, [0], [offer()]).assignments == {0: "water"}
    with pytest.raises(ValueError):
        p.tick(0, [0], [])


def test_unknown_resource_is_not_infinite_capacity():
    p = pool(mission())
    result = p.tick(0, [0], [offer(claims=(("shed_space", 1),))])
    assert result.rejected_offers == {"RESOURCE_CAPACITY": 1}


@pytest.mark.parametrize("roster", [[0, 0], list(range(14))])
def test_invalid_roster_fails_before_assignment(roster):
    p = pool(mission())
    with pytest.raises(ValueError):
        p.tick(0, roster, [offer()])
    assert p.last_snapshot == -1


def test_idle_workers_pull_distinct_work_from_one_shared_pool():
    p = pool(mission("a"), mission("b"), mission("c"))
    offers = [offer(key, worker) for key in ("a", "b", "c") for worker in (0, 4, 7)]
    result = p.tick(0, [0, 4, 7], offers)
    assert len(result.assignments) == 3
    assert set(result.assignments.values()) == {"a", "b", "c"}
    assert not result.idle


def test_retry_rebuilds_assignment_instead_of_replaying_old_worker_route():
    p = pool(mission())
    p.tick(0, [0, 2], [offer()])
    result = p.tick(
        1,
        [0, 2],
        [
            offer(snapshot=1, remaining_steps=5),
            offer(worker=2, snapshot=1, remaining_steps=2),
        ],
        retry={"water"},
    )
    assert result.assignments == {2: "water"}


def test_missing_fresh_offer_does_not_keep_old_stock_claim():
    p = pool(mission(), mission("other"))
    p.tick(0, [0, 1], [offer(claims=(("stock", 1),))], capacities={"stock": 1})
    result = p.tick(
        1,
        [0, 1],
        [offer("other", 1, 1, claims=(("stock", 1),))],
        capacities={"stock": 1},
    )
    assert result.assignments == {1: "other"}
    assert p.records["water"].reason == "REVALIDATION_MISSING"


def test_randomized_allocation_invariants_and_input_order():
    rng = Random(30)
    for _ in range(100):
        roster = list(range(rng.randint(1, 13)))
        missions = [
            mission(
                str(i),
                deadline=rng.randint(0, 23),
                value=rng.randint(0, 100),
                safety=bool(i % 2),
            )
            for i in range(10)
        ]
        offers = [
            offer(
                m.key,
                w,
                remaining_steps=rng.randint(1, 12),
                claims=(("stock", rng.randint(1, 3)),),
            )
            for m in missions
            for w in roster
            if rng.random() < 0.5
        ]
        capacity = rng.randint(0, 25)
        a = pool(*missions).tick(0, roster, offers, capacities={"stock": capacity})
        rng.shuffle(offers)
        b = pool(*reversed(missions)).tick(
            0, reversed(roster), offers, capacities={"stock": capacity}
        )
        assert a == b
        assert set(a.assignments) <= set(roster)
        assert len(a.assignments.values()) == len(set(a.assignments.values()))
        assert a.reserved.get("stock", 0) <= capacity
        for worker, key in a.assignments.items():
            route = next(o for o in offers if (o.worker, o.mission) == (worker, key))
            m = next(m for m in missions if m.key == key)
            assert route.remaining_steps - 1 <= m.deadline
