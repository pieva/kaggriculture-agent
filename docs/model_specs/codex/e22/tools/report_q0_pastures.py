"""Standalone HTML/CSV daily KPI, generated only from audited engine results."""
import csv
import json
from collections import Counter
from statistics import mean, median
from compare_q0_pastures import ART, OUT
from e209_s56165462_charts import chart

def totals(row, seat):
    total = Counter()
    for d in row['ledgers'][seat]['daily']:
        total['labor'] += d['hire_cash']
        total['purchases'] += sum(d['purchase_cash'].values())
        total['sales'] += sum(d['sales_cash'].values())
        for name in ['harvested', 'sold_units', 'sales_cash', 'bought_units', 'purchase_cash']:
            for item, value in d[name].items(): total[name + ':' + item] += value
    return total

def main():
    rows = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(ART.glob('*.json'))]
    summaries = []
    for phase in ['exposed', 'confirmation']:
        rs = [r for r in rows if r['phase'] == phase]
        if not rs: continue
        keys = set().union(*(totals(r, s) for r in rs for s in (0, 1)))
        kpi = {k: mean(totals(r, r['seat'])[k] - totals(r, 1-r['seat'])[k] for r in rs) for k in sorted(keys)}
        pairs = {str(seed): mean(r['margin'] for r in rs if r['seed'] == seed) for seed in sorted({r['seed'] for r in rs})}
        summaries.append(dict(phase=phase, games=len(rs), wins=sum(r['margin'] > 0 for r in rs),
                              mean_margin=mean(r['margin'] for r in rs), median_margin=median(r['margin'] for r in rs),
                              min_margin=min(r['margin'] for r in rs), max_margin=max(r['margin'] for r in rs),
                              paired_seed_means=pairs, mean_kpi_deltas=kpi,
                              escapes=sum(r['checks']['escapes'] for r in rs),
                              cash_errors=sum(l['cash_parity_errors'] for r in rs for l in r['ledgers'])))
    (OUT / 'SUMMARY.json').write_text(json.dumps(summaries, indent=2), encoding='utf-8')
    exposed = next(s for s in summaries if s['phase'] == 'exposed')
    if exposed['games'] == 14 and (exposed['mean_margin'] < 0 or exposed['wins'] < 7):
        decision = ('Non promuovere 8C9S v1: il vantaggio non è regolare tra i seed. '
                    f"Margine medio {exposed['mean_margin']:+.1f}, mediana {exposed['median_margin']:+.1f}, vittorie {exposed['wins']}/14; "
                    'i due ruoli replicano lo stesso esito per seed e non costituiscono 14 osservazioni indipendenti. '
                    'Questa è una decisione diagnostica sui risultati esposti, non un criterio statistico preregistrato. '
                    'Non usare i seed 180912401–407 per questo candidato; restano riservati alla conferma di una futura variante congelata. '
                    'Nessuna pubblicazione Kaggle. La replica 6C10S resta distinta e non implementata in questo braccio. '
                    'Il calendario ripetuto nei replay esterni è documentato nel report delle traiettorie, ma non dimostra la convenienza del mix 8C9S.')
    else:
        decision = 'Risultati diagnostici interni; nessuna pubblicazione. Consultare il numero di partite prima di considerare completo il confronto.'
    (OUT / 'DECISION.json').write_text(json.dumps(dict(decision=decision, games=exposed['games'],
        confirmation_used=any(r['phase']=='confirmation' for r in rows)), indent=2), encoding='utf-8')
    records = []
    for r in rows:
        for s in (0, 1):
            for snap, d in zip(r['daily'][s], r['ledgers'][s]['daily']):
                rec = dict(phase=r['phase'], seed=r['seed'], candidate_seat=r['seat'],
                           model='8C9S' if s == r['seat'] else 'E22', day=d['day'],
                           cash_h24=snap['cash'], labor=d['hire_cash'],
                           net_flow=sum(d['sales_cash'].values())-sum(d['purchase_cash'].values())-d['hire_cash']-d['land_cash']+d['unit_cash_delta'])
                for item in ['WHEAT', 'MILK', 'WOOL', 'EGG', 'FERTILIZER', 'MELON', 'STRAWBERRY', 'CARROT']:
                    for metric in ['harvested', 'sold_units', 'sales_cash']:
                        rec[metric + ':' + item] = d[metric].get(item, 0)
                    rec['realized_price:' + item] = d['sales_cash'].get(item, 0) / d['sold_units'][item] if d['sold_units'].get(item) else ''
                    rec['shed:' + item] = snap['shed'].get(item, 0)
                    rec['carried:' + item] = snap['carried'].get(item, 0)
                rec['wheat_bought'] = d['bought_units'].get('BUY_PRODUCT:WHEAT', 0)
                rec['wheat_purchase_cash'] = d['purchase_cash'].get('BUY_PRODUCT:WHEAT', 0)
                for animal in ['COW', 'SHEEP', 'GOOSE']: rec[animal] = snap['animals'].get(animal, 0)
                records.append(rec)
    with (OUT / 'DAILY_KPI.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0])); writer.writeheader(); writer.writerows(records)
    intro = ('Braccio interno 8C9S contro E22 congelata, submission 56206528. Tre pascoli Q0 in (4,1), (3,2), (2,3), tutti occupati da pecore; '
             'restano le 8 mucche e le 6 pecore originarie. Non replica il caso 6C10S della submission 56165125, che lascia (4,1) vuoto. '
             'Il confronto misura il pacchetto strutture, sostituzione animali e servizio/vendite adattati, non il solo tipo di struttura.')
    method = ('Partite dirette a seed accoppiati nei due ruoli, una simulazione alla volta. Seed esposti 180911301–307; conferma 180912401–407 solo dopo il congelamento. '
              'Mercato condiviso: le vendite cambiano i prezzi di entrambi. KPI di flusso attribuiti al giorno dell’azione; cassa, animali e scorte alle osservazioni H24 '
              '(prima dell’ultima azione del giorno salvo D30 terminale). Prezzi giornalieri ponderati sulle unità effettivamente vendute; assenza vendite = dato mancante.')
    md = '# E22 · tre pascoli Q0, 8C9S\n\n' + intro + '\n\n' + method + '\n\n'
    md += '## Decisione\n\n' + decision + '\n\n'
    md += '| Fase | Vittorie | Margine medio | Mediana | Min | Max |\n|---|---:|---:|---:|---:|---:|\n'
    for s in summaries:
        md += f"| {s['phase']} | {s['wins']}/{s['games']} | {s['mean_margin']:.1f} | {s['median_margin']:.1f} | {s['min_margin']} | {s['max_margin']} |\n"
    md += '\n## KPI medi: candidato meno E22\n\n| KPI | ' + ' | '.join(s['phase'] for s in summaries) + ' |\n|---|' + '---:|' * len(summaries) + '\n'
    for key in ['labor', 'purchases', 'sales', 'purchase_cash:BUY_PRODUCT:WHEAT', 'bought_units:BUY_PRODUCT:WHEAT',
                'harvested:WHEAT', 'harvested:MILK', 'harvested:WOOL', 'harvested:EGG',
                'sales_cash:MILK', 'sales_cash:WOOL', 'sales_cash:EGG', 'sales_cash:FERTILIZER']:
        md += '| ' + key + ' | ' + ' | '.join(f"{s['mean_kpi_deltas'].get(key, 0):+.1f}" for s in summaries) + ' |\n'
    scope = ('Caricatore reale da file per entrambi gli agenti, 720 stati e stato DONE. Audit cassa sulle 719 transizioni per entrambi i lati; controllo invariato per 719/719 azioni in ogni partita. '
             'Tre strutture e mix finale 8C9S verificati; zero fughe. Nessuna partita di conferma eseguita. '
             'Le quantità massime degli ordini SELL WOOL sono ampliate anche prima di D11: i primi dieci giorni conservano le azioni degli operai, ma non necessariamente identici incassi, per il regolamento per-unità del mercato condiviso. '
             'Questo braccio misura anche tale modifica alle vendite. Tutto il latte e la lana raccolti sono venduti; a D30 restano due unità di fertilizzante trasportate, nessun latte/lana/uova in magazzino, sugli operai o sulle caselle.')
    md += '\n## Controlli e limiti\n\n' + scope + '\n\n'
    md += '[Dashboard D1–D30](REPORT.html) · [CSV giornaliero](DAILY_KPI.csv) · [Protocollo](PROTOCOL.json) · [Sintesi](SUMMARY.json)\n\n'
    md += '| Seed | Ruolo candidato | Cassa candidato | Cassa E22 | Margine |\n|---|---:|---:|---:|---:|\n'
    for r in rows:
        md += f"| {r['seed']} | {r['seat']} | {r['rewards'][r['seat']]} | {r['rewards'][1-r['seat']]} | {r['margin']} |\n"
    (OUT / 'REPORT.md').write_text(md, encoding='utf-8')
    body = '<h1>E22 · tre pascoli Q0 · 8C9S</h1><p>' + intro + '</p><p>' + method + '</p>'
    body += '<p><b>Decisione:</b> ' + decision + '</p>'
    body += '<details><summary>Controlli e perimetro della modifica</summary><p>' + scope + '</p></details>'
    body += '<p><a href="REPORT.md">Report e decisione</a> · <a href="DAILY_KPI.csv">CSV KPI</a> · <a href="SUMMARY.json">Sintesi</a> · <a href="PROTOCOL.json">Protocollo</a></p>'
    for s in summaries:
        body += f"<p><b>{s['phase']}</b>: {s['wins']}/{s['games']} vittorie · margine medio {s['mean_margin']:,.1f} · intervallo {s['min_margin']:,} / {s['max_margin']:,} · fughe {s['escapes']} · errori contabili {s['cash_errors']}.</p>"
    body += '<p>Blu: E22 controllo · Arancio: 8C9S. Valori sui punti.</p><label>Partita <select id="match">'
    body += ''.join(f'<option value="{i}">{r["phase"]} · {r["seed"]} · ruolo {r["seat"]} · margine {r["margin"]:+,}</option>' for i, r in enumerate(rows)) + '</select></label>'
    for i, r in enumerate(rows):
        seats = [1-r['seat'], r['seat']]
        def flow(fn): return [[fn(d) for d in r['ledgers'][s]['daily']] for s in seats]
        def snap(fn): return [[fn(d) for d in r['daily'][s]] for s in seats]
        def plot(title, seq, unit='unità'): return chart(title, seq, unit).replace('E20.9', 'E22').replace('s56165462', '8C9S')
        body += f'<section data-i="{i}"' + (' hidden' if i else '') + f'><h2>{r["seed"]} · ruolo {r["seat"]}</h2><div class="plots">'
        body += plot('Cassa H24', snap(lambda d: d['cash']), 'monete')
        margin = [r['daily'][r['seat']][d]['cash']-r['daily'][1-r['seat']][d]['cash'] for d in range(30)]
        body += plot('Margine H24: 8C9S meno E22', [[0]*30, margin], 'monete')
        body += plot('Costo lavoro', flow(lambda d: d['hire_cash']), 'monete/giorno')
        body += plot('Grano acquistato', flow(lambda d: d['bought_units'].get('BUY_PRODUCT:WHEAT', 0)))
        body += plot('Costo grano acquistato', flow(lambda d: d['purchase_cash'].get('BUY_PRODUCT:WHEAT', 0)), 'monete/giorno')
        for item in ['WHEAT', 'MILK', 'WOOL', 'EGG']:
            for metric, label in [('harvested', 'raccolto'), ('sold_units', 'venduto'), ('sales_cash', 'ricavi')]:
                body += plot(item + ' · ' + label, flow(lambda d: d[metric].get(item, 0)), 'monete/giorno' if metric == 'sales_cash' else 'unità/giorno')
            body += plot(item + ' · prezzo realizzato', flow(lambda d: d['sales_cash'].get(item, 0)/d['sold_units'][item] if d['sold_units'].get(item) else None), 'monete/unità')
            body += plot(item + ' · magazzino + trasportato H24', snap(lambda d: d['shed'].get(item, 0) + d['carried'].get(item, 0)))
        for animal in ['COW', 'SHEEP', 'GOOSE']: body += plot(animal + ' · capi effettivi', snap(lambda d: d['animals'].get(animal, 0)))
        body += '</div><details><summary>Rimanenze terminali complete</summary><pre>' + json.dumps({name: r['terminal'][s] for name, s in zip(['E22', '8C9S'], seats)}, indent=2) + '</pre></details></section>'
    body += '<script>document.getElementById("match").addEventListener("change",e=>document.querySelectorAll("section[data-i]").forEach(x=>x.hidden=x.dataset.i!==e.target.value));</script>'
    (OUT / 'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>E22 Q0 8C9S</title><style>body{font:16px system-ui;max-width:1400px;margin:30px auto;padding:0 24px;background:#f3f5f0;color:#24332d}section{background:white;padding:24px;border-radius:12px;margin:20px 0}p{line-height:1.6}.plots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.plot{border:1px solid #ddd;padding:12px;border-radius:8px;min-width:0}svg{width:100%}select{padding:10px;font:inherit}pre{overflow:auto}@media(max-width:850px){.plots{grid-template-columns:1fr}}</style>' + body + '</html>', encoding='utf-8')
    print(json.dumps([{k: v for k, v in s.items() if k != 'mean_kpi_deltas'} for s in summaries]), flush=True)

if __name__ == '__main__': main()
