"""Audit the frozen 17:00 public cohort; no policy execution or new games."""
import csv,hashlib,json,sys,traceback,inspect
from collections import Counter
from pathlib import Path
from statistics import mean,median
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
OUT=BASE/'reports/external_770_772_774_775'; DERIVED=OUT/'profiles_1700';DERIVED.mkdir(exist_ok=True)
from docs.model_specs.codex.e20.tools.analyze_first_external import profile
from docs.model_specs.codex.e21 import build_trajectory_report as quad
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
MODELS=['770','772','774','775'];COLORS=['#858585','#d18322','#216ec0','#23804c']
PHASES=[('D1–11',0,11),('D12–19',11,19),('D20–29',19,29),('D30',29,30)]

# Public policies can request commands for workers that do not exist. Keep
# these requests in the global KPI and expose their unassignable remainder;
# never invent a quadrant or discard an otherwise complete financial replay.
_qsource=inspect.getsource(quad.profile)
_qsource=_qsource.replace('    rows=[];target=[];last=object()',"    unattributed=[{'MOVE':0,'PASS':0} for _ in range(30)]\n    rows=[];target=[];last=object()")
_old="            if key!='money':assert sum(q[d][key] for q in rows)==s['kpi'][d][key],(label,d,key,sum(q[d][key] for q in rows),s['kpi'][d][key])"
_new="""            if key!='money':
                delta=s['kpi'][d][key]-sum(q[d][key] for q in rows)
                if delta>0 and key in ('MOVE','PASS'):
                    unattributed[d][key]=delta
                else:
                    assert delta==0,(label,d,key,delta)
"""
assert _old in _qsource
_qsource=_qsource.replace(_old,_new).replace("reward=s['reward'],ledger=s['ledger']","unattributed=unattributed,reward=s['reward'],ledger=s['ledger']")
exec(compile(_qsource,'<external-quadrant-attribution>','exec'),quad.__dict__)

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def net(d):return sum(d['sales_cash'].values())-sum(d['purchase_cash'].values())-d['hire_cash']-d['land_cash']+d['unit_cash_delta']
def money(x):return f'{x:,.0f}'.replace(',','.')

