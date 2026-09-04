from agricola.strategy.copilot.e18_economic_recovery_v3 import (
    CopilotE18EconomicRecoveryV3Policy,
    load_copilot_e18_economic_recovery_v3_config,
)

CONFIG = load_copilot_e18_economic_recovery_v3_config()


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
        "market": {},
    }


def test_hire_gate_triggers_when_workforce_is_below_target():
    policy = CopilotE18EconomicRecoveryV3Policy(config=CONFIG)
    action = policy(_obs(money=10.0, hands=[], step=0, day=0))
    assert action["market"][0] == ["HIRE"] or action["market"][0][0] == "HIRE"


def test_policy_adds_seed_purchase_and_productive_tasking():
    policy = CopilotE18EconomicRecoveryV3Policy(config=CONFIG)
    action = policy(_obs(money=50.0, hands=[[2, 2]], step=24, day=1))
    assert action["market"] or action["farmer"] != ["PASS"] or action["hands"]


def test_policy_does_not_fall_back_to_pass_without_seed_budget():
    policy = CopilotE18EconomicRecoveryV3Policy(config=CONFIG)
    action = policy(_obs(money=40.0, hands=[], step=120, day=5,))
    assert action["market"] or action["farmer"] != ["PASS"]
