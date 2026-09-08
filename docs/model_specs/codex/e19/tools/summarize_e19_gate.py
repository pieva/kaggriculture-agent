"""Matched development summary; historical controls are not external benchmarks."""
import argparse
import json
from pathlib import Path
from statistics import mean, median


def key(m): return m['seed'],m['seat'],m['opponent']


def stats(matches):
    return dict(cases=len(matches),cash_mean=mean(m['reward'] for m in matches),
        crop_deaths=sum(len(m['crop_starvation']) for m in matches),
        animal_losses=sum(len(m['ledger']['animal_escapes']) for m in matches),
        incomplete_missions=sum(m['incomplete_missions'] for m in matches),
        errors=sum(m['errors'] for m in matches),
        cash_parity_errors=sum(m['ledger']['cash_parity_errors'] for m in matches),
        max_call_seconds=max(m.get('max_call_seconds',0) for m in matches),
        maximum_overage_seconds=max(m.get('overage_seconds',0) for m in matches),
        pass_d5_d10_mean=mean(sum(m['action_daily'][i].get('PASS',0) for i in range(4,10)) for m in matches),
        daily=[dict(day=i+1,cash_mean=mean(m['daily'][i]['money'] for m in matches),
            cows_median=median(m['daily'][i]['animals']['COW'] for m in matches),
            sheep_median=median(m['daily'][i]['animals']['SHEEP'] for m in matches),
            hands_median=median(m['daily'][i]['hands'] for m in matches),
            crops_mean=mean(m['daily'][i]['crop_tiles'] for m in matches),
            pass_mean=mean(m['action_daily'][i].get('PASS',0) for m in matches),
            move_mean=mean(m['action_daily'][i].get('MOVE',0) for m in matches),
            executed_mean={op:mean(m['ledger']['daily'][i]['executed_actions'].get(op,0) for m in matches)
                for op in ('FEED','CARE','WATER','HARVEST')}) for i in range(30)])


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--gate',type=Path,required=True)
    p.add_argument('--control',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    d=json.loads(a.gate.read_text()); c=json.loads(a.control.read_text())
    assert d['complete'] and c['complete'] and not a.output.exists()
    dm={key(m):m for m in d['matches']}; cm={key(m):m for m in c['matches']}
    assert len(dm)==len(d['matches']) and set(dm)==set(cm)
    ds,cs=stats(list(dm.values())),stats(list(cm.values()))
    result=dict(gate=str(a.gate),control=str(a.control),external_benchmark=False,
        candidate=ds,reference=cs,cash_change_percent=100*(ds['cash_mean']/cs['cash_mean']-1),
        exact_populated_topology=sum(m['exact_populated_topology'] for m in dm.values()),
        safety_pass=sum(m['safety_pass'] for m in dm.values()),
        paired_cash=[dict(seed=k[0],seat=k[1],opponent=k[2],candidate=dm[k]['reward'],
            reference=cm[k]['reward'],difference=dm[k]['reward']-cm[k]['reward']) for k in sorted(dm)])
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('candidate','reference','paired_cash')}))
    print(json.dumps(ds|{'daily':'see report'}))


if __name__=='__main__': main()
