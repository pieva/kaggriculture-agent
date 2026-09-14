"""External results, standard 22 KPIs and adjacent product volumes/prices."""
import csv,html,json,sys,statistics as st,hashlib
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
OUT=ROOT/'docs/model_specs/codex/e22/reports/external_e22_2_20260914'
PRODUCTS={'occupied_livestock_tiles':'FERTILIZER','COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG',**{x:x for x in ['MELON','WHEAT','STRAWBERRY','CARROT','TOMATO']}}
CSS='''body{font:15px/1.55 system-ui;background:#f4f6f8;color:#24344b;margin:0}main{max-width:1380px;margin:auto;padding:28px}h1{font-size:30px}h2{margin-top:30px}a{color:#176cb1}section,.card{background:white;border:1px solid #dce3ea;border-radius:9px;padding:16px}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}td,th{padding:8px 10px;border-bottom:1px solid #e0e5eb;text-align:right}td:first-child,th:first-child{text-align:left}.tablewrap{overflow:auto}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin:20px 0}h3{font-size:16px;margin:0 0 8px}.panel svg{width:100%;display:block}.detail,.meta{font-size:13px;color:#56647a}.toolbar{position:sticky;top:0;background:#f4f6f8;padding:12px 0;z-index:2;display:flex;gap:12px;flex-wrap:wrap;align-items:center}select,button,input{font:inherit;padding:7px}button{border:1px solid #b9c6d5;border-radius:5px;background:white}.note{border-left:4px solid #ce7628;padding:12px 16px;background:#fff5e9}.swatch{width:20px;display:inline-block;border-top:3px solid #1577bb}.orange{border-color:#ca6425}button[aria-pressed=false]{opacity:.4}svg text{font-family:system-ui;font-size:11px}pre{overflow:auto}@media(max-width:800px){main{padding:15px}.grid{grid-template-columns:1fr}}'''
CHART_JS=r'''
const D=JSON.parse(document.getElementById('data').textContent),fmt=v=>v==null?'n/d':new Intl.NumberFormat('it-IT',{maximumFractionDigits:1}).format(v),NS='http://www.w3.org/2000/svg';
const active=new Set([0,1]);function elem(t,a={},text){const e=document.createElementNS(NS,t);for(const [k,v] of Object.entries(a))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;return e}
function draw(){const view=D.views[document.getElementById('view').value],grid=document.getElementById('charts');grid.replaceChildren();document.getElementById('viewnote').textContent=view.note;document.querySelectorAll('[data-series]').forEach(b=>b.textContent=view.labels[+b.dataset.series]);
for(const m of D.metrics){const sec=document.createElement('section');sec.className='panel';sec.dataset.metric=m.key;const h=document.createElement('h3');h.textContent=m.label;sec.append(h);const svg=elem('svg',{viewBox:'0 0 600 280',role:'img','aria-label':m.label,tabindex:0});sec.append(svg);const info=document.createElement('div');info.className='detail';info.textContent=m.unit+' · D1–D30';sec.append(info);grid.append(sec);
const keys=m.key==='crop_tiles'?[m.key,'unlocked_tiles']:[m.key],vals=view.series.flatMap(s=>keys.flatMap(k=>s[k].flat())).filter(v=>v!==null),max=Math.max(1,...vals)*1.08,L=64,R=580,T=15,B=235,x=d=>L+d/29*(R-L),y=v=>B-v/max*(B-T);
for(let j=0;j<5;j++){let v=max*j/4;svg.append(elem('line',{x1:L,x2:R,y1:y(v),y2:y(v),stroke:'#dce3ea'}));svg.append(elem('text',{x:L-6,y:y(v)+4,'text-anchor':'end',fill:'#65748a'},max>9999?fmt(v/1000)+'k':fmt(v)))}for(const d of [1,5,10,15,20,25,30])svg.append(elem('text',{x:x(d-1),y:257,'text-anchor':'middle',fill:'#65748a'},'D'+d));
for(let s=0;s<2;s++){const g=elem('g',{'data-group':s});g.style.display=active.has(s)?'':'none';svg.append(g);for(const k of keys){const rows=view.series[s][k],color=s?'#ca6425':'#1577bb';let run=[];function flush(){if(!run.length)return;const path=run.map(([d,r],i)=>(i?'L':'M')+x(d)+','+y(r[0])).join(' ');if(k===m.key){const poly=run.map(([d,r])=>x(d)+','+y(r[2])).concat([...run].reverse().map(([d,r])=>x(d)+','+y(r[1]))).join(' ');g.append(elem('polygon',{points:poly,fill:color,opacity:.12}))}g.append(elem('path',{d:path,fill:'none',stroke:color,'stroke-width':2.5,'stroke-dasharray':k!==m.key?'7 4':s?'4 3':'none'}));for(const [d,r] of run)g.append(elem('circle',{cx:x(d),cy:y(r[0]),r:2,fill:color}));run=[]}rows.forEach((r,d)=>{if(r[0]===null)flush();else run.push([d,r])});flush()}}
const guide=elem('line',{y1:T,y2:B,stroke:'#334',visibility:'hidden'});svg.append(guide);let day=0,pinned=false;function show(d){day=Math.max(0,Math.min(29,d));guide.setAttribute('x1',x(day));guide.setAttribute('x2',x(day));guide.setAttribute('visibility','visible');info.textContent='D'+(day+1)+' · '+view.labels.map((label,s)=>active.has(s)?keys.map(k=>{const r=view.series[s][k][day];return label+(keys.length>1?' '+k:'')+': '+fmt(r[0])+' ['+fmt(r[1])+'–'+fmt(r[2])+']'}).join(' · '):'').filter(Boolean).join(' · ')}function at(e){const r=svg.getBoundingClientRect();return Math.round(((e.clientX-r.left)*600/r.width-L)/(R-L)*29)}svg.addEventListener('pointermove',e=>{if(!pinned)show(at(e))});svg.addEventListener('click',e=>{pinned=!pinned;show(at(e))});svg.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();pinned=true;show(day+(e.key==='ArrowRight'?1:-1))}})
}}
document.getElementById('view').addEventListener('change',draw);document.querySelectorAll('[data-series]').forEach(b=>b.addEventListener('click',()=>{const s=+b.dataset.series;active.has(s)?active.delete(s):active.add(s);b.setAttribute('aria-pressed',active.has(s));document.querySelectorAll('[data-group="'+s+'"]').forEach(g=>g.style.display=active.has(s)?'':'none')}));draw();
'''
def metric_defs():
 out=[]
 for i,(k,l,u) in enumerate(FIELDS,1):
  out.append(dict(key=k,label=f'{i:02d} · {l}',unit=u))
  if k in PRODUCTS:
   item=PRODUCTS[k];out.extend([dict(key='sold:'+item,label=item+' · unità vendute',unit='unità/giorno'),dict(key='price:'+item,label=item+' · prezzo realizzato',unit='monete/unità; ponderato sulle vendite')])
 return out
