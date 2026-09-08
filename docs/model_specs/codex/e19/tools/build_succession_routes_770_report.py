"""Full-portfolio review of the integrated revisions, including failed stages."""

import hashlib

import json

from pathlib import Path

from statistics import mean, median

import sys

ROOT=Path(__file__).resolve().parents[5]

sys.path.insert(0,str(ROOT))

from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import aggregate,FIELDS,TOP,fmt

from docs.model_specs.codex.e19.tools.build_teacher_770_control_report import assess,CROPS,PHASES

BASE=ROOT/'docs/model_specs/codex/e19'

OUT=BASE/'reports/succession_routes_770_20260908'

LABELS={'portfolio_v18':'Piano V18','daily_routes_v25':'Piano V25','daily_routes_v26':'Raccolta V26','daily_routes_v27':'Successione V27 bloccante','daily_routes_v28':'Successione V28 provvisoria','daily_routes_v29':'Successione V29 certificata'}



def read(p):return json.loads(p.read_text(encoding='utf-8'))



def inventory_loss(profile):

    result={}

    for c in CROPS+['MILK','WOOL','EGG']:

        units=sum(f['harvested'].get(c,0)+f['bought_units'].get('BUY_PRODUCT:'+c,0)-f['sold_units'].get(c,0)-(f['executed_actions'].get('FEED',0) if c=='WHEAT' else 0) for f in profile['ledger']['daily'])

        units-=profile['terminal']['shed'].get(c,0)+profile['terminal']['carried'].get(c,0)

        assert units>=0,(c,units)

        result[c]=units

    return result



