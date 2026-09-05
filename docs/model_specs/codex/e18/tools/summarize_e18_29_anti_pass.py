"""Evidence-backed economic and safety verdict for the anti-PASS development."""

import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean

BASE = Path(__file__).resolve().parents[1]
DERIVED = BASE / "artifacts/derived"


def load(label):
    path = DERIVED / f"E18_29_ANTI_PASS_{label}.json"
    payload = json.loads(path.read_text())
    assert payload["complete"] and not payload["failures"], path
    return path, payload["matches"]


def totals(profile):
    result = Counter()
    for day in profile["ledger"]["daily"]:
        for field in (
            "sales_cash",
            "purchase_cash",
            "sold_units",
            "bought_units",
            "harvested",
            "executed_actions",
            "requested_actions",
        ):
            for item, units in day[field].items():
                result[f"{field}:{item}"] += units
        for field in ("hire_cash", "land_cash", "unit_cash_delta"):
            result[field] += day[field]
    for day in profile.get("fertilizer_daily", []):
        for field in ("collected", "delivered", "drop_destroyed", "used"):
            result["fertilizer:" + field] += day.get(field, 0)
    return result


def compare(profiles):
    parents = {
        (p["opponent"], p["seed"], p["seat"]): p
        for p in profiles
        if p["variant"] == "PARENT"
    }
    rows = []
    for child in profiles:
        if child["variant"] == "PARENT":
            continue
        parent = parents[(child["opponent"], child["seed"], child["seat"])]
        ct, pt = totals(child), totals(parent)
        delta = {
            k: ct[k] - pt[k] for k in sorted(ct.keys() | pt.keys()) if ct[k] != pt[k]
        }
        net = (
            sum(v for k, v in delta.items() if k.startswith("sales_cash:"))
            - sum(v for k, v in delta.items() if k.startswith("purchase_cash:"))
            - delta.get("hire_cash", 0)
            - delta.get("land_cash", 0)
            + delta.get("unit_cash_delta", 0)
        )
        assert net == child["reward"] - parent["reward"]
        safe = all(
            [
                child["statuses"] == ["DONE", "DONE"],
                child["errors"] == child["opponent_errors"] == 0,
                child["ledger"]["cash_parity_errors"] == 0,
                not child["ledger"]["animal_escapes"],
                child["max_resources"] <= 14,
                child["max_hands"] <= 12,
                child["daily"][-1]["pasture_topology"]
                == {"Q0": 7, "Q1": 7, "Q2": 0, "Q3": 0},
                not child["lower_quadrant_structure_observations"],
                child["incomplete_missions"] == 0,
                child["prefix_d1_d6_sha256"] == parent["prefix_d1_d6_sha256"],
                all(
                    not child["terminal"][k]
                    for k in ("shed", "carried", "seeds", "tile_yield_units")
                ),
                ct["fertilizer:drop_destroyed"] <= pt["fertilizer:drop_destroyed"],
                child["variant"] not in {"B2", "B3"}
                or child.get("crop_starvation") == [],
            ]
        )
        if child["variant"] == "OFF":
            assert child["actions_sha256"] == parent["actions_sha256"] and net == 0
        rows.append(
            dict(
                variant=child["variant"],
                opponent=child["opponent"],
                seed=child["seed"],
                seat=child["seat"],
                parent=parent["reward"],
                candidate=child["reward"],
                delta=net,
                safe=safe,
                parent_pass=pt["requested_actions:PASS"],
                candidate_pass=ct["requested_actions:PASS"],
                parent_move=pt["requested_actions:MOVE"],
                candidate_move=ct["requested_actions:MOVE"],
                economic_delta=delta,
            )
        )
    return rows


