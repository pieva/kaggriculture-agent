"""Extend the approved chart source mechanically with five diagnostic panels."""

import argparse
import hashlib
import html
import json
import re
import statistics
from pathlib import Path

from docs.model_specs.codex.e18.tools.build_e18_27_top770_complete_kpi import (
    METRICS,
    flatten,
)

BASE = Path(__file__).resolve().parents[1]
DERIVED = BASE / "artifacts/derived"
EXTRA = (
    ("MOVE", "Movimenti · per giornata", "Comandi (n.)", "moves"),
    ("PASS", "PASS · per giornata", "Comandi (n.)", "passes"),
    ("unwatered_tiles_h24", "Non irrigate · checkpoint H24", "Tile (n.)", "dry"),
    (
        "verified_animal_losses",
        "Perdite animali · per giornata",
        "Animali (n.)",
        "losses",
    ),
    ("weed_tiles", "Erbacce · checkpoint H24", "Tile (n.)", "weeds"),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", type=Path, required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    gate = json.loads(args.gate.read_text())
    assert gate["complete"]
    candidates = [
        p
        for p in gate["matches"]
        if p["variant"] == args.variant and p["opponent"] == "E18.16"
    ]
    assert candidates
    top = json.loads((DERIVED / "E18_26_JESSE_770_D01_D30_CLOSURE.json").read_text())[
        "jesse"
    ]
    operational = {
        p["episode_id"]: p
        for p in json.loads(
            (DERIVED / "TOP770_D01_D30_OPERATIONAL_KPI.json").read_text()
        )["profiles"]
    }
    keys = [*METRICS, *(r[0] for r in EXTRA)]
    source = {
        "candidate": [
            [flatten(p["daily"][i]) | p["operational_daily"][i] for i in range(30)]
            for p in candidates
        ],
        "top770": [
            [
                flatten(p["daily"][i]) | operational[p["episode_id"]]["daily"][i]
                for i in range(30)
            ]
            for p in top
        ],
    }
    series = {
        name: {
            k: [
                [statistics.median(v), min(v), max(v)]
                for v in [[p[i][k] for p in profiles] for i in range(30)]
            ]
            for k in keys
        }
        for name, profiles in source.items()
    }
    dataset = {
        "analysis_id": f"E18_28_{args.variant}_TOP770_D01_D30_KPI_19",
        "report_standard": "E18_AGENT_COMPARISON_REPORT_STANDARD_V2",
        "series": series,
        "cohorts": {
            "candidate": {
                "variant": args.variant,
                "n": len(candidates),
                "seeds": sorted({p["seed"] for p in candidates}),
                "seats": sorted({p["seat"] for p in candidates}),
                "opponent": "E18.16",
            },
            "top770": {"n": 5, "episodes": [p["episode_id"] for p in top]},
        },
        "checkpoint": "H24 pre-last batch D1-D29, terminal D30. Unwatered is a state, not a verified missed deadline.",
        "flow": "MOVE/PASS totals by pre-action day; verified refresh animal losses assigned to that service day.",
        "comparison": "Descriptive public/local comparison; different seeds/opponents/markets. Median and observed min-max, not confidence intervals.",
        "gate_file": str(args.gate),
        "gate_sha256": hashlib.sha256(args.gate.read_bytes()).hexdigest(),
    }
    dataset_path = DERIVED / (dataset["analysis_id"] + ".json")
    dataset_path.write_text(json.dumps(dataset, indent=2) + "\n", encoding="utf-8")
    # Recover the unchanged approved inline source retained in its standalone
    # export, so regeneration does not depend on a previous task directory.
    reference = (BASE / "reports/E18_27_TOP770_D01_D30_COMPLETE_KPI.html").read_text(
        encoding="utf-8"
    )
    inner = html.unescape(re.search(r'srcdoc="(.*?)"', reference, re.DOTALL).group(1))
    start = inner.index('<div id="top770-e27-complete-d30">')
    data_start = inner.index("const data=", start)
    fragment = inner[start : inner.index("</script>", data_start) + len("</script>")]
    fragment, n = re.subn(
        r"^  const data=.*;$",
        "  const data=" + json.dumps(series, separators=(",", ":")) + ";",
        fragment,
        flags=re.MULTILINE,
    )
    assert n == 1
    fragment = fragment.replace("top770-e27-complete-d30", "top770-e28-diagnostic-d30")
    fragment = fragment.replace("E18.27 V3", f"E18.28 {args.variant}").replace(
        "14 partite", f"{len(candidates)} partite"
    )
    marker = next(
        line
        for line in fragment.splitlines()
        if '<section data-metric="empty_coops"' in line
    )
    panels = [
        f'    <section data-metric="{key}" data-title="{title}" data-unit="{unit}" data-family="{family}"><h3>{title}</h3><div class="jt-chart"></div></section>'
        for key, title, unit, family in EXTRA
    ]
    fragment = fragment.replace(marker, marker + "\n" + "\n".join(panels))
    fragment = fragment.replace(
        'coop:["empty_coops"]',
        'coop:["empty_coops"],'
        + ",".join(f'{family}:["{key}"]' for key, _, _, family in EXTRA),
    )
    assert fragment.count("<section data-metric=") == 19
    args.output.write_text(fragment + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "dataset": str(dataset_path),
                "fragment": str(args.output),
                "panels": 19,
                "n": len(candidates),
            }
        )
    )


if __name__ == "__main__":
    main()
