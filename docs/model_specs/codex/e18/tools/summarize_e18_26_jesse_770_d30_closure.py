"""Build macro closure report from the saved cash-verified D30 dataset."""
from __future__ import annotations
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import OUTPUT, REPORT, aggregates


def total(rows, key):
    out = Counter()
    for row in rows:
        out.update(row[key])
    return dict(out)


def distribution(values):
    return {"median": statistics.median(values), "min": min(values), "max": max(values)}


def number(value):
    return f"{value:,.1f}".rstrip("0").rstrip(".").replace(",", "_").replace(".", ",").replace("_", ".")


def display(stat):
    return number(stat["median"]) + (f" [{number(stat['min'])}–{number(stat['max'])}]" if stat["min"] != stat["max"] else "")


def summarize(payload):
    phase = {}
    for cohort in ("jesse", "codex"):
        phase[cohort] = []
        for p in payload[cohort]:
            late = p["ledger"]["daily"][20:]
            last = p["ledger"]["daily"][-1]
            phase[cohort].append({"identity": p["identity"],
                "sold_units": total(late, "sold_units"), "sales_cash": total(late, "sales_cash"),
                "harvested": total(late, "harvested"), "planted": total(late, "planted"),
                "actions": total(late, "requested_actions"), "executed": total(late, "executed_actions"),
                "empty_pasture_checkpoints_d14_d30": sum(sum(r["pasture_topology"].values())-r["animals"]["COW"]-r["animals"]["SHEEP"] for r in p["daily"][13:]),
                "cash_growth_h24_d20_d30": p["daily"][-1]["money"]-p["daily"][19]["money"],
                "cash_flow_day30": sum(last["sales_cash"].values())-sum(last["purchase_cash"].values())-last["hire_cash"]-last["land_cash"]+last["unit_cash_delta"],
                "hires_cash_d21_d30": sum(row["hire_cash"] for row in late)})
    payload["macro_closure"] = phase
    payload["aggregates"] = {cohort: aggregates(payload[cohort]) for cohort in ("jesse", "codex")}
    return payload


