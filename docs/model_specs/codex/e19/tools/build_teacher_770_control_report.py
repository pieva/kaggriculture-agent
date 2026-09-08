"""Read every crop and phase before assessing the D11 handover control."""
import hashlib
import json
from pathlib import Path
from statistics import mean, median
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate, FIELDS, TOP, fmt

BASE = ROOT/'docs/model_specs/codex/e19'
OUT = BASE/'reports/teacher_770_control_20260907'
CROPS = ['WHEAT', 'STRAWBERRY', 'CARROT', 'TOMATO', 'MELON']
PHASES = [(12, 15), (16, 24), (25, 29)]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def assess(matches):
    profiles = [m['sides']['assisted'] for m in matches]
    cash = mean(p['reward'] for p in profiles)
    opponent = mean(m['sides']['v4d']['reward'] for m in matches)
    return dict(cases=len(matches), cash=cash, opponent_cash=opponent,
                relative_pct=100*(cash/opponent-1),
                crop_starvation=sum(len(p['crop_starvation']) for p in profiles),
                animal_escapes=sum(len(p['ledger']['animal_escapes']) for p in profiles),
                opponent_crop_starvation=sum(len(m['sides']['v4d']['crop_starvation']) for m in matches),
                phases={f'D{a}-D{b}': {
                    c: dict(occupancy=mean(sum(p['daily'][d-1]['crops'][c] for d in range(a,b+1))/(b-a+1) for p in profiles),
                            planted=mean(sum(p['ledger']['daily'][d-1]['planted'].get(c,0) for d in range(a,b+1)) for p in profiles),
                            harvested=mean(sum(p['ledger']['daily'][d-1]['harvested'].get(c,0) for d in range(a,b+1)) for p in profiles))
                    for c in CROPS} for a,b in PHASES})


