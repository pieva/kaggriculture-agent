"""Explain phase asymmetry from frozen runs and plan, without new simulations."""

import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean

BASE = Path(__file__).resolve().parents[1]
DERIVED = BASE / "artifacts/derived"


def build():
    sources = {}

    def read(name):
        path = DERIVED / name
        sources[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        data = json.loads(path.read_text(encoding="utf-8"))
        if "matches" in data:
            assert data["complete"] and not data["failures"]
        return data

    candidates = [
        p
        for part in ("CROP_STRESS", "CROP_DEVELOPMENT")
        for p in read(f"E18_30_MISSION_GATE_{part}_V2_20260906.json")["matches"]
    ]
    parents = [
        p
        for part in ("SMOKE", "DEVELOPMENT")
        for p in read(f"E18_30_MISSION_GATE_{part}_V1_20260906.json")["matches"]
        if p["variant"] == "PARENT" and p["opponent"] == "E18.16"
    ]
    top = read("E18_26_JESSE_770_D01_D30_CLOSURE.json")["jesse"]
    plan = read("E18_28_FULL_SEASON_C_PLAN_V1.json")
    assert len(candidates) == len(parents) == 14 and len(top) == 5
    assert all(
        p["variant"] == "CROP_POOL" and p["opponent"] == "E18.16" for p in candidates
    )
    assert {(p["seed"], p["seat"]) for p in candidates} == {
        (p["seed"], p["seat"]) for p in parents
    }
    windows = {}
    for first, last in ((1, 6), (7, 11), (1, 14), (15, 30), (1, 15), (16, 30)):
        values = {
            name: mean(
                sum(
                    d["requested_actions"].get("PASS", 0)
                    for d in p["ledger"]["daily"][first - 1 : last]
                )
                for p in profiles
            )
            for name, profiles in (
                ("parent", parents),
                ("candidate", candidates),
                ("top770", top),
            )
        }
        values["reduction_vs_parent_pct"] = 100 * (
            1 - values["candidate"] / values["parent"]
        )
        windows[f"D{first}-D{last}"] = values
    daily = []
    for day in range(1, 31):
        counts = Counter(r["opcode"] for r in plan["trajectory"] if r["day"] == day)
        daily.append(
            {
                "day": day,
                "candidate_pass_mean": mean(
                    p["action_daily"][day - 1].get("PASS", 0) for p in candidates
                ),
                "parent_pass_mean": mean(
                    p["action_daily"][day - 1].get("PASS", 0) for p in parents
                ),
                "pool_missions_started_mean": mean(
                    p["runtime_daily"].get(str(day), {}).get("missions_started", 0)
                    for p in candidates
                ),
                "pool_fertilizer_ack_mean": mean(
                    p["runtime_daily"]
                    .get(str(day), {})
                    .get("ack_COLLECT_FERTILIZER", 0)
                    for p in candidates
                ),
                "pool_crop_ack_mean": mean(
                    p["runtime_daily"].get(str(day), {}).get("ack_PLANT_WATER", 0)
                    for p in candidates
                ),
                "planned_collection_commands": counts["COLLECT_FERTILIZER"],
            }
        )
    config = plan["treatment_config"]
    rules = {
        k: config[k]
        for k in (
            "fertilizer_collection_caps_by_day",
            "animal_care_blackout_days",
            "force_peak_hands_from_day",
            "force_peak_hands_through_day",
            "workers_peak_hands",
        )
    }
    assert all(d["pool_missions_started_mean"] == 0 for d in daily[:11])
    assert all(d["candidate_pass_mean"] == d["parent_pass_mean"] for d in daily[:11])
    for name in (
        "e18_30_mission_runtime.py",
        "e18_19_retrying_trajectory_controller.py",
        "e18_18_capacity_trajectory_planner.py",
    ):
        sources["tools/" + name] = hashlib.sha256(
            (BASE / "tools" / name).read_bytes()
        ).hexdigest()
    return {
        "analysis_id": "E18_30_PASS_PHASE_DIAGNOSIS_20260906",
        "sources": sources,
        "windows": windows,
        "daily": daily,
        "legacy_calendar_rules": rules,
        "new_simulation": False,
        "policy_changed": False,
        "limitations": [
            "Top770 descriptive, not matched markets/opponents",
            "No quantified all-cause decomposition of V2 PASS from aggregate records",
            "V2 core has no D15 dispatcher switch; inherited plan has dated rules",
        ],
    }


if __name__ == "__main__":
    data = build()
    output = DERIVED / (data["analysis_id"] + ".json")
    assert not output.exists(), "Preserve previous diagnosis"
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output),
                "windows": data["windows"],
                "legacy_calendar_rules": data["legacy_calendar_rules"],
            },
            indent=2,
        )
    )
