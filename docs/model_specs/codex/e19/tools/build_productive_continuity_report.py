"""Report the ablations in the owner's full 22-panel comparison format."""
import hashlib
import json
from pathlib import Path
from statistics import mean,median
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate,FIELDS,TOP,fmt
BASE=ROOT/'docs/model_specs/codex/e19'
DATA=BASE/'artifacts/derived/productive_continuity_20260907'
OUT=BASE/'reports/productive_continuity_20260907'
LABELS={'essential':'770 · servizi obbligatori','essential_renewal':'770 · servizi e rinnovo grano','wheat_deadline':'770 · scadenza grano (scartata)','wheat_safe':'770 · priorità biologiche (scartata)'}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[(s,t) for s in range(180903001,180903004) for t in (0,1)]
    oldpaths=[BASE/'artifacts/derived/assisted_770_complete_20260907'/f'{s}_{t}.json' for s,t in cases]
    old=[read(p) for p in oldpaths]
    top=read(TOP[0])['jesse']
    frozenpath=ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_28_C_TOP770_D01_D30_KPI_19.json'
    frozen=read(frozenpath)
    assert frozen['cohorts']['top770']['episodes']==[p['episode_id'] for p in top]
    summary={};groups={};files=list(oldpaths)+[TOP[0],frozenpath]
    for v in LABELS:
        paths=[DATA/f'{v}_{s}_{t}.json' for s,t in cases];files+=paths
        group=[read(p) for p in paths];groups[v]=group
    allgroups={'base':[dict(p,sides={'candidate':p['sides']['assisted'],'v4d':p['sides']['v4d']}) for p in old],**groups}
    for v,group in allgroups.items():
        candidate=[p['sides']['candidate'] for p in group]
        cash=mean(p['reward'] for p in candidate);reference=mean(p['sides']['v4d']['reward'] for p in group)
        summary[v]=dict(cash=cash,reference=reference,relative_pct=100*(cash/reference-1),
                        crop_deaths=sum(len(p['crop_starvation']) for p in candidate),animal_escapes=sum(len(p['ledger']['animal_escapes']) for p in candidate),
                        incomplete=sum(p.get('incomplete',p.get('incomplete_missions',0))>0 for p in group),
                        errors=sum(p.get('errors',p.get('core_errors',0)) for p in group),
                        wheat={str(d):median(p['daily'][d-1]['crops']['WHEAT'] for p in candidate) for d in [12,15,20,23,25,28,30]},
                        crops={str(d):median(p['daily'][d-1]['crop_tiles'] for p in candidate) for d in [12,15,20,23,25,28,30]},
                        wheat_replanted_d12_d25=mean(sum(f['planted'].get('WHEAT',0) for f in p['ledger']['daily'][11:25]) for p in candidate),
                        crop_days_d12_d25=mean(sum(r['crop_tiles'] for r in p['daily'][11:25]) for p in candidate))
    comparison='<div class="tablewrap"><table><tr><th>Stessi 6 casi locali</th><th>Base</th><th>Servizi obbligatori</th><th>Servizi + rinnovo</th><th>Scadenza grano (scartata)</th><th>Grano con priorità biologiche</th></tr>'
    for title,key in [('Cassa finale media','cash'),('Cassa V4D avversaria','reference'),('Scarto relativo V4D (%)','relative_pct'),('Somma coltivate D12–D25','crop_days_d12_d25'),('Semine grano D12–D25','wheat_replanted_d12_d25'),('Morti colture','crop_deaths'),('Fughe animali','animal_escapes'),('Casi con missioni residue','incomplete')]:
        comparison+='<tr><td>'+title+'</td>'+''.join('<td>'+fmt(summary[v][key])+'</td>' for v in allgroups)+'</tr>'
    for d in [12,15,20,23,25,28]:comparison+=f'<tr><td>Coltivate D{d}, mediana</td>'+''.join('<td>'+fmt(summary[v]['crops'][str(d)])+'</td>' for v in allgroups)+'</tr>'
    for d in [12,15,20,23,25,28]:comparison+=f'<tr><td>Grano D{d}, mediana</td>'+''.join('<td>'+fmt(summary[v]['wheat'][str(d)])+'</td>' for v in allgroups)+'</tr>'
    comparison+='</table></div>'
    diagnosis='''<h2>Che cosa abbiamo cambiato</h2><p>Sui 14 casi originali il grano spiega circa l’81% del divario medio di coltivate a D15 e D20 rispetto ai cinque Top001 (differenza delle medie per specie / differenza delle medie totali). Le prove sotto usano invece sei casi locali. Il grano è dunque la componente principale: la base interrompe la rotazione, mentre Top001 mantiene 23 caselle nella fase centrale. La prova della scadenza verifica la continuità del grano già presente; non impone una quota23 o copia coordinate del Top.</p><p>Il vecchio certificato della crescita richiedeva di inserire nei percorsi tutti i servizi osservati, inclusi raccolta, CARE e fertilizzazione facoltativi. La prima prova mantiene nel certificato ogni FEED e WATER richiesto, anche non ancora urgente; gli altri lavori restano proposti ed eseguibili nel pianificatore. Non vengono eliminate le verifiche del percorso della semina, le riserve di cassa o i limiti del profilo.</p><p>La terza prova assegna precedenza alla raccolta del grano arrivato al suo ultimo giorno di resa massima, conserva WATER prima di HARVEST e richiede quattro giorni per un nuovo ciclo completo. La terza prova ha causato quattro fughe animali ed è scartata. La quarta assegna alla scadenza economica un livello inferiore alle urgenze biologiche, mantenendo raccolta e risemina accoppiate.</p><p>La seconda prova aggiunge alla raccolta del grano PLANT WHEAT e WATER sulla stessa casella, quando restano almeno tre giorni e la cassa osservata copre la manutenzione più il seme. È un rinnovo legato allo stato della coltura, non una tabella di coordinate o date copiata dai Top.</p><p>La prima modifica testa se il certificato sovraccarico impediva l'espansione; la seconda testa la continuità delle rotazioni. Maggiore superficie non equivale a maggiore profitto: la tabella mostra anche V4D nelle stesse partite. Nessuna prova è promossa: il solo certificato essenziale aumenta la superficie ma peggiora il confronto economico; le prove di scadenza introducono perdite biologiche. La quarta registra due morti di colture e due fughe di animali nei sei casi. Le modifiche restano adattatori sperimentali locali. L'avvio D1–D11 è identico azione per azione alla candidata congelata.</p>'''
    for v,label in LABELS.items():
        ps=[p['sides']['candidate'] for p in groups[v]]
        payload=dict(topLabel='Top770-001',metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate(ps),top770=aggregate(top,frozen['series']['top770'])))
        filename=f'{v}_TOP770_D01_D30_COMPLETE_KPI'
        (OUT/f'{filename}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')
        a=template.index('<h2>Diagnosi</h2>');b=template.index('<details>',a)
        template=template[:a]+diagnosis+template[b:]
        template=template.replace('770 assistita V1',label).replace("candidate:'770 assistita'",f"candidate:{json.dumps(label)}")
        template=template.replace('Altro Top770','Altra prova').replace('Rigenerazione dei 14 run locali verificata contro tutti i KPI, ledger e risultati precedenti.','Sei casi per variante; 264 azioni iniziali identiche alla base, contabilità riconciliata e perdite biologiche verificate.')
        other='wheat_safe' if v!='wheat_safe' else 'essential'
        values={'TITLE':label+' vs Top770-001 · KPI D1–D30','COHORTS':'6 partite locali contro V4D · 5 replay storici Top770-001','OTHER':other+'_TOP770_D01_D30_COMPLETE_KPI.html','TOP':'Top770-001','ECONOMY':comparison,'PROVENANCE':'Esperimento '+v+'; semi 180903001–180903003, entrambe le posizioni. Top770-001: '+', '.join(str(p['episode_id']) for p in top)+'. Cassa e mercati esterni non comparabili come ranking.','DATAFILE':filename+'.json','DATA':json.dumps(payload,ensure_ascii=False).replace('</',r'<\/')}
        for key,value in values.items():template=template.replace('__'+key+'__',value)
        (OUT/f'{filename}.html').write_text(template,encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    files += [Path(__file__).with_name('wheat_safe_continuity.py'),Path(__file__).with_name('run_wheat_safe_continuity.py'),ROOT/'submission/submission_codex_e19_control_770_v2.py',Path(__file__).with_name('wheat_continuity.py'),Path(__file__).with_name('run_wheat_continuity.py'),Path(__file__),Path(__file__).with_name('productive_continuity.py'),Path(__file__).with_name('run_productive_continuity.py'),Path(__file__).with_name('complete_kpi_template.html')]
    (OUT/'manifest.json').write_text(json.dumps(dict(sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
