"""Chronological marginal crop revenue using only observed town demand.

No future shop draws or opponent orders are assumed. Cashflows are valuation
scenarios, never a source of spendable cash for the execution controller.
"""
from collections import Counter

SHOPS = {
    'BAKERY': ['EGG', 'WHEAT'],
    'PIZZA_SHOP': ['MILK', 'TOMATO', 'WHEAT'],
    'BRUNCH_SPOT': ['EGG', 'WHEAT', 'STRAWBERRY'],
    'YARN_STORE': ['WOOL'],
    'ICE_CREAM_SHOP': ['STRAWBERRY', 'MILK', 'WHEAT'],
    'PET_CAFE': ['CARROT'],
    'SMOOTHIE_SHOP': ['STRAWBERRY', 'MILK'],
    'FARMERS_MARKET': ['WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY'],
}


def demand_between(item, shops, start, stop, shop_interval=4, center_interval=24):
    """Consumption at refresh steps start < step <= stop, including duplicates."""
    shop_units = sum((2 if len(SHOPS[s]) == 1 else 1)
                     for s in shops if item in SHOPS[s])
    return (stop // shop_interval - start // shop_interval) * shop_units + (
        (stop // center_interval - start // center_interval) if item != 'FERTILIZER' else 0)


def portfolio_revenue(item, flows, inventory, quote, historical_low, shops,
                      current_step, turns=24, shop_interval=4, center_interval=24):
    """Engine unit pricing and floor inventory semantics in two scenarios."""
    neutral = prudent = 0
    previous = current_step
    for day, quantity in sorted(flows.items()):
        step = max(current_step, day * turns)
        inventory -= demand_between(item, shops, previous, step, shop_interval, center_interval)
        previous = step
        for _ in range(quantity):
            price = quote(item, inventory)
            neutral += price
            prudent += min(price, historical_low)
            if price > 1:
                inventory += 1
    return neutral, prudent


def marginal_crop_revenue(item, committed, candidate, **kwargs):
    before = portfolio_revenue(item, committed, **kwargs)
    after_flows = Counter(committed)
    after_flows.update(dict(candidate))
    after = portfolio_revenue(item, after_flows, **kwargs)
    return tuple(a-b for a, b in zip(after, before))
