"""Reproducible report for the actual operational772 adapter."""
from pathlib import Path
import sys,json,gzip,hashlib,csv,html,shutil
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
OUT=BASE/'reports/operational772_adaptation';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def profile(stage,name,seed):return read(BASE/f'artifacts/{stage}/{name}_E18_{seed}.kpi.json')['sides'][0]
def meta(stage,name,seed):return read(BASE/f'artifacts/{stage}/{name}_E18_{seed}.json')
def replay(stage,name,seed):return json.load(gzip.open(BASE/f'artifacts/{stage}/{name}_E18_{seed}.replay.json.gz','rt',encoding='utf-8'))
def structures(r):
 f=r['steps'][-1][0]['observation']['farms'][0]
 return [(x,y,t['kind'],t.get('animal')) for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict) and t['kind'] in ['PASTURE','COOP']]
def table(headers,rows):return '<table><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</table>'
series=[('772 pubblicata','calendar772_c1','Base772'),('772 operativa V8','operational772_v8','Op772'),('Comune nativo (770 + oche)','operational772_recorded_control','OpRecorded')]
profiles={label:profile(st,n,180911301) for label,st,n in series}
fig,axes=plt.subplots(11,2,figsize=(16,33));colors=['#667085','#006b8f','#d68019']
for ax,(key,label,unit) in zip(axes.flat,FIELDS):
 for (name,p),c in zip(profiles.items(),colors):ax.plot(range(1,31),[d[key] for d in p['kpi']],label=name,color=c,lw=1.7)
 ax.set_title('Caselle coltivate' if key=='crop_tiles' else label);ax.set_ylabel(unit);ax.set_xlabel('Giorno');ax.grid(alpha=.22);ax.set_xlim(1,30)
