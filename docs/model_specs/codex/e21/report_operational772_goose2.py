from pathlib import Path
import sys,json,gzip,hashlib,csv,html
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
OUT=BASE/'reports/operational772_goose2_v2'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def table(headers,rows):return '<table><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</table>'
def load(stage,name,seed):
 path=BASE/f'artifacts/{stage}/{name}_E18_{seed}'
 return read(path.with_suffix('.json')),read(path.with_suffix('.kpi.json'))['sides'][0],path
rows=[];verification=[];melon=[];flows=[];data=[]
for seed in [180911301,180911303]:
 cases=[('772 pubblicata','calendar772_c1' if seed==180911301 else 'operational772_validation','Base772'),('V8 senza oche','operational772_v8' if seed==180911301 else 'operational772_validation','Op772'),('V8 con 2 oche','operational772_goose2_v2','Goose2')]
 profiles=[];original_sites=None
 for label,stage,name in cases:
  meta,p,path=load(stage,name,seed);profiles.append((label,p));r=json.load(gzip.open(path.with_suffix('.replay.json.gz'),'rt',encoding='utf-8'))
  f=r['steps'][-1][0]['observation']['farms'][0]
  sites={(x,y):(t['kind'],t.get('animal')) for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict) and t.get('kind') in ['PASTURE','COOP']}
  if name=='Base772':original_sites=sites
  last=p['kpi'][-1];losses=sum(d['verified_animal_losses'] for d in p['kpi'])
  rows.append([seed,label,int(p['reward']),int(meta['rewards'][1]),int(p['reward']-meta['rewards'][1]),'/'.join(str(last[k]) for k in ['COW','SHEEP','GOOSE']),'/'.join(str(p['kpi'][d-1]['STRAWBERRY']) for d in [6,9,12]),losses])
  ledger=p['ledger']['daily'];sales={k:sum(d['sales_cash'].get(k,0) for d in ledger) for k in ['MILK','EGG','WOOL']}
  flows.append([seed,label,sales['MILK'],sales['EGG'],sales['WOOL'],sum(sum(d['sales_cash'].values()) for d in ledger),sum(sum(d['purchase_cash'].values()) for d in ledger),sum(d['hire_cash'] for d in ledger)])
  for d in p['kpi']:data.append(dict(seed=seed,version=label,day=d['day'],**{k:d[k] for k,_,_ in FIELDS}))
  melon.append({'seed':seed,'version':label,'end_of_day_counts':[d['MELON'] for d in p['kpi'][:12]],'planted':[{ 'day':d['day'],'units':d['planted'].get('MELON',0)} for d in ledger if d['planted'].get('MELON')],'harvested':[{ 'day':d['day'],'units':d['harvested'].get('MELON',0)} for d in ledger if d['harvested'].get('MELON')]})
  if name=='Goose2':
   expected=dict(original_sites)
   for pos in [(6,3),(4,5)]:expected[pos]=('COOP','GOOSE')
   check={'seed':seed,'exact_expected_sites':sites==expected,'calls':meta['runtime'][0]['calls'],'core_errors':meta['runtime'][0]['core_errors'],'animal_losses':losses,'final_mix':{k:last[k] for k in ['COW','SHEEP','GOOSE']},'crop_losses':len(p['crop_starvation']),'terminal':p['terminal'],'cash_parity_errors':p['ledger']['cash_parity_errors']}
   verification.append(check)
   assert check['exact_expected_sites'] and check['calls']==719 and check['core_errors']==0 and losses==0,check
 fig,axes=plt.subplots(11,2,figsize=(16,33))
 for ax,(key,title,unit) in zip(axes.flat,FIELDS):
  for (label,p),color,style in zip(profiles,['#89939d','#156b98','#d06900'],[':','--','-']):ax.plot(range(1,31),[d[key] for d in p['kpi']],label=label,color=color,ls=style,lw=1.8)
  ax.set_title('Caselle coltivate' if key=='crop_tiles' else title);ax.set_ylabel(unit);ax.set_xlabel('Giorno (conteggio a fine giornata)');ax.grid(alpha=.2);ax.set_xlim(1,30)
  if key=='MELON':ax.annotate('V8 e variante oche coincidono: raccolta D11',xy=(11,0),xytext=(12,8),fontsize=8,arrowprops={'arrowstyle':'->'})
 h,l=axes.flat[0].get_legend_handles_labels();fig.legend(h,l,loc='upper center',ncol=3);fig.tight_layout(rect=(0,0,1,.98));fig.savefig(OUT/f'KPI22_{seed}.png',dpi=110);plt.close(fig)
