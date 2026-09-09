#!/usr/bin/env python3
"""Build 22-panel D1-D30 KPI reports (E18 standard V4.1) comparing, per
development line, the newest draft against the previous version and
against Codex V48 in a single three-way dashboard.

Reuses the live paired-match profiles already produced by
run_e19_vs_codex_v48_paired_kpi.py (each candidate vs Codex V48, 14 games:
7 development seeds x 2 seats) -- no new candidate-vs-candidate matches are
run. New and old never played each other directly in this corpus; only
each one's own matches against the same external reference (Codex V48, on
the same seven development seeds) are available, so the Codex series shown
here is the pool of both candidates' Codex-side games (28 total) rather
than either pairing's Codex side alone -- documented in each report's note
and provenance so it reads as a shared-opponent comparison, not a round
robin.

Standard: experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V4_IT.md
Template: experiments/e18/tools/common/complete_kpi_template_3way.html
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
TEMPLATE = ROOT / "experiments/e18/tools/common/complete_kpi_template_3way.html"

LINES = ("ANTIGRAVITY", "CLAUDE", "COPILOT")

NEW_NAME = {
    "ANTIGRAVITY": "ANTIGRAVITY_E19_2",
    "CLAUDE": "CLAUDE_E18_5",
    "COPILOT": "COPILOT_E18_10_V6",
}
OLD_NAME = {
    "ANTIGRAVITY": "ANTIGRAVITY_E19_1",
    "CLAUDE": "CLAUDE_E18_4",
    "COPILOT": "COPILOT_E18_8_V5",
}
NEW_LABEL = {
    "ANTIGRAVITY": "Antigravity E19.2 Hybrid Livestock",
    "CLAUDE": "Claude E18.5 Wheat-Market-Fix",
    "COPILOT": "Copilot E18.10 Economic Recovery V6",
}
OLD_LABEL = {
    "ANTIGRAVITY": "Antigravity E19.1 Hybrid Livestock",
    "CLAUDE": "Claude E18.4 Capacity-Certified",
    "COPILOT": "Copilot E18.8 Economic Recovery V5",
}
FILENAME_STEM = {
    "ANTIGRAVITY": "E18_ANTIGRAVITY_E19_2_VS_E19_1_VS_CODEX_V48",
    "CLAUDE": "E18_CLAUDE_E18_5_VS_E18_4_VS_CODEX_V48",
    "COPILOT": "E18_COPILOT_E18_10_VS_E18_8_VS_CODEX_V48",
}
SOURCE_PATH = {
    "ANTIGRAVITY_E19_2": "src/agricola/strategy/antigravity/antigravity_e19_2_hybrid_livestock.py",
    "ANTIGRAVITY_E19_1": "src/agricola/strategy/antigravity/antigravity_e19_hybrid_livestock_v1.py",
    "CLAUDE_E18_5": "src/agricola/strategy/claude/e18_wheat_market_fix_v5.py",
    "CLAUDE_E18_4": "src/agricola/strategy/claude/e18_capacity_certified_v4.py",
    "COPILOT_E18_10_V6": "src/agricola/strategy/copilot/e18_economic_recovery_v6.py",
    "COPILOT_E18_8_V5": "src/agricola/strategy/copilot/e18_economic_recovery_v5.py",
}


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_pairing(name: str) -> tuple[list[dict[str, Any]], list[Path]]:
    paths = sorted(DERIVED.glob(f"{name}_*.json"))
    if len(paths) != 14:
        raise RuntimeError(f"{name}: expected 14 game files, found {len(paths)} in {DERIVED}")
    return [read(p) for p in paths], paths


def economy_table(new_label: str, old_label: str, new_c: list[dict], old_c: list[dict], codex_pool: list[dict]) -> str:
    new_cash = [p["reward"] for p in new_c]
    old_cash = [p["reward"] for p in old_c]
    codex_cash = [p["reward"] for p in codex_pool]
    new_codex_cash = codex_cash[:14]
    old_codex_cash = codex_cash[14:]
    new_wins = sum(a > b for a, b in zip(new_cash, new_codex_cash))
    old_wins = sum(a > b for a, b in zip(old_cash, old_codex_cash))
    new_losses = sum(len(p["ledger"]["animal_escapes"]) for p in new_c)
    old_losses = sum(len(p["ledger"]["animal_escapes"]) for p in old_c)
    codex_losses = sum(len(p["ledger"]["animal_escapes"]) for p in codex_pool)
    rows = [
        ["Cassa finale media", fmt(mean(new_cash)), fmt(mean(old_cash)), fmt(mean(codex_cash))],
        ["Cassa finale mediana", fmt(median(new_cash)), fmt(median(old_cash)), fmt(median(codex_cash))],
        ["Cassa finale minima", fmt(min(new_cash)), fmt(min(old_cash)), fmt(min(codex_cash))],
        ["Cassa finale massima", fmt(max(new_cash)), fmt(max(old_cash)), fmt(max(codex_cash))],
        [
            "Record diretto vs Codex V48 (14 partite proprie, entrambi i ruoli)",
            f"{new_wins} vittorie",
            f"{old_wins} vittorie",
            "—",
        ],
        ["Fughe animali verificate (somma delle proprie 14 partite)", str(new_losses), str(old_losses), str(codex_losses)],
    ]
    html = (
        '<div class="tablewrap"><table><tr><th>Misura</th><th>'
        + new_label
        + "</th><th>"
        + old_label
        + "</th><th>Codex V48 (pool 28)</th></tr>"
    )
    for row in rows:
        html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    html += "</table></div>"
    return html


def diagnosis(new_label: str, old_label: str, new_c: list[dict], old_c: list[dict], codex_pool: list[dict]) -> str:
    new_cash = mean(p["reward"] for p in new_c)
    old_cash = mean(p["reward"] for p in old_c)
    codex_cash = mean(p["reward"] for p in codex_pool)
    pct_new_vs_old = 100.0 * (new_cash / old_cash - 1.0) if old_cash else 0.0
    pct_new_vs_codex = 100.0 * (new_cash / codex_cash - 1.0) if codex_cash else 0.0
    pct_old_vs_codex = 100.0 * (old_cash / codex_cash - 1.0) if codex_cash else 0.0

    def d30_animals(group: list[dict]) -> float:
        return mean(p["daily"][-1]["occupied_livestock_tiles"] for p in group)

    def d30_crops(group: list[dict]) -> float:
        return mean(p["daily"][-1]["crop_tiles"] for p in group)

    def mean_pass(group: list[dict]) -> float:
        return mean(sum(d["requested_actions"].get("PASS", 0) for d in p["ledger"]["daily"]) for p in group)

    return (
        f"<p>Confronto a tre vie su partite dal vivo contro Codex V48, stessi sette seed di "
        f"sviluppo, entrambi i ruoli (14 partite per candidata, 28 partite Codex in totale: "
        f"{new_label} non ha giocato direttamente contro {old_label} in questo corpus). "
        f"Cassa media: {fmt(new_cash)} ({new_label}, nuova) contro {fmt(old_cash)} "
        f"({old_label}, precedente) contro {fmt(codex_cash)} (Codex V48, pool). "
        f"Nuova vs precedente: {fmt(pct_new_vs_old)}%. Nuova vs Codex: {fmt(pct_new_vs_codex)}%. "
        f"Precedente vs Codex: {fmt(pct_old_vs_codex)}%.</p>"
        f"<p>A fine partita (D30): {fmt(d30_animals(new_c))} animali collocati (nuova) contro "
        f"{fmt(d30_animals(old_c))} (precedente) contro {fmt(d30_animals(codex_pool))} (Codex); "
        f"{fmt(d30_crops(new_c))} caselle coltivate (nuova) contro {fmt(d30_crops(old_c))} "
        f"(precedente) contro {fmt(d30_crops(codex_pool))} (Codex). PASS medio per partita: "
        f"{fmt(mean_pass(new_c))} (nuova) / {fmt(mean_pass(old_c))} (precedente) / "
        f"{fmt(mean_pass(codex_pool))} (Codex). Osservazioni dirette su questo corpus, non "
        "ancora un'attribuzione causale del divario economico.</p>"
    )


def build_line(line: str, template: str) -> tuple[Path, list[Path], str]:
    new_name = NEW_NAME[line]
    old_name = OLD_NAME[line]
    new_profiles, new_paths = load_pairing(new_name)
    old_profiles, old_paths = load_pairing(old_name)

    new_candidate = [p["sides"]["candidate"] for p in new_profiles]
    old_candidate = [p["sides"]["candidate"] for p in old_profiles]
    codex_pool = [p["sides"]["codex"] for p in new_profiles] + [p["sides"]["codex"] for p in old_profiles]

    new_label = NEW_LABEL[line]
    old_label = OLD_LABEL[line]

    payload = dict(
        newLabel=new_label,
        oldLabel=old_label,
        metrics=[dict(key=k, label=l, unit=u) for k, l, u in FIELDS],
        series=dict(new=aggregate(new_candidate), old=aggregate(old_candidate), codex=aggregate(codex_pool)),
        aggregation="median/min/max",
        checkpoint="24*D-1, pre-last-batch D1-D29; D30 terminal",
    )
    for series in payload["series"].values():
        for values in series.values():
            assert len(values) == 30 and all(lo <= m <= hi for m, lo, hi in values)

    stem = FILENAME_STEM[line]
    datafile = f"{stem}_D01_D30_COMPLETE_KPI.json"
    (REPORT_DIR / datafile).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    result = template
    vals = dict(
        TITLE=f"{new_label} vs {old_label} vs Codex V48 · KPI D1-D30",
        COHORTS="28 partite locali dal vivo (nuova: 14 vs Codex; precedente: 14 vs Codex; 7 seed x 2 ruoli ciascuna)",
        NEWLABEL=new_label,
        OLDLABEL=old_label,
        NOTE=(
            "Partite locali dal vivo, non un confronto con replay esterni: ogni candidata ha "
            "giocato le proprie 14 partite contro Codex V48 (stessi sette seed di sviluppo, "
            f"entrambi i ruoli). {new_label} e {old_label} non si sono affrontate direttamente "
            "in questo corpus; la serie Codex V48 qui mostrata è il pool delle 28 partite Codex "
            "(14 contro la nuova, 14 contro la precedente), non una singola serie appaiata. "
            "Nessun seed holdout o di conferma finale consumato."
        ),
        ECONOMY=economy_table(new_label, old_label, new_candidate, old_candidate, codex_pool),
        DIAGNOSIS=diagnosis(new_label, old_label, new_candidate, old_candidate, codex_pool),
        PROVENANCE=(
            f"Nuova: {new_label} ({SOURCE_PATH[new_name]}). Precedente: {old_label} "
            f"({SOURCE_PATH[old_name]}). Avversario: Codex V48 "
            "(submission/submission_codex_e18_770_v48_external.py). Seed 180903001-180903007, "
            "entrambi i ruoli, per ciascuna candidata separatamente. Nessun seed holdout o di "
            "conferma finale consumato."
        ),
        DATAFILE=datafile,
        DATA=json.dumps(payload, ensure_ascii=False).replace("</", r"<\/"),
    )
    for key, value in vals.items():
        result = result.replace("__" + key + "__", value)
    assert not re.search(r"__[A-Z]+__", result), re.findall(r"__[A-Z]+__", result)

    output = REPORT_DIR / (stem + "_D01_D30_COMPLETE_KPI.html")
    output.write_text(result, encoding="utf-8")
    return output, new_paths + old_paths, datafile


def main() -> int:
    template = TEMPLATE.read_text(encoding="utf-8")
    outputs = []
    all_sources: list[Path] = [TEMPLATE, Path(__file__)]
    built: list[str] = []
    skipped: list[str] = []
    for line in LINES:
        new_name = NEW_NAME[line]
        old_name = OLD_NAME[line]
        have_new = len(list(DERIVED.glob(f"{new_name}_*.json")))
        have_old = len(list(DERIVED.glob(f"{old_name}_*.json")))
        if have_new != 14 or have_old != 14:
            print(f"skipping {line}: new={have_new}/14 ({new_name}), old={have_old}/14 ({old_name})")
            skipped.append(line)
            continue
        output, paths, datafile = build_line(line, template)
        outputs.append(output)
        all_sources.extend(paths)
        all_sources.append(REPORT_DIR / datafile)
        built.append(line)
        print(output)
    if skipped:
        print(f"built {len(built)}/{len(LINES)} lines; skipped (incomplete data): {skipped}")

    manifest = dict(
        standard="E18 V4.1",
        panels=22,
        comparison="new_vs_old_vs_codex_v48",
        date="2026-09-09",
        lines=built,
        skipped_incomplete=skipped,
        new_name=NEW_NAME,
        old_name=OLD_NAME,
        opponent="CODEX_V48",
        codex_pool_size=28,
        seeds=[180903001 + i for i in range(7)],
        seats=[0, 1],
        matches_per_candidate=14,
        holdout_consumed=False,
        final_confirmation_consumed=False,
        sources={str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in all_sources},
        outputs={p.name: sha(p) for p in outputs},
    )
    (REPORT_DIR / "E18_NEW_VS_OLD_VS_CODEX_V48_TOURNAMENT_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print("manifest written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
