"""Paired economic and biological gates against the frozen local V49F."""
import json
from pathlib import Path
from statistics import mean
import sys
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools import build_pass_reduction_v49_report as audit
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v50'
OLD=audit.OUT;audit.OUT=OUT


def analyze(variant):
    result={}
    for split in ['development','validation']:
        paths=[p for p in sorted(OUT.glob(f'{split}_{variant}_*.json')) if not p.name.endswith('_obligations.json')]
        if not paths:continue
        cases=[]
        for path in paths:
            b=audit.enrich(path)
            a=audit.enrich((OLD if split=='development' else OUT)/f'{split}_v49f_{b["seed"]}_{b["seat"]}.json')
            keys=['cash','pass_count','share','slots','move','hire_cash','FEED','CARE','WATER','HARVEST','losses','escapes']
            deficits=['missed_feed','missed_useful_care','missed_critical_water','decay_lost_units','productive_water_loss_units']
            av={k:audit.total(a,k) for k in keys};bv={k:audit.total(b,k) for k in keys}
            ac={k:sum(d[k] for d in a['obligations']) for k in deficits};bc={k:sum(d[k] for d in b['obligations']) for k in deficits}
            cases.append(dict(seed=b['seed'],seat=b['seat'],baseline=av,candidate=bv,
                delta={k:bv[k]-av[k] for k in keys},baseline_deficits=ac,candidate_deficits=bc,
                errors=b['errors'],incomplete=b['incomplete'],calls=b['runtime']['calls']))
        delta={k:mean(c['delta'][k] for c in cases) for k in keys}
        gates=dict(complete=all(c['calls']==719 and not c['errors'] and not c['incomplete'] for c in cases),
            pass_absolute=delta['pass_count']<0,pass_share=delta['share']<0,move=delta['move']<=0,
            cash_mean=delta['cash']>=0,cash_cases=all(c['candidate']['cash']>=.98*c['baseline']['cash'] for c in cases),
            losses=delta['losses']<=0,escapes=delta['escapes']<=0,
            services=all(delta[k]>=0 for k in ['FEED','CARE','HARVEST']),
            obligations=all(sum(c['candidate_deficits'][k]-c['baseline_deficits'][k] for c in cases)<=0 for k in deficits))
        result[split]=dict(n=len(cases),cases=cases,mean_delta=delta,gates=gates)
    failed=any(not all(part['gates'].values()) for part in result.values())
    complete=result.get('development',{}).get('n')==6 and result.get('validation',{}).get('n')==4
    output=dict(variant=variant,partitions=result,local_only=True,
        status='REJECTED' if failed else 'LOCAL_CANDIDATE_ONLY' if complete else 'SCREEN_ONLY_NOT_VALIDATED')
    (OUT/f'summary_{variant}.json').write_text(json.dumps(output,indent=2))
    print(json.dumps({s:{k:v for k,v in r.items() if k!='cases'} for s,r in result.items()}),flush=True)
    return output


if __name__=='__main__':analyze(sys.argv[1])