protocol=read(OUT/'PROTOCOL.json')
for name,digest in protocol['sources'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
(OUT/'VERIFICATION.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
(OUT/'MELONS.json').write_text(json.dumps(melon,indent=2),encoding='utf-8')
(OUT/'RESULTS.json').write_text(json.dumps({'columns':['seed','version','cash','opponent_cash','margin','mix_C_S_G','strawberries_D6_D9_D12','animal_losses'],'rows':rows},indent=2),encoding='utf-8')
with (OUT/'KPI22.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
body='''<h1>Due mucche sostituite con due oche</h1><p>Confronto della V8 con <strong>8 mucche, 6 pecore e 2 oche</strong> contro la V8 con 10 mucche e 6 pecore. Le caselle (6,3) e (4,5) diventano pollai. Restano 16 caselle animali, di cui 14 pascoli e 2 pollai: la sigla dei soli pascoli è 7-6-1. Coordinate (x,y) da zero.</p><p>Conservati calendario colturale, rotte, aiutante aggiuntivo e regole di mercato della V8; acquisti e vendite rispondono alle nuove specie attraverso le stesse regole sulle scorte osservate. Le giornate di collocamento restano quelle previste per i due animali sostituiti. Non è la ricostruzione del nativo con tre oche.</p><h2>Risultati: stessi due seed e ruolo 0 contro la 775 congelata</h2>'''
body+=table(['Seed','Versione','Cassa','Cassa 775','Scarto contro 775','Mucche/pecore/oche','Fragole D6/9/12','Fughe'],rows)
body+='<p><strong>Le due oche migliorano la cassa di 3.398 e 3.614</strong> rispetto alla V8 senza oche. Contro la 775 il primo seed resta sotto di 1.432; il secondo passa da −375 a +2.049. Fragole D6/D9/D12: 4/20/33 in entrambi. Variante locale verificata, nessuna nuova submission.</p><h2>Flussi economici osservati</h2>'+table(['Seed','Versione','Vendite latte','Vendite uova','Vendite lana','Tutte le vendite','Acquisti','Assunzioni'],flows)
body+='''<p>Il confronto include la reazione del mercato condiviso: i prezzi possono cambiare anche per la 775. Due seed esposti, un solo ruolo, non sono una validazione generale. Le differenze di cassa non vanno attribuite interamente ai ricavi delle uova.</p><h2>I 12 meloni erano rispettati</h2><p>Nella V8 e nel controllo nativo: 12 meloni seminati a D1, presenti fino all’inizio di D11, raccolti durante D11 per 72 unità. Il grafico a fine giornata mostra quindi 12 da D1 a D10 e zero a D11. Sul primo seed V8 la raccolta avviene fra H6 e H20 di D11. Le linee coincidono; il precedente grafico le sovrapponeva.</p><p>I conteggi e le raccolte della nuova variante sono verificabili in <a href="MELONS.json">MELONS.json</a>. Nei grafici seguenti le versioni hanno anche tratteggi differenti e il pannello meloni segnala la sovrapposizione.</p><h2>Controlli</h2><p>Geometria verificata casella per casella, entrambe le oche effettivamente collocate, 719 chiamate e zero errori per caso; hash delle fonti identici al protocollo congelato. Scorte finali e perdite colturali sono in <a href="VERIFICATION.json">VERIFICATION.json</a>.</p><p>La prima prova è esclusa: una costruzione conservata dalla sequenza originale aveva lasciato (6,3) come pascolo e impedito di collocare la seconda oca. La V2 corregge anche quel comando BUILD, senza cambiare la rotta. Le prove iniziali restano conservate in artifacts/operational772_goose2.</p>'''
for seed in [180911301,180911303]:body+=f'<h2>22 KPI — seed {seed}</h2><img style="width:100%;height:auto" src="KPI22_{seed}.png" alt="22 KPI comparati, seed {seed}">'
body+='<p><a href="KPI22.csv">Dati CSV</a> · <a href="PROTOCOL.json">Protocollo e hash</a> · <a href="RESULTS.json">Risultati JSON</a></p>'
(OUT/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>772 — due oche</title><style>body{font:17px/1.5 system-ui;max-width:1250px;margin:40px auto;padding:20px;color:#243746}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:8px;border-bottom:1px solid #ccd6df;text-align:left}th{background:#edf4f7}h1,h2{color:#006582}</style>'+body+'</html>',encoding='utf-8')
print(json.dumps({'rows':rows,'verification':verification},indent=2))
