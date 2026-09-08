"""Render complete KPI and explicit analysis of the frozen external cohort."""
import json, re, html, hashlib, sys
from pathlib import Path
from statistics import mean, median
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate,FIELDS,TOP,fmt
from docs.model_specs.codex.e18.tools.build_e18_27_top770_complete_kpi import flatten
BASE=ROOT/'docs/model_specs/codex/e19'
OUT=BASE/'reports/v29_external_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
records=read(OUT/'profiles.json')
candidate=[x['sides']['candidate'] for x in records]
opponents=[x['sides']['opponent'] for x in records]
top=read(TOP[0])['jesse']
frozen=read(ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_28_C_TOP770_D01_D30_KPI_19.json')['series']['top770']
series=aggregate(candidate)
def rows(profiles):
    return [[flatten(s)|o|{k:f['executed_actions'].get(k,0) for k in ['WATER','FEED','CARE','PLANT']} for s,o,f in zip(p['daily'],p['operational_daily'],p['ledger']['daily'])] for p in profiles]
crows,orows=rows(candidate),rows(opponents)
def table(headers, values):
    return '<div class="tablewrap"><table><tr>'+''.join('<th>'+html.escape(str(h))+'</th>' for h in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in values)+'</table></div>'
cash=[p['terminal']['cash'] for p in candidate]; ocash=[p['terminal']['cash'] for p in opponents]
diff=[a-b for a,b in zip(cash,ocash)]
wins=sum(d>0 for d in diff)
deaths=[len(p['crop_starvation']) for p in candidate]
assert all(p['ledger']['daily'][d-1]['executed_actions'].get('PLANT',0)==0 for p in candidate for d in [21,22])
assert all(p['ledger']['daily'][d-1]['requested_actions'].get('PLANT',0)==0 for p in candidate for d in [21,22])
games=[]
for r,a,b,dd in zip(records,cash,ocash,deaths):
    ep=r['episode_id']; opponent=html.escape(r['names'][1-r['seat']])
    games.append([f'<a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56093101&episodeId={ep}">{ep}</a>',opponent,r['seat'],fmt(a),fmt(b),fmt(a-b),'V' if a>b else 'S' if a<b else 'P',dd])
economy=table(['Episodio','Avversario','Seat V29','Cassa V29','Cassa avversario','Delta','Esito','Morti idriche V29'],games)
phase=[]
for lo,hi in [(1,11),(12,20),(21,25),(26,30)]:
    for k in ['crop_tiles','WHEAT','STRAWBERRY','CARROT','people','MOVE','PASS','WATER','FEED','CARE','weed_tiles']:
        vals=[mean(row[d-1][k] for row in rs for d in range(lo,hi+1)) for rs in [crows,orows]]
        phase.append([f'D{lo}–D{hi}',k,*map(fmt,vals),fmt(vals[0]-vals[1])])
economy+='<h2>Fasi: media su tutte le partite e tutti i giorni della finestra</h2>'+table(['Finestra','KPI','V29','Avversari','Delta'],phase)
daily=[]
for d in range(19,31):
    vals=[median(rs[d-1][k] for rs in crows) for k in ['WHEAT','STRAWBERRY','CARROT','crop_tiles','PLANT','MOVE','PASS','WATER','CARE','weed_tiles']]
    daily.append([f'D{d}',*map(fmt,vals)])
economy+='<h2>Successione e chiusura: mediane giornaliere V29</h2>'+table(['Giorno','Grano','Fragole','Carote','Coltivate','PLANT','MOVE','PASS','WATER','CARE','Infestanti'],daily)
diagnosis=f'''<h2>Analisi del benchmark</h2>
<p><strong>{wins} vittorie e {len(records)-wins} sconfitte.</strong> Cassa finale media {fmt(mean(cash))} contro {fmt(mean(ocash))}; delta medio {fmt(mean(diff))} ({fmt(100*mean(diff)/mean(ocash))}% sul totale avversario), delta mediano {fmt(median(diff))}. Il risultato medio quasi pari non dimostra il raggiungimento del Top. Rating Kaggle osservato: 860,3, provvisorio e relativo alla submission complessiva, non a questo sottoinsieme.</p>
<p><strong>La successione resta bloccata a D21–D22 in 11/11 partite.</strong> Non viene neppure richiesto un PLANT: non sono semine tentate e rifiutate dal motore. Grano mediano D20–D25: {', '.join(fmt(series['WHEAT'][d-1][0]) for d in range(20,26))}. L'identica finestra senza semine compare nelle sei prove locali V29: il benchmark conferma un difetto ricorrente del piano, non un episodio isolato dovuto a un avversario. L'attribuzione interna al filtro di ammissione richiede il log decisionale; i replay certificano l'assenza dei comandi e la perdita di continuità.</p>
<p><strong>PASS e spostamenti vanno letti insieme.</strong> La tabella per fasi mostra il tempo inutilizzato ancora elevato a D12–D20 e D26–D30. A D21–D25 il calo dei PASS non risolve la produttività: la V29 impiega molti MOVE mentre la superficie coltivata e i CARE calano. Non basta minimizzare PASS: occorre proteggere i turni di servizio e la risemina nei percorsi.</p>
<p><strong>Irrigazione: il problema è reale, oltre all'effetto del minor terreno coltivato.</strong> Sono verificate {sum(deaths)} morti idriche V29 in {sum(d>0 for d in deaths)}/{len(deaths)} partite, contro {sum(len(p['crop_starvation']) for p in opponents)} negli avversari complessivi. H24 non irrigato non equivale a morte: il controllo ricostruisce anche l'ultimo batch prima del refresh. Il minor numero di WATER riflette anche la superficie ridotta; non va interpretato da solo come tasso di copertura. Le infestanti sono uno stock distinto dalle morti idriche e possono derivare anche dalla fine del ciclo.</p>
<p><strong>La chiusura a carote resta poco sviluppata.</strong> La curva mediana non riproduce il picco storico Top770-001 di circa 38 caselle. Anche diversi avversari esterni usano altre chiusure: il confronto con il loro aggregato non sostituisce il benchmark Top. Va pianificato il ciclo completo, dalla liberazione della parcella alla raccolta e vendita entro D30, senza adottare un obiettivo di caselle scollegato dai prezzi e dai tempi.</p>
<p><strong>Passo successivo proposto:</strong> correggere nella sola 770 il passaggio raccolta–risemina di D20–D23, prenotando acqua e lavoro per il ciclo successivo; misurare insieme superficie, perdite idriche, CARE, MOVE, PASS e cassa. Il confronto esterno è diagnostico: nessuna nuova policy o submission è stata creata in questo benchmark.</p>'''
template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')
template=template.replace('770 assistita V1','V29 esterna').replace("candidate:'770 assistita'","candidate:'V29 esterna'").replace('7 settembre 2026','8 settembre 2026')
template=re.sub(r'<h2>Diagnosi</h2>.*?<details>',diagnosis+'<details>',template,flags=re.S)
template=re.sub(r'<p class="note">.*?</p>','<p class="note">Primo campione congelato: 11 partite completate del pannello V29, scelte in ordine di recenza, 5 vittorie e 6 sconfitte. Esclusi gli episodi ancora in corso, il self-play e gli otto completati più vecchi. <a href="__OTHER__">Passa all’altro confronto</a>.</p>',template,count=1,flags=re.S)
template=template.replace('Stessi corpus storici già utilizzati; nessun nuovo benchmark esterno o invio di submission. Rigenerazione dei 14 run locali verificata contro tutti i KPI, ledger e risultati precedenti.','Nuovo benchmark esterno V29. Ogni replay contiene 720 stati e due agenti DONE. Nessun nuovo invio di submission.')
for name,label,reference,other in [('V29_VS_AVVERSARI','Avversari affrontati',aggregate(opponents),'V29_VS_TOP770'),('V29_VS_TOP770','Top770-001',aggregate(top,frozen),'V29_VS_AVVERSARI')]:
    payload=dict(topLabel=label,metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=series,top770=reference),aggregation='median/min/max',episodes=[r['episode_id'] for r in records])
    filename=name+'_D01_D30_COMPLETE_KPI'
    provenance='Submission 56093101; SHA256 fa7e3fa7df0d5f02e7937e9940ca66f411154b1059a577790d970fb41e6ec71c. Seat identificato dai TeamNames dei replay scaricati dal pannello della submission. Gli avversari sono quelli delle stesse 11 partite; Top770-001 è un corpus storico diverso, non un confronto competitivo appaiato. Le mediane puntuali possono appartenere a partite diverse. Moduli di audit e relativi hash registrati nel manifest.'
    values=dict(TITLE='V29 esterna vs '+label+' · KPI completi D1–D30',COHORTS='11 replay esterni V29 · '+('11 avversari nelle stesse partite' if name=='V29_VS_AVVERSARI' else '5 replay storici Top770-001'),OTHER=other+'_D01_D30_COMPLETE_KPI.html',TOP=label,ECONOMY=economy,PROVENANCE=provenance,DATAFILE=filename+'.json',DATA=json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
    result=template
    for k,v in values.items(): result=result.replace('__'+k+'__',v)
    assert not re.search(r'__[A-Z]+__',result)
    assert not any(x in result for x in ['\u00c3','\u00c2','\ufffd'])
    (OUT/(filename+'.html')).write_text(result,encoding='utf-8')
    (OUT/(filename+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print(filename)
summary=dict(n=len(records),wins=wins,losses=len(records)-wins,cash_mean=mean(cash),opponent_cash_mean=mean(ocash),delta_mean=mean(diff),delta_median=median(diff),water_deaths=sum(deaths),zero_plant_D21_D22_games=len(records),episodes=[r['episode_id'] for r in records])
(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
sources=[BASE/'artifacts/derived/v29_external_20260908'/f"{r['episode_id']}.json" for r in records]+[Path(__file__),Path(__file__).with_name('benchmark_v29_external.py'),Path(__file__).with_name('complete_kpi_template.html'),TOP[0],ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_28_C_TOP770_D01_D30_KPI_19.json']
sources += [ROOT/p for p in ['docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d30_closure.py','docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d20_trajectories.py','docs/model_specs/codex/e18/tools/e18_29_crop_service_audit.py','experiments/e18/tools/common/replay_daily_operational_kpi.py']]
manifest=dict(created_utc=datetime.now(timezone.utc).isoformat(),submission_id=56093101,observed_rating=860.3,cohort_rule='First 11 completed games in captured UI ordering; in-progress, older eight and self-play excluded. No outcome selection.',sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'})
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
receipt=BASE/'artifacts/derived/v29_external_receipt.json'
v=read(receipt);v.update(status='Complete',submission_id=56093101,score=860.3,score_observed_date='2026-09-08',benchmark=str((OUT/'summary.json').relative_to(ROOT)))
receipt.write_text(json.dumps(v,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