def main():

    OUT.mkdir(exist_ok=True)

    cases=[(s,t) for s in range(180903001,180903004) for t in (0,1)]

    sources=[BASE/'artifacts/derived/assisted_770_complete_20260907'/f'{s}_{t}.json' for s,t in cases]

    groups={'base':[read(p) for p in sources]}

    raw={}

    for variant in LABELS:

        paths=[BASE/'artifacts/derived/portfolio_succession_20260907'/f'{variant}_{s}_{t}.json' for s,t in cases]

        sources+=paths

        rows=[read(p) for p in paths];raw[variant]=rows

        assert all(p['prefix_parity'] for p in rows)

        for p in rows:

            for d in p['sides']['candidate']['daily']:

                assert d['pasture_topology']=={'Q0':7,'Q1':7,'Q2':0,'Q3':0} or d['day']<=11

        for row in rows:
            for plan in row.get('daily_routes',[]):
                targets=[tuple(v['target']) for route in plan['routes'] for v in route['visits']]
                assert len(targets)==len(set(targets))
                assert all(route['cost']<=route.get('available',plan['budget']) for route in plan['routes'])
        groups[variant]=[dict(p,sides={'assisted':p['sides']['candidate'],'v4d':p['sides']['v4d']}) for p in rows]

    summary={v:assess(ps) for v,ps in groups.items()}

    for v,ps in groups.items():

        summary[v]['inventory_loss']={c:sum(inventory_loss(p['sides']['assisted'])[c] for p in ps) for c in CROPS+['MILK','WOOL','EGG']}

        summary[v]['inventory_loss_units']=sum(summary[v]['inventory_loss'].values())

    for v in LABELS:

        s=summary[v];b=summary['portfolio_v18']

        s['core_errors']=sum(p['errors'] for p in raw[v])

        s['incomplete_cases']=sum(p['incomplete']>0 for p in raw[v])

        s['runtime_checked']=all('runtime' in p for p in raw[v])

        s['runtime_complete']=s['runtime_checked'] and all(p['runtime']['complete'] and not p['runtime']['backend_statuses'] for p in raw[v])

        s['max_call_seconds']=max((p.get('runtime',{}).get('max_seconds',0) for p in raw[v]),default=0) if s['runtime_checked'] else None

        s['local_gate_pass']=(s['cash']>=b['cash'] and s['relative_pct']>=b['relative_pct'] and s['crop_starvation']==0 and s['animal_escapes']==0 and s['inventory_loss_units']==0 and s['runtime_complete'] and s['core_errors']==0 and s['incomplete_cases']==0)

        s['status']='LOCAL_GATE_ONLY_NOT_RELEASED' if s['local_gate_pass'] else 'NOT_PROMOTED'

        s['median_crops']={str(d):{c:median(p['sides']['assisted']['daily'][d-1]['crops'][c] for p in groups[v]) for c in CROPS} for d in [12,13,15,20,25,28]}

        s['median_cultivated']={str(d):median(p['sides']['assisted']['daily'][d-1]['crop_tiles'] for p in groups[v]) for d in [12,13,15,20,25,28]}

    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')

    top=read(TOP[0])['jesse']

    frozenpath=ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_28_C_TOP770_D01_D30_KPI_19.json'

    frozen=read(frozenpath)

    assert frozen['cohorts']['top770']['episodes']==[p['episode_id'] for p in top]

    economic='<div class="tablewrap"><table><tr><th>Stessi 6 casi</th><th>Base</th>'+''.join('<th>'+l+'</th>' for l in LABELS.values())+'</tr>'

    for label,key in [('Cassa media','cash'),('Cassa V4D avversaria','opponent_cash'),('Scarto relativo (%)','relative_pct'),('Perdite colture per acqua','crop_starvation'),('Fughe animali','animal_escapes'),('Prodotti raccolti persi in deposito','inventory_loss_units')]:

        economic+='<tr><td>'+label+'</td>'+''.join('<td>'+fmt(summary[v][key])+'</td>' for v in groups)+'</tr>'

    economic+='</table></div><p>Il mercato è condiviso: sono riportate entrambe le casse. Superare la base su questi casi è soltanto un filtro locale, non una prova indipendente per la pubblicazione.</p>'

    for v,label in LABELS.items():

        profiles=[p['sides']['assisted'] for p in groups[v]]

        phase='<h2>Portafoglio completo per fase</h2><div class="tablewrap"><table><tr><th>Fase</th><th>Coltura</th><th>Base: superficie</th><th>Revisione: superficie</th><th>Top001: superficie</th><th>Revisione: semine</th><th>Top001: semine</th></tr>'

        for a,b in PHASES:

            for c in CROPS:

                vals=[summary[k]['phases'][f'D{a}-D{b}'][c]['occupancy'] for k in ['base',v]]

                vals+=[mean(sum(p['daily'][d-1]['crops'][c] for d in range(a,b+1))/(b-a+1) for p in top),summary[v]['phases'][f'D{a}-D{b}'][c]['planted'],mean(sum(p['ledger']['daily'][d-1]['planted'].get(c,0) for d in range(a,b+1)) for p in top)]

                phase+=f'<tr><td>D{a}–D{b}</td><td>{c}</td>'+''.join('<td>'+fmt(x)+'</td>' for x in vals)+'</tr>'

        phase+='</table></div><p>Superficie media per giorno e partita; semine medie per partita. Le semine comprendono espansione e sostituzioni. D30 resta nei grafici come liquidazione. Le mediane marginali dei grafici non vanno sommate.</p>'

        diagnosis="""<h2>Raccolta e impegno successivo sulla casella</h2><p>V27 conserva la raccolta preventiva diV26, ma registra anche un impegno di rinnovo per la casella. Quando il terreno risulta vuoto o infestato, il rinnovo ammissibile entra nelle code dei percorsi come NEW_CROP con precedenza sulle attivita ordinarie. La comparsa di una nuova casella da riseminare provoca il ricalcolo delle code. Il completamento viene riconosciuto dal nuovo ciclo osservato sulla casella; un cambio di giorno non cancella l'impegno.</p><p>La raccolta resta indipendente dal finanziamento e dal certificato del nuovo ciclo. Le missioni gia attive non vengono interrotte. Il test su osservazioni reali verifica l'ingresso di PLANT WHEAT nelle code diD21, unicita delle destinazioni e identita dell'aperturaD1–D11. Il test usa osservazioni storiche: i risultati reali della nuova policy sono quelli delle sei simulazioni riportate qui.</p><p>Questa revisione modifica la successione nel piano D12–D25. DaD26 resta il precedente selettore di chiusura: il calendario integrato delle carote e la prenotazione completa di tutte le scadenze biologiche non sono implementati. Gli impegni registrati non equivalgono a una garanzia di completamento: capacita, input e certificati possono ancora rinviare una semina. Solo770, casualita disattivata, nessun upload.</p><p>Il conteggio delle perdite per acqua non comprende prodotto decaduto. Le infestanti finali comprendono anche perenni gia raccolte. Questi limiti restano rilevanti nel valutare il risultato.</p>"""

        diagnosis+='<p>V28 conserva gli impegni diV27 ma rende provvisoria la prenotazione delle semine: la testa NEW_CROP non impedisce di preparare servizi eseguibili quando la semina non e ancora autorizzata. V27 resta nel confronto come controllo diagnostico del blocco introdotto dalle prenotazioni. Entrambe sono esperimenti, non versioni pubblicate.</p>'
        diagnosis+='<p>V29 aggiunge una correzione al certificato: le proposte NEW_CROP su terreno vuoto o infestato non sono conteggiate come piante esistenti da irrigare. La missione candidata conserva PLANT e WATER, e gli obblighi delle colture esistenti restano nel controllo. Il test verifica esplicitamente entrambe queste condizioni. La modifica non elimina il controllo di capacita.</p>'
        diagnosis+='<h2>Obiettivo D21: non raggiunto</h2><p>Le prenotazioni persistenti sono implementate, ma nei casi V29 misurati D21 e D22 restano senza nuove semine. La superficie di grano scende ancora dopo il raccolto. V27 mostrava un blocco delle code e V28 lo riduce; V29 elimina dal certificato le irrigazioni ipotetiche, ma queste correzioni non assicurano tempo sufficiente alle semine. Non si tratta quindi di una soluzione riuscita della continuita colturale. Il numero di prenotazioni e i test del meccanismo non sostituiscono il controllo delle azioni eseguite.</p>'
        diagnosis+='<p><strong>Nessuna revisione promossa.</strong> Sui sei casi per versione V26 aveva cassa media68.520, scarto relativo+3,03% e18morti per acqua. V27:72.093, −14,42%,134morti. V28:75.140, −1,41%,42morti. V29:74.993, −5,49%,54morti. La cassa assoluta da sola nasconde il peggioramento relativo e dei servizi. V18 resta il riferimento sperimentale. Il calendario di chiusura delle carote non viene risolto da queste modifiche.</p>'
        diagnosis+=f"<p><strong>Esito: {s['status']}.</strong> Cassa {fmt(s['cash'])}, scarto relativo {fmt(s['relative_pct'])}%, perdite colture {s['crop_starvation']}, fughe {s['animal_escapes']}, unità raccolte perse {s['inventory_loss_units']}. Nessun upload. Prefisso D1–D11 identico; errori core {s['core_errors']}, casi con missioni residue {s['incomplete_cases']}, verifica delle chiamate fino al termine {s['runtime_complete']}. Topologia verificata nei checkpoint giornalieri.</p>"

        # Explicitly enumerate all deficits; the owner must not discover them

        # by correcting an analysis restricted to the most conspicuous crop.

        diagnosis+='<h2>Uso della manodopera D16–D24</h2><div class="tablewrap"><table><tr><th>Azioni medie per giorno e partita</th>'+''.join('<th>'+label+'</th>' for label in LABELS.values())+'<th>Top770-001</th></tr>'

        comparison=[[p['sides']['assisted'] for p in groups[k]] for k in LABELS]+[top]
        for op,executed in [('MOVE',False),('PASS',False),('CARE',True),('HARVEST',True),('FERTILIZE',True),('FEED',True),('WATER',True)]:
            vals=[mean(sum(p['ledger']['daily'][d]['executed_actions' if executed else 'requested_actions'].get(op,0) for d in range(15,24))/9 for p in ps) for ps in comparison]
            diagnosis+='<tr><td>'+op+'</td>'+''.join('<td>'+fmt(x)+'</td>' for x in vals)+'</tr>'
        diagnosis+='</table></div><p>HARVEST riusciti contano azioni, non unità raccolte. PASS è una richiesta: la sua riduzione da sola non dimostra lavoro utile.</p>'
        diagnosis+='<h2>Effetto iniziale D12–D13</h2><div class="tablewrap"><table><tr><th>Giorno/KPI</th>'+''.join('<th>'+label+'</th>' for label in LABELS.values())+'</tr>'
        for d in [12,13,20,21,22,25]:
            for key in ['PASS','MOVE','crop_tiles','WHEAT','PLANT']:
                vals=[mean(p['sides']['assisted']['daily'][d-1]['crop_tiles'] if key=='crop_tiles' else p['sides']['assisted']['daily'][d-1]['crops']['WHEAT'] if key=='WHEAT' else p['sides']['assisted']['ledger']['daily'][d-1]['executed_actions'].get('PLANT',0) if key=='PLANT' else p['sides']['assisted']['operational_daily'][d-1][key] for p in groups[k]) for k in LABELS]
                diagnosis+='<tr><td>D'+str(d)+' '+key+'</td>'+''.join('<td>'+fmt(x)+'</td>' for x in vals)+'</tr>'
        diagnosis+='</table></div>'
        diagnosis+='<h2>Piano e chiusura: carico eseguito</h2><div class="tablewrap"><table><tr><th>Fase</th><th>Indicatore</th>'+''.join('<th>'+l+'</th>' for l in LABELS.values())+'</tr>'
        for a,b in [(12,25),(26,30)]:
            for op in ['MOVE','PASS','FEED','CARE','WATER','HARVEST','FERTILIZE']:
                vals=[mean(sum(p['sides']['assisted']['ledger']['daily'][d-1]['requested_actions' if op in ['MOVE','PASS'] else 'executed_actions'].get(op,0) for d in range(a,b+1))/(b-a+1) for p in groups[k]) for k in LABELS]
                diagnosis+='<tr><td>D'+str(a)+'–D'+str(b)+'</td><td>'+op+'</td>'+''.join('<td>'+fmt(x)+'</td>' for x in vals)+'</tr>'
        diagnosis+='</table></div><p>Medie per giorno e partita; le azioni da sole non misurano il valore della produzione. A D30 non esiste un refresh successivo: la riduzione dei servizi va distinta da una mancanza nei giorni produttivi.</p>'
        diagnosis+='<h2>Divari rispetto al Top: tutte le colture</h2><ul>'

        for a,b in PHASES:

            deficits=[]

            for c in CROPS:

                reference=mean(sum(p['daily'][d-1]['crops'][c] for d in range(a,b+1))/(b-a+1) for p in top)

                value=s['phases'][f'D{a}-D{b}'][c]['occupancy']

                if value<reference: deficits.append(f'{c}: {fmt(value)} contro {fmt(reference)}')

            diagnosis+=f'<li>D{a}–D{b}: '+('; '.join(deficits) or 'nessun deficit medio per singola coltura')+'.</li>'

        diagnosis+='</ul><p>Questo confronto storico è descrittivo: i Top hanno semi, avversari e mercati diversi. Aumentare le caselle non dimostra maggiore redditività.</p>'

        template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')

        a=template.index('<h2>Diagnosi</h2>');b=template.index('<details>',a)

        template=template[:a]+diagnosis+phase+template[b:]

        template=template.replace('770 assistita V1',label).replace("candidate:'770 assistita'",f"candidate:{json.dumps(label)}")

        template=template.replace('Altro Top770','Altra revisione').replace('Rigenerazione dei 14 run locali verificata contro tutti i KPI, ledger e risultati precedenti.','Sei casi per revisione, parità del prefisso e contabilità riconciliata.')

        payload=dict(topLabel='Top770-001',metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate(profiles),top770=aggregate(top,frozen['series']['top770'])))

        filename=v+'_TOP770_D01_D30_COMPLETE_KPI'

        (OUT/(filename+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')

        other='daily_routes_v29' if v!='daily_routes_v29' else 'daily_routes_v26'

        replacements=dict(TITLE=label+' vs Top770-001 · KPI completi D1–D30',COHORTS='6 partite locali contro V4D · 5 replay storici Top770-001',OTHER=other+'_TOP770_D01_D30_COMPLETE_KPI.html',TOP='Top770-001',ECONOMY=economic,PROVENANCE='Semi 180903001–003, entrambe le posizioni. Top001: '+', '.join(str(p['episode_id']) for p in top)+'. Fonti e codice degli esperimenti nel manifest.',DATAFILE=filename+'.json',DATA=json.dumps(payload,ensure_ascii=False).replace('</',r'<\/'))

        for k,value in replacements.items():template=template.replace('__'+k+'__',value)

        assert len(payload['metrics'])==22 and all(len(xs)==30 for g in payload['series'].values() for xs in g.values())

        (OUT/(filename+'.html')).write_text(template,encoding='utf-8')

    sources+=[TOP[0],frozenpath,Path(__file__),Path(__file__).with_name('complete_kpi_template.html')]

    for rows in raw.values():

        for row in rows:

            for name,digest in row['sources'].items():

                p=ROOT/name

                assert hashlib.sha256(p.read_bytes()).hexdigest()==digest, name

                sources.append(p)

    (OUT/'manifest.json').write_text(json.dumps(dict(sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2),encoding='utf-8')

    print(json.dumps({v:{k:x for k,x in s.items() if k not in ['phases','median_crops','median_cultivated']} for v,s in summary.items()},indent=2))



if __name__=='__main__':main()