handles,labels=axes.flat[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',ncol=3);fig.tight_layout(rect=(0,0,1,.98));fig.savefig(OUT/'KPI22.png',dpi=110);plt.close(fig)
with (OUT/'KPI22.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['version','day']+[k for k,_,_ in FIELDS]);w.writeheader()
 for name,p in profiles.items():
  for d in p['kpi']:w.writerow(dict(version=name,day=d['day'],**{k:d[k] for k,_,_ in FIELDS}))
current=read(BASE/'reports/operational772_v8/RESULTS.json')[1]
a=replay('operational772_v8','Op772',180911301);native=replay('operational772_recorded_control','OpRecorded',180911301);base=replay('calendar772_c1','Base772',180911301)
prefix=[i for i in range(1,len(a['steps'])) if a['steps'][i-1][0]['observation']['day']<6]
comparison=[]
for label,p in profiles.items():
 l=p['ledger']['daily'];comparison.append([label,int(p['reward']),sum(sum(d['sales_cash'].values()) for d in l),sum(sum(d['purchase_cash'].values()) for d in l),sum(d['hire_cash'] for d in l),len(p['crop_starvation']),sum(d['verified_animal_losses'] for d in p['kpi'])])
checkrows=[]
for d in [1,6,9,12,15,20,25,30]:
 for label,p in profiles.items():
  z=p['kpi'][d-1];checkrows.append([d,label,z['money'],z['STRAWBERRY'],z['WHEAT'],z['COW'],z['SHEEP'],z['GOOSE'],z['people']])
fullcalendar=[]
for d in range(30):
 x=profiles['772 operativa V8']['kpi'][d];y=profiles['Comune nativo (770 + oche)']['kpi'][d]
 delta={k:x[k]-y[k] for k in ['MELON','WHEAT','STRAWBERRY','CARROT','TOMATO'] if x[k]!=y[k]}
 if delta:fullcalendar.append({'day':d+1,'crop_count_deltas_vs_native':delta})
checks={'geometry_and_species_equal_published772':structures(a)==structures(base),'calls':current['runtime']['calls'],'core_errors':current['runtime']['core_errors'],'full_action_prefix_D1_D6_equal':all(a['steps'][i][0]['action']==native['steps'][i][0]['action'] for i in prefix),'prefix_frames':len(prefix),'animal_losses':current['animal_losses'],'strawberries_D6_D9_D12':[current['checkpoints'][str(d)]['STRAWBERRY'] for d in [6,9,12]],'full_crop_calendar_exact':not fullcalendar,'crop_calendar_differences':fullcalendar,'terminal':current['terminal'],'cash_parity_errors':profiles['772 operativa V8']['ledger']['cash_parity_errors'],'structures':structures(a)}
(OUT/'VERIFICATION.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
assert checks['geometry_and_species_equal_published772'] and checks['calls']==719 and checks['core_errors']==0 and checks['full_action_prefix_D1_D6_equal']
attempts=[]
notes={1:'Non valido: ordine mercato vuoto, run interrotta.',2:'Prima esecuzione completa; rifornimenti e visite ricostruiti.',3:'Riserva fertilizzante e rientro finale.',4:'Precarico animali, dipendenze BUILD/PLACE.',5:'Ripristinate sequenze originali dei lavoratori non coinvolti.',6:'Aggiunto specialista Q2; corretti indici delle sequenze originali.',7:'Recupero servizi mancanti: zero fughe.',8:'Recupero posizione reale degli aiutanti durante pause/servizi.'}
for v in range(1,9):
 p=BASE/f'reports/operational772_v{v}/RESULTS.json';rows=read(p) if p.exists() else []
 z=next((r for r in rows if r['name']=='Op772'),None)
 attempts.append([f'V{v}',z['rewards'][0] if z and v!=1 else 'non valido',('/'.join(str(z['checkpoints'][str(d)]['STRAWBERRY']) for d in [6,9,12]) if z and v!=1 else '—'),z['animal_losses'] if z and v!=1 else '—',notes[v]])
validation=[]
for seed in [180911301,180911303]:
 for label,st,n in [('772 pubblicata','calendar772_c1' if seed==180911301 else 'operational772_validation','Base772'),('772 V8','operational772_v8' if seed==180911301 else 'operational772_validation','Op772')]:
  pp=BASE/f'artifacts/{st}/{n}_E18_{seed}.kpi.json'
  if pp.exists():
   p=profile(st,n,seed);m=meta(st,n,seed)
   validation.append({'seed':seed,'version':label,'cash':p['reward'],'opponent_cash':m['rewards'][1],'calls':m['runtime'][0]['calls'],'core_errors':m['runtime'][0]['core_errors'],'strawberries':[p['kpi'][d-1]['STRAWBERRY'] for d in [6,9,12]],'animals_final':{k:p['kpi'][-1][k] for k in ['COW','SHEEP','GOOSE']},'animal_losses':sum(d['verified_animal_losses'] for d in p['kpi']),'crop_losses':len(p['crop_starvation'])})
(OUT/'VALIDATION.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
for v in validation:
 if v['version']=='772 V8':
  assert v['calls']==719 and v['core_errors']==0 and v['animal_losses']==0 and v['strawberries']==[4,20,33]
  assert v['animals_final']==dict(COW=10,SHEEP=6,GOOSE=0)
second=replay('operational772_validation','Op772',180911303)
assert structures(second)==structures(base)
protocols=[BASE/'reports/operational772_v8/PROTOCOL.json',BASE/'reports/operational772_validation/PROTOCOL.json']
for protocol in protocols:
 for name,digest in read(protocol)['sources'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
sourcefiles=[BASE/'adapt_operational772_v2.py',BASE/'operational772_v8_policy.py',BASE/'run_operational772_v8.py',BASE/'validate_operational772_v8.py',BASE/'reports/operational772_v8/PLAN_772.json',BASE/'reports/operational772_v8/PLAN_NATIVE.json',BASE/'reports/operational772_v8/PROTOCOL.json',BASE/'reports/common_operational_program/PROGRAM.json',Path(__file__)]
freeze=OUT/'sources';freeze.mkdir(exist_ok=True)
for p in sourcefiles:shutil.copyfile(p,freeze/p.name)
(OUT/'MANIFEST.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sourcefiles},indent=2),encoding='utf-8')
body='''<h1>772: organizzazione operativa adattata e provata</h1>
<p>La traduzione ora è eseguibile sulla geometria della 772: visite, rifornimenti, collocamenti, servizi e consegne sono implementati. La candidata locale è <strong>operational772_v8_policy.py</strong>. Non è una nuova submission.</p>
<p>Nel caso di sviluppo 180911301, ruolo 0 contro la 775 congelata, la V8 chiude a <strong>82.342</strong>, contro <strong>80.178</strong> della 772 pubblicata (+2.164; +2,7%). Conserva la geometria e le specie esatte della 772, senza fughe. Le fragole sono 4/20/33 a D6/D9/D12. Il calendario completo non è ancora identico: a D12 risultano 20 grani invece di 21.</p>
<h2>Che cosa è stato adattato</h2>
<p>Le visite animali spostano la pecora da (1,4) a (4,6), sostituiscono l’oca in (4,1) con una mucca in (4,5), l’oca in (3,2) con una pecora, eliminano l’oca in (2,3) e trasformano la pecora in (6,3) in mucca. Le colture delle due caselle Q2 sono trasferite in (4,1) e (2,3). Coordinate zero-based (x,y).</p>
<p>Da D12 un aiutante aggiuntivo serve i due pascoli Q2; terminata la routine interviene sugli animali osservati senza cibo e, se raggiungibili, sulle colture in stress idrico. Le giornate dei lavoratori non coinvolti mantengono gli ordini originali. Quando la posizione reale differisce da quella attesa, le pause e le finestre di servizio permettono il recupero del percorso. Sono stati necessari 9 comandi di recupero nel caso di sviluppo.</p>
<p>I primi 144 turni (D1–D6) sono identici al controllo registrato. Il mercato conserva l’ordine degli ordini storici, ma adegua animali, rifornimenti e vendite alle scorte osservate. Non è stata ricostruita una politica privata di previsione dei prezzi.</p><h2>Confronto dei due seed</h2>'''
body+=table(['Seed','Versione','Cassa','Cassa 775 avversaria','Fragole D6/9/12','Fughe','Perdite colture'],[[v['seed'],v['version'],v['cash'],v['opponent_cash'],v['strawberries'],v['animal_losses'],v['crop_losses']] for v in validation])
body+='''<p><strong>La maggiore cassa non equivale a una vittoria.</strong> Sul seed 301 lo scarto contro la 775 passa da −16.352 a −4.968; sul seed 303 passa da +2.624 a −375. La V8 perde entrambi gli scontri, mentre la base ne vince uno. Non viene quindi promossa per una nuova pubblicazione.</p>
<p>Sono seed esposti di sviluppo, stesso ruolo 0. La strategia modifica anche il mercato condiviso: stessi seed e avversario non significano stessi prezzi. Queste prove non dimostrano un vantaggio generalizzato e non coprono il ruolo opposto. I seed riservati 180912401–407 restano inutilizzati. Su entrambi i casi V8: 719 chiamate, zero errori, zero fughe, geometria/specie finali identiche alla 772 pubblicata e fragole 4/20/33. Gli hash di policy, piani e controlli coincidono con i protocolli congelati.</p>
<h2>Controllo decisivo: la sequenza nativa funziona</h2>
<p>Gli ordini originali eseguiti direttamente nel nuovo ambiente, senza adattamento, chiudono a 95.229 contro 83.193 della 775. È la struttura nativa 770 con 8 mucche, 6 pecore e 3 oche. Le prime ricostruzioni dell’esecutore nativo producevano solo 74–76 mila: avevano alterato troppe visite. Da V5 il controllo nativo è quindi la sequenza originale esatta. Il divario con la V8 comprende struttura, specie, lavoro, ordini di mercato ed esecuzione: non attribuirlo soltanto agli animali.</p><h2>Contabilità sul seed 180911301</h2>'''
body+=table(['Versione','Cassa finale','Incassi vendite','Acquisti','Costo assunzioni','Perdite colture','Fughe'],comparison)
body+='<p>Acquisti e assunzioni sono flussi osservati; il ledger include anche terreni e altre variazioni. Il divario di circa 13 mila dal nativo non è spiegato dalle sole scorte residue.</p><h2>Checkpoint osservati</h2>'
body+=table(['D','Versione','Cassa','Fragole','Grano','Mucche','Pecore','Oche','Persone'],checkrows)
body+='''<h2>Limiti residui verificati</h2><p>La V8 sul primo seed perde due colture e nessun animale. A fine partita restano 3 unità di lana nel magazzino, 1 grano trasportato e semi inutilizzati (3 grano, 3 carota). La liquidazione non è quindi completa. Il passaggio dei tre checkpoint delle fragole non certifica l’intera successione colturale: tutte le differenze giornaliere sono in VERIFICATION.json.</p>
<p>Rettifica diagnostica: la mucca persa nelle V5/V6 era in (5,3), nel quadrante nord-est, a D26 H24; non era una delle due Q2. Nelle V7/V8 la perdita non si ripete sul caso di sviluppo.</p><h2>Registro completo dei tentativi</h2>'''
body+=table(['Versione','Cassa 772','Fragole D6/9/12','Fughe','Modifica'],attempts)
body+='''<p>Le revisioni sono sviluppo sullo stesso caso, non repliche statistiche. V1 è esclusa dai confronti economici. I log di visite incompiute V5 includono un errore di avanzamento degli indici delle azioni originali, corretto da V6: non usarli come conteggio affidabile delle visite fallite.</p><h2>22 KPI — seed 180911301</h2><p>MOVE/PASS sono comandi richiesti; WATER/FEED/CARE sono azioni riuscite. Cassa e quantità sono osservate nel replay. I tracciati riguardano tutta la fattoria.</p><img src="KPI22.png" alt="Traiettorie dei 22 KPI per 772 pubblicata, V8 e comune nativo" style="width:100%;height:auto"><p><a href="KPI22.csv">Dati KPI CSV</a> · <a href="VERIFICATION.json">Verifiche e differenze giornaliere</a> · <a href="VALIDATION.json">Risultati dei due seed</a> · <a href="MANIFEST.json">Hash sorgenti congelate</a> · <a href="sources/operational772_v8_policy.py">Policy implementata</a></p>'''
(OUT/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>772 — adattamento operativo</title><style>body{font:17px/1.5 system-ui;color:#243746;max-width:1250px;margin:40px auto;padding:0 24px}h1,h2{color:#005f78}table{border-collapse:collapse;width:100%;font-size:14px;margin:20px 0}th,td{padding:8px;border-bottom:1px solid #cfd8df;text-align:left}th{background:#e9f2f5}tr:nth-child(even){background:#f7f9fa}a{color:#006b8f}</style>'+body+'</html>',encoding='utf-8')
print(json.dumps({'checks':checks,'validation':validation},ensure_ascii=False,indent=2))
