"""Historical, non-matched trend report requested by the owner."""
import base64
import hashlib
import json
import os
from pathlib import Path
from statistics import mean,median
ROOT=Path(__file__).resolve().parents[5]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'scratch/matplotlib_kpi'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt

BASE=ROOT/'docs/model_specs/codex/e19'
OUT=BASE/'reports/v4c_top770_20260907'
SOURCES=[ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_26_JESSE_770_D01_D30_CLOSURE.json',ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_31_EXTERNAL_TOP002_FULL_20260906.json']
NAMES=['V4C · locale INERT_PASS','Top770-001 · storico esterno','Top770-002 · storico esterno']
COLORS=['#176b9b','#bd512f','#7755a8']
def num(x):return f'{x:,.1f}'.replace(',','X').replace('.',',').replace('X','.')

def rows(profile):
    out=[];sales=0
    for s,f in zip(profile['daily'],profile['ledger']['daily']):
        sales+=sum(f['sales_cash'].values())
        r=dict(cash=s['money'],hands=s['hands'],crops=s['crop_tiles'],animals=s['occupied_livestock_tiles'],
            **s['crops'],**s['animals'],cum_sales=sales,PASS=f['requested_actions'].get('PASS',0),MOVE=f['requested_actions'].get('MOVE',0),
            **{k:f['executed_actions'].get(k,0) for k in ['FEED','CARE','WATER','HARVEST']})
        out.append(r)
    return out

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    paths=sorted((BASE/'artifacts/derived/v4c_top770_20260907').glob('*.json'))
    v=[json.loads(p.read_text()) for p in paths];assert len(v)==6 and all(r['historical_parity'] for r in v)
    top1=json.loads(SOURCES[0].read_text())['jesse']
    full=json.loads(SOURCES[1].read_text());top2=[p for p in full['profiles'] if p['exact770_final']]
    assert len(top1)==5 and len(top2)==4
    groups=[v,top1,top2]
    ag=[]
    for group in groups:
        rr=[rows(p) for p in group]
        ag.append([{k:dict(mean=mean(r[i][k] for r in rr),min=min(r[i][k] for r in rr),max=max(r[i][k] for r in rr)) for k in rr[0][i]} for i in range(30)])
    def plot(keys,titles,end,name):
        fig,axs=plt.subplots(3,2,figsize=(13,10),layout='constrained')
        for ax,k,title in zip(axs.flat,keys,titles):
            for a,label,color in zip(ag,NAMES,COLORS):
                ax.plot(range(1,end+1),[r[k]['mean'] for r in a[:end]],label=label,color=color,lw=2)
                ax.fill_between(range(1,end+1),[r[k]['min'] for r in a[:end]],[r[k]['max'] for r in a[:end]],color=color,alpha=.08)
            ax.set_title(title,loc='left');ax.set_xlabel('Giorno');ax.set_xlim(1,end);ax.grid(alpha=.2)
        axs.flat[0].legend(fontsize=8)
        fig.suptitle('V4C e Top770 — confronto storico descrittivo\nAvversari, seed e mercati diversi: le curve monetarie non misurano superiorità',fontsize=13)
        fig.savefig(OUT/f'{name}.png',dpi=150);fig.savefig(OUT/f'{name}.svg');plt.close(fig)
    plot(['cash','COW','SHEEP','STRAWBERRY','hands','cum_sales'],['Cassa osservata','Mucche','Pecore','Caselle di fragole','Manovali','Incassi cumulati'],30,'trend')
    plot(['MELON','WHEAT','COW','STRAWBERRY','CARE','HARVEST'],['Caselle di meloni','Caselle di grano','Mucche','Caselle di fragole','CARE eseguiti','HARVEST eseguiti'],15,'avvio')
    plot(['cash','crops','GOOSE','MOVE','PASS','HARVEST'],['Cassa osservata','Colture presenti','Oche','MOVE richiesti','PASS richiesti','HARVEST eseguiti'],30,'servizi_chiusura')
    lines=['# V4C rispetto ai Top770 — report storico dei KPI','',
        '**Modello analizzato: E17.2 V4C**, `CODEX_E17_2_CAPACITY_AWARE_BATCHED_ROUTING_V4C_D28.json`. È distinto dal campione E18.2 capacity-governed V4D discusso nei report precedenti. Il nome V4C della richiesta è seguito letteralmente.','',
        '**Questo è un confronto descrittivo, non un torneo né una nuova validazione competitiva.** V4C: sei partite locali contro INERT_PASS; Top770: nove replay esterni in due corpus distinti. Differenze di avversario, mercato e seed impediscono di interpretare un maggiore ricavo come superiorità.','',
        '## Risultati principali','',
        'L’avvio V4C è già vicino ai Top: 12 meloni e 7 grani iniziali, quattro mucche D5 e circa venti fragole D10. Tutti raggiungono il primo raccolto dei meloni a D11. Il punto di divergenza da studiare è soprattutto il reinvestimento dopo il primo raccolto e la composizione successiva.','',
        '**Perimetro diverso:** V4C termina con pascoli 7-7-5, 8 COW, 10 SHEEP e 1 GOOSE nel campione locale, contro i pascoli 7-7-0 dei Top selezionati. Ha quindi più strutture e animali: anche questa differenza impedisce di leggere la maggiore cassa come efficienza superiore a parità di risorse.','',
        'La modifica specifica V4C interviene da D28: le somiglianze o differenze di D1–D27 appartengono alla strategia precedente da cui deriva, non al batching V4C. Da D12 V4C torna a piantare meloni, mentre nei due corpus Top i meloni restano assenti e cresce prima la superficie a fragole. Sono scelte diverse da sottoporre a confronto controllato.','',
        '| KPI medio | V4C locale | Top770-001 esterno | Top770-002 esterno |','|---|---:|---:|---:|']
    for day,k,label in [(1,'MELON','Meloni D1'),(1,'WHEAT','Grano D1'),(5,'COW','COW D5'),(10,'COW','COW D10'),(10,'STRAWBERRY','Fragole D10'),(11,'cash','Cassa D11'),(20,'STRAWBERRY','Fragole D20'),(30,'cash','Cassa D30 — non confrontabile come ranking')]:
        lines.append('| '+label+' | '+' | '.join(num(a[day-1][k]['mean']) for a in ag)+' |')
    lines+=['', '### Primo raccolto dei meloni','', '| Serie | Primo giorno di raccolta, mediana (min–max) | Vendite meloni D11, media |','|---|---:|---:|']
    for name,group in zip(NAMES,groups):
        first=[next((i+1 for i,f in enumerate(p['ledger']['daily']) if f['harvested'].get('MELON',0)),31) for p in group]
        cash=mean(p['ledger']['daily'][10]['sales_cash'].get('MELON',0) for p in group)
        lines.append(f'| {name} | {num(median(first))} ({min(first)}–{max(first)}) | {num(cash)} |')
    lines+=['','![Avvio](avvio.png)','','![Trend](trend.png)','',
        '## Popolazioni, identità e provenienza','',
        '- V4C: seed 26090101, 26090102, 26090103, entrambi i ruoli. Tutte le azioni e i ricavi coincidono con il gate storico V4C; contabilità ricostruita e riconciliata per ogni batch.',
        '- Top770-001: cinque replay storici del corpus già esposto, mantenuti integralmente. Alias invariato.',
        '- Top770-002: quattro dei cinque replay dello screening storico hanno topologia finale 770; il quinto 10-7-0 resta documentato nella fonte, escluso dalle curve per il criterio topologico originale, non per il risultato economico.',
        '- I corpus Top sono già consumati: riuso documentale richiesto dal proprietario, nessuna nuova pretesa di holdout e nessuna acquisizione di episodi nuovi.',
        '- Stock al checkpoint D×24−1, prima del refresh; D30 terminale. Flussi su tutti i batch del giorno. Bande minimo–massimo, non intervalli di confidenza.',
        '- Top770 descrive i pascoli: non implica uguaglianza di animali o strutture accessorie. Top770-002 utilizza anche oche.','',
        '| Serie | Episodi / seed |','|---|---|',
        '| V4C | 26090101–26090103, seat 0/1 |',
        '| Top770-001 | '+', '.join(str(p['episode_id']) for p in top1)+' |',
        '| Top770-002 | '+', '.join(str(p['episode_id']) for p in top2)+' |','',
        '## D1–D15: impostazione produttiva','',
        '| Giorno / serie | Grano | Meloni | Fragole | COW | SHEEP | Manovali |','|---|---:|---:|---:|---:|---:|---:|']
    for day in [1,3,5,7,10,11,12,15]:
        for name,a in zip(['V4C','Top001','Top002'],ag):
            lines.append(f'| D{day} {name} | '+' | '.join(num(a[day-1][k]['mean']) for k in ['WHEAT','MELON','STRAWBERRY','COW','SHEEP','hands'])+' |')
    lines+=['','## D1–D30: cassa e servizi','',
        'Ogni cella contiene V4C / Top770-001 / Top770-002.','',
        '| Giorno | Cassa | FEED | CARE | WATER | HARVEST | MOVE | PASS |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for i in range(30):lines.append(f'| {i+1} | '+' | '.join(' / '.join(num(a[i][k]['mean']) for a in ag) for k in ['cash','FEED','CARE','WATER','HARVEST','MOVE','PASS'])+' |')
    lines+=['','![Servizi e chiusura](servizi_chiusura.png)','',
        '## Come usare il confronto','',
        'Confrontare anzitutto i tempi di semina/raccolta, il passaggio a fragole, la crescita delle mucche e l’impiego del lavoro. Per giudicare il miglioramento specifico V4C serve un’ablation contro il suo parent sullo stesso mercato; per giudicare la competitività servono avversari attivi e condizioni confrontabili. Il confronto monetario INERT_PASS/Top esterni non soddisfa nessuna delle due condizioni.',
        'Prima di trasferire indicazioni ai parametrici, verificare separatamente portafoglio iniziale e transizione D5–D15. Non attribuire a una modifica attiva da D28 il gradino dei raccolti a D11.','',
        '## File di evidenza','', '[Aggregati](aggregati.json) · [Manifest e hash](manifest.json). Strategie non modificate; nessuna submission effettuata.','']
    md=OUT/'REPORT_V4C_VS_TOP770_IT.md';md.write_text('\n'.join(lines),encoding='utf-8')
    html=MarkdownIt('commonmark').enable('table').render(md.read_text(encoding='utf-8'))
    for p in OUT.glob('*.png'):html=html.replace(f'src="{p.name}"',f'src="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"')
    css='body{max-width:1200px;margin:40px auto;padding:0 24px;font:16px/1.6 system-ui;color:#243445}img{max-width:100%}h2{margin-top:2em}table{display:block;overflow:auto;border-collapse:collapse;font-size:13px}td,th{padding:7px 10px;border-bottom:1px solid #ddd;white-space:nowrap;text-align:right}td:first-child,th:first-child{text-align:left}th{background:#edf2f7}code{overflow-wrap:anywhere}'
    md.with_suffix('.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>V4C vs Top770</title><style>'+css+'</style><body>'+html+'</body></html>',encoding='utf-8')
    (OUT/'aggregati.json').write_text(json.dumps(dict(zip(NAMES,ag)),indent=2)+'\n')
    source_paths=SOURCES+paths+[Path(__file__),BASE/'tools/run_v4c_historical_kpi.py',ROOT/'docs/model_specs/codex/e17/configs/CODEX_E17_2_CAPACITY_AWARE_BATCHED_ROUTING_V4C_D28.json']
    (OUT/'manifest.json').write_text(json.dumps(dict(historical_only=True,matched_comparison=False,new_holdout=False,cohort_sizes=[6,5,4],sources={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}),indent=2)+'\n')
    print(md,flush=True)

if __name__=='__main__':main()
