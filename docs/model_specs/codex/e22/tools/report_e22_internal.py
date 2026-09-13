"""Internal E22 comparison: causal scope and daily plots for each paired game."""
import gzip,json
from pathlib import Path
from statistics import mean
from e209_s56165462_charts import chart
ROOT=Path(__file__).resolve().parents[5];OUT=ROOT/'docs/model_specs/codex/e22/reports/e22_replica_internal';ART=ROOT/'docs/model_specs/codex/e22/artifacts/e22_replica_internal'
def main():
 rows=json.loads((OUT/'RESULTS.json').read_text(encoding='utf-8'));summary=[]
 for model in ['E22Replica','E209Fix']:
  rs=[r for r in rows if r['model']==model];summary.append(dict(model=model,n=len(rs),wins=sum(r['margin']>0 for r in rs),mean_margin=mean(r['margin'] for r in rs),min_margin=min(r['margin'] for r in rs),max_margin=max(r['margin'] for r in rs)))
 (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
 intro='E22 replica il piano costante osservato della submission s56165462 56165462: 719 azioni indicizzate da giorno e ora. Non ricostruisce il codice interno né usa osservazioni future. Parità esatta su 14.380 azioni in 20 replay. E20.9 congelata resta intatta; E209Fix cambia soltanto la condizione che saltava PLACE di prodotti sulle caselle già occupate da animali.'
 method='Due seed esposti (180911301 e 180911303), entrambi i ruoli, quattro partite per variante contro E20.9 congelata. Otto simulazioni seriali. Mercato condiviso e politiche eseguite nel motore; non replay avversari forzati. Verifica della cassa a ogni transizione per entrambi i giocatori. Non è una stima del rating, né una conferma su seed riservati.'
 md='# E22 — replica osservata e correzione consegne\n\n'+intro+'\n\n'+method+'\n\n| Variante | Vittorie | Margine medio | Min | Max |\n|---|---:|---:|---:|---:|\n'+'\n'.join(f"| {s['model']} | {s['wins']}/{s['n']} | {s['mean_margin']:.1f} | {s['min_margin']} | {s['max_margin']} |" for s in summary)
 md+='\n\n## Causa e intervento\n\n`PLACE` ha due significati: collocare animali e depositare prodotti. Il controllo di lavoro già soddisfatto verificava soltanto la presenza di un animale sulla casella: saltava anche PLACE MELON. Ora applica quel controllo soltanto se il prodotto richiesto è un animale. Test di regressione sullo stato reale D11: PLACE MELON 6 non viene saltato. L’esistenza di un ordine SELL non dimostra la consegna né il suo successo.\n\n## Come è sfuggito\n\nLe verifiche precedenti controllavano correttamente quantità raccolte, cassa e corrispondenza bundle/sorgente, ma non imponevano la consegna del raccolto entro la finestra di vendita. La parità con la sorgente preservava anche questo difetto. La correzione resta separata dalla replica, per attribuire gli effetti.\n\n## Limiti e prossima decisione\n\nLa replica è un riferimento interno: non adattando il piano, può fallire azioni quando cassa o stato divergono. Il confronto a seed accoppiati non rende identiche le condizioni di mercato dopo l’intervento: entrambi i giocatori influenzano il mercato, come previsto dal gioco. Non promuovere automaticamente alcun candidato dai soli seed esposti. Nessuna pubblicazione o commit.\n\n[Grafici 30 giorni e dettaglio partite](REPORT.html) · [Protocollo](PROTOCOL.json) · [Dati](RESULTS.json)\n'
 (OUT/'REPORT.md').write_text(md,encoding='utf-8')
 body='<h1>E22 · Replica osservata e fix consegne</h1><p>'+intro+'</p><p>'+method+'</p><p><a href="REPORT.md">Diagnosi e limiti</a> · <a href="PROTOCOL.json">Protocollo</a> · <a href="SUMMARY.json">Risultati sintetici</a></p><section><h2>Confronto contro E20.9 congelata</h2><ul>'+''.join(f"<li><b>{s['model']}</b>: {s['wins']}/{s['n']} vittorie, margine medio {s['mean_margin']:,.1f}; intervallo {s['min_margin']:,} / {s['max_margin']:,}.</li>" for s in summary)+'</ul></section><label>Partita <select id="match">'+''.join(f'<option value="{i}">{r["model"]} · seed {r["seed"]} · ruolo {r["seat"]}</option>' for i,r in enumerate(rows))+'</select></label>'
 for i,r in enumerate(rows):
  seat=r['seat'];ls=[r['ledgers'][1-seat],r['ledgers'][seat]]
  g=json.load(gzip.open(ART/f"{r['model']}_{r['seed']}_{seat}.replay.json.gz",'rt',encoding='utf-8'))
  def series(fn):return [[fn(d) for d in l['daily']] for l in ls]
  def plot(title,s,unit):return chart(title,s,unit).replace('s56165462',r['model'])
  body+=f'<section class="match" data-i="{i}"'+(' hidden' if i else '')+f'><h2>{r["model"]}, seed {r["seed"]}, ruolo {seat}</h2><p>Margine candidato − E20.9: {r["margin"]:,}. Blu: E20.9 congelata; arancio: candidato. Valori sui punti.</p><div class="plots">'
  body+=plot('Cassa giornaliera',[[g['steps'][d*24-1][s]['observation']['farms'][s]['money'] for d in range(1,31)] for s in [1-seat,seat]],'monete')
  body+=plot('Costo lavoro',series(lambda d:d['hire_cash']),'monete/giorno')
  body+=plot('Meloni raccolti',series(lambda d:d['harvested'].get('MELON',0)),'unità')
  body+=plot('Meloni venduti',series(lambda d:d['sold_units'].get('MELON',0)),'unità')
  body+=plot('Prezzo medio meloni venduti',series(lambda d:d['sales_cash'].get('MELON',0)/d['sold_units']['MELON'] if d['sold_units'].get('MELON',0) else None),'monete/unità')
  body+=plot('Ricavi meloni',series(lambda d:d['sales_cash'].get('MELON',0)),'monete/giorno')
  body+=plot('Fragole vendute',series(lambda d:d['sold_units'].get('STRAWBERRY',0)),'unità')
  body+=plot('Ricavi complessivi',series(lambda d:sum(d['sales_cash'].values())),'monete/giorno')+'</div></section>'
 body+='<script>document.getElementById("match").addEventListener("change",e=>document.querySelectorAll(".match").forEach(x=>x.hidden=x.dataset.i!==e.target.value));</script>'
 (OUT/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>E22 confronto interno</title><style>body{font:16px system-ui;max-width:1400px;margin:30px auto;padding:0 24px;background:#f3f5f0;color:#24332d}section{background:white;padding:24px;border-radius:12px;margin:20px 0}p{line-height:1.6}.plots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.plot{border:1px solid #ddd;padding:12px;border-radius:8px;min-width:0}svg{width:100%}select{padding:10px;font:inherit}@media(max-width:850px){.plots{grid-template-columns:1fr}}</style>'+body+'</html>',encoding='utf-8')
 print(json.dumps(summary))
if __name__=='__main__':main()
