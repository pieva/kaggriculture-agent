"""Matched revision evaluation; exposed development and fresh confirmation stay separate."""
import argparse
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

def evaluate(stages,models,out,seeds):
    records={}
    sources={}
    for stage in stages:
        for path in sorted((BASE/'artifacts'/stage).glob('*.kpi.json')):
            case=json.loads(path.read_text())
            if case['seed'] not in seeds:continue
            meta=json.loads(path.with_name(path.name.replace('.kpi.json','.json')).read_text())
            assert all(v['calls']==719 for v in meta['runtime']),(path,'Incomplete agent execution; economic comparison invalid')
            for s in case['sides']:
                name='E20v18' if s['name']=='E20' else s['name']
                opponent=case['sides'][1-s['seat']]['name']
                if name in models and opponent=='E18':
                    key=(name,case['seed'],s['seat'])
                    records[key]=s
                    sources[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    common=sorted(set.intersection(*[{(seed,seat) for name,seed,seat in records if name==m} for m in models]))
    assert common,'No matched cases'
    out.mkdir(parents=True,exist_ok=True)
    summary={}
    for m in models:
        ss=[records[m,*key] for key in common]
        seed_deltas=[mean(records[m,seed,seat]['reward']-records['E19',seed,seat]['reward'] for s,seat in common if s==seed) for seed in sorted({k[0] for k in common})]
        summary[m]=dict(cases=len(ss),cash=mean(s['reward'] for s in ss),median_cash=median(s['reward'] for s in ss),
            min_cash=min(s['reward'] for s in ss),stress=mean(len(s['crop_starvation']) for s in ss),
            animal_losses=sum(len(s['ledger']['animal_escapes']) for s in ss),
            positive_seeds_vs_E19=sum(d>0 for d in seed_deltas),seed_count=len(seed_deltas),
            median_seed_delta_vs_E19=median(seed_deltas),worst_seed_delta_vs_E19=min(seed_deltas),
            actions={a:mean(sum(d[a] for d in s['kpi']) for s in ss) for a in ['MOVE','PASS','WATER','FEED','CARE']})
    reference=summary['E19']
    complete=set(common)=={(s,p) for s in seeds for p in (0,1)}
    for m,v in summary.items():
        v['delta_vs_E19']=v['cash']-reference['cash']
        v['delta_percent_vs_E19']=100*(v['cash']/reference['cash']-1)
        v['gate_passed']=bool(complete and v['cash']>=reference['cash'] and v['median_seed_delta_vs_E19']>0
            and v['positive_seeds_vs_E19']>v['seed_count']/2 and v['stress']<=reference['stress'] and v['animal_losses']==0)
    rows=[dict(seed=seed,seat=seat,**{m:records[m,seed,seat]['reward'] for m in models}) for seed,seat in common]
    series={m:{k:[mean(records[m,*key]['kpi'][d][k] for key in common) for d in range(30)] for k in [f[0] for f in FIELDS]+['unlocked_tiles']} for m in models}
    data=dict(models=models,summary=summary,matched=rows,complete_both_seats=complete,
        expected_seeds=seeds,fields=FIELDS,series=series,sources=sources,
        note='Matched opponent E18, actual executed actions. Seats of one seed are paired, not independent replicates. Daily means are descriptive, not confidence intervals.')
    (out/'evaluation.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    with (out/'daily_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['model','seed','seat','day']+[k for k,_,_ in FIELDS]);w.writeheader()
        for m in models:
            for seed,seat in common:
                for day,kpi in enumerate(records[m,seed,seat]['kpi'],1):
                    w.writerow(dict(model=m,seed=seed,seat=seat,day=day,**{k:kpi[k] for k,_,_ in FIELDS}))
    lines=['# E20.1 — confronto appaiato','',
        f"Avversario comune E18; {len(common)} partite per modello. Copertura di tutti i seed attesi in entrambi i ruoli: {'sì' if complete else 'no: confronto parziale, non valido per la promozione'}.",'',
        '| Modello | Cassa media | Delta E19 | Seed positivi | Stress colture / partita | Perdite animali | Gate |',
        '|---|---:|---:|---:|---:|---:|---|']
    for m,v in summary.items():lines.append(f"| {m} | {v['cash']:,.1f} | {v['delta_percent_vs_E19']:+.2f}% | {v['positive_seeds_vs_E19']}/{v['seed_count']} | {v['stress']:.2f} | {v['animal_losses']} | {'PASS' if v['gate_passed'] else 'non superato'} |")
    lines+=['','## Distribuzione per seed e ruolo','','| Seed | Ruolo | '+' | '.join(models)+' |','|---|---|'+'---:|'*len(models)]
    for r in rows:lines.append(f"| {r['seed']} | {r['seat']} | "+' | '.join(f"{r[m]:,.0f}" for m in models)+' |')
    lines+=['','## Servizi eseguiti per partita','','| Modello | MOVE | PASS | WATER | FEED | CARE |','|---|---:|---:|---:|---:|---:|']
    for m,v in summary.items():lines.append('| '+m+' | '+' | '.join(f'{n:.1f}' for n in v['actions'].values())+' |')
    lines+=['','I seed di sviluppo già osservati non sono una conferma indipendente. Il diagnostico stress include transizioni crop→weed dopo mancata irrigazione: va letto insieme a età e produzione residua. I 22 KPI usano lo standard del progetto e il ledger verificato, non i comandi proposti.','',
        '[Traiettorie dei 22 KPI](REPORT.html) · [Dati e provenienza](evaluation.json) · [CSV giornaliero](daily_kpi.csv)']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    table='<table><tr><th>Modello</th><th>Cassa media</th><th>Δ E19</th><th>Stress / partita</th></tr>'+''.join(f'<tr><td>{m}</td><td>{v["cash"]:,.1f}</td><td>{v["delta_percent_vs_E19"]:+.2f}%</td><td>{v["stress"]:.2f}</td></tr>' for m,v in summary.items())+'</table>'
    page='''<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>E20.1 — 22 KPI</title>
<style>body{font:16px system-ui;background:#f4f5f8;color:#202735;margin:0;padding:24px;max-width:1400px;margin:auto}h1{font-size:30px}table{border-collapse:collapse;background:white;max-width:100%}td,th{padding:10px;border-bottom:1px solid #ddd;text-align:right}#charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:18px;margin-top:24px}article{background:white;border-radius:12px;padding:16px;min-width:0}svg{width:100%;height:auto}h2{font-size:17px}.legend{display:flex;gap:20px;flex-wrap:wrap}text{font:11px system-ui;fill:#555}</style>
<h1>E20.1 · traiettorie dei 22 KPI</h1><p>Avversario comune E18. Medie giornaliere sui medesimi seed e ruoli. I ruoli dello stesso seed non sono repliche indipendenti.</p>'''+table+'''<p id="coverage"></p><div class="legend" id="legend"></div><div id="charts"></div><script>
const D='''+json.dumps(data)+''';const colors=['#555d70','#e08a1e','#147db3','#a548a0','#168468','#b84a41','#3746bd'];
document.getElementById('coverage').textContent=D.complete_both_seats?'Copertura completa di entrambi i ruoli.':'Screen parziale: non valido per la promozione.';
D.models.forEach((m,i)=>{let e=document.createElement('span');e.textContent=m;e.style.color=colors[i%colors.length];document.getElementById('legend').append(e)});
for(const [key,label,unit] of D.fields){let card=document.createElement('article');let all=D.models.flatMap(m=>key==='crop_tiles'?[...D.series[m][key],...D.series[m].unlocked_tiles]:D.series[m][key]);let lo=Math.min(0,...all),hi=Math.max(1,...all);let x=d=>44+d*490/29,y=v=>185-(v-lo)*160/(hi-lo);let body='<path d="M44 25V185H534" fill="none" stroke="#bbb"/>';
for(let d of [0,9,19,29])body+=`<text x="${x(d)}" y="207" text-anchor="middle">D${d+1}</text>`;
for(let v of [lo,(lo+hi)/2,hi])body+=`<text x="39" y="${y(v)+4}" text-anchor="end">${Math.round(v).toLocaleString('it-IT')}</text>`;
D.models.forEach((m,i)=>{body+=`<polyline fill="none" stroke="${colors[i%colors.length]}" stroke-width="2.4" points="${D.series[m][key].map((v,d)=>x(d)+','+y(v)).join(' ')}"/>`;D.series[m][key].forEach((v,d)=>{body+=`<circle cx="${x(d)}" cy="${y(v)}" r="3" fill="transparent"><title>${m} · D${d+1}: ${v.toFixed(2)} ${unit}</title></circle>`})});
if(key==='crop_tiles')D.models.forEach((m,i)=>{body+=`<polyline fill="none" stroke="${colors[i%colors.length]}" stroke-dasharray="5 5" stroke-width="1.3" points="${D.series[m].unlocked_tiles.map((v,d)=>x(d)+','+y(v)).join(' ')}"><title>${m}: terreno sbloccato (tratteggio)</title></polyline>`});
card.innerHTML=`<h2>${label}</h2><svg viewBox="0 0 550 220" role="img" aria-label="${label}">${body}</svg>`;document.getElementById('charts').append(card)}
</script></html>'''
    (out/'REPORT.html').write_text(page,encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stages',nargs='+',required=True);p.add_argument('--models',nargs='+',default=['E19','E20v18','E20v24']);p.add_argument('--seeds',nargs='+',type=int,required=True);p.add_argument('--out',default='e20_1/development');a=p.parse_args()
    evaluate(a.stages,a.models,BASE/'reports'/a.out,a.seeds)
