"""Frozen-cohort D1-D30 report; no simulation, download, or policy mutation."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean, median

from docs.model_specs.codex.e18.tools.build_e18_27_top770_complete_kpi import flatten
from docs.model_specs.codex.e18.tools.summarize_e18_29_anti_pass import totals

BASE = Path(__file__).resolve().parents[1]
DERIVED = BASE / "artifacts/derived"
STANDARD = ("money", "people", "crop_tiles", "occupied_livestock_tiles", "COW", "SHEEP", "GOOSE", "empty_pastures", "MELON", "WHEAT", "STRAWBERRY", "CARROT", "TOMATO", "empty_coops", "MOVE", "PASS", "unwatered_tiles_h24", "verified_animal_losses", "weed_tiles", "WATER", "FEED")
EXTRA = ("pass_share", "net_cash_100_slots", "fertilizer_collected", "fertilizer_used")
LABELS = {"candidate": "E18.29 B3", "parent": "E18.28 C", "top770": "Top770"}
REASONS = ("exhausted", "calendar", "prerequisite", "extra_wait")
CHART_COHORTS = ("candidate", "top770")


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def pass_reasons(profile, day):
    c = profile["anti_daily"][str(day)]
    result = {
        "exhausted": c.get("baseline_pass_NO_MORE_PRODUCTIVE_TASKS_TODAY", 0) - c.get("missions_started", 0),
        "calendar": c.get("baseline_pass_WAIT_FOR_SCHEDULED_TURN", 0),
        "prerequisite": c.get("baseline_pass_BLOCKED_DUE_TASK", 0),
        "extra_wait": c.get("extra_PASS", 0),
    }
    assert min(result.values()) >= 0
    assert sum(result.values()) == profile["operational_daily"][day-1]["PASS"]
    return result


def daily_rows(profile, operational, *, fertilizer_available):
    assert len(profile["daily"]) == len(operational) == len(profile["ledger"]["daily"]) == 30
    rows = []
    for i in range(30):
        ledger = profile["ledger"]["daily"][i]
        commands = sum(ledger["requested_actions"].values())
        net = (sum(ledger["sales_cash"].values()) - sum(ledger["purchase_cash"].values())
               - ledger["hire_cash"] - ledger["land_cash"] + ledger["unit_cash_delta"])
        row = flatten(profile["daily"][i]) | operational[i]
        row.update(pass_share=100 * ratio(ledger["requested_actions"].get("PASS", 0), commands),
                   net_cash_100_slots=100 * ratio(net, commands),
                   WATER=ledger["executed_actions"].get("WATER", 0),
                   FEED=ledger["executed_actions"].get("FEED", 0),
                   fertilizer_used=ledger["executed_actions"].get("FERTILIZE", 0))
        if fertilizer_available:
            row["fertilizer_collected"] = profile["fertilizer_daily"][i].get("collected", 0)
        rows.append({k: row[k] for k in (*STANDARD, *EXTRA) if k in row})
    return rows


def aggregate(profiles):
    keys = set.intersection(*(set(p[0]) for p in profiles))
    return {k: [[median(v), min(v), max(v)] for v in [[p[i][k] for p in profiles] for i in range(30)]] for k in (*STANDARD, *EXTRA) if k in keys}


def build_dataset():
    sources = {}

    def read(name):
        path = DERIVED / name
        sources[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        payload = json.loads(path.read_text(encoding="utf-8"))
        if "matches" in payload and "complete" in payload:
            assert payload["complete"]
        return payload

    candidates = read("E18_29_ANTI_PASS_SMOKE_B3_V3.json")["matches"] + read("E18_29_ANTI_PASS_DEVELOPMENT_B3_V3.json")["matches"]
    parents = [p for p in read("E18_29_ANTI_PASS_DEVELOPMENT_V1.json")["matches"] if p["variant"] == "PARENT"]
    top = read("E18_26_JESSE_770_D01_D30_CLOSURE.json")["jesse"]
    top_ops = {p["episode_id"]: p["daily"] for p in read("TOP770_D01_D30_OPERATIONAL_KPI.json")["profiles"]}
    summary = read("E18_29_ANTI_PASS_SUMMARY.json")
    checked_parent = read("E18_29_ANTI_PASS_PARENT_CROP_CHECK_V3.json")["matches"][0]
    earlier_trials = read("E18_28_FULL_SEASON_SUMMARY.json")["rejected_progressive"]
    assert len(candidates) == len(parents) == 14 and len(top) == 5
    assert {(p["seed"], p["seat"]) for p in candidates} == {(p["seed"], p["seat"]) for p in parents}
    assert len({(p["seed"], p["seat"]) for p in candidates}) == 14
    assert all(p["opponent"] == "E18.16" for p in candidates + parents)
    assert all(p["variant"] == "B3" for p in candidates)
    groups = {"candidate": candidates, "parent": parents, "top770": top}
    rows = {name: [daily_rows(p, top_ops[p["episode_id"]] if name == "top770" else p["operational_daily"], fertilizer_available=name != "top770") for p in profiles] for name, profiles in groups.items()}
    reason_profiles = [[pass_reasons(p, day) for day in range(1,31)] for p in candidates]
    reasons = [{"day": day+1, **{k: mean(p[day][k] for p in reason_profiles) for k in REASONS}} for day in range(30)]
    operational = {}
    for name, profiles in groups.items():
        counters = [totals(p) for p in profiles]
        commands = [sum(d["requested_actions"].values()) for p in profiles for d in p["ledger"]["daily"]]
        operational[name] = {
            "n": len(profiles), "cash_mean": mean(p["terminal"]["cash"] for p in profiles),
            "cash_median": median(p["terminal"]["cash"] for p in profiles),
            "commands_mean": sum(commands)/len(profiles),
            "pass_mean": mean(c["requested_actions:PASS"] for c in counters),
            "pass_share_pooled": 100*sum(c["requested_actions:PASS"] for c in counters)/sum(commands),
            "move_mean": mean(c["requested_actions:MOVE"] for c in counters),
            "operational_requested_mean": mean(sum(d["requested_actions"].values()) - d["requested_actions"].get("PASS",0) - d["requested_actions"].get("MOVE",0) for p in profiles for d in p["ledger"]["daily"])*30,
            "feed_mean": mean(c["executed_actions:FEED"] for c in counters),
            "water_mean": mean(c["executed_actions:WATER"] for c in counters),
            "care_mean": mean(c["executed_actions:CARE"] for c in counters),
            "fertilize_mean": mean(c["executed_actions:FERTILIZE"] for c in counters),
            "fertilizer_collected_mean": None if name == "top770" else mean(c["fertilizer:collected"] for c in counters),
            "fertilizer_sold_mean": mean(c["sold_units:FERTILIZER"] for c in counters),
            "hire_cost_mean": mean(c["hire_cash"] for c in counters),
            "crop_tile_days_mean": mean(sum(r["crop_tiles"] for r in p["daily"]) for p in profiles),
            "weed_tile_days_mean": mean(sum(r["weed_tiles"] for r in rr) for rr in rows[name]),
        }
    extra = Counter()
    for p in candidates:
        for day in p["anti_daily"].values():
            extra.update(day)
    moves = sum(extra["extra_"+d] for d in ("NORTH","SOUTH","EAST","WEST"))
    missions = {"started": extra["missions_started"], "completed": extra["missions_completed"],
                "collected_units": extra["collection_ack_units"], "extra_moves": moves,
                "moves_per_collected_unit_pooled": ratio(moves, extra["collection_ack_units"]),
                "completion_rate": ratio(extra["missions_completed"], extra["missions_started"])}
    exceptions = [{"seed":p["seed"],"seat":p["seat"],**e} for p in candidates for e in p["crop_starvation"]]
    windows = {}
    for first, last in ((15,30), (16,30), (25,30)):
        window = {}
        for name, profiles in groups.items():
            ledgers = [p["ledger"]["daily"][first-1:last] for p in profiles]
            passes = [sum(d["requested_actions"].get("PASS",0) for d in days) for days in ledgers]
            commands = sum(sum(d["requested_actions"].values()) for days in ledgers for d in days)
            window[name] = {"pass_mean":mean(passes), "pass_per_day_mean":mean(passes)/(last-first+1),
                            "pass_share_pooled":100*sum(passes)/commands,
                            "water_mean":mean(sum(d["executed_actions"].get("WATER",0) for d in days) for days in ledgers),
                            "feed_mean":mean(sum(d["executed_actions"].get("FEED",0) for d in days) for days in ledgers)}
        windows[f"D{first}-D{last}"] = window
    parent_by_case = {(p["seed"],p["seat"]):p for p in parents}
    cows = {
        "solution_validated":False,
        "candidate_cows_d1_d10":[median(p["daily"][i]["animals"].get("COW",0) for p in candidates) for i in range(10)],
        "top770_cows_d1_d10":[median(p["daily"][i]["animals"].get("COW",0) for p in top) for i in range(10)],
        "candidate_parent_cash_d1_d11_identical":all(p["daily"][i]["money"]==parent_by_case[(p["seed"],p["seat"])]["daily"][i]["money"] for p in candidates for i in range(11)),
        "rejected_trials":[{"variant":p["variant"],"seed":p["seed"],"seat":p["seat"],"cash":p["reward"],"cows_d1_d10":p["cows_d1_d10"],"animal_losses":len(p["losses"])} for pp in earlier_trials.values() for p in pp],
        "interpretation":"B3 leaves early cash/cow trajectory unchanged; extra cash from D12 cannot fund D3-D9. Earlier D/E attempts failed animal safety, not proof that every progressive schedule is infeasible."
    }
    payload = {
        "analysis_id": "E18_29_B3_SIMULATION_REPORT_D01_D30_V2",
        "report_standard": "V3: 21 standard panels plus 4 diagnostic additions; Top770 vs candidate only; no PASS reasons chart",
        "chart_cohorts":CHART_COHORTS,
        "series": {name: aggregate(rr) for name,rr in rows.items()},
        "profile_daily": {name:[{"identity": (p.get("seed"),p["seat"],p.get("episode_id")),"daily":rr} for p,rr in zip(groups[name],rows[name])] for name in groups},
        "cohorts": {"candidate":{"n":14,"seeds":sorted({p["seed"] for p in candidates}),"seats":[0,1],"opponent":"E18.16"}, "parent":{"n":14,"matched_to":"candidate"},"top770":{"n":5,"episodes":[p["episode_id"] for p in top],"filter":"final-770", "frozen":True}},
        "pass_reasons": {"n":14,"daily_mean":reasons,"total_mean":{k:sum(r[k] for r in reasons) for k in REASONS},"unrecoverable_not_proven":True},
        "operational":operational,"extra_missions":missions,"crop_exceptions":exceptions,
        "pass_windows":windows,"progressive_cows":cows,
        "crop_safety_coverage":{"candidate":"14/14 audited", "parent":"1 selected case audited, not a representative rate", "top770":"N/D"},
        "checked_parent_crop_events":checked_parent["crop_starvation"],
        "economic_gate_passed":summary["economic_gate_passed"],"release_gate_passed":summary["development_passed"],
        "matched_delta":summary["mean_delta"],"sources":sources,
        "checkpoint":"H24 pre-last batch D1-D29; D30 terminal. Flows attributed to pre-action day.",
        "comparison":"E18.29/E18.28 matched; Top770 descriptive, different prices/seeds/opponents. Bands are observed min-max, not confidence intervals.",
        "new_kpi_definitions":{"WATER":"successful WATER per execution day, all units, not commands or unwatered stock", "FEED":"successful FEED per execution day, all units, not commands or animal stock", "pass_share":"100 PASS/requested unit commands, ratio per profile/day; chart median/range", "net_cash_100_slots":"100*(sales-purchases-hires-land+unit cash change)/requested unit commands, includes investments", "fertilizer_collected":"engine-verified actual inventory gain; Top770 missing", "fertilizer_used":"successful FERTILIZE, one unit each", "pass_reasons":"Raw diagnostic data only; chart removed by owner. Actual PASS partition, not proof of economically recoverable work."},
    }
    return payload


def report_markdown(data):
    def fmt(v):
        return "N/D" if v is None else f"{v:,.2f}".translate(str.maketrans({",":".",".":","}))
    lines = ["# E18.29 B3 — report della simulazione D1–D30", "",
             "[Grafici interattivi: Top770 vs E18.29 B3, 21 standard + 4 diagnostici](E18_29_B3_SIMULATION_REPORT_D01_D30.html)", "",
             "Revisione V2 del report: due sole serie, nessun diagramma Cause PASS, WATER/FEED riusciti al giorno aggiunti. Il confronto matched con E18.28 rimane esclusivamente nelle tabelle. Standard corrente: `experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V3_IT.md`.", "",
             "E18.29 B3 ed E18.28 C: 14 profili matched, sette seed × due seat contro E18.16. Top770: cinque replay final-770 congelati, confronto descrittivo, non una rilevazione aggiornata della leaderboard. Nessuna nuova simulazione o modifica della policy per generare questo report.", "",
             "Grafici standard: mediana puntuale e min-max osservato. Non sono intervalli di confidenza; una mediana non è una partita reale. Stock H24 D1–D29 prima dell'ultimo batch, D30 terminale. MOVE, PASS e flussi usano la giornata dell'azione.", "",
             "Le tile non irrigate al checkpoint non sono automaticamente deadline mancate o colture morte: possono non richiedere WATER quel giorno oppure riceverlo nell'ultimo batch. Il delta fra checkpoint della cassa non coincide necessariamente con il flusso del giorno del ledger. I 14 profili comprendono due seat per seed, non 14 seed indipendenti.", "",
             "## Sintesi operativa", "", "| KPI | E18.29 B3 · n14 | E18.28 C · n14 | Top770 · n5 |", "|---|---:|---:|---:|"]
    labels = {"cash_mean":"Cassa finale media ($)","cash_median":"Cassa finale mediana ($)","commands_mean":"Comandi unità / partita", "pass_mean":"PASS / partita", "pass_share_pooled":"PASS / 100 comandi (rapporto dei totali)", "move_mean":"MOVE / partita", "operational_requested_mean":"Altre azioni richieste / partita (non prova di utilità)","feed_mean":"FEED riusciti", "water_mean":"WATER riusciti", "care_mean":"CARE riusciti", "fertilize_mean":"FERTILIZE riusciti", "fertilizer_collected_mean":"Fertilizzante raccolto, verificato", "fertilizer_sold_mean":"Fertilizzante venduto", "hire_cost_mean":"Costo manodopera ($)", "crop_tile_days_mean":"Crop tile-days ai checkpoint", "weed_tile_days_mean":"WEED tile-days ai checkpoint"}
    for key,label in labels.items():
        lines.append(f"| {label} | "+" | ".join(fmt(data["operational"][s][key]) for s in LABELS)+" |")
    lines += ["", "## KPI aggiunti e perché", "",
              "1. Quota PASS: distingue inattività e semplice aumento del numero di lavoratori. Il grafico è giornaliero, la tabella usa il rapporto dei totali.",
              "2. WATER e FEED giornalieri: azioni riuscite, sommate su tutte le unità. Distinti dalle richieste e dalle consistenze. I totali sono riconciliati con il ledger operativo. Nessun diagramma Cause PASS; i contatori restano solo nei derivati per audit.",
              "3. Flusso netto per 100 comandi: ricavi meno acquisti, personale, terra e più variazioni monetarie delle azioni. Include investimenti; non è il rendimento marginale di un singolo lavoratore o un premio per ridurre gli slot.",
              "4. Fertilizzante raccolto: quantità realmente acquisita, non numero di comandi. Per Top770 il dato verificato è assente: N/D, mai zero.",
              "5. Fertilizzante utilizzato: FERTILIZE riusciti. Permette di vedere se la raccolta extra alimenta i boost del piano, oltre alla vendita.", "",
              "WATER/FEED entrano nello standard comune V3 su richiesta del proprietario. Quota PASS, flusso netto e fertilizzante raccolto/utilizzato restano quattro approfondimenti aggiuntivi.", "",
              "## PASS: miglioramento parziale, gap ancora aperto", "",
              "Totali medi per partita nella finestra, non somma delle mediane. Quota PASS = rapporto dei totali PASS/comandi. Le finestre si sovrappongono e non vanno sommate.", "",
              "| Finestra | E18.29 PASS | E18.28 PASS | Top770 PASS | E18.29 quota % | Top770 quota % |",
              "|---|---:|---:|---:|---:|---:|"]
    for label, values in data["pass_windows"].items():
        lines.append(f"| {label} | {fmt(values['candidate']['pass_mean'])} | {fmt(values['parent']['pass_mean'])} | {fmt(values['top770']['pass_mean'])} | {fmt(values['candidate']['pass_share_pooled'])} | {fmt(values['top770']['pass_share_pooled'])} |")
    gap = data["pass_windows"]["D15-D30"]
    lines += ["", f"Da D15 a D30 la B3 riduce i PASS del {fmt(100*(1-gap['candidate']['pass_mean']/gap['parent']['pass_mean']))}% contro il parent, ma resta al {fmt(100*(gap['candidate']['pass_mean']/gap['top770']['pass_mean']-1))}% sopra Top770. È una riduzione, non la risoluzione del problema. I cohort Top770 sono diversi: questo gap è descrittivo, non una stima causale del profitto perso.", "",
              "## Mucche progressive: risorse non ancora validate", "",
              "La B3 mantiene la sequenza D1–D10 2,2,2,2,4,4,4,4,4,9. La cassa D1–D11 coincide con quella del parent in tutti i 14 profili; i nuovi incassi iniziano D12, quindi non finanziano retroattivamente D3–D9. Non esiste ancora una soluzione validata di crescita progressiva.", "",
              "I tentativi precedenti D/E, smoke seed180903001 in entrambi i seat, arrivavano a 8 Cow D10 e perdevano una Sheep al refresh D11→D12. D chiudeva a 74.300, E a 69.912, contro C 77.898. La disponibilità nominale per comprare non dimostra la copertura di mangime, pickup, PLACE e FEED. Questi tentativi non dimostrano che una progressione sicura sia impossibile, ma non sono adottabili.", "",
              "Prossimo esperimento proposto, non eseguito in questo report: bilancio impegnato D1–D10 con riserve separate per hire/semi/mangime, costo e slot completi BUY→PICKUP→PLACE→FEED, e anticipi ammessi solo con servizio garantito. Misurare cow-days, ricavi latte, acquisti mangime, PASS/MOVE e sicurezza; testare gli stessi seed/seat interni, senza nuovi dati pubblici per il tuning.", "",
              "## Missioni extra: tabella di controllo", "",
              f"Su tutti i 14 profili: {data['extra_missions']['started']} missioni iniziate, {data['extra_missions']['completed']} completate; {data['extra_missions']['collected_units']} unità raccolte. {fmt(data['extra_missions']['moves_per_collected_unit_pooled'])} MOVE extra per unità raccolta (rapporto dei totali). Il costo MOVE delle missioni non coincide con il delta totale di MOVE: cambiano anche le azioni del piano a valle.", "",
              "## Guasti: non affidarsi alla sola mediana", "",
              "La mediana delle morti crop è zero, ma un evento esiste. I casi individuali e l'incidenza vanno sempre riportati accanto alle traiettorie aggregate.", "",
              "| Seed | Seat | Giorno di servizio | Tile (x,y, base 0) | Coltura | Esito |", "|---|---:|---:|---|---|---|"]
    for e in data["crop_exceptions"]:
        lines.append(f"| {e['seed']} | {e['seat']} | D{e['service_day']} | {tuple(e['position'])} | {e['crop']} | morte per sete verificata al refresh |")
    lines += ["", "E18.29: 1/14 profili con morte crop (7,14%). Lo stesso evento D12 è stato verificato nel parent selezionato; gli altri 13 parent non hanno questo audit specifico salvato. Non confrontare 1/1 parent con 1/14 candidata come tassi rappresentativi. Top770: N/D per questa diagnosi. Gate economico positivo; gate assoluto zero morti crop non superato.", "",
              "## Telemetria da aggiungere al prossimo simulatore", "",
              "Priorità 1: deadline PLANT→primo WATER e FEED, ritardo in turni, numero di task scaduti e minimo margine della coda; separare richiesti, eseguiti e confermati. Questo è il KPI più utile per prevenire il difetto D12.",
              "Priorità 2: copertura Wheat in obbligazioni FEED finanziate e prelievi per-worker; copertura di cassa di hire/feed/semi già impegnati. Cash assoluto non prova che una missione sia finanziabile.",
              "Priorità 3: latenza e quantità HARVEST→DROP→SELL per prodotto, compresi residui e perdite da shed pieno. Serve una provenienza di lotti: non è identificabile esattamente dai soli saldi aggregati.",
              "Priorità 4: distribuzione della saturazione e del margine residuo per worker, non solo media della squadra; visualizzare code che sforano accanto a worker inattivi.", "",
              "Non aggiungerei punteggi sintetici o un 'profitto per tile' ottenuto assegnando arbitrariamente costi condivisi: renderebbero meno chiara l'attribuzione causale.", "",
              "## Diagnosi e riproducibilità", "",
              "Il beneficio anti-PASS è concentrato D16–D30; D7–D11 rimane sostanzialmente invariato. Più fertilizzante rende eseguibili fertilizzazioni prima saltate. L'assegnazione delle code ai due ultimi hands corregge il ritardo D21; il difetto ereditato PLANT→WATER D12 resta la priorità prima di un rilascio.", "",
              "La scomposizione suggerisce due indagini distinte: D7 prevale l'attesa calendario (circa 51,6 PASS/partita); D8–D10 prevalgono code proprie esaurite (102, 94 e 103,1 PASS/partita). Per D7 va verificato il vincolo temporale; per D8–D10 la distribuzione e la copertura del lavoro. Non basta aggiungere missioni: prima bisogna dimostrare che esistano attività finanziabili, utili e chiudibili entro le deadline.", "",
              "[Report economico e ablation](E18_29_ANTI_PASS_DEVELOPMENT_REPORT_IT.md) · [Tentativi di mucche progressive](E18_28_FULL_SEASON_REPORT_IT.md) · [Model spec V3](../MODEL_SPEC_CODEX_E18_29_770_ANTI_PASS_V3.md). Dati e SHA-256 delle fonti: `../artifacts/derived/E18_29_B3_SIMULATION_REPORT_D01_D30_V2.json`. Il report non dipende dai download grezzi Kaggle.", "",
              "Rigenerazione: `python -m docs.model_specs.codex.e18.tools.build_e18_29_simulation_report --fragment <percorso-assoluto.html>`, poi il renderer visualize sul frammento per l'export HTML. Test: `pytest docs/model_specs/codex/e18/tests/test_e18_29_simulation_report.py`.", "",
              "QA della revisione: test dati e vincolo due serie; controllo a 360 e 736 px, light/dark. Esito separato: `../artifacts/derived/E18_29_SIMULATION_REPORT_QA_V2.json`. L'audit V1 rimane storico e non certifica questa revisione."]
    return "\n".join(lines)+"\n"


def render_fragment(payload):
    template = (BASE / "tools/templates/e18_29_simulation_report.html").read_text(encoding="utf-8")
    chart_series = {key:payload["series"][key] for key in CHART_COHORTS}
    fragment = template.replace("__REPORT_SERIES__", json.dumps(chart_series, separators=(",",":")))
    assert "__REPORT_" not in fragment and "__PASS_REASONS__" not in fragment
    assert len(fragment.encode()) < 1_000_000
    return fragment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fragment", type=Path, required=True)
    args = parser.parse_args()
    payload = build_dataset()
    output = DERIVED / (payload["analysis_id"]+".json")
    output.write_text(json.dumps(payload, indent=2)+"\n", encoding="utf-8")
    fragment = render_fragment(payload)
    args.fragment.write_text(fragment, encoding="utf-8")
    (BASE / "reports/E18_29_SIMULATION_REPORT_IT.md").write_text(report_markdown(payload), encoding="utf-8")
    print(json.dumps({"dataset":str(output),"fragment":str(args.fragment),"charts":25,"chart_cohorts":CHART_COHORTS,"profile_days":990}))


if __name__ == "__main__":
    main()
