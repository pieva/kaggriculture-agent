"""Readable pilot evidence and a browser explorer of observed decision contexts."""
import csv,html,json
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]/'reports/top_trigger_pilot_20260913'


def main():
    analysis=json.loads((OUT/'ANALYSIS.json').read_text(encoding='utf-8'))
    replication=json.loads((OUT/'YARN_REPLICATION.json').read_text(encoding='utf-8'))
    profiles=[json.loads(p.read_text(encoding='utf-8')) for p in (OUT/'profiles').glob('*.json')]
    rules={'Olympus':(8,2),'kiki yi2':(8,2),'Majkel1337':(7,7)};discovery=[]
    for p in profiles:
        if p['name'] not in rules:continue
        day,hour=rules[p['name']]
        es=[e for e in p['events'] if e['kind']=='BUY_ANIMAL' and e['features']['day']==day and e['features']['hour']==hour]
        assert len(es)==1
        e=es[0];f=e['features'];yarn='YARN_STORE' in f['shops'];sheep=any(c[1]=='SHEEP' and c[2]>0 for c in e['choice'])
        discovery.append(dict(name=p['name'],episode=p['episode'],day=day,hour=hour,yarn=yarn,sheep=sheep,match=yarn==sheep,prices=f['prices'],cash=f['cash'],requested=e['choice']))
    assert len(discovery)==15 and all(x['match'] for x in discovery)
    (OUT/'YARN_DISCOVERY.json').write_text(json.dumps(discovery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    csvrows=[]
    for p in profiles:
        for e in p['events']:
            f=e['features'];row=dict(name=p['name'],submission=p['submission'],episode=p['episode'],kind=e['kind'],step=e['step'],day=f['day'],hour=f['hour'],choice=json.dumps(e['choice']),cell=str(e.get('cell','')),cash=f['cash'],people=f['people'],shops=json.dumps(f['shops'],sort_keys=True))
            row.update({f'price_{k}':v for k,v in f['prices'].items()})
            row.update({f'own_{k}':f['own'].get(k,0) for k in ['COW','SHEEP','GOOSE','MELON','STRAWBERRY','TOMATO','WHEAT','CARROT']})
            row.update({f'opponent_{k}':f['opponent'].get(k,0) for k in ['COW','SHEEP','GOOSE','MELON','STRAWBERRY','TOMATO','WHEAT','CARROT']})
            csvrows.append(row)
    with (OUT/'DECISIONS.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(csvrows[0]));w.writeheader();w.writerows(csvrows)
    for m in analysis['models']:
        m['purchases']=[dict(episode=p['episode'],**e) for p in profiles if p['submission']==m['submission'] for e in p['events'] if e['kind']=='BUY_ANIMAL' and e['features']['day']<=12]
    table=''.join(f"<tr><td>{html.escape(m['name'])}</td><td>{m['rating']:.1f}</td><td>{100*m['mean_worker_share']:.1f}%</td><td>{m['n_animal_branches']}</td><td>{m['n_crop_branches']}</td></tr>" for m in analysis['models'])
    rr=''.join(f"<tr><td>{html.escape(r['name'])}</td><td><a href='https://www.kaggle.com/competitions/episodes/{r['episode']}/replay.json'>{r['episode']}</a></td><td>D{r['day']} H{r['hour']}</td><td>{'sì' if r['yarn'] else 'no'}</td><td>{html.escape(str(r['requested']))}</td><td>{r['prices']['WOOL']}</td><td>{'coerente' if r['match'] else 'controesempio'}</td></tr>" for r in replication['rows'])
    payload=json.dumps(analysis['models'],ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    (OUT/'REPORT.html').write_text(TEMPLATE.replace('__TABLE__',table).replace('__REPLICATION__',rr).replace('__DATA__',payload),encoding='utf-8')
    print('Reports saved; decision events:',len(csvrows),'replication:',replication['matches'],'/',replication['n'])


TEMPLATE='''<!doctype html><html lang="it"><meta charset="utf-8"><title>E22 · Trigger dei top</title><style>body{font:16px system-ui;background:#f3f5f0;color:#24332d;max-width:1350px;margin:32px auto;padding:0 24px}section{padding:24px;background:#fff;border-radius:12px;margin:22px 0}h1{font-size:34px}h2{font-size:23px}p{line-height:1.55}a{color:#176e57}table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:10px;text-align:left;border-bottom:1px solid #dae0d8;vertical-align:top}select{font:inherit;padding:10px;max-width:100%;margin:6px}.muted{color:#58685f}.callout{border-left:5px solid #197b67;padding-left:18px}.overflow{overflow:auto}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}@media(max-width:850px){.grid{grid-template-columns:1fr}}</style>
<h1>E22 · Quali segnali cambiano il piano dei top?</h1><p>Classifica congelata il 13 settembre 2026 · 6 submission, 5 replay ciascuna · 9 replay aggiuntivi per una replica dell'ipotesi.</p>
<p><a href="REPORT.md">Analisi e limiti</a> · <a href="DECISIONS.csv">Decisioni e stato precedente CSV</a> · <a href="PROTOCOL.json">Campionamento</a></p>
<section class="callout"><h2>Scelta consigliata: 2000–2500 per isolare i trigger, 3000+ come confronto</h2><p>Il pilota mostra scelte più localizzate e colture più stabili nella fascia intermedia. I tre top cambiano molto di più le successioni colturali. Tuttavia il primo classificato condivide un segnale animale leggibile con due modelli intermedi: domanda di lana e passaggio alle pecore.</p><p>Non assumiamo che score maggiore significhi codice indecifrabile. Il campione serve a scegliere casi di studio, non a stimare la complessità di un'intera fascia.</p></section>
<section><h2>Variabilità osservata nella stessa submission</h2><table><tr><th>Modello</th><th>Rating</th><th>Gruppi di comandi identici, media fra replay</th><th>Slot animali con alternative</th><th>Slot colturali con alternative</th></tr>__TABLE__</table><p class="muted">Uno slot confronta la stessa casella e lo stesso numero progressivo di collocamento/semina, con almeno tre osservazioni. Non è un ramo del codice: ritardi, perdite e precedenti scelte possono alterare l'allineamento. Le coppie di replay non sono indipendenti.</p></section>
<section><h2>Primo pattern replicato: domanda di lana → acquisto di pecore</h2><p>Olympus e kiki yi2, D8 H2; Majkel1337, D7 H7. Nei 15 replay esplorativi, presenza di YARN_STORE prima dell'azione e ordine che include SHEEP coincidono. Ipotesi congelata prima di acquisire 9 ulteriori replay: <b>9/9 coerenti, con 6 casi positivi e 3 negativi</b>.</p><div class="overflow"><table><tr><th>Modello</th><th>Replay aggiuntivo</th><th>Decisione</th><th>Negozio lana</th><th>Ordine emesso</th><th>Prezzo lana prima</th><th>Esito</th></tr>__REPLICATION__</table></div><p class="muted">È una replica osservazionale, non prova del codice interno. Negozio, prezzo e domanda sono correlati. Gli ordini possono fallire per cassa insufficiente: qui misuriamo la scelta emessa, non il suo successo. Non estendere automaticamente questa regola a tutti i giorni o modelli.</p></section>
<section><h2>Due casi da approfondire: spbforce</h2><div class="grid"><div><h3>Espansione delle pecore a D13</h3><p>Replay 108505403: due negozi di lana, prezzo 238, cassa 14.101 a H1; acquisto di terreno a H2 e allevamento che raggiunge 17 pecore a D20. Nel replay 108503246 la lana vale ancora 238, ma c'è un solo negozio e nessuna espansione. Il prezzo istantaneo da solo non separa questi casi.</p></div><div><h3>Dieci pomodori a D19</h3><p>Replay 108504264: prezzo pomodoro 87 e cassa 45.259 a H1; espansione a H2 e dieci semine nello stesso giorno. Nel replay 108505285, con cassa maggiore (46.073) ma pomodoro a 64, nessuna espansione. La cassa da sola non separa questi casi.</p></div></div><p class="muted">Due casi esplorativi, non soglie identificate. Disponibilità di terreno, domanda persistente, mix già scelto e tempo residuo restano possibili condizioni.</p></section>
<section><h2>Esplora le alternative e lo stato precedente</h2><select id="model"></select><select id="kind"><option value="ANIMAL">Collocamenti animali</option><option value="CROP">Semine</option><option value="STRUCTURE">Strutture</option><option value="PURCHASE">Acquisti animali D1–D12</option></select><select id="slot"></select><div id="details"></div></section>
<script>const models=__DATA__;const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const fmt=x=>Number(x).toLocaleString('it-IT',{maximumFractionDigits:1});let options=[];
function load(){const m=models[document.getElementById('model').value],kind=document.getElementById('kind').value;options=m.branches.filter(b=>b.kind===kind);document.getElementById('slot').hidden=kind==='PURCHASE';document.getElementById('slot').innerHTML=options.map((b,i)=>`<option value="${i}">Casella (${b.cell.join(',')}) · ciclo ${b.ordinal} · D${b.day_range.join('–')}</option>`).join('');show()}
function show(){const m=models[document.getElementById('model').value],kind=document.getElementById('kind').value,b=options[document.getElementById('slot').value],es=kind==='PURCHASE'?m.purchases:(b?b.events:[]);document.getElementById('details').innerHTML=`<h3>${esc(m.name)} · submission ${m.submission}</h3><p class="muted">${kind==='PURCHASE'?'Stato prima dell’ordine di acquisto.':'Stato prima dell’azione nel campo; la specie può essere stata scelta e acquistata prima. Queste righe non identificano da sole il trigger iniziale.'}</p>${es.length?`<div class="overflow"><table><tr><th>Replay</th><th>Tempo</th><th>Scelta</th><th>Cassa</th><th>Latte / lana / uova</th><th>Pomodoro / fragola</th><th>Negozi</th><th>Animali propri C/S/G</th><th>Animali avversari C/S/G</th></tr>${es.map(e=>{const f=e.features;return `<tr><td><a href="https://www.kaggle.com/competitions/episodes/${e.episode}/replay.json">${e.episode}</a></td><td>D${f.day} H${f.hour}</td><td>${esc(typeof e.choice==='string'?e.choice:JSON.stringify(e.choice))}</td><td>${fmt(f.cash)}</td><td>${['MILK','WOOL','EGG'].map(p=>f.prices[p]).join(' / ')}</td><td>${['TOMATO','STRAWBERRY'].map(p=>f.prices[p]).join(' / ')}</td><td>${Object.entries(f.shops).map(([k,v])=>esc(k)+' ×'+v).join('<br>')}</td><td>${['COW','SHEEP','GOOSE'].map(p=>f.own[p]||0).join(' / ')}</td><td>${['COW','SHEEP','GOOSE'].map(p=>f.opponent[p]||0).join(' / ')}</td></tr>`}).join('')}</table></div>`:'Nessuno slot con alternative e almeno tre osservazioni in questa categoria. Non significa assenza di variabilità: possono cambiare quantità, geometria o tempi.'}`}
document.getElementById('model').innerHTML=models.map((m,i)=>`<option value="${i}">${esc(m.name)} · ${m.rating}</option>`).join('');document.getElementById('model').addEventListener('change',load);document.getElementById('kind').addEventListener('change',load);document.getElementById('slot').addEventListener('change',show);load();</script></html>'''


if __name__=='__main__':main()
