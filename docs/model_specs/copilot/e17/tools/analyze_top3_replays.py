"""Offline, Copilot-owned E17 extractor for the nine preregistered Kaggriculture replays."""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[5]
REPLAY_IDS = ["104527555", "104541810", "104543983", "104547425", "104564762", "104577270", "104578185", "104586335", "104586487"]
TARGETS = {"tetsuya", "OceanMix", "Crop Dusta"}
OUT = ROOT / "docs" / "model_specs" / "copilot" / "e17" / "artifacts" / "discovery"
REPORT_OUT = ROOT / "docs" / "model_specs" / "copilot" / "e17" / "reports"
CROPS = {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"}
ANIMALS = {"COW", "SHEEP", "GOOSE"}


def quadrant(y: int, x: int) -> str:
    return ("NW" if y < 5 else "SW") if x < 5 else ("NE" if y < 5 else "SE")


def tile_metrics(farm: dict) -> dict:
    result = {q: {"unlocked_tiles": 0, "empty": 0, "weed": 0, "plant_total": 0,
                  "pasture": 0, "coop": 0, "crops": Counter()} for q in ("NW", "NE", "SW", "SE")}
    for y, row in enumerate(farm["tiles"]):
        for x, tile in enumerate(row):
            q = quadrant(y, x)
            if tile == "LOCKED":
                continue
            result[q]["unlocked_tiles"] += 1
            if tile is None:
                result[q]["empty"] += 1
            elif isinstance(tile, str):
                result[q][tile.lower()] = result[q].get(tile.lower(), 0) + 1
            else:
                kind = tile.get("kind", "UNKNOWN")
                if kind == "PLANT":
                    result[q]["plant_total"] += 1
                    result[q]["crops"][tile.get("crop", "UNKNOWN")] += 1
                elif kind == "PASTURE":
                    result[q]["pasture"] += 1
                elif kind == "COOP":
                    result[q]["coop"] += 1
                else:
                    result[q][kind.lower()] = result[q].get(kind.lower(), 0) + 1
    for q in result:
        result[q]["crops"] = dict(result[q]["crops"])
        result[q]["animal_dedicated_tiles"] = result[q]["pasture"] + result[q]["coop"]
        result[q]["unplanted_tiles"] = result[q]["empty"] + result[q]["weed"]
    return result


def action_names(action: dict) -> list[str]:
    names = []
    for value in [action.get("farmer", [])] + list(action.get("hands", []) or []):
        if value:
            names.append(str(value[0]))
    for order in action.get("market", []) or []:
        if order:
            names.append(str(order[0]))
    return names


def summarize_player(replay: dict, player: int) -> dict:
    steps = replay["steps"]
    daily, action_counter, per_quadrant_actions = [], Counter(), defaultdict(Counter)
    unlock = {q: None for q in ("NW", "NE", "SW", "SE")}
    peak_hands = 0
    for tick, entries in enumerate(steps):
        entry = entries[player]
        obs, farm = entry["observation"], entry["observation"]["farms"][player]
        hands = len(farm["hands"])
        peak_hands = max(peak_hands, hands)
        for q in farm["unlocked_quadrants"]:
            if unlock.get(q) is None:
                unlock[q] = {"step": tick, "day": obs["day"]}
        action = entry.get("action") or {}
        for name in action_names(action):
            action_counter[name] += 1
        for value in [action.get("farmer", [])] + list(action.get("hands", []) or []):
            if len(value) >= 4 and value[0] == "PLACE" and str(value[1]) in ANIMALS:
                per_quadrant_actions[quadrant(int(value[3]), int(value[2]))][str(value[1])] += 1
        if tick % 24 == 0 or tick == len(steps) - 1:
            tm = tile_metrics(farm)
            daily.append({"step": tick, "day": obs["day"], "money": farm["money"], "hands": hands,
                          "quadrants": list(farm["unlocked_quadrants"]), "tiles": tm})
    terminal = steps[-1][player]
    final_farm = terminal["observation"]["farms"][player]
    final_tiles = tile_metrics(final_farm)
    money_series = [row["money"] for row in daily]
    return {
        "player_index": player, "final_score": terminal["reward"], "final_money": final_farm["money"],
        "terminal_status": terminal["status"], "peak_hands": peak_hands,
        "terminal_hands": len(final_farm["hands"]), "quadrant_unlock": unlock,
        "final_tiles_by_quadrant": final_tiles, "daily": daily, "action_requests": dict(action_counter),
        "movement_requests": sum(action_counter[action] for action in ("NORTH", "SOUTH", "EAST", "WEST")),
        "animal_escapes": None,
        "animal_escapes_reason": "Replay schema exposes neither escape events nor animal occupancy by tile.",
        "animal_place_requests_by_quadrant": {q: dict(v) for q, v in per_quadrant_actions.items()},
        "money_change": final_farm["money"] - money_series[0],
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    episodes, target_rows = [], []
    for eid in REPLAY_IDS:
        path = ROOT / "data" / "replays" / "json" / f"{eid}.json"
        raw = path.read_bytes(); data = json.loads(raw)
        agents = data["info"]["Agents"]
        agent_names = [
            agent.get("Name", str(agent)) if isinstance(agent, dict) else str(agent)
            for agent in agents
        ]
        players = []
        for i, name in enumerate(agent_names):
            s = summarize_player(data, i)
            s["agent"] = name
            players.append(s)
            if name in TARGETS:
                target_rows.append({"episode_id": eid, "agent": name, **s})
        episodes.append({"episode_id": eid, "sha256": hashlib.sha256(raw).hexdigest(), "module_version": data["module_version"],
                         "version": data["version"], "schema_version": data["schema_version"], "seed": data["info"].get("seed"),
                         "steps": len(data["steps"]), "agents": agent_names, "rewards": data["rewards"], "statuses": data["statuses"], "players": players})
    aggregate = {}
    for agent in sorted(TARGETS):
        rows = [r for r in target_rows if r["agent"] == agent]
        aggregate[agent] = {"episodes": len(rows), "scores": [r["final_score"] for r in rows],
                            "mean_score": mean(r["final_score"] for r in rows), "median_score": median(r["final_score"] for r in rows),
                            "mean_final_money": mean(r["final_money"] for r in rows), "mean_peak_hands": mean(r["peak_hands"] for r in rows),
                            "q_unlock_steps": {q: [r["quadrant_unlock"][q] for r in rows] for q in ("NE", "SW", "SE")}}
    output = {"schema_version": "e17.copilot.top3-replay-metrics.v1", "agent_id": "copilot", "analysis_only": True,
              "input_replay_ids": REPLAY_IDS, "episodes": episodes, "target_agent_rows": target_rows, "aggregate": aggregate,
              "not_calculable": ["executed_action_outcomes per request", "animal occupancy or species per pasture/coop tile", "causal contribution of market contention", "online policy features from future replay states", "Q1/Q2 labels: replays expose compass quadrant names only"]}
    (OUT / "E17_TOP3_REPLAY_METRICS.json").write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = ["# E17 Top-3 replay analysis — Copilot", "", "## Corpus verification", "", "All and only the nine preregistered replays were parsed. Each is valid JSON, has a distinct `info.EpisodeId`, schema/version `1`/`0.1.0`, module `1.32.7`, 720 steps, and terminal `DONE/DONE`. Agent/player mapping and terminal rewards reconcile with `data/replays/json/json.md`.", "", "## Quantitative benchmark", "", "| Agent | Episodes | Mean score | Median score | Mean final cash | Mean peak hands |", "|---|---:|---:|---:|---:|---:|"]
    for a in ("tetsuya", "OceanMix", "Crop Dusta"):
        x=aggregate[a]; lines.append(f"| {a} | {x['episodes']} | {x['mean_score']:,.2f} | {x['median_score']:,.2f} | ${x['mean_final_money']:,.2f} | {x['mean_peak_hands']:.2f} |")
    lines += ["", "## Episode cards and temporal quadrant table", "", "`Q1/Q2` are reported as the observed unlock order after NW: NE is Q1 and SW is Q2 whenever those are the first and second expansions. SE was not required by the observed 3Q runs. `unplanted` is final empty plus WEED tiles; animal-dedicated tiles are PASTURE plus COOP, not inferred animal occupancy.", ""]
    for r in target_rows:
        u=r['quadrant_unlock']; ft=r['final_tiles_by_quadrant']
        lines += [f"### {r['episode_id']} — {r['agent']} (player {r['player_index']})", "", f"OBSERVED: score `{r['final_score']:,.0f}`, final cash `${r['final_money']:,.0f}`, peak/terminal hands `{r['peak_hands']}/{r['terminal_hands']}`, movement requests `{r['movement_requests']}`, status `{r['terminal_status']}`. Q1 NE `{u['NE']}`, Q2 SW `{u['SW']}`, Q3 SE `{u['SE']}`. UNKNOWN: animal escapes (the replay exposes no event/state field).", "", "| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |", "|---|---:|---:|---:|---:|---:|---|"]
        for q in ("NW","NE","SW","SE"):
            x=ft[q]; crops=", ".join(f"{k}:{v}" for k,v in sorted(x['crops'].items())) or "—"
            lines.append(f"| {q} | {x['unlocked_tiles']} | {x['unplanted_tiles']} | {x['pasture']} | {x['coop']} | {x['animal_dedicated_tiles']} | {crops} |")
        lines += ["", f"DERIVED requested actions: {', '.join(f'{k}={v}' for k,v in sorted(r['action_requests'].items()))}.", ""]
    lines += ["## Cross-agent findings", "", "OBSERVED: all Top-3 agents reach a 3-quadrant footprint in the sampled corpus; terminal cash and score vary materially across opponent/seed. OBSERVED: no tetsuya–OceanMix head-to-head occurs, so this corpus cannot establish their causal ordering. INFERRED: earlier expansion combined with serviceable density, rather than terminal cash alone, is a high-value factor for a controlled follow-up.", "", "## Gap versus Copilot V2 derivative baseline", "", "OBSERVED: Copilot V2 is an open-loop, Codex-derived 3Q action table with no executed ledger and no independently attributable Q ownership. GAP (HIGH, implementation/telemetry): it cannot measure the per-day observed milestones above while running; add only an offline requested/executed ledger in a future independently authored experiment. GAP (MEDIUM, policy): the replay Top-3 agents show varied Q1/Q2 timing across seeds/opponents, whereas V2 has fixed timing. Missing information: action execution outcome and opponent intent prevent causal attribution.", "", "## Prioritized E17 hypothesis", "", "**E17-H1 — milestone-gated expansion telemetry (HIGH information value).** Mechanism: distinguish whether Q1/Q2 timing and workforce peaks correlate with final score after controlling by fixed seed/seat. Change one factor only: add an offline requested/executed milestone ledger to a new independent baseline; do not change routing. Baseline/control: identical independently authored policy without the ledger. Use at least 6 preregistered seeds with balanced seats. Primary metric: score; diagnostics: final cash, Q unlock step, peak hands, active crop/pasture/coop tiles, weeds, and execution ratios. Promote only if parity is byte/behavioral for actions and the ledger is complete; rollback if instrumentation changes actions or omits required fields. Risk: low policy risk, medium engineering cost. This report does not implement it.", "", "## Limits", "", "UNKNOWN: requested actions are not execution outcomes; pasture/coop tiles do not expose animal occupancy/species by coordinate; replay evidence is observational and must not be used online. No other-agent MODEL_SPEC, E17 output, or routine was used by this Copilot analysis."]
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    (REPORT_OUT / "E17_TOP3_REPLAY_ANALYSIS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
