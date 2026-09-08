"""Two reproducible KPI reports with paired V4D controls and Q0 charts."""
from collections import Counter
import json
from pathlib import Path
from statistics import mean,median
import os
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parents[5]/'scratch/matplotlib_kpi'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from docs.model_specs.codex.e19.tools.run_paired_kpi_v4d import OUT,BUNDLES

REPORT=OUT.parents[2]/'reports/kpi_v4d_20260907'
CROPS=['WHEAT','CARROT','MELON','TOMATO','STRAWBERRY']
COLORS=['#c49a35','#ef873b','#49a568','#9374b5','#da5c72']

def num(x):return f'{x:,.1f}'.replace(',','X').replace('.',',').replace('X','.')
def money(x):return f'{x:,.0f}'.replace(',','.')

def metrics(side):
    out=[];cum=Counter()
    for i,(snap,flow) in enumerate(zip(side['daily'],side['ledger']['daily'])):
        values=dict(cash=snap['money'],hands=snap['hands'],cows=snap['animals']['COW'],
            sheep=snap['animals']['SHEEP'],crops=snap['crop_tiles'],q0_crops=snap['q0_crop_tiles'],
            q0_animals=snap['q0_animals_total'],q0_pastures=snap['q0_pastures'],
            pastures=snap['livestock_structures'],unfed=snap['unfed'],uncared=snap['uncared'])
        values.update({f'crop_{c}':snap['crops'].get(c,0) for c in CROPS})
        values.update({f'q0_{c}':snap['q0_crops'].get(c,0) for c in CROPS})
        for op in ['PASS','MOVE']:
            values[op]=flow['requested_actions'].get(op,0)
        values['pass_share']=100*values['PASS']/max(1,sum(flow['requested_actions'].values()))
        for op in ['FEED','CARE','WATER','HARVEST']:
            values[op]=flow['executed_actions'].get(op,0)
        values['sales']=sum(flow['sales_cash'].values())
        values['purchases']=sum(flow['purchase_cash'].values())
        values['hire']=flow['hire_cash'];values['land']=flow['land_cash']
        values['unit_cash']=flow['unit_cash_delta']
        values['feed_bought']=flow['purchase_cash'].get('BUY_PRODUCT:WHEAT',0)
        values['animal_bought']=sum(v for k,v in flow['purchase_cash'].items() if k.startswith('BUY_ANIMAL:'))
        values['seed_bought']=sum(v for k,v in flow['purchase_cash'].items() if k.startswith('BUY_SEED:'))
        for c in CROPS+['MILK','WOOL','FERTILIZER']:
            values['sold_'+c]=flow['sales_cash'].get(c,0)
            values['harvest_'+c]=flow['harvested'].get(c,0)
        for k in ['sales','purchases','hire','land','unit_cash','feed_bought','animal_bought','seed_bought','PASS','MOVE']:
            cum[k]+=values[k];values['cum_'+k]=cum[k]
        values['settled_cash']=side['ledger']['initial_cash']+cum['sales']-cum['purchases']-cum['hire']-cum['land']+cum['unit_cash']
        out.append(values)
    assert out[-1]['settled_cash']==side['reward']
    return out

def aggregate(rows):
    return [{k:dict(mean=mean(r[i][k] for r in rows),median=median(r[i][k] for r in rows),
             min=min(r[i][k] for r in rows),max=max(r[i][k] for r in rows)) for k in rows[0][i]} for i in range(30)]