def process():
    inventory=read(OUT/'INVENTORY.json');save(OUT/'INVENTORY_1700.json',inventory)
    allrows=[];errors=[]
    for model in MODELS:
        spec=inventory['models'].get(model,{})
        for g in spec.get('games',[]):
            if not g.get('complete') or g.get('error') or g.get('missing_observation_fields'):
                errors.append({'model':model,'episode':g['episode'],'error':'Incomplete or missing fields','record':g});continue
            path=DERIVED/f"{g['episode']}_seat{g['seat']}.json"
            try:
                raw=(ROOT/g['raw_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256']
                if path.exists():
                    row=read(path);assert row['sha256']==g['sha256'] and row['model']==model
                else:
                    r=json.loads(raw);seat=g['seat'];s=profile(r,seat)
                    assert len(s['kpi'])==30 and s['ledger']['cash_parity_errors']==0
                    assert abs(s['ledger']['initial_cash']+sum(net(d) for d in s['ledger']['daily'])-s['reward'])<1e-6
                    # Reuse the previously verified quadrant attribution with
                    # externally supplied metadata and already audited ledger.
                    quad.load=lambda _:({'seed':r['info'].get('seed'),'agents':r['info']['TeamNames'],'opening':[{'topology':g['final_topology'][:3]}]*2},{'sides':[s,s]},r)
                    q,_=quad.profile(model,ROOT/g['raw_path'],seat)
                    own=next(a for a in g['metadata']['agents'] if a['submissionId']==spec['submission_id'])
                    opponent=next(a for a in g['metadata']['agents'] if a['submissionId']!=spec['submission_id'])
                    towns=[];last=None
                    for i,st in enumerate(r['steps']):
                        town=st[seat]['observation']['town']
                        if town!=last:towns.append({'step':i,'day':st[seat]['observation']['day']+1,'town':town});last=town
                    row={'model':model,'version':spec['version'],**g,'profile':s,'quadrants':q['quadrants'],'unattributed':q['unattributed'],
                         'rating_before':own.get('initialScore'),'rating_after':own.get('updatedScore'),
                         'opponent_rating_before':opponent.get('initialScore'),'town_changes':towns}
                    save(path,row)
                allrows.append(row)
                print('VERIFIED',model,g['episode'],flush=True)
            except Exception as exc:
                errors.append({'model':model,'episode':g['episode'],'error':str(exc),'trace':traceback.format_exc()})
                print('ERROR',model,g['episode'],str(exc),flush=True)
    save(OUT/'AUDIT_ERRORS.json',errors)
    return inventory,allrows,errors

def plot(rows,region):
    fig,axes=plt.subplots(6,4,figsize=(18,22),layout='constrained')
    fig.suptitle(f'{region} · replay esterni · 22 KPI D1–D30\nMediana e intervallo interquartile · campioni diversi, confronto descrittivo',fontsize=18)
    for ax,(key,label,unit) in zip(axes.flat,FIELDS):
        if region!='Fattoria' and key=='money':
            ax.text(.5,.5,'Cassa comune\nnon attribuita al quadrante',ha='center',va='center');ax.axis('off');continue
        for model,color in zip(MODELS,COLORS):
            group=[r for r in rows if r['model']==model]
            if not group:continue
            series=[r['profile']['kpi'] if region=='Fattoria' else r['quadrants'][region] for r in group]
            arr=np.array([[d[key] for d in s] for s in series])
            ax.plot(range(1,31),np.median(arr,axis=0),color=color,lw=1.9,label=f'{model} (n={len(group)})')
            ax.fill_between(range(1,31),np.quantile(arr,.25,axis=0),np.quantile(arr,.75,axis=0),color=color,alpha=.10)
        ax.set_title('Caselle coltivate' if key=='crop_tiles' else label,fontsize=10)
        ax.set_xlabel('Giorno');ax.set_ylabel(unit);ax.grid(alpha=.2);ax.set_xlim(1,30)
    for ax in list(axes.flat)[22:]:ax.axis('off')
    h,l=axes.flat[1].get_legend_handles_labels();axes.flat[22].legend(h,l,loc='center',frameon=False)
    fig.savefig(OUT/f'{region}_KPI22.png',dpi=115);plt.close(fig)

def report(inventory,rows,errors):
    summaries={};phase_rows=[];products=[];daily=[];games=[];kpi_phase=[]
    for model in MODELS:
        group=[r for r in rows if r['model']==model]
        if not group:continue
        rewards=[r['profile']['reward'] for r in group]
        margins=[r['profile']['reward']-r['rewards'][1-r['seat']] for r in group]
        latest=max(group,key=lambda r:(r['metadata']['createTime'],r['episode']))
        summaries[model]={'n':len(group),'cash_mean':mean(rewards),'cash_median':median(rewards),'cash_min':min(rewards),'cash_max':max(rewards),
                         'cash_q25':float(np.quantile(rewards,.25)),'cash_q75':float(np.quantile(rewards,.75)),
                         'wins':sum(m>0 for m in margins),'draws':sum(m==0 for m in margins),'margin_mean':mean(margins),
                         'rating_latest_episode':latest['rating_after'],'opponent_rating_mean':mean(r['opponent_rating_before'] for r in group),
                         'latest_episode':latest['episode'],'cutoff_latest_end':latest['metadata']['endTime'],
                         'final_topologies':dict(Counter(str(r['final_topology']) for r in group)),
                         'animal_losses':sum(len(r['profile']['ledger']['animal_escapes']) for r in group),
                         'crop_losses_mean':mean(len(r['profile']['crop_starvation']) for r in group),
                         'unattributed_requests':sum(sum(d.values()) for r in group for d in r.get('unattributed',[]))}
        for phase,start,end in PHASES:
            row={'model':model,'phase':phase}
            for k in ['sales_cash','purchase_cash','hire_cash','land_cash','unit_cash_delta']:
                row[k]=mean(sum(sum(d[k].values()) if isinstance(d[k],dict) else d[k] for d in r['profile']['ledger']['daily'][start:end]) for r in group)
            row['net_cash']=mean(sum(net(d) for d in r['profile']['ledger']['daily'][start:end]) for r in group)
            phase_rows.append(row)
            for region in ['Fattoria','Q0','Q1']:
                for key,_,_ in FIELDS:
                    if key=='money' and region!='Fattoria':continue
                    series=[r['profile']['kpi'] if region=='Fattoria' else r['quadrants'][region] for r in group]
                    values=[mean(d[key] for d in s[start:end]) for s in series]
                    kpi_phase.append({'model':model,'region':region,'phase':phase,'kpi':key,'mean_daily_level':mean(values),'median_daily_level':median(values)})
        for item in ['WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','MILK','WOOL','EGG','FERTILIZER']:
            total=lambda key:sum(d[key].get(item,0) for r in group for d in r['profile']['ledger']['daily'])
            qty=total('sold_units');cash=total('sales_cash')
            products.append({'model':model,'product':item,'mean_harvested':total('harvested')/len(group),'mean_sold':qty/len(group),'mean_sales_cash':cash/len(group),'realized_price_weighted':cash/qty if qty else None})
        for r in group:
            games.append({'model':model,'episode':r['episode'],'seat':r['seat'],'opponent':r['teams'][1-r['seat']],
                          'opponent_submission':r['opponent_submission_id'],'cash':r['profile']['reward'],'opponent_cash':r['rewards'][1-r['seat']],
                          'rating_before':r['rating_before'],'rating_after':r['rating_after'],'opponent_rating_before':r['opponent_rating_before'],
                          'final_topology':str(r['final_topology']),'animal_losses':len(r['profile']['ledger']['animal_escapes']),
                          'crop_losses':len(r['profile']['crop_starvation']),'terminal_shed':json.dumps(r['profile']['terminal']['shed']),
                          'terminal_carried':json.dumps(r['profile']['terminal']['carried'])})
            for region in ['Fattoria','Q0','Q1','Q2','Q3']:
                series=r['profile']['kpi'] if region=='Fattoria' else r['quadrants'][region]
                for d,z in enumerate(series):daily.append({'model':model,'episode':r['episode'],'seat':r['seat'],'region':region,'day':d+1,**{k:z[k] for k,_,_ in FIELDS}})
            for d,z in enumerate(r.get('unattributed',[])):
                if any(z.values()):daily.append({'model':model,'episode':r['episode'],'seat':r['seat'],'region':'NON_ATTRIBUIBILE','day':d+1,**{k:None if k=='money' else z.get(k,0) for k,_,_ in FIELDS}})
    for filename,data in [('DAILY_KPI.csv',daily),('GAMES.csv',games),('PHASE_CASH.csv',phase_rows),('PRODUCTS.csv',products),('PHASE_KPI.csv',kpi_phase)]:
        if data:
            with (OUT/filename).open('w',encoding='utf-8',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    save(OUT/'SUMMARY.json',summaries)
    # Full individual cash paths reveal variability hidden by aggregate curves.
    fig,axes=plt.subplots(2,2,figsize=(15,9),layout='constrained')
    for ax,model,color in zip(axes.flat,MODELS,COLORS):
        group=[r for r in rows if r['model']==model]
        for r in group:ax.plot(range(1,31),[d['money'] for d in r['profile']['kpi']],color=color,alpha=.25,lw=.8)
        if group:ax.plot(range(1,31),np.median([[d['money'] for d in r['profile']['kpi']] for r in group],axis=0),color=color,lw=3)
        ax.set_title(f'{model} · {len(group)} replay · curve singole e mediana');ax.grid(alpha=.2);ax.set_xlabel('Giorno');ax.set_ylabel('Cassa')
    fig.savefig(OUT/'CASH_INDIVIDUAL.png',dpi=120);plt.close(fig)
    for region in ['Fattoria','Q0','Q1']:plot(rows,region)
    table='\n'.join(f"| {m} | {s['n']} | {s['wins']}/{s['n']} | {money(s['cash_mean'])} | {money(s['cash_median'])} | {money(s['cash_q25'])}–{money(s['cash_q75'])} | {money(s['margin_mean'])} | {s['rating_latest_episode']:.1f} |" for m,s in summaries.items())
    pt='\n'.join(f"| {m} | "+' | '.join(money(next(r['net_cash'] for r in phase_rows if r['model']==m and r['phase']==p)) for p,_,_ in PHASES)+' |' for m in summaries)
    prod='\n'.join(f"| {p['model']} | {p['product']} | {p['mean_harvested']:.1f} | {p['mean_sold']:.1f} | {money(p['mean_sales_cash'])} | {p['realized_price_weighted']:.2f} |" for p in products if p['product'] in ['STRAWBERRY','MILK','WOOL'] and p['realized_price_weighted'] is not None)
    anomalies='\n'.join(f"- {m}: {s['final_topologies']}; fughe totali {s['animal_losses']}; perdite crop per sete medie {s['crop_losses_mean']:.1f}." for m,s in summaries.items())
    text=f'''# 770 / 772 / 774 / 775 — confronto dei replay esterni

Acquisizione richiesta alle 17:00 Europe/Rome del 12 settembre 2026. Cutoff registrato: {inventory['observed_at_utc']}. Analisi di **{len(rows)} replay completi**. Errori di acquisizione/analisi: **{len(errors)}**, dettagli in AUDIT_ERRORS.json. Nessuna simulazione o modifica della policy.

## Risultato

| Modello | n | Vittorie | Cassa media | Mediana | Q25–Q75 | Margine medio sull'avversario | Rating ultimo episodio |
|---|---:|---:|---:|---:|---:|---:|---:|
{table}

Rating provvisori ricavati dai metadati dell'ultimo episodio della coorte, non una rilettura della classifica live. Vittorie e cassa si riferiscono ai 20 episodi selezionati, non a tutta la vita della submission. Vedi INTERPRETATION.md per la lettura dei risultati.

## Dove si forma la cassa

Flusso netto medio per fase, da libro contabile (vendite − acquisti − lavoratori − terra + variazioni da azioni). La somma delle fasi più il capitale iniziale riconcilia la cassa finale in ogni replay.

| Modello | D1–11 | D12–19 | D20–29 | D30 |
|---|---:|---:|---:|---:|
{pt}

![Traiettorie individuali della cassa](CASH_INDIVIDUAL.png)

PHASE_CASH.csv separa ricavi, acquisti, manodopera e terra; PRODUCTS.csv riporta quantità raccolte/vendute e prezzi realizzati. Quantità vendute possono includere prodotti comprati. Prezzi medi ponderati per le unità vendute, non quotazioni finali.

| Modello | Prodotto | Raccolto medio | Venduto medio | Ricavi medi | Prezzo realizzato |
|---|---|---:|---:|---:|---:|
{prod}

## 22 KPI e quadranti

Mediana e intervallo interquartile per giorno. FLOW come MOVE/PASS/WATER/FEED/CARE sono conteggi giornalieri; gli altri KPI sono stock ai checkpoint. D1–D29: stato H24 prima dell'ultima azione del giorno; D30: terminale. Le fasi contabili usano tutte le azioni effettive e non differenze tra quei checkpoint. PHASE_KPI.csv riporta livelli/conteggi medi giornalieri per fase; DAILY_KPI.csv conserva tutti i singoli replay.

![Fattoria: 22 KPI](Fattoria_KPI22.png)
![Q0: KPI attribuibili](Q0_KPI22.png)
![Q1: KPI attribuibili](Q1_KPI22.png)

Cassa comune non attribuita arbitrariamente a Q0/Q1. I 21 KPI additivi sono riconciliati con i quattro quadranti e un residuo esplicito NON_ATTRIBUIBILE per richieste MOVE/PASS a lavoratori inesistenti, quando presenti. Quel residuo non rappresenta lavoro eseguito. MOVE/PASS sono richieste; WATER/FEED/CARE sono azioni riuscite verificate dal motore sulle osservazioni salvate, senza generare nuove partite.

## Anomalie e dati di contesto

{anomalies}

Scorte terminali per episodio in GAMES.csv; dettagli di deposito, inventari, semi, rese residue e prezzi in profiles_1700. I profili conservano anche i cambiamenti della città osservati e tutti i metadati dell'avversario. Nessuna anomalia di topologia è rimossa dal campione.

## Identità, selezione e limiti

770 = **V48 56101593**; 772 = **E20.1 loaderfix 56142698**, non E20.2 locale; 774 = **E21 Repair2 56185961**; 775 = **E18.2 56147218**. La V51 770 è una versione distinta e non mescolata alla V48. Ultimi 20 episodi PUBLIC completati per submission, ordine createTime/ID, esclusi self-play per team e validation; history complete salvate, compresi esclusi e partite in corso. Gli episodi incompleti o con dati insufficienti vengono segnalati e non entrano negli aggregati stagionali.

Coorti diverse per avversari, seed, epoca e domanda: confronto descrittivo, non stima causale della topologia. Il campione 774 iniziale può essere influenzato dall'abbinamento basato sul rating. Anche i prezzi e i negozi dipendono dalle azioni tramite RNG condiviso del motore. Le bande interquartili descrivono la dispersione, non sono intervalli di confidenza.

Verificati hash raw, 720 stati/DONE, identità submission/ruolo, campi per KPI, parità contabile, riconciliazione dei quadranti. Nessun errore è ignorato; esclusioni elencate separatamente. La baseline del primo cutoff resta in BASELINE_INVENTORY.json.
'''
    (OUT/'REPORT.md').write_text(text,encoding='utf-8')
    render()
    return summaries

def render():
    text=(OUT/'REPORT.md').read_text(encoding='utf-8')
    interp=OUT/'INTERPRETATION.md'
    if interp.exists():text=text.replace('Vedi INTERPRETATION.md per la lettura dei risultati.', '\n'+interp.read_text(encoding='utf-8'))
    doc='<!doctype html><meta charset="utf-8"><title>Confronto esterno 770 772 774 775</title><style>body{max-width:1200px;margin:36px auto;padding:0 22px;font:17px/1.5 system-ui;color:#203044}img{max-width:100%}h1,h2{color:#174c79}table{border-collapse:collapse;font-size:14px}td,th{padding:8px 12px;border-bottom:1px solid #ddd}a{color:#216ec0}</style>'+MarkdownIt().enable('table').render(text)
    (OUT/'REPORT.html').write_text(doc,encoding='utf-8')
    files=[p for p in OUT.iterdir() if p.is_file() and p.name!='MANIFEST_1700.json']+list(DERIVED.glob('*.json'))+[Path(__file__)]
    save(OUT/'MANIFEST_1700.json',{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files})

if __name__=='__main__':
    if '--render' in sys.argv:render()
    else:
        inventory,rows,errors=process();print(json.dumps(report(inventory,rows,errors),indent=2),flush=True)
