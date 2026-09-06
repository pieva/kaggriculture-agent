"""Paired E18.32 audit: absolute idle time AND utilization, yield and safety."""
import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import mean

BASE=Path(__file__).resolve().parents[1]
DERIVED=BASE/'artifacts/derived'
CONTROL='E18_31_ASSIGNMENT_GATE_UNIFIED_V11_DEVELOPMENT_20260906.json'


def key(m):
    return m['opponent'],m['seed'],m['seat']


def phase(m,first,last):
    counts=sum((Counter(d) for d in m['action_daily'][first-1:last]),Counter())
    slots=sum(counts.values())
    productive=sum(n for op,n in counts.items() if op not in {'MOVE','PASS','PICKUP','DROP'})
    return dict(passes=counts['PASS'],moves=counts['MOVE'],slots=slots,pass_percent=100*counts['PASS']/slots,
                productive_requests=productive,productive_percent=100*productive/slots,
                hire_cash=sum(d['hire_cash'] for d in m['ledger']['daily'][first-1:last]),
                cow_days=sum(d['animals']['COW'] for d in m['daily'][first-1:last]))


def safety(m):
    return dict(errors=m['errors']==0,crop_deaths=not m['crop_starvation'],
                escapes=not m['ledger']['animal_escapes'],missions=m['incomplete_missions']==0,
                ledger=m['ledger']['cash_parity_errors']==0,cap=m['max_resources']<=14 and m['max_hands']<=12,
                filled=m['daily'][-1]['animals']=={'COW':9,'SHEEP':5,'GOOSE':0},
                topology=m['daily'][-1]['pasture_topology']=={'Q0':7,'Q1':7,'Q2':0,'Q3':0})


def summarize(matches,control):
    controls=[control[key(m)] for m in matches]
    result=dict(n=len(matches),independent_seeds=len({m['seed'] for m in matches}),
                baseline_cash=mean(m['reward'] for m in controls),candidate_cash=mean(m['reward'] for m in matches),
                positive=sum(m['reward']>b['reward'] for m,b in zip(matches,controls)),
                minimum_cash_delta=min(m['reward']-b['reward'] for m,b in zip(matches,controls)),
                wins_baseline=sum(m['reward']>m['opponent_reward'] for m in controls),
                wins_candidate=sum(m['reward']>m['opponent_reward'] for m in matches))
    result['cash_delta_percent']=100*(result['candidate_cash']/result['baseline_cash']-1)
    result['phases']={}
    for first,last in [(1,10),(5,10),(11,15),(16,30),(1,30)]:
        left=[phase(m,first,last) for m in controls]
        right=[phase(m,first,last) for m in matches]
        result['phases'][f'D{first}_D{last}']={
            'baseline':{k:mean(v[k] for v in left) for k in left[0]},
            'candidate':{k:mean(v[k] for v in right) for k in right[0]}}
    result['days']=[dict(day=d,
        baseline_pass=mean(m['action_daily'][d-1].get('PASS',0) for m in controls),
        candidate_pass=mean(m['action_daily'][d-1].get('PASS',0) for m in matches),
        baseline_hands=mean(m['daily'][d-1]['hands'] for m in controls),
        candidate_hands=mean(m['daily'][d-1]['hands'] for m in matches),
        baseline_cows=mean(m['daily'][d-1]['animals']['COW'] for m in controls),
        candidate_cows=mean(m['daily'][d-1]['animals']['COW'] for m in matches)) for d in range(1,31)]
    result['pairs']=[dict(case=key(m),baseline_cash=b['reward'],candidate_cash=m['reward'],
                        cash_delta=m['reward']-b['reward'],
                        cow_day_delta=phase(m,1,10)['cow_days']-phase(b,1,10)['cow_days'],
                        checks=safety(m)) for m,b in zip(matches,controls)]
    result['daily_cow_stock_identical']=all([d['animals']['COW'] for d in m['daily']]==
        [d['animals']['COW'] for d in b['daily']] for m,b in zip(matches,controls))
    result['daily_crop_stock_identical']=all([d['crops'] for d in m['daily']]==
        [d['crops'] for d in b['daily']] for m,b in zip(matches,controls))
    harvested=lambda m:sum((Counter(d['harvested']) for d in m['ledger']['daily']),Counter())
    products=sorted({k for m in [*matches,*controls] for k in harvested(m)})
    result['harvested_units']={k:dict(baseline=mean(harvested(m)[k] for m in controls),
        candidate=mean(harvested(m)[k] for m in matches)) for k in products}
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--candidate',required=True)
    p.add_argument('--label',required=True)
    args=p.parse_args()
    data=json.loads((DERIVED/args.candidate).read_text())
    assert data['complete'] and not data['failures']
    control={key(m):m for m in json.loads((DERIVED/CONTROL).read_text())['matches']}
    assert len({key(m) for m in data['matches']})==len(data['matches'])
    result=dict(candidate_source=args.candidate,baseline_source=CONTROL,holdout_consumed=False,
                all=summarize(data['matches'],control),
                opponents={o:summarize([m for m in data['matches'] if m['opponent']==o],control)
                           for o in sorted({m['opponent'] for m in data['matches']})})
    output=DERIVED/f'E18_32_READY_WORK_SUMMARY_{args.label}.json'
    assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result['all'].items() if k not in {'days','pairs'}},indent=2))


if __name__=='__main__':
    main()
