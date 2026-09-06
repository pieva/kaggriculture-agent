"""Restore the approved two-column interactive report for frozen E18.30 V2."""

import argparse
import json
import re
from pathlib import Path

from docs.model_specs.codex.e18.tools.build_e18_30_mobile_kpi import DATASET, STANDARD

BASE = Path(__file__).resolve().parents[1]


def render_fragment(data):
    assert data["cohorts"]["candidate"]["version"] == "E18.30 CROP_POOL V2"
    assert data["chart_cohorts"] == ["candidate", "top770"]
    template = (BASE / "tools/templates/e18_29_simulation_report.html").read_text(
        encoding="utf-8"
    )
    for metric in (
        "pass_share",
        "net_cash_100_slots",
        "fertilizer_collected",
        "fertilizer_used",
    ):
        template, count = re.subn(
            r'    <section data-metric="' + metric + r'"[^\n]+</section>\n',
            "",
            template,
        )
        assert count == 1, metric
    fragment = template.replace("e29-simulation-d30", "e30-top770-desktop-d30").replace(
        "e29-", "e30-"
    )
    fragment = fragment.replace("E18.29 B3", "E18.30 V2")
    fragment = fragment.replace(
        "Traiettorie 7–7–0 · D1–D30", "E18.30 V2 vs Top770 · 21 KPI · D1–D30"
    )
    fragment = fragment.replace(
        "Mediana e intervallo min–max · confronto descrittivo con Top770",
        "Mediana e min–max osservato · Top770 storico, final-770 · confronto descrittivo",
    )
    series = {
        name: {key: data["series"][name][key] for key in STANDARD}
        for name in data["chart_cohorts"]
    }
    fragment = fragment.replace(
        "__REPORT_SERIES__", json.dumps(series, separators=(",", ":"))
    )
    assert fragment.count('<section data-metric="') == 21
    assert '"parent":' not in fragment and "Cause PASS" not in fragment
    assert "__REPORT_" not in fragment and "E18.29" not in fragment
    assert len(fragment.encode()) < 1_000_000
    return fragment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fragment", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    fragment = render_fragment(data)
    args.fragment.parent.mkdir(parents=True, exist_ok=True)
    args.fragment.write_text(fragment, encoding="utf-8", newline="\n")
    assert args.fragment.read_text(encoding="utf-8") == fragment
    print(
        json.dumps(
            {
                "fragment": str(args.fragment.resolve()),
                "panels": 21,
                "series": data["chart_cohorts"],
            }
        )
    )


if __name__ == "__main__":
    main()
