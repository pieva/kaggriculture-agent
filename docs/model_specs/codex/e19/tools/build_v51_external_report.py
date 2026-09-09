"""Reproducible V51 external KPI report; no strategy execution or modification."""
import csv
import hashlib
import html
import json
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[5]
B=ROOT/'docs/model_specs/codex/e19'
O=B/'reports/v51_external_20260909'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
s=read(O/'summary.json');cohort=read(O/'cohort.json')
ps=[read(O/f"profile_{r['episode']}.json") for r in cohort['games']]
old=read(B/'reports/v48_external_pass_update_20260908/summary.json')['all38']
v=s['all42'];opp=s['opponents42'];total=v['phases']['D1-D30']
fmt=lambda x:f'{x:,.2f}'.replace(',','_').replace('.',',').replace('_','.')
esc=html.escape
def table(headers,rows):
    return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+esc(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def chart(key,title,percent=False):
    groups=[(v,'V51C','#4fe1c0'),(opp,'Avversari V51C','#f6a36c')]
    if key in old['daily'][0]:groups.append((old,'V48 storico','#72b1de'))
    scale=100 if percent else 1
    high=max(d[key]*scale for g,_,_ in groups for d in g['daily'])*1.12 or 1
    svg='<svg viewBox="0 0 720 255" role="img" aria-label="'+esc(title)+'">'
    for i in range(5):
        y=215-i*47
        svg+=f'<path d="M65 {y}H700" stroke="#394452"/><text x="3" y="{y+4}">{high*i/4:.0f}</text>'
    for day in [1,5,10,15,20,25,30]:
        x=65+(day-1)*635/29;svg+=f'<text x="{x-8}" y="240">D{day}</text>'
    for g,label,color in groups:
        points=' '.join(f"{65+i*635/29:.1f},{215-d[key]*scale/high*188:.1f}" for i,d in enumerate(g['daily']))
        svg+=f'<polyline points="{points}" stroke="{color}" stroke-width="2.5" fill="none"/>'
        for i,d in enumerate(g['daily']):
            svg+=f'<circle cx="{65+i*635/29}" cy="{215-d[key]*scale/high*188}" r="3" fill="{color}"><title>{label}, D{i+1}: {fmt(d[key]*scale)}</title></circle>'
    return '<section><h2>'+title+'</h2>'+svg+'</svg></section>'

bio_keys=['missed_feed','missed_useful_care','missed_critical_water','decay_lost_units','productive_water_loss_units']
bio={k:sum(d[k] for p in ps for d in p['biological_obligations']) for k in bio_keys}
escapes=sum(len(p['candidate_ledger']['animal_escapes']) for p in ps)
hours=[sum(d['pass_hours'][h] for p in ps for d in p['candidate']) for h in range(24)]
discrepancies=[dict(episode=p['episode'],**d) for p in ps for d in p['candidate_ledger'].get('cash_discrepancies',[])]
residuals={side:sum(p[side+'_ledger'].get('net_cash_residual',0) for p in ps) for side in ['candidate','opponent']}
d29=v['daily'][28];o29=old['daily'][28]
peaks=sorted([(d['explicit_pass'],p['episode'],d['day'],p['opponent_name'],d['slots'],d['move']) for p in ps for d in p['candidate']],reverse=True)[:12]
overview=table(['Coorte','Partite','V / S / P','Cassa finale media','PASS/giorno','Quota PASS','MOVE/giorno'],[
    [label,g['n'],f"{g['wins']} / {g['losses']} / {g.get('draws',g['n']-g['wins']-g['losses'])}",fmt(g['cash_mean']),fmt(g['phases']['D1-D30']['explicit_pass']),fmt(100*g['phases']['D1-D30']['pass_share'])+'%',fmt(g['phases']['D1-D30']['move'])]
    for label,g in [('V51C',v),('Avversari V51C',opp),('V48 storico (8 settembre)',old)]])
body=f'''<h1>V51C esterna · report KPI dei replay</h1>
<p>Submission <a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56124996">56124996</a> · 9 settembre 2026 · stato Complete · rating osservato <strong>942,1</strong>.</p>
<p><strong>{v['wins']} vittorie e {v['losses']} sconfitte su {v['n']} partite</strong> ({fmt(100*v['wins']/v['n'])}% vittorie). Cassa finale media {fmt(v['cash_mean'])}; differenza media rispetto all'avversario {fmt(v['cash_mean']-opp['cash_mean'])}.</p>
<p>Coorte congelata: tutte le 42 partite contro altri giocatori presenti nella cronologia iniziale, senza filtro sull'esito; ultimo match alle 21:09:33 italiane. Il self-play 107150551 è escluso. Eventuali nuovi match non sono inclusi.</p>
{overview}<p>V48 è una coorte storica di 38 partite, con altri avversari e condizioni: il confronto è descrittivo e non misura l'effetto causale della versione. Il rating V48 nella stessa pagina era 950,3; entrambi i rating sono snapshot mobili.</p>
<h2>PASS e chiusura D29</h2>
<p>V51C registra <strong>{fmt(total['explicit_pass'])} PASS/giorno</strong>, il {fmt(100*total['pass_share'])}% degli slot disponibili, e {fmt(total['move'])} MOVE/giorno. Il {fmt(100*sum(hours[18:])/sum(hours))}% dei PASS cade nelle ore H19–H24.</p>
<p>A D29: <strong>{fmt(d29['explicit_pass'])} PASS</strong> medi, intervallo {d29['pass_min']}–{d29['pass_max']}, contro {fmt(o29['explicit_pass'])} nella coorte V48. MOVE {fmt(d29['move'])} contro {fmt(o29['move'])}; personale al checkpoint {fmt(d29['people_h24'])} contro {fmt(o29['people_h24'])}. Quota PASS {fmt(100*d29['pass_share'])}% contro {fmt(100*o29['pass_share'])}%. Questo controllo esterno non è un confronto appaiato con V49F.</p>
<p>{fmt(total['pass_current_tile_service'])} PASS/giorno coincidono con un servizio potenzialmente disponibile sulla casella senza un altro comando attivo nello stesso punto; {fmt(total['pass_critical_water'])} coincidono con acqua critica ancora pendente e {fmt(total['pass_unfed_animals'])} con animali ancora da alimentare. Sono osservazioni prima del batch, non conteggi di PASS sicuramente evitabili. Utilità, prenotazioni e scadenze richiedono diagnosi separata.</p>
<h2>Integrità e obblighi biologici</h2>
<p>Tutti i 42 replay hanno 720 stati e stato finale DONE per entrambi i giocatori. Ricostruzione della cassa verificata su tutte le 719 transizioni per partita, per entrambi i lati, con {len(discrepancies)} discrepanze conservate. Residuo fra saldo finale registrato e flussi ricostruiti: V51C {fmt(residuals['candidate'])}, avversari {fmt(residuals['opponent'])}. I risultati e la cassa dei grafici provengono direttamente dal replay. Engine locale verificato tramite hash del manifest congelato.</p>'''
body+=table(['Episodio','Transizione','Seat','Cassa registrata','Cassa ricostruita'],[[d['episode'],d['index'],d['seat'],d['expected'],d['reconstructed']] for d in discrepancies])
body+=table(['KPI V51C','Totale nelle 42 partite','Media/partita'],[[label,bio[k],fmt(bio[k]/len(ps))] for k,label in zip(bio_keys,['FEED mancati a fine giornata','CARE utili mancati a fine giornata','WATER critici produttivi mancati','Unità perse per decadimento','Unità esposte a carenza idrica critica'])]+[['Fughe di animali',escapes,fmt(escapes/len(ps))]])
body+='''<p>Gli obblighi sono verificati dopo i comandi dell'ultima ora di D1–D29; D30 non ha un successivo aggiornamento giornaliero. Decadimento misurato dopo ogni batch. Il CARE utile usa la funzione biologica del progetto. Le unità esposte a carenza idrica non sono una perdita monetaria stimata; il controllo non certifica l'ottimalità economica delle azioni.</p>'''
bio_daily=[dict(day=d+1,**{k:sum(p['biological_obligations'][d][k] for p in ps) for k in bio_keys}) for d in range(30)]
body+="<p><strong>D29: nessun FEED, CARE utile o WATER critico mancato nei 42 replay.</strong> Restano deficit negli altri giorni: non si puo dichiarare copertura biologica completa. I picchi idrici sono D16 e D22; D28 concentra 134 FEED mancati. Alcuni deficit iniziali riguardano il periodo di espansione. Questi conteggi misurano obblighi secondo il modello del progetto, non dimostrano da soli perdite economiche equivalenti.</p>"
body+='<h2>Deficit biologici per giorno: totali di coorte</h2>'+table(['Giorno','FEED mancati','CARE utili mancati','WATER critici mancati','Unita decadute','Unita esposte ad acqua critica'],[[d['day'],*[d[k] for k in bio_keys]] for d in bio_daily if any(d[k] for k in bio_keys)])
with (O/'biological_daily.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['day',*bio_keys]);w.writeheader();w.writerows(bio_daily)
body+='<h2>Andamento per fase</h2>'+table(['Fase','PASS V51C','PASS avversari','Quota V51C','MOVE V51C','Persone V51C'],[[k,fmt(x['explicit_pass']),fmt(opp['phases'][k]['explicit_pass']),fmt(100*x['pass_share'])+'%',fmt(x['move']),fmt(x['people_h24'])] for k,x in v['phases'].items()])
body+='<p>Medie per giorno-partita. Verde: V51C · Arancio: avversari delle 42 partite · Blu: V48 storico, dove disponibile. I punti mostrano i valori al passaggio del mouse.</p><div class="grid">'
for key,title,pct in [('explicit_pass','PASS su persone presenti',False),('pass_share','Quota PASS (%)',True),('move','MOVE richiesti',False),('people_h24','Persone al checkpoint',False),('crop_tiles','Caselle coltivate',False),('animals','Animali presenti',False),('cash_h24','Cassa al checkpoint',False),('hire_cash','Spesa assunzioni',False),('WATER','WATER riusciti',False),('FEED','FEED riusciti',False),('CARE','CARE riusciti',False),('HARVEST','HARVEST riusciti',False)]:body+=chart(key,title,pct)
body+='</div><h2>Flussi economici medi per partita</h2>'+table(['Voce','V51C','Avversari'],[[label,*[fmt(mean(sum(sum(d[k].values()) if isinstance(d[k],dict) else d[k] for d in p[side+'_ledger']['daily']) for p in ps)) for side in ['candidate','opponent']]] for k,label in [('sales_cash','Vendite'),('purchase_cash','Acquisti'),('hire_cash','Assunzioni'),('land_cash','Terreno'),('unit_cash_delta','Altri flussi azioni')]])
body+='<h2>Picchi di PASS</h2>'+table(['Replay','Avversario','Giorno','PASS','Slot','Quota','MOVE'],[[f'<a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56124996&amp;episodeId={ep}">{ep}</a>',esc(name),day,n,slots,fmt(100*n/slots)+'%',move] for n,ep,day,name,slots,move in peaks])
body+='<h2>Dettaglio D1–D30</h2>'+table(['Giorno','PASS [min–max]','Quota','MOVE','Persone','Colture','Animali','Cassa','WATER','FEED','CARE','HARVEST'],[[d['day'],f"{fmt(d['explicit_pass'])} [{d['pass_min']}–{d['pass_max']}]",fmt(100*d['pass_share'])+'%',*[fmt(d[k]) for k in ['move','people_h24','crop_tiles','animals','cash_h24','WATER','FEED','CARE','HARVEST']]] for d in v['daily']])
body+='<h2>Risultati per partita</h2>'+table(['Replay','Avversario','Seat','Esito','Cassa','Delta','PASS/giorno','MOVE/giorno','PASS D29','Persone D29'],[[p['episode'],esc(p['opponent_name']),p['seat'],'V' if p['cash']>p['opponent_cash'] else 'S' if p['cash']<p['opponent_cash'] else 'P',fmt(p['cash']),fmt(p['cash']-p['opponent_cash']),fmt(mean(d['explicit_pass'] for d in p['candidate'])),fmt(mean(d['move'] for d in p['candidate'])),p['candidate'][28]['explicit_pass'],p['candidate'][28]['people_h24']] for p in reversed(ps)])
extra={side:sum(d['extra_requested_pass'] for p in ps for d in p[side]) for side in ['candidate','opponent']}
idle={side:sum(d['implicit_idle'] for p in ps for d in p[side]) for side in ['candidate','opponent']}
body+=f'''<h2>Metodo, fonti e riproduzione</h2><p>Azioni attribuite al giorno dell'osservazione precedente: 719 batch su 30 giorni. PASS e MOVE sono richiesti su persone presenti prima del batch; WATER, FEED, CARE e HARVEST contano cambiamenti riusciti. PASS per lavoratori inesistenti esclusi: V51C {extra['candidate']}, avversari {extra['opponent']}. Slot senza comando valido separati: V51C {idle['candidate']}, avversari {idle['opponent']}. Metodo identico a V48, compreso il default PASS per farmer assente; tale default non interviene nelle azioni V51C verificate.</p>
<p>Checkpoint H24 prima dell'ultimo batch per D1–D29, terminale per D30. I flussi economici sono invece attribuiti al giorno dell'azione. Le medie di consistenze non sono inventari di una singola fattoria; i servizi vanno letti rispetto al fabbisogno, non solo al volume.</p>
<p><a href="cohort.json">Coorte e hash originali</a> · <a href="summary.json">KPI JSON</a> · <a href="daily_kpi.csv">KPI giornalieri CSV</a> · <a href="matches.csv">Partite CSV</a> · <a href="biological_daily.csv">Deficit giornalieri CSV</a> · <a href="manifest.json">Manifest</a>. Replay originali in data/replays/json/v51_external_20260909. Questi casi sono ora esposti e non sono holdout per nuove varianti. Gli script download_v51_external.py, analyze_v51_external.py e build_v51_external_report.py riproducono il report.</p>'''
page='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V51C esterna — KPI replay</title><style>body{background:#191f27;color:#dce6ef;font:16px/1.6 system-ui;max-width:1400px;margin:30px auto;padding:20px}h1,h2,a{color:#91ccf4}h2{font-size:22px}table{border-collapse:collapse;font-size:13px;width:100%}td,th{padding:7px;border:1px solid #3f4d5d;text-align:right}th{background:#253343}td:first-child,th:first-child{text-align:left}.scroll{overflow:auto;margin:20px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,400px),1fr));gap:22px}svg{width:100%}svg text{fill:#b8c9dd;font-size:12px}strong{color:#4fe1c0}</style>'+body+'</html>'
assert '\ufffd' not in page
(O/'REPORT_V51_REPLAY_KPI_IT.html').write_text(page,encoding='utf-8')
rows=[dict(cohort=name,**{k:x for k,x in d.items() if not isinstance(x,list)}) for name,g in [('V51C',v),('opponents',opp),('V48_historical',old)] for d in g['daily']]
with (O/'daily_kpi.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
with (O/'matches.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(cohort['games'][0]));w.writeheader();w.writerows(cohort['games'])
(O/'diagnostics.json').write_text(json.dumps(dict(biological_totals=bio,animal_escapes=escapes,late_pass_fraction=sum(hours[18:])/sum(hours),extra_pass=extra,implicit_idle=idle,cash_discrepancies=discrepancies,net_cash_residuals=residuals),indent=2),encoding='utf-8')
sources=[Path(__file__).with_name('audit_v51_external_ledger.py'),Path(__file__),Path(__file__).with_name('analyze_v51_external.py'),Path(__file__).with_name('download_v51_external.py'),Path(__file__).with_name('audit_v49_obligations.py'),Path(__file__).with_name('portfolio_workforce_v16.py'),ROOT/'docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d30_closure.py',ROOT/'docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d20_trajectories.py',ROOT/'docs/foundation/ENGINE_SOURCE_MANIFEST.json',B/'reports/v48_external_pass_update_20260908/summary.json']
manifest=dict(submission_id=56124996,raw_replays=cohort['games'],sources={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.is_file() and p.name not in ['manifest.json','analysis.log','download.log','build.log']})
(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(results={k:v[k] for k in ['n','wins','losses','cash_mean']},pass_daily=total['explicit_pass'],pass_share=total['pass_share'],d29=d29,old_d29=o29,biology=bio,escapes=escapes),indent=2))