def main():
    sources, groups, comparisons = {}, {}, {}
    for label in ("SMOKE_V1", "DEVELOPMENT_V1", "INTERNAL_E2_V1"):
        path, profiles = load(label)
        sources[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        groups[label] = profiles
        comparisons[label] = compare(profiles)
    for label in ("SMOKE_B3_V3", "DEVELOPMENT_B3_V3", "INTERNAL_E2_B3_V3"):
        path, profiles = load(label)
        sources[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        groups[label] = profiles
    for label in ("SMOKE_B2_V2", "PARENT_CROP_CHECK_V3"):
        path, profiles = load(label)
        sources[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        groups[label] = profiles
    parents = [p for p in groups["DEVELOPMENT_V1"] if p["variant"] == "PARENT"]
    candidates = groups["SMOKE_B3_V3"] + groups["DEVELOPMENT_B3_V3"]
    assert len({(p["seed"], p["seat"]) for p in candidates}) == len(candidates) == 14
    groups["SELECTED_DEVELOPMENT"] = parents + candidates
    comparisons["SELECTED_DEVELOPMENT"] = compare(parents + candidates)
    e2parents = [p for p in groups["INTERNAL_E2_V1"] if p["variant"] == "PARENT"]
    comparisons["SELECTED_E2"] = compare(e2parents + groups["INTERNAL_E2_B3_V3"])
    dev = comparisons["SELECTED_DEVELOPMENT"]
    assert len(dev) == 14 and all(r["variant"] == "B3" for r in dev)
    passed = all(r["safe"] and r["delta"] > 0 for r in dev)
    passed = passed and all(r["safe"] for r in comparisons["SELECTED_E2"])
    baseline_crop_check = groups["PARENT_CROP_CHECK_V3"][0]
    baseline_cached = next(p for p in parents if (p["seed"], p["seat"]) == (baseline_crop_check["seed"], baseline_crop_check["seat"]))
    assert baseline_cached["actions_sha256"] == baseline_crop_check["actions_sha256"]
    candidate_checked = next(p for p in candidates if (p["seed"], p["seat"]) == (baseline_crop_check["seed"], baseline_crop_check["seat"]))
    summary = dict(
        development_passed=passed,
        economic_gate_passed=all(r["delta"] > 0 for r in dev),
        best_development_variant="B3",
        selected="B3" if passed else None,
        rejected_variant_B="Economic improvement, but extra water death in the instrumented seed180903001 seat0 (D21 service / D22 display)",
        B2_verdict="REJECTED_BEHAVIORALLY_INERT_SMOKE_ONLY",
        checked_crop_case={"seed": baseline_crop_check["seed"], "seat": baseline_crop_check["seat"], "parent": baseline_crop_check["crop_starvation"], "B3": candidate_checked["crop_starvation"]},
        incumbent_promoted=False,
        submitted=False,
        holdout_consumed=False,
        sources=sources,
        comparisons=comparisons,
        mean_delta=mean(r["delta"] for r in dev),
        min_delta=min(r["delta"] for r in dev),
    )
    lines = [
        "# E18.29 B3 — anti-PASS con protezione del servizio",
        "",
        "2026-09-05. Parent E18.28 C pubblicata (56036993), topologia 770 invariata.",
        "Development: sette seed × due seat contro E18.16; non sono 14 seed indipendenti.",
        "Controllo aggiuntivo E18.2/V4D su un seed × due seat. Nessun holdout o upload.",
        "",
        "## Intervento",
        "",
        "Missioni aggiuntive solo quando il worker ha terminato tutti i task produttivi del giorno e ha inventario vuoto: raccolta fertilizzante disponibile, consegna allo shed, rientro alla posizione iniziale. Prenotazione tile e budget completo entro H23; nessun nuovo acquisto, hire, semina o cambio calendario. Il mercato parent può vendere il surplus o usarlo al posto degli acquisti previsti.",
        "",
        "OFF riproduce tutti i 719 batch del parent in entrambi i seat. A isola D7-D12; B estende D7-D30. Lo smoke iniziale è conservato; prima dell'estensione si è aggiunta una guardia prudenziale per gli inventari degli altri worker presso lo shed e l'audit delle consegne effettive.",
        "",
        "B migliorava tutti i 14 profili (+5.577,43 medi), ma è stata fermata: il fertilizzante aggiuntivo rende eseguibili boost prima saltati, riducendo il margine della coda. Nel caso diagnosticato PLANT Wheat slittava a D21 H24, senza WATER, causando morte al refresh. Il tentativo B2 di saltare FERTILIZE è risultato inerte: il worker interessato non aveva tale task. La traccia completa rivela invece due MOVE aggiuntivi per lo spawn differente di M11, con mangime già disponibile. B3 confronta le due assegnazioni delle code dei due ultimi hands appena assunti e le scambia solo se questo permette a entrambe di rispettare la scadenza. Nessuna regola condizionata a seed o coordinate. L'audit delle morti per sete viene eseguito in ogni match B3.",
        "",
        "## KPI medi development",
        "",
        "| KPI | E18.28 C | E18.29 B3 | Delta |",
        "|---|---:|---:|---:|",
    ]
    profiles = groups["SELECTED_DEVELOPMENT"]
    grouped = {v: [p for p in profiles if p["variant"] == v] for v in ("PARENT", "B3")}
    metrics = [
        ("Cassa finale", lambda p: p["reward"]),
        ("PASS", lambda p: totals(p)["requested_actions:PASS"]),
        ("MOVE", lambda p: totals(p)["requested_actions:MOVE"]),
        ("Fertilizzante raccolto", lambda p: totals(p)["fertilizer:collected"]),
        ("Fertilizzante consegnato", lambda p: totals(p)["fertilizer:delivered"]),
        ("Fertilizzante venduto", lambda p: totals(p)["sold_units:FERTILIZER"]),
        (
            "Fertilizzante acquistato",
            lambda p: totals(p)["bought_units:BUY_PRODUCT:FERTILIZER"],
        ),
        ("Fertilizzante utilizzato", lambda p: totals(p)["fertilizer:used"]),
        ("Costo manodopera", lambda p: totals(p)["hire_cash"]),
        ("FEED eseguiti", lambda p: totals(p)["executed_actions:FEED"]),
        ("WATER eseguiti", lambda p: totals(p)["executed_actions:WATER"]),
    ]
    summary["kpi_means"] = {}
    for label, getter in metrics:
        p, c = [mean(getter(r) for r in grouped[v]) for v in ("PARENT", "B3")]
        summary["kpi_means"][label] = {"parent": p, "candidate": c, "delta": c - p}
        lines.append(f"| {label} | {p:,.2f} | {c:,.2f} | {c - p:+,.2f} |")
    lines += [
        "",
        "## Esiti matched",
        "",
        "| Seed | Seat | Parent | B3 | Delta | Sicurezza |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for r in dev:
        lines.append(
            f"| {r['seed']} | {r['seat']} | {r['parent']:,.0f} | {r['candidate']:,.0f} | {r['delta']:+,.0f} | {'PASS' if r['safe'] else 'FAIL'} |"
        )
    lines += [
        "",
        "## Attribuzione economica",
        "",
        "I flussi sono rieseguiti nel motore esatto e riconciliati con la cassa finale in tutti i 719 batch di entrambi i giocatori. La differenza comprende gli effetti endogeni su disponibilità e prezzi; non attribuire tutto l'aumento al prezzo iniziale del fertilizzante.",
        "",
        "| Voce | Delta medio |",
        "|---|---:|",
    ]
    for key in sorted(set().union(*(r["economic_delta"] for r in dev))):
        if key.startswith(("sales_cash:", "purchase_cash:")) or key in (
            "hire_cash",
            "land_cash",
            "unit_cash_delta",
        ):
            value = mean(r["economic_delta"].get(key, 0) for r in dev)
            if value:
                lines.append(f"| {key} | {value:+,.2f} |")
    lines += [
        "",
        "## Andamento temporale",
        "",
        "| Giorni | PASS parent | PASS B3 | MOVE parent | MOVE B3 |",
        "|---|---:|---:|---:|---:|",
    ]
    for start, end in [(1, 6), (7, 12), (13, 15), (16, 24), (25, 30)]:
        values = [
            mean(
                sum(d[field] for d in p["operational_daily"][start - 1 : end])
                for p in grouped[v]
            )
            for field in ("PASS", "MOVE")
            for v in ("PARENT", "B3")
        ]
        lines.append(
            f"| D{start}–D{end} | " + " | ".join(f"{v:,.2f}" for v in values) + " |"
        )
    lines += [
        "",
        "## Controllo E18.2/V4D",
        "",
        "| Seat | Parent | B3 | Delta | Sicurezza |",
        "|---|---:|---:|---:|---|",
    ]
    for r in comparisons["SELECTED_E2"]:
        lines.append(
            f"| {r['seat']} | {r['parent']:,.0f} | {r['candidate']:,.0f} | {r['delta']:+,.0f} | {'PASS' if r['safe'] else 'FAIL'} |"
        )
    lines += [
        "",
        "## Verdetto e limiti",
        "",
        f"Gate economico: {'PASS' if summary['economic_gate_passed'] else 'FAIL'}; gate completo di sicurezza: {'PASS' if passed else 'FAIL'}. Delta medio {summary['mean_delta']:+,.2f}; peggiore {summary['min_delta']:+,.0f}. Nessuna promozione automatica a incumbent.",
        "",
        f"Verifica crop nel caso seed {baseline_crop_check['seed']} seat {baseline_crop_check['seat']}: parent {baseline_crop_check['crop_starvation']}; B3 {candidate_checked['crop_starvation']}. La riesecuzione parent ha gli stessi 719 batch del parent congelato. Il criterio preregistrato di zero morti per sete rimane assoluto: un eventuale difetto ereditato non viene nascosto né trasformato retroattivamente in un PASS del gate.",
        "",
        "Prima del rilascio va risolta la missione PLANT→WATER di D12 già difettosa nel parent: prenotare e confermare l'irrigazione iniziale insieme alla semina. Questo primo intervento non risolve il sottoutilizzo iniziale né ripristina le giornate CARE escluse dal piano. Successivamente, in ablation separate: accorpare le raccolte compatibili in giri multi-tile e valutare CARE soltanto dove il bonus sarà prodotto, raccolto e venduto entro D30. I MOVE aumentano per la logistica aggiuntiva; il beneficio va giudicato sulla cassa netta, non su PASS=0.",
        "",
        "Artefatti, strumenti e test sono sotto docs/model_specs/codex/e18. NEW_SESSION/PROJECT_STATE, pulizia cache e Git restano distinti e differiti al workflow di verifica dell'upload E18.28. Nessuna nuova submission in questo sviluppo.",
    ]
    before_B = {
        (p["seed"], p["seat"]): p
        for p in groups["DEVELOPMENT_V1"]
        if p["variant"] == "B"
    }
    summary["B3_minus_B_mean"] = mean(
        p["reward"] - before_B[(p["seed"], p["seat"])]["reward"] for p in candidates
    )
    summary["direct_wins"] = {
        v: sum(p["reward"] > p["opponent_reward"] for p in grouped[v])
        for v in ("PARENT", "B3")
    }
    summary["crop_starvation_B3"] = sum(len(p["crop_starvation"]) for p in candidates)
    summary["B3_fresh_worker_route_swap_mean"] = mean(
        sum(d.get("fresh_worker_route_swap", 0) for d in p["anti_daily"].values())
        for p in candidates
    )
    lines += [
        "",
        f"B3−B medio: {summary['B3_minus_B_mean']:+,.2f}; scambi di code ai nuovi hands: {summary['B3_fresh_worker_route_swap_mean']:.2f} per partita. Vittorie dirette su E18.16: parent {summary['direct_wins']['PARENT']}/14, B3 {summary['direct_wins']['B3']}/14. Il miglioramento matched non equivale a dominare il campione interno.",
    ]
    (DERIVED / "E18_29_ANTI_PASS_SUMMARY.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (BASE / "reports/E18_29_ANTI_PASS_DEVELOPMENT_REPORT_IT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                k: summary[k]
                for k in ("development_passed", "mean_delta", "min_delta", "kpi_means")
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