def chart_trends(top,ag,keys,titles,name,end=30):
    fig,axes=plt.subplots(3,2,figsize=(13,10),layout='constrained')
    days=np.arange(1,end+1)
    for ax,key,title in zip(axes.flat,keys,titles):
        for side,color,label in [('parametric','#176b9b',f'Parametrico {top} V2'),('v4d','#bd512f','Campione V4D')]:
            rows=ag[side][:end]
            ax.plot(days,[r[key]['mean'] for r in rows],color=color,label=label,lw=2)
            ax.fill_between(days,[r[key]['min'] for r in rows],[r[key]['max'] for r in rows],alpha=.10,color=color)
        ax.set_title(title,loc='left',fontsize=11);ax.grid(alpha=.2);ax.set_xlabel('Giorno')
        ax.ticklabel_format(axis='y',style='plain');ax.set_xlim(1,end)
    axes.flat[0].legend(fontsize=9)
    fig.suptitle(f'{top} contro V4D | media e intervallo min–max su 14 partite\nStesse partite, entrambi i ruoli; ombreggiatura = variabilità, non intervallo di confidenza',fontsize=13)
    fig.savefig(REPORT/f'{top}_{name}.png',dpi=150);fig.savefig(REPORT/f'{top}_{name}.svg');plt.close(fig)

def q0_charts(top,ag,cases):
    fig,axes=plt.subplots(2,2,figsize=(13,8),layout='constrained')
    for i,side in enumerate(['parametric','v4d']):
        label=f'Parametrico {top}' if side=='parametric' else 'Campione V4D'
        axes[i,0].stackplot(range(1,11),*[[r['q0_'+c]['mean'] for r in ag[side][:10]] for c in CROPS],labels=CROPS,colors=COLORS)
        axes[i,0].set_title(label+' — colture in Q0');axes[i,0].set_ylabel('Caselle medie');axes[i,0].set_ylim(0,25)
        axes[i,1].plot(range(1,11),[r['q0_animals']['mean'] for r in ag[side][:10]],label='Animali Q0',color='#4e6172')
        axes[i,1].plot(range(1,11),[r['q0_pastures']['mean'] for r in ag[side][:10]],label='Pascoli Q0',ls='--',color='#8c638c')
        axes[i,1].set_title(label+' — bestiame in Q0');axes[i,1].legend();axes[i,1].set_ylim(0,10)
    for ax in axes.flat:ax.set_xlabel('Giorno');ax.grid(alpha=.2)
    axes[0,0].legend(ncol=3,fontsize=8,loc='upper right')
    fig.suptitle(f'Impostazione Q0 — {top} e V4D | 14 partite, D1–D10',fontsize=14)
    fig.savefig(REPORT/f'{top}_q0.png',dpi=150);plt.close(fig)
    sample=next(c for c in cases if c['seed']==180903001 and c['seat']==0)
    codes=['EMPTY','WHEAT','CARROT','MELON','TOMATO','STRAWBERRY','COW','SHEEP','PASTURE','WEED']
    palette=['#f1eadc',*COLORS,'#537b9b','#97aaba','#e7c6a9','#777777']
    short=['·','WH','CA','ME','TO','ST','CW','SH','PA','WE']
    fig,axes=plt.subplots(2,3,figsize=(10,7),layout='constrained')
    for i,side in enumerate(['parametric','v4d']):
        for j,day in enumerate([1,5,10]):
            grid=sample['sides'][side]['daily'][day-1]['q0_grid']
            arr=np.array([[codes.index(c) if c in codes else 0 for c in row] for row in grid])
            ax=axes[i,j];ax.imshow(arr,cmap=ListedColormap(palette),vmin=0,vmax=len(codes)-1)
            for y in range(5):
                for x in range(5):ax.text(x,y,short[arr[y,x]],ha='center',va='center',fontsize=10)
            ax.set_xticks(range(5));ax.set_yticks(range(5));ax.set_title(f'{top if side=="parametric" else "V4D"} — D{day}')
    fig.suptitle(f'Q0 osservato, seed 180903001, {top} seat 0 / V4D seat 1\nWH grano · CA carote · ME meloni · TO pomodori · ST fragole\nCW mucche · SH pecore · PA pascolo · WE infestanti · punto = vuoto',fontsize=11)
    fig.savefig(REPORT/f'{top}_q0_map.png',dpi=150);plt.close(fig)

