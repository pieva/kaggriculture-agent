"""Rebuild paired KPI figures and the full, explicitly limited V49 report."""
import csv
import gzip
import hashlib
import html
import json
from pathlib import Path
from statistics import mean
import sys

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909'


def dump(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')


def total(run,key):
    if key=='cash':return run['reward']
    if key=='share':return sum(d['pass_count'] for d in run['daily'])/sum(d['slots'] for d in run['daily'])*100
    if key=='losses':return sum(e['productive_loss'] for e in run['losses'])
    if key=='escapes':return len(run['ledger']['animal_escapes'])
    if key in ['FEED','CARE','WATER','HARVEST']:return sum(d['executed'].get(key,0) for d in run['daily'])
    return sum(d[key] for d in run['daily'])


def enrich(path):
    from docs.model_specs.codex.e19.tools.audit_v49_obligations import audit_obligations,route_capacity
    run=json.loads(path.read_text())
    raw=ROOT/run['details']
    audit_path=OUT/(path.stem+'_obligations.json')
    source=ROOT/'docs/model_specs/codex/e19/tools/audit_v49_obligations.py'
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    raw_sha=hashlib.sha256(raw.read_bytes()).hexdigest()
    if audit_path.exists():
        cached=json.loads(audit_path.read_text())
        assert cached['source_sha256']==sha and cached['raw_sha256']==raw_sha
    else:
        details=json.load(gzip.open(raw,'rt',encoding='utf-8'))
        worker_counts={}
        for i,step in enumerate(details['replay']['steps'][1:],1):
            obs=details['replay']['steps'][i-1][run['seat']]['observation']
            a=step[run['seat']]['action'];n=1+len(obs['farms'][run['seat']]['hands'])
            for w,c in enumerate([a['farmer'],*a['hands']][:n]):
                key=f"{obs['day']+1}:{w}"
                counts=worker_counts.setdefault(key,dict(day=obs['day']+1,worker=w,slots=0,pass_count=0,move=0))
                counts['slots']+=1;counts['pass_count']+=int(c[0]=='PASS')
                counts['move']+=int(c[0] in ['NORTH','SOUTH','EAST','WEST'])
        cached=dict(source_sha256=sha,raw_sha256=raw_sha,
            daily=audit_obligations(details['replay'],run['seat']),
            worker_daily=list(worker_counts.values()),
            capacity=route_capacity(details['replay'],run['seat'],details['routes']))
        dump(audit_path,cached)
    run['obligations']=cached['daily']
    return run


def table(headers,rows):
    return '<table><thead><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plots=OUT/'figures';plots.mkdir(exist_ok=True)
    selected=sys.argv[1] if len(sys.argv)>1 else 'v49f'
    assert selected in {'v49','v49b','v49c','v49d','v49f'}
    results={}
    for split,n in ([('development',6)] if selected=='v49' else [('development',6),('validation',4)]):
        cases={}
        for variant in ['v48','v49']:
            actual=selected if variant=='v49' else variant
            paths=sorted(OUT.glob(f'{split}_{actual}_*.json'))
            paths=[p for p in paths if not p.name.endswith('_obligations.json')]
            cases[variant]=[enrich(p) for p in paths]
            assert len(cases[variant])==n,(split,variant,len(cases[variant]))
        results[split]=cases
    metrics=['cash','pass_count','share','slots','move','hire_cash','FEED','CARE','WATER','HARVEST','losses','escapes']
    sections=[];summary={}
    for split,cases in results.items():
        a,b=cases['v48'],cases['v49']
        assert [(r['seed'],r['seat']) for r in a]==[(r['seed'],r['seat']) for r in b]
        deltas=[dict(seed=x['seed'],seat=x['seat'],cash=y['reward']-x['reward'],
            cash_percent=(y['reward']/x['reward']-1)*100,
            **{k:total(y,k)-total(x,k) for k in metrics if k!='cash'}) for x,y in zip(a,b)]
        averages={v:{k:mean(total(r,k) for r in cases[v]) for k in metrics} for v in cases}
        coverage_keys=['missed_feed','missed_useful_care','missed_critical_water','decay_lost_units','productive_water_loss_units']
        coverage={v:{k:sum(d[k] for r in cases[v] for d in r['obligations']) for k in coverage_keys} for v in cases}
        gates=dict(complete_errors_incomplete=all(r['runtime']['calls']==719 and r['errors']==0 and r['incomplete']==0 for r in a+b),
            pass_absolute=averages['v49']['pass_count']<averages['v48']['pass_count'],
            pass_share=averages['v49']['share']<averages['v48']['share'],
            move=averages['v49']['move']<=averages['v48']['move'],
            cash_mean=averages['v49']['cash']>=averages['v48']['cash'],
            cash_cases=min(d['cash_percent'] for d in deltas)>=-2,
            productive_losses=averages['v49']['losses']<=averages['v48']['losses'],
            escapes=averages['v49']['escapes']<=averages['v48']['escapes'],
            service_counts=all(averages['v49'][k]>=averages['v48'][k] for k in ['FEED','CARE','HARVEST']),
            observed_obligation_deficits=all(coverage['v49'][k]<=coverage['v48'][k] for k in coverage_keys))
        summary[split]=dict(n=len(a),averages=averages,paired_deltas=deltas,gates=gates,coverage=coverage)
        label='Sviluppo esposto' if split=='development' else 'Seed nuovi · controllo V4D esposto'
        sections.append(f'<h2>{label} · {len(a)} coppie</h2>')
        sections.append(table(['KPI medio per partita','V48','V49','Δ'],[[k,*[f'{averages[v][k]:,.3f}' for v in ['v48','v49']],f"{averages['v49'][k]-averages['v48'][k]:+,.3f}"] for k in metrics]))
        sections.append('<h3>Tutti i casi appaiati</h3>'+table(['Seed','Posto','Δ cassa','Δ cassa %','Δ PASS','Δ MOVE'],[[d['seed'],d['seat'],d['cash'],round(d['cash_percent'],3),d['pass_count'],d['move']] for d in deltas]))
        sections.append('<h3>Gate locali</h3>'+table(['Controllo','Esito'],[[k,'SUPERATO' if v else 'NON SUPERATO'] for k,v in gates.items()]))
        sections.append('<h3>Obblighi scoperti e stock perso · somma del campione</h3>'+table(['Misura','V48','V49'],[[k,coverage['v48'][k],coverage['v49'][k]] for k in coverage_keys]))
        panels=[('pass_count','PASS / giorno'),('share','PASS / slot (%)'),('move','MOVE / giorno'),('cash','Cassa H24'),('slots','Slot effettivamente disponibili'),('hire_cash','Spesa assunzioni'),('FEED','FEED riusciti'),('CARE','CARE riusciti'),('WATER','WATER riusciti'),('HARVEST','HARVEST riusciti'),('crops','Caselle con colture H24'),('animals','Animali H24')]
        panels += [('decay_lost_units','Stock perso per decadimento'),('productive_water_loss_units','Stock esposto alla perdita per acqua')]
        sections.append('<div class="grid">')
        for key,title in panels:
            fig,ax=plt.subplots(figsize=(6.2,3.2),layout='constrained')
            for variant,color in [('v48','#566573'),('v49','#007e80')]:
                series=[]
                for run in cases[variant]:
                    if key in ['decay_lost_units','productive_water_loss_units']:
                        series.append([d[key] for d in run['obligations']])
                    else:
                        series.append([d['executed'].get(key,0) if key in ['FEED','CARE','WATER','HARVEST'] else d['pass_count']/d['slots']*100 if key=='share' else d[key] for d in run['daily']])
                middle=[mean(s[i] for s in series) for i in range(30)]
                ax.plot(range(1,31),middle,label=(selected if variant=='v49' else variant).upper(),color=color,linewidth=2)
                ax.fill_between(range(1,31),[min(s[i] for s in series) for i in range(30)],[max(s[i] for s in series) for i in range(30)],color=color,alpha=.09)
            ax.set(title=title,xlabel='Giorno',xlim=(1,30));ax.grid(alpha=.18);ax.legend(frameon=False)
            name=f'{selected}_{split}_{key}.svg';fig.savefig(plots/name)
            qa=ROOT/'scratch/v49/figures';qa.mkdir(exist_ok=True)
            fig.savefig(qa/Path(name).with_suffix('.png'),dpi=120)
            plt.close(fig)
            sections.append(f'<figure><img src="figures/{name}" alt="{html.escape(title)}"><figcaption>Media e intervallo min–max; stessi seed e posti.</figcaption></figure>')
        sections.append('</div>')
    diag=json.loads((OUT/'diagnostic_106843637.json').read_text())
    assert not diag['mismatches']
    priority=[d for d in diag['daily'] if d['day'] in [2,11,12,13,14,15,29]]
    labels={
        'opening_teacher_or_governor':'Piano assistito / override',
        'waiting_observed_input':'Missione attiva in attesa',
        'reservation_rejection_present_not_proven_causal':'Rifiuto con prenotazioni presenti',
        'prepare_rejection_resources_time_or_policy':'Preparazione rifiutata: causa non isolata',
        'no_offer_unknown_useful_work':'Nessuna offerta osservata',
        'admission_certificate_rejection':'Certificato di ammissione rifiutato'}
    fig,ax=plt.subplots(figsize=(9,4.8),layout='constrained')
    bottom=[0]*len(priority)
    for key,label in labels.items():
        values=[d['causes'].get(key,0) for d in priority]
        ax.bar([str(d['day']) for d in priority],values,bottom=bottom,label=label)
        bottom=[x+y for x,y in zip(bottom,values)]
    ax.set(title='V48 esposta: evidenza osservata nei giorni prioritari',xlabel='Giorno',ylabel='PASS')
    ax.set_ylim(0,max(bottom)*1.1)
    ax.legend(loc='upper left',bbox_to_anchor=(1,1),frameon=False,fontsize=8)
    fig.savefig(plots/'diagnostic_causes.svg');fig.savefig(ROOT/'scratch/v49/figures/diagnostic_causes.png',dpi=120);plt.close(fig)
    workers=1+max(int(w) for d in diag['daily'] for w in d['workers'])
    matrix=[[d['workers'].get(str(w),0) for w in range(workers)] for d in diag['daily']]
    fig,ax=plt.subplots(figsize=(9,6.8),layout='constrained')
    heat=ax.imshow(matrix,aspect='auto',cmap='YlGnBu',vmin=0)
    ax.set(title='V48 esposta: PASS per giorno e persona',xlabel='Persona (0 = agricoltore)',ylabel='Giorno',xticks=range(workers),yticks=range(30),yticklabels=range(1,31))
    fig.colorbar(heat,ax=ax,label='PASS')
    fig.savefig(plots/'diagnostic_workers.svg');fig.savefig(ROOT/'scratch/v49/figures/diagnostic_workers.png',dpi=120);plt.close(fig)
    rows=json.load(gzip.open(ROOT/diag['detail'],'rt',encoding='utf-8'))
    with (OUT/'diagnostic_pass_events.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow(['day','hour','worker','position','remaining','reason','inventory','job','attempts'])
        for r in rows:writer.writerow([r[k] if k in ['day','hour','worker','remaining','reason'] else json.dumps(r[k],ensure_ascii=False) for k in ['day','hour','worker','position','remaining','reason','inventory','job','attempts']])
    external=ROOT/'docs/model_specs/codex/e19/reports/v48_external_pass_update_20260908'
    cohort=json.loads((external/'cohort.json').read_text())
    with (OUT/'external_worker_pass.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow(['episode','raw_sha256','day','worker','pass_count'])
        for game in cohort['games']:
            profile=json.loads((external/f"profile_{game['episode']}.json").read_text())
            assert profile['sha256']==game['sha256']
            for day in profile['candidate']:
                for worker,count in day['worker_pass'].items():
                    writer.writerow([game['episode'],game['sha256'],day['day'],worker,count])
    diagnostic='<h2>Diagnosi V48 congelata · episodio 106843637</h2><p>Replay esposto selezionato per il picco D29, non per esito economico. 719/719 azioni riprodotte. Le categorie descrivono rifiuti osservati; non sono una certificazione che tutto quel lavoro fosse evitabile.</p>'
    diagnostic+=table(['Giorno','PASS','Per persona','Categorie'],[[d['day'],d['total'],json.dumps(d['workers']),json.dumps(d['causes'])] for d in priority])
    diagnostic+='<div class="grid"><figure><img src="figures/diagnostic_causes.svg" alt="Categorie osservate dei PASS"><figcaption>Classificazione esclusiva per priorità, non cause economiche dimostrate.</figcaption></figure><figure><img src="figures/diagnostic_workers.svg" alt="PASS per persona e giorno"><figcaption>Zero può indicare anche persona assente; non è una quota di capacità.</figcaption></figure></div>'
    diagnostic+='<p><a href="diagnostic_pass_events.csv">Tutti i 1.074 eventi PASS</a>, con persona, posizione, inventario, missione e tentativi. Una prenotazione presente durante un rifiuto non prova che ne sia la causa. La classe preparazione raggruppa risorse, tempo e policy senza separarli causalmente; nessuna offerta non significa nessun lavoro utile.</p>'
    diagnostic+='<p><a href="opening_attribution.json">Provenienza verificata dell’avvio</a>: tutti i 69 PASS di D2 e 55 dei 56 di D11 sono già nella tabella fissa ROUTINE_ACTIONS. Un PASS D11 è aggiunto dagli override. L’assenza di un lavoro pianificato nella tabella non dimostra assenza di lavoro utile nello stato osservato. <a href="external_worker_pass.csv">Conteggi per persona dei 38 replay esposti</a>: nessuna nuova validazione esterna.</p>'
    diagnostic+='<p>D2 e D11 appartengono all’avvio assistito: le modifiche V49 entrano dopo D11. La causa interna delle singole attese del teacher non è interamente identificata; la ripetitività non basta a certificarne l’evitabilità. D12–D15 restano un problema di assegnazione e pianificazione parzialmente corretto. D29: 89 rifiuti con prenotazione e 46 assenze di offerte; la verifica causale locale separa il recupero dei servizi dall’eliminazione delle assunzioni per cicli impossibili.</p>'
    ablation=json.loads((OUT/'development_local_only_180903001_0.json').read_text())
    first_a=results['development']['v48'][0];first_b=results['development']['v49'][0]
    diagnostic+='<h3>Ablazione sul primo caso di sviluppo</h3>'+table(['Policy','Cassa','PASS','MOVE'],[[name,total(r,'cash'),total(r,'pass_count'),total(r,'move')] for name,r in [('V48',first_a),('Solo recupero locale',ablation),('V49 completa',first_b)]])
    manifest_name={'v49':'candidate_manifest.json','v49b':'candidate_b_manifest.json','v49c':'candidate_c_manifest.json','v49d':'candidate_d_manifest.json','v49f':'candidate_f_manifest.json'}[selected]
    manifest=json.loads((OUT/manifest_name).read_text())
    parities=[json.loads(p.read_text()) for p in sorted(OUT.glob('parity_*.json')) if json.loads(p.read_text())['bundle_sha256']==manifest['sha256']]
    summary['parity']=parities;summary['candidate_sha256']=manifest['sha256']
    summary['external_unexposed_opponent_gate']='NOT_RUN'
    summary['kaggle_runtime_gate']='NOT_CERTIFIED_LOCAL_TIMEOUT_RELAXED'
    summary['promotion']='LOCAL_CANDIDATE_ONLY' if all(all(part['gates'].values()) for part in summary.values() if isinstance(part,dict) and 'gates' in part) else 'REJECTED'
    summary['selected_variant']=selected
    dump(OUT/('rejected_a_summary.json' if selected=='v49' else 'summary.json'),summary)
    body='''<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V49 · Riduzione dei PASS</title><style>body{font:16px/1.55 system-ui,sans-serif;color:#20313a;background:#f5f7f8;max-width:1320px;margin:auto;padding:32px}h1{font-size:38px}h2{margin-top:48px}table{border-collapse:collapse;background:white;width:100%;font-size:14px;margin:20px 0}th,td{padding:9px;border-bottom:1px solid #dde3e6;text-align:left;overflow-wrap:anywhere}th{background:#dcebed}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0;background:white;padding:10px}img{width:100%;display:block}figcaption{font-size:12px;color:#53656e}.note{border-left:5px solid #007e80;padding:20px;background:white}code{overflow-wrap:anywhere}@media(max-width:800px){.grid{grid-template-columns:1fr}body{padding:16px}table{display:block;overflow:auto}}</style><h1>V49 · Riduzione dei PASS evitabili</h1><p>Candidata locale 770 · 9 settembre 2026 · V48 pubblicata preservata</p><div class="note">Due correzioni: servizi biologici utili sulla casella prima del PASS e rimozione del lavoro di semina impossibile dal calcolo delle assunzioni. Nessuna nuova pubblicazione Kaggle. La validazione con avversari esterni non esposti resta da eseguire.</div>'''
    if selected=='v49f':
        body+='<h2>Risultato locale appaiato</h2>'+table(['Partizione','Coppie','Δ PASS medi','Δ MOVE medi','Δ cassa media','Gate locali'],[[split,part['n'],round(part['averages']['v49']['pass_count']-part['averages']['v48']['pass_count'],3),round(part['averages']['v49']['move']-part['averages']['v48']['move'],3),round(part['averages']['v49']['cash']-part['averages']['v48']['cash'],3),'SUPERATI' if all(part['gates'].values()) else 'NON SUPERATI'] for split,part in summary.items() if isinstance(part,dict) and 'gates' in part])
    body+=diagnostic+''.join(sections)
    if selected in {'v49b','v49c','v49d','v49f'}:
        rejected=json.loads((OUT/'rejected_a_summary.json').read_text())['development']
        body+='<h2>V49 A respinta · tutti i casi di sviluppo</h2>'+table(['Seed','Posto','Δ cassa','Δ PASS'],[[d['seed'],d['seat'],d['cash'],d['pass_count']] for d in rejected['paired_deltas']])
        body+='<p>La revisione A ha fallito il gate economico. Anche B, con recupero limitato all’ultimo tick e riduzione massima di un manovale, perde 924 di cassa e aggiunge 19 MOVE sul seed 180903003 posto 0. V49C recupera solo CARE utile nell’ultimo tick su animali già alimentati; assunzioni e raccolte restano gestite dalla V48. Le correzioni sono state fatte sui soli seed di sviluppo, prima di aprire la validazione. <a href="REJECTED_V49A_IT.html">Report integrale A</a>.</p>'
    body+='<div class="note">Runtime Kaggle NON certificato. Dopo run concorrenti con azioni assenti, la matrice è stata ripetuta con actTimeout=120; regole economiche e biologiche invariate. Non usare questi risultati per dichiarare superato il limite temporale standard. Campione piccolo: sei coppie di sviluppo ma tre seed distinti, quattro coppie di trasferimento ma due seed distinti. I due posti non sono repliche statisticamente indipendenti.</div>'
    body+='<h2>Riproducibilità e limiti</h2><p>Bundle candidata SHA-256: <code>'+manifest['sha256']+'</code>. Baseline e 18 sorgenti congelati controllati dalla verifica di parità. Parità registrate: '+html.escape(json.dumps(parities))+'.</p>'
    body+='<p>Le curve misurano richieste PASS/MOVE su persone presenti prima del batch, servizi effettivamente riusciti tramite engine, cassa H24 e cassa finale separatamente. Ultimo giorno: 23 transizioni, non 24. Ogni ledger ricostruisce i saldi dei due giocatori per tutte le 719 transizioni. I deficit a fine giornata sono misurati dopo i comandi e il decadimento, prima del refresh; la cura utile è una previsione a regole note, non un ricavo garantito. Rimangono fuori dal gate la copertura ottima su tutto il ciclo, tutti gli effetti del mercato futuro e la redditività marginale di ciascun investimento.</p>'
    body+='<p>Gli audit <code>*_obligations.json</code> riportano per persona costo del percorso pianificato, lavoro già impegnato e comandi realizzati nella finestra residua. I checkpoint possono sovrapporsi e NON vanno sommati. Nessuna ottimizzazione completa dell’organico: il termine di carico viene corretto solo dove il ciclo è biologicamente impossibile. D2/D11 sono invariati; la sola riduzione dei PASS non autorizza a dichiarare risolto tutto il problema.</p><p>Protocollo: <a href="PROTOCOL_IT.md">PROTOCOL_IT.md</a> · Dati: <a href="summary.json">summary.json</a> · Inventario: <a href="candidate_manifest.json">candidate_manifest.json</a>.</p></html>'
    if selected!='v49':
        label=selected.upper()
        body=body.replace('V49 ·',label+' ·').replace('V49 completa',label+' completa').replace('>V49<','>'+label+'<').replace('href="candidate_manifest.json"','href="'+manifest_name+'"').replace('>candidate_manifest.json<','>'+manifest_name+'<')
    if selected=='v49c':
        body=body.replace('Due correzioni: servizi biologici utili sulla casella prima del PASS e rimozione del lavoro di semina impossibile dal calcolo delle assunzioni.','Correzione conservativa: CARE con beneficio futuro nell’ultimo tick del giorno su un animale già alimentato. Le modifiche più ampie a servizi e assunzioni sono state respinte.')
    if selected=='v49d':
        body=body.replace('Due correzioni: servizi biologici utili sulla casella prima del PASS e rimozione del lavoro di semina impossibile dal calcolo delle assunzioni.','Correzione isolata del carico per le assunzioni: quando nessuna semina può maturare, riduzione del target di manovali limitata a uno rispetto all’estimatore originale. Dispatcher V48 invariato; nessun recupero locale.')
        body=body.replace('V49C recupera solo CARE utile nell’ultimo tick su animali già alimentati; assunzioni e raccolte restano gestite dalla V48.','Anche C (sola CARE finale) è respinta: −2.167 di cassa e +35 PASS sullo stesso caso. D isola la sola correzione prudente dell’organico e conserva integralmente il dispatcher V48.')
    if selected=='v49f':
        body=body.replace('Ablazione sul primo caso di sviluppo','Confronto esplorativo sul primo caso di sviluppo (policy diverse)')
        body=body.replace('D12–D15 restano un problema di assegnazione e pianificazione parzialmente corretto.','D12–D15 restano un problema aperto di assegnazione e pianificazione; F non lo modifica.')
        body=body.replace('la verifica causale locale separa il recupero dei servizi dall’eliminazione delle assunzioni per cicli impossibili.','i tentativi sui servizi locali e sulle assunzioni per cicli impossibili sono stati separati e respinti; F non interviene su D29.')
        body=body.replace('Due correzioni: servizi biologici utili sulla casella prima del PASS e rimozione del lavoro di semina impossibile dal calcolo delle assunzioni.','Avvio 770 con tre manovali operativi in D2: eliminazione di un’assunzione destinata a 23 PASS, compensazione del punto di ingresso e rimozione di due spostamenti senza lavoro successivo.')
        body=body.replace('V49C recupera solo CARE utile nell’ultimo tick su animali già alimentati; assunzioni e raccolte restano gestite dalla V48.','C è respinta (−2.167 cassa, +35 PASS). D migliora la cassa ma aumenta MOVE medi di 6,33 e fallisce quel gate. E ometteva la diversa posizione di ingresso del manovale ed è scartata per errore di rimappatura, non usata come prova di miglioramento. F corregge la geometria e interviene solo sull’avvio D2.')
        body=body.replace('le modifiche V49 entrano dopo D11','le revisioni A–D entrano dopo D11; F interviene in D2')
        body=body.replace('D2/D11 sono invariati','D11 e i problemi generali D12–D15/D29 restano fuori dalla correzione mirata di F')
        body=body.replace('il termine di carico viene corretto solo dove il ciclo è biologicamente impossibile','il piano noto di D2 viene eseguito con tre manovali operativi; le correzioni al carico fuori orizzonte non sono attive in F')
        body=body.replace('<h2>Riproducibilità e limiti</h2>','<h2>Riproducibilità e limiti</h2><p><a href="REPRODUCE_IT.md">Comandi e inventario delle prove</a> · <a href="opening_equivalence.json">Equivalenza degli stati dopo D2</a> · <a href="integrity.json">Integrità della baseline e del motore</a>.</p>')
    (OUT/('REJECTED_V49A_IT.html' if selected=='v49' else 'REPORT_V49_PASS_IT.html')).write_text(body,encoding='utf-8')
    print(json.dumps({k:v.get('gates') for k,v in summary.items() if isinstance(v,dict)},indent=2))


if __name__=='__main__':main()
