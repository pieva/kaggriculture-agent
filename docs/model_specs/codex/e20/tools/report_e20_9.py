"""Readable paired 22 KPI report, production followed immediately by its market."""
import json,gzip,hashlib,sys,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'docs/model_specs/codex/e20'
OUT=BASE/'reports/e20_9_release'
def main():
    rows=[]
    for model,stage,label in [('Reference','c','E20.8'),('Finance','c','Correzioni senza pomodori'),('Tomato','d','E20.9')]:
        for seed in [180911301,180911303]:
            for seat in [0,1]:
                names=[model,'E18'] if seat==0 else ['E18',model]
                p=BASE/f'artifacts/e20_9_development_{stage}'/f'{names[0]}_{names[1]}_{seed}.kpi.json'
                k=json.loads(p.read_text());s=k['sides'][seat]
                replay=p.with_name(p.name.replace('.kpi.json','.replay.json.gz'))
                r=json.load(gzip.open(replay,'rt',encoding='utf-8'))
                market={}
                for product in r['steps'][-1][seat]['observation']['market']['prices']:
                    market[product]=[]
                    for d,l in enumerate(s['ledger']['daily'],1):
                        q=l['sold_units'].get(product,0);revenue=l['sales_cash'].get(product,0)
                        o=r['steps'][min(d*24,719)][seat]['observation']
                        market[product].append({'volume':q,'revenue':revenue,'realized':revenue/q if q else None,'spot':o['market']['prices'][product]})
                assert s['ledger']['cash_parity_errors']==0
                assert all(x['status']=='DONE' for x in r['steps'][-1]) and len(r['steps'])==720
                assert sum(x['verified_animal_losses'] for x in s['kpi'])==0
                assert s['kpi'][-1]['animals']=={'COW':8,'SHEEP':6,'GOOSE':2}
                assert s['kpi'][-1]['pasture_topology']=={'Q0':7,'Q1':6,'Q2':1,'Q3':0}
                if model=='Tomato':
                    assert s['terminal']['shed'].get('TOMATO',0)==0 and s['terminal']['carried'].get('TOMATO',0)==0
                    assert sum(v['volume'] for v in market['TOMATO'])>0
                rows.append(dict(model=label,seed=seed,seat=seat,cash=s['reward'],opponent=k['sides'][1-seat]['reward'],kpi=s['kpi'],market=market,terminal=s['terminal'],crop_losses=s['crop_starvation'],replay=str(replay.relative_to(ROOT)),sha256=hashlib.sha256(replay.read_bytes()).hexdigest()))
    fields=json.loads((BASE/'reports/external_e20_8_20260913/REPORT_DATA.json').read_text())['fields']
    data=dict(rows=rows,fields=fields)
    (OUT/'REPORT_DATA.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
    with (OUT/'DAILY_22_KPI.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['model','seed','seat','day']+[x[0] for x in fields])
        for r in rows:
            for day in r['kpi']:w.writerow([r['model'],r['seed'],r['seat'],day['day']]+[day[x[0]] for x in fields])
    with (OUT/'PRODUCTS.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['model','seed','seat','product','day','volume','revenue','realized','spot'])
        for r in rows:
            for p,days in r['market'].items():
                for d,x in enumerate(days,1):w.writerow([r['model'],r['seed'],r['seat'],p,d]+list(x.values()))
    template=(BASE/'tools/e20_8_external_template.html').read_text(encoding='utf-8')
    chart=template.split('function chart(')[1].split('\nconst s=D.summary')[0]
    css=template.split('<style>')[1].split('</style>')[0]
    intro='''<h1>E20.9 — correzione dell’apertura e pomodori tardivi</h1>
<p>Derivata dalla 772 operativa: 14 pascoli (7-6-1), 2 pollai, 8 mucche, 6 pecore e 2 oche. Due fragole sostituite da pomodori a D20–D21. Candidata sperimentale, non pubblicata.</p>
<p class="warning">Nei 20 controlli delle aperture esterne, la correzione recupera le tre aperture critiche: cassa D1 da 0 a 26, tre assunzioni a D2 e quattro animali conservati. Mosse avversarie registrate e seed sostitutivo esposto: verifica diagnostica, non torneo reattivo.</p>
<p>Il controllo «Correzioni senza pomodori» include rimozione del giro di acquisto/vendita del grano a D1 H1 e anticipo dei rientri finali. Il confronto con E20.9 isola l’aggiunta delle due caselle di pomodoro. Due seed già esposti, entrambi i ruoli: i ruoli danno risultati uguali e non costituiscono quattro scenari indipendenti.</p>
<p><a href="REPORT.md">Valutazione e limiti</a> · <a href="OPENINGS.json">Aperture</a> · <a href="DAILY_22_KPI.csv">22 KPI</a> · <a href="PRODUCTS.csv">Vendite e prezzi</a></p>
<div class="toolbar"><label>Scenario <select id="case"><option value="all">Media dei due seed e ruoli</option><option value="180911301">Seed 180911301</option><option value="180911303">Seed 180911303</option></select></label></div><div id="table" class="scroll"></div>
<p class="note">22 KPI standard. Sotto ogni produzione: volumi venduti e prezzo realizzato ponderato, poi prezzo di mercato a fine giornata. Tutti gli assi temporali D1–D30; nessuna vendita = prezzo realizzato assente, non zero. Il fertilizzante è associato all’insieme degli animali. Le medie di scenario non sono una singola partita.</p><div id="panels"></div>'''
    js='''
const labels=['E20.8','Correzioni senza pomodori','E20.9'];
const products={MELON:'MELON',WHEAT:'WHEAT',STRAWBERRY:'STRAWBERRY',CARROT:'CARROT',TOMATO:'TOMATO',COW:'MILK',SHEEP:'WOOL',GOOSE:'EGG',occupied_livestock_tiles:'FERTILIZER'};
function render(){let rows=D.rows.filter(r=>el('case').value==='all'||r.seed==el('case').value);el('panels').innerHTML='';
el('table').innerHTML='<table><tr><th>Variante</th><th>Cassa media</th><th>Margine su E18</th><th>Vittorie / prove</th></tr>'+labels.map(m=>{let rs=rows.filter(r=>r.model===m);return `<tr><td>${m}</td><td>${fmt(avg(rs.map(r=>r.cash)),1)}</td><td>${fmt(avg(rs.map(r=>r.cash-r.opponent)),1)}</td><td>${rs.filter(r=>r.cash>r.opponent).length} / ${rs.length}</td></tr>`}).join('')+'</table>';
function series(fn){return labels.map((m,i)=>({name:m,color:C[i],dash:i===1,points:Array.from({length:30},(_,d)=>[d+1,fn(rows.filter(r=>r.model===m),d)])}))}
D.fields.forEach(([key,label,unit])=>{let box=document.createElement('section');box.className='product';box.innerHTML=`<h2>${label}</h2><div class="tiles"></div>`;el('panels').appendChild(box);let ss=series((rs,d)=>avg(rs.map(r=>r.kpi[d][key])));if(key==='crop_tiles')ss.push(...series((rs,d)=>avg(rs.map(r=>r.kpi[d].unlocked_tiles))).map(s=>({...s,name:s.name+' terreno sbloccato',dash:true})));chart(box.querySelector('.tiles'),ss,unit);
let p=products[key];if(p){let below=document.createElement('div');below.innerHTML=`<h3>${p} · volumi venduti</h3><div class="vol"></div><h3>${p} · prezzi unitari realizzati</h3><div class="price"></div><h3>${p} · prezzo di mercato a fine giornata</h3><div class="spot"></div>`;box.appendChild(below);chart(below.querySelector('.vol'),series((rs,d)=>avg(rs.map(r=>r.market[p][d].volume))),'unità / giorno');chart(below.querySelector('.price'),series((rs,d)=>{let q=rs.reduce((s,r)=>s+r.market[p][d].volume,0);return q?rs.reduce((s,r)=>s+r.market[p][d].revenue,0)/q:null}),'denaro / unità');chart(below.querySelector('.spot'),series((rs,d)=>avg(rs.map(r=>r.market[p][d].spot))),'denaro / unità')}})}
el('case').addEventListener('change',render);render();
'''
    # Include missing-sale days in the x domain, even when no realized price exists.
    chart=chart.replace("xmin=Math.min(...pts.map(p=>p[0])),xmax=Math.max(...pts.map(p=>p[0]))","xmin=1,xmax=30")
    html='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>E20.9 · 22 KPI e produzione</title><style>'+css+'</style><main>'+intro+'</main><script>const D='+json.dumps(data,ensure_ascii=False)+';const C=["#1479b8","#d57120","#279272"];const fmt=(v,n=0)=>v==null?"—":v.toLocaleString("it-IT",{maximumFractionDigits:n});const avg=a=>a.reduce((s,v)=>s+v,0)/a.length;const el=id=>document.getElementById(id);function chart('+chart+js+'</script></html>'
    (OUT/'REPORT.html').write_text(html,encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['model','seed','seat','cash','opponent','terminal']} for r in rows],indent=2))
if __name__=='__main__':main()
