"""Standalone Italian report: balanced tournament, paired 22-panel trajectories."""
import csv
import hashlib
import html
import json
from pathlib import Path
from statistics import mean,median
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
BASE=ROOT/'docs/model_specs/codex/e20'

def build(stage='tournament'):
    paths=sorted((BASE/'artifacts'/stage).glob('*.kpi.json'))
    cases=[json.loads(p.read_text()) for p in paths]
    assert cases
    models=sorted({s['name'] for c in cases for s in c['sides']})
    groups={m:[s for c in cases for s in c['sides'] if s['name']==m] for m in models}
    metadata=[json.loads(p.with_name(p.name.replace('.kpi.json','.json')).read_text()) for p in paths]
    assert len(set(map(len,groups.values())))==1
    out=BASE/'reports'/stage;out.mkdir(parents=True,exist_ok=True)
    def fmt(n):return f'{n:,.1f}'.replace(',','X').replace('.',',').replace('X','.')
    summary={}
    for m,ss in groups.items():
        wins=sum(c['sides'][i]['reward']>c['sides'][1-i]['reward'] for c in cases for i in (0,1) if c['sides'][i]['name']==m)
        summary[m]=dict(matches=len(ss),wins=wins,mean_cash=mean(s['reward'] for s in ss),median_cash=median(s['reward'] for s in ss),
            min_cash=min(s['reward'] for s in ss),losses=sum(len(s['ledger']['animal_escapes']) for s in ss),
            crop_stress_transitions=sum(len(s['crop_starvation']) for s in ss),
            sales=mean(sum(sum(d['sales_cash'].values()) for d in s['ledger']['daily']) for s in ss),
            purchases=mean(sum(sum(d['purchase_cash'].values()) for d in s['ledger']['daily']) for s in ss),
            wages=mean(sum(d['hire_cash'] for d in s['ledger']['daily']) for s in ss))
        target={'E18':[7,7,5],'E19':[7,7,0],'E20':[7,7,2]}[m]
        observed=[o['topology'] for r in metadata for o in r['opening'] if o['name']==m]
        summary[m]['target_topology']=target
        summary[m]['exact_target_cases']=sum(t==target for t in observed)
        summary[m]['observed_topologies']={str(t):sum(tuple(v)==t for v in observed) for t in sorted(set(map(tuple,observed)))}
    pairings=[]
    for i,a in enumerate(models):
        for b in models[i+1:]:
            matches=[c for c in cases if {s['name'] for s in c['sides']}=={a,b}]
            series={}
            for m in (a,b):
                ss=[s for c in matches for s in c['sides'] if s['name']==m]
                series[m]={k:[[median(v),min(v),max(v)] for d in range(30) for v in [[s['kpi'][d][k] for s in ss]]] for k in [f[0] for f in FIELDS]+['unlocked_tiles']}
            pairings.append(dict(label=f'{a} / {b}',models=[a,b],matches=len(matches),series=series))
    data=dict(fields=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],pairings=pairings,summary=summary,
              seeds=sorted({c['seed'] for c in cases}),match_count=len(cases))
    data['matches']=[dict(seed=r['seed'],agents=r['agents'],rewards=r['rewards'],topologies=[o['topology'] for o in r['opening']],replay_sha256=r['replay_sha256']) for r in metadata]
    (out/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (out/'daily_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=['seed','model','seat','day']+[k for k,_,_ in FIELDS]+['unlocked_tiles']);writer.writeheader()
        for c in cases:
            for s in c['sides']:
                for day,row in enumerate(s['kpi'],1):writer.writerow(dict(seed=c['seed'],model=s['name'],seat=s['seat'],day=day,**{k:row[k] for k,_,_ in FIELDS},unlocked_tiles=row['unlocked_tiles']))
    lines=['# E18 · E19 · E20 — torneo e traiettorie dei 22 KPI','',
           f"{len(cases)} partite interne complete, {len(data['seeds'])} seed, tutti gli accoppiamenti e scambio di posizione. E18 = V4D 775; E19 = V48 770; E20 = variante congelata 772. Nessuna nuova submission Kaggle.",'',
           '| Modello | Partite | Vittorie | Cassa media | Mediana | Minimo | Perdite animali |','|---|---:|---:|---:|---:|---:|---:|']
    for m,v in summary.items():lines.append(f"| {m} | {v['matches']} | {v['wins']} | {fmt(v['mean_cash'])} | {fmt(v['median_cash'])} | {fmt(v['min_cash'])} | {v['losses']} |")
    lines+=['','## Target e topologie osservate','','| Modello | Target | Casi esatti | Topologie finali osservate |','|---|---|---:|---|']
    for m,v in summary.items():
        counts={}
        for r in metadata:
            for o in r['opening']:
                if o['name']==m:
                    key='–'.join(map(str,o['topology']));counts[key]=counts.get(key,0)+1
        lines.append(f"| {m} | {'–'.join(map(str,v['target_topology']))} | {v['exact_target_cases']}/{v['matches']} | "+'; '.join(f'{k}: {n}' for k,n in sorted(counts.items()))+' |')
    lines+=['', 'Sono inclusi tutti i casi previsti dal protocollo, anche quelli che non raggiungono la topologia target. La topologia finale non equivale al numero di animali presenti; i pannelli 4–8 mostrano occupazione e strutture vuote.']
    lines+=['','## Scontri diretti','','| Coppia | Partite | Cassa media primo | Cassa media secondo | Delta primo |','|---|---:|---:|---:|---:|']
    for pair in pairings:
        a,b=pair['models'];matches=[c for c in cases if {s['name'] for s in c['sides']}=={a,b}]
        av=[mean(s['reward'] for c in matches for s in c['sides'] if s['name']==m) for m in (a,b)]
        lines.append(f"| {a} / {b} | {len(matches)} | {fmt(av[0])} | {fmt(av[1])} | {fmt(av[0]-av[1])} |")
    lines+=['','## Economia riconciliata','','| Modello | Vendite medie | Acquisti medi | Assunzioni medie |','|---|---:|---:|---:|']
    for m,v in summary.items():lines.append(f"| {m} | {fmt(v['sales'])} | {fmt(v['purchases'])} | {fmt(v['wages'])} |")
    lines+=['','| Prodotto | '+' | '.join(models)+' |','|---|'+'---:|'*len(models)]
    for product in ['WHEAT','MELON','STRAWBERRY','MILK','WOOL']:
        cells=[]
        for m,ss in groups.items():
            units=mean(sum(d['harvested'].get(product,0) for d in s['ledger']['daily']) for s in ss)
            cash=mean(sum(d['sales_cash'].get(product,0) for d in s['ledger']['daily']) for s in ss)
            cells.append(f'{fmt(units)} unità / {fmt(cash)} incassi')
        lines.append('| '+product+' | '+' | '.join(cells)+' |')
    lines+=['', 'Unità raccolte e incassi non danno un prezzo unitario esatto: gli incassi possono includere scorte iniziali o altri movimenti; la tabella distingue quantità prodotta da ricavo monetizzato. Il mercato e l’avversario reagiscono alle azioni di entrambi i giocatori.']
    if stage=='tournament':
        gate=json.loads((BASE/'artifacts/ECONOMIC_GATE.json').read_text())
        lines+=['','## Dalla selezione al torneo','',
                f"La candidata E20v18 era stata congelata dopo un vantaggio medio del {fmt(gate['delta_percent'])}% su E19 nei sei casi development. La policy del torneo conserva lo stesso hash; i sette seed di torneo non sono stati usati per scegliere la variante."]
        common={m:{(c['seed'],s['seat']):s['reward'] for c in cases if {x['name'] for x in c['sides']}=={m,'E18'} for s in c['sides'] if s['name']==m} for m in ['E19','E20']}
        assert set(common['E19'])==set(common['E20'])
        deltas=[common['E20'][k]-common['E19'][k] for k in sorted(common['E19'])]
        e19=mean(common['E19'].values());e20=mean(common['E20'].values())
        data['matched_vs_E18']=dict(E19_mean=e19,E20_mean=e20,delta_mean=mean(deltas),positive_cases=sum(d>0 for d in deltas),cases=len(deltas),deltas=deltas)
        lines+=['',f"A parità di avversario E18, seed e ruolo, E20 chiude a {fmt(e20)} contro {fmt(e19)} di E19: delta {fmt(mean(deltas))} ({fmt(100*(e20/e19-1))}%), positivo in {sum(d>0 for d in deltas)}/{len(deltas)} casi. È una conferma separata dalla classifica complessiva, che mescola due avversari per modello."]
        lines+=['','| Seed | E19 contro E18 | E20 contro E18 | Delta E20 |','|---|---:|---:|---:|']
        for seed in data['seeds']:
            v19=mean(v for (s,seat),v in common['E19'].items() if s==seed)
            v20=mean(v for (s,seat),v in common['E20'].items() if s==seed)
            lines.append(f'| {seed} | {fmt(v19)} | {fmt(v20)} | {fmt(v20-v19)} |')
        lines+=['', 'Ogni riga media i due ruoli dello stesso seed. Il seed è l’unità indipendente: quattordici confronti non equivalgono a quattordici scenari. Il mercato evolve in risposta alle due policy; il confronto fissa condizioni iniziali e avversario, non l’intera traiettoria dei prezzi.']
        matched_sides={m:[s for c in cases if {x['name'] for x in c['sides']}=={m,'E18'} for s in c['sides'] if s['name']==m] for m in ['E19','E20']}
        totals={m:{k:mean(sum(r[k] for r in s['kpi']) for s in ss) for k in ['PASS','MOVE','WATER','FEED','CARE']} for m,ss in matched_sides.items()}
        stress={m:mean(len(s['crop_starvation']) for s in ss) for m,ss in matched_sides.items()}
        lines+=['',f"Sulle stesse condizioni contro E18, E20 cambia il carico medio stagionale rispetto a E19: PASS {fmt(totals['E20']['PASS']-totals['E19']['PASS'])}, MOVE {fmt(totals['E20']['MOVE']-totals['E19']['MOVE'])}, FEED {fmt(totals['E20']['FEED']-totals['E19']['FEED'])}, CARE {fmt(totals['E20']['CARE']-totals['E19']['CARE'])}, WATER {fmt(totals['E20']['WATER']-totals['E19']['WATER'])}. Le transizioni crop→weed dopo stress passano da {fmt(stress['E19'])} a {fmt(stress['E20'])} per partita.",
                '', 'Questa combinazione segnala una competizione fra allevamento e servizio delle colture. Non è una prova causale isolata: la variante cambia anche rotte, raccolti e prezzi. La riduzione dei PASS non basta a dimostrare un miglioramento economico.']
        lines+=['','## Lettura delle traiettorie','',
                'D1–D11: l’avvio E20 riproduce E19. L’espansione iniziale di manodopera, colture e bestiame va letta insieme ai gradini del terreno nel pannello 3. D12 introduce i due pascoli Q2: il confronto fra pannelli 4–8 e FEED/CARE permette di distinguere capacità costruita, animali presenti e servizio effettivo.',
                '', 'D12–D20: le nuove risorse competono con l’irrigazione e con i viaggi. Più animali non garantiscono più margine: contano raccolto, prezzo di vendita e costo del grano acquistato. I pannelli 9–13 mostrano il mix di colture; MOVE/PASS vanno letti insieme ai servizi riusciti, senza considerare ogni riduzione dei PASS un miglioramento.',
                '', 'D21–D30: cassa e superficie coltivata descrivono raccolti e chiusura. Il calo terminale di colture o personale non identifica da solo una perdita: va confrontato con le vendite e con il calendario biologico. I pannelli 17–19 e la tabella seguente segnalano invece la fragilità idrica e le perdite.']
    lines+=['','## Servizi e fragilità operativa','','| Modello | PASS medi/giorno | MOVE medi/giorno | WATER riusciti/giorno | FEED riusciti/giorno | CARE riusciti/giorno | Crop→weed dopo stress, media/partita |','|---|---:|---:|---:|---:|---:|---:|']
    for m,ss in groups.items():
        vals=[mean(r[k] for s in ss for r in s['kpi']) for k in ['PASS','MOVE','WATER','FEED','CARE']]
        lines.append('| '+m+' | '+' | '.join(fmt(v) for v in vals)+f" | {fmt(summary[m]['crop_stress_transitions']/len(ss))} |")
    lines+=['', 'Crop→weed segue il diagnostico comune crop_service_audit: transizione osservata al cambio giorno dopo mancata acqua. È un indicatore complementare ai 22 KPI. Il vantaggio economico non implica una riduzione dello stress idrico; i casi individuali restano nei ledger e nel CSV.']
    lines+=['','## Traiettorie per fase','',
            'Ogni riga mostra media D1–D10 → D11–D20 → D21–D30. Per consistenze e cassa sono medie dei checkpoint; per azioni e perdite, medie giornaliere. Il CSV conserva ogni singola traiettoria.','',
            '| KPI | '+' | '.join(models)+' |','|---|'+'---:|'*len(models)]
    for k,label,unit in FIELDS:
        cells=[' → '.join(fmt(mean(s['kpi'][d][k] for s in groups[m] for d in range(start,start+10))) for start in (0,10,20)) for m in models]
        lines.append('| '+label+' | '+' | '.join(cells)+' |')
    lines+=['','## Metodo e limiti','',
            'I ledger verificano i saldi contro l’engine a ogni transizione. WATER, FEED e CARE contano esecuzioni riuscite, non richieste. MOVE e PASS seguono la definizione del report comune. Checkpoint 24×D−1: prima dell’ultimo batch D1–D29, terminale D30. La superficie coltivata esclude i pascoli; il pannello 3 include il terreno sbloccato.',
            '', 'Il grafico interattivo presenta mediana puntuale e min–max, sempre due avversari delle stesse partite. Non sono intervalli di confidenza. Gli aggregati complessivi usano due avversari per modello: gli scontri diretti restano la misura più chiara della superiorità relativa. Gli scambi di ruolo non sono nuovi seed indipendenti.',
            '', 'Seed: '+', '.join(map(str,data['seeds']))+'. I risultati interni non dimostrano il ranking esterno né una superiorità universale. Consultare il protocollo congelato e il registro development per distinguere tuning e valutazione.',
            '', '[Dashboard interattiva](REPORT.html) · [Dati aggregati](data.json) · [KPI per partita](daily_kpi.csv)']
    lines+=['','## Registro degli scontri e dei ruoli','','| Seed | Posizione 0 | Cassa 0 | Posizione 1 | Cassa 1 | Esito |','|---|---|---:|---|---:|---|']
    for r in sorted(metadata,key=lambda r:(r['agents'],r['seed'])):
        a,b=r['agents'];x,y=r['rewards'];winner=a if x>y else b if y>x else 'Parità'
        lines.append(f"| {r['seed']} | {a} | {fmt(x)} | {b} | {fmt(y)} | {winner} |")
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    # Markdown rendering uses an installed dependency already used by repository reports.
    from markdown_it import MarkdownIt
    body=MarkdownIt('commonmark').enable('table').render('\n'.join(lines[2:]))
    cards='<div class="cards">'+''.join(f'<section><strong>{m}</strong><div class="cash">{fmt(v["mean_cash"])}</div><div>Cassa media · {v["wins"]}/{v["matches"]} vittorie</div><small>Target {"–".join(map(str,v["target_topology"]))}: {v["exact_target_cases"]}/{v["matches"]} casi</small></section>' for m,v in summary.items())+'</div>'
    if stage=='tournament':
        matched=data['matched_vs_E18']
        cards+=f'<p>Contro lo stesso riferimento E18, E20 rispetto a E19: <strong>{fmt(matched["delta_mean"])} di cassa media</strong>; differenza positiva in {matched["positive_cases"]}/{matched["cases"]} casi. Il confronto dei servizi e dello stress idrico resta separato dal risultato economico.</p>'
    page='''<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>E20 — torneo 22 KPI</title>
<style>body{font:15px/1.55 system-ui;margin:0;background:#f6f7f9;color:#203047}main{max-width:1320px;margin:auto;padding:30px}h1{font-size:30px}h2{margin-top:32px}table{border-collapse:collapse;display:block;overflow:auto;font-size:13px;background:white}td,th{padding:8px 12px;border-bottom:1px solid #dce2eb;text-align:right;white-space:nowrap}td:first-child,th:first-child{text-align:left}a{color:#1473bd}.toolbar{position:sticky;top:0;background:#f6f7f9;padding:14px 0;z-index:2}select{font:inherit;padding:7px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}.panel{background:white;border:1px solid #dde4eb;border-radius:10px;padding:14px;min-width:0}.panel h3{font-size:15px;margin:0}.panel svg{width:100%;display:block}.detail{font-size:12px;min-height:40px;color:#56677a}svg text{font:11px system-ui;fill:#617184}.note{padding:12px;background:#e7eff6} @media(max-width:760px){main{padding:16px}.grid{grid-template-columns:1fr}}@media print{.toolbar{position:static}.panel{break-inside:avoid}}</style><main>
<h1>E18 · E19 · E20</h1><p>Confronti diretti · 22 KPI D1–D30 · dati riconciliati con l’engine.</p>__CARDS__
<div class="toolbar"><label>Accoppiamento <select id="pair"></select></label><span id="legend"></span></div>
<p class="note">Linea: mediana. Banda: min–max osservato. Passa sul grafico per leggere i valori del giorno. Nel pannello 3 le linee tratteggiate rappresentano il terreno sbloccato.</p>
<div id="charts" class="grid"></div>__BODY__</main><script id="data" type="application/json">__DATA__</script><script>
const data=JSON.parse(document.getElementById('data').textContent),colors=['#1473bd','#bb5228'];
const select=document.getElementById('pair');data.pairings.forEach((p,i)=>select.add(new Option(p.label,i)));
const fmt=n=>n.toLocaleString('it-IT',{maximumFractionDigits:1});
function render(){const p=data.pairings[+select.value];document.getElementById('legend').innerHTML=p.models.map((m,i)=>` <span style="color:${colors[i]}">● ${m}</span>`).join('')+` · ${p.matches} partite`;
const root=document.getElementById('charts');root.innerHTML='';data.fields.forEach((field,index)=>{const panel=document.createElement('section');panel.className='panel';const W=560,H=240,L=72,R=12,T=15,B=28, series=p.models.map(m=>p.series[m][field.key]);
let values=series.flat(2);if(field.key==='crop_tiles')p.models.forEach(m=>values.push(...p.series[m].unlocked_tiles.flat()));let max=Math.max(...values,1),min=Math.min(0,...values);const x=d=>L+d*(W-L-R)/29,y=v=>H-B-(v-min)/(max-min)*(H-T-B),path=(s,j)=>s.map((v,d)=>(d?'L':'M')+x(d)+','+y(v[j])).join(' ');
let svg='';for(let i=0;i<=4;i++){const v=min+(max-min)*i/4;svg+=`<line x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}" stroke="#e5eaf0"/><text x="${L-6}" y="${y(v)+4}" text-anchor="end">${fmt(v)}</text>`;}[0,9,19,29].forEach(d=>svg+=`<text x="${x(d)}" y="${H-7}" text-anchor="middle">D${d+1}</text>`);
series.forEach((s,i)=>{svg+=`<path d="${path(s,1)} ${s.slice().reverse().map((v,j)=>'L'+x(29-j)+','+y(v[2])).join(' ')} Z" fill="${colors[i]}" opacity=".10"/><path d="${path(s,0)}" fill="none" stroke="${colors[i]}" stroke-width="2.4"/>`;if(field.key==='crop_tiles')svg+=`<path d="${path(p.series[p.models[i]].unlocked_tiles,0)}" fill="none" stroke="${colors[i]}" stroke-dasharray="5 4"/>`;});
panel.innerHTML=`<h3>${String(index+1).padStart(2,'0')} · ${field.label}</h3><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${field.label}">${svg}</svg><div class="detail">${field.unit} · D1–D30</div>`;
panel.querySelector('svg').addEventListener('pointermove',e=>{const rect=e.currentTarget.getBoundingClientRect(),d=Math.max(0,Math.min(29,Math.round(((e.clientX-rect.left)*W/rect.width-L)/(W-L-R)*29)));panel.querySelector('.detail').textContent=`D${d+1} · `+p.models.map((m,i)=>{let v=series[i][d];return `${m}: ${fmt(v[0])} [${fmt(v[1])}–${fmt(v[2])}]`+(field.key==='crop_tiles'?` / terreno ${fmt(p.series[m].unlocked_tiles[d][0])}`:'');}).join(' · ');});root.append(panel);});}
select.addEventListener('change',render);render();</script></html>'''
    page=page.replace('</style>','.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:22px 0}.cards section{padding:18px;border:1px solid #dce2eb;border-radius:10px;background:white}.cash{font-size:28px;font-weight:650}.cards small{color:#617184}@media(max-width:760px){.cards{grid-template-columns:1fr}.panel svg text{font-size:16px}} </style>')
    page=page.replace('__CARDS__',cards).replace('__BODY__',body).replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
    (out/'REPORT.html').write_text(page,encoding='utf-8')
    (out/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    provenance=[Path(__file__),Path(__file__).with_name('audit_results.py'),
        ROOT/'docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d30_closure.py',
        ROOT/'docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d20_trajectories.py',
        ROOT/'docs/model_specs/codex/e18/tools/e18_29_crop_service_audit.py',
        ROOT/'experiments/e18/tools/common/replay_daily_operational_kpi.py',
        ROOT/'.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py',
        ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py',
        ROOT/'submission/submission_codex_e18_770_v48_external.py',
        ROOT/'submission/submission_codex_e20_772_e20v18_candidate.py',
        BASE/'VALIDATION_PROTOCOL.json',BASE/'artifacts/ECONOMIC_GATE.json']
    manifest=dict(stage=stage,panels=22,matches=len(cases),sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+provenance})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(summary,indent=2));print(out/'REPORT.html')

if __name__=='__main__':build(sys.argv[1] if len(sys.argv)>1 else 'tournament')
