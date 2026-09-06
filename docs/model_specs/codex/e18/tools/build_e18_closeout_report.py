"""Two-series V4.1 report and explicit descriptive gaps, no tuning."""
import json
from pathlib import Path
from statistics import mean
from docs.model_specs.codex.e18.tools.build_e18_31_desktop_report import build_dataset,render,DERIVED

OUT=Path('C:/Users/pietr/.codex/visualizations/2026/09/04/01a06ad3-93d8-77d0-a3b0-65d6af39fd46')

def main():
    data=build_dataset(DERIVED/'E18_32_READY_WORK_GATE_RELEASE_V9_DEVELOPMENT_20260906.json',
                       DERIVED/'E18_31_EXTERNAL_TOP002_FULL_20260906.json','Top770-002 storico',land_overlay=True)
    data.update(candidate_version='E18.32 DEMAND RELEASE V9',candidate_regime='Simulazioni interne E18.32 V9: sette seed, due seat contro E18.16; non replay pubblici',
                release_role='PROVISIONAL_EXTERNAL_CONTROL_NOT_E19_BENCHMARK',new_top_consumed=False)
    gaps={}
    for metric in ('money','people','crop_tiles','COW','SHEEP','MOVE','PASS','WATER','FEED','CARE','unlocked_tiles'):
        a=data['series']['candidate'][metric]; b=data['series']['top770'][metric]
        gaps[metric]=dict(candidate_d10=a[9][0],top_d10=b[9][0],candidate_d30=a[29][0],top_d30=b[29][0],
                          days_candidate_median_outside_top_observed_range=[d+1 for d in range(30) if not b[d][1]<=a[d][0]<=b[d][2]],
                          candidate_d5_d10=sum(x[0] for x in a[4:10]),top_d5_d10=sum(x[0] for x in b[4:10]))
    data['descriptive_gaps']=gaps
    data['equivalence_claim']=False
    dataset=DERIVED/'E18_32_CLOSEOUT_TOP002_KPI_V4_1_20260906.json'
    assert not dataset.exists()
    dataset.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    fragment=render(data,'e32-closeout-d30').replace('E18.31 V11','E18.32 V9').replace('E18.31 vs','E18.32 V9 vs')
    assert 'E18.31' not in fragment and fragment.count('<section data-metric=')==22
    target=OUT/'e18-32-v9-closeout-kpi-d30.html'
    assert not target.exists()
    target.write_text(fragment,encoding='utf-8',newline='\n')
    print(json.dumps(dict(dataset=str(dataset),fragment=str(target),gaps=gaps),ensure_ascii=False),flush=True)
    autonomy=json.loads((DERIVED/'E18_CLOSEOUT_GATE_E18_33_V9_AUTONOMY_20260906.json').read_text())
    for r in autonomy['matches']:
        exits=[e for e in r['common_events'] if e['event']=='bootstrap_retired']
        print(json.dumps(dict(opponent=r['opponent'],seat=r['seat'],cash=r['reward'],exit=exits,
                              topology=r['daily'][-1]['pasture_topology'],deaths=len(r['crop_starvation']),escapes=len(r['ledger']['animal_escapes']),
                              max_call=r['max_call_seconds'],PASS=r['totals'].get('PASS',0)),ensure_ascii=False))
    print('Autonomy mean cash:',mean(r['reward'] for r in autonomy['matches']))

if __name__=='__main__': main()
