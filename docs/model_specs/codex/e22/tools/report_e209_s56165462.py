"""Reproducible KPI comparison from previously cash-audited replay ledgers."""
import csv,html,json
from e209_s56165462_charts import dashboard
from pathlib import Path
from statistics import mean,median

ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/e22/reports/opponent_strategy_20260913'
OUT=ROOT/'docs/model_specs/codex/e22/reports/e209_s56165462_kpi_20260913'
PRODUCTS=['MELON','STRAWBERRY','WOOL','MILK','EGG','CARROT','TOMATO','WHEAT','FERTILIZER']
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def net(d):return sum(d['sales_cash'].values())-sum(d['purchase_cash'].values())-d['hire_cash']-d['land_cash']+d['unit_cash_delta']
def total(p,field,item):return sum(d[field].get(item,0) for d in p['ledger']['daily'])
def fmt(x):return str(x) if isinstance(x,str) else f'{x:,.1f}'.replace(',','X').replace('.',',').replace('X','.')
def table(headers,rows):return '<div class="scroll"><table><tr>'+''.join('<th>'+html.escape(h)+'</th>' for h in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(fmt(v))+'</td>' for v in r)+'</tr>' for r in rows)+'</table></div>'
def main():
 OUT.mkdir(exist_ok=True)
 game=read(BASE/'profiles/108480607.json');ps=[game['own'],game['opponent']]
 for p in ps:
  assert p['ledger']['cash_parity_errors']==0
  assert 3000+sum(net(d) for d in p['ledger']['daily'])==p['reward']
 headline=[]
 metrics=[('Cassa finale',lambda p:p['reward']),('Ricavi lordi',lambda p:sum(p['totals']['sales_cash'].values())),('Acquisti totali',lambda p:sum(p['totals']['purchase_cash'].values())),('Costo lavoratori',lambda p:p['totals']['hire_cash']),('Costo terreni',lambda p:p['totals']['land_cash']),('Assunzioni totali (giornaliere)',lambda p:sum(d['hires'] for d in p['ledger']['daily'])),('Comandi MOVE richiesti',lambda p:total(p,'requested_actions','MOVE')),('Comandi PASS richiesti',lambda p:total(p,'requested_actions','PASS')),('FEED eseguiti',lambda p:total(p,'executed_actions','FEED')),('Fughe animali verificate',lambda p:len(p['ledger']['animal_escapes']))]
 for label,fn in metrics:
  a,b=map(fn,ps);headline.append([label,a,b,b-a])
 products=[]
 for item in PRODUCTS:
  vals=[]
  for p in ps:
   t=p['totals'];q=t['sold_units'].get(item,0);r=t['sales_cash'].get(item,0);vals.extend([t['harvested'].get(item,0),q,r/q if q else '—',r])
  products.append([item,*vals,vals[7]-vals[3]])
 phases=[]
 for lo,hi in [(1,6),(7,11),(12,19),(20,29),(30,30)]:
  a,b=[sum(net(d) for d in p['ledger']['daily'] if lo<=d['day']<=hi) for p in ps];phases.append([f'D{lo}–D{hi}',a,b,b-a])
 assert sum(r[-1] for r in phases)==10946
 costs=[]
 for key in sorted(set().union(*(p['totals']['purchase_cash'] for p in ps))):
  a,b=[p['totals']['purchase_cash'].get(key,0) for p in ps];costs.append([key,a,b,a-b])
 for key in ['hire_cash','land_cash','unit_cash_delta']:
  a,b=[p['totals'][key] for p in ps];costs.append([key,a,b,(b-a) if key=='unit_cash_delta' else a-b])
 assert sum(r[-1] for r in products)+sum(r[-1] for r in costs)==10946
 grain=[]
 for label,fn in [('Raccolto',lambda p:total(p,'harvested','WHEAT')),('Comprato',lambda p:total(p,'bought_units','BUY_PRODUCT:WHEAT')),('Venduto',lambda p:total(p,'sold_units','WHEAT')),('FEED',lambda p:total(p,'executed_actions','FEED')),('Costo acquisti',lambda p:total(p,'purchase_cash','BUY_PRODUCT:WHEAT')),('Ricavo vendite',lambda p:total(p,'sales_cash','WHEAT'))]:grain.append([label,*map(fn,ps)])
 context=[]
 own=[read(p) for p in (BASE/'profiles').glob('*.json')];group=next(g for g in read(BASE/'VARIABILITY.json')['groups'] if g['name']=='s56165462')
 for label,vals in [('E20.9, 33 avversari vari',[g['own']['reward'] for g in own]),('s56165462, 3 avversari vari',[m['rewards'][m['seat']] for m in group['members']])]:context.append([label,len(vals),mean(vals),median(vals),min(vals),max(vals)])
 days=[]
 for i in range(30):
  row={'day':i+1}
  for label,p in zip(['E20.9','s56165462'],ps):
   d=p['ledger']['daily'][i];row[label]={'cash':p['daily'][i]['money'],'net':net(d),'sales':d['sales_cash'],'units':d['sold_units'],'wheat_bought':d['bought_units'].get('BUY_PRODUCT:WHEAT',0),'wheat_cost':d['purchase_cash'].get('BUY_PRODUCT:WHEAT',0),'feed':d['executed_actions'].get('FEED',0)}
  days.append(row)
 data=dict(episode=108480607,source=str(BASE/'profiles/108480607.json'),headline=headline,products=products,costs=costs,phases=phases,grain=grain,context=context,daily=days,terminal=[p['terminal'] for p in ps],d20=[p['daily'][19] for p in ps])
 (OUT/'KPI.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 for name,heads,rows in [('PRODUCTS',['Prodotto','E20 raccolto','E20 venduto','E20 prezzo medio','E20 ricavi','DB raccolto','DB venduto','DB prezzo medio','DB ricavi','Delta ricavi DB-E20'],products),('DAILY',['Giorno','Modello','Cassa','Flusso netto','Grano acquistato','Spesa grano','FEED'],[[d['day'],s,d[s]['cash'],d[s]['net'],d[s]['wheat_bought'],d[s]['wheat_cost'],d[s]['feed']] for d in days for s in ['E20.9','s56165462']])]:
  with (OUT/f'{name}.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.writer(f);w.writerow(heads);w.writerows(rows)
 intro='Scontro diretto 108480607: E20.9 70.898, s56165462 81.844. Distacco 10.946 monete (+15,4% rispetto alla nostra cassa). La cassa è il risultato della partita, non il rating Kaggle. Entrambi partono da 3.000; verifica già completata delle 719 transizioni di cassa per entrambi e riconciliazione dei totali.'
 findings='Il distacco comprende +3.890 ricavi dai meloni, +1.943 dalla lana e 1.974 di minor costo del lavoro. Entrambi raccolgono 72 meloni, ma noi ne vendiamo 66 contro 72 e a prezzo medio inferiore. s56165462 vende inoltre 28 fragole e 22 uova in più. Sono contributi contabili: non provano l’effetto causale di una singola scelta.'
 body='<h1>E20.9 vs s56165462 · KPI</h1><p>'+intro+'</p><p><a href="KPI.json">Dati JSON</a> · <a href="PRODUCTS.csv">Prodotti CSV</a> · <a href="DAILY.csv">Giorni CSV</a></p><section><h2>Cosa spiega il risultato</h2><p>'+findings+'</p>'+table(['KPI','E20.9','s56165462','Differenza DB − E20'],headline)+'</section>'
 body+='<section><h2>Quando si forma il distacco</h2>'+table(['Fase','Flusso netto E20.9','Flusso netto DB','Vantaggio DB'],phases)+'<p>Flusso netto = vendite − acquisti − lavoro − terreni + altre variazioni monetarie. Le fasi sommano esattamente il distacco finale.</p><div id="chart"></div></section>'
 body+='<section><h2>Produzione e monetizzazione</h2><p>Quantità raccolte e vendute sono distinte. Prezzo medio ponderato = ricavi / unità vendute. Grano e fertilizzante possono provenire da acquisti; fertilizzante raccolto tramite COLLECT_FERTILIZER non è contato dal campo HARVEST.</p>'+table(['Prodotto','E20 raccolto','E20 venduto','E20 prezzo','E20 ricavi','DB raccolto','DB venduto','DB prezzo','DB ricavi','Delta ricavi'],products)+'<h3>Vendite giornaliere</h3><select id="product">'+''.join('<option>'+p+'</option>' for p in PRODUCTS)+'</select><div id="sales"></div></section>'
 body+='<section><h2>Costi: contributo al distacco</h2>'+table(['Voce','E20.9','s56165462','Vantaggio economico DB'],costs)+'<p>Delta ricavi più vantaggio dei costi = 10.946. Il costo delle assunzioni cresce in modo non lineare: confrontare anche i picchi giornalieri prima di attribuire il divario alla sola quantità di lavoro. MOVE e PASS sono comandi richiesti, non misure automatiche di spreco o di produttività.</p></section>'
 labor=[]
 for i in range(30):
  a,b=[p['ledger']['daily'][i] for p in ps];labor.append([i+1,a['hires'],b['hires'],a['hire_cash'],b['hire_cash'],a['hire_cash']-b['hire_cash']])
 body+='<section><h2>Assunzioni e picchi di costo</h2>'+table(['Giorno','E20 assunzioni','DB assunzioni','E20 costo','DB costo','Minor costo DB'],labor)+'</section>'
 body+='<section><h2>Grano: produzione, autoconsumo e mercato</h2>'+table(['KPI','E20.9','s56165462'],grain)+'<p>La minore spesa di acquisto non coincide con un risparmio netto da autoconsumo: cambiano anche vendite, scorte e tempi. Non attribuiamo univocamente l’origine del grano usato nei FEED. Il confronto vendita alta/riacquisto basso richiede la sequenza delle transazioni, non solo prezzi medi mensili.</p></section>'
 body+='<section><h2>Configurazione D20 e chiusura</h2>'+table(['Voce','E20.9','s56165462'],[[k,*[json.dumps(p['daily'][19][k],ensure_ascii=False) for p in ps]] for k in ['animals','crops','livestock_structures','unlocked_tiles']]+[[k,*[json.dumps(p['terminal'][k]) for p in ps]] for k in ['shed','carried','seeds','tile_yield_units']])+'<p>Gli avanzi non sono valutati automaticamente al prezzo finale: la liquidazione richiede azioni fattibili e muove il mercato. I sei meloni raccolti ma non venduti non risultano nello stock finale; il bilancio dei ricavi non ne identifica da solo il destino.</p></section>'
 body+='<section><h2>Contesto fuori dallo scontro diretto</h2>'+table(['Campione','N','Cassa media','Mediana','Min','Max'],context)+'<p>Campioni descrittivi, non accoppiati: cambiano avversari e mercati; non usare la differenza delle medie come stima di forza. Lo scontro diretto è incluso in entrambi. La configurazione di s56165462 è stabile nei tre replay analizzati. Nessuna nuova simulazione competitiva eseguita.</p></section>'
 body+='<section><h2>Priorità E22</h2><ol><li>Ricostruire le consegne dei meloni: stessa produzione raccolta, monetizzazione diversa.</li><li>Confrontare assunzioni e picchi di lavoro nei giorni costosi, verificando servizi e quantità vendute.</li><li>Spiegare i cicli aggiuntivi di fragole e lana; distinguere produzione da liquidazione.</li><li>Misurare grano e fertilizzante come ciclo integrato, preservando tempi e impatto sul mercato.</li></ol><p>Fonte: profilo economico verificato dello scontro diretto; inventari e snapshot congelati il 13 settembre 2026. E20.9 submission 56202079; s56165462 56166543.</p></section>'
 js='''<script>const days=DATA;const names=['E20.9','s56165462'];const f=x=>x.toLocaleString('it-IT',{maximumFractionDigits:1});const colors=['#2563eb','#c05e12'];const max=Math.max(...days.flatMap(d=>names.map(n=>d[n].cash)));document.getElementById('chart').innerHTML='<p style="color:#2563eb">Blu: E20.9 · <span style="color:#c05e12">arancio: s56165462</span> · Cassa D1–D30</p><svg viewBox="0 0 900 240" role="img" aria-label="Cassa giornaliera">'+names.map((n,i)=>'<polyline fill="none" stroke="'+colors[i]+'" stroke-width="3" points="'+days.map((d,j)=>(20+j*29)+','+(215-195*d[n].cash/max)).join(' ')+'"/>').join('')+'<text x="20" y="237">D1</text><text x="830" y="237">D30</text><text x="20" y="15">'+f(max)+'</text></svg>';function show(){const p=document.getElementById('product').value;document.getElementById('sales').innerHTML='<div class="scroll"><table><tr><th>Giorno</th><th>E20 unità</th><th>E20 prezzo medio</th><th>E20 ricavi</th><th>DB unità</th><th>DB prezzo medio</th><th>DB ricavi</th></tr>'+days.map(d=>'<tr><td>'+d.day+'</td>'+names.map(n=>{const q=d[n].units[p]||0,r=d[n].sales[p]||0;return '<td>'+q+'</td><td>'+(q?f(r/q):'—')+'</td><td>'+f(r)+'</td>'}).join('')+'</tr>').join('')+'</table></div>'}document.getElementById('product').addEventListener('change',show);show();</script>'''.replace('DATA',json.dumps(days))
 (OUT/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>E20.9 vs s56165462 · KPI</title><style>body{font:16px system-ui;max-width:1400px;margin:30px auto;padding:0 22px;background:#f3f5f0;color:#24332d}section{background:white;padding:24px;margin:22px 0;border-radius:12px}p{line-height:1.6}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:10px;border-bottom:1px solid #dde2dc;text-align:right}th:first-child,td:first-child{text-align:left}.scroll{overflow:auto}svg{width:100%;max-height:290px}select{padding:10px;font:inherit}a{color:#176e57}</style>'+dashboard(ps)+'<details><summary>Tabelle di verifica, metodo e contesto</summary>'+body+'</details>'+js+'</html>',encoding='utf-8')
 md='# E20.9 vs s56165462 — KPI\n\n'+intro+'\n\n'+findings+'\n\n[Report interattivo](REPORT.html) · [Dati verificabili](KPI.json)\n\n| KPI | E20.9 | s56165462 | DB − E20 |\n|---|---:|---:|---:|\n'+'\n'.join('| '+' | '.join(map(fmt,r))+' |' for r in headline)+'\n\nUn solo scontro diretto; i campioni esterni (33 e 3 partite) non sono accoppiati. Nessuna conclusione causale o stima di rating dalla differenza di cassa. Report HTML con prodotti, prezzi ponderati, fasi, costi, grano, residui e dettaglio giornaliero.\n'
 (OUT/'REPORT.md').write_text(md,encoding='utf-8')
 print(json.dumps({'headline':headline,'phases':phases,'grain':grain,'context':context},ensure_ascii=True))
if __name__=='__main__':main()
