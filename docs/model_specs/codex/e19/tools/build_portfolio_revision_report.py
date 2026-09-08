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

OUT=BASE/'reports/portfolio_revision_20260907'

LABELS={'portfolio_v1':'Successioni V1','portfolio_v2':'Successioni e servizi V2','portfolio_v3':'Successioni e fertilizzazione V3','portfolio_v4':'Portafoglio ed esecuzione V4','portfolio_v5':'Autoconsumo V5','portfolio_v6':'Scorte cronologiche V6','portfolio_v7':'Espansione governata V7','portfolio_v8':'Espansione e servizi combinati V8','portfolio_v9':'Espansione e scadenze V9','portfolio_v10':'Valori monetari coerenti V10','portfolio_v11':'Logistica del deposito V11','portfolio_v12':'Pianificazione giornaliera V12','portfolio_v13':'Pianificazione con ricerca limitata V13','portfolio_v14':'Cicli completi e liquidazione V14'}



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

        s=summary[v];b=summary['base']

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

        diagnosis='''<h2>Modifica e limiti</h2><p>Il core confronta successioni di colture fino al termine, usando ricavi condizionali, costo dei semi, durata di occupazione e lavoro ricorrente. Le missioni di rinnovo possono cambiare coltura; vengono ammesse solo con risorse osservate e il certificato dei servizi FEED/WATER. Le versioni V7–V12 usano quote derivate dal mix osservato nell’avvio e dalla capacità del profilo, non leggono quote o coordinate dai replay. Il criterio è stato progettato studiando questo corpus: il confronto non è indipendente.</p>

<p>V1 introduce il confronto delle successioni. V2 separa i servizi biologici giornalieri dalle attività facoltative. V3 mantiene visibili le raccolte anticipate dopo WATER, sostituisce anche il vecchio filtro economico e valuta fertilizzante per le colture a raccolta ripetuta; trattiene stock osservato per produzioni imminenti. V4 elimina il rinvio indifferente della semina e ordina servizi biologici, rinnovi e raccolte in scadenza. V5 introduce il valore di autoconsumo del grano; V6 ne corregge la contabilità temporale: raccolti alla data pianificata, consumo delle scorte e nessun credito retroattivo per alimentazioni già acquistate. V7 estende proporzionalmente il mix osservato al passaggio al core fino alla superficie target; la guida termina quando le colture iniziali a raccolta ripetuta non possono più arrivare alla prima produzione. V8 combina FEED/CARE/raccolta animale e WATER/raccolta delle colture ripetute, mantenendo una alternativa breve e certificando la missione combinata. V9 distingue le urgenze biologiche osservate dai servizi non ancora urgenti: le semine possono competere con questi ultimi, mantenendo il certificato che ne riserva il lavoro necessario. V10 corregge le unità del punteggio: profitto totale sull’orizzonte, confrontabile con il valore dei servizi, al posto della media giornaliera. V11 usa il trasferimento automatico degli inventari a fine giornata, controllando saturazione e liquidazione finale. V12 certifica ogni assegnazione contro le obbligazioni residue, consentendo lavoro produttivo in parallelo anche quando vi sono irrigazioni da completare entro fine giornata; in caso di mancata fattibilità passa a servizi biologici brevi e registra l’emergenza. V13 limita deterministicamente le verifiche dei percorsi per decisione e misura chiamate, tempi e stati del motore: DONE finale da solo non dimostra che l’agente abbia operato fino a D30.</p>

<p>V14 mantiene i cicli fino alla loro ultima produzione raggiungibile e rimuove i servizi finali che richiederebbero un aggiornamento giornaliero successivo alla fine effettiva della partita. Conserva WATER quando aumenta ancora il raccolto annuale finale.</p><p>Il piano economico resta condizionale: non simula l’intero mercato avversario e non certifica tutti i percorsi futuri. Il lavoro ricorrente è stimato; la fertilizzazione valutata può essere ritardata dall’esecuzione. I ricavi futuri non finanziano gli ordini. I report mostrano tutte le colture, non soltanto il grano.</p>'''

        s=summary[v]

        diagnosis+=f"<p><strong>Esito: {s['status']}.</strong> Cassa {fmt(s['cash'])}, scarto relativo {fmt(s['relative_pct'])}%, perdite colture {s['crop_starvation']}, fughe {s['animal_escapes']}, unità raccolte perse {s['inventory_loss_units']}. Nessun upload. Prefisso D1–D11 identico; errori core {s['core_errors']}, casi con missioni residue {s['incomplete_cases']}, verifica delle chiamate fino al termine {s['runtime_complete']}. Topologia verificata nei checkpoint giornalieri.</p>"

        # Explicitly enumerate all deficits; the owner must not discover them

        # by correcting an analysis restricted to the most conspicuous crop.

        if v=='portfolio_v14':
            diagnosis='<h2>Risultato della revisione: recupero iniziale, rendimento insufficiente</h2><p>La superficie mediana arriva a 58 caselle a D13 e 59 a D15. Il grano resta presente dopo D15; a D20 le mediane sono 12 grano e 38 fragole, con 50 coltivate complessive. La continuità resta inferiore al Top. Le carote finali non sono stabili: a D28 la mediana è zero. Pomodori e meloni sono assenti dopo la transizione; non costituiscono una compensazione.</p><p>Il problema ora è anche la resa del lavoro: fra D16 e D24 le fragole occupano mediamente 34,41 caselle invece di 23,89 della base, ma vengono raccolte 105 unità invece di 130,33. Aumentare la superficie senza completare bene i servizi e la raccolta non basta. Il ledger dimostra zero prodotti già raccolti persi in deposito; non esclude produzioni mancate sul campo. Occorre isolare irrigazione, fertilizzazione e tempi di raccolta delle fragole, oltre ai rinnovi del grano.</p><p>Cassa media 66.132 contro 65.065 della base (+1,64%), ma il divario dalla V4D avversaria peggiora da −19,50% a −25,00%. Due colture perse per mancata acqua nei sei casi, nessuna fuga animale. Tutte le 719 chiamate completate per partita; massimo osservato 0,922 secondi, nessun errore core o missione residua. Variante sperimentale non promossa.</p>'+diagnosis
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

        other='portfolio_v14' if v!='portfolio_v14' else 'portfolio_v13'

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

