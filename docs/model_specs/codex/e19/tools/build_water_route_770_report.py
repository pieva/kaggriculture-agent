"""Complete KPI report for measured succession experiments; no promotion implied."""
import json,re,hashlib,sys
from pathlib import Path
from statistics import mean,median
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate,FIELDS,TOP,fmt
from docs.model_specs.codex.e19.tools.build_succession_routes_770_report import inventory_loss
BASE=ROOT/'docs/model_specs/codex/e19';RAW=BASE/'artifacts/derived/portfolio_succession_20260907'
OUT=BASE/'reports/water_route_770_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def table(headers,rows):
    return '<div class="tablewrap"><table><tr>'+''.join('<th>'+str(x)+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</table></div>'
def main():
    chosen=sys.argv[1] if len(sys.argv)>1 else 'v44'
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[(s,t) for s in range(180903001,180903004) for t in (0,1)]
    sourcepaths=[];groups={};summary={}
    for version in ['v33','v38','v39','v41','v44']:
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
        for key in ['crop_tiles','WHEAT','STRAWBERRY','CARROT','MOVE','PASS','WATER','FEED','CARE','weed_tiles','unwatered_tiles_h24','water_stressed_tiles_h24']:
            values=[]
            for v in groups:
                vals=[]
                for p in prof(v):
                    for d in range(a-1,b):
                        if key=='crop_tiles':value=p['daily'][d][key]
                        elif key in ['WHEAT','STRAWBERRY','CARROT']:value=p['daily'][d]['crops'][key]
                        elif key in ['MOVE','PASS','weed_tiles','unwatered_tiles_h24','water_stressed_tiles_h24']:value=p['operational_daily'][d][key]
                        else:value=p['ledger']['daily'][d]['executed_actions'].get(key,0)
                        vals.append(value)
                values.append(fmt(mean(vals)))
            phase.append([f'D{a}–D{b}',key,*values])
    overview+='<h2>Portafoglio e persone: medie per giorno e partita</h2><p>unwatered_tiles_h24 conta le piante non irrigate al checkpoint; water_stressed_tiles_h24 conta il flag consecutive_unwatered positivo. Quest’ultimo ricorda lo stress del giorno precedente anche se la pianta ha ricevuto acqua oggi: non misura da solo il rischio residuo. I checkpoint D1–D29 precedono l’ultimo batch, D30 e terminale.</p>'+table(['Finestra','KPI',*groups],phase)
    overview+='<h2>Semine e grano D20–D25</h2>'+table(['Giorno','KPI',*groups],[[f'D{d}',k,*[fmt(summary[v][k][str(d)]) for v in groups]] for d in range(20,26) for k in ['wheat','planted']])
    games=[]
    for idx,(seed,seat) in enumerate(cases):
        games.append([seed,seat,*[fmt(groups[v][idx]['sides']['candidate']['reward']) for v in groups]])
    overview+='<h2>Cassa per caso</h2>'+table(['Seed','Seat',*groups],games)
    overview+='<h2>Confronto diretto con V4D</h2>'+table(['Versione','Seed','Seat','Cassa candidata','Cassa V4D','Delta','Esito'],[[v,r['seed'],r['seat'],fmt(r['sides']['candidate']['reward']),fmt(r['sides']['v4d']['reward']),fmt(r['sides']['candidate']['reward']-r['sides']['v4d']['reward']),'Vittoria' if r['sides']['candidate']['reward']>r['sides']['v4d']['reward'] else 'Sconfitta'] for v,rs in groups.items() for r in rs])
    screens=[]
    for v in ['v41','v42','v43','v44']:
        p=RAW/f'daily_routes_{v}_180903001_0.json'
        if not p.exists():continue
        sourcepaths.append(p)
        screen=read(p)
        for name,digest in screen['sources'].items():
            dep=ROOT/name
            assert hashlib.sha256(dep.read_bytes()).hexdigest()==digest,name
            sourcepaths.append(dep)
        r=screen['sides']['candidate']
        screens.append([v,fmt(r['reward']),len(r['crop_starvation']),sum(d['verified_animal_losses'] for d in r['operational_daily']),*[r['ledger']['daily'][d-1]['executed_actions'].get('PLANT',0) for d in [21,22]],r['daily'][22]['crops']['WHEAT']])
    overview+='<h2>Prove del meccanismo: solo seed 180903001, seat 0</h2>'+table(['Versione','Cassa','Morti idriche','Perdite animali','Semine D21','Semine D22','Grano D23'],screens)
    base=summary['v41']
    diagnosis=f"""<h2>Copertura idrica e recupero del percorso</h2>
<p>La V41 protegge le visite animali a rischio e azzera le fughe, ma registra 26 perdite idriche sui sei casi. La V42 estende la precedenza di percorso e selezione alle colture gia rimaste un giorno senza acqua, mantenendo la visita completa. Nel caso preliminare azzera tutte le perdite, ma riduce superficie e competitivita: resta una prova su un solo caso.</p>
<p>La V43 conserva priorita e pianificazione V41. Per una coltura a rischio stima il completamento della visita dell'addetto assegnato, includendo missione attiva, tragitto, servizi precedenti e prelievi. Se il tempo stimato raggiunge il residuo meno due turni, oppure manca un addetto assegnato, permette il recupero fuori area. Non alza la priorita di tutte le irrigazioni e non considera l'acqua delle nuove semine un debito idrico esistente. La stima puo sovrastimare prelievi coperti dalla missione attiva; non e una garanzia di esecuzione.</p>
<p>La V43 e anch'essa una prova su un caso, non una versione promossa. La V44 torna alla V41 e corregge la coda: un servizio esistente puo essere candidato oltre una semina o un rinnovo non ancora ammesso. L'ordine fra servizi esistenti e la precedenza delle missioni ammissibili restano invariati. Non modifica le priorita, il recupero fuori area o il calendario idrico della V41. Il filtro e temporaneo durante la preparazione dell'alternativa, non cancella il rinnovo dal piano.</p><p><strong>{chosen.upper()}, sei casi:</strong> cassa media {fmt(new['cash'])} contro {fmt(base['cash'])} V41, vittorie {new['wins']}/6 contro {base['wins']}/6. Perdite animali {new['animal_losses']} contro {base['animal_losses']}; perdite idriche {new['water_deaths']} contro {base['water_deaths']}. Coltivate mediane D25 {fmt(new['cultivated']['25'])} contro {fmt(base['cultivated']['25'])}; infestanti mediane D30 {fmt(new['weeds_D30'])} contro {fmt(base['weeds_D30'])}.</p>
<p>Tutte le fasi includono FEED, CARE, WATER, MOVE, PASS, portafoglio e semine. Il margine sulla cassa avversaria e distinto dalle vittorie. Tre semi di sviluppo nelle due posizioni: non sono sei semi indipendenti. Top770-001 e un corpus storico descrittivo; i confronti locali usano gli stessi casi. Le fasce rappresentano min-max osservati.</p>
<p>Prefisso D1–D11, topologia 7–7–0 e completamento delle partite verificati, nessun errore o missione incompleta. D26–D30 conserva la chiusura precedente. Solo 770, nessuna submission. V33 resta riferimento, V29 pubblicata. Sorgenti e dati verificati con SHA256.</p>
<h2>Valutazione: V44 non promossa</h2><p>La correzione della coda migliora WATER medio D21–D25 da 29,47 a 33,47, FEED da 13,53 a 13,73 e PLANT da 6 a 6,47; MOVE scende da 161 a 158,87 e PASS da 19,2 a 17,53. CARE peggiora da 12,2 a 11,8. Le infestanti mediane D30 salgono da 20 a 26,5, nonostante la minore mortalita idrica: i due indicatori non sono equivalenti.</p>
<p>La cassa media V41/V44 e 37.239/36.702 a D20, 66.631/64.440 a D25 e 94.704/87.725 al termine. Il divario di circa 2.190 al checkpoint D25 si amplia a circa 6.980 al termine. Questo localizza una parte rilevante del peggioramento nella fase finale, ma non ne identifica da solo la causa: il mercato e condiviso e i checkpoint D25 precedono l'ultimo batch. Non basta correggere il calendario dell'acqua per assicurare la conversione del portafoglio in cassa.</p>
<p>V44 vince 4/6 casi contro 6/6 della V41 e lo scarto relativo medio passa dal 3,66% all'1,25%. Manteniamo V41 come confronto operativo migliore di questa prova, senza promuovere o pubblicare V44. Il meccanismo della coda e verificato, ma va integrato con raccolte, rinnovi e chiusura: piu caselle coltivate non garantiscono maggiore rendimento economico.</p>"""
    template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')
    template=re.sub(r'<h2>Diagnosi</h2>.*?<details>',diagnosis+'<details>',template,flags=re.S)
    template=re.sub(r'<p class="note">.*?</p>','<p class="note">Scadenze biologiche '+chosen.upper()+': servizio urgente, percorsi e produzione. <a href="__OTHER__">Altro confronto completo</a>.</p>',template,count=1,flags=re.S)
    template=template.replace('770 assistita V1',chosen.upper()).replace("candidate:'770 assistita'", "candidate:'"+chosen.upper()+"'").replace('7 settembre 2026','8 settembre 2026')
    template=template.replace('Stessi corpus storici già utilizzati; nessun nuovo benchmark esterno o invio di submission. Rigenerazione dei 14 run locali verificata contro tutti i KPI, ledger e risultati precedenti.','Sei simulazioni locali per versione completa. Prove preliminari su un caso riportate separatamente. Nessun invio esterno.')
    for suffix,label,ref,other in [('TOP770','Top770-001',aggregate(top,frozen),'V33'),('V33','V33 locale',aggregate(prof('v33')),'TOP770'),('V38','V38 locale',aggregate(prof('v38')),'TOP770'),('V39','V39 locale',aggregate(prof('v39')),'TOP770'),('V41','V41 locale',aggregate(prof('v41')),'TOP770')]:
        stem=f'{chosen}_{suffix}_D01_D30_COMPLETE_KPI'
        payload=dict(topLabel=label,metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate(prof(chosen)),top770=ref))
        vals=dict(TITLE=chosen.upper()+' vs '+label+' · KPI completi D1–D30',COHORTS='6 casi locali, semi 180903001–003, entrambe le posizioni',TOP=label,OTHER=f'{chosen}_{other}_D01_D30_COMPLETE_KPI.html',ECONOMY=overview,PROVENANCE='Prefisso D1–D11 e topologia verificati. Dati e sorgenti congelati nel manifest; V33, V38 e V39 sono confrontate sugli stessi sei casi. V33 è il riferimento locale scelto dall’utente; V29 resta la submission pubblicata.',DATAFILE=stem+'.json',DATA=json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
        result=template
        for k,v in vals.items():result=result.replace('__'+k+'__',v)
        assert not re.search(r'__[A-Z]+__',result) and not any(c in result for c in ['\u00c3','\u00c2','\ufffd'])
        (OUT/(stem+'.html')).write_text(result,encoding='utf-8');(OUT/(stem+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    sourcepaths += [TOP[0],frozenpath,Path(__file__),Path(__file__).with_name('complete_kpi_template.html'),BASE/'tests/test_renewal_certificate_v32.py',BASE/'tests/test_biological_water_calendar_v38.py',BASE/'tests/test_spent_renewal_v39.py',BASE/'tests/test_protected_routes_v40.py',BASE/'tests/test_biological_protection_v42.py',BASE/'tests/test_water_route_rescue_v43.py',BASE/'tests/test_provisional_queue_v44.py']
    for rs in groups.values():
        for r in rs:
            for name,digest in r['sources'].items():
                p=ROOT/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
                sourcepaths.append(p)
    (OUT/'manifest.json').write_text(json.dumps(dict(chosen=chosen,status='LOCAL_EXPERIMENT_NOT_PROMOTED',sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sourcepaths},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
