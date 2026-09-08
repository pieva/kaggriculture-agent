"""Independent arithmetic and installed-engine checks for price scenarios."""
import importlib

from docs.model_specs.codex.e18.tools.e18_33_portfolio import (
    SHOPS, demand_between, portfolio_revenue, marginal_crop_revenue,
)


def test_observed_duplicate_shops_match_engine_rules():
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    assert SHOPS == engine.SHOPS
    assert demand_between('CARROT', ['PET_CAFE', 'PET_CAFE'], 0, 24) == 25
    assert demand_between('WHEAT', ['BAKERY', 'PIZZA_SHOP'], 5, 13) == 4
    assert demand_between('FERTILIZER', [], 0, 24) == 0


def test_adding_output_accounts_for_cannibalization_of_existing_sales():
    args = dict(inventory=0, quote=lambda item, n: max(1, 10-n), historical_low=10,
                shops=[], current_step=0, center_interval=10000)
    # Baseline two later units: 10+9. One added earlier unit displaces their
    # prices: 10+9+8. Marginal value is eight, not the initial quote of ten.
    assert marginal_crop_revenue('CARROT', {2: 2}, [(1, 1)], **args) == (8, 8)


def test_demand_changes_only_after_observed_consumption_steps():
    args = dict(inventory=0, quote=lambda item, n: max(1, 10-n), historical_low=100,
                shops=[], current_step=0)
    assert portfolio_revenue('CARROT', {0: 2, 1: 1}, **args) == (28, 28)


def test_floor_sales_do_not_add_inventory_and_prudent_is_separate():
    seen = []
    def quote(item, inventory):
        seen.append(inventory)
        return 1
    assert portfolio_revenue('CARROT', {0: 3}, 20, quote, 10, [], 0) == (3, 3)
    assert seen == [20, 20, 20]
    assert portfolio_revenue('CARROT', {0: 2}, 0, lambda item, n: 20, 5, [], 0) == (40, 10)
