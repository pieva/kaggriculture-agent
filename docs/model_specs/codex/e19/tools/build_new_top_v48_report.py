"""Build phase-aware census, spatial templates and complete KPI reports."""
import sys,json,hashlib,re
from pathlib import Path
from collections import Counter
from statistics import mean
from html import escape
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate,FIELDS,fmt
B=ROOT/'docs/model_specs/codex/e19';O=B/'reports/new_top_v48_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def table(head,rows):
 return '<div class="tablewrap"><table><tr>'+''.join('<th>'+escape(str(x))+'</th>' for x in head)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</table></div>'
def topo(q):return '–'.join(map(str,q[:3]))+(' / Q3='+str(q[3]) if q[3] else '')
def main():
 c=read(O/'census.json');ps=read(O/'profiles.json');cohorts=read(O/'cohorts.json');phase=read(O/'phase_summary.json')
 paths=sorted((B/'artifacts/derived/portfolio_succession_20260907').glob('daily_routes_v48_*.json'));v48=[read(p)['sides']['candidate'] for p in paths];assert len(v48)==6
 by={n:[p for p in ps if p['name']==n] for n in ['Subin An','Matthew Huang','Suliman Tadros']}
 strict=[p for p in by['Subin An'] if list(p['daily'][-1]['pasture_topology'].values())==[7,7,0,0]]
 assert len(strict)==4 and all(all(list(d['pasture_topology'].values())==[7,7,0,0] for d in p['daily'][14:]) for p in strict)
 groups=[('TOP770_003','Top770-003 · 4 replay 770',strict),('TOP770_003_TUTTI','Top770-003 · tutti i 5 replay',by['Subin An']),('MATTHEW_ESPLORATIVO','Matthew · corpus misto 5 replay',by['Matthew Huang']),('TOP1070_ESPLORATIVO','Suliman · 10–7–0 · 3 replay',by['Suliman Tadros'])]
 intro='''<h2>Conclusione e limiti</h2><p><strong>Il piano biologico resta il principio da conservare. La prima alternativa da sperimentare è 10–7–0, con Q2 dedicato alle colture.</strong> La raccomandazione riguarda una prova futura, non una superiorità dimostrata: V48 non è stata eseguita in 10–7–0 e le casse di corpus diversi non sono confronti competitivi appaiati.</p>
<p>Lo screening comprende 12 autori nuovi rispetto al registro precedente. Un solo autore soddisfa il criterio storico 4/5 finali 770: <strong>Top770-003, Subin An</strong>. Quattro replay sono 770 stabili D15–D30; il quinto è 10–7–0 e rimane nel corpus completo. Matthew resta esplorativo: 3/5 finali 770. Non sono stati riciclati Jesse Bullard o Marlubie come nuovi riferimenti.</p>
<p>Il criterio D15–D25 è un’analisi aggiunta su richiesta del proprietario dopo lo screening; non viene presentato come criterio preregistrato. Topologia prevalente = moda dei checkpoint D15–D25; stabilità = durata osservata, non prova di una policy fissa. Tutti gli autori aperti sono ora esposti e non vanno riutilizzati come holdout per release successive.</p>
<h2>Avvio comune, poi poche diramazioni</h2><p>Nei 13 replay approfonditi di Subin, Matthew e Suliman, Q2 viene sbloccato e utilizzato entro il checkpoint D12. La 770 lascia Q2 senza pascoli ma lo coltiva: zero pascoli non significa quadrante inutilizzato. Le strutture e i cicli vanno letti separatamente.</p>
<p>Suliman raggiunge 10–7–0 a D11 e lo mantiene fino a D30 nei tre casi. Subin ha quattro piani 770 e un piano 10–7–0, già distinti a D15 e invariati fino a D30. Matthew ha tre 770; negli altri due casi passa da 11–7–0 a D15 a 10–7–0 da D16, poi aggiunge un pascolo Q2 a D29. Questo è compatibile con un piano a fasi; non prova una ripianificazione continua né identifica la regola che sceglie la diramazione.</p>
<p>Non tutta la variabilità dei leader è virtuosa: nel replay SpaTaro 106815633 si verificano tre fughe animali a D20–D21, seguite dalla riduzione dei pascoli 8–6–0 → 8–3–0. Le cause economiche delle altre diramazioni (prezzi, avversario, capacità) restano ipotesi: non abbiamo il codice della policy né un controfattuale.</p>'''
 overview=intro+'<h2>Registro dello screening: nessun filtro sulla cassa</h2>'
 screen=[]
 for n,sub,eps in cohorts:
  xs=[x for x in c if x['name']==n];cnt=sum(x['topology_D30']==[7,7,0,0] for x in xs)
  modes=Counter(topo(x['mode_D15_D25']) for x in xs)
  screen.append([escape(n),sub,f'{cnt}/{len(xs)}','; '.join(f'{k}: {v}' for k,v in modes.items()),'Top770-003' if n=='Subin An' else 'Esplorativo / non qualificato'])
 overview+=table(['Autore','Submission','Finali 770','Assetto prevalente D15–D25','Esito'],screen)
 overview+='<h2>Fasi produttive: medie per giorno e partita</h2><p>Subin e Matthew includono tutti i cinque replay, senza eliminare le topologie non 770. Persone include il farmer; gli animali comprendono anche le oche. Le azioni non sono normalizzate per il diverso carico biologico.</p>'
 keys=['crop_tiles','people','occupied_livestock_tiles','PASS','MOVE','WATER','FEED','CARE','weed_tiles','verified_animal_losses','hire_cash']
 overview+=table(['Periodo','Misura','V48 locale n6','Subin n5','Matthew n5','Suliman n3'],[[period,k,*[fmt(phase[n][period][k]) for n in phase]] for period in ['D1-11','D15-25','D26-30'] for k in keys])
 overview+='''<h2>Che cosa cambia rispetto a V48</h2><p>A D15–D25 Subin gestisce più animali e leggermente più colture con meno persone: MOVE 111 contro 150,2; PASS 6,9 contro 28,8; WATER 44,3 contro 35,1; CARE 16,8 contro 12. Le infestanti osservate sono zero contro 2,15 medie. Non basta ridurre i PASS: occorre ottenere più servizi utili per percorso e assegnare persone in funzione del lavoro già pianificato.</p><p>V48 spende 376 al giorno in assunzioni contro 195,4 del corpus Subin. Il dato sostiene la priorità su pianificazione e percorsi, non una riduzione cieca della manodopera. Suliman costa 253,4 e ha MOVE 117,7, ma presenta fughe animali anche prima della chiusura: non va imitato senza controllo del servizio.</p>
<h2>Alternativa proposta: 10–7–0, a parità di disciplina biologica</h2><p>Passare da 14 a 17 pascoli aggiunge tre siti in Q0, mantiene Q2 agricolo e richiede una modifica circoscritta del layout. È osservato come assetto produttivo stabile in tre replay Suliman, uno Subin e due Matthew dopo D16. La ripetizione tra autori è un indizio, non prova di indipendenza delle strategie o di superiorità.</p><p>Se tutti i nuovi pascoli sono popolati, occorre pianificare fino a tre FEED e tre CARE aggiuntivi al giorno, oltre a raccolte, rifornimenti e percorrenze. Sono tre caselle agricole in meno rispetto a 770; il beneficio va confrontato con i cicli colturali rinunciati. Il mix animale non va copiato: deve rispettare maturazione, alimentazione e produzioni residue.</p><p>662 rimane un controllo futuro a 14 pascoli: sposta due servizi in Q2 e modifica la logistica, ma nel campione non emerge come template stabile ripetuto. 870 compare in carbonapi (2/3 assetti prevalenti) ed è una prova intermedia possibile, con evidenza più debole. Gli assetti molto variabili dei primi leader non forniscono ancora un target fisso trasferibile.</p>
<p><strong>Prima della prova:</strong> risolvere la capacità dei percorsi su 770; poi confrontare 770 e 10–7–0 con lo stesso core, calendario biologico, budget e semi nuovi, includendo avversari diversi. Prenotare l’intero ciclo prima di popolare nuovi pascoli. Misurare ricavi e costi, produzione persa, servizi, carichi e stabilità. Tenere la chiusura separata e non usare questi replay già analizzati come nuova validazione.</p>'''
 overview+='<h2>Checkpoint per ogni replay approfondito</h2>'+table(['Autore','Replay','Q2 sblocco / uso','D11','D15','Prevalente D15–25 (giorni/11)','D25','D30'],[[escape(x['name']),f'<a href="https://www.kaggle.com/competitions/kaggriculture/leaderboard?submissionId={x["submission"]}&amp;episodeId={x["episode"]}">{x["episode"]}</a>',f'{x["q2_open"]} / {x["q2_used"]}',topo(x['topology_D11']),topo(x['topology_D15']),topo(x['mode_D15_D25'])+f' ({x["mode_days"]}/11)',topo(x['topology_D25']),topo(x['topology_D30'])] for x in c if x['name'] in by])
 overview+='<h2>Mappe dei template a D15</h2><p>Primo replay in ordine di corpus per ogni autore/topologia D15. Mappe osservate, non target prescritti. P = pascolo; W = grano; S = fragole; C = carote; T = pomodori; M = meloni; punto = altro. Coordinate da 0 a 9, Q0 in alto a sinistra. Vedi spatial in census.json per colture, data di semina, specie e data di collocamento.</p>'
 seen=set()
 for x in c:
  if x['name'] not in by:continue
  k=(x['name'],tuple(x['topology_D15']))
  if k in seen:continue
  seen.add(k);e=x['spatial'][14];grid=[['·']*10 for _ in range(10)]
  for a,b in e['pastures']:grid[b][a]='P'
  for a,b,crop,day in e['plants']:grid[b][a]={'WHEAT':'W','STRAWBERRY':'S','CARROT':'C','TOMATO':'T','MELON':'M'}[crop]
  overview+=f'<h3>{escape(x["name"])} · {x["episode"]} · {topo(x["topology_D15"])}</h3><pre>'+ '\n'.join(' '.join(row[:5])+' │ '+' '.join(row[5:]) for row in grid)+'</pre>'
 overview+='<h2>Report completi: 22 KPI D1–D30</h2><ul>'+''.join(f'<li><a href="V48_VS_{key}_D01_D30_COMPLETE_KPI.html">V48 vs {escape(label)}</a></li>' for key,label,g in groups)+'</ul><p><a href="census.json">Censimento completo</a> · <a href="profiles.json">Profili e ledger</a> · <a href="manifest.json">Provenienza e hash</a></p>'
 template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8').replace('770 assistita V1','V48 locale').replace("candidate:'770 assistita'","candidate:'V48 locale'").replace('7 settembre 2026','8 settembre 2026')
 template=re.sub(r'<p class="note">.*?</p>','<p class="note">V48 congelata. Confronto descrittivo tra corpus diversi, non test competitivo appaiato. <a href="REPORT_NUOVI_TOP_V48_IT.html">Analisi delle topologie e selezione</a></p>',template,count=1)
 for key,label,g in groups:
  payload=dict(topLabel=label,metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate(v48),top770=aggregate(g)))
  for ser in payload['series'].values():
   for values in ser.values():assert len(values)==30 and all(lo<=m<=hi for m,lo,hi in values)
  filename='V48_VS_'+key+'_D01_D30_COMPLETE_KPI'
  econ='<p>Corpus completo conservato. Subin: 4/5 finali 770; il report filtrato è condizionato alla topologia e va letto insieme a quello con tutti i cinque replay. Matthew e Suliman sono esplorativi.</p>'+table(['Misura','V48',label],[['Cassa media',fmt(mean(p['terminal']['cash'] for p in v48)),fmt(mean(p['terminal']['cash'] for p in g))]])
  vals=dict(TITLE='V48 vs '+label+' · KPI D1–D30',COHORTS=f'6 casi locali V48 · {len(g)} replay esterni',TOP=label,ECONOMY=econ,PROVENANCE='Nuovo corpus del 8 settembre; esclusi autori precedentemente esposti. Episodi: '+', '.join(str(p['episode']) for p in g)+'. Una volta analizzato, corpus esposto per il solo ciclo corrente.',DATAFILE=filename+'.json',DATA=json.dumps(payload,ensure_ascii=False).replace('</',r'<\/'),OTHER='REPORT_NUOVI_TOP_V48_IT.html')
  result=template
  for k,v in vals.items():result=result.replace('__'+k+'__',v)
  assert not re.search(r'__[A-Z]+__',result)
  (O/(filename+'.html')).write_text(result,encoding='utf-8');(O/(filename+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
 page='<!doctype html><html lang="it"><meta charset="utf-8"><title>Nuovi Top e V48: pianificazione e topologie</title><style>body{background:#191c21;color:#e1e6ee;font:16px/1.6 system-ui;margin:30px auto;max-width:1280px;padding:20px}a,h1,h2{color:#83cafa}table{border-collapse:collapse;font-size:13px}td,th{border:1px solid #48515b;padding:7px;text-align:left}.tablewrap{overflow:auto}pre{font-size:18px}strong{color:#f4a16d}</style><h1>Nuovi Top e V48: pianificazione biologica e topologie</h1><p>8 settembre 2026 · Nessuna modifica della policy · Report descrittivo</p>'+overview+'</html>'
 for text in [page,result]:assert not any(c in text for c in ['\ufffd','\u00c3','\u00c2'])
 (O/'REPORT_NUOVI_TOP_V48_IT.html').write_text(page,encoding='utf-8')
 sources=paths+[B/'artifacts/derived/new_top_screen_20260908'/f'{ep}.json' for ep in sorted({x['episode'] for x in c})]+[Path(__file__),Path(__file__).with_name('analyze_new_top_v48.py'),Path(__file__).with_name('complete_kpi_template.html'),O/'cohorts.json']
 (O/'manifest.json').write_text(json.dumps(dict(authors=12,unique_episodes=len({x['episode'] for x in c}),qualified='Top770-003 / Subin An',sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.name!='manifest.json'}),indent=2),encoding='utf-8')
 print(O/'REPORT_NUOVI_TOP_V48_IT.html')
if __name__=='__main__':main()
