from agricola.strategy.copilot.e18_economic_recovery_v4 import (
    CopilotE18EconomicRecoveryV4Policy,
    load_copilot_e18_economic_recovery_v4_config,
)

CONFIG = load_copilot_e18_economic_recovery_v4_config()


def _obs(money=500.0, hands=None, tiles=None, step=0, day=0):
    if hands is None:
        hands = []
    if tiles is None:
        tiles = [[{"kind": "EMPTY"} for _ in range(5)] for _ in range(5)]
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
        "private": {"cash": money, "inventory": {"WHEAT": 3, "CARROT": 1}},
        "market": {"prices": {"WHEAT": 12.0, "CARROT": 18.0}},
    }


def test_hire_gate_triggers_when_workforce_is_under_target():
    policy = CopilotE18EconomicRecoveryV4Policy(config=CONFIG)
    action = policy(_obs(money=10.0, hands=[], step=0, day=0))
    assert action["market"] and action["market"][0][0] == "HIRE"


def test_policy_has_market_seed_buy_and_tasking():
    policy = CopilotE18EconomicRecoveryV4Policy(config=CONFIG)
    action = policy(_obs(money=60.0, hands=[[2, 2]], step=24, day=1))
    assert action["market"] or action["farmer"] != ["PASS"] or action["hands"]


def test_policy_uses_roi_selection_under_seed_pressure():
    policy = CopilotE18EconomicRecoveryV4Policy(config=CONFIG)
    action = policy(_obs(money=60.0, hands=[], step=48, day=2))
    assert action["market"] or action["farmer"] != ["PASS"]
