"""Two-cohort V4 desktop report: successful WATER, FEED and CARE separately."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from statistics import median

from docs.model_specs.codex.e18.tools.build_e18_27_top770_complete_kpi import flatten
from docs.model_specs.codex.e18.tools.build_e18_29_simulation_report import STANDARD as V3

BASE=Path(__file__).resolve().parents[1]
DERIVED=BASE/'artifacts/derived'
STANDARD=(*V3,'CARE')


def acquisition_events(replay,seat):
    """Executed unlocks, timestamped by the action's input observation."""
    names={'NW':'Q0','NE':'Q1','SW':'Q2','SE':'Q3'}
    events=[]
    for index in range(1,len(replay['steps'])):
        previous=replay['steps'][index-1][seat]['observation']
        after=replay['steps'][index][seat]['observation']
        old=set(previous['farms'][seat]['unlocked_quadrants'])
        new=set(after['farms'][seat]['unlocked_quadrants'])
        assert old<=new
        for quadrant in sorted(new-old):
            events.append(dict(quadrant=names[quadrant],recorded_step=index,
                               day=previous['day']+1,hour=previous['hour']+1,
                               total_tiles=25*len(new)))
    return events


def build_dataset(candidate_path,top_path=None,top_label='Top770-001 storico',*,land_overlay=False):
    sources={}
    def read(path):
        sources[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
        return json.loads(path.read_text(encoding='utf-8'))
    candidate_payload=read(candidate_path)
    if 'matches' in candidate_payload:
        candidates=[p for p in candidate_payload['matches'] if p['opponent']=='E18.16']
        candidate_regime='Simulazioni interne, sette seed e due seat; non replay pubblici'
    else:
        candidates=candidate_payload['profiles']
        candidate_regime='Replay pubblici della submission E18.31'
    top_excluded=[]
    if top_path:
        top_payload=read(top_path)
        assert top_payload['stable_preliminary'], 'Screen topology before economic comparison'
        top_all=top_payload['profiles']
        top=[p for p in top_all if p['exact770_final'] and p['exact770_d15_d30_share']>=.8]
        top_excluded=[p['episode_id'] for p in top_all if p not in top]
    else:
        top=read(DERIVED/'E18_26_JESSE_770_D01_D30_CLOSURE.json')['jesse']
        ops={p['episode_id']:p['daily'] for p in read(DERIVED/'TOP770_D01_D30_OPERATIONAL_KPI.json')['profiles']}
        top=[p|{'operational_daily':ops[p['episode_id']]} for p in top]
    assert candidates and top
    series,profile_daily,land_events={},{},{}
    metrics=(*STANDARD,'unlocked_tiles') if land_overlay else STANDARD
    for name,profiles in [('candidate',candidates),('top770',top)]:
        days_all=[]
        for p in profiles:
            assert len(p['daily'])==len(p['ledger']['daily'])==len(p['operational_daily'])==30
            assert p['ledger']['cash_parity_errors']==0
            days=[]
            for stock,ops,ledger in zip(p['daily'],p['operational_daily'],p['ledger']['daily'],strict=True):
                row=flatten(stock)|ops
                for op in ('WATER','FEED','CARE'):
                    row[op]=ledger['executed_actions'].get(op,0)
                days.append({k:row[k] for k in metrics})
            days_all.append(days)
        series[name]={k:[[median(v),min(v),max(v)] for v in [[p[d][k] for p in days_all] for d in range(30)]] for k in metrics}
        profile_daily[name]=[dict(episode_id=p.get('episode_id'),seed=p.get('seed'),seat=p['seat'],daily=d) for p,d in zip(profiles,days_all)]
        if land_overlay:
            land_events[name]=[]
            for p in profiles:
                path=Path(p.get('cache_path','')) if p.get('cache_path') else None
                if path and path.is_file():
                    assert hashlib.sha256(path.read_bytes()).hexdigest()==p['sha256']
                    replay=read(path)
                    assert replay['info']['EpisodeId']==p['episode_id']
                    land_events[name].append(dict(episode_id=p['episode_id'],seat=p['seat'],
                                                  events=acquisition_events(replay,p['seat'])))
    return dict(standard='V4.1' if land_overlay else 'V4',land_overlay=land_overlay,
                land_definition='Coltivate = PLANT; totali = 25 × quadranti sbloccati. Nessuna somma delle mediane.',
                candidate_version='E18.31 UNIFIED V11',candidate_regime=candidate_regime,
                top_label=top_label,counts=dict(candidate=len(candidates),top770=len(top)),sources=sources,
                top_excluded_episodes=top_excluded,top_screen_count=len(top)+len(top_excluded),
                series=series,profile_daily=profile_daily,land_purchase_events=land_events,
                interpretation='Mediane e min–max osservati, non intervalli di confidenza. Confronto descrittivo, non matched.',
                checkpoint='H24 prima dell’ultimo batch D1–D29; D30 terminale. 12 manovali = 13 persone incluso farmer.')


def render(data,slug):
    template_name='e18_31_simulation_land_report.html' if data.get('land_overlay') else 'e18_29_simulation_report.html'
    template=(BASE/'tools/templates'/template_name).read_text(encoding='utf-8')
    for key in ('pass_share','net_cash_100_slots','fertilizer_collected','fertilizer_used'):
        template,count=re.subn(r'    <section data-metric="'+key+r'"[^\n]+</section>\n','',template)
        assert count==1
    care='    <section data-metric="CARE" data-unit="CARE / giorno"><h3>22 · CARE riusciti al giorno</h3><div class="e29-chart"></div></section>\n'
    template=template.replace('  </div>\n  <div class="tooltip',care+'  </div>\n  <div class="tooltip',1)
    template=template.replace('e29-simulation-d30',slug).replace('e29-','e31-')
    template=template.replace('E18.29 B3 · n14',f"E18.31 V11 · n{data['counts']['candidate']}").replace('E18.29 B3','E18.31 V11')
    template=template.replace('Top770 · n5',f"{data['top_label']} · n{data['counts']['top770']}")
    template=template.replace("name:'Top770'",f"name:{json.dumps(data['top_label'])}")
    template=template.replace('Traiettorie 7–7–0 · D1–D30',f"E18.31 vs {data['top_label']} · 22 KPI · D1–D30")
    template=template.replace('Mediana e intervallo min–max · confronto descrittivo con Top770',data['candidate_regime']+' · mediana e min–max · confronto descrittivo')
    template=template.replace('__REPORT_SERIES__',json.dumps(data['series'],separators=(',',':')))
    assert template.count('<section data-metric="')==22 and 'Cause PASS' not in template
    assert len(template.encode())<1_000_000
    return template


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--candidate',type=Path,default=DERIVED/'E18_31_ASSIGNMENT_GATE_UNIFIED_V11_DEVELOPMENT_20260906.json')
    parser.add_argument('--top',type=Path)
    parser.add_argument('--top-label',default='Top770-001 storico')
    parser.add_argument('--label',required=True)
    parser.add_argument('--fragment',type=Path,required=True)
    parser.add_argument('--land-overlay',action='store_true')
    args=parser.parse_args()
    data=build_dataset(args.candidate,args.top,args.top_label,land_overlay=args.land_overlay)
    suffix='V4_1' if args.land_overlay else 'V4'
    dataset=DERIVED/f'E18_31_DESKTOP_{args.label}_{suffix}.json'
    dataset.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    fragment=render(data,'e31-'+args.label.lower().replace('_','-')+'-d30')
    args.fragment.parent.mkdir(parents=True,exist_ok=True)
    args.fragment.write_text(fragment,encoding='utf-8',newline='\n')
    assert args.fragment.read_text(encoding='utf-8')==fragment
    print(json.dumps(dict(dataset=str(dataset),fragment=str(args.fragment),counts=data['counts'])))


if __name__=='__main__':
    main()
