import gzip,json,sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'docs/model_specs/codex/e22/tools'))
import e209_s56165462_charts as charts
def main():
    version=sys.argv[1];out=HERE/'reports'/('triangle_'+version)
    rows=json.loads((out/'RESULTS.json').read_text(encoding='utf-8'));summaries=[]
    for left,right in [('E19.2','E19.3'),('E19.2','E22'),('E19.3','E22')]:
        rs=[r for r in rows if (r['left'],r['right'])==(left,right)]
        if not rs:continue
        stats=[]
        for side in [0,1]:
            def ledger(r):return r['ledgers'][r['seat'] if side==0 else 1-r['seat']]
            stats.append(dict(model=[left,right][side],cash=mean(r['rewards'][r['seat'] if side==0 else 1-r['seat']] for r in rs),labor=mean(sum(d['hire_cash'] for d in ledger(r)['daily']) for r in rs),escapes=sum(len(ledger(r)['animal_escapes']) for r in rs),sales={k:dict(units=mean(sum(d['sold_units'].get(k,0) for d in ledger(r)['daily']) for r in rs),revenue=mean(sum(d['sales_cash'].get(k,0) for d in ledger(r)['daily']) for r in rs)) for k in ['MELON','STRAWBERRY','WOOL','MILK','EGG','WHEAT','CARROT','TOMATO']}))
        summaries.append(dict(left=left,right=right,n=len(rs),left_wins=sum(r['margin']>0 for r in rs),ties=sum(r['margin']==0 for r in rs),left_margin=mean(r['margin'] for r in rs),stats=stats))
    (out/'SUMMARY.json').write_text(json.dumps(dict(complete=len(rows)==12,comparisons=summaries),indent=2),encoding='utf-8')
    intro='E19.2 V52C: cap ordinario11 invece12 da D12 a D29, ripristinato con stress. E19.3 V53: massimo originale12 e fix su grano, FEED urgente e chiusura. Entrambe derivano da V51C: V53 non è V52C più fix. E22 è il piano osservato pubblicato, invariato.'
    method='Triangolare di scontri a due giocatori: stessi due seed esposti180911301/303, entrambi i ruoli. Otto nuovi incontri; quattro E19.3–E22 riutilizzati dopo verifica degli hash. Moduli E19 isolati nelle copie di test, nessuna modifica strategica. Ogni coppia genera il proprio mercato: non sono tre curve della stessa partita e non è una stima del rating.'
    bullets='\n'.join(f"- **{s['left']} vs {s['right']}**: {s['left_wins']}/{s['n']} vittorie del primo; margine medio del primo **{s['left_margin']:,.1f}**. Lavoro medio {s['stats'][0]['labor']:,.1f} / {s['stats'][1]['labor']:,.1f}; fughe {s['stats'][0]['escapes']} / {s['stats'][1]['escapes']}." for s in summaries)
    (out/'REPORT.md').write_text('# E19.2 V52C, E19.3 V53 ed E22\n\n'+intro+'\n\n'+method+'\n\n'+('12/12 incontri completati.' if len(rows)==12 else f'{len(rows)}/12, parziale.')+'\n\n'+bullets+'\n\n[Grafici D1–D30](REPORT.html) · [KPI sintetici](SUMMARY.json) · [Protocollo e hash](PROTOCOL.json). Cassa riconciliata su tutte le transizioni dei due giocatori; residui e fughe separati dai ricavi. Nessuna nuova submission.\n',encoding='utf-8')
    body='<h1>E19.2 V52C · E19.3 V53 · E22</h1><p>'+intro+'</p><p>'+method+'</p><p>'+str(len(rows))+'/12 incontri completati.</p><ul>'+''.join(f"<li><b>{s['left']} vs {s['right']}</b>: {s['left_wins']}/{s['n']} vittorie del primo, margine medio {s['left_margin']:,.1f}. Lavoro {s['stats'][0]['labor']:,.1f} / {s['stats'][1]['labor']:,.1f}.</li>" for s in summaries)+'</ul><p><a href="SUMMARY.json">KPI e volumi medi per coppia</a> · <a href="PROTOCOL.json">Protocollo</a></p><label>Incontro <select id="match">'+''.join(f'<option value="{i}">{r["left"]} vs {r["right"]} · seed{r["seed"]} · primo nel ruolo{r["seat"]}</option>' for i,r in enumerate(rows))+'</select></label>'
    for i,r in enumerate(rows):
        seat=r['seat'];order=[seat,1-seat];ls=[r['ledgers'][s] for s in order];replay=json.load(gzip.open(ROOT/r['replay'],'rt',encoding='utf-8'))
        charts.NAMES=[r['left']+(' V52C' if r['left']=='E19.2' else ' V53'),r['right']]
        palette={'E19.2':'#2563eb','E19.3':'#c05e12','E22':'#15803d'}
        charts.COLORS=[palette[r['left']],palette[r['right']]]
        def plot(title,series,unit):return charts.chart(title,series,unit)
        def daily(fn):return [[fn(d) for d in l['daily']] for l in ls]
        fs=[[replay['steps'][d*24-1][s]['observation']['farms'][s] for d in range(1,31)] for s in order]
        def farms(fn):return [[fn(f) for f in seq] for seq in fs]
        body+=f'<section data-i="{i}"'+(' hidden' if i else '')+f'><h2>{r["left"]} vs {r["right"]} · seed{r["seed"]} · ruolo{seat}</h2><p><b style="color:{palette[r["left"]]}">{r["left"]}</b> / <b style="color:{palette[r["right"]]}">{r["right"]}</b>. Margine {r["left"]}: {r["margin"]:,.0f}.</p><div class="plots">'
        body+=plot('Cassa',farms(lambda f:f['money']),'monete')+plot('Costo lavoro',daily(lambda d:d['hire_cash']),'monete/giorno')+plot('Assunzioni',daily(lambda d:d['hires']),'persone/giorno')
        for item in ['MELON','STRAWBERRY','WOOL','MILK','EGG','WHEAT','CARROT','TOMATO']:
            species={'WOOL':'SHEEP','MILK':'COW','EGG':'GOOSE'}.get(item,item)
            body+=plot(item+' · caselle',farms(lambda f:sum(t.get('animal',t.get('crop'))==species for row in f['tiles'] for t in row if isinstance(t,dict))),'caselle')
            body+=plot(item+' · raccolto',daily(lambda d:d['harvested'].get(item,0)),'unità/giorno')
            body+=plot(item+' · venduto',daily(lambda d:d['sold_units'].get(item,0)),'unità/giorno')
            body+=plot(item+' · prezzo realizzato',daily(lambda d:d['sales_cash'].get(item,0)/d['sold_units'][item] if d['sold_units'].get(item,0) else None),'monete/unità')
            body+=plot(item+' · ricavi',daily(lambda d:d['sales_cash'].get(item,0)),'monete/giorno')
        body+=plot('FERTILIZER · venduto',daily(lambda d:d['sold_units'].get('FERTILIZER',0)),'unità/giorno')
        body+=plot('FERTILIZER · prezzo realizzato',daily(lambda d:d['sales_cash'].get('FERTILIZER',0)/d['sold_units']['FERTILIZER'] if d['sold_units'].get('FERTILIZER',0) else None),'monete/unità')
        body+=plot('FERTILIZER · ricavi',daily(lambda d:d['sales_cash'].get('FERTILIZER',0)),'monete/giorno')
        body+='</div><details><summary>Residui finali</summary><pre>'+json.dumps({r['left']:r['terminal'][seat],r['right']:r['terminal'][1-seat]},indent=2)+'</pre></details></section>'
    if len(rows)==12 and version=='v52c':
        conclusion='E22 vince8/8 contro le due E19; E19.3 vince4/4 controE19.2. V52C risparmia mediamente2.126,75 di lavoro nello scontro conV53, ma perde2.519,75 di cassa. ControE22, V52C ha un margine negativo più contenuto diV53:−35.498,75 contro−38.828,5. Ogni coppia genera un mercato diverso: non attribuire la differenza al solo lavoro. E22 spende3.630 di lavoro contro4.880 dellaV52C e7.206 dellaV53 nei rispettivi confronti. Zero fughe in tutte le12partite. E22 resta il riferimento; nessuna nuova versione pubblicata.'
        body='<aside><h2>Esito del triangolare</h2><p>'+conclusion+'</p></aside>'+body
        mdpath=out/'REPORT.md';mdpath.write_text(mdpath.read_text(encoding='utf-8')+'\n\n## Interpretazione\n\n'+conclusion+'\n',encoding='utf-8')
    body+='<script>document.getElementById("match").onchange=e=>document.querySelectorAll("section[data-i]").forEach(s=>s.hidden=s.dataset.i!==e.target.value);</script>'
    (out/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>E19.2 E19.3 E22 · triangolare</title><style>body{font:16px system-ui;background:#f4f6f2;color:#22362e;max-width:1400px;margin:30px auto;padding:0 24px}p{line-height:1.6}section{background:white;padding:24px;margin-top:20px;border-radius:12px}.plots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.plot{border:1px solid #ddd;border-radius:8px;padding:14px}svg{width:100%}select{font:inherit;padding:10px;max-width:100%}pre{overflow:auto}@media(max-width:800px){.plots{grid-template-columns:1fr}}</style>'+body+'</html>',encoding='utf-8');print(json.dumps([{k:v for k,v in s.items() if k!='stats'} for s in summaries]))
if __name__=='__main__':main()
