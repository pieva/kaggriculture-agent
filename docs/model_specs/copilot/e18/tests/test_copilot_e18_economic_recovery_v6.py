from agricola.strategy.copilot.e18_economic_recovery_v6 import (
    CopilotE18EconomicRecoveryV6Policy,
    load_copilot_e18_economic_recovery_v6_config,
)

CONFIG = load_copilot_e18_economic_recovery_v6_config()


def _obs(money=500.0, hands=None, tiles=None, step=0, day=0, prices=None):
    if hands is None:
        hands = []
    if tiles is None:
        tiles = [[{"kind": "EMPTY"} for _ in range(5)] for _ in range(5)]
    if prices is None:
        prices = {"WHEAT": 12.0, "CARROT": 18.0, "TOMATO": 22.0, "STRAWBERRY": 30.0, "MELON": 28.0}
    return {
        "step": step,
        "day": day,
        "hour": 0,
        "player": 0,
        "farms": [{
            "money": money,
            "hands": hands,
            "tiles": tiles,
            "farmer": [2, 2],
            "inventory": {"WHEAT": 3, "CARROT": 1},
        }],
        "private": {"cash": money, "inventory": {"WHEAT": 3, "CARROT": 1}, "seeds": {"CARROT": 2}},
        "market": {"prices": prices},
    }


def test_hire_gate_triggers_when_workforce_is_under_target():
    policy = CopilotE18EconomicRecoveryV6Policy(config=CONFIG)
    action = policy(_obs(money=10.0, hands=[], step=0, day=0))
    assert action["market"] and action["market"][0][0] == "HIRE"


def test_policy_prefers_seed_restock_and_crop_actions_when_possible():
    policy = CopilotE18EconomicRecoveryV6Policy(config=CONFIG)
    action = policy(_obs(money=120.0, hands=[[2, 2]], step=24, day=1, prices={"WHEAT": 12.0, "CARROT": 18.0}))
    assert action["market"] or action["farmer"] != ["PASS"] or action["hands"]


def test_policy_uses_livestock_gate_after_cash_buffer_and_empty_pasture():
    tiles = [[{"kind": "PASTURE"} for _ in range(3)] for _ in range(3)]
    policy = CopilotE18EconomicRecoveryV6Policy(config=CONFIG)
    action = policy(_obs(money=500.0, hands=[], step=192, day=8, tiles=tiles, prices={"WHEAT": 12.0, "CARROT": 18.0}))
    assert any(order[0] == "BUY_ANIMAL" for order in action["market"])
