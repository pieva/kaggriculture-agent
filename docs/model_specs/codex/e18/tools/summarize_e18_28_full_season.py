"""Freeze paired economic evidence, including negative ablations."""

import json
import statistics
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DERIVED = BASE / "artifacts/derived"


def cash_parts(profile, start=1):
    days = profile["ledger"]["daily"][start - 1 :]
    result = Counter()
    for day in days:
        for field in (
            "sales_cash",
            "purchase_cash",
            "harvested",
            "sold_units",
            "planted",
        ):
            for item, quantity in day[field].items():
                result[f"{field}:{item}"] += quantity
        for field in ("hire_cash", "land_cash", "unit_cash_delta"):
            result[field] += day[field]
    return result


def main():
    cases = json.loads(
        (DERIVED / "E18_28_FULL_SEASON_DEVELOPMENT_BC.json").read_text()
    )["matches"]
    parents = json.loads((DERIVED / "E18_27_D10_D15_DEVELOPMENT_V3.json").read_text())[
        "matches"
    ]
    groups = {
        v: {(p["seed"], p["seat"]): p for p in cases if p["variant"] == v}
        for v in ("B", "C")
    }
    groups["PARENT"] = {
        (p["seed"], p["seat"]): p
        for p in parents
        if p["version"] == "E18.27" and p["opponent"] == "E18.16"
    }
    assert all(len(g) == 14 for g in groups.values())
    summaries = {}
    for v, group in groups.items():
        profiles = list(group.values())
        reward = [p["reward"] for p in profiles]
        economic = [cash_parts(p) for p in profiles]
        summaries[v] = {
            "n": len(profiles),
            "mean_reward": statistics.mean(reward),
            "min_reward": min(reward),
            "max_reward": max(reward),
            "direct_wins": sum(p["reward"] > p["opponent_reward"] for p in profiles),
            "mean_opponent_reward": statistics.mean(
                p["opponent_reward"] for p in profiles
            ),
            "mean_30d_economic_parts": {
                k: statistics.mean(c[k] for c in economic)
                for k in sorted(set().union(*economic))
            },
        }
    comparisons = []
    for key in sorted(groups["C"]):
        p, b, c = (groups[v][key] for v in ("PARENT", "B", "C"))
        assert c["errors"] == c["opponent_errors"] == 0
        assert c["ledger"]["cash_parity_errors"] == 0
        assert not c["ledger"]["animal_escapes"]
        assert c["max_resources"] <= 14 and c["max_hands"] <= 12
        assert not c["lower_quadrant_structure_observations"]
        assert all(r["people"] == 13 for r in c["daily"][24:])
        assert all(
            not c["terminal"][k]
            for k in ("shed", "carried", "seeds", "tile_yield_units")
        ), (key, c["terminal"])
        cb, cc = cash_parts(b), cash_parts(c)
        delta = {k: cc[k] - cb[k] for k in sorted(set(cb) | set(cc)) if cc[k] != cb[k]}
        net = (
            sum(v for k, v in delta.items() if k.startswith("sales_cash:"))
            - sum(v for k, v in delta.items() if k.startswith("purchase_cash:"))
            - delta.get("hire_cash", 0)
            - delta.get("land_cash", 0)
            + delta.get("unit_cash_delta", 0)
        )
        assert net == c["reward"] - b["reward"], (key, delta)
        comparisons.append(
            {
                "seed": key[0],
                "seat": key[1],
                "parent": p["reward"],
                "B": b["reward"],
                "C": c["reward"],
                "C_minus_parent": c["reward"] - p["reward"],
                "C_minus_B": net,
                "C_minus_B_cash_parts": delta,
            }
        )
    rejected = {}
    for label in ("SMOKE_PROGRESSIVE", "SMOKE_PROGRESSIVE_E"):
        profiles = json.loads(
            (DERIVED / f"E18_28_FULL_SEASON_{label}.json").read_text()
        )["matches"]
        rejected[label] = [
            {
                "variant": p["variant"],
                "seed": p["seed"],
                "seat": p["seat"],
                "reward": p["reward"],
                "cows_d1_d10": [r["animals"]["COW"] for r in p["daily"][:10]],
                "losses": p["ledger"]["animal_escapes"],
            }
            for p in profiles
        ]
    payload = {
        "selected": "C",
        "incumbent_promoted": False,
        "holdout_consumed": False,
        "summaries": summaries,
        "comparisons": comparisons,
        "rejected_progressive": rejected,
        "safe_zero_terminal_inventory_all_14": True,
    }
    output = DERIVED / "E18_28_FULL_SEASON_SUMMARY.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# E18.28 C — verifica full-season 770",
        "",
        "2026-09-05. Candidata diagnostica quotidiana, non promossa a incumbent. Matrice development: 7 seed × 2 seat, stesso avversario E18.16; nessun holdout. Confronto Top770 pubblico/locale descrittivo, non causale (mercati e avversari diversi).",
        "",
        "## Risultati economici matched",
        "",
        "| Variante | Cassa finale media | Min–max | Vittorie su E18.16 |",
        "|---|---:|---:|---:|",
    ]
    for v in ("PARENT", "B", "C"):
        s = summaries[v]
        lines.append(
            f"| {v} | {s['mean_reward']:,.2f} | {s['min_reward']:,.0f}–{s['max_reward']:,.0f} | {s['direct_wins']}/14 |"
        )
    lines.extend(
        [
            "",
            "| Seed | Seat | Parent E18.27 V3 | B Wheat | C Carrot | C−parent | C−B |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for r in comparisons:
        lines.append(
            f"| {r['seed']} | {r['seat']} | {r['parent']:,.0f} | {r['B']:,.0f} | {r['C']:,.0f} | {r['C_minus_parent']:+,.0f} | {r['C_minus_B']:+,.0f} |"
        )
    delta_mean = statistics.mean(r["C_minus_parent"] for r in comparisons)
    lines += [
        "",
        f"C guadagna {delta_mean:,.2f} ({delta_mean / summaries['PARENT']['mean_reward']:.2%}) sul parent, minimo {min(r['C_minus_parent'] for r in comparisons):+,.0f}. C−B medio +2.148; due seed hanno delta negativo: nessuna regola condizionata al seed è stata introdotta.",
        "",
        "## Carote: attribuzione economica B/C",
        "",
        "Stesso calendario nominale, route e servizio; cambia la specie delle nuove semine D26-D28. Tabella seguente: flussi medi dell'intera partita (i delta B/C derivano dal trattamento tardivo). I prezzi reagiscono anche alle nostre vendite: ricavi per specie non equivalgono a prezzi esogeni.",
        "",
        "| Voce | B Wheat | C Carrot | Delta C−B |",
        "|---|---:|---:|---:|",
    ]
    keys = sorted(
        set(summaries["B"]["mean_30d_economic_parts"])
        | set(summaries["C"]["mean_30d_economic_parts"])
    )
    for k in keys:
        b = summaries["B"]["mean_30d_economic_parts"].get(k, 0)
        c = summaries["C"]["mean_30d_economic_parts"].get(k, 0)
        if b != c or k == "hire_cash":
            lines.append(f"| {k} | {b:,.2f} | {c:,.2f} | {c - b:+,.2f} |")
    lines += [
        "",
        "Tutti i delta di cassa sono riconciliati con vendite/acquisti/personale/terra/azioni. A D30: zero prodotti su tile, nello shed o trasportati, zero semi residui in tutti i 14 casi C. Non è un aumento puramente contabile delle consistenze.",
        "",
        "## Traiettoria e sicurezza",
        "",
        "12 hands + farmer mantenuti D25-D30 in tutti i casi C. Nuovi annuali D26-D28, raccolti a età 3 o 2 al terminale, prenotazione rotte entro H23 D30, nessun DIG finale senza resa. D1-D24 congelato rispetto a E18.27 V3, compreso il lookahead di mercato. Nel seed smoke le crop H24 D25-D30 sono 61,60,58,61,23,0 (parent 61,51,39,29,0,0). Anche Top770 liquida D29-D30: mantenere produzione fino a D30 non significa lasciare crop invendute al terminale.",
        "",
        "Zero errori, fughe, violazioni cap 14/max 12 hands e strutture nel quadrante agricolo in tutti i 14 casi. Resta il posto Sheep vuoto ereditato sul seed 180903007. La candidata perde 13/14 contro E18.16; smoke E18.2/V4D 60.612 contro 85.329 in entrambi i seat. Vantaggio sul parent, non dimostrazione di competitività da top.",
        "",
        "## Apertura progressiva: tentativi respinti",
        "",
        "D anticipa Q0 a D3/D5 e Q1 a D8/D9/D10. E posticipa la terza Cow a D4 e attiva JIT/inflight da D1. Entrambi perdono una Sheep nello smoke: rispettivamente cassa 74.300 e 69.912 contro C 77.898. L'anticipo altera cash disponibile, pickup e servizio FEED; il piano nominale non basta. La release C conserva l'apertura a step. Il requisito della crescita progressiva resta aperto, non viene dichiarato implementato.",
        "",
        "## Report standard a 19 pannelli",
        "",
        "Cassa, persone, totale crop/animali, tutte le 5 colture e 3 specie, pascoli/COOP vuoti, MOVE e PASS per giornata, non irrigate H24, perdite animali verificate, WEED H24. Mancata irrigazione nel grafico è uno stato di servizio: H24 D1-D29 precede l'ultimo batch e non prova un danno o una scadenza mancata. WEED non significa automaticamente sete (esaurimento e spawn casuale sono distinti). Linea mediana, fascia min-max osservata; C n=14, Top770 n=5, campione pubblico final-770 congelato.",
        "",
        "Grafici: `E18_28_TOP770_D01_D30_KPI_19.html`. Dati: `../artifacts/derived/E18_28_C_TOP770_D01_D30_KPI_19.json`. Standard comune: `experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V2_IT.md`.",
        "",
        "## Rilascio e conservazione",
        "",
        "Standalone stdlib-only, source hash e piano nel manifest; parity 719 azioni per seat e loader file Kaggle, 27 test unitari/regressione superati. Il dossier dei 22 download riscaricabili conserva URL, ID, seed, reward, SHA-256 e dimensione; i derivati restano. NEW_SESSION/PROJECT_STATE, pulizia conclusiva e Git sono differiti ai primi cicli esterni. Nessuna promozione automatica o tuning sullo score iniziale.",
    ]
    (BASE / "reports/E18_28_FULL_SEASON_REPORT_IT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output": str(output), "summaries": summaries}, indent=2))


if __name__ == "__main__":
    main()
