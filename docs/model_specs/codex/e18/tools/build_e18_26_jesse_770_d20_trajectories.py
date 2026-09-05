"""Reproducible daily composition comparison; no policy or gate mutation."""

from __future__ import annotations

import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
BASE = ROOT / "docs/model_specs/codex/e18"
OUTPUT = BASE / "artifacts/derived/E18_26_JESSE_770_D01_D20_TRAJECTORIES.json"
REPORT = BASE / "reports/E18_26_TOP770_D01_D20_TRAJECTORIES_IT.md"
EPISODES = (105405557, 105384058, 105398563, 105391568, 105565293)
CROPS = ("MELON", "WHEAT", "STRAWBERRY", "CARROT", "TOMATO")
ANIMALS = ("COW", "SHEEP", "GOOSE")
SEED = 180903001


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(replay, day, seat):
    index = day * 24 - 1
    observation = replay["steps"][index][seat]["observation"]
    assert replay["steps"][index][0]["observation"]["step"] == index
    assert observation["day"] == day - 1
    farm = observation["farms"][seat]
    tiles = [(x, y, tile) for y, row in enumerate(farm["tiles"]) for x, tile in enumerate(row) if isinstance(tile, dict)]
    crops = Counter(tile["crop"] for _, _, tile in tiles if tile.get("kind") == "PLANT")
    animals = Counter(tile["animal"] for _, _, tile in tiles if tile.get("animal"))
    topology = Counter(f"Q{int(x >= 5) + 2 * int(y >= 5)}" for x, y, tile in tiles if tile.get("kind") == "PASTURE")
    structures = sum(tile.get("kind") in ("PASTURE", "COOP") for _, _, tile in tiles)
    hands = len(farm.get("hands", []))
    unlocked = 25 * len(farm["unlocked_quadrants"])
    assert sum(animals.values()) <= structures
    assert sum(crops.values()) + structures <= unlocked
    return {
        "day": day, "step_index": index, "hands": hands, "farmer": 1,
        "people": hands + 1, "money": farm["money"],
        "crops": {crop: crops[crop] for crop in CROPS},
        "animals": {animal: animals[animal] for animal in ANIMALS},
        "crop_tiles": sum(crops.values()), "occupied_livestock_tiles": sum(animals.values()),
        "livestock_structures": structures, "empty_livestock_tiles": structures - sum(animals.values()),
        "unlocked_tiles": unlocked, "other_tiles": unlocked - structures - sum(crops.values()),
        "pasture_topology": {f"Q{i}": topology[f"Q{i}"] for i in range(4)},
    }


def flat(row):
    return {"people": row["people"], "hands": row["hands"], "crop_tiles": row["crop_tiles"],
            "empty_livestock_tiles": row["empty_livestock_tiles"], "livestock_structures": row["livestock_structures"],
            **row["crops"], **row["animals"]}


def aggregate(profiles):
    output = []
    for day in range(1, 21):
        values = [flat(profile["daily"][day - 1]) for profile in profiles]
        output.append({"day": day, "metrics": {
            metric: {"median": statistics.median(row[metric] for row in values),
                     "min": min(row[metric] for row in values), "max": max(row[metric] for row in values)}
            for metric in values[0]}})
    return output


