from agricola.strategy.copilot.e18_economic_recovery_v1 import (
    CopilotE18EconomicRecoveryV1Policy,
    load_copilot_e18_economic_recovery_v1_config,
)

CONFIG = load_copilot_e18_economic_recovery_v1_config()


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
        }],
        "private": {"cash": money, "inventory": {"WHEAT": 4}},
        "market": {},
    }


def test_hire_gate_triggers_on_empty_workforce():
    policy = CopilotE18EconomicRecoveryV1Policy(config=CONFIG)
    action = policy(_obs(money=10.0, hands=[], step=0, day=0))
    assert action["market"] == [["HIRE"]]


def test_policy_produces_real_productive_actions_on_open_tiles():
    policy = CopilotE18EconomicRecoveryV1Policy(config=CONFIG)
    action = policy(_obs(money=50.0, hands=[[2, 2]], step=24, day=1))
    assert action["farmer"] != ["PASS"] or action["hands"]
