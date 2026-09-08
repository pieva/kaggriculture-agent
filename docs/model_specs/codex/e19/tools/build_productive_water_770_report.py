"""Complete KPI report for measured succession experiments; no promotion implied."""
import json,re,hashlib,sys
from pathlib import Path
from statistics import mean,median
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate,FIELDS,TOP,fmt
from docs.model_specs.codex.e19.tools.build_succession_routes_770_report import inventory_loss
BASE=ROOT/'docs/model_specs/codex/e19';RAW=BASE/'artifacts/derived/portfolio_succession_20260907'
OUT=BASE/'reports/productive_water_770_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def table(headers,rows):
    return '<div class="tablewrap"><table><tr>'+''.join('<th>'+str(x)+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</table></div>'
def main():
    chosen=sys.argv[1] if len(sys.argv)>1 else 'v48'
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[(s,t) for s in range(180903001,180903004) for t in (0,1)]
    sourcepaths=[];groups={};summary={}
    for version in ['v33','v38','v39','v41','v44','v45','v46','v47','v48']:
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
    for old,newrun in zip(groups['v47'],groups[chosen]):
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
    for v in ['v41','v45','v47','v48']:
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
    closing_versions=['v41','v45','v47',chosen]
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
    base=summary['v47']
    diagnosis=f"""<h2>Acqua produttiva prima della raccolta: V48</h2>
<p>La V47 riduce una visita in scadenza al solo HARVEST. Nel motore WATER puo ancora aggiungere resa alle colture annuali, se non irrigate oggi, nella finestra di maturazione e sotto la resa massima. La V48 conserva WATER prima di HARVEST in questi casi, solo a D28–D30. Il valore della visita include l'incremento stimato al prezzo corrente; non promette un prezzo futuro.</p>
<p>Il solo HARVEST resta disponibile con priorita inferiore. Se il lavoro completo non entra nel tempo residuo, il dispatcher non puo trasformarlo nel solo WATER: considera la raccolta breve. Le due alternative vengono preparate con i normali controlli di percorso e ritorno al deposito. Non aggiunge irrigazioni a piante gia irrigate, a resa massima o perenni; non modifica le scelte precedenti a D28.</p>
<p><strong>{chosen.upper()}, sei casi:</strong> cassa media {fmt(new['cash'])} contro {fmt(base['cash'])} V47; vittorie {new['wins']}/6 contro {base['wins']}/6; perdite idriche {new['water_deaths']} contro {base['water_deaths']}; perdite animali {new['animal_losses']} contro {base['animal_losses']}; infestanti mediane D30 {fmt(new['weeds_D30'])} contro {fmt(base['weeds_D30'])}.</p>
<p>Consistenze, ledger giornalieri e KPI operativi D1–D27 verificati uguali a V47. Le tabelle distinguono raccolte, vendite e prezzo realizzato nel mercato condiviso. Tre semi di sviluppo nelle due posizioni, non sei semi indipendenti. Top770-001 e un corpus storico descrittivo. Prefisso, topologia 7–7–0 e completamento verificati; nessun errore o missione incompleta. Solo 770, nessuna submission.</p>
<h2>Valutazione: beneficio misurato, due perdite residue</h2><p>Rispetto a V47, la cassa media cresce di 1.486 (+1,64%) e le vittorie passano da 4/6 a 6/6. Il margine relativo sulla cassa avversaria cresce dal 4,74% al 6,29%. Le carote raccolte e vendute D28–D30 passano da 21,33 a 32 unita medie; il grano raccolto da 38,67 a 51,67 e venduto da 46 a 61,67. Il risultato e quindi sostenuto da prodotto aggiuntivo, non dal solo numero di irrigazioni.</p>
<p>La regressione residua e localizzata: una fragola in [2,9] muore per sete a D28 sul seme 180903003, in entrambe le posizioni. Le perdite idriche complessive salgono da 20 a 22; perdite animali e inventario restano zero. Infestanti mediane D30 invariate a 23. Il caso debole ora vince: 62.931 contro 61.518 V4D.</p>
<p>V48 e la candidata locale per proseguire da V47. V41 resta un controllo utile: cassa media superiore (94.704), ma scarto relativo minore (3,66%), meno coltivate a D25 e piu perdite idriche. Nessuna pubblicazione e nessuna validazione indipendente: tutti i casi sono gia utilizzati nello sviluppo. Prima di considerare definitiva la variante, verificare la copertura della fragola residua senza annullare il guadagno delle raccolte.</p>"""
    template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')
    template=re.sub(r'<h2>Diagnosi</h2>.*?<details>',diagnosis+'<details>',template,flags=re.S)
    template=re.sub(r'<p class="note">.*?</p>','<p class="note">Scadenze biologiche '+chosen.upper()+': servizio urgente, percorsi e produzione. <a href="__OTHER__">Altro confronto completo</a>.</p>',template,count=1,flags=re.S)
    template=template.replace('770 assistita V1',chosen.upper()).replace("candidate:'770 assistita'", "candidate:'"+chosen.upper()+"'").replace('7 settembre 2026','8 settembre 2026')
    template=template.replace('Stessi corpus storici già utilizzati; nessun nuovo benchmark esterno o invio di submission. Rigenerazione dei 14 run locali verificata contro tutti i KPI, ledger e risultati precedenti.','Sei simulazioni locali per versione completa. Prove preliminari su un caso riportate separatamente. Nessun invio esterno.')
    for suffix,label,ref,other in [('TOP770','Top770-001',aggregate(top,frozen),'V47'),('V33','V33 locale',aggregate(prof('v33')),'TOP770'),('V38','V38 locale',aggregate(prof('v38')),'TOP770'),('V39','V39 locale',aggregate(prof('v39')),'TOP770'),('V41','V41 locale',aggregate(prof('v41')),'TOP770'),('V44','V44 locale',aggregate(prof('v44')),'TOP770'),('V45','V45 locale',aggregate(prof('v45')),'TOP770'),('V46','V46 locale',aggregate(prof('v46')),'TOP770'),('V47','V47 locale',aggregate(prof('v47')),'TOP770')]:
        stem=f'{chosen}_{suffix}_D01_D30_COMPLETE_KPI'
        payload=dict(topLabel=label,metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate(prof(chosen)),top770=ref))
        vals=dict(TITLE=chosen.upper()+' vs '+label+' · KPI completi D1–D30',COHORTS='6 casi locali, semi 180903001–003, entrambe le posizioni',TOP=label,OTHER=f'{chosen}_{other}_D01_D30_COMPLETE_KPI.html',ECONOMY=overview,PROVENANCE='Prefisso D1–D11 e topologia verificati. Dati e sorgenti congelati nel manifest; V33, V38 e V39 sono confrontate sugli stessi sei casi. V33 è il riferimento locale scelto dall’utente; V29 resta la submission pubblicata.',DATAFILE=stem+'.json',DATA=json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
        result=template
        for k,v in vals.items():result=result.replace('__'+k+'__',v)
        assert not re.search(r'__[A-Z]+__',result) and not any(c in result for c in ['\u00c3','\u00c2','\ufffd'])
        (OUT/(stem+'.html')).write_text(result,encoding='utf-8');(OUT/(stem+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    sourcepaths += [TOP[0],frozenpath,Path(__file__),Path(__file__).with_name('complete_kpi_template.html'),BASE/'tests/test_renewal_certificate_v32.py',BASE/'tests/test_biological_water_calendar_v38.py',BASE/'tests/test_spent_renewal_v39.py',BASE/'tests/test_protected_routes_v40.py',BASE/'tests/test_biological_protection_v42.py',BASE/'tests/test_water_route_rescue_v43.py',BASE/'tests/test_provisional_queue_v44.py',BASE/'tests/test_closure_bridge_v45.py',BASE/'tests/test_final_services_v46.py',BASE/'tests/test_final_water_v47.py',BASE/'tests/test_productive_water_v48.py']
    for rs in groups.values():
        for r in rs:
            for name,digest in r['sources'].items():
                p=ROOT/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
                sourcepaths.append(p)
    (OUT/'manifest.json').write_text(json.dumps(dict(chosen=chosen,status='LOCAL_EXPERIMENT_NOT_PROMOTED',sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sourcepaths},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
