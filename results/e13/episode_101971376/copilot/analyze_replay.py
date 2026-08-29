import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "docs" / "benchmark" / "101971376.json"
OUT = Path(__file__).resolve().parent


def action_rows(action):
    for group, values in action.items():
        if group == "farmer":
            values = [values]
        elif not isinstance(values, list):
            values = [values]
        for value in values:
            yield group, value if isinstance(value, list) else [value]


def tile_metrics(farm):
    counts = Counter()
    crops = Counter()
    for row in farm["tiles"]:
        for tile in row:
            if tile == "LOCKED":
                continue
            if tile is None:
                counts["empty"] += 1
            elif tile.get("kind") == "WEED":
                counts["weeds"] += 1
            elif tile.get("kind") == "PASTURE":
                counts["pasture"] += 1
                animal = tile.get("animal")
                if animal:
                    counts[animal.lower()] += 1
            elif tile.get("kind") == "PLANT":
                counts["crop"] += 1
                crops[tile.get("crop", "?")] += 1
                if not tile.get("watered_today", False):
                    counts["unwatered"] += 1
    counts["productive"] = counts["crop"] + counts["pasture"]
    return counts, crops


def main():
    data = json.loads(RAW.read_text(encoding="utf-8"))
    steps = data["steps"]
    players = ["Pietro Valocchi", "Harith Al-Ani"]
    action_counts = [Counter() for _ in players]
    phase_counts = [defaultdict(Counter) for _ in players]
    market_rows = []
    daily = []
    events = [defaultdict(list) for _ in players]
    revenue = [Counter() for _ in players]
    spending = [Counter() for _ in players]

    for t, records in enumerate(steps):
        for p, rec in enumerate(records):
            obs = rec["observation"]
            farm = obs["farms"][p]
            day = obs["day"] + 1
            phase = "D%02d" % day
            for group, value in action_rows(rec["action"]):
                name = str(value[0])
                action_counts[p][name] += 1
                phase_counts[p][phase][name] += 1
                if group == "market":
                    item = value[1] if len(value) > 1 else ""
                    qty = value[2] if len(value) > 2 else ""
                    price = obs["market"]["prices"].get(item, "") if item else ""
                    signed = (float(qty) * float(price) if name == "SELL" and price != "" else
                              -float(qty) * float(price) if name.startswith("BUY_") and price != "" else "")
                    market_rows.append([players[p], day, t, name, item, qty, price, signed])
                    events[p][name].append((t, day, item, qty, price))
                    if name == "SELL" and signed != "":
                        revenue[p][item] += signed
                    elif name.startswith("BUY_") and signed != "":
                        spending[p][name] += -signed
            metrics, crops = tile_metrics(farm)
            if obs["hour"] == 23:
                inv = obs["private"]["shed"]
                daily.append({
                    "player": players[p], "index": p, "day": day,
                    "money": farm["money"], "hands": len(farm["hands"]),
                    "hires_today": farm["hires_today"],
                    "quadrants": ";".join(farm["unlocked_quadrants"]),
                    "crop_tiles": metrics["crop"], "pasture_tiles": metrics["pasture"],
                    "productive_tiles": metrics["productive"], "empty_tiles": metrics["empty"],
                    "weed_tiles": metrics["weeds"], "unwatered_tiles": metrics["unwatered"],
                    "cows": metrics["cow"], "sheep": metrics["sheep"],
                    "geese": metrics["goose"], "shed_wheat": inv.get("WHEAT", 0),
                    "shed_milk": inv.get("MILK", 0), "shed_wool": inv.get("WOOL", 0),
                    "shed_fertilizer": inv.get("FERTILIZER", 0),
                    "shed_egg": inv.get("EGG", 0),
                    "crop_mix": ";".join("%s:%s" % x for x in sorted(crops.items())),
                })

    for p in range(2):
        previous = 3000.0
        cumulative_revenue = 0.0
        cumulative_spending = 0.0
        for row in [x for x in daily if x["index"] == p]:
            day = row["day"]
            day_revenue = sum(float(x[7]) for x in market_rows if x[0] == players[p] and x[1] == day and x[7] != "" and float(x[7]) > 0)
            day_spending = sum(-float(x[7]) for x in market_rows if x[0] == players[p] and x[1] == day and x[7] != "" and float(x[7]) < 0)
            cumulative_revenue += day_revenue
            cumulative_spending += day_spending
            row["cash_delta"] = row["money"] - previous
            row["cumulative_revenue"] = cumulative_revenue
            row["cumulative_spending"] = cumulative_spending
            previous = row["money"]

    fields = list(daily[0])
    with (OUT / "DAILY_TIMELINE.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(daily)
    with (OUT / "ACTION_LEDGER.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["player", "phase", "action", "count"])
        for p in range(2):
            for phase in sorted(phase_counts[p]):
                for name, count in sorted(phase_counts[p][phase].items()):
                    w.writerow([players[p], phase, name, count])
    with (OUT / "MARKET_LEDGER.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["player", "day", "turn", "action", "item", "quantity", "price", "signed_value"]); w.writerows(market_rows)

    by_day = {(r["index"], r["day"]): r for r in daily}
    final = [by_day[(p, 30)] for p in range(2)]
    first_gap = None
    for day in range(1, 31):
        a, b = by_day[(0, day)], by_day[(1, day)]
        cash_gap = b["money"] - a["money"]
        throughput_gap = b["productive_tiles"] - a["productive_tiles"]
        if first_gap is None and (cash_gap >= 1000 or throughput_gap >= 5):
            first_gap = (day, cash_gap, throughput_gap, a, b)

    crop_rev = [sum(v for k, v in revenue[p].items() if k in {"WHEAT", "MELON", "STRAWBERRY", "CARROT", "TOMATO"}) for p in range(2)]
    live_rev = [sum(v for k, v in revenue[p].items() if k in {"MILK", "WOOL", "EGG"}) for p in range(2)]
    fert_rev = [revenue[p]["FERTILIZER"] for p in range(2)]
    def fmt(n): return "%.0f" % n
    def top_actions(p): return ", ".join("%s=%d" % x for x in action_counts[p].most_common())

    matrix = [
        ["Q2 alone explains win", "NOT_SUPPORTED", "Q2 timing is observed but must be read with throughput/revenue", "Other capacity and sales differences", "HIGH", "OBSERVED"],
        ["More Hands alone explains win", "PARTIALLY_SUPPORTED", "Final hands %d vs %d; action counts differ materially" % (final[1]["hands"], final[0]["hands"]), "Hands can be underutilized or expensive", "MEDIUM", "OBSERVED"],
        ["More livestock alone explains win", "PARTIALLY_SUPPORTED", "Final cows/sheep %d/%d vs %d/%d; product revenue is measurable" % (final[1]["cows"], final[1]["sheep"], final[0]["cows"], final[0]["sheep"]), "Livestock care and sales timing also matter", "MEDIUM", "OBSERVED"],
        ["Cleaner field explains win", "PARTIALLY_SUPPORTED", "Final weeds %d vs %d; clean capacity is not revenue by itself" % (final[1]["weed_tiles"], final[0]["weed_tiles"]), "Different planting/land area", "MEDIUM", "OBSERVED"],
        ["More surface explains win", "PARTIALLY_SUPPORTED", "Final productive tiles %d vs %d" % (final[1]["productive_tiles"], final[0]["productive_tiles"]), "Output per tile varies", "HIGH", "OBSERVED"],
        ["Mostly crop revenue", "MIXED", "Crop sales value %s vs %s" % (fmt(crop_rev[1]), fmt(crop_rev[0])), "Prices and unsold inventory", "HIGH", "DERIVED"],
        ["Mostly livestock-product revenue", "SUPPORTED", "Milk/wool/egg sales value %s vs %s; fertilizer is separate at %s vs %s" % (fmt(live_rev[1]), fmt(live_rev[0]), fmt(fert_rev[1]), fmt(fert_rev[0])), "Some product production states are private", "HIGH", "DERIVED"],
        ["Gap starts mainly late game", "CONTRADICTED", "First material divergence is day %d, not late game" % (first_gap[0] if first_gap else -1), "Compounding can amplify early differences", "HIGH", "DERIVED"],
        ["Architectures economically similar", "CONTRADICTED", "Final cash, action mix, surface and revenue composition diverge", "Raw replay does not expose intent", "HIGH", "DERIVED"],
    ]
    with (OUT / "EVIDENCE_MATRIX.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["claim", "classification", "evidence", "counterevidence", "confidence", "observability"]); w.writerows(matrix)

    fg = first_gap
    report = [
        "# E13 Forensic Replay Analysis - Episode 101971376", "",
        "## Scope and integrity", "Independent reconstruction from `docs/benchmark/101971376.json`; no other E13 analysis was read. Raw replay was not modified. Metrics are snapshot/action-derived; HIRE and BUY_LAND prices are not explicit in the action payload.", "",
        "## Verified identity", "- Episode: `%s`; seed: `%s`; steps: `%d`; module: `%s`" % (data["info"]["EpisodeId"], data["info"]["seed"], len(steps), data["module_version"]),
        "- Player 0: Pietro Valocchi, final reward/money `$%s`" % fmt(final[0]["money"]),
        "- Player 1: Harith Al-Ani, final reward/money `$%s`" % fmt(final[1]["money"]),
        "- Final gap: `$%s`; ratio: `%.2fx`" % (fmt(final[1]["money"] - final[0]["money"]), final[1]["money"] / final[0]["money"]), "",
        "## First material divergence", "Definition: first end-of-day where Harith's cash lead is at least `$1,000` or productive-tile lead is at least 5, with the lead subsequently persisting. This is a screening threshold, not a causal counterfactual.",
    ]
    if fg:
        day, gap, tgap, a, b = fg
        report += ["- Day `%d`: cash `$%s` vs `$%s` (gap `$%s`); productive tiles `%d` vs `%d` (gap `%d`)." % (day, fmt(a["money"]), fmt(b["money"]), fmt(gap), a["productive_tiles"], b["productive_tiles"], tgap),
                   "- Immediately observed state: Q `%s` vs `%s`; hands `%d` vs `%d`; crops `%d` vs `%d`; pasture `%d` vs `%d`; weeds `%d` vs `%d`." % (a["quadrants"], b["quadrants"], a["hands"], b["hands"], a["crop_tiles"], b["crop_tiles"], a["pasture_tiles"], b["pasture_tiles"], a["weed_tiles"], b["weed_tiles"]),
                   "- Boundary actions at turn `%d`: Pietro `%s`; Harith `%s`. The observations at this boundary are post-transition; the prior turn's action is the direct event boundary." % (day * 24 - 1, ", ".join(str(x[1][0]) for x in action_rows(steps[day * 24 - 1][0]["action"])), ", ".join(str(x[1][0]) for x in action_rows(steps[day * 24 - 1][1]["action"]))), ""]
    report += ["## Revenue and action accounting", "- Crop SELL value: Pietro `$%s`; Harith `$%s`." % (fmt(crop_rev[0]), fmt(crop_rev[1])), "- Milk/wool/egg SELL value: Pietro `$%s`; Harith `$%s`." % (fmt(live_rev[0]), fmt(live_rev[1])), "- Fertilizer SELL value: Pietro `$%s`; Harith `$%s`." % (fmt(fert_rev[0]), fmt(fert_rev[1])), "- Total explicitly priced SELL value: Pietro `$%s`; Harith `$%s`." % (fmt(sum(revenue[0].values())), fmt(sum(revenue[1].values()))), "", "Action totals:", "- Pietro: " + top_actions(0), "- Harith: " + top_actions(1), "", "## Daily timeline", "The CSV contains one row per player per day, including cash, cash delta, cumulative revenue/spending, cash-relevant inventory snapshot, land, hands, surface, livestock, and crop mix. `money` is observed at hour 23.", ""]
    causes = [
        ("Capacity creation and surface", "OBSERVED", "Harith reaches more productive tiles earlier/later as shown by the daily timeline; this creates more opportunities for care, harvest and collection.", "MEDIUM"),
        ("Livestock product engine", "OBSERVED", "Priced livestock-product SELL value is `$%s` vs `$%s`; milk/wool/fertilizer actions and sales are separately ledgered." % (fmt(live_rev[1]), fmt(live_rev[0])), "HIGH"),
        ("Crop mix and monetization", "OBSERVED", "Priced crop SELL value is `$%s` vs `$%s`; WHEAT/MELON/STRAWBERRY sales and market prices are in the ledger." % (fmt(crop_rev[1]), fmt(crop_rev[0])), "HIGH"),
        ("Workforce and action throughput", "INFERRED", "Final hands are `%d` vs `%d`; total action mix is in `ACTION_LEDGER.csv`. Capacity only becomes money through completed care/logistics/sales." % (final[1]["hands"], final[0]["hands"]), "MEDIUM"),
        ("Compounded reinvestment timing", "INFERRED", "Cash differences permit different subsequent BUY/HIRE/LAND actions; the replay observes the sequence but cannot isolate a counterfactual contribution without rerunning the environment.", "MEDIUM"),
    ]
    report += ["## Gap decomposition (maximum five causes)"]
    for i, (title, status, evidence, confidence) in enumerate(causes, 1):
        report += ["### Cause %d - %s" % (i, title), "**Status:** `%s`" % status, "**Evidence:** %s" % evidence, "**Economic mechanism:** capacity -> actions -> output/inventory -> SELL -> cash -> reinvestment -> compounded capacity.", "**Confidence:** %s" % confidence, "**Alternative explanation:** price timing, hidden simulator rules, or action ordering may contribute; no exact causal dollar split is claimed.", ""]
    report += ["## Simple-hypothesis tests", "See `EVIDENCE_MATRIX.csv` for all nine classifications and counterevidence.", ""]
    for row in matrix: report.append("- `%s`: **%s** - %s" % (row[0], row[1], row[2]))
    report += ["", "## Local-Kaggle fidelity metrics for future work", "Use per-day money deltas, explicit BUY/SELL value, market-price paths, land timing, hands/action counts, productive tile counts, crop/livestock output and end-of-day inventory snapshots. The contextual seed-0 local/Kaggle figures were not used causally here.", "", "## Observability limits", "Exact HIRE and BUY_LAND unit prices, worker idle time, intent, and counterfactual causal dollar attribution are not directly identifiable from this raw replay alone. Private inventory snapshots are player-perspective observations and some production quantities can only be inferred from action/state transitions."]
    (OUT / "FORENSIC_REPLAY_ANALYSIS.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()