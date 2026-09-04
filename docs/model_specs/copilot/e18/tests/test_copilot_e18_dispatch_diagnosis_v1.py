from agricola.strategy.copilot.e18_dispatch_diagnosis_v1 import (
    CopilotE18DispatchDiagnosisV1Policy,
    load_copilot_e18_dispatch_diagnosis_v1_config,
)

CONFIG = load_copilot_e18_dispatch_diagnosis_v1_config()


def _observation(day=0, step=0, money=420.0, hands=0, tiles=None):
    tiles = tiles or [[{"kind": "EMPTY", "crop": "WHEAT", "watered_today": False} for _ in range(3)] for _ in range(3)]
    return {
        "step": step,
        "day": day,
        "hour": 0,
        "player": 0,
        "farms": [{
            "money": money,
            "hands": [],
            "tiles": tiles,
            "farmer": [1, 1],
            "worker_count": hands,
        }],
        "private": {"cash": money, "inventory": {"wheat": 0}},
        "market": {"catalog": []},
    }


def test_hire_gate_trigger_when_hands_are_empty():
    policy = CopilotE18DispatchDiagnosisV1Policy(config=CONFIG)
    action = policy(_observation(day=1, step=24, money=420.0, hands=0))
    assert action["market"] == [["HIRE"]]
    assert action["farmer"] in (["PASS"], ["DIG"])


def test_smoke_run_produces_productive_activity():
    policy = CopilotE18DispatchDiagnosisV1Policy(config=CONFIG)
    productive_actions = 0
    peak_hands = 0
    money_trace = []
    for step in range(0, 720, 1):
        day = step // 24
        hour = step % 24
        farm = {
            "money": 420.0 + max(0, day - 1) * 120,
            "hands": [ [1, 1] ] if day > 1 else [],
            "tiles": [[{"kind": "EMPTY", "crop": "WHEAT", "watered_today": False} for _ in range(3)] for _ in range(3)],
            "farmer": [0, 0],
            "worker_count": 1 if day > 1 else 0,
        }
        obs = {
            "step": step,
            "day": day,
            "hour": hour,
            "player": 0,
            "farms": [farm],
            "private": {"cash": farm["money"], "inventory": {"wheat": 0}},
            "market": {"catalog": []},
        }
        action = policy(obs)
        money_trace.append(float(farm["money"]))
        if action["market"] or action["farmer"] != ["PASS"] or action["hands"]:
            productive_actions += 1
        peak_hands = max(peak_hands, len(farm["hands"]))
    assert productive_actions > 0
    assert peak_hands > 0
    assert max(money_trace) > 420.0
    assert policy.diagnostic_reason.startswith("root_cause=")


def test_diagnostic_reason_documents_hire_gap():
    policy = CopilotE18DispatchDiagnosisV1Policy(config=CONFIG)
    action = policy(_observation(day=2, step=48, money=480.0, hands=0, tiles=[[{"kind": "ALL"}]]) )
    assert "missing_hire_dispatch" in policy.diagnostic_reason
    assert action["market"] == [["HIRE"]]
