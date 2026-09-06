"""Static mobile-readable standard V3 figures from frozen, audited cohorts.

Reporting only: no simulations, downloads, policy changes or promotion.
"""

import argparse
import hashlib
import json
from pathlib import Path
from statistics import mean, median

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MaxNLocator

from docs.model_specs.codex.e18.tools.build_e18_27_top770_complete_kpi import flatten
from docs.model_specs.codex.e18.tools.build_e18_29_simulation_report import STANDARD

BASE = Path(__file__).resolve().parents[1]
DERIVED = BASE / "artifacts/derived"
DATASET = DERIVED / "E18_30_TOP770_D01_D30_KPI_V3_MOBILE.json"
PANELS = (
    ("money", "Cassa", "Cassa ($)"),
    ("people", "Persone, incluso farmer", "Persone (n.)"),
    ("crop_tiles", "Tile coltivate", "Tile (n.)"),
    ("occupied_livestock_tiles", "Tile con animali", "Tile (n.)"),
    ("COW", "Mucche", "Animali (n.)"),
    ("SHEEP", "Pecore", "Animali (n.)"),
    ("GOOSE", "Oche", "Animali (n.)"),
    ("empty_pastures", "Pascoli vuoti", "Tile (n.)"),
    ("MELON", "Meloni", "Tile (n.)"),
    ("WHEAT", "Grano", "Tile (n.)"),
    ("STRAWBERRY", "Fragole", "Tile (n.)"),
    ("CARROT", "Carote", "Tile (n.)"),
    ("TOMATO", "Pomodori", "Tile (n.)"),
    ("empty_coops", "Ricoveri oche vuoti", "Tile (n.)"),
    ("MOVE", "Movimenti", "MOVE / giorno"),
    ("PASS", "PASS", "PASS / giorno"),
    ("unwatered_tiles_h24", "Colture non irrigate a H24", "Tile (n.)"),
    ("verified_animal_losses", "Perdite animali verificate", "Perdite / giorno"),
    ("weed_tiles", "Tile di erbacce", "Tile (n.)"),
    ("WATER", "WATER riusciti", "WATER / giorno"),
    ("FEED", "FEED riusciti", "FEED / giorno"),
)
FLOWS = {"MOVE", "PASS", "verified_animal_losses", "WATER", "FEED"}
STYLE = {
    "candidate": {
        "label": "E18.30 V2 · n14",
        "color": "#1764B0",
        "marker": "o",
        "linestyle": "-",
    },
    "top770": {
        "label": "Top770 · n5",
        "color": "#A66B00",
        "marker": "s",
        "linestyle": (0, (4, 3)),
    },
}


