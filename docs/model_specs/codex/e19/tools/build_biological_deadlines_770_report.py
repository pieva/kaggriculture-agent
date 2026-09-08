"""Complete KPI report for measured succession experiments; no promotion implied."""
import json,re,hashlib,sys
from pathlib import Path
from statistics import mean,median
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate,FIELDS,TOP,fmt
from docs.model_specs.codex.e19.tools.build_succession_routes_770_report import inventory_loss
BASE=ROOT/'docs/model_specs/codex/e19';RAW=BASE/'artifacts/derived/portfolio_succession_20260907'
OUT=BASE/'reports/biological_deadlines_770_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def table(headers,rows):
    return '<div class="tablewrap"><table><tr>'+''.join('<th>'+str(x)+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</table></div>'
def main():
    chosen=sys.argv[1] if len(sys.argv)>1 else 'v38'
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[(s,t) for s in range(180903001,180903004) for t in (0,1)]
    sourcepaths=[];groups={};summary={}
    for version in ['v33','v35','v38']:
        paths=[RAW/f'daily_routes_{version}_{s}_{t}.json' for s,t in cases]
        if not all(p.exists() for p in paths):continue
        sourcepaths+=paths
        rs=[read(p) for p in paths];groups[version]=rs
        assert all(r['prefix_parity'] and r['runtime']['complete'] and not r['runtime']['backend_statuses'] and r['errors']==0 and r['incomplete']==0 for r in rs)
        for r in rs:
            for d in r['sides']['candidate']['daily'][11:]:assert d['pasture_topology']=={'Q0':7,'Q1':7,'Q2':0,'Q3':0}
        ps=[r['sides']['candidate'] for r in rs]
        cash=mean(p['reward'] for p in ps);opp=mean(r['sides']['v4d']['reward'] for r in rs)
        summary[version]=dict(cash=cash,opponent_cash=opp,relative_pct=100*(cash/opp-1),wins=sum(r['sides']['candidate']['reward']>r['sides']['v4d']['reward'] for r in rs),
            water_deaths=sum(len(p['crop_starvation']) for p in ps),animal_losses=sum(d['verified_animal_losses'] for p in ps for d in p['operational_daily']),inventory_loss=sum(sum(inventory_loss(p).values()) for p in ps),
            wheat={str(d):median(p['daily'][d-1]['crops']['WHEAT'] for p in ps) for d in range(20,26)},
            cultivated={str(d):median(p['daily'][d-1]['crop_tiles'] for p in ps) for d in range(20,26)},
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
    overview+='<h2>Confronto diretto con V4D</h2>'+table(['Versione','Seed','Seat','Cassa candidata','Cassa V4D','Delta','Esito'],[[v,r['seed'],r['seat'],fmt(r['sides']['candidate']['reward']),fmt(r['sides']['v4d']['reward']),fmt(r['sides']['candidate']['reward']-r['sides']['v4d']['reward']),'Vittoria' if r['sides']['candidate']['reward']>r['sides']['v4d']['reward'] else 'Sconfitta'] for v,rs in groups.items() for r in rs])
    screens=[]
    for v in ['v33','v34','v35','v36','v37','v38']:
        p=RAW/f'daily_routes_{v}_180903001_0.json'
        if not p.exists():continue
        sourcepaths.append(p);r=read(p)['sides']['candidate']
        screens.append([v,fmt(r['reward']),len(r['crop_starvation']),*[r['ledger']['daily'][d-1]['executed_actions'].get('PLANT',0) for d in [21,22]],r['daily'][22]['crops']['WHEAT']])
    overview+='<h2>Prove del meccanismo: solo seed 180903001, seat 0</h2>'+table(['Versione','Cassa','Morti idriche','Semine D21','Semine D22','Grano D23'],screens)
    diagnosis=f"""<h2>Proteggere i servizi senza abbandonare la produzione</h2>
<p>Partenza dalla V33. La V34 dà precedenza assoluta a WATER/FEED in scadenza e consente il recupero fuori area fin dal mattino. Nel caso preliminare azzera le morti idriche ma riduce fortemente superficie e cassa: il miglioramento di un solo KPI non basta. Rimane una prova su un caso, non una revisione promossa.</p>
<p>La V35 conserva le aree assegnate. Per ogni servizio in scadenza stima quando l'addetto lo raggiungerà, includendo missione attiva, spostamenti, prelievi e visite che lo precedono nella coda. Se la stima raggiunge o supera il tempo residuo, il servizio può essere recuperato da un altro lavoratore. Resta il precedente recupero nelle ultime sei ore. Acqua e cibo in scadenza ricevono precedenza sulle nuove coltivazioni.</p>
<p>La V36 assegna precedenza anche alla visita completa che contiene il servizio urgente: acqua, raccolta e gli altri comandi già previsti vengono conservati insieme. Il servizio breve rimane disponibile come alternativa. L'obiettivo è evitare di risparmiare una pianta al prezzo di due viaggi e di una raccolta persa.</p>
<p><strong>{chosen.upper()}, sei casi:</strong> cassa media {fmt(new['cash'])}, V4D avversaria {fmt(new['opponent_cash'])}, scarto relativo {fmt(new['relative_pct'])}%. Morti idriche {new['water_deaths']}, perdite animali {new['animal_losses']}, perdite inventario {new['inventory_loss']} unità. Infestanti mediane D30: {fmt(new['weeds_D30'])}. Casi senza semine in entrambi D21–D22: {new['zero_sowing_cases']}/6. Grano mediano D20–D25: {', '.join(fmt(x) for x in new['wheat'].values())}.</p>
<p>Il confronto va letto su tutte le colonne: cassa propria e avversaria, coltivate, fragole, grano, carote, MOVE, PASS, WATER, FEED e CARE. Il mercato è condiviso: produrre e vendere diversamente modifica anche i risultati di V4D. Una crescita della sola cassa non dimostra maggiore competitività.</p>
<p>La previsione del ritardo è una stima sul piano corrente, non una garanzia multigiorno. Le infestanti possono derivare da sete oppure dalla fine del ciclo: lo stock finale non equivale al numero di morti idriche. D26–D30 conserva la chiusura precedente; il calendario dedicato delle carote resta aperto.</p>
<p>Verificati prefisso D1–D11 identico, topologia 7–7–0, 719 chiamate e 720 stati per partita, assenza di errori e missioni incomplete. Tempi misurati localmente con simulazioni concorrenti, non su Kaggle. Sei casi già usati nello sviluppo: nessuna validazione indipendente o nuova submission. Solo 770; 662 non modificata.</p>"""
    diagnosis+='<h2>Prevenzione nel calendario: V38</h2><p>La V37 restringe la priorità speciale ai servizi stimati in ritardo, ma il caso preliminare non migliora l’economia. La V38 riparte invece dalle priorità della V33 e aggiunge un appuntamento alternato per l’acqua delle fragole: due gruppi definiti dalla parità di riga e colonna si alternano ogni giorno. Restano obbligatori i servizi già richiesti per sopravvivenza o fertilizzazione. Non è una scelta casuale, non usa coordinate del Top e non presume manodopera futura. Il calendario opera da D12 a D25; l’acqua viene integrata nella visita ordinaria già prevista.</p>'
    base=summary['v33']
    diagnosis+=f'<p><strong>Confronto completo {chosen.upper()} / V33:</strong> cassa media {fmt(new["cash"])} / {fmt(base["cash"])}, scarto competitivo {fmt(new["relative_pct"])}% / {fmt(base["relative_pct"])}%, morti idriche {new["water_deaths"]} / {base["water_deaths"]}. Coltivate mediane D23: {fmt(new["cultivated"]["23"])} / {fmt(base["cultivated"]["23"])}; D25: {fmt(new["cultivated"]["25"])} / {fmt(base["cultivated"]["25"])}. Le regressioni della superficie restano visibili anche quando la cassa migliora. Questo è un esperimento locale e non una versione pubblicata.</p>'
    diagnosis+=f'<h2>Decisione</h2><p>{chosen.upper()}: {new["wins"]}/6 vittorie contro V4D, rispetto a {base["wins"]}/6 della V33. Il miglioramento competitivo e la minore mortalità rendono il calendario alternato un candidato da approfondire; non cancellano il calo della cassa e della superficie. Manteniamo V33 come riferimento, V38 come esperimento sulla prevenzione. Nessuna promozione o pubblicazione. Il prossimo intervento deve integrare questo carico di acqua con il rinnovo delle fragole e delle caselle liberate a D22–D25, prima di giudicare la chiusura.</p>'
    template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')
    template=re.sub(r'<h2>Diagnosi</h2>.*?<details>',diagnosis+'<details>',template,flags=re.S)
    template=re.sub(r'<p class="note">.*?</p>','<p class="note">Scadenze biologiche '+chosen.upper()+': servizio urgente, percorsi e produzione. <a href="__OTHER__">Altro confronto completo</a>.</p>',template,count=1,flags=re.S)
    template=template.replace('770 assistita V1',chosen.upper()).replace("candidate:'770 assistita'", "candidate:'"+chosen.upper()+"'").replace('7 settembre 2026','8 settembre 2026')
    template=template.replace('Stessi corpus storici già utilizzati; nessun nuovo benchmark esterno o invio di submission. Rigenerazione dei 14 run locali verificata contro tutti i KPI, ledger e risultati precedenti.','Sei simulazioni locali per versione completa. Prove preliminari su un caso riportate separatamente. Nessun invio esterno.')
    for suffix,label,ref,other in [('TOP770','Top770-001',aggregate(top,frozen),'V33'),('V33','V33 locale',aggregate(prof('v33')),'TOP770')]:
        stem=f'{chosen}_{suffix}_D01_D30_COMPLETE_KPI'
        payload=dict(topLabel=label,metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate(prof(chosen)),top770=ref))
        vals=dict(TITLE=chosen.upper()+' vs '+label+' · KPI completi D1–D30',COHORTS='6 casi locali, semi 180903001–003, entrambe le posizioni',TOP=label,OTHER=f'{chosen}_{other}_D01_D30_COMPLETE_KPI.html',ECONOMY=overview,PROVENANCE='Prefisso D1–D11 e topologia verificati. Dati e sorgenti congelati nel manifest; V34 è confrontata su un solo caso. V33 è il riferimento locale scelto dall’utente; V29 resta la submission pubblicata.',DATAFILE=stem+'.json',DATA=json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
        result=template
        for k,v in vals.items():result=result.replace('__'+k+'__',v)
        assert not re.search(r'__[A-Z]+__',result) and not any(c in result for c in ['\u00c3','\u00c2','\ufffd'])
        (OUT/(stem+'.html')).write_text(result,encoding='utf-8');(OUT/(stem+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    sourcepaths += [TOP[0],frozenpath,Path(__file__),Path(__file__).with_name('complete_kpi_template.html'),BASE/'tests/test_renewal_certificate_v32.py',BASE/'tests/test_biological_water_calendar_v38.py']
    for rs in groups.values():
        for r in rs:
            for name,digest in r['sources'].items():
                p=ROOT/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
                sourcepaths.append(p)
    (OUT/'manifest.json').write_text(json.dumps(dict(chosen=chosen,status='LOCAL_EXPERIMENT_NOT_PROMOTED',sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sourcepaths},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
