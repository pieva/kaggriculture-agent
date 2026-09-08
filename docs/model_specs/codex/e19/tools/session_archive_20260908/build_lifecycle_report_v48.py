import json,hashlib
from pathlib import Path
from collections import Counter
from html import escape
base=Path('docs/model_specs/codex/e19')
src=base/'artifacts/derived/lifecycle_audit_770_20260908'
files=sorted(src.glob('daily_routes_v48_*.json'))
assert len(files)==6
rows=[]; events=[]
for f in files:
    d=json.loads(f.read_text(encoding='utf-8'))
    assert d['frozen_sides_equal'] and d['errors']==0 and d['incomplete']==0
    e=d['lifecycle_audit']['candidate']
    assert len(e)==len(d['sides']['candidate']['crop_starvation'])
    rows.append([d['seed'],d['seat'],len(e),sum(x['productive_loss'] for x in e),sum(not x['productive_loss'] for x in e),d['sides']['candidate']['reward']])
    events.extend(dict(seed=d['seed'],seat=d['seat'],**x) for x in e)
productive=[e for e in events if e['productive_loss']]
summary=dict(cases=rows,legacy_events=len(events),productive_events=len(productive),spent_events=len(events)-len(productive),held_units=sum(e['held_units_after_actions'] for e in productive),events=events)
dst=base/'reports/lifecycle_audit_770_20260908';dst.mkdir(parents=True,exist_ok=True)
(dst/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
def table(headers,rows):
    return '<table><thead><tr>'+''.join('<th>'+escape(str(v))+'</th>' for v in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+escape(str(v))+'</td>' for v in r)+'</tr>' for r in rows)+'</tbody></table>'
html='''<!doctype html><html lang="it"><meta charset="utf-8"><title>V48: audit biologico delle perdite</title><style>body{background:#181d22;color:#e1e7ee;font:17px/1.6 system-ui;max-width:1150px;margin:40px auto;padding:20px}h1,h2{color:#83cafa}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #46525f;padding:8px;text-align:left}a{color:#83cafa}strong{color:#ffb789}</style><h1>V48: audit biologico delle perdite</h1>
<p>8 settembre 2026 · Solo 770 · Policy invariata · Sei partite locali contro V4D</p>
<h2>Correzione della diagnosi precedente</h2><p>La fragola [2,9], seme 180903003, non perde l’ultimo raccolto a D28. Il lavoratore 9 raggiunge la casella e raccoglie l’unità residua a H24. Il ciclo produttivo è già concluso. La precedente descrizione dei due eventi aggiuntivi come perdita da correggere irrigando era sbagliata.</p>
<p>Il vecchio indicatore osserva piante asciutte che diventano infestanti: non distingue produzione persa, pianta esaurita e decadimento. Le serie storiche rimangono conservate; questo audit riclassifica esclusivamente V48. Non è corretto confrontare il nuovo conteggio con la vecchia mortalità delle altre versioni.</p>
<h2>Che cosa accade nella casella</h2>'''
html+=table(['Momento','Evidenza'],[['D12','Semina fragola'],['D22, D24, D26, D28','Quattro date biologiche di produzione'],['D28 H13','Assegnazione del percorso al lavoratore 9'],['D28 H24','Arrivo a [2,9], HARVEST dell’ultima unità'],['Fine D28','Nessuna unità residua, nessuna produzione futura; trasformazione per stress idrico'],['Controfattuale WATER','La pianta supera il refresh, ma diventa infestante al decadimento della prima azione D29: nessuna resa aggiuntiva']])
html+='<h2>Verifica su sei casi</h2><p>Consistenze giornaliere, ledger, KPI operativi, risultati e indicatori originali coincidono integralmente con i sei file V48 congelati.</p>'
html+=table(['Seme','Posizione','Eventi vecchio audit','Con prodotto o potenziale residuo','Esaurite e vuote','Cassa'],rows)
html+=f'<p><strong>{len(events)} eventi complessivi: {len(productive)} con prodotto o potenziale residuo, {len(events)-len(productive)} su piante esaurite e vuote.</strong> Le unità presenti dopo le azioni negli eventi con rischio produttivo sono {summary["held_units"]}. Il potenziale futuro non è una stima di ricavo perso: dipende da cure, raccolta e prezzi.</p>'
html+='<h2>Registro verificabile</h2>'
html+=table(['Seme','Pos.','Giorno','Casella','Coltura','Unità residue','Produzioni future','Causa fisica','Rischio produttivo'],[[e['seed'],e['seat'],e['service_day'],e['position'],e['crop'],e['held_units_after_actions'],e['future_production'],e['physical_cause'],e['productive_loss']] for e in events])
html+='''<h2>Decisione</h2><p>Conservare V48. Non aggiungere acqua sulle fragole esaurite per migliorare artificialmente il KPI. La prossima ottimizzazione deve concentrarsi sugli eventi con prodotto o potenziale residuo, distinguendo la raccolta mancata dalla mancata irrigazione. L’infestante resta un costo di occupazione e di eventuale rinnovo: assenza di prodotto perso non significa terreno già pronto per la semina.</p><p><a href="../productive_water_770_20260908/v48_TOP770_D01_D30_COMPLETE_KPI.html">Report completo: 22 KPI V48 / Top770 (conteggi storici non riclassificati)</a> · <a href="summary.json">Dati dell’audit</a></p></html>'''
assert not any(c in html for c in ['\ufffd','\u00c3','\u00c2'])
(dst/'REPORT_AUDIT_BIOLOGICO_V48_IT.html').write_text(html,encoding='utf-8')
sources=files+[src/'counterfactual.json',base/'tools/crop_lifecycle_audit_v48.py',base/'tools/run_lifecycle_audit_v48.py',Path('.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py')]
(dst/'manifest.json').write_text(json.dumps({str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in sources},indent=2),encoding='utf-8')
note=f'''# Rettifica audit V48 — 2026-09-08

La fragola [2,9] D28 seme 180903003 è raccolta a H24 ed esaurita. WATER ritarda l'infestante di una sola azione, senza altra resa. Non correggere la policy per questo caso. Sei replay rieseguiti con sides integralmente uguali ai congelati. Audit V48: {len(events)} vecchi eventi, {len(productive)} con prodotto/potenziale residuo, {len(events)-len(productive)} esauriti e vuoti. I vecchi conteggi delle altre versioni NON sono riclassificati e non sono comparabili a quello nuovo. V48 resta candidata locale, non pubblicata. Solo 770.

Report: docs/model_specs/codex/e19/reports/lifecycle_audit_770_20260908/REPORT_AUDIT_BIOLOGICO_V48_IT.html
Prossimo passo: diagnosticare gli eventi produttivi del registro; separare scadenza del raccolto, acqua e costo del rinnovo. Non elevare priorità su piante senza prodotto e senza produzioni future.

---

'''
for f in [Path('docs/NEW_SESSION.md'),Path('docs/PROJECT_STATE.md')]:
    f.write_text(note+f.read_text(encoding='utf-8'),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='events'},indent=2))
