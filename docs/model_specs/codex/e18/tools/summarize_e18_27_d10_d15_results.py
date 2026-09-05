"""Consolidate completed matched E18.27 gates without rerunning simulations."""

from __future__ import annotations

import json
import statistics
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUTPUT = BASE / "artifacts/derived/E18_27_D10_D15_CONSOLIDATED_V3.json"
REPORT = BASE / "reports/E18_27_D10_D15_CONSOLIDATED_V3_REPORT_IT.md"


def cash_after_actions(profile, day):
    cash = profile["ledger"]["initial_cash"]
    for row in profile["ledger"]["daily"][:day]:
        cash += (
            sum(row["sales_cash"].values())
            - sum(row["purchase_cash"].values())
            - row["hire_cash"]
            - row["land_cash"]
            + row["unit_cash_delta"]
        )
    return cash


def main():
    sources = {
        label: json.loads(
            (BASE / f"artifacts/derived/E18_27_D10_D15_{label}_V3.json").read_text()
        )
        for label in ("SMOKE", "DEVELOPMENT", "V4D")
    }
    assert all(p["complete"] for p in sources.values()), (
        "Wait for all preregistered comparisons."
    )
    # DEVELOPMENT repeats smoke seed 1 against E18.16. Count it once.
    matches = {}
    pairs = {}
    for source in sources.values():
        for m in source["matches"]:
            key = (m["version"], m["opponent"], m["seed"], m["seat"])
            if key in matches:
                assert matches[key]["reward"] == m["reward"]
                assert matches[key]["prefix_d1_d9_sha256"] == m["prefix_d1_d9_sha256"]
                assert matches[key]["daily"] == m["daily"]
            matches[key] = m
        for p in source["pairs"]:
            key = (p["opponent"], p["seed"], p["seat"])
            if key in pairs:
                assert pairs[key] == p
            pairs[key] = p
    groups = []
    for opponent in ("E18.16", "E18.25", "E18.2/V4D"):
        rows = [p for p in pairs.values() if p["opponent"] == opponent]
        candidate = [
            m
            for m in matches.values()
            if m["version"] == "E18.27" and m["opponent"] == opponent
        ]
        parent_mean = statistics.mean(p["parent_reward"] for p in rows)
        candidate_mean = statistics.mean(p["candidate_reward"] for p in rows)
        groups.append(
            {
                "opponent": opponent,
                "paired_cases": len(rows),
                "parent_mean": parent_mean,
                "candidate_mean": candidate_mean,
                "delta_mean": candidate_mean - parent_mean,
                "delta_percent": 100 * (candidate_mean / parent_mean - 1),
                "positive_pairs": sum(p["delta"] > 0 for p in rows),
                "worst_delta": min(p["delta"] for p in rows),
                "best_delta": max(p["delta"] for p in rows),
                "opponent_mean_against_candidate": statistics.mean(
                    m["opponent_reward"] for m in candidate
                ),
                "candidate_wins": sum(
                    m["reward"] > m["opponent_reward"] for m in candidate
                ),
                "checks": {
                    k: all(p["checks"][k] for p in rows) for k in rows[0]["checks"]
                },
            }
        )
    temporal = []
    for day in range(10, 16):
        row = {"day": day}
        for version in ("E18.26", "E18.27"):
            profiles = [
                m
                for m in matches.values()
                if m["version"] == version
                and m["opponent"] == "E18.16"
                and m["seed"] == 180903001
            ]
            stats = [m["daily"][day - 1] for m in profiles]
            row[version] = {
                "cash_h24": statistics.median(s["money"] for s in stats),
                "cash_after_all_day_actions": statistics.median(
                    cash_after_actions(m, day) for m in profiles
                ),
                "people": statistics.median(s["people"] for s in stats),
                "strawberry": statistics.median(
                    s["crops"]["STRAWBERRY"] for s in stats
                ),
                "crop_tiles": statistics.median(s["crop_tiles"] for s in stats),
                "animals": statistics.median(
                    s["occupied_livestock_tiles"] for s in stats
                ),
            }
        temporal.append(row)
    checks = {
        k: all(p["checks"][k] for p in pairs.values())
        for k in next(iter(pairs.values()))["checks"]
    }
    candidate_matches = [m for m in matches.values() if m["version"] == "E18.27"]
    incomplete_crops = [
        {
            "opponent": m["opponent"],
            "seed": m["seed"],
            "seat": m["seat"],
            "D15": m["daily"][14]["crops"],
        }
        for m in candidate_matches
        if m["daily"][14]["crop_tiles"] != 61
    ]
    incomplete_animals = [
        {
            "opponent": m["opponent"],
            "seed": m["seed"],
            "seat": m["seat"],
            "D10": m["daily"][9]["animals"],
            "D15": m["daily"][14]["animals"],
            "D30": m["daily"][29]["animals"],
        }
        for m in candidate_matches
        if m["daily"][29]["occupied_livestock_tiles"] != 14
    ]
    payload = {
        "candidate": "E18.27 V3",
        "incomplete_crop_cases": incomplete_crops,
        "incomplete_livestock_cases": incomplete_animals,
        "groups": groups,
        "unique_matches": len(matches),
        "unique_paired_cases": len(pairs),
        "checks": checks,
        "temporal_smoke_vs_e18_16": temporal,
        "animal_escapes": sum(
            len(m["ledger"]["animal_escapes"]) for m in candidate_matches
        ),
        "technical_errors": sum(m["errors"] for m in candidate_matches),
        "holdout_consumed": False,
        "kaggle_upload_authorized": False,
        "sources": {k: f"E18_27_D10_D15_{k}_V3.json" for k in sources},
        "status": "DEVELOPMENT_PROGRESS_NOT_PROMOTED",
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# E18.27 V3 — risultati consolidati D10-D15",
        "",
        "Candidata development, non promossa. Topologia 770, cap 14, massimo 12 hands. Chiusura D30 non modificata.",
        "",
        f"{len(pairs)} casi matched unici, {len(matches)} episodi unici (parent e candidata). Lo smoke seed 1 ripetuto nella matrice development è verificato identico e deduplicato.",
        "",
        "## Confronti economici interni",
        "",
        "Le prime due colonne sono le prestazioni del parent e della candidata contro lo stesso avversario: non sono il punteggio dell'avversario. Tutti i seed sono development già preregistrati.",
        "",
        "| Avversario | Casi matched | E18.26 media | E18.27 V3 media | Delta | Delta % | Casi positivi | Avversario contro V3, media | Vittorie V3 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for g in groups:
        lines.append(
            f"| {g['opponent']} | {g['paired_cases']} | {g['parent_mean']:.1f} | {g['candidate_mean']:.1f} | {g['delta_mean']:+.1f} | {g['delta_percent']:+.2f}% | {g['positive_pairs']}/{g['paired_cases']} | {g['opponent_mean_against_candidate']:.1f} | {g['candidate_wins']}/{g['paired_cases']} |"
        )
    lines += [
        "",
        "## Traiettoria D10-D15",
        "",
        "Seed 180903001, entrambi i seat contro E18.16, mediane. Nelle coppie E18.26 / E18.27 V3. H24 è il checkpoint storico; la colonna successiva include anche l'ultimo batch della giornata, registrato nel primo stato del giorno dopo.",
        "",
        "| D | Cassa H24 | Cassa dopo tutte le azioni D | Persone | Strawberry | Crop totali | Animali H24 |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in temporal:
        keys = (
            "cash_h24",
            "cash_after_all_day_actions",
            "people",
            "strawberry",
            "crop_tiles",
            "animals",
        )
        lines.append(
            f"| {row['day']} | "
            + " | ".join(f"{row['E18.26'][k]:g} / {row['E18.27'][k]:g}" for k in keys)
            + " |"
        )
    lines += [
        "",
        "## Diagnosi dell'effetto",
        "",
        "V1 anticipa HARVEST a D11: elimina le fughe nello smoke, ma vende in D12 e resta a 29 Strawberry. V2 completa DROP+SELL in D11 e attiva tutte le semine Q2 in D12, ma altera richieste di acquisto antecedenti D10 tramite l'orizzonte futuro. V3 mantiene il piano V2 e congela il fabbisogno futuro del mercato al parent fino a D9: il prefisso viene verificato come action stream completo, non soltanto come consistenze.",
        "",
        "Sul seed 180903001 contro E18.16, V3 raccoglie/vende 71 Melon nelle azioni D11, incassando 12.445. Il checkpoint H24 è 3.956, ma dopo l'ultimo batch D11 la cassa è 10.321: l'ultimo incasso non va attribuito erroneamente a un nuovo giorno produttivo. Rispetto al parent viene sacrificata una sola unità Melon, mantenendo la copertura FEED e finanziando l'attivazione di 38 Strawberry in D12. Il target D15 è 38 Strawberry + 23 Wheat e 9 Cow + 5 Sheep.",
        "",
        "Non è stata aggiunta una politica generale di refill: la candidata previene le fughe osservate; una risposta economica a perdite forzate resta da testare separatamente. Neppure una riserva finanziaria universale è stata dimostrata: l'evidenza riguarda questo trattamento e questi avversari/seed.",
        "",
        "## Gate",
        "",
        "```json",
        json.dumps(checks, indent=2),
        "```",
        "",
        "Il planner espone ancora due FAIL legacy: picco 62 crop entro D13 (61 a D15) e output shadow almeno 885 (868). I vincoli di sicurezza, legalità e fattibilità passano; quei due target non vengono cancellati né convertiti silenziosamente in PASS. La candidata va giudicata anche sugli esiti reali matched, senza promuoverla soltanto perché supera E18.26.",
        "",
        "## Prossima fase e limiti",
        "",
        "La matrice estesa non ripete tutti i PASS dello smoke: nel seed 180903004 (entrambi i seat) e nel 180903005 seat 1 restano 37 Strawberry invece di 38 a D15. Nel seed 180903007 entrambi i seat arrivano a D10 con un animale già mancante e terminano con 9 Cow + 4 Sheep: nessuna fuga, ma acquisizione/placement non recuperato. Questi casi sono enumerati nel dataset consolidato.",
        "",
        "Contro E18.16, i seed 180903003 e 180903004 sono negativi in entrambi i seat; worst delta -21.920. Nel seed 4 seat 0 la candidata è avanti di 1.115 a D15 e 2.164 a D20, ma perde 14.504 a fine partita. In D16-D30 vende 144 Milk contro 96 incassando 10.148 contro 20.442, e 142 Strawberry contro 116 incassando 8.703 contro 16.057. Il volume Wheat venduto scende da 353 a 316. Il vantaggio si deteriora già D20-D25: non basta attribuire tutto all'ultimo giorno o alla sola quantità prodotta. Offerta, prezzi realizzati e risposta avversaria richiedono ulteriore separazione causale.",
        "",
        "Il miglioramento del parent non prova superiorità su E18.16 o E18.2/V4D: usare le colonne del confronto diretto e i relativi gate. E18.2/V4D è controllo competitivo storico con topologia diversa, non un benchmark architetturale omogeneo né una proposta di cambiare la 770. Lo smoke contro V4D usa un solo seed, non sette.",
        "",
        "Nessuna submission, promozione, holdout/final confirmation, commit o push. La chiusura D30 resta una seconda fase: missioni complete di raccolta/consegna/vendita prima del taglio hands, valorizzazione dei residui e cutoff basati sul ritorno entro il termine. Conservare le ablation e verificare che eventuali nuove modifiche non riaprano il divario D10-D15.",
        "",
        f"Dataset consolidato: `{OUTPUT.name}`.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {"groups": groups, "checks": checks, "report": str(REPORT)}, indent=2
        )
    )


if __name__ == "__main__":
    main()
