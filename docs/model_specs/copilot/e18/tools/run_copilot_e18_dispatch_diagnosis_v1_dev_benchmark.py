from __future__ import annotations

import csv
import json
from pathlib import Path

from agricola.strategy.copilot.e18_dispatch_diagnosis_v1 import (
    CopilotE18DispatchDiagnosisV1Policy,
    load_copilot_e18_dispatch_diagnosis_v1_config,
)

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT / "artifacts" / "derived"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def build_observation(step: int, money: float, hands: int, tiles: int = 3):
    board = [[{"kind": "EMPTY", "crop": "WHEAT", "watered_today": False} for _ in range(tiles)] for _ in range(tiles)]
    return {
        "step": step,
        "day": step // 24,
        "hour": step % 24,
        "player": 0,
        "farms": [{
            "money": money,
            "hands": [[1, 1]] if hands > 0 else [],
            "tiles": board,
            "farmer": [0, 0],
            "worker_count": hands,
        }],
        "private": {"cash": money, "inventory": {"wheat": 0}},
        "market": {"catalog": []},
    }


def main() -> None:
    config = load_copilot_e18_dispatch_diagnosis_v1_config()
    policy = CopilotE18DispatchDiagnosisV1Policy(config=config)
    rows = []
    for step in range(0, 720, 24):
        hands = 0 if step < 24 else 1
        money = 420.0 + (step // 24) * 120.0
        obs = build_observation(step, money, hands, tiles=3)
        action = policy(obs)
        rows.append(
            {
                "step": step,
                "day": step // 24,
                "money": money,
                "hands": hands,
                "market_action": action["market"],
                "farmer_action": action["farmer"],
                "productive": bool(action["market"] or action["farmer"] != ["PASS"] or action["hands"]),
                "diagnosis": policy.diagnostic_reason,
            }
        )
    payload = {
        "candidate_id": config.candidate_id,
        "version": config.model_spec_version,
        "samples": rows,
        "summary": {
            "positive_market_actions": sum(1 for r in rows if r["market_action"]),
            "productive_turns": sum(1 for r in rows if r["productive"]),
            "average_money": round(sum(r["money"] for r in rows) / len(rows), 2),
            "peak_hands": 1,
        },
    }
    config_file = ARTIFACT_DIR / "E18_COPILOT_DISPATCH_DIAGNOSIS_V1_DEVELOPMENT_FIXTURES.json"
    csv_file = ARTIFACT_DIR / "E18_COPILOT_DISPATCH_DIAGNOSIS_V1_DEVELOPMENT_FIXTURES.csv"
    config_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    with csv_file.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["step", "day", "money", "hands", "market_action", "farmer_action", "productive", "diagnosis"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {config_file}")
    print(f"Wrote {csv_file}")


if __name__ == "__main__":
    main()
