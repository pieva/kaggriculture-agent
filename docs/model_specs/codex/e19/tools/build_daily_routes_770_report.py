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

OUT=BASE/'reports/daily_routes_770_20260907'

LABELS={'portfolio_v18':'Piano V18','daily_routes_v20':'Percorsi V20 iniziali','daily_routes_v21':'Percorsi V21 con assunzioni osservate','daily_routes_v22':'Percorsi V22 con recupero','daily_routes_v23':'Percorsi V23 con costi coerenti','daily_routes_v24':'Percorsi V24 e recupero delle urgenze'}



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

        diagnosis="""<h2>Percorsi giornalieri, non un altro spareggio delle priorità</h2><p>Casualità disattivata, solo770. AperturaD1–D11 e chiusuraD26–D30 ereditate daV18. DaD12 vengono costruite sequenze di visite complete per ciascun lavoratore con inserimento a costo incrementale minimo. Il costo include spostamenti, azioni dei servizi e un passaggio al deposito per gli input mancanti. Non è un ottimo globale e non simula tutti i futuri ricavi.</p><p>Si pianificano i servizi osservati, il riempimento dei pascoli esistenti e i rinnovi arrivati a scadenza. La raccolta del vecchio grano conserva l'eventuale WATER che ne incrementa la resa; resta anche WATER dopo la nuova PLANT. I lavoratori seguono la propria coda di destinazioni; la parte non assegnata e il lavoro nuovo possono essere recuperati quando la coda si libera. Gli input di più visite possono essere prelevati insieme se disponibili.</p><p>V20 costruisce il piano soltanto all'inizio della giornata, quando il motore ha rimosso i manovali del giorno precedente: è un controllo diagnostico incompleto. V21 ricalcola anche quando nuove assunzioni diventano osservate, riservando il tempo delle missioni già attive e partendo dalla loro destinazione prevista. Non interrompe tali missioni e non inventa lavoratori futuri.</p><p>V22 aggiorna le code anche ogni6ore, preservando il lavoro già attivo. Nelle ultime6ore permette il recupero di WATER/FEED urgenti fuori dalla coda assegnata. V23 corregge il costo dei percorsi: il deposito viene visitato quando la visita corrente richiede input, come fa realmente l’esecutore; il conto comprende quindi eventuali ritorni al deposito dopo visite senza input.</p><p>V24 estende il recupero alla seconda metà della giornata e controlla anche colture e animali già reclamati da una missione attiva. Il soccorso esegue soltanto WATER/FEED su uno stato biologicamente urgente; non modifica le missioni in corso. Questo può produrre servizi ridondanti da misurare, ma evita che una prenotazione impedisca di intervenire prima della perdita.</p><p>Le code pianificate e i costi sono conservati nei dati dei run. Il packing può lasciare visite non assegnate: il rispetto del suo budget stimato non equivale al completamento effettivo, verificato qui tramite ledger e KPI. Capacità condivisa del deposito, attese e interferenze con gli investimenti restano limiti da controllare sui risultati.</p>"""
        s=summary[v]

        diagnosis+="""<h2>Decisione e causa verificata</h2><p><strong>Nessuna variante V20–V24 viene promossa; V18 resta il riferimento sperimentale.</strong> V22 è la più promettente: cassa media 91.268 contro 90.613 di V18, ma perde una coltura in ciascuno dei sei casi. D16–D24 MOVE scende da 160,6 a 118,1, mentre PASS sale da 32,1 a 57,3. Le infestanti a D30 aumentano da 20,2 a 28,3. Questi peggioramenti impediscono di considerare risolto il problema delle persone.</p><p>Audit esatto V22, seme 180903001, posizione 0: la fragola (9,4), piantata al giorno interno 6, non viene irrigata né a D21 né a D22 e diventa infestante a D23. Non è una semina tardiva. A D22 H3 WATER è in coda al lavoratore 7, a H7 passa al 12; a H13 scompare dalle code. Nessuna missione verso quella casella viene avviata nell'intera giornata. A H19 gli unici due lavoratori liberi sono a distanza Manhattan 10 e 8, oltre le sei azioni residue necessarie anche senza ostacoli. Il soccorso tardivo non basta.</p><p>Il replay dell'audit riproduce esattamente tutti i risultati del caso originale e l'esecuzione strumentata verifica le azioni fino al passo 528. La medesima perdita D22/(9,4) compare nei sei casi; la ricostruzione oraria è stata eseguita su uno. Il difetto osservato è un impegno urgente che non conserva una capacità di esecuzione riservata durante le ripianificazioni. La prossima correzione deve verificare scadenza e fattibilità dell'incarico fino al completamento, comprese attese e rifornimenti, e trasferirlo solo a un sostituto che possa terminarlo. Non basta aumentare nuovamente una priorità.</p><p>V23 e V24 non risolvono il difetto complessivo: due perdite per caso; V24 riduce la cassa media a 75.028. Nessuna modifica alla 662 e nessuna pubblicazione esterna.</p>"""

        diagnosis+=f"<p><strong>Esito: {s['status']}.</strong> Cassa {fmt(s['cash'])}, scarto relativo {fmt(s['relative_pct'])}%, perdite colture {s['crop_starvation']}, fughe {s['animal_escapes']}, unità raccolte perse {s['inventory_loss_units']}. Nessun upload. Prefisso D1–D11 identico; errori core {s['core_errors']}, casi con missioni residue {s['incomplete_cases']}, verifica delle chiamate fino al termine {s['runtime_complete']}. Topologia verificata nei checkpoint giornalieri.</p>"

        # Explicitly enumerate all deficits; the owner must not discover them

        # by correcting an analysis restricted to the most conspicuous crop.

        diagnosis+='<h2>Uso della manodopera D16–D24</h2><div class="tablewrap"><table><tr><th>Azioni medie per giorno e partita</th><th>V18</th><th>V20</th><th>V21</th><th>V22</th><th>V23</th><th>V24</th><th>Top770-001</th></tr>'
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

        other='daily_routes_v22' if v!='daily_routes_v22' else 'portfolio_v18'

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