def main():
    from kaggle_environments import make
    from docs.model_specs.codex.e18.tools.e18_26_jesse_boost_d10_controller import JesseBoostD10Controller
    from docs.model_specs.codex.e18.tools.run_e18_26_770_jesse_boost_d10_gate import _incumbent

    jesse = []
    old = json.loads((BASE / "artifacts/derived/E18_18_770_COMPOSITION_COMPARISON_2026_09_04.json").read_text())
    for episode in EPISODES:
        path = ROOT / f"data/replays/json/{episode}.json"
        replay = json.loads(path.read_text(encoding="utf-8"))
        assert replay["info"]["EpisodeId"] == episode
        assert len(replay["steps"]) == 720
        assert all(record["status"] == "DONE" for record in replay["steps"][-1])
        seat = next(i for i, entry in enumerate(replay["info"]["Agents"]) if entry["Name"] == "Jesse Bullard")
        final = snapshot(replay, 30, seat)
        assert final["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0, "Q3": 0}
        daily = [snapshot(replay, day, seat) for day in range(1, 21)]
        for day in (1, 5, 10, 15, 20):
            ref = old["daily_comparison"][f"D{day:02d}"]
            assert {k: v for k, v in daily[day - 1]["crops"].items() if v} in ref["jesse_crop_variants"]
            assert {k: v for k, v in daily[day - 1]["animals"].items() if v} in ref["jesse_animal_variants"]
        jesse.append({"episode_id": episode, "seat": seat, "seed": replay["info"].get("seed"),
                      "opponent": replay["info"]["Agents"][1-seat]["Name"], "sha256": digest(path),
                      "url": f"https://www.kaggle.com/competitions/episodes/{episode}/replay.json", "daily": daily})
        print(f"Jesse {episode}: 20 daily checkpoints verified", flush=True)

    plan_path = BASE / "artifacts/derived/E18_26_770_JESSE_BOOST_D10_PLAN_V1.json"
    gate_path = BASE / "artifacts/derived/E18_26_770_JESSE_BOOST_D10_GATE_V1.json"
    plan = json.loads(plan_path.read_text())
    gate = json.loads(gate_path.read_text())
    frozen_matches = next(value["matches"] for value in gate.values()
                          if isinstance(value, dict) and value.get("matches") and value["matches"][0]["opponent"] == "E18.16")
    codex = []
    for seat in (0, 1):
        candidate = JesseBoostD10Controller(plan, seat=seat)
        opponent = _incumbent({}, 1-seat)
        policies = [candidate, opponent] if seat == 0 else [opponent, candidate]
        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": SEED, "turnsPerDay": 24}, debug=False)
        env.run(policies)
        candidate.finalize_metrics()
        replay = env.toJSON()
        assert all(record["status"] == "DONE" for record in replay["steps"][-1])
        assert candidate.error_count == 0
        daily = [snapshot(replay, day, seat) for day in range(1, 21)]
        frozen = next(row for row in frozen_matches if row["candidate_seat"] == seat)
        assert replay["rewards"][seat] == frozen["candidate_reward"], (replay["rewards"], frozen["candidate_reward"])
        for label, reference in frozen["candidate_snapshots"].items():
            row = snapshot(replay, int(label[1:]), seat)
            for field in ("money", "hands"):
                assert row[field] == reference[field], (seat, label, field)
            for field in ("crops", "animals"):
                assert {k: v for k, v in row[field].items() if v} == reference[field], (seat, label, field)
        assert snapshot(replay, 30, seat)["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0, "Q3": 0}
        codex.append({"version": "E18.26 BoostD10", "seat": seat, "seed": SEED, "opponent": "E18.16",
                      "reward": replay["rewards"][seat], "matches_frozen_gate": True,
                      "daily": daily})
        print(f"E18.26 seat {seat}: daily series and frozen gate parity verified ({replay['rewards'][seat]})", flush=True)

    payload = {"schema_version": 1, "analysis_id": OUTPUT.stem, "observed_at": "2026-09-05",
        "methodology": {
            "sample": "D1-D20 at H24: replay step 24*day-1, observation.day=day-1; same sampling for both cohorts, no interpolation of missing days.",
            "people": "len(farm.hands)+1 farmer; all employed hands, including positions outside the grid. This is not a count of visible avatars.",
            "crop_tiles": "Tile kind PLANT grouped by crop, irrespective of maturity; not seeds or harvested units.",
            "animal_tiles": "Occupied tile grouped by animal; unoccupied livestock structures counted separately, never attributed to a species.",
            "cohort": "Five historical Jesse final-7-7-0 replays; current episode 105717134 excluded. Two E18.26 seats against incumbent E18.16 on development seed 180903001.",
            "bands": "Median and observed min-max, not confidence intervals; cohorts have different seeds, markets and opponents.",
            "checks": "Raw identity, terminal status, topology, historical checkpoints and frozen E18.26 gate parity verified."},
        "sources": {"plan": str(plan_path.relative_to(ROOT)), "plan_sha256": digest(plan_path),
                    "frozen_gate": str(gate_path.relative_to(ROOT)), "frozen_gate_sha256": digest(gate_path)},
        "jesse": jesse, "codex": codex, "aggregates": {"jesse": aggregate(jesse), "codex": aggregate(codex)},
        "planned_daily": [{"day": row["day"], "hands": row["planned_hands"], "people": row["active_units"],
                           "crops": row["crop_mix_end_of_actions"], "animals": row["animal_mix_end_of_actions"]}
                          for row in plan["daily"] if row["day"] <= 20]}
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = ["# E18.26 e Jesse 7-7-0 — traiettorie D1-D20", "",
             "Esecuzione effettiva E18.26 BoostD10 contro E18.16, seed development 180903001, entrambi i seat. Riferimento: cinque replay Jesse con topologia finale 7-7-0.", "",
             "Campionamento uniforme H24: step 24 × giorno − 1. Persone = hands assunti + farmer, anche fuori griglia. Colture = tile PLANT; specie allevate = tile occupate. Le strutture vuote sono separate. Mediana e range osservato non sono intervalli di confidenza né prova causale.", "",
             "Replay Jesse: " + ", ".join(map(str, EPISODES)) + ". La variante 105717134 è esclusa.", "",
             "| Giorno | Persone noi / Jesse | Melon | Wheat | Strawberry | Carrot | Tomato | Cow | Sheep | Goose | Strutture vuote |",
             "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    metrics = ("people", *CROPS, *ANIMALS, "empty_livestock_tiles")
    for day in range(20):
        def fmt(value):
            return f"{value['median']:g}" if value["min"] == value["max"] else f"{value['median']:g} [{value['min']:g}–{value['max']:g}]"
        pairs = [fmt(payload["aggregates"]["codex"][day]["metrics"][metric]) + " / " + fmt(payload["aggregates"]["jesse"][day]["metrics"][metric]) for metric in metrics]
        lines.append(f"| D{day+1} | " + " | ".join(pairs) + " |")
    lines.extend(["", "## Lettura diagnostica", "",
        "Le serie mostrate sono identiche nei cinque replay Jesse e nei due seat E18.26: mediana, minimo e massimo coincidono per tutte le metriche di consistenza D1-D20. Questo non implica uguale economia né generalizzazione a nuovi scenari.", "",
        "- D6-D9: il recupero del checkpoint D10 nasconde un ritardo precedente. A D7 abbiamo 7 Strawberry contro 12; a D9 soltanto 6 animali contro 13. A D10 persone, mix crop e animali coincidono.",
        "- D11-D12: E18.26 scende a 9 persone mentre Jesse resta a 12. Jesse ritira tutti i Melon entro H24 D11, E18.26 entro H24 D13. Le 38 Strawberry Jesse sono presenti da D12; noi restiamo a 29.",
        "- D14: i checkpoint mostrano 13→9 animali, mentre Jesse sale a 14. Il successivo audit D30 per turno corregge la prima interpretazione: scappano cinque animali al cambio di D14 (13→8), poi una Sheep già prevista viene piazzata durante D14 (8→9). A D20 persistono 6 Cow + 3 Sheep contro 9 Cow + 5 Sheep, con 5 pascoli vuoti. La diagnosi è documentata in `E18_26_TOP770_D01_D30_CLOSURE_IT.md`.",
        "- D15-D20: Wheat coincide a 23 tile. L'intero gap di 9 crop tile (52 contro 61) riguarda Strawberry. Da D16 la workforce coincide a 13 persone, quindi il semplice aumento finale di personale non ha recuperato la capacità produttiva persa.", "",
        "## Precisione sulla topologia", "",
        "La selezione Jesse è per topologia finale 7-7-0, come nel benchmark precedente. Durante l'esecuzione i replay presentano 15 strutture pasture a D11-D12 e 16 a D14, tornando a 14 da D15. Sono costruzioni transitorie con posti vuoti, non un plateau alternativo da importare nel target Codex. Il vincolo Codex resta 14 pascoli 7-7-0. Non si può quindi interpretare l'intera traiettoria strutturale Jesse come un'esecuzione con cap 14 rigoroso a ogni turno.", "",
        "Verifica: entrambe le esecuzioni E18.26 coincidono con reward e checkpoint del gate congelato. Tutti i checkpoint Jesse D1/D5/D10/D15/D20 coincidono con il benchmark storico. Nessuna policy modificata.", "", f"Dataset completo: `{OUTPUT.relative_to(ROOT).as_posix()}`.", ""])
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT, flush=True)
    print("Daily composition dataset and report saved.", flush=True)


if __name__ == "__main__":
    main()
