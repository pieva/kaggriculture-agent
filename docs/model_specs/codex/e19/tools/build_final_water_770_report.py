"""Complete KPI report for measured succession experiments; no promotion implied."""
import json,re,hashlib,sys
from pathlib import Path
from statistics import mean,median
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate,FIELDS,TOP,fmt
from docs.model_specs.codex.e19.tools.build_succession_routes_770_report import inventory_loss
BASE=ROOT/'docs/model_specs/codex/e19';RAW=BASE/'artifacts/derived/portfolio_succession_20260907'
OUT=BASE/'reports/final_water_770_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def table(headers,rows):
    return '<div class="tablewrap"><table><tr>'+''.join('<th>'+str(x)+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</table></div>'
def main():
    chosen=sys.argv[1] if len(sys.argv)>1 else 'v47'
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[(s,t) for s in range(180903001,180903004) for t in (0,1)]
    sourcepaths=[];groups={};summary={}
    for version in ['v33','v38','v39','v41','v44','v45','v46','v47']:
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
    for old,newrun in zip(groups['v45'],groups[chosen]):
        for key in ['daily','operational_daily']:
            assert old['sides']['candidate'][key][:27]==newrun['sides']['candidate'][key][:27],key
        assert old['sides']['candidate']['ledger']['daily'][:27]==newrun['sides']['candidate']['ledger']['daily'][:27],'D1-D27 ledger'

    def prof(v):return [r['sides']['candidate'] for r in groups[v]]
    top=read(TOP[0])['jesse'];frozenpath=ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_28_C_TOP770_D01_D30_KPI_19.json'
    frozen=read(frozenpath)['series']['top770'];new=summary[chosen]
    overview=table(['Sei casi per versione',*groups],[[label,*[fmt(summary[v][key]) for v in groups]] for label,key in [('Cassa media','cash'),('Cassa V4D avversaria','opponent_cash'),('Scarto relativo %','relative_pct'),('Morti idriche totali','water_deaths'),('Perdite animali totali','animal_losses'),('Vittorie contro V4D','wins'),('Perdite inventario, unità','inventory_loss'),('Casi ancora senza semine D21–D22','zero_sowing_cases'),('Infestanti mediane D30','weeds_D30'),('Chiamata più lenta, secondi','runtime_max_seconds'),('Overage massimo per partita, secondi','runtime_max_overage')]])
    phase=[]
    for a,b in [(12,20),(21,25),(26,27),(28,30)]:
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
    for v in ['v41','v45','v46','v47']:
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
    closing_versions=['v41','v45','v46',chosen]
    closing_rows=[]
    for product in ['WHEAT','CARROT','STRAWBERRY','MILK','WOOL','FERTILIZER']:
        for metric in ['harvested','sold_units','sales_cash','realized_unit_price']:
            vals=[]
            for v in closing_versions:
                ps=prof(v)
                if metric=='realized_unit_price':
                    units=sum(d['sold_units'].get(product,0) for p in ps for d in p['ledger']['daily'][27:])
                    cash=sum(d['sales_cash'].get(product,0) for p in ps for d in p['ledger']['daily'][27:])
                    value=cash/units if units else 0
                else:value=mean(sum(d[metric].get(product,0) for d in p['ledger']['daily'][27:]) for p in ps)
                vals.append(fmt(value))
            closing_rows.append([product,metric,*vals])
    overview+='<h2>Raccolte e vendite D28–D30</h2><p>Quantita e ricavi medi per partita. Prezzo realizzato ponderato = ricavi / unita vendute; zero indica assenza di vendite. Le vendite possono includere scorte precedenti a D28.</p>'+table(['Prodotto','Misura',*closing_versions],closing_rows)
    overview+='<h2>Cassa ai checkpoint</h2>'+table(['Giorno',*closing_versions],[[d,*[fmt(mean(p['daily'][d-1]['money'] for p in prof(v))) for v in closing_versions]] for d in [20,25,27,30]])
    base=summary['v45']
    diagnosis=f"""<h2>Servizi e scadenze idriche finali: V46 e V47</h2>
<p>Nella V45 FEED passa da 14 interventi a D27 a 5,67 medi a D28, quando termina la gestione pianificata. La V46 mantiene pianificazione, percorsi e priorita fino a D29 incluso. CARE a D28–D29 viene proposto solo se il suo bonus puo essere utilizzato da una produzione entro fine partita, tenendo conto del ciclo e della capacita di prodotto detenuto. FEED rimane attivo; a D30 torna la gestione terminale precedente.</p>
<p>Restano le scadenze delle semine della V45: nessun nuovo ciclo pianificato da D27, mentre le colture gia presenti vengono servite e raccolte. Consistenze, ledger giornalieri e KPI operativi D1–D27 sono verificati uguali a V45. La modifica riguarda la transizione finale.</p>
<p>La V46 introduce 12 perdite idriche aggiuntive a D28: 10 carote e 2 fragole sul totale dei sei casi. Il suo WATER complessivo aumenta, ma non copre tutte le scadenze. La V47 conserva il piano V46 e protegge le visite WATER delle piante gia rimaste un giorno senza acqua, solo a D28–D29: precedenza di percorso e possibilita di recupero fuori area. Non applica questa protezione all'acqua delle nuove semine. Scorte terminali vuote non escludono perdite di prodotto avvenute prima del termine.</p><p><strong>{chosen.upper()}, sei casi:</strong> cassa media {fmt(new['cash'])} contro {fmt(base['cash'])} V45; vittorie {new['wins']}/6 contro {base['wins']}/6; perdite idriche {new['water_deaths']} contro {base['water_deaths']}; perdite animali {new['animal_losses']} contro {base['animal_losses']}; infestanti mediane D30 {fmt(new['weeds_D30'])} contro {fmt(base['weeds_D30'])}.</p>
<p>Le tabelle distinguono raccolte, vendite e prezzo realizzato nel mercato condiviso. Tre semi di sviluppo nelle due posizioni, non sei semi indipendenti. Top770-001 e un corpus storico descrittivo. Prefisso, topologia 7–7–0 e completamento verificati; nessun errore o missione incompleta. Solo 770, nessuna submission.</p>
<h2>Valutazione: recupero della regressione, vantaggio economico limitato</h2><p>V47 azzera le 12 perdite idriche aggiuntive di V46 a D28; le 20 perdite complessive sono tutte precedenti a D28. La cassa media cresce di appena 143 rispetto a V45 (+0,16%), con 4/6 vittorie in entrambe. Sul seme piu debole V47 perde di 694 contro V4D, mentre V45 perdeva di 60. Il risultato non dimostra un miglioramento robusto.</p>
<p>D28–D30: rispetto a V45, FEED medio sale da 6,56 a 8,44, WATER da 7,56 a 9,56; MOVE scende da 136,67 a 126,11. CARE scende da 1,11 a 1, HARVEST da 20,44 a 20,22 e PASS sale da 38,11 a 39,11. Le infestanti finali mediane restano 23. Nessuna nuova pubblicazione o promozione automatica.</p>
<h2>Prossimo punto verificato nel codice: acqua che aumenta la resa</h2><p>Il percorso sostituisce una visita in scadenza con il solo HARVEST, eliminando WATER. Nel motore, per le colture annuali, WATER aumenta invece la resa nella finestra che va dalla meta arrotondata in alto del ciclo alla maturita, se non gia irrigate e sotto la resa massima. Per grano e carote questo puo quindi eliminare un incremento utile immediatamente prima della raccolta. Il meccanismo e verificato nel codice; l'impatto economico della sua correzione non e ancora misurato. Occorre conservare l'acqua produttiva quando c'e tempo per raccogliere, mantenendo una raccolta breve di ripiego se la scadenza non consente entrambi i comandi.</p>"""
    template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')
    template=re.sub(r'<h2>Diagnosi</h2>.*?<details>',diagnosis+'<details>',template,flags=re.S)
    template=re.sub(r'<p class="note">.*?</p>','<p class="note">Scadenze biologiche '+chosen.upper()+': servizio urgente, percorsi e produzione. <a href="__OTHER__">Altro confronto completo</a>.</p>',template,count=1,flags=re.S)
    template=template.replace('770 assistita V1',chosen.upper()).replace("candidate:'770 assistita'", "candidate:'"+chosen.upper()+"'").replace('7 settembre 2026','8 settembre 2026')
    template=template.replace('Stessi corpus storici già utilizzati; nessun nuovo benchmark esterno o invio di submission. Rigenerazione dei 14 run locali verificata contro tutti i KPI, ledger e risultati precedenti.','Sei simulazioni locali per versione completa. Prove preliminari su un caso riportate separatamente. Nessun invio esterno.')
    for suffix,label,ref,other in [('TOP770','Top770-001',aggregate(top,frozen),'V45'),('V33','V33 locale',aggregate(prof('v33')),'TOP770'),('V38','V38 locale',aggregate(prof('v38')),'TOP770'),('V39','V39 locale',aggregate(prof('v39')),'TOP770'),('V41','V41 locale',aggregate(prof('v41')),'TOP770'),('V44','V44 locale',aggregate(prof('v44')),'TOP770'),('V45','V45 locale',aggregate(prof('v45')),'TOP770'),('V46','V46 locale',aggregate(prof('v46')),'TOP770')]:
        stem=f'{chosen}_{suffix}_D01_D30_COMPLETE_KPI'
        payload=dict(topLabel=label,metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate(prof(chosen)),top770=ref))
        vals=dict(TITLE=chosen.upper()+' vs '+label+' · KPI completi D1–D30',COHORTS='6 casi locali, semi 180903001–003, entrambe le posizioni',TOP=label,OTHER=f'{chosen}_{other}_D01_D30_COMPLETE_KPI.html',ECONOMY=overview,PROVENANCE='Prefisso D1–D11 e topologia verificati. Dati e sorgenti congelati nel manifest; V33, V38 e V39 sono confrontate sugli stessi sei casi. V33 è il riferimento locale scelto dall’utente; V29 resta la submission pubblicata.',DATAFILE=stem+'.json',DATA=json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
        result=template
        for k,v in vals.items():result=result.replace('__'+k+'__',v)
        assert not re.search(r'__[A-Z]+__',result) and not any(c in result for c in ['\u00c3','\u00c2','\ufffd'])
        (OUT/(stem+'.html')).write_text(result,encoding='utf-8');(OUT/(stem+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    sourcepaths += [TOP[0],frozenpath,Path(__file__),Path(__file__).with_name('complete_kpi_template.html'),BASE/'tests/test_renewal_certificate_v32.py',BASE/'tests/test_biological_water_calendar_v38.py',BASE/'tests/test_spent_renewal_v39.py',BASE/'tests/test_protected_routes_v40.py',BASE/'tests/test_biological_protection_v42.py',BASE/'tests/test_water_route_rescue_v43.py',BASE/'tests/test_provisional_queue_v44.py',BASE/'tests/test_closure_bridge_v45.py',BASE/'tests/test_final_services_v46.py',BASE/'tests/test_final_water_v47.py']
    for rs in groups.values():
        for r in rs:
            for name,digest in r['sources'].items():
                p=ROOT/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
                sourcepaths.append(p)
    (OUT/'manifest.json').write_text(json.dumps(dict(chosen=chosen,status='LOCAL_EXPERIMENT_NOT_PROMOTED',sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sourcepaths},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