METRICS=metric_defs();KEYS=[m['key'] for m in METRICS]+['unlocked_tiles']
def rowdata(p):
 rows=[]
 for k,d in zip(p['kpi'],p['ledger']['daily']):
  row=dict(k)
  for item in PRODUCTS.values():
   n=d['sold_units'].get(item,0);row['sold:'+item]=n;row['price:'+item]=d['sales_cash'].get(item,0)/n if n else None
  rows.append(row)
 return rows
def aggregate(ps):
 rows=[rowdata(p) for p in ps];result={}
 for k in KEYS:
  result[k]=[]
  for d in range(30):
   vals=[r[d][k] for r in rows if r[d][k] is not None];result[k].append([st.median(vals),min(vals),max(vals)] if vals else [None]*3)
 return result
def summ(ps):
 own=[p['own'] for p in ps];margins=[p['meta']['own']['reward']-p['meta']['opponent']['reward'] for p in ps]
 return dict(n=len(ps),wins=sum(m>0 for m in margins),cash_mean=st.mean(p['reward'] for p in own),cash_median=st.median(p['reward'] for p in own),margin_mean=st.mean(margins),margin_median=st.median(margins),opponent_rating_mean=st.mean(p['meta']['opponent']['initialScore'] for p in ps),escapes=sum(len(p['ledger']['animal_escapes']) for p in own),crop_starvation=sum(len(p['crop_starvation']) for p in own),unfed=sum(len(p['unfed']) for p in own),policy_differences=sum(len(p['policy_differences']) for p in own),cash_errors=sum(p['ledger']['cash_parity_errors'] for p in own),mixes=dict(Counter(str({a:p['kpi'][-1][a] for a in ['COW','SHEEP','GOOSE']}) for p in own)),failed_actions=dict(Counter(e['command'][0] for p in own for e in p['failed_actions'])),mean_totals={k:{item:st.mean(p['totals'][k].get(item,0) for p in own) for item in set().union(*(p['totals'][k] for p in own))} for k in ['harvested','sold_units','sales_cash','purchase_cash']})
