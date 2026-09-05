from __future__ import annotations

from docs.model_specs.codex.e18.tools.e18_20_wheat_market_netting_controller import (
    WheatMarketNettingController,
)


def test_extra_horizon_reserve_is_applied_before_same_batch_netting() -> None:
    orders = [
        ["SELL", "WHEAT", 12],
        ["HIRE"],
        ["BUY_PRODUCT", "WHEAT", 7],
        ["SELL", "MILK", 4],
    ]

    adjusted, metrics = WheatMarketNettingController._net_wheat_orders(
        orders, extra_reserve=3
    )

    assert adjusted == [
        ["SELL", "WHEAT", 2],
        ["HIRE"],
        ["SELL", "MILK", 4],
    ]
    assert metrics == {
        "reserved_sell_units": 3,
        "netted_round_trip_units": 7,
    }


def test_non_wheat_orders_are_unchanged() -> None:
    orders = [["SELL", "MILK", 6], ["BUY_SEED", "WHEAT", 4], ["HIRE"]]

    adjusted, metrics = WheatMarketNettingController._net_wheat_orders(
        orders, extra_reserve=10
    )

    assert adjusted == orders
    assert metrics == {
        "reserved_sell_units": 0,
        "netted_round_trip_units": 0,
    }
