from __future__ import annotations

from collections import Counter

from docs.model_specs.codex.e18.tools.e18_21_wheat_obligation_ledger_controller import (
    WheatObligationLedgerController,
)


def test_selected_defaults_enable_only_inflight_guard() -> None:
    assert WheatObligationLedgerController.protect_inflight_pickups is True
    assert WheatObligationLedgerController.protect_procurement_contracts is False


def test_reduce_wheat_sales_preserves_other_orders() -> None:
    orders = [
        ["SELL", "MILK", 4],
        ["SELL", "WHEAT", 9],
        ["HIRE"],
        ["BUY_SEED", "CARROT", 2],
    ]

    adjusted, protected = WheatObligationLedgerController._reduce_wheat_sales(
        orders, reserve=5
    )

    assert adjusted == [
        ["SELL", "MILK", 4],
        ["SELL", "WHEAT", 4],
        ["HIRE"],
        ["BUY_SEED", "CARROT", 2],
    ]
    assert protected == 5


def test_contract_allocation_is_worker_specific_and_capped() -> None:
    controller = object.__new__(WheatObligationLedgerController)
    controller.wheat_contracts = Counter({(18, 2): 1})

    allocated = controller._allocate_contracts(
        18, Counter({2: 3, 5: 4}), units=10
    )

    assert allocated == 6
    assert controller.wheat_contracts == Counter({(18, 2): 3, (18, 5): 4})


def test_contracts_release_when_parent_reserve_takes_over() -> None:
    controller = object.__new__(WheatObligationLedgerController)
    controller.wheat_contracts = Counter(
        {(12, 1): 2, (13, 4): 3, (14, 7): 4}
    )

    released = controller._release_near_contracts(day=12)

    assert released == 5
    assert controller.wheat_contracts == Counter({(14, 7): 4})
