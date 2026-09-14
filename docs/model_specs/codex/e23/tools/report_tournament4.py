"""Standings, paired deltas and 22 KPI/price panels for the frozen tournament."""
import argparse,csv,html,itertools,json,statistics as st,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,'C:/Users/pietr/.codex/worktrees/756c/kaggriculture-agent')
from docs.model_specs.codex.e22.tools.report_external_20260914 import METRICS,aggregate,page,rowdata,KEYS
OUT=ROOT/'docs/model_specs/codex/e23/reports/tournament4_v1'
LABELS={'E22G':'E22.1 · 8C6S3G','E22S':'E22.2 · 8C9S','E23G':'E23.1 · 9C5S3G','E23S':'E23.2 · 6C11S'}

def main():
 global OUT
 parser=argparse.ArgumentParser();parser.add_argument('--five',action='store_true');args=parser.parse_args()
 if args.five:
  OUT=OUT.parent/'tournament5_v1';LABELS['E23M']='E23.3 · 7C10S'
 expected=140 if args.five else 84
 name='cinque' if args.five else 'quattro'
 protocol=json.loads((OUT/'matches/PROTOCOL.json').read_text())
 rows=[json.loads(p.read_text()) for p in sorted((OUT/'matches').glob('E*.json'))]
 if not rows:return
 assert len({r['id'] for r in rows})==len(rows)
 assert {r['id'] for r in rows}<={r['id'] for r in protocol['schedule']}
 assert all(r['hashes']==protocol['hashes'] for r in rows)
 profiles={k:[] for k in LABELS};standings=[];views=[];pairings=[]
 for k in LABELS:
  games=[(r,r['players'].index(k)) for r in rows if k in r['players']]
  if not games:continue
  ps=[r['profiles'][s] for r,s in games];profiles[k]=ps
  margins=[r['rewards'][s]-r['rewards'][1-s] for r,s in games]
  wins=sum(m>0 for m in margins);draws=margins.count(0)
  standings.append(dict(key=k,label=LABELS[k],n=len(games),wins=wins,draws=draws,losses=sum(m<0 for m in margins),points=wins+draws*.5,cash_mean=st.mean(p['reward'] for p in ps),margin_mean=st.mean(margins),margin_min=min(margins),margin_max=max(margins),escapes=sum(len(p['ledger']['animal_escapes']) for p in ps),unfed=sum(len(p['unfed']) for p in ps),crop_stress=sum(len(p['crop_starvation']) for p in ps),mixes=dict(Counter(str(c['checks'][s]['mix']) for c,s in games)),sold_mean={prod:st.mean(p['totals']['sold_units'].get(prod,0) for p in ps) for prod in ['MILK','WOOL','EGG','WHEAT','STRAWBERRY']},sales_mean={prod:st.mean(p['totals']['sales_cash'].get(prod,0) for p in ps) for prod in ['MILK','WOOL','EGG','WHEAT','STRAWBERRY']}))
 standings.sort(key=lambda s:(s['points'],s['margin_mean']),reverse=True)
 for x,y in itertools.combinations(LABELS,2):
  games=[r for r in rows if set(r['players'])=={x,y}]
  if not games:continue
  sx=[r['profiles'][r['players'].index(x)] for r in games];sy=[r['profiles'][r['players'].index(y)] for r in games]
  margins=[a['reward']-b['reward'] for a,b in zip(sx,sy)]
  seedmeans=[st.mean(margins[i] for i,r in enumerate(games) if r['seed']==seed) for seed in sorted({r['seed'] for r in games})]
  products=sorted(set().union(*(p['totals']['sales_cash'] for p in sx+sy)))
  sales_delta={prod:st.mean(a['totals']['sales_cash'].get(prod,0)-b['totals']['sales_cash'].get(prod,0) for a,b in zip(sx,sy)) for prod in products}
  purchase_delta=st.mean(sum(a['totals']['purchase_cash'].values())-sum(b['totals']['purchase_cash'].values()) for a,b in zip(sx,sy))
  cost_deltas={key:st.mean(a['totals'][key]-b['totals'][key] for a,b in zip(sx,sy)) for key in ['hire_cash','land_cash','unit_cash_delta']}
  assert abs(sum(sales_delta.values())-purchase_delta-cost_deltas['hire_cash']-cost_deltas['land_cash']+cost_deltas['unit_cash_delta']-st.mean(margins))<.01
  pairings.append(dict(a=x,b=y,n=len(games),wins_a=sum(m>0 for m in margins),draws=margins.count(0),wins_b=sum(m<0 for m in margins),mean_margin_a=st.mean(margins),min_margin_a=min(margins),max_margin_a=max(margins),seed_mean_margins=seedmeans,sales_delta_a=sales_delta,purchase_delta_a=purchase_delta,**cost_deltas))
  views.append(dict(title=LABELS[x]+' / '+LABELS[y]+' · '+str(len(games))+' incontri',labels=[LABELS[x],LABELS[y]],note='Confronti diretti: stesso mercato. Mediana giornaliera e banda min–max sui semi e posti completati. I posti invertiti non sono campioni indipendenti.',series=[aggregate(sx),aggregate(sy)]))
 for r in rows:
  views.append(dict(title=r['id'],labels=[LABELS[k] for k in r['players']],note=f"Partita singola, seed {r['seed']}. Cassa finale: {r['rewards'][0]:,.0f} / {r['rewards'][1]:,.0f}.",series=[aggregate([p]) for p in r['profiles']]))
 verification=dict(matches=len(rows),expected=expected,profiles=2*len(rows),cash_parity_errors=sum(p['ledger']['cash_parity_errors'] for ps in profiles.values() for p in ps),reserved_seeds_used=False,all_hashes_match=True,reused_matches=sum('reused_from' in r for r in rows))
 diagnostic=None
 if (OUT/'DIAGNOSTICS.json').exists():
  diagnostic=json.loads((OUT/'DIAGNOSTICS.json').read_text())
  if diagnostic['matches']!=len(rows):diagnostic=None
 if diagnostic:
  verification['expected_mix_profiles']=sum(s['expected_mix_games'] for s in diagnostic['summary'].values())
  verification['q2_wheat_harvest_profiles']=sum(s['q2_wheat_harvest_games'] for s in diagnostic['summary'].values())
  verification['animal_escapes']=sum(s['escapes'] for s in diagnostic['summary'].values())
 assert verification['cash_parity_errors']==0
 seed_table=[]
 for seed in sorted({r['seed'] for r in rows}):
  scores={k:0 for k in LABELS};counts={k:0 for k in LABELS}
  for r in rows:
   if r['seed']!=seed:continue
   for s,k in enumerate(r['players']):scores[k]+=1 if r['rewards'][s]>r['rewards'][1-s] else .5 if r['rewards'][s]==r['rewards'][1-s] else 0;counts[k]+=1
  seed_table.append(dict(seed=seed,points=scores,matches=counts))
 summary=dict(verification=verification,standings=standings,pairings=pairings,seed_scores=seed_table)
 if len(rows)==expected:
  assert all(s['n']==(56 if args.five else 42) for s in standings)
  assert all(p['n']==14 for p in pairings)
  verification['complete_balanced_schedule']=True
 (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
 md='# E23 / E22 — torneo a '+name+'\n\n'
 md+=f"**{len(rows)}/{expected} incontri completati.** Sette semi esposti, tutti gli abbinamenti, posti invertiti. Un punto per vittoria, mezzo per pareggio.\n\n"
 if len(rows)==expected:md+=f"Prima in classifica: **{standings[0]['label']}**, {standings[0]['wins']} vittorie su {standings[0]['n']}. Ordine per punti e, a parità, margine medio.\n\n"
 interpretation=''
 if args.five and len(rows)==expected:
  middle=next(p for p in pairings if (p['a'],p['b'])==('E23S','E23M'));parent=next(p for p in pairings if (p['a'],p['b'])==('E22S','E23M'))
  interpretation=f"La 7C10S batte la 6C11S {middle['wins_b']}–{middle['wins_a']} negli scontri diretti (margine medio {-middle['mean_margin_a']:+.2f}), ma perde {parent['wins_b']}–{parent['wins_a']} contro E22.2 8C9S (margine medio {-parent['mean_margin_a']:+.2f}). È un'intermedia utile nel confronto, ma questo torneo non giustifica la sua promozione rispetto al genitore. Nessuna E23 è stata pubblicata."
  md+=interpretation+'\n\n'
 if len(rows)<expected:md+='Classifica provvisoria: numero di incontri ancora diverso fra le versioni.\n\n'
 md+='| Versione | Incontri | Vittorie | Pareggi | Sconfitte | Cassa media | Margine medio |\n|---|---:|---:|---:|---:|---:|---:|\n'
 for s in standings:md+=f"| {s['label']} | {s['n']} | {s['wins']} | {s['draws']} | {s['losses']} | {s['cash_mean']:.1f} | {s['margin_mean']:+.1f} |\n"
 md+='\n## Scontri diretti\n\n| A | B | Vittorie A / pari / B | Margine medio A |\n|---|---|---:|---:|\n'
 for p in pairings:md+=f"| {LABELS[p['a']]} | {LABELS[p['b']]} | {p['wins_a']} / {p['draws']} / {p['wins_b']} | {p['mean_margin_a']:+.1f} |\n"
 md+='\n## Versioni e limiti\n\nE22.1 Q2 Grano 56228842 ed E22.2 fix Q2 Grano 56231638 sono i controlli byte-identici. E23.1: 9C5S3G, pecora → mucca in (6,2). E23.2: 6C11S, mucche → pecore in (6,4) e (5,2). '
 if args.five:md+='E23.3: 7C10S, solo (6,4) diventa pecora. '
 md+='Tutte le E23 mantengono percorsi e colture E22, incluso Q2 Grano, con servizi/vendite adattati e correzioni esecutive condivise da E22.2. Il confronto misura questo pacchetto; non isola causalmente la sola specie. La 7C10S è una specifica disposizione intermedia, non tutte le disposizioni possibili di sette mucche.\n\nI semi 180911301–180911307 erano già esposti; 180912401–180912407 non sono utilizzati. Gli incontri a posti invertiti condividono il seme e non sono campioni indipendenti. Nessuna stima del rating Kaggle e nessuna pubblicazione.\n\n'
 md+='[Report interattivo: 22 KPI + volumi/prezzi](REPORT.html) · [Esiti CSV](ALL_RESULTS.csv) · [Diagnostica](DIAGNOSTICS.json) · [Versioni e hash](BUNDLES.json) · [Protocollo](matches/PROTOCOL.json) · [Ambiente di esecuzione](RUNTIME.json).\n'
 (OUT/'REPORT.md').write_text(md,encoding='utf-8')
 def table(headers,rs):return '<div class="tablewrap"><table><thead><tr>'+''.join('<th>'+html.escape(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(c))+'</td>' for c in row)+'</tr>' for row in rs)+'</tbody></table></div>'
 body=f'<p>{len(rows)}/{expected} incontri completati · 7 semi esposti × {10 if args.five else 6} abbinamenti × 2 posti. Un punto per vittoria, mezzo per pareggio.</p>'
 if len(rows)==expected:body+=f"<p class=\"note\"><b>Prima in classifica: {html.escape(standings[0]['label'])}</b>, {standings[0]['wins']} vittorie su {standings[0]['n']}. Ordine per punti e, a parità, margine medio. <a href=\"#view\">Vai ai grafici</a>.</p>"
 if interpretation:body+='<p>'+html.escape(interpretation)+'</p><p><a href="VERIFICATION.json">Verifica finale</a> · <a href="REPLAY_MANIFEST.json">Replay e hash</a> · <a href="REPORT.md">Sintesi testuale</a>.</p>'
 if len(rows)<expected:body+='<p class="note"><b>Classifica provvisoria:</b> i partecipanti hanno disputato numeri diversi di incontri. Attendere il calendario completo per confrontare i punti totali.</p>'
 body+=table(['Versione','Incontri','V–P–S','Punti','Cassa media','Margine medio','Fughe'],[[s['label'],s['n'],f"{s['wins']}–{s['draws']}–{s['losses']}",s['points'],f"{s['cash_mean']:,.1f}",f"{s['margin_mean']:+,.1f}",s['escapes']] for s in standings])
 body+='<h2>Scontri diretti</h2>'+table(['A','B','V A / pari / V B','Margine medio A','Min / max'],[[LABELS[p['a']],LABELS[p['b']],f"{p['wins_a']} / {p['draws']} / {p['wins_b']}",f"{p['mean_margin_a']:+,.1f}",f"{p['min_margin_a']:+,.0f} / {p['max_margin_a']:+,.0f}"] for p in pairings])
 body+='<h2>Punti per seme</h2>'+table(['Seme']+list(LABELS.values()),[[r['seed']]+[f"{r['points'][k]:g} / {r['matches'][k]}" for k in LABELS] for r in seed_table])
 body+='<h2>E23 contro il proprio genitore: origine del delta</h2><p>Monete medie E23 meno E22 negli scontri diretti. Gli incrementi di costo riducono il guadagno.</p>'+table(['Evoluzione','Δ ricavi latte','Δ ricavi lana','Δ altri ricavi','Δ acquisti','Δ lavoro','Δ terreni','Δ cassa finale'],[[LABELS[p['b']],f"{-p['sales_delta_a'].get('MILK',0):+,.1f}",f"{-p['sales_delta_a'].get('WOOL',0):+,.1f}",f"{-sum(v for k,v in p['sales_delta_a'].items() if k not in ('MILK','WOOL')):+,.1f}",f"{-p['purchase_delta_a']:+,.1f}",f"{-p['hire_cash']:+,.1f}",f"{-p['land_cash']:+,.1f}",f"{-p['mean_margin_a']:+,.1f}"] for p in pairings if (p['a'],p['b']) in [('E22G','E23G'),('E22S','E23S'),('E22S','E23M')]])
 body+='<h2>Produzione venduta e ricavi medi</h2>'+table(['Versione','Latte unità / ricavi','Lana unità / ricavi','Uova unità / ricavi','Fragole unità / ricavi'],[[s['label']]+[f"{s['sold_mean'][p]:.1f} / {s['sales_mean'][p]:,.1f}" for p in ['MILK','WOOL','EGG','STRAWBERRY']] for s in standings])
 if diagnostic:
  body+='<h2>Verifica dell’esecuzione</h2>'+table(['Versione','Mix corretto','Fughe','Stress colture','Grano Q2 raccolto','Latte non raccolto finale, media'],[[LABELS[k],f"{v['expected_mix_games']}/{v['n']}",v['escapes'],v['crop_stress'],f"{v['q2_wheat_harvest_games']}/{v['n']}",v['mean_terminal_tile_yield']['MILK']] for k,v in diagnostic['summary'].items()])
  body+='<p class="meta">Stress colture = transizioni osservate dopo stress. I prodotti rimasti sulle caselle sono distinti dalle scorte raccolte e dalle vendite. <a href="DIAGNOSTICS.json">Diagnostica di ogni lato</a>.</p>'
 body+='<p class="note">Le E23 mantengono percorsi e colture E22, incluso il grano Q2. E23.1 cambia la pecora (6,2) in mucca; E23.2 cambia le mucche (6,4) e (5,2) in pecore. Sono adattati servizi e vendite; entrambe usano le correzioni esecutive di E22.2. Il risultato riguarda questo pacchetto, non il solo cambio specie. I sette semi erano già esposti; non è una stima del rating Kaggle.</p>'
 body+='<p>Controlli E22 congelati: submission 56228842 e 56231638. <a href="BUNDLES.json">File e SHA256</a> · <a href="matches/PROTOCOL.json">Protocollo</a> · <a href="SUMMARY.json">Risultati e diagnostica</a> · <a href="ALL_RESULTS.csv">Esiti CSV</a> · <a href="DAILY_22_KPI_PRICES.csv">KPI giornalieri CSV</a>.</p><p class="meta">40 pannelli: 22 KPI più volumi e prezzi realizzati per nove prodotti. Checkpoint H24 prima dell’ultimo batch nei giorni 1–29; D30 terminale. Flussi su tutti i batch. Prezzi senza vendite = n/d. Passaggio, clic e frecce sui grafici mostrano i valori.</p>'
 if args.five:body+='<p><b>E23.3 7C10S:</b> solo (6,4) diventa pecora, mentre (5,2) resta mucca. Completa la sequenza 8C9S → 7C10S → 6C11S. Riutilizzati i risultati già completi del torneo a quattro, con gli stessi hash; gli incontri aggiuntivi seguono tutti i dieci abbinamenti per seme.</p>'
 (OUT/'REPORT.html').write_text(page('E23 / E22 · torneo a '+name,body,dict(metrics=METRICS,views=views)),encoding='utf-8')
 with (OUT/'ALL_RESULTS.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(['id','seed','seat0','seat1','cash0','cash1','margin0']);w.writerows([r['id'],r['seed'],*r['players'],*r['rewards'],r['rewards'][0]-r['rewards'][1]] for r in rows)
 with (OUT/'DAILY_22_KPI_PRICES.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(['match','policy','seat','day']+KEYS)
  for r in rows:
   for seat,p in enumerate(r['profiles']):
    for day,row in enumerate(rowdata(p),1):w.writerow([r['id'],r['players'][seat],seat,day]+[row[k] for k in KEYS])
 print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
