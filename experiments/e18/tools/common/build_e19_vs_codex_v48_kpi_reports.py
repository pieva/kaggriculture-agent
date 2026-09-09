#!/usr/bin/env python3
"""Build 22-panel D1-D30 KPI reports (E18 standard V4.1) from the live
paired matches produced by run_e19_vs_codex_v48_paired_kpi.py: each
registered candidate vs Codex V48 (770), 14 games each (7 development
seeds, both seats).

A standing verification instrument, not a one-off: PAIRINGS/LABELS/
FILENAME_STEM below mirror the runner's REGISTRY -- add a candidate there
and here to get its report; every existing report regenerates identically
on each run (deterministic from the same JSON profiles), so re-running
this after adding one new candidate is the normal way to extend the
dashboard, not a special case.

Standard: experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V4_IT.md
Template: docs/model_specs/codex/e19/tools/complete_kpi_template.html (generic,
topLabel/candidate-label driven -- reused as-is, not modified).
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from statistics import mean, median
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import (
    FIELDS,
    aggregate,
    fmt,
)
DERIVED = ROOT / "experiments/e18/artifacts/derived/common/e19_vs_codex_v48_paired_kpi_20260909"
REPORT_DIR = ROOT / "experiments/e18/reports/common"
TEMPLATE = ROOT / "docs/model_specs/codex/e19/tools/complete_kpi_template.html"

CLAUDE = "CLAUDE_E18_4"
ANTIGRAVITY = "ANTIGRAVITY_E19_1"
ANTIGRAVITY_V2 = "ANTIGRAVITY_E19_2"
COPILOT = "COPILOT_E18_8_V5"
CLAUDE_V5 = "CLAUDE_E18_5"
PAIRINGS = (CLAUDE, ANTIGRAVITY, ANTIGRAVITY_V2, COPILOT, CLAUDE_V5)

LABELS = {
    CLAUDE: "Claude E18.4 Capacity-Certified",
    ANTIGRAVITY: "Antigravity E19.1 Hybrid Livestock",
    ANTIGRAVITY_V2: "Antigravity E19.2 Hybrid Livestock",
    COPILOT: "Copilot E18.8 Economic Recovery V5",
    CLAUDE_V5: "Claude E18.5 Wheat-Market-Fix",
}
FILENAME_STEM = {
    CLAUDE: "E18_CLAUDE_E18_4_VS_CODEX_V48",
    ANTIGRAVITY: "E18_ANTIGRAVITY_E19_1_VS_CODEX_V48",
    ANTIGRAVITY_V2: "E18_ANTIGRAVITY_E19_2_VS_CODEX_V48",
    COPILOT: "E18_COPILOT_E18_8_V5_VS_CODEX_V48",
    CLAUDE_V5: "E18_CLAUDE_E18_5_VS_CODEX_V48",
}


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pairing_ready(name: str) -> bool:
    return len(list(DERIVED.glob(f"{name}_*.json"))) == 14


def load_pairing(name: str) -> list[dict[str, Any]]:
    paths = sorted(DERIVED.glob(f"{name}_*.json"))
    if len(paths) != 14:
        raise RuntimeError(f"{name}: expected 14 game files, found {len(paths)} in {DERIVED}")
    return [read(p) for p in paths], paths


def economy_table(name: str, candidate: list[dict], codex: list[dict]) -> str:
    cand_cash = [p["reward"] for p in candidate]
    codex_cash = [p["reward"] for p in codex]
    cand_wins = sum(a > b for a, b in zip(cand_cash, codex_cash))
    codex_wins = sum(b > a for a, b in zip(cand_cash, codex_cash))
    ties = 14 - cand_wins - codex_wins
    losses_cand = sum(len(p["ledger"]["animal_escapes"]) for p in candidate)
    losses_codex = sum(len(p["ledger"]["animal_escapes"]) for p in codex)
    rows = [
        ["Cassa finale media", fmt(mean(cand_cash)), fmt(mean(codex_cash))],
        ["Cassa finale mediana", fmt(median(cand_cash)), fmt(median(codex_cash))],
        ["Cassa finale minima", fmt(min(cand_cash)), fmt(min(codex_cash))],
        ["Cassa finale massima", fmt(max(cand_cash)), fmt(max(codex_cash))],
        [
            "Record diretto (14 partite, entrambi i ruoli)",
            f"{cand_wins} vittorie",
            f"{codex_wins} vittorie ({ties} pareggi)",
        ],
        ["Fughe animali verificate (somma 14 partite)", str(losses_cand), str(losses_codex)],
    ]
    label = LABELS[name]
    html = (
        '<div class="tablewrap"><table><tr><th>Misura</th><th>'
        + label
        + "</th><th>Codex V48</th></tr>"
    )
    for row in rows:
        html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    html += "</table></div>"
    return html


def diagnosis(name: str, candidate: list[dict], codex: list[dict]) -> str:
    cand_cash = mean(p["reward"] for p in candidate)
    codex_cash = mean(p["reward"] for p in codex)
    pct = 100.0 * (cand_cash / codex_cash - 1.0) if codex_cash else 0.0
    cand_pass = mean(
        sum(d["requested_actions"].get("PASS", 0) for d in p["ledger"]["daily"]) for p in candidate
    )
    codex_pass = mean(
        sum(d["requested_actions"].get("PASS", 0) for d in p["ledger"]["daily"]) for p in codex
    )
    cand_animals = mean(p["daily"][-1]["occupied_livestock_tiles"] for p in candidate)
    codex_animals = mean(p["daily"][-1]["occupied_livestock_tiles"] for p in codex)
    cand_crops = mean(p["daily"][-1]["crop_tiles"] for p in candidate)
    codex_crops = mean(p["daily"][-1]["crop_tiles"] for p in codex)
    return (
        "<p>Su 14 partite dirette (sette seed di sviluppo, entrambi i ruoli), la candidata "
        f"chiude con cassa media {fmt(cand_cash)} contro {fmt(codex_cash)} di Codex V48 "
        f"({fmt(pct)}%). Il divario non è attribuito a una singola causa da questo solo "
        "confronto: le curve seguenti permettono di leggere insieme colture, bestiame, "
        "servizi e comandi PASS/MOVE giorno per giorno, non solo il risultato finale.</p>"
        f"<p>A fine partita (D30): {fmt(cand_animals)} animali collocati contro "
        f"{fmt(codex_animals)}; {fmt(cand_crops)} caselle coltivate contro {fmt(codex_crops)}. "
        f"PASS medio per partita: {fmt(cand_pass)} contro {fmt(codex_pass)}. Queste cifre sono "
        "osservazioni dirette su questo corpus di 14 partite, non ancora un'attribuzione "
        "causale del divario economico.</p>"
    )


def build_pairing(name: str, template: str) -> Path:
    profiles, paths = load_pairing(name)
    candidate = [p["sides"]["candidate"] for p in profiles]
    codex = [p["sides"]["codex"] for p in profiles]

    payload = dict(
        topLabel="Codex V48 (770)",
        metrics=[dict(key=k, label=l, unit=u) for k, l, u in FIELDS],
        series=dict(candidate=aggregate(candidate), top770=aggregate(codex)),
        aggregation="median/min/max",
        checkpoint="24*D-1, pre-last-batch D1-D29; D30 terminal",
    )
    for series in payload["series"].values():
        for values in series.values():
            assert len(values) == 30 and all(lo <= m <= hi for m, lo, hi in values)

    label = LABELS[name]
    stem = FILENAME_STEM[name]
    datafile = f"{stem}_D01_D30_COMPLETE_KPI.json"
    (REPORT_DIR / datafile).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    result = template
    result = result.replace("770 assistita V1", label)
    result = result.replace("candidate:'770 assistita'", f"candidate:{json.dumps(label)}")
    result = re.sub(
        r'<p class="note">.*?</p>',
        '<p class="note">Partite locali dal vivo, non un confronto con replay esterni: '
        "entrambi i giocatori sono agenti eseguiti realmente nello stesso motore, sugli "
        "stessi sette seed di sviluppo, in entrambi i ruoli. Nessun seed holdout o di "
        "conferma finale consumato.</p>",
        result,
        count=1,
        flags=re.DOTALL,
    )
    assert "Partite locali dal vivo" in result, "note substitution did not match"
    result = re.sub(
        r'<p class="meta">__COHORTS__ · Standard E18 V4\.1 · 7 settembre 2026</p>',
        '<p class="meta">__COHORTS__ · Standard E18 V4.1 · 9 settembre 2026</p>',
        result,
        count=1,
    )
    result = re.sub(
        r"<h2>Diagnosi</h2><p>.*?</p><p>.*?</p>",
        "<h2>Diagnosi</h2>" + diagnosis(name, candidate, codex),
        result,
        count=1,
        flags=re.DOTALL,
    )
    assert "Su 14 partite dirette" in result, "Diagnosi placeholder substitution did not match"

    other_reports = "".join(
        f'<li><a href="{FILENAME_STEM[other]}_D01_D30_COMPLETE_KPI.html">{LABELS[other]} vs Codex V48</a></li>'
        for other in PAIRINGS
        if other != name
    )
    vals = dict(
        TITLE=f"{label} vs Codex V48 · KPI D1-D30",
        COHORTS="14 partite locali dal vivo (7 seed × 2 ruoli)",
        TOP="Codex V48",
        ECONOMY=economy_table(name, candidate, codex),
        PROVENANCE=(
            f"Candidata: {label}. Avversario: Codex V48 "
            "(submission/submission_codex_e18_770_v48_external.py). Seed 180903001-180903007, "
            "entrambi i ruoli. Nessun seed holdout o di conferma finale consumato. "
            f"Altri confronti dello stesso torneo: <ul>{other_reports}</ul>"
        ),
        DATAFILE=datafile,
        DATA=json.dumps(payload, ensure_ascii=False).replace("</", r"<\/"),
    )
    for key, value in vals.items():
        result = result.replace("__" + key + "__", value)
    assert not re.search(r"__[A-Z]+__", result), re.findall(r"__[A-Z]+__", result)

    output = REPORT_DIR / (stem + "_D01_D30_COMPLETE_KPI.html")
    output.write_text(result, encoding="utf-8")
    return output, paths, datafile


def main() -> int:
    template = TEMPLATE.read_text(encoding="utf-8")
    outputs = []
    all_sources: list[Path] = [TEMPLATE, Path(__file__)]
    built: list[str] = []
    skipped: list[str] = []
    for name in PAIRINGS:
        if not pairing_ready(name):
            found = len(list(DERIVED.glob(f"{name}_*.json")))
            print(f"skipping {name}: {found}/14 game files present (tournament still running elsewhere?)")
            skipped.append(name)
            continue
        output, paths, datafile = build_pairing(name, template)
        outputs.append(output)
        all_sources.extend(paths)
        all_sources.append(REPORT_DIR / datafile)
        built.append(name)
        print(output)
    if skipped:
        print(f"built {len(built)}/{len(PAIRINGS)} pairings; skipped (incomplete data): {skipped}")

    manifest = dict(
        standard="E18 V4.1",
        panels=22,
        date="2026-09-09",
        pairings=built,
        skipped_incomplete=skipped,
        opponent="CODEX_V48",
        seeds=[180903001 + i for i in range(7)],
        seats=[0, 1],
        matches_per_pairing=14,
        holdout_consumed=False,
        final_confirmation_consumed=False,
        sources={
            str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in all_sources
        },
        outputs={p.name: sha(p) for p in outputs},
    )
    (REPORT_DIR / "E18_E19_VS_CODEX_V48_TOURNAMENT_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print("manifest written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
