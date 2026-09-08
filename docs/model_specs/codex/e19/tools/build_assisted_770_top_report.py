"""D1-D30 frozen assisted 770 / previously used Top770 cohorts."""
import base64
import hashlib
import json
import os
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[5]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'scratch/matplotlib_kpi'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt

BASE=ROOT/'docs/model_specs/codex/e19'
DATA=BASE/'artifacts/derived/assisted_770_d30_20260907'
OUT=BASE/'reports/assisted_770_top770_d30_20260907'
TOP=[ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_26_JESSE_770_D01_D30_CLOSURE.json',ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_31_EXTERNAL_TOP002_FULL_20260906.json']
NAMES=['770 assistita · locale','Top770-001 · storico','Top770-002 · storico','V4D · avversaria locale']
COLORS=['#15699a','#b85b2e','#7951a4','#438567']


def num(n):return f'{n:,.1f}'.replace(',','X').replace('.',',').replace('X','.')


def rows(profile):
    out=[];cash=profile['ledger']['initial_cash'];cum_sales=0
    for s,f in zip(profile['daily'],profile['ledger']['daily']):
        sales=sum(f['sales_cash'].values());purchases=sum(f['purchase_cash'].values())
        delta=sales-purchases-f['hire_cash']-f['land_cash']+f['unit_cash_delta']
        cash+=delta;cum_sales+=sales
        row=dict(cash=cash,snapshot_cash=s['money'],net=delta,sales=sales,purchases=purchases,
                 hire=f['hire_cash'],land=f['land_cash'],cum_sales=cum_sales,
                 hands=s['hands'],crop_tiles=s['crop_tiles'],animals=s['occupied_livestock_tiles'],
                 pastures=sum(s['pasture_topology'].values()),**s['crops'],**s['animals'])
        for q,n in s['pasture_topology'].items():row[q]=n
        for op in ['FEED','CARE','WATER','HARVEST','FERTILIZE']:
            row[op]=f['executed_actions'].get(op,0)
        total=sum(f['requested_actions'].values())
        for op in ['MOVE','PASS']:
            row[op]=f['requested_actions'].get(op,0)
            row[op+'_share']=100*row[op]/max(total,1)
        for product in ['MELON','STRAWBERRY','MILK','WOOL','FERTILIZER','WHEAT']:
            row['yield_'+product]=f['harvested'].get(product,0)
            row['sale_'+product]=f['sales_cash'].get(product,0)
        out.append(row)
    assert len(out)==30
    return out


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    paths=[DATA/f'{s}_{p}.json' for s in range(180903001,180903008) for p in (0,1)]
    local=[json.loads(p.read_text()) for p in paths]
    assert all(p['prefix_parity'] for p in local)
    top1=json.loads(TOP[0].read_text())['jesse']
    top2=[p for p in json.loads(TOP[1].read_text())['profiles'] if p['exact770_final']]
    assert len(top1)==5 and len(top2)==4
    groups=[[p['sides']['assisted'] for p in local],top1,top2,[p['sides']['v4d'] for p in local]]
    rr=[[rows(p) for p in group] for group in groups]
    ag=[[{k:dict(mean=mean(r[d][k] for r in group),min=min(r[d][k] for r in group),max=max(r[d][k] for r in group)) for k in group[0][d]} for d in range(30)] for group in rr]
    def plot(keys,titles,name):
        fig,axes=plt.subplots(3,2,figsize=(13,10),layout='constrained')
        for ax,key,title in zip(axes.flat,keys,titles):
            for i in range(3):
                a=ag[i]
                ax.plot(range(1,31),[d[key]['mean'] for d in a],label=NAMES[i],color=COLORS[i],lw=2)
                ax.fill_between(range(1,31),[d[key]['min'] for d in a],[d[key]['max'] for d in a],color=COLORS[i],alpha=.08)
            ax.axvline(11.5,color='#333',ls=':',lw=1);ax.set_title(title,loc='left');ax.grid(alpha=.18);ax.set_xticks([1,5,11,12,15,20,25,30]);ax.set_xlabel('Giorno')
        axes.flat[0].legend(fontsize=8)
        fig.suptitle('770 assistita e Top770 storici · D1–D30\nLinea verticale: subentro del core D12. Bande: minimo–massimo, mercati differenti.',fontsize=12)
        fig.savefig(OUT/f'{name}.png',dpi=140);fig.savefig(OUT/f'{name}.svg');plt.close(fig)
    plot(['cash','net','cum_sales','sales','purchases','hire'],['Cassa regolata a fine giornata','Delta netto di cassa','Incassi cumulati','Vendite giornaliere','Acquisti giornalieri','Costo assunzioni giornaliero'],'economia')
    plot(['MELON','WHEAT','STRAWBERRY','COW','SHEEP','pastures'],['Piante di meloni','Piante di grano','Piante di fragole','Mucche','Pecore','Pascoli'],'produzione')
    plot(['hands','CARE','WATER','HARVEST','MOVE_share','PASS_share'],['Manovali','CARE eseguiti','WATER eseguiti','HARVEST eseguiti','MOVE / comandi richiesti (%)','PASS / comandi richiesti (%)'],'lavoro')
    fig,axes=plt.subplots(1,2,figsize=(12,4),layout='constrained')
    for i in [0,3]:
        for ax,key in zip(axes,['cash','net']):ax.plot(range(1,31),[d[key]['mean'] for d in ag[i]],label=NAMES[i],color=COLORS[i],lw=2)
    for ax,title in zip(axes,['Cassa · stesso mercato per partita','Delta giornaliero · confronto locale']):
        ax.set_title(title);ax.axvline(11.5,color='#333',ls=':');ax.grid(alpha=.2);ax.legend(fontsize=8);ax.set_xlabel('Giorno')
    fig.savefig(OUT/'confronto_locale.png',dpi=140);plt.close(fig)
    wins=sum(p['sides']['assisted']['reward']>p['sides']['v4d']['reward'] for p in local)
    mean_cash=ag[0][29]['cash']['mean'];ref_cash=ag[3][29]['cash']['mean']
    summary=dict(cash=mean_cash,v4d_cash=ref_cash,paired_gap_pct=100*(mean_cash/ref_cash-1),wins=wins,
                 core_errors=sum(p['core_errors'] for p in local),incomplete_cases=sum(p['incomplete_missions']>0 for p in local),
                 crop_deaths=sum(len(p['sides']['assisted']['crop_starvation']) for p in local),
                 animal_escapes=sum(len(p['sides']['assisted']['ledger']['animal_escapes']) for p in local),
                 topology_counts={},max_call_seconds=max(p['max_call_seconds'] for p in local))
    for p in local:
        topology=str(p['sides']['assisted']['daily'][-1]['pasture_topology'])
        summary['topology_counts'][topology]=summary['topology_counts'].get(topology,0)+1
    lines=['# Nuova 770 assistita rispetto ai Top770 · KPI D1–D30','',
           '**Candidata analizzata:** `submission_codex_e18_770_assisted_start_v1_candidate.py`, lo stesso file del test D11, senza modifiche. Guida V4D fino a D11; core parametrico V2 da D12.','',
           '## Risultato principale','',
           f'L’avvio conserva il raccolto di D11. A fine partita la candidata raggiunge **{num(mean_cash)}** di cassa media contro **{num(ref_cash)}** della V4D avversaria ({num(summary["paired_gap_pct"])}%; {wins}/14 vittorie locali). Il dato competitivo confrontabile è questo confronto diretto. Le curve Top descrivono invece traiettorie storiche in mercati e contro avversari diversi.','',
           'Il passaggio di controllo è il confine D11/D12, indicato nei grafici. L’esperimento estende esattamente i prefissi già verificati; le 264 azioni iniziali coincidono in tutte le 14 partite. Non si attribuisce automaticamente ogni divergenza successiva al solo cambio di controller: anche stato ereditato e interazioni di mercato contribuiscono.','',
           '## Traguardi produttivi e monetari','',
           '| KPI medio | 770 assistita, locale | Top770-001, storico | Top770-002, storico |','|---|---:|---:|---:|']
    for day,key,title in [(1,'MELON','Meloni D1'),(10,'STRAWBERRY','Fragole D10'),(11,'net','Delta di cassa D11'),(12,'net','Delta di cassa D12'),(15,'STRAWBERRY','Fragole D15'),(20,'STRAWBERRY','Fragole D20'),(20,'COW','Mucche D20'),(30,'COW','Mucche D30'),(30,'SHEEP','Pecore D30'),(30,'cash','Cassa D30 — mercati differenti')]:
        lines.append('| '+title+' | '+' | '.join(num(a[day-1][key]['mean']) for a in ag[:3])+' |')
    lines+=['','![Composizione produttiva](produzione.png)','','## D12–D30: utilizzo del capitale iniziale','',
            'Le differenze seguenti sono osservazioni sui campioni, non stime causali di superiorità rispetto ai Top.','']
    for day in [12,15,20,30]:
        lines.append(f'- **D{day}:** fragole '+ ' / '.join(num(a[day-1]['STRAWBERRY']['mean']) for a in ag[:3])+', mucche '+ ' / '.join(num(a[day-1]['COW']['mean']) for a in ag[:3])+', manovali '+ ' / '.join(num(a[day-1]['hands']['mean']) for a in ag[:3])+'. Ordine: nuova 770 / Top001 / Top002.')
    lines+=['', '### Lettura delle divergenze', '',
            f'**Il primo stacco produttivo è già a D12.** Le fragole della candidata passano da {num(ag[0][10]["STRAWBERRY"]["mean"])} a {num(ag[0][11]["STRAWBERRY"]["mean"])}; Top001 passa da {num(ag[1][10]["STRAWBERRY"]["mean"])} a {num(ag[1][11]["STRAWBERRY"]["mean"])} e Top002 da {num(ag[2][10]["STRAWBERRY"]["mean"])} a {num(ag[2][11]["STRAWBERRY"]["mean"])}. Il capitale iniziale è disponibile, ma l’espansione della produzione ricorrente procede diversamente.', '',
            f'**La composizione successiva si separa dai Top.** A D20 la nuova 770 ha {num(ag[0][19]["WHEAT"]["mean"])} grani e {num(ag[0][19]["MELON"]["mean"])} meloni; nei Top i grani sono {num(ag[1][19]["WHEAT"]["mean"])} / {num(ag[2][19]["WHEAT"]["mean"])} e i meloni {num(ag[1][19]["MELON"]["mean"])} / {num(ag[2][19]["MELON"]["mean"])}. Questo cambia autoproduzione di mangime, durata dei cicli e fabbisogno di servizio.', '',
            f'**Anche il servizio agli animali cambia al passaggio.** CARE eseguiti a D12: {num(ag[0][11]["CARE"]["mean"])} contro {num(ag[1][11]["CARE"]["mean"])} / {num(ag[2][11]["CARE"]["mean"])} nei Top. Le consistenze animali diverse richiedono cautela, ma il salto interno della candidata da D11 ({num(ag[0][10]["CARE"]["mean"])}) segnala una continuità operativa da migliorare.', '',
            f'Il core registra in media {num(mean(p["core_metrics"].get("growth_rejected_day_route",0) for p in local))} rifiuti nelle valutazioni di crescita per il certificato dei percorsi giornalieri e {num(mean(p["core_metrics"].get("jobs_at_refresh",0) for p in local))} missioni attive ai refresh. Sono contatori di valutazioni/eventi ripetuti, non altrettante opportunità economiche indipendenti. Insieme ai KPI suggeriscono di verificare il coordinamento di percorsi, servizi e nuove piantagioni; non dimostrano che basti allentare i vincoli.', '',
            '**Priorità suggerita:** mantenere l’apertura D1–D11 e isolare il passaggio D12–D15: continuità di CARE, consegna delle scorte ereditate, ammissione delle fragole e uso delle nuove superfici. Verificare poi la resa e i ricavi per prodotto fino a D30. Evitare di ricopiare i volumi dei Top come obiettivi economici senza tener conto del mercato locale.', '']
    lines+=['','| Fase / serie | Vendite | Acquisti | Assunzioni | Terreni | Delta cassa | Fragole raccolte | Latte raccolto |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for start,end in [(1,11),(12,20),(21,30)]:
        for i,name in enumerate(NAMES[:3]):
            keys=['sales','purchases','hire','land','net','yield_STRAWBERRY','yield_MILK']
            lines.append(f'| D{start}–D{end} {name} | '+' | '.join(num(sum(d[k]['mean'] for d in ag[i][start-1:end])) for k in keys)+' |')
    lines+=['','![Economia](economia.png)','','## Confronto locale di controllo contro V4D','',
            'Stessi 7 semi di sviluppo 180903001–180903007, entrambe le posizioni. V4D è l’avversaria effettiva, quindi domanda e offerta sono quelle della stessa partita. Le due curve partono dallo stesso risultato D11; questo confronto misura se il vantaggio iniziale viene mantenuto durante la continuazione.','',
            '![Confronto diretto locale](confronto_locale.png)','','| Seed / posizione | Nuova 770 | V4D avversaria | Delta | Missioni residue |','|---|---:|---:|---:|---:|']
    for p in local:
        a=p['sides']['assisted']['reward'];b=p['sides']['v4d']['reward']
        lines.append(f'| {p["seed"]} / {p["seat"]} | {num(a)} | {num(b)} | {num(a-b)} | {p["incomplete_missions"]} |')
    lines+=['','## Lavoro, servizi e chiusura','',f'Errori registrati dal core: **{summary["core_errors"]}**. Morti di colture per mancata irrigazione: **{summary["crop_deaths"]}**; fughe di animali: **{summary["animal_escapes"]}**. Partite con missioni residue al termine: **{summary["incomplete_cases"]}/14**. Il conteggio delle missioni non misura da solo il valore economico lasciato in campo.','',
            'Topologie finali osservate: '+str(summary['topology_counts'])+'.','',
            '![Lavoro e servizi](lavoro.png)','','Le azioni di servizio sono esecuzioni effettive ricostruite dal motore. MOVE e PASS sono quote dei comandi richiesti: non equivalgono automaticamente a spreco, perché dipendono anche da percorsi e disponibilità del lavoro.','',
            '| Serie | Scorte nel deposito a D30 | Scorte trasportate a D30 | Produzione rimasta sulle caselle |','|---|---|---|---|']
    for name,group in zip(NAMES,groups):
        def avg_inventory(key):
            keys=sorted(set(k for p in group for k in p['terminal'].get(key,{})))
            return ', '.join(k+': '+num(mean(p['terminal'].get(key,{}).get(k,0) for p in group)) for k in keys) or '0'
        lines.append('| '+name+' | '+' | '.join(avg_inventory(k) for k in ['shed','carried','tile_yield_units'])+' |')
    lines+=['','## KPI giornalieri D1–D30','',
            'Ogni cella contiene **770 assistita / Top001 / Top002**. Cassa dopo il regolamento di tutti i batch del giorno; gli altri stock sono al checkpoint D×24−1, prima del refresh (D30 terminale).','',
            '| Giorno | Cassa | Fragole | Mucche | Manovali | CARE | WATER | HARVEST |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for d in range(30):lines.append(f'| {d+1} | '+' | '.join(' / '.join(num(a[d][k]['mean']) for a in ag[:3]) for k in ['cash','STRAWBERRY','COW','hands','CARE','WATER','HARVEST'])+' |')
    lines+=['','## Provenienza e limiti','',
            '- Nuova 770: 14 partite complete nel motore reale, orizzonte 720 step e 719 batch. Riconciliazione contabile di entrambi i lati e verifica delle perdite biologiche.',
            '- Top770-001: gli stessi cinque replay '+', '.join(str(p['episode_id']) for p in top1)+'.',
            '- Top770-002: gli stessi quattro replay '+', '.join(str(p['episode_id']) for p in top2)+'. Il quinto replay 10–7–0 resta escluso secondo il criterio topologico precedente.',
            '- I Top sono campioni già utilizzati, non nuovi holdout. Nessun nuovo episodio esterno acquisito e nessuna submission effettuata.',
            '- I corpus esterni differiscono per semi, avversari, mercati e composizione: Top002 usa anche oche. Le differenze monetarie tra corpus non costituiscono una classifica.',
            '- L’etichetta Top770 identifica i corpus e la configurazione finale selezionata, non garantisce 14 pascoli in ogni istante: le curve riportano anche le deviazioni transitorie effettivamente osservate.',
            '- Cassa giornaliera ricostruita dai flussi e riconciliata alla chiusura; bande dei grafici minimo–massimo, non intervalli di confidenza.',
            '- Il confronto non modifica il codice. Le priorità di intervento vanno decise dai risultati della continuazione, senza rimettere in discussione l’apertura già verificata salvo nuove evidenze.','',
            '[Aggregati giornalieri](aggregati.json) · [Sintesi numerica](summary.json) · [Manifest delle fonti](manifest.json).','']
    md=OUT/'REPORT_NUOVA_770_VS_TOP770_D1_D30_IT.md';md.write_text('\n'.join(lines),encoding='utf-8')
    html=MarkdownIt().enable('table').render(md.read_text(encoding='utf-8'))
    for p in OUT.glob('*.png'):html=html.replace(f'src="{p.name}"','src="data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()+'"')
    css='body{max-width:1200px;margin:40px auto;padding:0 24px;font:16px/1.6 system-ui;color:#243445}img{max-width:100%}h2{margin-top:2em}table{display:block;overflow:auto;border-collapse:collapse;font-size:13px}td,th{padding:7px 10px;border-bottom:1px solid #ddd;white-space:nowrap;text-align:right}td:first-child,th:first-child{text-align:left}th{background:#edf2f7}'
    md.with_suffix('.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nuova 770 vs Top770 · D1–D30</title><style>'+css+'</style><body>'+html+'</body></html>',encoding='utf-8')
    (OUT/'aggregati.json').write_text(json.dumps(dict(zip(NAMES,ag)),indent=2)+'\n')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    sources=TOP+paths+[Path(__file__),Path(__file__).with_name('run_assisted_770_d30.py'),ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py']
    (OUT/'manifest.json').write_text(json.dumps(dict(cohort_sizes=[14,5,4,14],new_external_episodes=False,source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},output_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
