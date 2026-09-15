"""Frozen external crop economics for E24. No new games or policy execution."""
import contextlib,io,json,sys,hashlib,gzip,csv,statistics as st
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[5]
SOURCE=Path('C:/Users/pietr/.codex/worktrees/756c/kaggriculture-agent')
OUT=ROOT/'docs/model_specs/codex/e24/reports/crop_economics_20260915'
CROPS=['MELON','WHEAT','STRAWBERRY','CARROT','TOMATO']
PRODUCTS=CROPS+['MILK','WOOL','EGG','FERTILIZER']
NAMES={'E22.1':'E22.1 · 8C6S3G','56218385':'Catalyst','56222223':'Thomas Tschinkel','56223630':'Deodims & Co'}
sys.path.insert(0,str(SOURCE))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
  from docs.model_specs.codex.e22.tools.analyze_external_20260914 import enrich
  from docs.model_specs.codex.e22.tools.report_external_20260914 import page,METRICS,aggregate
 groups={k:[] for k in NAMES}; manifest=[]
 baseline=SOURCE/'docs/model_specs/codex/e23/reports/external_e22_1_q2_grano_20260914/profiles'
 for path in sorted(baseline.glob('*.json')):
  d=read(path); assert d['meta']['submission']==56228842
  groups['E22.1'].append(d['own']); manifest.append(dict(group='E22.1',episode=d['meta']['episode'],seat=d['meta']['seat'],profile_path=str(path),profile_sha256=digest(path),replay_sha256=d['meta']['sha256']))
 origin=ROOT/'docs/model_specs/codex/e23/reports/near3000_20260914'
 profiles={ (p['submission'],p['episode']):p for p in read(origin/'PROFILES.json') }
 cohort=[g for g in read(origin/'COHORT.json') if str(g['submission']) in NAMES]+read(origin/'CONFIRMATION.json')['games']
 for g in cohort:
  key=str(g['submission']); ep=g['episode']; seat=g['seat']; path=ROOT/f'data/replays/json/e23_near3000_20260914/{ep}.json'
  sha=g.get('sha256') or profiles[g['submission'],ep]['sha256']; assert digest(path)==sha
  cache=OUT/f'profile_{ep}_{seat}.json.gz'
  if cache.exists(): p=json.loads(gzip.decompress(cache.read_bytes()))
  else:
   r=read(path)
   for i,s in enumerate(r['steps']):s[0]['observation']['step']=i
   p=enrich(r,seat); cache.write_bytes(gzip.compress(json.dumps(p,separators=(',',':')).encode(),compresslevel=6))
  groups[key].append(p); manifest.append(dict(group=key,episode=ep,seat=seat,replay_sha256=sha,profile_path=cache.relative_to(ROOT).as_posix(),profile_sha256=digest(cache)))
  print('Audited',key,ep,flush=True)
 assert len(groups['E22.1'])==20 and all(len(groups[k])==8 for k in list(NAMES)[1:])
 summary={}; rows=[]
 for key,ps in groups.items():
  gs={'label':NAMES[key],'n':len(ps),'cash_mean':st.mean(p['reward'] for p in ps),'cash_min':min(p['reward'] for p in ps),'cash_max':max(p['reward'] for p in ps),'products':{},'costs':{}}
  for item in PRODUCTS:
   vals=[]
   for p in ps:
    t=p['totals']; sales=t['sales_cash'].get(item,0); units=t['sold_units'].get(item,0); seeds=t['purchase_cash'].get('BUY_SEED:'+item,0)
    vals.append(dict(revenue=sales,seeds=seeds,partial_margin=sales-seeds,units=units,harvest=t['harvested'].get(item,0),product_purchases=t['purchase_cash'].get('BUY_PRODUCT:'+item,0),planted=t['planted'].get(item,0)))
   gs['products'][item]={k:st.mean(v[k] for v in vals) for k in vals[0]}
   gs['products'][item]['net_product_cash']=gs['products'][item]['revenue']-gs['products'][item]['seeds']-gs['products'][item]['product_purchases']
   gs['products'][item]['price']=sum(v['revenue'] for v in vals)/sum(v['units'] for v in vals) if sum(v['units'] for v in vals) else None
   gs['products'][item]['revenue_min']=min(v['revenue'] for v in vals);gs['products'][item]['revenue_max']=max(v['revenue'] for v in vals)
  for k in ['hire_cash','land_cash','unit_cash_delta']:gs['costs'][k]=st.mean(p['totals'][k] for p in ps)
  gs['costs']['purchases']=st.mean(sum(p['totals']['purchase_cash'].values()) for p in ps)
  gs['costs']['animal_purchases']=st.mean(sum(v for k,v in p['totals']['purchase_cash'].items() if k.startswith('BUY_ANIMAL:')) for p in ps)
  assert abs(3000+sum(v['revenue'] for v in gs['products'].values())-gs['costs']['purchases']-gs['costs']['hire_cash']-gs['costs']['land_cash']+gs['costs']['unit_cash_delta']-gs['cash_mean'])<1e-6
  summary[key]=gs
  for p,m in zip(ps,[m for m in manifest if m['group']==key]):
   assert p['ledger']['cash_parity_errors']==0
   for day in p['ledger']['daily']:
    for item in PRODUCTS:
     rows.append(dict(group=key,episode=m['episode'],day=day['day'],product=item,revenue=day['sales_cash'].get(item,0),seed_cost=day['purchase_cash'].get('BUY_SEED:'+item,0),product_purchase_cost=day['purchase_cash'].get('BUY_PRODUCT:'+item,0),sold=day['sold_units'].get(item,0),harvested=day['harvested'].get(item,0),planted=day['planted'].get(item,0)))
 (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
 with (OUT/'CROP_DAILY.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 # Preserve the baseline profiles too; next session does not depend on another checkout.
 (OUT/'BASELINE_PROFILES.json.gz').write_bytes(gzip.compress(json.dumps(groups['E22.1'],separators=(',',':')).encode(),compresslevel=6))
 data=dict(metrics=METRICS,views=[dict(title='E22.1 / '+NAMES[k],labels=[NAMES['E22.1'],NAMES[k]],note='Replay congelati 14 settembre: E22.1 n=20; top n=8. Mediana e min–max giornalieri. Mercati e avversari diversi; confronto descrittivo.',series=[aggregate(groups['E22.1']),aggregate(groups[k])]) for k in list(NAMES)[1:]])
 fmt=lambda v: f'{v:,.0f}'.replace(',','.')
 body='<p>Base E24 · replay esterni congelati il 14 settembre 2026 · 20 E22.1 e 8 per ciascuno dei tre top selezionati.</p><p class="note">E22.1 è il candidato di punta indicato dall’utente. Questo confronto usa la submission 56228842, identica al bundle ripubblicato il 15 settembre; non contiene partite della nuova submission. Il torneo E23 non ha mostrato un miglioramento sufficiente: ciò non esclude ogni possibile modifica agli animali.</p>'
 body+='<h2>Risultati e ponte contabile</h2><div class="tablewrap"><table><tr><th>Serie</th><th>n</th><th>Cassa media</th><th>Ricavi</th><th>Acquisti</th><th>Manodopera</th><th>Terreni</th></tr>'
 for key,g in summary.items():body+='<tr><td>'+g['label']+'</td>'+''.join('<td>'+fmt(x)+'</td>' for x in [g['n'],g['cash_mean'],sum(v['revenue'] for v in g['products'].values()),g['costs']['purchases'],g['costs']['hire_cash'],g['costs']['land_cash']])+'</tr>'
 body+='</table></div><p>Verifica: cassa iniziale 3.000 + ricavi − acquisti − manodopera − terreni + altri flussi unità = cassa finale, per ogni replay.</p>'
 body+='<h2>Istogrammi per coltura</h2><section><label>Periodo <select id="cropPeriod"><option value="1,30">D1–D30</option><option value="1,10">D1–D10</option><option value="11,20">D11–D20</option><option value="21,30">D21–D30</option></select></label><p>Medie per partita. Blu: ricavi delle vendite; arancio: semi; viola: acquisti del prodotto; verde: saldo ricavi meno entrambi gli acquisti. Valori esatti al passaggio del mouse. Il verde è un saldo di cassa per prodotto, prima dei costi condivisi; include anche commercio e autoconsumo.</p><div id="cropBars" class="grid"></div><div id="cropTable" class="tablewrap"></div></section>'
 body+='<p class="note">Gli acquisti di prodotto sono distinti dai semi: il grano comprato alimenta anche gli animali e non è automaticamente un costo della coltivazione. Fertilizzante, manodopera e terreni restano condivisi, senza ripartizioni arbitrarie. I semi sono esborsi nel periodo, non costi ammortizzati. Le produzioni autoconsumate non sono ricavi; le scorte finali non vengono valorizzate come vendite.</p>'
 body+='<h2>Prodotti, volumi e prezzi realizzati</h2><div class="tablewrap"><table><tr><th>Serie / prodotto</th><th>Ricavi medi</th><th>Semi</th><th>Acquisto prodotto</th><th>Raccolto</th><th>Venduto</th><th>Prezzo ponderato</th></tr>'
 for key,g in summary.items():
  for item,v in g['products'].items():body+='<tr><td>'+g['label']+' / '+item+'</td>'+''.join('<td>'+('n/d' if x is None else fmt(x))+'</td>' for x in [v['revenue'],v['seeds'],v['product_purchases'],v['harvest'],v['units'],v['price']])+'</tr>'
 body+='</table></div><h2>Priorità E24</h2><div id="findings">FINDINGS_PLACEHOLDER</div><p><a href="CROP_DAILY.csv">Dati giornalieri per replay</a> · <a href="SUMMARY.json">Sintesi numerica</a> · <a href="MANIFEST.json">Campione e hash</a> · <a href="REPORT.md">Metodo e lettura</a></p><h2>22 KPI, volumi e prezzi D1–D30</h2>'
 js=r'''const cropRows=CROP_ROWS,labels=CROP_LABELS,crops=['MELON','WHEAT','STRAWBERRY','CARROT','TOMATO'],counts=CROP_COUNTS;function cropDraw(){let [lo,hi]=document.getElementById('cropPeriod').value.split(',').map(Number),root=document.getElementById('cropBars');root.replaceChildren();let table='<table><tr><th>Coltura / serie</th><th>Ricavi</th><th>Semi</th><th>Acquisto prodotto</th><th>Saldo prodotto</th></tr>';for(let crop of crops){let vals=['E22.1','56218385','56222223','56223630'].map(k=>{let rr=cropRows.filter(r=>r.group===k&&r.product===crop&&r.day>=lo&&r.day<=hi);let rev=rr.reduce((a,r)=>a+r.revenue,0)/counts[k],cost=rr.reduce((a,r)=>a+r.seed_cost,0)/counts[k];let buys=rr.reduce((a,r)=>a+r.product_purchase_cost,0)/counts[k];return [rev,cost,buys,rev-cost-buys]});let max=Math.max(1,...vals.flat().map(Math.abs)),sec=document.createElement('section'),h=document.createElement('h3');h.textContent=crop+' · D'+lo+'–D'+hi;sec.append(h);let svg=elem('svg',{viewBox:'0 0 680 440',role:'img','aria-label':'Costi e ricavi '+crop});svg.style.width='100%';let zero=220,scale=320/max;svg.append(elem('line',{x1:zero,x2:zero,y1:15,y2:430,stroke:'#556'}));['E22.1','56218385','56222223','56223630'].map(k=>[k,labels[k]]).forEach(([key,label],i)=>{svg.append(elem('text',{x:6,y:38+i*103},label));vals[i].forEach((v,j)=>{let rect=elem('rect',{x:v>=0?zero:zero+v*scale,y:18+i*103+j*19,width:Math.abs(v)*scale,height:15,fill:['#1577bb','#ca6425','#8056a8','#288765'][j]});rect.append(elem('title',{},label+' · '+['Ricavi','Semi','Acquisto prodotto','Saldo prodotto'][j]+': '+fmt(v)));svg.append(rect);svg.append(elem('text',{x:zero+(v>=0?v*scale+4:v*scale-4),y:30+i*103+j*19,'text-anchor':v>=0?'start':'end'},fmt(v)))});table+='<tr><td>'+crop+' / '+label+'</td>'+vals[i].map(v=>'<td>'+fmt(v)+'</td>').join('')+'</tr>'});sec.append(svg);root.append(sec)}document.getElementById('cropTable').innerHTML=table+'</table>'}document.getElementById('cropPeriod').addEventListener('change',cropDraw);cropDraw();'''
 js=js.replace('CROP_ROWS',json.dumps(rows)).replace('CROP_LABELS',json.dumps(NAMES)).replace('CROP_COUNTS',json.dumps({k:len(p) for k,p in groups.items()}))
 body=body.replace('FINDINGS_PLACEHOLDER',(OUT/'FINDINGS.html').read_text(encoding='utf-8'))
 out=page('E24 · E22.1 e top: economia delle colture',body,data).replace('</html>','<script>'+js+'</script></html>')
 (OUT/'REPORT.html').write_text(out,encoding='utf-8')
 verify=dict(profiles=44,cash_parity_errors=0,top_replay_hashes_verified=24,new_games=0,standard_panels=len(METRICS),crop_histograms=5,baseline_submission=56228842,top_submissions=[56218385,56222223,56223630],snapshot_date='2026-09-14',report_date='2026-09-15')
 (OUT/'VERIFICATION.json').write_text(json.dumps(verify,indent=2),encoding='utf-8')
 print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