def page(title,body,data):
 controls='<div class="toolbar"><label>Vista <select id="view">'+''.join(f'<option value="{i}">{html.escape(v["title"])}</option>' for i,v in enumerate(data['views']))+'</select></label><button data-series="0" aria-pressed="true">Serie 1</button><button data-series="1" aria-pressed="true">Serie 2</button></div><p id="viewnote" class="meta"></p><div id="charts" class="grid"></div>'
 return '<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>'+CSS+'</style><main><h1>'+title+'</h1>'+body+controls+'</main><script type="application/json" id="data">'+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+'</script><script>'+CHART_JS+'</script></html>'
def main():
 ps=[json.loads(p.read_text()) for p in sorted((OUT/'profiles').glob('*.json'))];assert len(ps)==40
 groups={str(s):[p for p in ps if p['meta']['submission']==s] for s in [56212495,56206528]};summary={s:summ(p) for s,p in groups.items()};history=json.loads((OUT/'HISTORY_SUMMARY.json').read_text())
 for sid,h in history.items():
  eps=[e for e in h['episodes'] if e['state']=='COMPLETED' and e['type']=='EPISODE_TYPE_PUBLIC' and not e['selfplay']]
  h['results_all']=dict(n=len(eps),wins=sum(e['own']['reward']>e['opponent']['reward'] for e in eps),cash_mean=st.mean(e['own']['reward'] for e in eps),margin_mean=st.mean(e['own']['reward']-e['opponent']['reward'] for e in eps),opponent_rating_mean=st.mean(e['opponent']['initialScore'] for e in eps))
 common=set(e['opponent']['submissionId'] for e in history['56212495']['episodes'] if not e['selfplay'])&set(e['opponent']['submissionId'] for e in history['56206528']['episodes'] if not e['selfplay']);matched=[]
 for op in sorted(common):
  rec={'opponent_submission':op}
  for sid,h in history.items():
   es=[e for e in h['episodes'] if not e['selfplay'] and e['opponent']['submissionId']==op];rec[sid]={'n':len(es),'margin_mean':st.mean(e['own']['reward']-e['opponent']['reward'] for e in es)}
  matched.append(rec)
 diagnostics=[];rows=[]
 for p in ps:
  g=p['meta'];o=p['own'];r=json.loads((ROOT/g['path']).read_text());absent=[];hires=[]
  for i in range(719):
   obs=r['steps'][i][g['seat']]['observation'];a=r['steps'][i+1][g['seat']]['action'];f=obs['farms'][g['seat']]
   if a.get('market'):
    requested=sum(bool(c) and c[0]=='HIRE' for c in a['market']);nxt=r['steps'][i+1][g['seat']]['observation']['farms'][g['seat']]
    if requested and obs['hour']<23:
     got=nxt['hires_today']-f['hires_today']
     if got<requested:hires.append(dict(day=obs['day']+1,hour=obs['hour']+1,cash_before=f['money'],requested=requested,actual=got))
   for w,c in enumerate(a.get('hands',[]),1):
    if w>len(f['hands']) and c and c[0]!='PASS':absent.append(dict(day=obs['day']+1,hour=obs['hour']+1,worker=w,command=c))
  residual={item:sum(o['terminal'][kind].get(item,0) for kind in ['shed','carried','tile_yield_units']) for item in ['MILK','WOOL','EGG']}
  diagnostics.append(dict(submission=g['submission'],episode=g['episode'],hire_shortfalls=hires,commands_to_absent_workers=absent,stranded_cow=o['terminal']['shed'].get('COW',0),animal_product_residual=residual,unfed_days=o['unfed'],failed_actions=o['failed_actions']))
  for day,k in enumerate(rowdata(o),1):rows.append(dict(submission=g['submission'],episode=g['episode'],seat=g['seat'],day=day,**{key:k[key] for key in KEYS}))
 (OUT/'DIAGNOSTICS.json').write_text(json.dumps(diagnostics,separators=(',',':')))
 (OUT/'SUMMARY.json').write_text(json.dumps(dict(history={s:{k:v for k,v in h.items() if k!='episodes'} for s,h in history.items()},latest20=summary,common_opponents=matched),indent=2))
 with (OUT/'DAILY_22_KPI_PRICES.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 with (OUT/'ALL_RESULTS.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['submission','episode','created','state','selfplay','own_cash','opponent_cash','opponent_submission','own_rating_after','opponent_rating_before'])
  for sid,h in history.items():
   for e in h['episodes']:w.writerow([sid,e['episode'],e['created'],e['state'],e['selfplay'],e['own']['reward'],e['opponent']['reward'],e['opponent']['submissionId'],e['own'].get('updatedScore'),e['opponent'].get('initialScore')])
 views=[dict(title='E22.2 vs E22.1 · ultimi 20 per versione',labels=['E22.2 Pascoli','E22.1 Pollai'],note='Blu E22.2; arancio E22.1. Mediana puntuale e banda min–max. Coorti esterne non appaiate: avversari, semi e mercato diversi.',series=[aggregate([p['own'] for p in groups[s]]) for s in ['56212495','56206528']])]
 for p in ps:
  g=p['meta'];views.append(dict(title=f"E22.{2 if g['submission']==56212495 else 1} · episodio {g['episode']}",labels=[f"E22.{2 if g['submission']==56212495 else 1}",str(g['opponent']['submissionId'])],note='Confronto dei due lati della stessa partita; nessuna aggregazione.',series=[aggregate([p['own']]),aggregate([p['opponent']])]))
 data=dict(metrics=METRICS,views=views);(OUT/'CHART_DATA.json').write_text(json.dumps(data,separators=(',',':')))
 md='# E22.2 vs E22.1 — risultati esterni, 14 settembre 2026\n\n'
 md+='Entrambe Complete. Rating dell’ultimo episodio nello storico congelato: **E22.2 1706,92**, **E22.1 2147,08** (delta −440,16). Sono osservazioni temporalmente datate, non rating stabilizzati.\n\n| Versione | Episodi competitivi | Vittorie | Rating ultimo | Vittorie ultimi 20 | Cassa media ultimi 20 | Rating medio avversari ultimi 20 |\n|---|---:|---:|---:|---:|---:|---:|\n'
 for sid,label in [('56212495','E22.2'),('56206528','E22.1')]:
  h=history[sid];s=summary[sid];md+=f"| {label} | {h['competitive_n']} | {h['wins']} | {h['latest_rating']:.2f} | {s['wins']}/20 | {s['cash_mean']:.1f} | {s['opponent_rating_mean']:.1f} |\n"
 md+='\nLa percentuale di vittorie e la cassa grezza non provano superiorità di E22.2: affronta avversari mediamente più deboli (circa 407 punti in meno nel campione recente). Gli storici coprono durate diverse e includono la salita iniziale del rating. Un self-play per versione è escluso dalle medie. Nessun episodio non completato nello storico congelato.\n\n## Errori evidenti e controlli\n\n- **Due mucche mai collocate, in due replay E22.2 su 20** (108729054, 108777186): D2 H1 cassa 3, richiesti tre HIRE ma eseguiti due; operaio 3 assente alla costruzione D2 H6. D4 H24 PLACE COW fallisce sulla casella (2,4) priva di pascolo. Una mucca resta in magazzino; finale 7C9S. Il piano non recupera.\n- E22.2: 18/20 finali 8C9S, 2/20 7C9S; **zero fughe**. E22.1: **tre fughe** complessive, 16/20 mix atteso; ulteriori problemi di costruzione/collocamento.\n- In E22.2 si osservano 40 transizioni crop→weed dopo stress nel campione; sei PLANT senza effetto, spesso su infestanti non rimosse. Non confondere le caselle non irrigate al checkpoint con perdite certe.\n- Giorni isolati senza alimentazione e comandi CARE/WATER/HARVEST senza effetto sono documentati per episodio; alcuni sono ridondanze, non errori fatali.\n- Due fertilizzanti trasportati residui in ogni partita E22.2. Nessun residuo finale di latte/lana/uova, ma questo non implica vendita integrale: nei due casi con mucca bloccata si scartano 12 lane ciascuno (7 a D26 e 5 a D27) per saturazione del magazzino al refresh. Totale E22.2: 24 lane, 18 grani e 2 fertilizzanti scartati. E22.1 mostra overflow in 4/20 replay, con 25 lane, 11 latti e 19 uova persi. [Audit overflow](OVERFLOW.json).\n- **Parità del bundle E22.2 su 14.380 azioni**, altrettante per E22.1; zero errori di riconciliazione della cassa su tutti gli 80 lati analizzati. Nessuna simulazione nuova, nessuna modifica alla policy.\n\n## Lettura economica\n\nLa lana aumenta a 225 unità medie contro 158,1 di E22.1, ma il ricavo medio lana è 15.933,45 contro 15.444,20. Il confronto è descrittivo: prezzi e controparti differiscono. Il rapporto dei ricavi alle unità vendute è circa 71,20 contro 98,46 monete/lana (223,8 e 156,85 unità medie vendute). E22.2 rinuncia inoltre alle uova (ricavo medio E22.1 4.113,50). L’aumento di volume non si traduce in un aumento proporzionale di ricavi. Non attribuire tutto il divario di rating a una sola causa.\n\n## Metodo\n\nStorici completi acquisiti via EpisodeService/ListEpisodes; ultimi 20 incontri pubblici competitivi per submission, senza selezione per esito. 40 replay, 720 stati ciascuno, 80 ledger auditati. 22 KPI standard più nove coppie volumi/prezzo, immediatamente sotto la produzione associata: **40 pannelli**, selezione aggregata o singolo episodio. Mediana e min–max; prezzo realizzato ponderato sulle unità vendute in ogni partita/giorno, poi mediana tra le partite con vendite. Nessuna vendita = dato mancante, non zero. Cassa/consistenze al checkpoint 24D−1; flussi su tutti i batch. Nel grafico coltivate, la linea aggiuntiva tratteggiata mostra terreno sbloccato.\n\n[Report interattivo](REPORT.html) · [CSV 22 KPI e prezzi](DAILY_22_KPI_PRICES.csv) · [Tutti gli esiti](ALL_RESULTS.csv) · [Diagnostica](DIAGNOSTICS.json) · [Catalogo e hash](COHORT.json) · [Protocollo](PROTOCOL.json) · [Top 2750–3000](../top_2750_3000_20260914/REPORT.html).\n'
 (OUT/'REPORT.md').write_text(md,encoding='utf-8')
 table='<div class="tablewrap"><table><tr><th>Versione</th><th>Rating ultimo</th><th>Vittorie storico</th><th>Vittorie recenti</th><th>Cassa media recente</th><th>Rating avversari recente</th></tr>'
 for sid,label in [('56212495','E22.2'),('56206528','E22.1')]:
  h=history[sid];s=summary[sid];table+=f"<tr><td>{label}</td><td>{h['latest_rating']:.2f}</td><td>{h['wins']}/{h['competitive_n']}</td><td>{s['wins']}/20</td><td>{s['cash_mean']:.1f}</td><td>{s['opponent_rating_mean']:.1f}</td></tr>"
 body='<p>Snapshot del 14 settembre 2026 · submission <a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56212495">56212495</a> e 56206528 · entrambe Complete.</p>'+table+'</table></div><p class="note"><b>E22.2 è sotto E22.1 di circa 440 punti.</b> Le coorti recenti affrontano avversari diversi: la cassa media maggiore di E22.2 non prova superiorità.</p><p><b>Difetto concreto:</b> in 2/20 replay di E22.2 manca un manovale a D2, il pascolo (2,4) non viene costruito e una mucca resta in magazzino. In questi due casi il magazzino saturo scarta inoltre 12 lane ciascuno a D26–27. Zero fughe E22.2, tre E22.1; 40 transizioni di colture a infestanti dopo stress per E22.2. Bundle eseguiti fedelmente e contabilità riconciliata.</p><p><a href="REPORT.md">Diagnosi completa e metodo</a> · <a href="DAILY_22_KPI_PRICES.csv">CSV giornaliero</a> · <a href="ALL_RESULTS.csv">Tutti gli esiti</a> · <a href="COHORT.json">Replay e hash</a> · <a href="../top_2750_3000_20260914/REPORT.html">Topologie e traiettorie top</a></p><p class="meta">22 KPI standard + 18 pannelli volumi/prezzi associati alle produzioni. Prezzi senza vendite = n/d. Passaggio/clic e frecce sui grafici per i valori. Checkpoint H24 prima dell’ultimo batch D1–D29; D30 terminale. I flussi coprono tutte le azioni del giorno.</p>'
 (OUT/'REPORT.html').write_text(page('E22.2 / E22.1 · 22 KPI e prezzi esterni',body,data),encoding='utf-8')
 verify=dict(games=40,profiles=80,kpi=22,price_panels=9,volume_panels=9,views=len(views),cash_parity_errors=sum(p[k]['ledger']['cash_parity_errors'] for p in ps for k in ['own','opponent']),policy_actions_verified=40*719,failed_policy_actions=sum(len(p['own']['policy_differences']) for p in ps),new_simulations=0)
 assert verify['cash_parity_errors']==0 and verify['failed_policy_actions']==0
 assert all(all(v==0 for v in d['animal_product_residual'].values()) for d in diagnostics)
 overflow=json.loads((OUT/'OVERFLOW.json').read_text());overflow_map={(r['submission'],r['episode']):r for r in overflow}
 for p in ps:
  losses=sum((Counter(e['discarded']) for e in overflow_map[(p['meta']['submission'],p['meta']['episode'])]['events']),Counter())
  for item in ['MILK','WOOL','EGG']:
   assert p['own']['totals']['harvested'].get(item,0)==p['own']['totals']['sold_units'].get(item,0)+losses[item]
 verify['overflow_transitions_verified']=40*29;verify['animal_product_mass_balance']='harvest = sold + observed discarded; all 40 own profiles pass'
 (OUT/'VERIFICATION.json').write_text(json.dumps(verify,indent=2));print(json.dumps(verify),flush=True)
if __name__=='__main__':main()
