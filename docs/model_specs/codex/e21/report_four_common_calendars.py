"""Readable paired 22 KPI report, production followed immediately by its market."""
import json,gzip,hashlib,sys,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'docs/model_specs/codex/e21';E20=ROOT/'docs/model_specs/codex/e20'
OUT=BASE/'reports/four_common_calendars';OUT.mkdir(exist_ok=True)
def main():
    rows=[]
    cases=[('OpRecorded','operational772_recorded_control','Piano comune nativo'),('Tomato','e20_9_development_d','772 fix + pomodori (E20.9)'),('Common774','operational774_v1','774 comune')]
    for model,stage,label in cases:
        for seed in [180911301,180911303]:
            for seat in [0,1]:
                p=(E20 if model=='Tomato' else BASE)/f'artifacts/{stage}'/f'{model}_E18_{seed}.kpi.json'
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
                rows.append(dict(model=label if seat==0 else "E18.2 V4D",context=label,seed=seed,seat=seat,cash=s['reward'],opponent=k['sides'][1-seat]['reward'],kpi=s['kpi'],market=market,terminal=s['terminal'],crop_losses=s['crop_starvation'],replay=str(replay.relative_to(ROOT)),sha256=hashlib.sha256(replay.read_bytes()).hexdigest()))
    fields=json.loads((E20/'reports/external_e20_8_20260913/REPORT_DATA.json').read_text())['fields']
    data=dict(rows=rows,fields=fields)
    (OUT/'REPORT_DATA.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
    with (OUT/'DAILY_22_KPI.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['model','context','seed','seat','day']+[x[0] for x in fields])
        for r in rows:
            for day in r['kpi']:w.writerow([r['model'],r['context'],r['seed'],r['seat'],day['day']]+[day[x[0]] for x in fields])
    with (OUT/'PRODUCTS.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['model','context','seed','seat','product','day','volume','revenue','realized','spot'])
        for r in rows:
            for p,days in r['market'].items():
                for d,x in enumerate(days,1):w.writerow([r['model'],r['context'],r['seed'],r['seat'],p,d]+list(x.values()))
    template=(E20/'tools/e20_8_external_template.html').read_text(encoding='utf-8')
    chart=template.split('function chart(')[1].split('\nconst s=D.summary')[0]
    css=template.split('<style>')[1].split('</style>')[0]
    intro="""<h1>Piano comune, 772 comune, 774 comune ed E18.2 V4D</h1><p>Confronto di sei partite esistenti: due seed esposti (180911301/303), ciascun calendario nel ruolo0 contro E18.2 V4D nel ruolo1. Nessuna nuova simulazione. Piano nativo: programma comune registrato, geometria770; 772 con fix e pomodori: E20.9/v44 con pascoli761 e2oche; 774 comune: E21 Common774 V1, pascoli774 e1oca. Sono tre partite distinte per seed, non un torneo diretto fra i tre calendari.</p><p><b>La772 con fix e pomodori non prevale sulla E18.2 in queste prove:97105,5 contro98276 (−1170,5).</b> Perde entrambi i seed:301 (−1885) e303 (−456). La precedente prevalenza media di308,5 riguardava E20.8, non questa variante. Ha cassa più alta della774 nei rispettivi match, ma un margine inferiore sull’avversaria. Il mercato cambia con entrambi gli agenti.</p><p>La curva E18.2 dipende dalla partita: seleziona sotto l’avversario di riferimento. Il default è la E18.2 che affronta la772. Le altre tre curve provengono dai rispettivi match contro E18.2. <a href="REPORT.md">Metodo e risultati</a> · <a href="DAILY_22_KPI.csv">22 KPI CSV</a> · <a href="PRODUCTS.csv">Vendite e prezzi</a></p><div class="toolbar"><label>Scenario <select id="case"><option value="all">Media dei due seed</option><option value="180911301">Seed180911301</option><option value="180911303">Seed180911303</option></select></label><label>E18.2 nella partita contro <select id="context"><option>772 fix + pomodori (E20.9)</option><option>Piano comune nativo</option><option>774 comune</option></select></label></div><div id="table" class="scroll"></div><p>22 KPI. Subito sotto ogni produzione: volumi venduti, prezzo realizzato ponderato e prezzo di mercato. Tutti gli assi D1–D30. Nessuna vendita = prezzo realizzato assente. Le medie non sono una singola partita.</p><div id="panels"></div>"""
    js='''
const labels=['Piano comune nativo','772 fix + pomodori (E20.9)','774 comune','E18.2 V4D'];
const products={MELON:'MELON',WHEAT:'WHEAT',STRAWBERRY:'STRAWBERRY',CARROT:'CARROT',TOMATO:'TOMATO',COW:'MILK',SHEEP:'WOOL',GOOSE:'EGG',occupied_livestock_tiles:'FERTILIZER'};
function render(){let rows=D.rows.filter(r=>(el('case').value==='all'||r.seed==el('case').value)&&(r.model!=='E18.2 V4D'||r.context===el('context').value));el('panels').innerHTML='';
el('table').innerHTML='<table><tr><th>Variante</th><th>Cassa media</th><th>Margine sul proprio avversario</th><th>Vittorie / prove</th></tr>'+labels.map(m=>{let rs=rows.filter(r=>r.model===m);return `<tr><td>${m}</td><td>${fmt(avg(rs.map(r=>r.cash)),1)}</td><td>${fmt(avg(rs.map(r=>r.cash-r.opponent)),1)}</td><td>${rs.filter(r=>r.cash>r.opponent).length} / ${rs.length}</td></tr>`}).join('')+'</table>';
function series(fn){return labels.map((m,i)=>({name:m,color:C[i],dash:i===1,points:Array.from({length:30},(_,d)=>[d+1,fn(rows.filter(r=>r.model===m),d)])}))}
D.fields.forEach(([key,label,unit])=>{let box=document.createElement('section');box.className='product';box.innerHTML=`<h2>${label}</h2><div class="tiles"></div>`;el('panels').appendChild(box);let ss=series((rs,d)=>avg(rs.map(r=>r.kpi[d][key])));if(key==='crop_tiles')ss.push(...series((rs,d)=>avg(rs.map(r=>r.kpi[d].unlocked_tiles))).map(s=>({...s,name:s.name+' terreno sbloccato',dash:true})));chart(box.querySelector('.tiles'),ss,unit);
let p=products[key];if(p){let below=document.createElement('div');below.innerHTML=`<h3>${p} · volumi venduti</h3><div class="vol"></div><h3>${p} · prezzi unitari realizzati</h3><div class="price"></div><h3>${p} · prezzo di mercato a fine giornata</h3><div class="spot"></div>`;box.appendChild(below);chart(below.querySelector('.vol'),series((rs,d)=>avg(rs.map(r=>r.market[p][d].volume))),'unità / giorno');chart(below.querySelector('.price'),series((rs,d)=>{let q=rs.reduce((s,r)=>s+r.market[p][d].volume,0);return q?rs.reduce((s,r)=>s+r.market[p][d].revenue,0)/q:null}),'denaro / unità');chart(below.querySelector('.spot'),series((rs,d)=>avg(rs.map(r=>r.market[p][d].spot))),'denaro / unità')}})}
el('case').addEventListener('change',render);el('context').addEventListener('change',render);render();
'''
    # Include missing-sale days in the x domain, even when no realized price exists.
    chart=chart.replace("xmin=Math.min(...pts.map(p=>p[0])),xmax=Math.max(...pts.map(p=>p[0]))","xmin=1,xmax=30")
    html='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Quattro calendari - 22 KPI</title><style>'+css+'</style><main>'+intro+'</main><script>const D='+json.dumps(data,ensure_ascii=False)+';const C=["#7e55a7","#1479b8","#279272","#d57120"];const fmt=(v,n=0)=>v==null?"—":v.toLocaleString("it-IT",{maximumFractionDigits:n});const avg=a=>a.reduce((s,v)=>s+v,0)/a.length;const el=id=>document.getElementById(id);function chart('+chart+js+'</script></html>'
    (OUT/'REPORT.html').write_text(html,encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['model','seed','seat','cash','opponent','terminal']} for r in rows],indent=2))
if __name__=='__main__':main()
