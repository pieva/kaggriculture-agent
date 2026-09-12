"""Audit the frozen candidate and render the familiar interactive 22 KPI report."""
import csv,gzip,hashlib,json,re,sys
from pathlib import Path
from statistics import mean,median
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.audit_results import run as audit
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
BASE=ROOT/'docs/model_specs/codex/e20';OUT=BASE/'reports/e20_2';ART=BASE/'artifacts/e20_2_care_floor'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    pairs=[];daily=[];profiles={'control':[],'candidate':[]};sources={}
    for seed in [180910201,180910203]:
        for seat in [0,1]:
            pair=dict(seed=seed,seat=seat,conditions={});metas=[]
            for condition in ['control','candidate']:
                p=ART/f'E20.2_{seed}_seat{seat}_{condition}.json';m=read(p);metas.append(m)
                assert all(x['calls']==719 for x in m['runtime']) and m['runtime'][seat]['core_errors']==0
                assert m['verification']['prefix_actions_per_agent']==456
                if condition=='control':assert m['verification']['suffix_states']==m['verification']['suffix_action_batches']==263
                with gzip.open(p.with_suffix('.replay.json.gz'),'rb') as f:raw=f.read()
                assert hashlib.sha256(raw).hexdigest()==m['replay_sha256'];r=json.loads(raw)
                assert len(r['steps'])==720 and all(x['status']=='DONE' for x in r['steps'][-1])
                for step in r['steps']:
                    counts=[0]*4
                    for y,row in enumerate(step[seat]['observation']['farms'][seat]['tiles']):
                        for x,t in enumerate(row):
                            if isinstance(t,dict) and t.get('kind')=='PASTURE':counts[(x>=5)+2*(y>=5)]+=1
                    assert all(n<=cap for n,cap in zip(counts,[7,7,2,0]))
                assert counts==[7,7,2,0]
                audit(str(p));k=read(p.with_suffix('.kpi.json'));assert k['replay_sha256']==m['replay_sha256']
                s=k['sides'][seat];profiles[condition].append(s['kpi']);ledger=s['ledger']['daily'][19:]
                pair['conditions'][condition]=dict(cash=m['rewards'][seat],margin=m['rewards'][seat]-m['rewards'][1-seat],stress=len(s['crop_starvation']),losses=len(s['ledger']['animal_escapes']),
                    actions={op:sum(d['executed_actions'].get(op,0) if op in ['CARE','FEED','WATER'] else d['requested_actions'].get(op,0) for d in ledger) for op in ['CARE','FEED','WATER','MOVE','PASS']},
                    sales=sum(sum(d['sales_cash'].values()) for d in ledger),purchases=sum(sum(d['purchase_cash'].values()) for d in ledger),wages=sum(d['hire_cash'] for d in ledger))
                for side in [0,1]:
                    daily.extend(dict(seed=seed,target_seat=seat,seat=side,model='E20' if side==seat else 'E18',condition=condition,day=d,**{key:v[key] for key,_,_ in FIELDS}) for d,v in enumerate(k['sides'][side]['kpi'],1))
                sources[p.relative_to(ROOT).as_posix()]=sha(p)
            assert metas[0]['source_replay_sha256']==metas[1]['source_replay_sha256'] and metas[0]['engine']==metas[1]['engine']
            a,b=[pair['conditions'][c] for c in ['control','candidate']]
            pair.update(delta_cash=b['cash']-a['cash'],delta_margin=b['margin']-a['margin'],biological_regression=b['stress']>a['stress'] or b['losses']>a['losses'])
            pairs.append(pair)
    delta=mean(p['delta_cash'] for p in pairs)
    decision='DEVELOPMENT_SIGNAL_ONLY' if delta>0 and not any(p['biological_regression'] for p in pairs) else 'NOT_ADOPTED'
    result=dict(version='E20.2',variant='E20v32',decision=decision,adopted=False,uploaded=False,distinct_seeds=2,paired_cases=4,mean_delta_cash=delta,mean_delta_margin=mean(p['delta_margin'] for p in pairs),pairs=pairs,sources=sources)
    (OUT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    with (OUT/'daily_22_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(daily[0]));w.writeheader();w.writerows(daily)
    lines=['# E20.2 / E20v32: CARE al prezzo minimo','',f'Decisione: **{decision}**. Delta cassa medio {delta:+.1f}; margine medio {result["mean_delta_margin"]:+.1f}. Candidata locale, nessuna promozione o submission. Due seed diagnostici gia esposti, ruoli accoppiati.', '', '| Seed | Ruolo | Cassa E20.1 | Cassa E20.2 | Delta margine | CARE controllo/candidata | PASS controllo/candidata | Stress controllo/candidata |','|---|---:|---:|---:|---:|---:|---:|---:|']
    table='<table><tr><th>Seed / ruolo</th><th>Cassa E20.1</th><th>Cassa E20.2</th><th>Delta cassa</th><th>Delta margine</th></tr>'
    for p in pairs:
        a,b=[p['conditions'][c] for c in ['control','candidate']]
        lines.append(f"| {p['seed']} | {p['seat']} | {a['cash']:.0f} | {b['cash']:.0f} | {p['delta_margin']:+.0f} | {a['actions']['CARE']}/{b['actions']['CARE']} | {a['actions']['PASS']}/{b['actions']['PASS']} | {a['stress']}/{b['stress']} |")
        table+=f"<tr><td>{p['seed']} / {p['seat']}</td><td>{a['cash']:.0f}</td><td>{b['cash']:.0f}</td><td>{p['delta_cash']:+.0f}</td><td>{p['delta_margin']:+.0f}</td></tr>"
    table+='</table>'
    lines+=['', 'Da D20 le nuove offerte escludono CARE se il prezzo pubblico del prodotto animale e 1. FEED e raccolta restano disponibili. Il prezzo futuro non e noto: questo filtro e un ipotesi economica, non la prova che la cura abbia resa nulla.', '', 'Otto rami completi con 719 chiamate per agente e nessun errore core E20. Quattro controlli esatti; prefisso di 456 azioni per agente identico anche nella candidata. Bundle caricato senza __file__. Topologia 7-7-2 verificata, seed riservati inutilizzati.', '', '[22 KPI interattivi](REPORT.html) - [Dati](RESULT.json) - [Traiettorie CSV](daily_22_kpi.csv) - [Protocollo](../../E20_2_PROTOCOL.md).']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    metrics=FIELDS
    series={name:{key:[[median(v),min(v),max(v)] for d in range(30) for v in [[p[d][key] for p in profiles[c]]]] for key,_,_ in [*metrics,('unlocked_tiles','Terreno sbloccato','caselle')]} for name,c in [('candidate','candidate'),('top770','control')]}
    payload=dict(topLabel='E20.1',metrics=[dict(key=k,label=l,unit=u) for k,l,u in metrics],series=series)
    (OUT/'KPI.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    template=(ROOT/'docs/model_specs/codex/e19/tools/complete_kpi_template.html').read_text(encoding='utf-8')
    template=re.sub(r'<p class="note">.*?</p>','<p class="note">Modifica da D20: filtro CARE al prezzo minimo. Stessi seed e avversario E18; quattro casi su due seed, non quattro repliche indipendenti.</p>',template)
    template=re.sub(r'<h2>Diagnosi</h2>.*?<details>',f'<h2>Esito</h2><p>{decision}. Delta cassa medio {delta:+.1f}. Nessuna promozione; il prezzo minimo corrente non garantisce quello futuro.</p><details>',template,flags=re.S)
    template=re.sub(r'Stessi corpus storici.*?</p>','Otto prosecuzioni complete; nessuna submission.</p>',template)
    template=template.replace('770 assistita V1','E20.2 candidata').replace("candidate:'770 assistita'","candidate:'E20.2'").replace('7 settembre 2026','12 settembre 2026')
    for key,value in dict(TITLE='E20.2 vs E20.1 - 22 KPI D1-D30',COHORTS='Controlli appaiati contro E18',TOP='E20.1',ECONOMY=table,PROVENANCE='E20v32 candidata, base E20v28 congelata. Campione diagnostico esposto; bande descrittive.',DATAFILE='KPI.json',DATA=json.dumps(payload,ensure_ascii=False)).items():template=template.replace('__'+key+'__',value)
    # The inherited graph marks the opening transition; here mark the intervention.
    template=template.replace('x(11.5)','x(19.5)').replace('day=12','day=20')
    assert not re.search(r'__[A-Z]+__',template)
    (OUT/'REPORT.html').write_text(template,encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['pairs','sources']},indent=2))
if __name__=='__main__':main()
