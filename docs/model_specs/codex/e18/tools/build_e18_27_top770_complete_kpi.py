"""Complete the D1-D30 population panels without changing the frozen cohorts."""

import hashlib
import json
import statistics
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]
DERIVED = BASE / "artifacts/derived"
CROPS = ("MELON", "WHEAT", "STRAWBERRY", "CARROT", "TOMATO")
ANIMALS = ("COW", "SHEEP", "GOOSE")
METRICS = (
    "money",
    "people",
    "crop_tiles",
    "occupied_livestock_tiles",
    "empty_pastures",
    "empty_coops",
    *CROPS,
    *ANIMALS,
)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coop_transitions(replay, seat):
    """Record actual COOP tile transitions and commands, without inferring intent."""
    events = []
    for index in range(1, len(replay["steps"])):
        before = replay["steps"][index - 1][seat]["observation"]
        entry = replay["steps"][index][seat]
        farm = before["farms"][seat]
        after = entry["observation"]["farms"][seat]
        action = entry.get("action") or {}
        commands = [action.get("farmer", ["PASS"]), *action.get("hands", [])]
        positions = [farm["farmer"], *farm["hands"]]
        for y, row in enumerate(farm["tiles"]):
            for x, old in enumerate(row):
                new = after["tiles"][y][x]
                old_kind = old.get("kind") if isinstance(old, dict) else old
                new_kind = new.get("kind") if isinstance(new, dict) else new
                if old_kind == new_kind or "COOP" not in (old_kind, new_kind):
                    continue
                events.append(
                    {
                        "day": before["day"] + 1,
                        "hour": before["hour"] + 1,
                        "recorded_step": index,
                        "tile_xy_zero_based": [x, y],
                        "before_kind": old_kind,
                        "after_kind": new_kind,
                        "commands_on_tile": [
                            {"worker": worker, "command": command}
                            for worker, (pos, command) in enumerate(
                                zip(positions, commands)
                            )
                            if pos == [x, y]
                        ],
                    }
                )
    return events


def flatten(row):
    assert set(row["crops"]) == set(CROPS)
    assert set(row["animals"]) == set(ANIMALS)
    assert sum(row["crops"].values()) == row["crop_tiles"]
    assert sum(row["animals"].values()) == row["occupied_livestock_tiles"]
    pasture = sum(row["pasture_topology"].values())
    empty_pastures = pasture - row["animals"]["COW"] - row["animals"]["SHEEP"]
    empty_coops = row["livestock_structures"] - pasture - row["animals"]["GOOSE"]
    assert empty_pastures >= 0 and empty_coops >= 0
    assert empty_pastures + empty_coops == row["empty_livestock_tiles"]
    return (
        row
        | row["crops"]
        | row["animals"]
        | {"empty_pastures": empty_pastures, "empty_coops": empty_coops}
    )


def main():
    top_path = DERIVED / "E18_26_JESSE_770_D01_D30_CLOSURE.json"
    local_path = DERIVED / "E18_27_D10_D15_DEVELOPMENT_V3.json"
    top = read(top_path)["jesse"]
    local = read(local_path)
    assert local["complete"]
    ours = [
        p
        for p in local["matches"]
        if p["version"] == "E18.27" and p["opponent"] == "E18.16"
    ]
    assert len(ours) == 14 and len(top) == 5
    series = {}
    for key, profiles in (("candidate", ours), ("top770", top)):
        assert all(len(p["daily"]) == 30 for p in profiles)
        flattened = [[flatten(row) for row in p["daily"]] for p in profiles]
        series[key] = {k: [] for k in METRICS}
        for day in range(30):
            for metric in METRICS:
                values = [p[day][metric] for p in flattened]
                series[key][metric].append(
                    [statistics.median(values), min(values), max(values)]
                )
    audit = []
    for profile in top:
        path = ROOT / f"data/replays/json/{profile['episode_id']}.json"
        assert sha(path) == profile["sha256"]
        replay = read(path)
        seat = profile["seat"]
        goose_max = tomato_max = goose_owned_max = 0
        for step in replay["steps"]:
            obs = step[seat]["observation"]
            tiles = [
                t
                for row in obs["farms"][seat]["tiles"]
                for t in row
                if isinstance(t, dict)
            ]
            goose_count = sum(t.get("animal") == "GOOSE" for t in tiles)
            goose_max = max(goose_max, goose_count)
            tomato_max = max(tomato_max, sum(t.get("crop") == "TOMATO" for t in tiles))
            private = obs["private"]
            goose_owned_max = max(
                goose_owned_max,
                goose_count
                + private["shed"].get("GOOSE", 0)
                + sum(inv.get("GOOSE", 0) for inv in private["inventories"]),
            )
        audit.append(
            {
                "episode_id": profile["episode_id"],
                "states_checked": len(replay["steps"]),
                "goose_placed_max": goose_max,
                "goose_owned_max": goose_owned_max,
                "tomato_tiles_max": tomato_max,
                "coop_transitions": coop_transitions(replay, seat),
            }
        )
        assert goose_max == tomato_max == goose_owned_max == 0
    for p in ours:
        assert all(
            r["animals"]["GOOSE"] == r["crops"]["TOMATO"] == 0 for r in p["daily"]
        )
        assert all(
            r["planted"].get("TOMATO", 0)
            == r["animal_placed"].get("GOOSE", 0)
            == r["bought_units"].get("BUY_ANIMAL:GOOSE", 0)
            == 0
            for r in p["ledger"]["daily"]
        )
    payload = {
        "analysis_id": "E18_27_TOP770_D01_D30_COMPLETE_KPI",
        "report_standard": "E18_AGENT_COMPARISON_REPORT_STANDARD_V1",
        "series": series,
        "cohorts": {
            "candidate": {
                "version": "E18.27 V3",
                "n": 14,
                "opponent": "E18.16",
                "seeds": sorted({p["seed"] for p in ours}),
                "seats": [0, 1],
            },
            "top770": {
                "n": 5,
                "episodes": [p["episode_id"] for p in top],
                "selection": "same frozen final-770 cohort",
            },
        },
        "aggregation": "pointwise median/min/max, observed range not confidence interval",
        "checkpoint": "H24, index 24*D-1; before last batch D1-D29; D30 terminal equals reward",
        "comparison": "descriptive; public and local seeds/opponents/prices differ",
        "added_panels": ["GOOSE", "TOMATO", "occupied_livestock_tiles", "empty_coops"],
        "coverage": {
            "crops": CROPS,
            "animals": ANIMALS,
            "goose_tomato_full_public_state_audit": audit,
            "local_zero_species_validated_against_daily_states_and_executed_ledgers": True,
        },
        "source_hashes": {
            top_path.name: sha(top_path),
            local_path.name: sha(local_path),
        },
    }
    output = DERIVED / "E18_27_TOP770_D01_D30_COMPLETE_KPI.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output),
                "audit": audit,
                "cow_first10": {
                    k: [d[0] for d in v["COW"][:10]] for k, v in series.items()
                },
            }
        )
    )


if __name__ == "__main__":
    main()
