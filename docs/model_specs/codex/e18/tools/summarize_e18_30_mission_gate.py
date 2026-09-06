"""Accounted matched deltas; failed safety remains visible in every summary."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean

BASE = Path(__file__).resolve().parents[1]
DERIVED = BASE / "artifacts/derived"


def cash_flow(p):
    return sum(
        sum(d["sales_cash"].values())
        - sum(d["purchase_cash"].values())
        - d["hire_cash"]
        - d["land_cash"]
        + d["unit_cash_delta"]
        for d in p["ledger"]["daily"]
    )


def evaluated(profiles):
    parents = {
        (p["opponent"], p["seed"], p["seat"]): p
        for p in profiles
        if p["variant"] == "PARENT"
    }
    rows = []
    for child in profiles:
        if child["variant"] == "PARENT":
            continue
        case = (child["opponent"], child["seed"], child["seat"])
        parent = parents[case]
        delta = child["reward"] - parent["reward"]
        assert cash_flow(child) - cash_flow(parent) == delta, case
        checks = {
            "complete": child["statuses"] == ["DONE", "DONE"],
            "no_errors": child["errors"] == child["opponent_errors"] == 0,
            "cash_audit": child["ledger"]["cash_parity_errors"] == 0,
            "zero_crop_deaths": not child["crop_starvation"],
            "zero_animal_losses": not child["ledger"]["animal_escapes"],
            "caps": child["max_resources"] <= 14 and child["max_hands"] <= 12,
            "topology": child["daily"][-1]["pasture_topology"]
            == {"Q0": 7, "Q1": 7, "Q2": 0, "Q3": 0}
            and not child["lower_quadrant_structure_observations"],
            "closed_missions": child["incomplete_missions"] == 0,
            "opening_frozen": child["prefix_d1_d6_sha256"]
            == parent["prefix_d1_d6_sha256"],
            "no_stranded_carried_or_shed": not child["terminal"]["carried"]
            and not child["terminal"]["shed"],
        }
        if child["variant"] == "OFF":
            assert (
                child["parity_batches"] == 719
                and child["actions_sha256"] == parent["actions_sha256"]
            ), case
        events = sum((Counter(d) for d in child["runtime_daily"].values()), Counter())
        rows.append(
            {
                "variant": child["variant"],
                "opponent": case[0],
                "seed": case[1],
                "seat": case[2],
                "parent": parent["reward"],
                "candidate": child["reward"],
                "opponent_reward": child["opponent_reward"],
                "delta": delta,
                "delta_pct": 100 * delta / parent["reward"],
                "safety": checks,
                "safe": all(checks.values()),
                "parent_crop_deaths": len(parent["crop_starvation"]),
                "candidate_crop_deaths": len(child["crop_starvation"]),
                "PASS": child["totals"].get("PASS", 0),
                "parent_PASS": parent["totals"].get("PASS", 0),
                "PASS_D15_D30": child["pass_d15_d30"],
                "parent_PASS_D15_D30": parent["pass_d15_d30"],
                "MOVE": child["totals"].get("MOVE", 0),
                "parent_MOVE": parent["totals"].get("MOVE", 0),
                "runtime_events": dict(events),
            }
        )
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    assert args.label.replace("_", "").isalnum()
    profiles, sources, seen = [], {}, set()
    for filename in args.inputs:
        path = DERIVED / filename
        source = json.loads(path.read_text())
        assert source["complete"] and not source["failures"], path
        sources[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        for p in source["matches"]:
            key = (p["variant"], p["opponent"], p["seed"], p["seat"])
            assert key not in seen, f"Duplicate matched case: {key}"
            seen.add(key)
            profiles.append(p)
    rows = evaluated(profiles)
    groups = []
    for variant, opponent in sorted({(r["variant"], r["opponent"]) for r in rows}):
        cases = [
            r for r in rows if (r["variant"], r["opponent"]) == (variant, opponent)
        ]
        group = {
            "variant": variant,
            "opponent": opponent,
            "n": len(cases),
            **{
                k: mean(r[k] for r in cases)
                for k in (
                    "parent",
                    "candidate",
                    "delta",
                    "PASS",
                    "parent_PASS",
                    "MOVE",
                    "parent_MOVE",
                    "PASS_D15_D30",
                    "parent_PASS_D15_D30",
                )
            },
            "worst_delta": min(r["delta"] for r in cases),
            "worst_pct": min(r["delta_pct"] for r in cases),
            "nonnegative": sum(r["delta"] >= 0 for r in cases),
            "safe": sum(r["safe"] for r in cases),
            "wins": sum(r["candidate"] > r["opponent_reward"] for r in cases),
        }
        group["development_economic_gate"] = (
            group["n"] == 14
            and group["delta"] > 0
            and group["nonnegative"] >= 12
            and group["worst_pct"] >= -1
        )
        groups.append(group)
    payload = {
        "analysis_id": f"E18_30_{args.label}",
        "sources": sources,
        "groups": groups,
        "cases": rows,
        "holdout_consumed": False,
        "new_submission": False,
    }
    out = DERIVED / f"E18_30_{args.label}.json"
    assert not out.exists(), out
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# E18.30 — gate runtime e delte economiche matched",
        "",
        "Seed development preregistrati; ogni candidata confrontata con E18.28 C sullo stesso seed/seat/avversario. OFF è un controllo di parità, non una candidata economica. Nessun holdout/upload. Gli esiti negativi non vengono esclusi.",
        "",
        "| Variante | Avversario | N | Cassa parent | Cassa candidata | Delta | Worst | Safety | Vittorie | PASS parent / candidata | MOVE parent / candidata |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for g in groups:
        lines.append(
            f"| {g['variant']} | {g['opponent']} | {g['n']} | {g['parent']:.1f} | {g['candidate']:.1f} | {g['delta']:+.1f} | {g['worst_delta']:+.0f} | {g['safe']}/{g['n']} | {g['wins']}/{g['n']} | {g['parent_PASS']:.1f} / {g['PASS']:.1f} | {g['parent_MOVE']:.1f} / {g['MOVE']:.1f} |"
        )
    lines += ["", "## Safety fallita o anomalie", ""]
    for r in rows:
        failed = [k for k, v in r["safety"].items() if not v]
        if failed:
            lines.append(
                f"- {r['variant']} / {r['opponent']} / {r['seed']} / P{r['seat']}: {', '.join(failed)}; crop deaths parent {r['parent_crop_deaths']}, candidata {r['candidate_crop_deaths']}."
            )
    if all(r["safe"] for r in rows):
        lines.append(
            "Nessun gate tecnico/safety fallito nei casi eseguiti; non equivale a promozione o verifica fuori campione."
        )
    lines += [
        "",
        "## Limiti",
        "",
        "Lo smoke su un solo seed non soddisfa il gate economico development a 14 casi. Le due seat sono controlli di posizione, non seed indipendenti. La cassa incrementale è riconciliata con vendite, acquisti, lavoro e altre spese nel motore; meno PASS da solo non dimostra maggiore efficienza.",
        "",
        f"Dataset completo: `../artifacts/derived/{out.name}`.",
    ]
    report = BASE / "reports" / f"E18_30_{args.label}_IT.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(groups, indent=2), flush=True)
    print(str(report), flush=True)


if __name__ == "__main__":
    main()