def interpretation(top,ag,rows,cases):
    a,b=ag['parametric'],ag['v4d']
    first={s:[next((i+1 for i,r in enumerate(rs) if r['harvest_MELON']),None) for rs in rr] for s,rr in rows.items()}
    assert all(x is not None for ss in first.values() for x in ss)
    pct=100*(a[-1]['cash']['mean']/b[-1]['cash']['mean']-1)
    lines=['## Lettura dei risultati e ipotesi Q0','',
        f'**L’ipotesi di un avvio Q0 inadeguato è sostenuta dai dati, ma non ancora dimostrata come unica causa del divario.** Il deficit finale medio è {num(pct)}% nel confronto diretto con la V4D.','',
        'Il bootstrap attuale è già pilotato: ammette solo WHEAT/CARROT e mantiene il tetto 2 COW/2 SHEEP fino a `first_confirmed_crop_harvest`. Questa guida impedisce proprio il portafoglio iniziale usato dal campione. Non basta quindi aggiungere più vincoli: occorre cambiare quelli economici e verificare l’effetto separatamente.','',
        '| Evidenza | Parametrico | V4D nella stessa partita |','|---|---:|---:|',
        f'| Meloni Q0 D1, media | {num(a[0]["q0_MELON"]["mean"])} | {num(b[0]["q0_MELON"]["mean"])} |',
        f'| Grano Q0 D1, media | {num(a[0]["q0_WHEAT"]["mean"])} | {num(b[0]["q0_WHEAT"]["mean"])} |',
        f'| COW D5, media | {num(a[4]["cows"]["mean"])} | {num(b[4]["cows"]["mean"])} |',
        f'| Primo raccolto meloni, giorno mediano (min–max) | {num(median(first["parametric"]))} ({min(first["parametric"])}–{max(first["parametric"])}) | {num(median(first["v4d"]))} ({min(first["v4d"])}–{max(first["v4d"])}) |',
        f'| Fragole D10, caselle medie | {num(a[9]["crop_STRAWBERRY"]["mean"])} | {num(b[9]["crop_STRAWBERRY"]["mean"])} |',
        f'| Vendite cumulate D15, media | {money(a[14]["cum_sales"]["mean"])} | {money(b[14]["cum_sales"]["mean"])} |',
        f'| Costo manovali D1–D10, media | {money(a[9]["cum_hire"]["mean"])} | {money(b[9]["cum_hire"]["mean"])} |','',
        'La maggiore liquidità iniziale del parametrico non è un vantaggio sufficiente: il campione investe prima nei meloni e prepara prima le fragole. Il ritardo dei raccolti osservato rende plausibile una propagazione del ritardo verso incassi e reinvestimenti. Anche la composizione successiva diverge: la sola correzione di D1 potrebbe non recuperare tutta la stagione.','',
        '**Controevidenza da conservare:** la vecchia variante E18 V19 (profilo V7, pesi grano:meloni 1:2) era già stata respinta: quattro casi, cassa 60.828 contro E18.16 e 57.245 contro E18.2, in entrambi i ruoli. Nel primo caso piantava già 10 meloni D1 e arrivava a 12 D2, ma D10 aveva 23 meloni, 11 grani e soltanto 1 fragola. È un core precedente, quindi non un’ablation causale di questa V2; dimostra però che ripetere soltanto il cambio dei pesi iniziali non è una soluzione già validata. Fonte: [gate V19](../../../e18/artifacts/derived/E18_CLOSEOUT_GATE_V19_INITIAL_PORTFOLIO_20260907.json) e [worklog E18](../../../e18/reports/E18_PARAMETRIC_RELEASE_WORKLOG_20260907_IT.md).','',
        '### Scomposizione contabile del divario finale','',
        'Differenze medie di contributo alla cassa: parametrico meno V4D. Un numero positivo aiuta il parametrico. Vendite e acquisti sono lordi: per esempio comprare e rivendere grano non va contato come ricavo netto.','',
        '| Componente | Contributo al divario |','|---|---:|']
    bridge=[]
    for key,sign,label in [('cum_sales',1,'Vendite'),('cum_purchases',-1,'Acquisti'),('cum_hire',-1,'Manovali'),('cum_land',-1,'Terreni'),('cum_unit_cash',1,'Operazioni sulle caselle')]:
        v=sign*(a[-1][key]['mean']-b[-1][key]['mean']);bridge.append(v);lines.append(f'| {label} | {num(v)} |')
    delta=a[-1]['cash']['mean']-b[-1]['cash']['mean'];assert abs(sum(bridge)-delta)<1e-6
    lines += [f'| **Totale cassa finale** | **{num(delta)}** |','',
        '### Guida iniziale da sottoporre a prova','',
        '1. Usare il portafoglio Q0 della V4D come ipotesi di partenza: 12 meloni, 7 grani e 2 COW/2 SHEEP iniziali, subordinati a budget e certificazione delle cure. Sono quantità osservate nel campione, non nuovi obiettivi già validati per ogni geometria.',
        '2. Riservare esplicitamente capitale e capacità di lavoro per quel portafoglio; impedire che grano opportunistico riempia tutta Q0. Portare l’obiettivo di lavoro dai compiti effettivi, confrontando il costo con la V4D.',
        '3. Verificare una transizione osservabile verso il portafoglio successivo, incluse mucche e fragole. Il primo raccolto di una coltura veloce, da solo, non certifica che l’impostazione economica sia quella desiderata.',
        '4. Isolare gli effetti: A = core congelato; B = solo mix iniziale corretto; C = solo crescita bestiame/lavoro corretta; D = combinazione dopo aver misurato B e C. Stessi avversari, entrambi i ruoli, più campione non usato nel tuning prima di una promozione.',
        '5. Mantenere V4D come gate competitivo. Richiedere sicurezza, flussi di cassa riconciliati e risultati diretti competitivi; non promuovere una variante perché batte soltanto la 770 o la 662 deboli.','',
        '**In questo lavoro non sono state modificate né pubblicate strategie.** Le proposte sono esperimenti da progettare dopo questi report.','']
    return lines

