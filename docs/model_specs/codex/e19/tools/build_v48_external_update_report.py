"""Build the frozen external PASS report and its artifact manifest."""
import html
import hashlib
import json
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[5]
B=ROOT/'docs/model_specs/codex/e19'
O=B/'reports/v48_external_pass_update_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
s=read(O/'summary.json');cohort=read(O/'cohort.json')
ps=[read(O/f"profile_{r['episode']}.json") for r in cohort['games']]
fmt=lambda x:f'{x:,.2f}'.replace(',','_').replace('.',',').replace('_','.')
esc=html.escape

def table(headers,rows):
    return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+esc(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def chart(key,title,percent=False):
    groups=[('first8','V48 primi 8','#72b1de'),('new30','V48 nuovi 30','#4fe1c0'),('opponents38','Avversari 38','#f6a36c')]
    scale=100 if percent else 1
    high=max(d[key]*scale for name,_,_ in groups for d in s[name]['daily'])*1.12 or 1
    svg='<svg viewBox="0 0 720 255" role="img" aria-label="'+esc(title)+'">'
    for i in range(5):
        y=215-i*47;v=high*i/4
        svg+=f'<path d="M50 {y}H700" stroke="#394452"/><text x="3" y="{y+4}">{v:.1f}</text>'
    for day in [1,5,10,15,20,25,30]:
        x=50+(day-1)*650/29;svg+=f'<text x="{x-8}" y="240">D{day}</text>'
    for name,label,color in groups:
        points=' '.join(f"{50+i*650/29:.1f},{215-d[key]*scale/high*188:.1f}" for i,d in enumerate(s[name]['daily']))
        svg+=f'<polyline points="{points}" stroke="{color}" stroke-width="2.5" fill="none"/>'
        for i,d in enumerate(s[name]['daily']):
            x=50+i*650/29;y=215-d[key]*scale/high*188
            svg+=f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"><title>{label}, D{i+1}: {fmt(d[key]*scale)}</title></circle>'
    return '<section class="chart"><h2>'+title+'</h2>'+svg+'</svg></section>'

overview=table(['Coorte','Partite','Vittorie / sconfitte','Cassa V48 media','PASS/giorno','PASS / slot'],[
 [label,s[k]['n'],f"{s[k]['wins']} / {s[k]['losses']}",fmt(s[k]['cash_mean']),fmt(s[k]['phases']['D1-D30']['explicit_pass']),fmt(100*s[k]['phases']['D1-D30']['pass_share'])+'%']
 for k,label in [('first8','Primo controllo'),('new30','Nuovi replay'),('all38','Totale osservato')]])
phase=table(['Fase','PASS V48','PASS avversari','MOVE V48','MOVE avversari','Quota PASS V48','Quota PASS avversari'],[
 [k,fmt(v['explicit_pass']),fmt(s['opponents38']['phases'][k]['explicit_pass']),fmt(v['move']),fmt(s['opponents38']['phases'][k]['move']),fmt(100*v['pass_share'])+'%',fmt(100*s['opponents38']['phases'][k]['pass_share'])+'%']
 for k,v in s['all38']['phases'].items()])
peaks=sorted([(d['explicit_pass'],p['episode'],d['day'],p['opponent_name'],d['slots'],d['move']) for p in ps for d in p['candidate']],reverse=True)[:12]
peak_table=table(['Episodio','Avversario','Giorno','PASS','Slot','Quota','MOVE'],[
 [f'<a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56101593&amp;episodeId={ep}">{ep}</a>',esc(opp),'D'+str(day),n,slots,fmt(100*n/slots)+'%',move] for n,ep,day,opp,slots,move in peaks])
daily=table(['Giorno','PASS V48 media [min–max]','PASS avversari','Quota V48','MOVE V48','Coltivate V48','WATER V48 / avv.','FEED V48 / avv.','CARE V48 / avv.'],[
 ['D'+str(d['day']),f"{fmt(d['explicit_pass'])} [{d['pass_min']}–{d['pass_max']}]",fmt(o['explicit_pass']),fmt(100*d['pass_share'])+'%',fmt(d['move']),fmt(d['crop_tiles']),f"{fmt(d['WATER'])} / {fmt(o['WATER'])}",f"{fmt(d['FEED'])} / {fmt(o['FEED'])}",f"{fmt(d['CARE'])} / {fmt(o['CARE'])}"] for d,o in zip(s['all38']['daily'],s['opponents38']['daily'])])
matches=table(['Episodio','Coorte','Avversario','Esito','Cassa V48','Delta cassa','PASS V48/giorno','PASS avv./giorno','Max PASS V48'],[
 [p['episode'],p['cohort'],esc(p['opponent_name']),'V' if p['cash']>p['opponent_cash'] else 'S' if p['cash']<p['opponent_cash'] else 'P',fmt(p['cash']),fmt(p['cash']-p['opponent_cash']),fmt(mean(d['explicit_pass'] for d in p['candidate'])),fmt(mean(d['explicit_pass'] for d in p['opponent'])),max(d['explicit_pass'] for d in p['candidate'])] for p in reversed(ps)])
total=s['all38']['phases']['D1-D30'];opp=s['opponents38']['phases']['D1-D30']
extras={side:sum(d.get('extra_requested_pass',0) for p in ps for d in p[side]) for side in ['candidate','opponent']}
implicit={side:sum(d['implicit_idle'] for p in ps for d in p[side]) for side in ['candidate','opponent']}
hours=[sum(d['pass_hours'][h] for p in ps for d in p['candidate']) for h in range(24)]
late=sum(hours[18:])/sum(hours)
peakdays=sorted(s['all38']['daily'],key=lambda d:-d['explicit_pass'])[:4]
findings=f'''<h2>Analisi dei PASS</h2><p>Nel totale osservato V48 richiede <strong>{fmt(total['explicit_pass'])} PASS al giorno</strong>, contro {fmt(opp['explicit_pass'])} degli avversari. La quota sulle opportunità d'azione delle persone presenti è {fmt(100*total['pass_share'])}% contro {fmt(100*opp['pass_share'])}%. Il confronto è descrittivo: gli avversari hanno strategie, dimensioni e livelli diversi e non sono una coorte Top770.</p>
<p>I giorni con più PASS medi sono {', '.join('D'+str(d['day'])+' ('+fmt(d['explicit_pass'])+')' for d in peakdays)}. Il {fmt(100*late)}% dei PASS cade nelle ultime sei ore del giorno. Nelle vittorie V48 ha {fmt(s['wins']['phases']['D1-D30']['explicit_pass'])} PASS/giorno; nelle sconfitte {fmt(s['losses']['phases']['D1-D30']['explicit_pass'])}. Questa associazione non dimostra un effetto causale.</p>
<p>Per giornata-partita, {fmt(total['pass_critical_water'])} PASS coincidono con almeno una pianta ancora senza acqua e con contatore di carenza ≥1; {fmt(total['pass_unfed_animals'])} coincidono con animali non ancora alimentati. Sono stati <em>prima</em> del batch, non servizi sicuramente persi a fine giornata. {fmt(total['pass_current_tile_service'])} PASS/giorno avvengono su una casella con WATER, CARE o FEED legalmente disponibile e senza altri comandi attivi sulla stessa casella (FEED richiede grano nell'inventario).</p>
<p>Questi ultimi casi sono candidati per la diagnosi del dispatcher, non un conteggio certificato di PASS evitabili: occorre ancora verificare utilità biologica, scadenze, prenotazioni e valore terminale. Il replay mostra azioni e stato, non le ragioni interne di scarto della policy.</p>
<p><strong>Prossimo intervento:</strong> riprodurre i picchi elencati sotto con telemetria dei lavori candidati e dei motivi di rifiuto; confrontare carico biologico e personale prima delle assunzioni. Non promuovere modifiche che sostituiscano PASS con MOVE o servizi inutili. La V48 resta congelata.</p>'''
body=f'''<h1>V48 esterna: aggiornamento replay e PASS</h1><p>Submission 56101593 · 38 partite complete · 30 nuove rispetto al primo controllo · 8 settembre 2026.</p>
<p><strong>Il rating cresce, i PASS restano invariati:</strong> {fmt(s['first8']['phases']['D1-D30']['explicit_pass'])} al giorno nei primi 8 replay e {fmt(s['new30']['phases']['D1-D30']['explicit_pass'])} nei 30 nuovi. Il risultato competitivo non dimostra una correzione della gestione del lavoro. D2 registra esattamente 69 PASS in tutti i 38 casi; D29 varia da 22 a 135. Avvio ripetitivo e chiusura variabile richiedono diagnosi separate.</p>
<p>Rating osservato all'inizio dell'acquisizione: <strong>972,5</strong> (primo controllo 822,1). V29 nella stessa pagina: 840,6; V4D ripubblicata: 1083,5. Snapshot di classifica, non una misura definitiva o un confronto controllato.</p>{overview}{findings}
<h2>Confronto per fase</h2>{phase}<p class="legend">Blu: V48 primi 8 · Verde: V48 nuovi 30 · Arancio: avversari delle 38 partite. Medie puntuali, non traiettoria di una singola partita. Passare sui punti per i valori.</p><div class="grid">'''
for key,title,pct in [('explicit_pass','PASS su persone presenti',False),('pass_share','Quota PASS (%)',True),('move','MOVE richiesti',False),('people_h24','Persone al checkpoint',False),('crop_tiles','Caselle coltivate',False),('WATER','WATER riusciti',False),('FEED','FEED riusciti',False),('CARE','CARE riusciti',False)]:body+=chart(key,title,pct)
body+='</div><h2>Picchi nei singoli replay</h2>'+peak_table+'<h2>Dettaglio D1–D30: tutte le 38 partite</h2>'+daily+'<h2>Risultati per episodio</h2>'+matches
body+=f'''<h2>Metodo e limiti</h2><p>Coorte congelata sulle 38 partite non-self visibili al primo accesso, fino all'episodio 106869264. Una partita contro se stessi esclusa. Eventuali partite comparse durante l'analisi non fanno parte di questa coorte. L'associazione alla submission proviene dalla cronologia UI Kaggle; i replay verificano ID episodio, nomi, stati DONE e 720 snapshot.</p>
<p>Azioni attribuite al giorno dell'osservazione precedente, su 719 transizioni. PASS e MOVE sono comandi richiesti a persone effettivamente presenti prima del batch. I comandi PASS per indici di lavoratori inesistenti sono esclusi dalla misura della capacità: V48 {extras['candidate']}, avversari {extras['opponent']}. Slot senza comando valido: V48 {implicit['candidate']}, avversari {implicit['opponent']}; sono riportati separatamente dai PASS espliciti. Non confrontare direttamente questi conteggi corretti con vecchi grafici che contavano qualsiasi elemento della lista hands.</p>
<p>WATER/FEED/CARE sono ricostruiti con le azioni dell'engine locale e verificati sul cambiamento della casella. Il ledger controlla i saldi di entrambi i giocatori a ogni transizione. Consistenze H24 prima dell'ultimo batch per D1–D29; D30 terminale. Non dedurre copertura dei servizi dai soli volumi: dipende anche da numero di colture/animali e loro fase.</p>
<p>Fonti e dati: <a href="cohort.json">coorte e hash dei replay</a>, <a href="summary.json">riepilogo numerico</a>, <a href="manifest.json">manifest</a>. I JSON grezzi nuovi sono conservati in data/replays/json/v48_update_20260908, esclusi da Git. Tutti questi casi sono ora esposti; non riutilizzarli come holdout di nuove varianti.</p>'''
page='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V48 esterna — replay e PASS</title><style>body{background:#191f27;color:#dce6ef;font:16px/1.6 system-ui;max-width:1400px;margin:30px auto;padding:20px}h1,h2,a{color:#91ccf4}h2{font-size:22px}table{border-collapse:collapse;font-size:13px;width:100%}td,th{padding:7px;border:1px solid #3f4d5d;text-align:right}th{background:#253343}td:first-child,th:first-child{text-align:left}.scroll{overflow:auto;margin:20px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:22px}svg{width:100%}svg text{fill:#b8c9dd;font-size:12px}.legend{color:#aaa}strong{color:#4fe1c0}</style>'+body+'</html>'
assert '\ufffd' not in page
(O/'REPORT_V48_REPLAY_PASS_IT.html').write_text(page,encoding='utf-8')
files=[Path(__file__),Path(__file__).with_name('analyze_v48_external_update.py'),Path(__file__).with_name('download_v48_update.py'),ROOT/'docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d30_closure.py',ROOT/'docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d20_trajectories.py']
files += [ROOT/'.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py', B/'artifacts/derived/v48_external_20260908/first_cohort.json',B/'artifacts/derived/v48_external_manifest.json']
manifest=dict(submission_id=56101593,raw_replays=cohort['games'],sources={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.is_file() and p.name!='manifest.json'})
(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(all=total,opponents=opp,extras=extras,implicit=implicit,late_hour_pass_fraction=late,peak_days=[d['day'] for d in peakdays]),indent=2))
