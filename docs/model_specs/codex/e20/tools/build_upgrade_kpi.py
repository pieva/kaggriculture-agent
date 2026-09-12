"""Readable 22-KPI charts for one upgrade against E18, with exact game identity."""
import csv,hashlib,json,re,sys
from pathlib import Path
from statistics import median,mean
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
BASE=ROOT/'docs/model_specs/codex/e20'
def build(stage,model):
    paths=[];cases=[]
    for p in sorted((BASE/'artifacts'/stage).glob('*.kpi.json')):
        c=json.loads(p.read_text(encoding='utf-8'))
        if {s['name'] for s in c['sides']}!={model,'E18'}:continue
        m=json.loads(p.with_name(p.name.replace('.kpi.json','.json')).read_text(encoding='utf-8'))
        assert all(x['calls']==719 for x in m['runtime'])
        assert c['replay_sha256']==m['replay_sha256']
        paths.append(p);cases.append(c)
    assert cases
    groups={key:[s for c in cases for s in c['sides'] if s['name']==name] for key,name in [('candidate',model),('top770','E18')]}
    data=dict(topLabel='E18',metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series={key:{k:[[median(v),min(v),max(v)] for d in range(30) for v in [[s['kpi'][d][k] for s in ss]]] for k in [x[0] for x in FIELDS]+['unlocked_tiles']} for key,ss in groups.items()})
    out=BASE/'reports'/stage;out.mkdir(parents=True,exist_ok=True)
    (out/'KPI_22.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    table=f'<table><tr><th>Seed</th><th>Ruolo {model}</th><th>Cassa {model}</th><th>Cassa E18</th><th>Margine</th></tr>'
    for c in cases:
        a=next(s for s in c['sides'] if s['name']==model);b=next(s for s in c['sides'] if s['name']=='E18')
        table+=f"<tr><td>{c['seed']}</td><td>{a['seat']}</td><td>{a['reward']:.0f}</td><td>{b['reward']:.0f}</td><td>{a['reward']-b['reward']:+.0f}</td></tr>"
    table+='</table>'
    template=ROOT/'docs/model_specs/codex/e19/tools/complete_kpi_template.html'
    h=template.read_text(encoding='utf-8')
    note=f'{len(cases)} scontri su {len({c["seed"] for c in cases})} seed esposti, ruoli appaiati. Confronto diagnostico; nessuna submission.'
    h=re.sub(r'<p class="note">.*?</p>',f'<p class="note">{note}</p>',h)
    h=re.sub(r'<h2>Diagnosi</h2>.*?<details>','<h2>Valutazione</h2><p>Consultare protocollo e risultati dello stage. Questi grafici descrivono le partite; non dimostrano da soli le cause delle differenze.</p><details>',h,flags=re.S)
    h=re.sub(r'Stessi corpus storici.*?</p>',note+'</p>',h)
    h=h.replace('770 assistita V1',model).replace("candidate:'770 assistita'",f"candidate:'{model}'").replace('7 settembre 2026','12 settembre 2026').replace('manifest.json','KPI_22_MANIFEST.json')
    for k,v in dict(TITLE=f'{model} / E18 - 22 KPI',COHORTS=note,TOP='E18',ECONOMY=table,PROVENANCE='Replay e saldi verificati. Mediane e bande min-max descrittive; le sequenze dei negozi possono differire fra varianti.',DATAFILE='KPI_22.json',DATA=json.dumps(data,ensure_ascii=False)).items():h=h.replace('__'+k+'__',v)
    assert not re.search(r'__[A-Z]+__',h) and len(data['metrics'])==22
    html=out/'REPORT_22_KPI.html';html.write_text(h,encoding='utf-8')
    with (out/'daily_22_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['seed','model','opponent','seat','day']+[x[0] for x in FIELDS]);w.writeheader()
        for c in cases:
            for i,s in enumerate(c['sides']):
                for day,r in enumerate(s['kpi'],1):w.writerow(dict(seed=c['seed'],model=s['name'],opponent=c['sides'][1-i]['name'],seat=s['seat'],day=day,**{x[0]:r[x[0]] for x in FIELDS}))
    files=paths+[template,Path(__file__),html,out/'KPI_22.json',out/'daily_22_kpi.csv']
    (out/'KPI_22_MANIFEST.json').write_text(json.dumps(dict(stage=stage,model=model,cases=len(cases),panels=22,visual_qa='Not performed; browser local URL policy blocked earlier preview.',sources={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n',encoding='utf-8')
    print(html)
if __name__=='__main__':build(sys.argv[1],sys.argv[2])
