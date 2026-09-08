"""Standard V4.1: two separate, self-contained 22-panel reports."""
import hashlib
import html
import json
from pathlib import Path
from statistics import mean,median
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi
from docs.model_specs.codex.e18.tools.build_e18_27_top770_complete_kpi import flatten
BASE=ROOT/'docs/model_specs/codex/e19'
OUT=BASE/'reports/assisted_770_complete_kpi_20260907'
TOP=[ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_26_JESSE_770_D01_D30_CLOSURE.json',ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_31_EXTERNAL_TOP002_FULL_20260906.json']
FIELDS=[('money','Cassa','denaro'),('people','Persone','persone'),('crop_tiles','Coltivate e terreno sbloccato','caselle'),('occupied_livestock_tiles','Animali collocati','animali'),('COW','Mucche','animali'),('SHEEP','Pecore','animali'),('GOOSE','Oche','animali'),('empty_pastures','Pascoli vuoti','strutture'),('MELON','Meloni','caselle'),('WHEAT','Grano','caselle'),('STRAWBERRY','Fragole','caselle'),('CARROT','Carote','caselle'),('TOMATO','Pomodori','caselle'),('empty_coops','Pollai vuoti','strutture'),('MOVE','MOVE','comandi / giorno'),('PASS','PASS','comandi / giorno'),('unwatered_tiles_h24','Colture non irrigate a H24','caselle'),('verified_animal_losses','Perdite animali verificate','animali / giorno'),('weed_tiles','Infestanti','caselle'),('WATER','WATER riusciti','azioni / giorno'),('FEED','FEED riusciti','azioni / giorno'),('CARE','CARE riusciti','azioni / giorno')]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fmt(v):return f'{v:,.1f}'.replace(',','X').replace('.',',').replace('X','.')
def aggregate(profiles, frozen=None):
    rows=[]
    for p in profiles:
        assert len(p['daily'])==30
        operations=p.get('operational_daily',[{} for _ in range(30)])
        assert len(operations)==30
        series=[]
        for s,o,f in zip(p['daily'],operations,p['ledger']['daily']):
            r=flatten(s)|o
            r.update({k:f['requested_actions'].get(k,0) for k in ['MOVE','PASS']})
            r.update({k:f['executed_actions'].get(k,0) for k in ['WATER','FEED','CARE']})
            assert r['people']==r['hands']+1
            series.append(r)
        rows.append(series)
    result={}
    for k in [f[0] for f in FIELDS]+['unlocked_tiles']:
        if k in rows[0][0]:
            result[k]=[[median(v),min(v),max(v)] for d in range(30) for v in [[p[d][k] for p in rows]]]
            if frozen is not None and k in frozen:assert result[k]==frozen[k],k
        else:
            assert frozen is not None and len(frozen[k])==30,k
            result[k]=frozen[k]
    return result
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    paths=[BASE/'artifacts/derived/assisted_770_complete_20260907'/f'{s}_{t}.json' for s in range(180903001,180903008) for t in (0,1)]
    candidate=[read(p)['sides']['assisted'] for p in paths]
    top1=read(TOP[0])['jesse'];top2=[p for p in read(TOP[1])['profiles'] if p['exact770_final']]
    frozenpath=ROOT/'docs/model_specs/codex/e18/artifacts/derived/E18_28_C_TOP770_D01_D30_KPI_19.json'
    frozen=read(frozenpath)
    assert frozen['cohorts']['top770']['episodes']==[p['episode_id'] for p in top1]
    replay_paths=[frozenpath]
    template=Path(__file__).with_name('complete_kpi_template.html').read_text(encoding='utf-8')
    for number,group in [('001',top1),('002',top2)]:
        topname='Top770-'+number
        title='770 assistita vs '+topname+' · KPI completi D1–D30'
        payload=dict(topLabel=topname,metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=dict(candidate=aggregate(candidate),top770=aggregate(group,frozen['series']['top770'] if number=='001' else None)),aggregation='median/min/max',checkpoint='24*D-1, pre-last-batch D1-D29; D30 terminal')
        datafile=f'E18_770_ASSISTED_{topname}_D01_D30_COMPLETE_KPI.json'
        (OUT/datafile).write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        economics='<div class="tablewrap"><table><tr><th>KPI / finestra</th><th>770 assistita</th><th>'+topname+'</th></tr>'
        for label,fun in [('Cassa finale media',lambda p:p['terminal']['cash']),('Cassa finale mediana',None),('Somma caselle coltivate ai checkpoint D1–D30',lambda p:sum(r['crop_tiles'] for r in p['daily']))]:
            values=[median(p['terminal']['cash'] for p in ps) if fun is None else mean(fun(p) for p in ps) for ps in [candidate,group]]
            economics+='<tr><td>'+label+'</td>'+''.join('<td>'+fmt(v)+'</td>' for v in values)+'</tr>'
        for start,end in [(1,10),(11,20),(21,30),(10,15),(25,30)]:
            metrics=[('Vendite',lambda f:sum(f['sales_cash'].values())),('Acquisti',lambda f:sum(f['purchase_cash'].values())),('Costo manovali',lambda f:f['hire_cash']),('Costo terreno',lambda f:f['land_cash'])]
            metrics += [(item+' raccolto, unità',lambda f,item=item:f['harvested'].get(item,0)) for item in ['MELON','STRAWBERRY','MILK','WOOL']]
            for label,fun in metrics:
                values=[mean(sum(fun(f) for f in p['ledger']['daily'][start-1:end]) for p in ps) for ps in [candidate,group]]
                economics+='<tr><td>'+label+f' D{start}–D{end}</td>'+''.join('<td>'+fmt(v)+'</td>' for v in values)+'</tr>'
        economics+='</table></div><p class="meta">Flussi medi per partita. Le finestre D10–D15 e D25–D30 si sovrappongono alle decadi e non vanno sommate. Importi di corpus differenti non misurano superiorità competitiva.</p>'
        replacements={'TITLE':title,'COHORTS':f'Candidata: 14 partite locali contro V4D · {topname}: {len(group)} replay storici','OTHER':f'E18_770_ASSISTED_Top770-{"002" if number=="001" else "001"}_D01_D30_COMPLETE_KPI.html','TOP':topname,'ECONOMY':economics,'PROVENANCE':f'Candidata: submission_codex_e18_770_assisted_start_v1_candidate.py; semi 180903001–180903007, posizioni 0/1. {topname}: episodi '+', '.join(str(p['episode_id']) for p in group)+'. Selezione storica finale 770; possibili variazioni transitorie. Top002: escluso il precedente replay 10–7–0 secondo il criterio già adottato.','DATAFILE':datafile,'DATA':json.dumps(payload,ensure_ascii=False).replace('</',r'<\/')}
        result=template
        for key,value in replacements.items():result=result.replace('__'+key+'__',value)
        assert '__TITLE__' not in result and len(payload['metrics'])==22
        output=OUT/datafile.replace('.json','.html');output.write_text(result,encoding='utf-8')
        print(output)
    files=TOP+paths+replay_paths+[Path(__file__),Path(__file__).with_name('complete_kpi_template.html'),Path(__file__).with_name('run_assisted_770_complete.py')]
    (OUT/'manifest.json').write_text(json.dumps(dict(standard='E18 V4.1',panels=22,new_external_episodes=False,sources={str(p.relative_to(ROOT)):sha(p) for p in files},outputs={p.name:sha(p) for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2)+'\n')
if __name__=='__main__':main()