def write_report(payload):
    summarize(payload)
    agg, phases = payload["aggregates"], payload["macro_closure"]
    lines = ["# Jesse 770 / E18.26 — traiettorie e valorizzazione D1-D30", "",
        "Coorte invariata: Jesse 105405557, 105384058, 105398563, 105391568, 105565293; E18.26 BoostD10 contro E18.16, seed development 180903001, entrambi i seat. Topologia finale pasture 7-7-0; nessuna policy modificata.", "",
        "## Metodo e verifiche", "",
        "30 checkpoint H24 per profilo (indice 24 × D − 1). Cassa = farm.money; a D30 coincide esattamente con il reward. Personale = hands assunti + farmer, inclusi gli agenti fuori griglia. Campioni, hash, reward e dati D1-D20 coincidono con il confronto congelato.", "",
        "Ogni batch registrato è rieseguito su una copia dello stato precedente: azioni unità, poi mercato simultaneo dei due giocatori. Sono stati verificati 719 batch per profilo, 5.033 batch complessivi e 10.066 saldi di cassa, senza scarti. Vendite e acquisti sono fill effettivi, non richieste. I flussi per giornata sono attribuiti al giorno prima dell'azione: il confine differisce di un'azione rispetto ai checkpoint H24.", "",
        "Linee = mediane per checkpoint; fasce = minimo–massimo osservato, non intervalli di confidenza. La mediana può cambiare episodio lungo la curva. Il pubblico e il locale hanno seed, avversari e prezzi diversi: il confronto economico è descrittivo, non un effetto causale.", "",
        "## Cassa e consistenze", "",
        "Nelle coppie il primo dato è E18.26, il secondo Jesse. Le parentesi riportano il range osservato.", "",
        "| D | Cassa noi / Jesse | Persone | Crop totali | Strawberry | Wheat | Carrot | Pascoli vuoti |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|"]
    keys = ("money", "people", "crop_tiles", "STRAWBERRY", "WHEAT", "CARROT", "empty_pastures")
    for day in range(30):
        pairs = [display(agg["codex"][day]["metrics"][k])+" / "+display(agg["jesse"][day]["metrics"][k]) for k in keys]
        lines.append(f"| {day+1} | " + " | ".join(pairs) + " |")
    lines.extend(["", "## Sequenza macro di chiusura", "",
        "1. **Mantenere capacità fino a D27.** Jesse conserva 61 crop a D21-D27. E18.26 ne conserva 52 soltanto fino a D25 e scende a 42/28/20 a D26/D27/D28. Il ritiro delle Strawberry Jesse inizia a D23, con 38/34/26/22/18/18/15/0 a D22-D29; Codex avvia il ritiro già a D21 su una base di sole 29 tile.",
        "2. **Rimpiazzare colture lunghe con cicli brevi.** Jesse semina ancora 90 tile Wheat+Carrot in D21-D30; noi 46 Wheat. Il totale raccolto della famiglia è invariato nei cinque replay (345 unità), con due combinazioni: 246 Wheat + 99 Carrot oppure 333 Wheat + 12 Carrot. Le nuove Carrot compaiono a D26. La selezione è compatibile con un adattamento al valore relativo, ma dai replay non si ricostruisce con certezza la sua funzione decisionale.",
        "3. **Mantenere lavoro per consegne e vendite finali.** Jesse tiene 12 persone da D26 a D30 (11 hands + farmer); E18.26 passa a 9/10/3 nelle ultime tre giornate. Jesse esegue 28 HARVEST a D30, Codex 4. Nessuno semina in D30; Jesse ha semine residuali in D29 che lasciano due crop terminali, perciò il suo cutoff non va copiato senza verificare maturazione e consegna.",
        "4. **Il bestiame rimane produttivo fino al termine.** Jesse conserva 9 Cow + 5 Sheep e non subisce fughe; Codex chiude con 6 + 3. Gli animali non sono liquidabili tramite SELL: solo i prodotti venduti entrano nel reward. Il modello deve prenotare ultimo raccolto e consegna, e valutare il costo del servizio che non può più generare ricavi entro il termine.", "",
        "## Produzione e vendite effettive D21-D30", "",
        "| KPI | E18.26, mediana [range] | Jesse, mediana [range] |", "|---|---:|---:|"])
    metrics = [("Semine completate Wheat+Carrot", lambda p: p["planted"].get("WHEAT",0)+p["planted"].get("CARROT",0)),
               ("Raccolto Wheat+Carrot, unità", lambda p:p["harvested"].get("WHEAT",0)+p["harvested"].get("CARROT",0)),
               ("Raccolto Strawberry, unità",lambda p:p["harvested"].get("STRAWBERRY",0)),
               ("Strawberry vendute, unità",lambda p:p["sold_units"].get("STRAWBERRY",0)),
               ("Milk venduto, unità",lambda p:p["sold_units"].get("MILK",0)),
               ("Wool venduta, unità",lambda p:p["sold_units"].get("WOOL",0)),
               ("Fertilizer venduto, unità",lambda p:p["sold_units"].get("FERTILIZER",0)),
               ("HARVEST eseguiti, crop e bestiame",lambda p:p["executed"].get("HARVEST",0)),
               ("WATER eseguiti",lambda p:p["executed"].get("WATER",0)),
               ("PASS richiesti",lambda p:p["actions"].get("PASS",0)),
               ("Costo assunzioni D21-D30",lambda p:p["hires_cash_d21_d30"]),
               ("Flusso netto delle azioni D30",lambda p:p["cash_flow_day30"])]
    for label, fn in metrics:
        lines.append("| "+label+" | "+" | ".join(display(distribution([fn(p) for p in phases[c]])) for c in ("codex","jesse"))+" |")
    lines.extend(["", "Il locale raccoglie 72 Strawberry ma ne vende 84, grazie allo stock precedente; Jesse raccoglie/vende 189. Allo stesso modo le unità vendute non sono sempre uguali alla produzione della medesima finestra. Il minore output locale riguarda anche FEED/CARE, continuità del bestiame e Fertilizer: in D21-D30 non viene richiesto alcun COLLECT_FERTILIZER da E18.26.", "",
        "## Variabilità economica a produzione uguale", "",
        "| Episodio Jesse | Milk venduto | Incasso Milk | Prezzo medio Milk | Strawberry vendute | Incasso Strawberry | Cassa D30 |",
        "|---|---:|---:|---:|---:|---:|---:|"])
    for p, phase in zip(payload["jesse"], phases["jesse"]):
        milk_units = phase["sold_units"]["MILK"]
        milk_cash = phase["sales_cash"]["MILK"]
        lines.append(f"| {p['episode_id']} | {milk_units} | {number(milk_cash)} | {number(milk_cash/milk_units)} | {phase['sold_units']['STRAWBERRY']} | {number(phase['sales_cash']['STRAWBERRY'])} | {number(p['terminal']['cash'])} |")
    lines.extend(["", "L'incasso Milk varia da 731 a 30.308 a parità di 135 unità vendute: è una prova diretta dell'effetto del prezzo realizzato. Le Strawberry vendute sono sempre 189, con incassi da 4.176 a 22.164. Non si deve attribuire il range della cassa soltanto alla scelta Carrot/Wheat.", "",
        "## Pascoli vuoti: correzione della diagnosi D20", "",
        "L'analisi ai soli checkpoint D13/D14 vedeva 13→9 e aveva ipotizzato quattro perdite più un animale mai aggiunto. Il dettaglio per turno corregge questa lettura: nello step 312, cambio di D14, scappano cinque animali (3 Cow + 2 Sheep), dopo due giornate senza FEED. Il numero scende realmente 13→8; durante D14 viene piazzata una Sheep già prevista, risalendo a 9. Non viene comprato alcun animale da D14 in poi. I cinque pascoli restano vuoti per tutti i 17 checkpoint D14-D30, cioè 85 posti-giornata osservati. Jesse non subisce fughe.", "",
        "Il refill automatico va valutato sul margine atteso entro D30, includendo primo yield (8 giorni Cow, 6 Sheep), feed, cura, trasporto e cash disponibile. Nei replay locali i prezzi Milk/Wool diventano molto bassi: prevenire la fuga non equivale a dimostrare conveniente qualsiasi acquisto tardivo. Ogni posto vuoto deve comunque avere una decisione esplicita, una scadenza e una motivazione economica, senza cambiare la topologia.", "",
        "## Residui terminali e priorità successive", "",
        "Jesse conserva 1 Wheat nello shed, 12 Fertilizer trasportati e due crop con yield registrato pari a 2 unità (non necessariamente mature). Codex ha shed e crop vuoti ma conserva 4 Wheat negli inventari. Il reward è soltanto cash: questi residui non vengono automaticamente valorizzati. La perfezione della pulizia terminale ha un impatto minore dei divari osservati in volume prodotto e venduto.", "",
        "Priorità per una prossima release, da isolare nei confronti interni:", "",
        "1. Proteggere il ponte D11-D14 con precedenza a raccolto/consegna Melon-Wheat e obblighi FEED, finanziando le scadenze prima del lavoro marginale; evitare le cinque fughe.",
        "2. Inserire controllo giornaliero dei posti vuoti con piano di refill e verifica del tempo di rientro; nessun posto dimenticato dal dispatcher.",
        "3. Mantenere il plateau crop e costruire cicli brevi D23-D28 con WATER, HARVEST e vendita prenotati; selezionare Wheat/Carrot usando margine e fattibilità, non il solo prezzo corrente.",
        "4. Prenotare raccolti/trasporto/vendite D29-D30 prima di ridurre gli hands. Il taglio deve essere conseguenza delle missioni esaurite. Recuperare anche il flusso Fertilizer e interrompere FEED/CARE privi di ritorno entro il termine.", "",
        "Nota di topologia: i replay Jesse sono 7-7-0 per i pascoli finali, con 15-16 strutture pasture transitorie a D11-D14. Inoltre costruiscono due coop vuote in D29, ancora vuote a D30 e senza Goose. I grafici distinguono i pascoli vuoti dalle coop; queste costruzioni non sono un target da importare nella nostra 770.", "",
        f"Dataset completo: `{OUTPUT.relative_to(ROOT).as_posix()}`.", ""])
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    OUTPUT.write_text(json.dumps(payload, indent=2)+"\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    write_report(json.loads(OUTPUT.read_text(encoding="utf-8")))
    print(REPORT)