def main():
    OUT.mkdir(exist_ok=True)
    cases = [(s,t) for s in range(180903001,180903004) for t in (0,1)]
    paths = [BASE/'artifacts/derived/teacher_770_d30_20260907'/f'{s}_{t}.json' for s,t in cases]
    oldpaths = [BASE/'artifacts/derived/assisted_770_complete_20260907'/f'{s}_{t}.json' for s,t in cases]
    new, old = [read(p) for p in paths], [read(p) for p in oldpaths]
    assert all(p['prefix_parity'] and not p['capacity_violations'] and p['teacher_errors']==0 and p['teacher_fallbacks']==0 for p in new)
    assert all(p['sides']['assisted']['daily'][-1]['pasture_topology']=={'Q0':7,'Q1':7,'Q2':0,'Q3':0} for p in new)
    summary = {'base':assess(old), 'teacher_770':assess(new)}
    summary['decision'] = 'NOT_PROMOTED: biological crop losses; diagnostic historical control, not a parametric core'
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    top = read(TOP[0])['jesse']
    frozenpath = ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_28_C_TOP770_D01_D30_KPI_19.json'
    frozen = read(frozenpath)
    assert frozen['cohorts']['top770']['episodes']==[p['episode_id'] for p in top]
    economic = '<div class="tablewrap"><table><tr><th>Stessi 6 casi</th><th>Core da D12</th><th>V4D guidata 770 fino D30</th></tr>'
    for label,key in [('Cassa media','cash'),('Cassa avversaria media','opponent_cash'),('Scarto relativo (%)','relative_pct'),('Perdite colture per mancata acqua','crop_starvation'),('Fughe animali','animal_escapes'),('Perdite colture avversarie','opponent_crop_starvation')]:
        economic += '<tr><td>'+label+'</td>'+''.join('<td>'+fmt(summary[k][key])+'</td>' for k in ['base','teacher_770'])+'</tr>'
    economic += '</table></div><p>Il mercato è condiviso: cambiando la candidata cambia anche il risultato di V4D. Si riportano entrambe le casse. Il confronto storico Top resta descrittivo.</p>'
    crop_table = '<div class="tablewrap"><table><tr><th>Fase</th><th>Coltura</th><th>Base: superficie media</th><th>Controllo: superficie media</th><th>Top001: superficie media</th><th>Base: semine</th><th>Controllo: semine</th><th>Top001: semine</th></tr>'
    for a,b in PHASES:
        for c in CROPS:
            values = []
            for metric in ['occupancy','planted']:
                values += [summary[k]['phases'][f'D{a}-D{b}'][c][metric] for k in ['base','teacher_770']]
                values += [mean(sum(p['daily'][d-1]['crops'][c] for d in range(a,b+1))/(b-a+1) for p in top) if metric=='occupancy' else mean(sum(p['ledger']['daily'][d-1]['planted'].get(c,0) for d in range(a,b+1)) for p in top)]
            crop_table += f'<tr><td>D{a}–D{b}</td><td>{c}</td>'+''.join('<td>'+fmt(v)+'</td>' for v in values)+'</tr>'
    crop_table += '</table></div><p>Medie per partita e fase. Le medie delle superfici sono additive; le mediane marginali dei grafici non lo sono. Le semine includono espansione e sostituzioni. D30 è liquidazione: visibile nei grafici ma escluso dalle tre finestre di produzione.</p>'
    diagnosis = '''<h2>Diagnosi integrata e decisione</h2>
<p>Il controllo mantiene il gestore storico V4D per tutta la partita e il filtro osservato 7–7–0. Non usa il core parametrico dopo D11. Il prefisso è identico azione per azione; topologia verificata in tutti i 720 stati, eccezioni del callback e fallback del gestore controllati.</p>
<p>L’espansione dopo D11 torna possibile: non è impedita dalla sola topologia. Il passaggio al core parametrico è quindi una causa sperimentalmente verificata della diversa traiettoria, a parità del prefisso e del filtro iniziale. Questo non isola ancora il peso rispettivo di scelta colturale, percorsi e servizi.</p>
<p>La gestione storica non è una soluzione finale: perde colture, continua a preferire meloni dopo D11 e non replica la conversione alle carote del Top. Le perdite sono presenti anche nella V4D avversaria: non attribuirle automaticamente al filtro 770. Nessuna versione è promossa.</p>
<h2>Lavoro successivo sul core</h2>
<ol><li>Mantenere l’apertura congelata D1–D11; pianificare insieme espansione, rinnovo e cambio di coltura.</li>
<li>Confrontare successioni di colture con lo stesso orizzonte, includendo occupazione del terreno, lavoro ricorrente, raccolta e consegna. La graduatoria attuale di un singolo ciclo per percorso iniziale non basta.</li>
<li>Assegnare missioni compatibili con acqua e alimentazione; diagnosticare separatamente rifiuti per capacità e scelte economiche. Acquisto terreno e prima messa a coltura devono appartenere allo stesso piano eseguibile.</li>
<li>Valutare tutte le cinque colture nelle tre fasi, tutti i 22 KPI, cassa propria e avversaria, perdite biologiche e topologia. Nessun miglioramento isolato della superficie o del grano basta per promuovere una versione.</li></ol>'''
    template = Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')
    a=template.index('<h2>Diagnosi</h2>');b=template.index('<details>',a)
    template=template[:a]+diagnosis+crop_table+template[b:]
    template=template.replace('Guida V4D fino a D11; core parametrico da D12, indicato dalla linea verticale.','Guida V4D con filtro 770 per tutta la partita. La linea D12 indica soltanto la fine del prefisso comune.')
    template=template.replace('770 assistita V1','Controllo V4D 770').replace("candidate:'770 assistita'","candidate:'Controllo V4D 770'")
    template=template.replace('Altro Top770','Diagnosi del core').replace('Rigenerazione dei 14 run locali verificata contro tutti i KPI, ledger e risultati precedenti.','Sei controlli locali conclusi: parità del prefisso, topologia e ledger verificati.')
    payload=dict(topLabel='Top770-001',metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate([p['sides']['assisted'] for p in new]),top770=aggregate(top,frozen['series']['top770'])))
    filename='CONTROLLO_V4D_770_Top770_001_D01_D30_COMPLETE_KPI'
    (OUT/(filename+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    values=dict(TITLE='Controllo V4D 770 vs Top770-001 · KPI D1–D30',COHORTS='6 partite locali contro V4D · 5 replay storici Top770-001',OTHER='../portfolio_transition_20260907/DIAGNOSI_PORTAFOGLIO_IT.md',TOP='Top770-001',ECONOMY=economic,PROVENANCE='Controllo diagnostico: stessa submission assistita congelata, assisted_days=30. Semi 180903001–003, entrambe le posizioni. Nessuna nuova fonte esterna. Episodi Top001: '+', '.join(str(p['episode_id']) for p in top),DATAFILE=filename+'.json',DATA=json.dumps(payload,ensure_ascii=False).replace('</',r'<\/'))
    for k,v in values.items():template=template.replace('__'+k+'__',v)
    assert '__TITLE__' not in template and len(payload['metrics'])==22
    assert all(len(series)==30 for group in payload['series'].values() for series in group.values())
    (OUT/(filename+'.html')).write_text(template,encoding='utf-8')
    sources=paths+oldpaths+[TOP[0],frozenpath,Path(__file__),Path(__file__).with_name('run_teacher_770_d30.py'),Path(__file__).with_name('complete_kpi_template.html'),ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py']
    (OUT/'manifest.json').write_text(json.dumps(dict(sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2))
    print(json.dumps({k:{m:v for m,v in s.items() if m!='phases'} if isinstance(s,dict) else s for k,s in summary.items()},indent=2))


if __name__=='__main__':
    main()
