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

OUT=BASE/'reports/commitments_random_770_20260907'

LABELS={'portfolio_v18':'Piano V18','commitment_v19_fixed':'Impegni V19 deterministica','commitment_v19_random':'Impegni V19 spareggio casuale'}



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

    economic+='</table></div><p>Il mercato è condiviso: sono riportate entrambe le casse. Superare la V18 su questi casi è soltanto un filtro locale, non una prova indipendente per la pubblicazione.</p>'

    for v,label in LABELS.items():

        profiles=[p['sides']['assisted'] for p in groups[v]]

        phase='<h2>Portafoglio completo per fase</h2><div class="tablewrap"><table><tr><th>Fase</th><th>Coltura</th><th>Base: superficie</th><th>Revisione: superficie</th><th>Top001: superficie</th><th>Revisione: semine</th><th>Top001: semine</th></tr>'

        for a,b in PHASES:

            for c in CROPS:

                vals=[summary[k]['phases'][f'D{a}-D{b}'][c]['occupancy'] for k in ['base',v]]

                vals+=[mean(sum(p['daily'][d-1]['crops'][c] for d in range(a,b+1))/(b-a+1) for p in top),summary[v]['phases'][f'D{a}-D{b}'][c]['planted'],mean(sum(p['ledger']['daily'][d-1]['planted'].get(c,0) for d in range(a,b+1)) for p in top)]

                phase+=f'<tr><td>D{a}–D{b}</td><td>{c}</td>'+''.join('<td>'+fmt(x)+'</td>' for x in vals)+'</tr>'

        phase+='</table></div><p>Superficie media per giorno e partita; semine medie per partita. Le semine comprendono espansione e sostituzioni. D30 resta nei grafici come liquidazione. Le mediane marginali dei grafici non vanno sommate.</p>'

        diagnosis="""<h2>Esperimento: impegni prima, casualità soltanto negli spareggi</h2><p>Solo770, prefisso assistitoD1–D11 invariato. V19 protegge i rinnovi HARVEST+PLANT+WATER rispetto alla raccolta semplice, assegna precedenza al riempimento dei pascoli vuoti e promuove in modo limitato gli investimenti in attesa. Le urgenze biologiche osservate mantengono il rango superiore. L'ammissione degli investimenti resta soggetta a risorse osservate e certificato FEED/WATER corrente; non è un certificato di tutti i servizi futuri.</p><p>Le due versioniV19 usano lo stesso codice. La differenza è esclusivamente uno spareggio pseudocasuale sotto rango, rinnovo, costo del percorso, valore e attesa. La chiave usa seed, giorno, lavoratore, destinazione e comandi: stabile nel giorno e riproducibile, senza cambiare una missione attiva. Nella deterministica vale zero. La chiusura daD26 è invariata.</p><p>Sei casi per versione: tre semi nelle due posizioni controV4D. Un solo seed di spareggio per seme di partita; questa prova non misura tutta la variabilità possibile della casualità e non è validazione esterna. Il Top770-001 è storico già esposto.</p>"""
        s=summary[v]

        diagnosis+=f"<p><strong>Esito: {s['status']}.</strong> Cassa {fmt(s['cash'])}, scarto relativo {fmt(s['relative_pct'])}%, perdite colture {s['crop_starvation']}, fughe {s['animal_escapes']}, unità raccolte perse {s['inventory_loss_units']}. Nessun upload. Prefisso D1–D11 identico; errori core {s['core_errors']}, casi con missioni residue {s['incomplete_cases']}, verifica delle chiamate fino al termine {s['runtime_complete']}. Topologia verificata nei checkpoint giornalieri.</p>"

        # Explicitly enumerate all deficits; the owner must not discover them

        # by correcting an analysis restricted to the most conspicuous crop.

        diagnosis+='<h2>Uso della manodopera D16–D24</h2><div class="tablewrap"><table><tr><th>Azioni medie per giorno e partita</th><th>V18</th><th>V19 deterministica</th><th>V19 casuale</th><th>Top770-001</th></tr>'
        comparison=[[p['sides']['assisted'] for p in groups[k]] for k in LABELS]+[top]
        for op,executed in [('MOVE',False),('PASS',False),('CARE',True),('HARVEST',True),('FERTILIZE',True),('FEED',True),('WATER',True)]:
            vals=[mean(sum(p['ledger']['daily'][d]['executed_actions' if executed else 'requested_actions'].get(op,0) for d in range(15,24))/9 for p in ps) for ps in comparison]
            diagnosis+='<tr><td>'+op+'</td>'+''.join('<td>'+fmt(x)+'</td>' for x in vals)+'</tr>'
        diagnosis+='</table></div><p>HARVEST riusciti contano azioni, non unità raccolte. PASS è una richiesta: la sua riduzione da sola non dimostra lavoro utile.</p>'
        diagnosis+='<h2>Piano e chiusura: carico eseguito</h2><div class="tablewrap"><table><tr><th>Fase</th><th>Indicatore</th>'+''.join('<th>'+l+'</th>' for l in LABELS.values())+'</tr>'
        for a,b in [(12,25),(26,30)]:
            for op in ['MOVE','PASS','FEED','CARE','WATER','HARVEST','FERTILIZE']:
                vals=[mean(sum(p['sides']['assisted']['ledger']['daily'][d-1]['requested_actions' if op in ['MOVE','PASS'] else 'executed_actions'].get(op,0) for d in range(a,b+1))/(b-a+1) for p in groups[k]) for k in LABELS]
                diagnosis+='<tr><td>D'+str(a)+'–D'+str(b)+'</td><td>'+op+'</td>'+''.join('<td>'+fmt(x)+'</td>' for x in vals)+'</tr>'
        diagnosis+='</table></div><p>Medie per giorno e partita; le azioni da sole non misurano il valore della produzione. A D30 non esiste un refresh successivo: la riduzione dei servizi va distinta da una mancanza nei giorni produttivi.</p>'
        fixed=groups['commitment_v19_fixed'];randomized=groups['commitment_v19_random']
        paired=[r['sides']['assisted']['reward']-f['sides']['assisted']['reward'] for f,r in zip(fixed,randomized)]
        diagnosis='<h2>Effetto dello spareggio sullo stesso insieme di casi</h2><p>Cassa media: V18 '+fmt(summary['portfolio_v18']['cash'])+'; V19 deterministica '+fmt(summary['commitment_v19_fixed']['cash'])+'; V19 casuale '+fmt(summary['commitment_v19_random']['cash'])+'. La casuale supera la deterministica in '+str(sum(x>0 for x in paired))+' casi su6, pareggia in '+str(sum(x==0 for x in paired))+'. Questo confronto riguarda la cassa; anche il risultato avversario cambia con il mercato condiviso ed è riportato nella tabella.</p><p>Il filtro di accettazione usa V18 come riferimento, non soltanto la vecchia base assistita. Riempire i pascoli o ridurre una singola oscillazione del grano non basta a promuovere la variante.</p>'+diagnosis
        diagnosis='<h2>Decisione: non promuovere V19</h2><p>Entrambe le versioni riempiono i due pascoli entroD13 in tutti i sei casi. Il granoD22 passa da1casella V18 a7–12 nella deterministica e6–12 nella casuale, ma resta molto sotto il Top. Il confronto complessivo peggiora: MOVE mediD16–D24 circa183 contro161 V18; CARE7,8 contro11,15, pur avendo ora14animali anziché12. Non è una prova che14animali siano troppi: il Top li gestisce. La nostra assegnazione non coordina ancora bene i servizi con rinnovi e nuovi impegni.</p><p>La casualità aumenta la cassa media rispetto aV19 deterministica (73.294 contro68.149), ma aumenta anche la cassa avversaria: il divario relativo peggiora da−9,52% a−17,30%. V18 resta a+2,19%. Lo spareggio non risolve il problema e non viene adottato. Servono capacità e percorsi giornalieri coerenti, non ulteriori scavalcamenti casuali dei ranghi.</p><p>Dodici partite V19 complete, zero perdite biologiche, fughe, prodotti raccolti dispersi, errori core o missioni finali residue. Tutte719chiamate per partita. Il massimo della casuale è1,858secondi con0,858secondi di overage consumato, entro il budget disponibile; non descriverlo come sempre inferiore al secondo.</p>'+diagnosis
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

        other='commitment_v19_random' if v!='commitment_v19_random' else 'commitment_v19_fixed'

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

