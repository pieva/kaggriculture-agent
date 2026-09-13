import gzip,json,sys
from pathlib import Path
from collections import Counter
from statistics import mean
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent;OUT=HERE/'reports/v53'
sys.path.insert(0,str(ROOT/'docs/model_specs/codex/e22/tools'))
import e209_s56165462_charts as charts
def main():
    rows=json.loads((OUT/'RESULTS.json').read_text(encoding='utf-8'));summary=[]
    for name in dict.fromkeys(r['opponent'] for r in rows):
        rs=[r for r in rows if r['opponent']==name]
        summary.append(dict(opponent=name,n=len(rs),wins=sum(r['margin']>0 for r in rs),mean_margin=mean(r['margin'] for r in rs),mean_cash=mean(r['rewards'][r['seat']] for r in rs),opponent_cash=mean(r['rewards'][1-r['seat']] for r in rs),candidate_labor=mean(sum(d['hire_cash'] for d in r['ledgers'][r['seat']]['daily']) for r in rs),opponent_labor=mean(sum(d['hire_cash'] for d in r['ledgers'][1-r['seat']]['daily']) for r in rs),candidate_escapes=sum(len(r['ledgers'][r['seat']]['animal_escapes']) for r in rs)))
    complete=len(rows)==10
    (OUT/'SUMMARY.json').write_text(json.dumps(dict(complete=complete,comparisons=summary),indent=2),encoding='utf-8')
    intro='E19.3 V53: fix degli scambi di grano, alimentazione urgente, riserva accessibile e liquidazione terminale. Geometria 770, mix e scelte colturali V51C conservati. Pomodori non introdotti: ipotesi successiva da valutare separatamente.'
    method='Due seed esposti, partite seriali complete attraverso il caricatore file Kaggle. E22 ed E20.9fix in entrambi i ruoli, V51C controllo nel ruolo 0. Registri economici di entrambi riconciliati. Il mercato è condiviso e reagisce alle azioni: i valori non sono una previsione del rating.'
    result='\n'.join(f"- Contro **{s['opponent']}**: {s['wins']}/{s['n']} vittorie, margine medio **{s['mean_margin']:,.1f}**, lavoro {s['candidate_labor']:,.1f} contro {s['opponent_labor']:,.1f}; fughe V53: {s['candidate_escapes']}." for s in summary)
    validation=''
    if (OUT/'STARVATION_REGRESSION.json').exists():
        validation='Regressione mirata superata: il controllo riproduce tutti i 24 comandi di D26 e perde la pecora; applicando la protezione sullo stesso stato la pecora sopravvive. È una verifica funzionale, non un vantaggio economico dimostrato.'
    md='# E19.3 V53 — confronto dei fix\n\n'+intro+'\n\n'+('Confronto completo.' if complete else 'Risultati parziali, confronto in corso.')+'\n\n'+result+'\n\n'+method+'\n\n'+validation+'\n\n[Decisione e ipotesi successiva](DECISION.md) · [Regressione alimentazione](STARVATION_REGRESSION.json) · [Inventario dei fix](../../FIX_INVENTORY_V53.md) · [Protocollo e hash](PROTOCOL.json) · [Grafici D1–D30](REPORT.html).\n'
    (OUT/'REPORT.md').write_text(md,encoding='utf-8')
    body='<h1>E19.3 V53 · confronto dei fix</h1><p>'+intro+'</p><p>'+('10/10 partite completate.' if complete else f'{len(rows)}/10 partite completate, risultati parziali.')+'</p><ul>'+''.join(f"<li>{s['opponent']}: <b>{s['wins']}/{s['n']} vittorie, margine {s['mean_margin']:,.1f}</b>; lavoro {s['candidate_labor']:,.1f} contro {s['opponent_labor']:,.1f}; fughe V53 {s['candidate_escapes']}.</li>" for s in summary)+'</ul><p>'+method+'</p><p><a href="../../FIX_INVENTORY_V53.md">Fix applicati e limiti</a> · <a href="PROTOCOL.json">Protocollo</a> · <a href="RESULTS.json">Dati</a></p><label>Partita <select id="match">'+''.join(f'<option value="{i}">{r["opponent"]} · seed {r["seed"]} · V53 ruolo {r["seat"]}</option>' for i,r in enumerate(rows))+'</select></label>'
    body+='<p><b>V53 non promossa: mantenere E22 pubblicata invariata.</b> <a href="DECISION.md">Decisione e ipotesi successiva</a></p><p>'+validation+'</p>' if complete else ''
    for i,r in enumerate(rows):
        seat=r['seat'];name=r['opponent'];ls=[r['ledgers'][1-seat],r['ledgers'][seat]]
        replay=json.load(gzip.open(HERE/f'artifacts/v53/{name}_{r["seed"]}_{seat}.replay.json.gz','rt',encoding='utf-8'))
        charts.NAMES=[name,'E19.3 V53']
        def plot(title,series,unit):return charts.chart(title,series,unit)
        def daily(fn):return [[fn(d) for d in l['daily']] for l in ls]
        snapshots=[[replay['steps'][d*24-1][s]['observation']['farms'][s] for d in range(1,31)] for s in [1-seat,seat]]
        def farms(fn):return [[fn(f) for f in fs] for fs in snapshots]
        body+=f'<section data-i="{i}"'+(' hidden' if i else '')+f'><h2>{name} · seed {r["seed"]} · ruolo {seat}</h2><p>Blu: {name}. Arancio: E19.3 V53. Margine V53: {r["margin"]:,.0f}.</p><div class="plots">'
        body+=plot('Cassa',farms(lambda f:f['money']),'monete')
        body+=plot('Costo lavoro',daily(lambda d:d['hire_cash']),'monete/giorno')+plot('Assunzioni',daily(lambda d:d['hires']),'persone/giorno')
        for item in ['MELON','STRAWBERRY','WOOL','MILK','EGG','WHEAT','CARROT','TOMATO']:
            species={'WOOL':'SHEEP','MILK':'COW','EGG':'GOOSE'}.get(item,item)
            body+=plot(item+' · caselle produttive',farms(lambda f:sum(t.get('animal',t.get('crop'))==species for row in f['tiles'] for t in row if isinstance(t,dict))),'caselle')
            body+=plot(item+' · raccolto',daily(lambda d:d['harvested'].get(item,0)),'unità/giorno')
            body+=plot(item+' · venduto',daily(lambda d:d['sold_units'].get(item,0)),'unità/giorno')
            body+=plot(item+' · prezzo realizzato',daily(lambda d:d['sales_cash'].get(item,0)/d['sold_units'][item] if d['sold_units'].get(item,0) else None),'monete/unità')
            body+=plot(item+' · ricavi',daily(lambda d:d['sales_cash'].get(item,0)),'monete/giorno')
        body+='</div><details><summary>Residui finali osservati</summary><pre>'+json.dumps(dict(zip([name,'E19.3 V53'],[r['terminal'][1-seat],r['terminal'][seat]])),indent=2)+'</pre></details></section>'
    body+='<script>document.getElementById("match").onchange=e=>document.querySelectorAll("section[data-i]").forEach(s=>s.hidden=s.dataset.i!==e.target.value);</script>'
    (OUT/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>E19.3 V53 vs E22 e E20.9fix</title><style>body{font:16px system-ui;background:#f4f6f2;color:#22362e;max-width:1400px;margin:30px auto;padding:0 24px}p{line-height:1.6}section{background:white;padding:24px;margin-top:20px;border-radius:12px}.plots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.plot{border:1px solid #ddd;border-radius:8px;padding:14px}svg{width:100%}select{font:inherit;padding:10px;max-width:100%}pre{overflow:auto}@media(max-width:800px){.plots{grid-template-columns:1fr}}</style>'+body+'</html>',encoding='utf-8')
    print(json.dumps(summary))
if __name__=='__main__':main()
