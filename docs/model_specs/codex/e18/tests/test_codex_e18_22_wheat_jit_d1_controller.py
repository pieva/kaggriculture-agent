from __future__ import annotations

from docs.model_specs.codex.e18.tools.e18_22_wheat_jit_d1_controller import (
    WheatJitD1Controller,
)


def test_cap_wheat_buys_preserves_order_and_unrelated_commands() -> None:
    orders = [
        ["SELL", "MILK", 5],
        ["BUY_PRODUCT", "WHEAT", 4],
        ["HIRE"],
        ["BUY_PRODUCT", "WHEAT", 3],
        ["BUY_SEED", "CARROT", 2],
    ]

    adjusted, removed = WheatJitD1Controller._cap_wheat_buys(orders, cap=5)

    assert adjusted == [
        ["SELL", "MILK", 5],
        ["BUY_PRODUCT", "WHEAT", 4],
        ["HIRE"],
        ["BUY_PRODUCT", "WHEAT", 1],
        ["BUY_SEED", "CARROT", 2],
    ]
    assert removed == 2


def test_zero_cap_removes_only_wheat_product_buys() -> None:
    orders = [
        ["BUY_PRODUCT", "WHEAT", 7],
        ["BUY_SEED", "WHEAT", 3],
        ["BUY_PRODUCT", "FERTILIZER", 2],
    ]

    adjusted, removed = WheatJitD1Controller._cap_wheat_buys(orders, cap=0)

    assert adjusted == [
        ["BUY_SEED", "WHEAT", 3],
        ["BUY_PRODUCT", "FERTILIZER", 2],
    ]
    assert removed == 7
