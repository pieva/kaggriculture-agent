"""Complete KPI report for measured succession experiments; no promotion implied."""
import json,re,hashlib,sys
from pathlib import Path
from statistics import mean,median
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate,FIELDS,TOP,fmt
from docs.model_specs.codex.e19.tools.build_succession_routes_770_report import inventory_loss
BASE=ROOT/'docs/model_specs/codex/e19';RAW=BASE/'artifacts/derived/portfolio_succession_20260907'
OUT=BASE/'reports/spent_renewal_770_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def table(headers,rows):
    return '<div class="tablewrap"><table><tr>'+''.join('<th>'+str(x)+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</table></div>'
def main():
    chosen=sys.argv[1] if len(sys.argv)>1 else 'v39'
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[(s,t) for s in range(180903001,180903004) for t in (0,1)]
    sourcepaths=[];groups={};summary={}
    for version in ['v33','v38','v39']:
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
    overview=table(['Sei casi per versione',*groups],[[label,*[fmt(summary[v][key]) for v in groups]] for label,key in [('Cassa media','cash'),('Cassa V4D avversaria','opponent_cash'),('Scarto relativo %','relative_pct'),('Morti idriche totali','water_deaths'),('Perdite animali totali','animal_losses'),('Vittorie contro V4D','wins'),('Perdite inventario, unità','inventory_loss'),('Casi ancora senza semine D21–D22','zero_sowing_cases'),('Infestanti mediane D30','weeds_D30'),('Chiamata più lenta, secondi','runtime_max_seconds'),('Overage massimo per partita, secondi','runtime_max_overage')]])
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
    for v in ['v33','v38','v39']:
        p=RAW/f'daily_routes_{v}_180903001_0.json'
        if not p.exists():continue
        sourcepaths.append(p);r=read(p)['sides']['candidate']
        screens.append([v,fmt(r['reward']),len(r['crop_starvation']),*[r['ledger']['daily'][d-1]['executed_actions'].get('PLANT',0) for d in [21,22]],r['daily'][22]['crops']['WHEAT']])
    overview+='<h2>Prove del meccanismo: solo seed 180903001, seat 0</h2>'+table(['Versione','Cassa','Morti idriche','Semine D21','Semine D22','Grano D23'],screens)
    base=summary['v33'];previous=summary['v38']
    diagnosis=f"""<h2>Rinnovo delle colture a fine ciclo: V39</h2>
<p>La V39 conserva il calendario idrico alternato della V38. Corregge l'esclusione dal rinnovo delle piante perenni già raccolte e giunte all'ultima produzione: possono ricevere DIG, PLANT e WATER nella stessa visita, senza un HARVEST vuoto. Il percorso ammette queste sostituzioni anche quando manca una visita ordinaria. Le produzioni future e il prodotto ancora presente sono protetti.</p>
<p>Quando una nuova fragola non arriverebbe alla prima produzione entro fine partita, il piano confronta grano e carote per margine corrente stimato per giorno, limitandosi a cicli con maturazione completa e un giorno residuo. Non è ancora una pianificazione della chiusura: i prezzi futuri non sono previsti e la selezione può favorire il grano. D26–D30 mantiene il precedente controllo.</p>
<p><strong>Sei casi V39:</strong> cassa media {fmt(new['cash'])}, contro {fmt(previous['cash'])} della V38 e {fmt(base['cash'])} della V33. Vittorie contro V4D: {new['wins']}/6; scarto medio relativo {fmt(new['relative_pct'])}%. Morti idriche: {new['water_deaths']}, contro {previous['water_deaths']} e {base['water_deaths']}. Coltivate mediane D25: {fmt(new['cultivated']['25'])}, contro {fmt(previous['cultivated']['25'])} e {fmt(base['cultivated']['25'])}. Infestanti mediane D30: {fmt(new['weeds_D30'])}, contro {fmt(previous['weeds_D30'])} e {fmt(base['weeds_D30'])}.</p>
<p>Il miglioramento di superficie va valutato insieme a PASS, MOVE, acqua, FEED, CARE, perdite e cassa. Le tabelle presentano tutte le fasi e tutti i casi; le fasce dei grafici sono minimi e massimi osservati, non intervalli di confidenza. Le infestanti comprendono anche fine ciclo, non soltanto morte per sete.</p>
<p>Prefisso D1–D11 identico, topologia 7–7–0, simulazioni complete, zero errori e missioni incomplete verificati. Quattro controlli mirati proteggono le produzioni future e l'ordine dei comandi. Sei casi già utilizzati nello sviluppo, tre semi nelle due posizioni: non costituiscono validazione indipendente. Il mercato condiviso modifica anche la cassa avversaria. Top770-001 è un corpus storico descrittivo, V33 e V38 usano gli stessi casi locali.</p>
<h2>Regressione da correggere: servizi animali</h2><p>V39 perde quattro animali complessivi, tutti a D23: uno per partita sui semi 180903001 e 180903003, in entrambe le posizioni. V33 e V38 ne perdevano zero. Le vittorie scendono da 6/6 della V38 a 4/6. Tra D21 e D25 FEED medio passa da 13,6 a 13,2 e CARE da 11,53 a 11; PLANT cresce da 3,27 a 6,67. Il rinnovo migliora il portafoglio ma non mantiene la copertura dei servizi. La fattibilita del percorso stimato non garantisce che venga poi eseguito: serve riservare ed eseguire i servizi animali prima di impegnare altra capacita nei rinnovi. Questa e una direzione di correzione, non una causa dimostrata con una prova isolata.</p><h2>Decisione</h2><p>V39 non sostituisce V38 o V33 a causa delle nuove perdite animali. Rimane un esperimento locale: nessuna promozione automatica o pubblicazione. V33 resta il riferimento e V29 la submission esterna. Occorre ancora valutare il portafoglio di chiusura e le perdite residue; 662 non modificata.</p>"""
    template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')
    template=re.sub(r'<h2>Diagnosi</h2>.*?<details>',diagnosis+'<details>',template,flags=re.S)
    template=re.sub(r'<p class="note">.*?</p>','<p class="note">Scadenze biologiche '+chosen.upper()+': servizio urgente, percorsi e produzione. <a href="__OTHER__">Altro confronto completo</a>.</p>',template,count=1,flags=re.S)
    template=template.replace('770 assistita V1',chosen.upper()).replace("candidate:'770 assistita'", "candidate:'"+chosen.upper()+"'").replace('7 settembre 2026','8 settembre 2026')
    template=template.replace('Stessi corpus storici già utilizzati; nessun nuovo benchmark esterno o invio di submission. Rigenerazione dei 14 run locali verificata contro tutti i KPI, ledger e risultati precedenti.','Sei simulazioni locali per versione completa. Prove preliminari su un caso riportate separatamente. Nessun invio esterno.')
    for suffix,label,ref,other in [('TOP770','Top770-001',aggregate(top,frozen),'V33'),('V33','V33 locale',aggregate(prof('v33')),'TOP770'),('V38','V38 locale',aggregate(prof('v38')),'TOP770')]:
        stem=f'{chosen}_{suffix}_D01_D30_COMPLETE_KPI'
        payload=dict(topLabel=label,metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate(prof(chosen)),top770=ref))
        vals=dict(TITLE=chosen.upper()+' vs '+label+' · KPI completi D1–D30',COHORTS='6 casi locali, semi 180903001–003, entrambe le posizioni',TOP=label,OTHER=f'{chosen}_{other}_D01_D30_COMPLETE_KPI.html',ECONOMY=overview,PROVENANCE='Prefisso D1–D11 e topologia verificati. Dati e sorgenti congelati nel manifest; V33, V38 e V39 sono confrontate sugli stessi sei casi. V33 è il riferimento locale scelto dall’utente; V29 resta la submission pubblicata.',DATAFILE=stem+'.json',DATA=json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
        result=template
        for k,v in vals.items():result=result.replace('__'+k+'__',v)
        assert not re.search(r'__[A-Z]+__',result) and not any(c in result for c in ['\u00c3','\u00c2','\ufffd'])
        (OUT/(stem+'.html')).write_text(result,encoding='utf-8');(OUT/(stem+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    sourcepaths += [TOP[0],frozenpath,Path(__file__),Path(__file__).with_name('complete_kpi_template.html'),BASE/'tests/test_renewal_certificate_v32.py',BASE/'tests/test_biological_water_calendar_v38.py',BASE/'tests/test_spent_renewal_v39.py']
    for rs in groups.values():
        for r in rs:
            for name,digest in r['sources'].items():
                p=ROOT/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
                sourcepaths.append(p)
    (OUT/'manifest.json').write_text(json.dumps(dict(chosen=chosen,status='LOCAL_EXPERIMENT_NOT_PROMOTED',sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sourcepaths},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