def build_dataset():
    sources = {}

    def read(name):
        path = DERIVED / name
        sources[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        payload = json.loads(path.read_text(encoding="utf-8"))
        if "matches" in payload:
            assert payload["complete"] and not payload["failures"]
        return payload

    candidates = [
        p
        for name in ("CROP_STRESS", "CROP_DEVELOPMENT")
        for p in read(f"E18_30_MISSION_GATE_{name}_V2_20260906.json")["matches"]
    ]
    assert len(candidates) == 14
    assert all(
        p["variant"] == "CROP_POOL" and p["opponent"] == "E18.16" for p in candidates
    )
    assert {(p["seed"], p["seat"]) for p in candidates} == {
        (s, seat) for s in range(180903001, 180903008) for seat in (0, 1)
    }
    top = read("E18_26_JESSE_770_D01_D30_CLOSURE.json")["jesse"]
    top_ops = {
        p["episode_id"]: p["daily"]
        for p in read("TOP770_D01_D30_OPERATIONAL_KPI.json")["profiles"]
    }
    assert len(top) == 5 and len({p["episode_id"] for p in top}) == 5
    groups = {"candidate": candidates, "top770": top}
    profile_daily, summaries, series = {}, {}, {}
    for name, profiles in groups.items():
        prepared = []
        for p in profiles:
            assert len(p["daily"]) == len(p["ledger"]["daily"]) == 30
            assert p["daily"][-1]["pasture_topology"] == {
                "Q0": 7,
                "Q1": 7,
                "Q2": 0,
                "Q3": 0,
            }
            assert p["ledger"]["cash_parity_errors"] == 0
            ops = (
                p["operational_daily"]
                if name == "candidate"
                else top_ops[p["episode_id"]]
            )
            days = []
            for i, (stock, ledger, operational) in enumerate(
                zip(p["daily"], p["ledger"]["daily"], ops, strict=True)
            ):
                assert stock["day"] == ledger["day"] == operational["day"] == i + 1
                row = flatten(stock) | operational
                for op in ("WATER", "FEED"):
                    row[op] = ledger["executed_actions"].get(op, 0)
                for op in ("PASS", "MOVE"):
                    assert row[op] == ledger["requested_actions"].get(op, 0)
                    if name == "candidate":
                        assert row[op] == p["action_daily"][i].get(op, 0)
                days.append({k: row[k] for k in STANDARD})
            assert days[-1]["money"] == p["terminal"]["cash"]
            prepared.append(
                {
                    "seed": p.get("seed"),
                    "seat": p["seat"],
                    "episode_id": p.get("episode_id"),
                    "daily": days,
                }
            )
        profile_daily[name] = prepared
        series[name] = {
            key: [
                [median(v), min(v), max(v)]
                for v in [[p["daily"][i][key] for p in prepared] for i in range(30)]
            ]
            for key in STANDARD
        }
        summaries[name] = {
            "cash_mean": mean(p["terminal"]["cash"] for p in profiles),
            "cash_median": median(p["terminal"]["cash"] for p in profiles),
            "pass_d15_d30_mean": mean(
                sum(d["PASS"] for d in p["daily"][14:]) for p in prepared
            ),
            **{
                op + "_mean": mean(sum(d[op] for d in p["daily"]) for p in prepared)
                for op in ("WATER", "FEED", "PASS", "MOVE")
            },
        }
    return {
        "analysis_id": DATASET.stem,
        "report_standard": "E18_AGENT_COMPARISON_REPORT_STANDARD_V3",
        "chart_cohorts": ["candidate", "top770"],
        "sources": sources,
        "cohorts": {
            "candidate": {
                "version": "E18.30 CROP_POOL V2",
                "n": 14,
                "seeds": list(range(180903001, 180903008)),
                "seats": [0, 1],
                "opponent": "E18.16",
            },
            "top770": {
                "n": 5,
                "episodes": [p["episode_id"] for p in top],
                "filter": "final-770",
                "frozen": True,
            },
        },
        "series": series,
        "profile_daily": profile_daily,
        "summary": summaries,
        "checkpoint": "H24 pre-last batch D1-D29; D30 terminal. 12 hands = 13 people including farmer.",
        "flows": "MOVE/PASS are requested unit commands; WATER/FEED are successful actions, by execution day; animal losses are verified refresh losses.",
        "interpretation": "Pointwise median and observed min-max, not confidence intervals or a real single trajectory. Public/local descriptive comparison: different seeds/opponents/markets.",
        "missing_irrigation": "Unwatered checkpoint tiles do not prove a missed deadline or crop death.",
        "new_simulation": False,
        "new_submission": False,
        "holdout_consumed": False,
    }


def number(value, _position=None):
    return (f"{value / 1000:g}k" if abs(value) >= 1000 else f"{value:g}").replace(
        ".", ","
    )


def render(data, output_dir):
    assert tuple(k for k, _, _ in PANELS) == STANDARD
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 15,
            "axes.titlesize": 15,
            "axes.labelsize": 14,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "axes.edgecolor": "#C4C7CC",
            "text.color": "#20242A",
            "axes.labelcolor": "#20242A",
            "xtick.color": "#20242A",
            "ytick.color": "#20242A",
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )
    outputs = []
    days = list(range(1, 31))
    for group in range(7):
        fig, axes = plt.subplots(3, 1, figsize=(6, 11.25), dpi=160)
        fig.subplots_adjust(left=0.18, right=0.96, top=0.875, bottom=0.105, hspace=0.64)
        fig.suptitle(
            "Top770 vs E18.30 · D1–D30", x=0.05, y=0.98, ha="left", fontsize=17
        )
        handles = [
            Line2D([], [], linewidth=2.3, markersize=5, **STYLE[k])
            for k in ("top770", "candidate")
        ]
        fig.legend(
            handles=handles,
            loc="upper left",
            bbox_to_anchor=(0.03, 0.95),
            ncol=2,
            frameon=False,
            fontsize=13.5,
            handlelength=2,
            columnspacing=1,
        )
        for index, ax in enumerate(axes, start=3 * group):
            key, title, unit = PANELS[index]
            observations = [
                v
                for series in data["series"].values()
                for triple in series[key]
                for v in triple
            ]
            low, high = min(0, min(observations)), max(observations)
            span = high - low or 1
            ax.set_ylim(low - span * 0.065, high + span * 0.12)
            ax.set_xlim(0.5, 30.5)
            for name in ("candidate", "top770"):
                values = data["series"][name][key]
                central, minimum, maximum = zip(*values, strict=True)
                style = STYLE[name]
                stepped = key not in FLOWS and key != "money"
                ax.fill_between(
                    days,
                    minimum,
                    maximum,
                    color=style["color"],
                    alpha=0.105,
                    step="post" if stepped else None,
                    linewidth=0,
                )
                ax.plot(
                    days,
                    central,
                    linewidth=2.0,
                    markersize=3.3,
                    markerfacecolor="white",
                    markeredgewidth=1.05,
                    drawstyle="steps-post" if stepped else "default",
                    **style,
                )
            ax.set_title(f"{index + 1:02d} · {title}", loc="left", pad=12)
            ax.set_ylabel(unit, labelpad=10)
            ax.set_xlabel("Giorno", labelpad=7)
            ax.set_xticks([1, 10, 20, 30], ["D1", "D10", "D20", "D30"])
            ax.yaxis.set_major_locator(
                MaxNLocator(nbins=4, integer=True, min_n_ticks=2)
            )
            ax.yaxis.set_major_formatter(FuncFormatter(number))
            ax.grid(axis="y", color="#D9DDE2", linewidth=0.65, zorder=0)
            ax.spines[["top", "right"]].set_visible(False)
            if high == 0:
                ax.set_yticks([0])
                ax.text(
                    0.55, 0.76, "0 in tutti i casi", transform=ax.transAxes, fontsize=13
                )
        fig.text(0.05, 0.035, "Mediane · fasce min–max osservato", fontsize=12.7)
        fig.text(
            0.05,
            0.013,
            f"Confronto descrittivo · pannelli {3 * group + 1}–{3 * group + 3}",
            fontsize=12.7,
        )
        target = output_dir / f"e18-30-top770-kpi-{group + 1:02d}.png"
        fig.savefig(
            target,
            dpi=160,
            metadata={
                "Title": "E18.30 CROP_POOL V2 vs Top770",
                "Description": data["interpretation"],
            },
        )
        plt.close(fig)
        outputs.append(str(target.resolve()))
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    payload = build_dataset()
    if DATASET.exists():
        assert json.loads(DATASET.read_text()) == payload, "Preserve previous evidence"
    else:
        DATASET.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    outputs = render(payload, args.output_dir)
    print(
        json.dumps(
            {"dataset": str(DATASET), "images": outputs, "summary": payload["summary"]},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
