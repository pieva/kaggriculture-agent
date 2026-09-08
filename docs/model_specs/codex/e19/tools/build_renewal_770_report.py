"""Complete KPI report for measured succession experiments; no promotion implied."""
import json,re,hashlib,sys
from pathlib import Path
from statistics import mean,median
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate,FIELDS,TOP,fmt
from docs.model_specs.codex.e19.tools.build_succession_routes_770_report import inventory_loss
BASE=ROOT/'docs/model_specs/codex/e19';RAW=BASE/'artifacts/derived/portfolio_succession_20260907'
OUT=BASE/'reports/renewal_certificate_770_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def table(headers,rows):
    return '<div class="tablewrap"><table><tr>'+''.join('<th>'+str(x)+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</table></div>'
def main():
    chosen=sys.argv[1] if len(sys.argv)>1 else 'v32'
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[(s,t) for s in range(180903001,180903004) for t in (0,1)]
    sourcepaths=[];groups={};summary={}
    for version in ['v29','v32','v33']:
        paths=[RAW/f'daily_routes_{version}_{s}_{t}.json' for s,t in cases]
        if not all(p.exists() for p in paths):continue
        sourcepaths+=paths
        rs=[read(p) for p in paths];groups[version]=rs
        assert all(r['prefix_parity'] and r['runtime']['complete'] and not r['runtime']['backend_statuses'] and r['errors']==0 and r['incomplete']==0 for r in rs)
        for r in rs:
            for d in r['sides']['candidate']['daily'][11:]:assert d['pasture_topology']=={'Q0':7,'Q1':7,'Q2':0,'Q3':0}
        ps=[r['sides']['candidate'] for r in rs]
        cash=mean(p['reward'] for p in ps);opp=mean(r['sides']['v4d']['reward'] for r in rs)
        summary[version]=dict(cash=cash,opponent_cash=opp,relative_pct=100*(cash/opp-1),
            water_deaths=sum(len(p['crop_starvation']) for p in ps),animal_losses=sum(d['verified_animal_losses'] for p in ps for d in p['operational_daily']),inventory_loss=sum(sum(inventory_loss(p).values()) for p in ps),
            wheat={str(d):median(p['daily'][d-1]['crops']['WHEAT'] for p in ps) for d in range(20,26)},
            planted={str(d):mean(p['ledger']['daily'][d-1]['executed_actions'].get('PLANT',0) for p in ps) for d in range(20,26)},
            zero_sowing_cases=sum(all(p['ledger']['daily'][d-1]['executed_actions'].get('PLANT',0)==0 for d in [21,22]) for p in ps),
            weeds_D30=median(p['operational_daily'][29]['weed_tiles'] for p in ps),
            runtime_max_seconds=max(r['runtime']['max_seconds'] for r in rs),runtime_max_overage=max(r['runtime']['overage_seconds'] for r in rs))
    assert chosen in groups
    def prof(v):return [r['sides']['candidate'] for r in groups[v]]
    top=read(TOP[0])['jesse'];frozenpath=ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_28_C_TOP770_D01_D30_KPI_19.json'
    frozen=read(frozenpath)['series']['top770'];new=summary[chosen]
    overview=table(['Sei casi per versione',*groups],[[label,*[fmt(summary[v][key]) for v in groups]] for label,key in [('Cassa media','cash'),('Cassa V4D avversaria','opponent_cash'),('Scarto relativo %','relative_pct'),('Morti idriche totali','water_deaths'),('Perdite inventario, unità','inventory_loss'),('Casi ancora senza semine D21–D22','zero_sowing_cases'),('Infestanti mediane D30','weeds_D30'),('Chiamata più lenta, secondi','runtime_max_seconds'),('Overage massimo per partita, secondi','runtime_max_overage')]])
    phase=[]
    for a,b in [(12,20),(21,25),(26,30)]:
        for key in ['crop_tiles','WHEAT','STRAWBERRY','CARROT','MOVE','PASS','WATER','FEED','CARE','weed_tiles']:
            values=[]
            for v in groups:
                vals=[]
                for p in prof(v):
                    for d in range(a-1,b):
                        if key=='crop_tiles':value=p['daily'][d][key]
                        elif key in ['WHEAT','STRAWBERRY','CARROT']:value=p['daily'][d]['crops'][key]
                        elif key in ['MOVE','PASS','weed_tiles']:value=p['operational_daily'][d][key]
                        else:value=p['ledger']['daily'][d]['executed_actions'].get(key,0)
                        vals.append(value)
                values.append(fmt(mean(vals)))
            phase.append([f'D{a}–D{b}',key,*values])
    overview+='<h2>Portafoglio e persone: medie per giorno e partita</h2>'+table(['Finestra','KPI',*groups],phase)
    overview+='<h2>Semine e grano D20–D25</h2>'+table(['Giorno','KPI',*groups],[[f'D{d}',k,*[fmt(summary[v][k][str(d)]) for v in groups]] for d in range(20,26) for k in ['wheat','planted']])
    games=[]
    for idx,(seed,seat) in enumerate(cases):
        games.append([seed,seat,*[fmt(groups[v][idx]['sides']['candidate']['reward']) for v in groups]])
    overview+='<h2>Cassa per caso</h2>'+table(['Seed','Seat',*groups],games)
    screens=[]
    for v in ['v29','v30','v31','v32','v33']:
        p=RAW/f'daily_routes_{v}_180903001_0.json'
        if not p.exists():continue
        sourcepaths.append(p);r=read(p)['sides']['candidate']
        screens.append([v,fmt(r['reward']),len(r['crop_starvation']),*[r['ledger']['daily'][d-1]['executed_actions'].get('PLANT',0) for d in [21,22]],r['daily'][22]['crops']['WHEAT']])
    overview+='<h2>Prove del meccanismo: solo seed 180903001, seat 0</h2>'+table(['Versione','Cassa','Morti idriche','Semine D21','Semine D22','Grano D23'],screens)
    diagnosis=f'''<h2>Conclusione della prova {chosen.upper()}</h2><p>La continuità va valutata sulle azioni reali: casi ancora senza semine in entrambi D21–D22: <strong>{new['zero_sowing_cases']}/6</strong>. Il grano mediano D20–D25 è {', '.join(fmt(x) for x in new['wheat'].values())}. Cassa media {fmt(new['cash'])}, contro {fmt(new['opponent_cash'])} di V4D nelle stesse partite.</p>
<p><strong>La sola fusione raccolta–risemina non risolveva il problema.</strong> V30 introduce la visita composta, lasciando disponibile la raccolta urgente da sola. V31 applica a entrambe la stessa eccezione all'assegnazione per area. Nel caso di diagnosi V31 le 298 valutazioni di nuovi lavori a D21–D22 sono tutte respinte: 294 rotazioni e 4 nuove colture. Anche le visite di cinque azioni proposte a inizio giornata non ottengono il certificato.</p>
<p><strong>V32 interviene sul calcolo della capacità.</strong> Dopo il rifiuto del controllo precedente prova l'inserimento degli obblighi di FEED/WATER nei percorsi, con posizioni, inventari e persone osservati. Sottrae tutti i passi delle missioni già impegnate e il prelievo degli input. Non tratta le proposte su terreno vuoto come colture già presenti. Il rinnovo conserva PLANT e WATER; se non è certificabile, resta disponibile la raccolta da sola. La ricerca è limitata deterministicamente per batch. V33 aggiunge anche il tempo dei CARE al controllo alternativo.</p>
<p><strong>Limiti e regressioni restano espliciti.</strong> Morti idriche {new['water_deaths']}, perdite inventario {new['inventory_loss']} unità, infestanti mediane finali {fmt(new['weeds_D30'])}. Una successione migliore non implica una gestione biologica risolta. Il certificato è un piano fattibile per oggi: non garantisce che i successivi ricalcoli e le missioni discrezionali lo seguano integralmente. Non prenota ancora l'intero ciclo futuro.</p>
<p>D1–D11 è identico al prefisso congelato in tutti i sei casi; topologia 7–7–0 verificata da D12, 719 chiamate e 720 stati per partita, nessun errore o missione incompleta. D26–D30 mantiene il precedente selettore di chiusura: la successione dedicata alle carote rimane da integrare. Nessuna modifica alla 662 e nessun invio esterno.</p>
<p><strong>Stato: esperimento locale, non promosso a nuova submission.</strong> I sei casi sono già usati nello sviluppo; non sono un holdout indipendente. Il mercato è condiviso: riportiamo anche la cassa V4D perché può cambiare con la nostra produzione. Il confronto con Top770 è descrittivo, su un corpus storico diverso.</p>'''
    if 'v33' in summary:
        diagnosis+='<h2>Scelta per il prossimo lavoro</h2><p>V32 massimizza la cassa in questo campione: 92.755, scarto contro V4D +0,92%, ma conserva 54 morti idriche. V33 porta la cassa a 89.624, scarto −2,46%, e riduce le morti a 42; le infestanti finali mediane scendono a 22,5. La V33 è il ramo da approfondire per coordinare i servizi, mantenendo V32 come controllo del costo della maggiore protezione. Nessuna è ancora un riferimento validato per la pubblicazione.</p><p>Nella V32 le morti non spariscono: 24 sono attribuite al servizio D16, 6 a D22, 20 a D23 e 4 a D25. La prossima correzione deve quindi far rispettare le prenotazioni dei servizi durante l’esecuzione, soprattutto sulle fragole; aumentare soltanto la priorità della semina non è sufficiente. I tempi massimi riportati sono misure locali con simulazioni concorrenti, non misure di latenza Kaggle.</p>'
    template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')
    template=re.sub(r'<h2>Diagnosi</h2>.*?<details>',diagnosis+'<details>',template,flags=re.S)
    template=re.sub(r'<p class="note">.*?</p>','<p class="note">Successione certificata '+chosen.upper()+': visita raccolta–risemina e controllo dei percorsi. <a href="__OTHER__">Altro confronto completo</a>.</p>',template,count=1,flags=re.S)
    template=template.replace('770 assistita V1',chosen.upper()).replace("candidate:'770 assistita'", "candidate:'"+chosen.upper()+"'").replace('7 settembre 2026','8 settembre 2026')
    template=template.replace('Stessi corpus storici già utilizzati; nessun nuovo benchmark esterno o invio di submission. Rigenerazione dei 14 run locali verificata contro tutti i KPI, ledger e risultati precedenti.','Sei simulazioni locali per versione completa. Prove preliminari su un caso riportate separatamente. Nessun invio esterno.')
    for suffix,label,ref,other in [('TOP770','Top770-001',aggregate(top,frozen),'V29'),('V29','V29 locale',aggregate(prof('v29')),'TOP770')]:
        stem=f'{chosen}_{suffix}_D01_D30_COMPLETE_KPI'
        payload=dict(topLabel=label,metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate(prof(chosen)),top770=ref))
        vals=dict(TITLE=chosen.upper()+' vs '+label+' · KPI completi D1–D30',COHORTS='6 casi locali, semi 180903001–003, entrambe le posizioni',TOP=label,OTHER=f'{chosen}_{other}_D01_D30_COMPLETE_KPI.html',ECONOMY=overview,PROVENANCE='Prefisso D1–D11 e topologia verificati. Dati e sorgenti congelati nel manifest; le prove V30 e V31 sono confrontate su un solo caso. V29 è la versione pubblicata, riesaminata qui sul corpus locale.',DATAFILE=stem+'.json',DATA=json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
        result=template
        for k,v in vals.items():result=result.replace('__'+k+'__',v)
        assert not re.search(r'__[A-Z]+__',result) and not any(c in result for c in ['\u00c3','\u00c2','\ufffd'])
        (OUT/(stem+'.html')).write_text(result,encoding='utf-8');(OUT/(stem+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    sourcepaths += [TOP[0],frozenpath,Path(__file__),Path(__file__).with_name('complete_kpi_template.html'),ROOT/'scratch/diagnose_v29_succession.py',ROOT/'scratch/v29_succession_diagnosis.json',ROOT/'scratch/run_v31_diagnostic.py',RAW/'daily_routes_v31_diagnostic_180903001_0.json',BASE/'tests/test_renewal_certificate_v32.py']
    for rs in groups.values():
        for r in rs:
            for name,digest in r['sources'].items():
                p=ROOT/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
                sourcepaths.append(p)
    (OUT/'manifest.json').write_text(json.dumps(dict(chosen=chosen,status='LOCAL_EXPERIMENT_NOT_PROMOTED',sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sourcepaths},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
