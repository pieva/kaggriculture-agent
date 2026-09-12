"""Read saved trajectories, verify quadrant services, and render 22-KPI figures."""
import csv,gzip,hashlib,html,importlib,json,sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
BASE=Path(__file__).resolve().parent;OUT=BASE/'reports/trajectory_774_772_775';OUT.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def quadrant(x,y):return int(x>=5)+2*int(y>=5)
def tile_state(t):return {'kind':t.get('kind'),'animal':t.get('animal'),'crop':t.get('crop')} if isinstance(t,dict) else t
def load(p):
    meta=read(p);kp=read(p.with_suffix('.kpi.json'))
    raw=gzip.decompress(p.with_suffix('.replay.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==meta['replay_sha256']==kp['replay_sha256']
    replay=json.loads(raw);assert len(replay['steps'])==720
    assert all(s['status']=='DONE' for s in replay['steps'][-1])
    assert all(r['calls']==719 for r in meta['runtime'])
    return meta,kp,replay
def profile(label,p,seat=0):
    m,k,r=load(p);s=k['sides'][seat]
    assert s['ledger']['cash_parity_errors']==0
    eng=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    rows=[];target=[];last=object()
    for i,step in enumerate(r['steps']):
        t=tile_state(step[seat]['observation']['farms'][seat]['tiles'][7][4])
        if t!=last:target.append(dict(step=i,day=step[seat]['observation']['day']+1,hour=step[seat]['observation']['hour']+1,state=t));last=t
    for q in range(4):
        qr=[]
        for d in range(1,31):
            farm=r['steps'][24*d-1][seat]['observation']['farms'][seat]
            ts=[t for y,row in enumerate(farm['tiles']) for x,t in enumerate(row) if quadrant(x,y)==q]
            tiles=[t for t in ts if isinstance(t,dict)]
            z={key:0 for key,_,_ in FIELDS};z['money']=None
            z['people']=sum(quadrant(*pos)==q for pos in [farm['farmer'],*farm['hands']])
            z['crop_tiles']=sum(t.get('kind')=='PLANT' for t in tiles)
            z['occupied_livestock_tiles']=sum(bool(t.get('animal')) for t in tiles)
            for species in ['COW','SHEEP','GOOSE']:z[species]=sum(t.get('animal')==species for t in tiles)
            for crop in ['MELON','WHEAT','STRAWBERRY','CARROT','TOMATO']:z[crop]=sum(t.get('kind')=='PLANT' and t.get('crop')==crop for t in tiles)
            z['empty_pastures']=sum(t.get('kind')=='PASTURE' and not t.get('animal') for t in tiles)
            z['empty_coops']=sum(t.get('kind')=='COOP' and not t.get('animal') for t in tiles)
            z['weed_tiles']=sum(t.get('kind')=='WEED' for t in tiles)
            z['unwatered_tiles_h24']=sum(t.get('kind')=='PLANT' and not t.get('watered_today') for t in tiles)
            z['unlocked_tiles']=sum(t!='LOCKED' for t in ts)
            z['pastures']=sum(t.get('kind')=='PASTURE' for t in tiles)
            qr.append(z)
        rows.append(qr)
    for i in range(1,720):
        obs=r['steps'][i-1][seat]['observation'];day=obs['day']
        farm=deepcopy(obs['farms'][seat]);private=deepcopy(obs['private'])
        action=r['steps'][i][seat]['action'] or {};cmds=[action.get('farmer',['PASS']),*action.get('hands',[])]
        demand=Counter(c[1] for c in cmds if isinstance(c,list) and len(c)>1 and c[0]=='PLANT')
        blocked={c for c,n in demand.items() if n>private['seeds'].get(c,0)}
        for worker,cmd in enumerate(cmds):
            if not isinstance(cmd,list) or not cmd:continue
            pos=eng._farmer_position(farm,worker)
            old=deepcopy(farm['tiles'][pos[1]][pos[0]]) if pos else None
            op=cmd[0]
            if pos:
                q=quadrant(*pos)
                if op in eng.FARMER_MOVES:rows[q][day]['MOVE']+=1
                elif op=='PASS':rows[q][day]['PASS']+=1
            allowed=['PASS'] if op=='PLANT' and len(cmd)>1 and cmd[1] in blocked else cmd
            eng._apply_unit_action(farm,private,worker,allowed,r['configuration'].get('boardSize',10),day,24,r['configuration'].get('shedCapacity',100))
            if pos and op in ['WATER','FEED','CARE'] and old!=farm['tiles'][pos[1]][pos[0]]:rows[q][day][op]+=1
    for e in s['ledger']['animal_escapes']:
        day=r['steps'][e['recorded_step']-1][seat]['observation']['day']
        rows[quadrant(e['x'],e['y'])][day]['verified_animal_losses']+=1
    for d in range(30):
        for key,_,_ in FIELDS:
            if key!='money':assert sum(q[d][key] for q in rows)==s['kpi'][d][key],(label,d,key,sum(q[d][key] for q in rows),s['kpi'][d][key])
    return dict(label=label,seed=m['seed'],seat=seat,opponent=m['agents'][1-seat],source=str(p.relative_to(ROOT)),
        global_kpi=s['kpi'],quadrants={f'Q{q}':rows[q] for q in range(4)},target=target,
        reward=s['reward'],ledger=s['ledger'],topology=m['opening'][seat]['topology']),r
COLORS=['#b34a1c','#286aaa','#24805b']
def plot(profiles,region,days):
    fig,axes=plt.subplots(6,4,figsize=(18,22),layout='constrained')
    fig.suptitle(f'{region} · 22 KPI · D1–D{days}\n774 ricostruita / E20.2 772 / E18 775 · seed 180911301, ruolo 0',fontsize=20)
    for ax,(key,label,unit) in zip(axes.flat,FIELDS):
        for j,p in enumerate(profiles):
            data=p['global_kpi'] if region=='Fattoria' else p['quadrants'][region]
            if data[0][key] is None:continue
            ax.plot(range(1,days+1),[d[key] for d in data[:days]],color=COLORS[j],lw=2,ls=['-','--',':'][j],label=p['label'])
        if region!='Fattoria' and key=='money':
            ax.text(.5,.5,'Cassa comune alla fattoria\nnon attribuibile al quadrante',ha='center',va='center',transform=ax.transAxes)
            ax.set_axis_off()
        if key=='crop_tiles':label='Caselle coltivate'
        ax.set_title(label if key!='people' or region=='Fattoria' else 'Persone presenti nel quadrante',fontsize=12)
        ax.set_xlabel('Giorno');ax.set_ylabel(unit);ax.grid(alpha=.2);ax.set_xlim(1,days)
        if days>11:ax.axvspan(1,11,color='#777777',alpha=.055)
        ax.tick_params(labelsize=10)
    for ax in list(axes.flat)[22:]:ax.axis('off')
    handles,labels=axes.flat[1].get_legend_handles_labels();axes.flat[22].legend(handles,labels,loc='center',fontsize=13,frameon=False)
    name=f'{region}_D1_{days}';fig.savefig(OUT/f'{name}.png',dpi=120);fig.savefig(OUT/f'{name}.svg');plt.close(fig)
    return name
def main():
    specs=[('774 ricostruita',BASE/'artifacts/fixed774/Fixed774_E18_180911301.json'),
        ('772 · E20.2',ROOT/'docs/model_specs/codex/e20/artifacts/e20_2_confirmation/E20.2_E18_180911301.json'),
        ('775 · E18',ROOT/'docs/model_specs/codex/e20/artifacts/e20_2_confirmation/E18_E20.2_180911301.json')]
    profiles=[];replays=[]
    for label,p in specs:
        prof,r=profile(label,p);profiles.append(prof);replays.append(r);print('VERIFIED '+label,flush=True)
    # Verify the target species across the existing 14 direct games.
    target_cohort=[]
    for p in sorted((ROOT/'docs/model_specs/codex/e20/artifacts/e20_2_confirmation').glob('*.kpi.json')):
        k=read(p)
        if {s['name'] for s in k['sides']}!={'E18','E20.2'}:continue
        seat=next(s['seat'] for s in k['sides'] if s['name']=='E18')
        raw=gzip.decompress(p.with_name(p.name.replace('.kpi.json','.replay.json.gz')).read_bytes());assert hashlib.sha256(raw).hexdigest()==k['replay_sha256']
        r=json.loads(raw)
        occupied=[(i,t['animal']) for i,step in enumerate(r['steps']) if isinstance(t:=step[seat]['observation']['farms'][seat]['tiles'][7][4],dict) and t.get('animal')]
        target_cohort.append(dict(seed=k['seed'],seat=seat,species=sorted({a for i,a in occupied}),first_occupied_step=occupied[0][0] if occupied else None))
    distances=[]
    for region in ['Q0','Q1']:
        for lo,hi in [(1,11),(12,19),(1,19)]:
            details=[]
            for key,label,_ in FIELDS:
                if key=='money':continue
                values=[[d[key] for d in p['quadrants'][region][lo-1:hi]] for p in profiles]
                scale=max(max(v) for v in values)-min(min(v) for v in values)
                if not scale:continue
                a,b=[sum(abs(x-y) for x,y in zip(values[0],v))/len(v)/scale for v in values[1:]]
                details.append(dict(metric=key,to772=a,to775=b))
            distances.append(dict(region=region,phase=f'D{lo}–{hi}',informative_metrics=len(details),
                to772=sum(d['to772'] for d in details)/len(details),to775=sum(d['to775'] for d in details)/len(details),details=details))
    divergence=[]
    for j in [1,2]:
        first=next((i for i in range(1,720) if replays[0]['steps'][i][0]['action']!=replays[j]['steps'][i][0]['action']),None)
        divergence.append(dict(reference=profiles[j]['label'],first_action_step=first,day=(first-1)//24+1 if first else None,hour=(first-1)%24+1 if first else None))
    attempt=read(BASE/'artifacts/reconstruction/CONTROLLER_TRACE.json')['0']['telemetry']
    result=dict(profiles=profiles,target_cohort=target_cohort,distances=distances,first_divergence=divergence,
        dormant_attempt=dict(final_topology=read(BASE/'artifacts/reconstruction/R774_E18_180911301.json')['opening'][0]['topology'],modes=attempt['mode_history'],aborts=attempt['aborted_reclaim_batches']),
        limits=['774 is a modern persistent reconstruction, not historical replay','One exposed seed, no uncertainty or causal ranking',
                'All focal policies seat 0; 775 opponent E20.2, other opponents E18','Cassa not allocated to quadrants; people are checkpoint presence',
                'KPI checkpoint 24*D-1: pre-last-batch D1-29, terminal D30; flows include all daily commands',
                'Distance is range-normalized mean absolute daily gap, equal metric weights, constant metrics omitted; descriptive and post hoc'])
    (OUT/'ANALYSIS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    with (OUT/'daily_22_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['model','seed','seat','opponent','region','day']+[k for k,_,_ in FIELDS]);w.writeheader()
        for p in profiles:
            for region,ds in [('Fattoria',p['global_kpi']),*p['quadrants'].items()]:
                for d,row in enumerate(ds,1):w.writerow(dict(model=p['label'],seed=p['seed'],seat=p['seat'],opponent=p['opponent'],region=region,day=d,**{k:row[k] for k,_,_ in FIELDS}))
    charts=[plot(profiles,'Fattoria',30)]+[plot(profiles,q,d) for d in [11,19] for q in ['Q0','Q1']]
    intro='La 774 è una ricostruzione moderna persistente: non è il vecchio eseguibile perduto. Nel ramo superstite riattivato il reclaim non si attiva: il controller rimane in RECOVERY e chiude 775, con zero rollback. Questa prima run è conservata separatamente.'
    lines=['# Traiettorie 774 / 772 / 775','',intro,'',
        'Target (x=4,y=7): '+str(target_cohort),'',
        '| Regione | Fase | Distanza da 772 | Distanza da 775 | Più vicina |','|---|---|---:|---:|---|']
    table='<table><tr><th>Quadrante / fase</th><th>Distanza 772</th><th>Distanza 775</th><th>Più vicina</th></tr>'
    for d in distances:
        winner='775' if d['to775']<d['to772'] else '772' if d['to772']<d['to775'] else 'pari'
        lines.append(f"| {d['region']} | {d['phase']} | {d['to772']:.4f} | {d['to775']:.4f} | {winner} |")
        table+=f"<tr><td>{d['region']} · {d['phase']}</td><td>{d['to772']:.4f}</td><td>{d['to775']:.4f}</td><td>{winner}</td></tr>"
    table+='</table>'
    cash='<table><tr><th>Modello</th><th>Topologia finale</th><th>Cassa finale</th><th>Avversario</th></tr>'+''.join(f"<tr><td>{p['label']}</td><td>{p['topology']}</td><td>{p['reward']:,.0f}</td><td>{p['opponent']}</td></tr>" for p in profiles)+'</table>'
    note='Un solo seed esposto 180911301; ruolo 0 per tutte le curve. 774 e 772 affrontano E18; E18 775 affronta E20.2. Il diverso avversario e i negozi endogeni limitano il confronto a una descrizione, non a un effetto causale o ranking.'
    methods='22 KPI standard. Nei quadranti la cassa non è attribuita; persone indica presenza al checkpoint, MOVE è attribuito al quadrante di partenza. WATER/FEED/CARE sono esecuzioni verificate riapplicando i batch registrati; le somme Q0–Q3 coincidono con tutti i KPI globali non monetari in 90 giornate-modello. Checkpoint 24×D−1: prima dell’ultimo batch per D1–29, terminale per D30. La distanza usa il divario assoluto medio normalizzato per escursione di ciascun KPI, omette le costanti e pesa ugualmente i KPI; è una misura descrittiva scelta dopo la run.'
    targettext='La casella (4,7) ospita una pecora in '+str(sum(t['species']==['SHEEP'] for t in target_cohort))+'/14 replay E18 verificati. Le transizioni della casella, incluse costruzione e collocazione, sono riportate nei dati. L’oca è contata tra gli animali.'
    doc='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>774 / 772 / 775 · 22 KPI</title><style>body{font:17px/1.6 system-ui;max-width:1500px;margin:40px auto;padding:0 24px;color:#17232c;background:#fff}h1{font-size:36px}p{max-width:1100px}table{border-collapse:collapse;margin:24px 0}th,td{padding:10px 18px;border-bottom:1px solid #ddd;text-align:left}img{width:100%;height:auto}.note{border-left:4px solid #b34a1c;padding-left:18px}a{color:#175e93}</style><h1>774 / 772 / 775 · traiettorie dei 22 KPI</h1><p class="note">'+intro+'</p><p>'+targettext+'</p><p>'+note+'</p>'+table+cash+'<p>'+methods+'</p><p><a href="ANALYSIS.json">Dati, transizioni e distanze per KPI</a> · <a href="daily_22_kpi.csv">CSV giornaliero</a></p>'
    for name in charts:doc+=f'<h2>{name.replace("_"," ")}</h2><p><a href="{name}.svg">Apri figura vettoriale</a></p><img src="{name}.png" alt="22 traiettorie {name}">'
    doc+='<h2>Prima divergenza delle azioni</h2><pre>'+html.escape(json.dumps(divergence,indent=2,ensure_ascii=False))+'</pre><h2>Ricostruzioni e limiti</h2><p>Due nuove partite seriali: prima riattivazione con rollback conservato; seconda esclusione persistente D12 del target usando il meccanismo ereditato E20v39 ridotto a una casella, apertura E18 conservata. Cap COW/SHEEP 18 prima di Q2 e 19 dopo: nessuna eliminazione automatica degli acquisti residui. Nessuna promozione.</p></html>'
    (OUT/'REPORT.html').write_text(doc,encoding='utf-8')
    lines+=['',targettext,'',note,'',methods,'',json.dumps(divergence,ensure_ascii=False),'','[Report con grafici](REPORT.html)']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    sources=[Path(__file__),BASE/'RECONSTRUCTION_PROTOCOL.json',BASE/'FIXED774_PROTOCOL.json']
    for _,p in specs:sources.extend([p,p.with_suffix('.kpi.json'),p.with_suffix('.replay.json.gz')])
    (OUT/'MANIFEST.json').write_text(json.dumps(dict(sources={str(p.relative_to(ROOT)):sha(p) for p in sources},checks=['719 calls per agent','720 states DONE','replay hashes','cash ledgers','all 21 additive KPI equal quadrant sums'],new_simulations=2),indent=2)+'\n')
    print(json.dumps(dict(distances=distances,divergence=divergence,cash=[p['reward'] for p in profiles],targets=[p['target'] for p in profiles]),ensure_ascii=False),flush=True)
if __name__=='__main__':main()