def export_html(path):
    import base64
    from markdown_it import MarkdownIt
    body=MarkdownIt('commonmark').enable('table').render(path.read_text(encoding='utf-8'))
    for img in REPORT.glob(path.name.split('_')[1]+'_*.png'):
        body=body.replace(f'src="{img.name}"',f'src="data:image/png;base64,{base64.b64encode(img.read_bytes()).decode()}"')
    css='body{font:16px/1.6 system-ui,sans-serif;color:#243445;max-width:1200px;margin:40px auto;padding:0 24px}h1,h2,h3{line-height:1.25}h2{margin-top:2.5em;border-top:1px solid #ccd6df;padding-top:1em}img{max-width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:13px;display:block;overflow-x:auto}th,td{border-bottom:1px solid #dce3e9;padding:7px 10px;text-align:right;white-space:nowrap}th:first-child,td:first-child{text-align:left}th{background:#eaf0f5}code{overflow-wrap:anywhere;white-space:normal;background:#f3f5f7}a{color:#176b9b}@media print{body{font-size:11px}h2{break-before:auto}img,table{break-inside:avoid}}'
    path.with_suffix('.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+path.stem+'</title><style>'+css+'</style><body>'+body+'</body></html>',encoding='utf-8')

def main():
    REPORT.mkdir(parents=True,exist_ok=True)
    for top in ['770','662']:
        cases=[json.loads(p.read_text()) for p in sorted(OUT.glob(f'{top}_*.json'))]
        assert len(cases)==14 and all(c['reproduces_frozen_gate'] for c in cases)
        assert len({(c['seed'],c['seat']) for c in cases})==14
        rows={s:[metrics(c['sides'][s]) for c in cases] for s in ['parametric','v4d']}
        ag={s:aggregate(rows[s]) for s in rows}
        (REPORT/f'{top}_aggregates.json').write_text(json.dumps(ag,indent=2)+'\n')
        chart_trends(top,ag,['cash','cows','crops','hands','cum_sales','pass_share'],
            ['Cassa ai checkpoint','Mucche presenti','Colture presenti','Manovali presenti','Incassi cumulati da vendite','PASS / comandi richiesti (%)'],'trend')
        chart_trends(top,ag,['cash','q0_animals','cum_sales','cum_feed_bought','HARVEST','CARE'],
            ['Cassa ai checkpoint','Animali in Q0','Incassi cumulati','Spesa cumulata per grano acquistato','HARVEST eseguiti al giorno','CARE eseguiti al giorno'],'startup',10)
        q0_charts(top,ag,cases)
        lines=[f'# KPI del parametrico {top} V2 rispetto al campione E18.2 V4D','',
            'Confronto locale riprodotto il 2026-09-07. Due lati delle stesse 14 partite: sette seed development, entrambi i ruoli. Nessuna modifica alle strategie e nessun nuovo campione esterno consumato.','',
            f'Il parametrico termina con cassa media **{money(ag["parametric"][-1]["cash"]["mean"])}**, contro **{money(ag["v4d"][-1]["cash"]["mean"])}** della V4D. Le 14 partite sono tutte sconfitte. Il riferimento è il campione effettivo, non un altro core parametrico.','',
            *interpretation(top,ag,rows,cases),f'![Trend KPI {top}]({top}_trend.png)','',
            '## Metodo e perimetro','',
            f'- Modello: `submission/{BUNDLES[top]}`. Profilo iniziale e core congelati V2; per 770 si usa il controllo sullo stesso core della E19 V2, non la vecchia E18 V24.',
            '- Campione: `submission/submission_codex_e18_2_capacity_governed_v4d.py`, invariato.',
            '- Seed 180903001–180903007, seat 0 e 1. Ogni partita riproduce hash di tutte le azioni e ricavi finali del gate precedente.',
            '- Cassa di entrambi i giocatori ricostruita dal motore per 719 batch per partita; nessuna discrepanza ammessa.',
            '- Stock e Q0 ai checkpoint indice D×24−1: ultima osservazione prima del refresh, con D30 terminale. I flussi giornalieri coprono tutti i batch del giorno: possono includere un batch successivo al checkpoint dello stock.',
            '- Curve = medie; bande = minimo/massimo, non intervalli di confidenza. Q0 = quadrante NW, coordinate x,y da 0 a 4. Mappe = un caso dichiarato, non una configurazione media.',
            '- Le due serie V4D dei due report sono i rispettivi avversari effettivi: non vanno unite fingendo identiche condizioni di mercato. Il test descrive differenze; non identifica da solo una causa.','',
            '## Avvio D1–D10','',f'![Avvio {top}]({top}_startup.png)','',
            '| Giorno | Cassa param./V4D | COW param./V4D | SHEEP param./V4D | Colture param./V4D | Manovali param./V4D | Incassi cumulati param./V4D |',
            '|---|---:|---:|---:|---:|---:|---:|']
        for day in range(1,11):
            a,b=ag['parametric'][day-1],ag['v4d'][day-1]
            lines.append('| '+str(day)+' | '+' | '.join(f'{num(a[k]["mean"])} / {num(b[k]["mean"])}' for k in ['cash','cows','sheep','crops','hands','cum_sales'])+' |')
        lines+=['','## Q0: composizione e geometria','',f'![Composizione Q0 {top}]({top}_q0.png)','',f'![Mappa Q0 {top}]({top}_q0_map.png)','',
            '| Giorno / modello | Grano Q0 | Carote Q0 | Meloni Q0 | Pomodori Q0 | Fragole Q0 | Animali Q0 |','|---|---:|---:|---:|---:|---:|---:|']
        for day in [1,3,5,7,10]:
            for side,label in [('parametric',top),('v4d','V4D')]:
                r=ag[side][day-1];lines.append(f'| D{day} {label} | '+' | '.join(num(r[k]['mean']) for k in [*['q0_'+c for c in CROPS],'q0_animals'])+' |')
        lines+=['','## Impiego del capitale e vendite','',
            'Valori cumulati medi, su giornate complete. La voce operazioni sulle caselle include costruzioni e altri effetti monetari delle azioni.','',
            '| Termine / modello | Vendite | Acquisti totali | Animali | Semi | Grano comprato | Manovali | Terreni | Operazioni caselle (saldo) | Cassa riconciliata |',
            '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
        for day in [1,5,10,20,30]:
            for side,label in [('parametric',top),('v4d','V4D')]:
                r=ag[side][day-1];lines.append(f'| D{day} {label} | '+' | '.join(money(r[k]['mean']) for k in ['cum_sales','cum_purchases','cum_animal_bought','cum_seed_bought','cum_feed_bought','cum_hire','cum_land','cum_unit_cash','settled_cash'])+' |')
        lines+=['','### Origine degli incassi nella stagione','',
            'Vendite lorde medie per prodotto. Il grano comprende compravendite, non solo produzione propria; confrontarlo insieme alla spesa per grano della tabella precedente.','',
            '| Prodotto | Parametrico | V4D | Differenza |','|---|---:|---:|---:|']
        for product in CROPS+['MILK','WOOL','FERTILIZER']:
            av=sum(r['sold_'+product]['mean'] for r in ag['parametric']);bv=sum(r['sold_'+product]['mean'] for r in ag['v4d'])
            lines.append(f'| {product} | {money(av)} | {money(bv)} | {money(av-bv)} |')
        lines+=['','### Composizione produttiva dopo l’avvio','',
            '| Giorno / modello | Grano | Carote | Meloni | Pomodori | Fragole | COW | SHEEP |','|---|---:|---:|---:|---:|---:|---:|---:|']
        for day in [10,15,20,25,30]:
            for side,label in [('parametric',top),('v4d','V4D')]:
                r=ag[side][day-1];lines.append(f'| D{day} {label} | '+' | '.join(num(r[k]['mean']) for k in [*['crop_'+c for c in CROPS],'cows','sheep'])+' |')
        lines+=['','### Stato finale e controlli','',
            '| Modello | Pascoli Q0/Q1/Q2/Q3 medi | Perdite colture totali | Fughe animali totali |','|---|---|---:|---:|']
        for side,label in [('parametric',top),('v4d','V4D')]:
            shape='/'.join(num(mean(c['sides'][side]['daily'][-1]['pasture_topology'][f'Q{i}'] for c in cases)) for i in range(4))
            deaths=sum(len(c['sides'][side]['crop_starvation']) for c in cases);escapes=sum(len(c['sides'][side]['ledger']['animal_escapes']) for c in cases)
            lines.append(f'| {label} | {shape} | {deaths} | {escapes} |')
        lines+=['','## Trend completo D1–D30','',
            '| Giorno | Cassa param./V4D | FEED param./V4D | CARE param./V4D | WATER param./V4D | HARVEST param./V4D | MOVE param./V4D | PASS % param./V4D |',
            '|---|---:|---:|---:|---:|---:|---:|---:|']
        for i in range(30):
            a,b=ag['parametric'][i],ag['v4d'][i]
            lines.append(f'| {i+1} | '+' | '.join(f'{num(a[k]["mean"])} / {num(b[k]["mean"])}' for k in ['cash','FEED','CARE','WATER','HARVEST','MOVE','pass_share'])+' |')
        lines+=['','## Dati e riproducibilità','',
            f'Aggregati: [{top}_aggregates.json]({top}_aggregates.json). Dati per partita: `../../artifacts/derived/paired_kpi_v4d_20260907/{top}_SEED_SEAT.json`.',
            f'Bundle parametrico SHA256: `{cases[0]["bundle_sha256"]}`.',f'Campione SHA256: `{cases[0]["champion_sha256"]}`.',
            'Runner `tools/run_paired_kpi_v4d.py`; generatore `tools/build_paired_kpi_reports.py`. Le osservazioni interpretative sono nel riepilogo iniziale aggiunto dopo l’esame dei risultati.','']
        path=REPORT/f'REPORT_{top}_VS_V4D_IT.md'
        path.write_text('\n'.join(lines),encoding='utf-8');export_html(path)
        print(top,'reports built',flush=True)

if __name__=='__main__':main()
