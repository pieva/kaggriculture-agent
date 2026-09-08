"""Report all release attempts and exact matched controls without cherry-picking."""
import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

BASE = Path(__file__).resolve().parents[1]
DERIVED = BASE/'artifacts/derived'


def summarize(path, controls):
    payload = json.loads(path.read_text())
    rows = []
    for r in payload['matches']:
        control = controls[(r['seed'],r['seat'],r['opponent'])]
        end = r['daily'][-1]
        actions = Counter()
        harvest = Counter()
        for day in r['ledger']['daily']:
            actions.update(day['executed_actions'])
            harvest.update(day['harvested'])
        row = dict(seed=r['seed'], seat=r['seat'], opponent=r['opponent'], cash=r['reward'],
            control_cash=control['reward'], cash_delta=r['reward']-control['reward'],
            final_topology=end['pasture_topology'], final_animals=end['animals'],
            exact_populated_770=(end['pasture_topology']=={'Q0':7,'Q1':7,'Q2':0,'Q3':0}
                                  and end['occupied_livestock_tiles']==14),
            crop_deaths=len(r['crop_starvation']), animal_escapes=len(r['ledger']['animal_escapes']),
            errors=r['errors'], statuses=r['statuses'], incomplete_missions=r['incomplete_missions'],
            cash_parity_errors=r['ledger']['cash_parity_errors'], max_hands=r['max_hands'],
            max_animals=r['max_resources'], min_cash=r['min_cash'],
            max_call_seconds=r.get('max_call_seconds'),
            PASS=r['totals'].get('PASS',0), control_PASS=control['totals'].get('PASS',0),
            pass_d5_d10=sum(d.get('PASS',0) for d in r['action_daily'][4:10]),
            control_pass_d5_d10=sum(d.get('PASS',0) for d in control['action_daily'][4:10]),
            cows_d10=r['daily'][9]['animals']['COW'], control_cows_d10=control['daily'][9]['animals']['COW'],
            executed_services=dict(actions), harvested=dict(harvest),
            bootstrap_release=[e for e in r.get('common_events',[]) if e['event']=='bootstrap_retired'])
        row['safety_pass'] = not any(row[k] for k in ('crop_deaths','animal_escapes','errors','incomplete_missions','cash_parity_errors')) and row['max_hands']<=12 and row['max_animals']<=14 and all(s=='DONE' for s in row['statuses'])
        rows.append(row)
    groups = defaultdict(list)
    for r in rows: groups[r['seed']].append(r['cash_delta'])
    return dict(file=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        complete=payload['complete'], failures=payload['failures'], cases=len(rows), matches=rows,
        aggregate=dict(cash=mean(r['cash'] for r in rows),control_cash=mean(r['control_cash'] for r in rows),
            cash_delta=mean(r['cash_delta'] for r in rows), cash_delta_percent=100*(sum(r['cash'] for r in rows)/sum(r['control_cash'] for r in rows)-1),
            safety_pass=sum(r['safety_pass'] for r in rows),exact_populated_770=sum(r['exact_populated_770'] for r in rows),
            crop_deaths=sum(r['crop_deaths'] for r in rows),animal_escapes=sum(r['animal_escapes'] for r in rows),
            incomplete_missions=sum(r['incomplete_missions'] for r in rows),
            median_cows_d10=median(r['cows_d10'] for r in rows),median_control_cows_d10=median(r['control_cows_d10'] for r in rows),
            mean_pass_d5_d10=mean(r['pass_d5_d10'] for r in rows),mean_control_pass_d5_d10=mean(r['control_pass_d5_d10'] for r in rows),
            seed_mean_deltas={str(s):mean(values) for s,values in groups.items()},
            max_call_seconds=max((r['max_call_seconds'] for r in rows if r['max_call_seconds'] is not None),default=None)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    assert not args.output.exists(), 'Preserve completed summaries'
    baseline = json.loads((DERIVED/'E18_31_ASSIGNMENT_GATE_UNIFIED_V11_DEVELOPMENT_20260906.json').read_text())
    controls = {(r['seed'],r['seat'],r['opponent']):r for r in baseline['matches']}
    assert len(controls)==len(baseline['matches'])
    paths = [DERIVED/'E18_33_COMMON_GATE_V10_SHORT_BOOTSTRAP_20260907.json'] + sorted(DERIVED.glob('E18_CLOSEOUT_GATE_V*_20260907.json'))
    recovered = {json.loads(path.read_text()).get('recovery',{}).get('original_file') for path in paths}
    paths = [path for path in paths if path.name not in recovered]
    runs = [summarize(path,controls) for path in paths if json.loads(path.read_text())['matches']]
    for run in runs:
        a = run['aggregate']
        run['eligible_for_release'] = bool(run['complete'] and run['cases']==28 and a['safety_pass']==28
            and a['exact_populated_770']==28 and a['cash_delta']>=0
            and a['median_cows_d10']>=a['median_control_cows_d10']
            and a['mean_pass_d5_d10']<=a['mean_control_pass_d5_d10'])
    result = dict(runs=runs, uploaded=False, e19_started=False,
                  selection=[r['file'] for r in runs if r['eligible_for_release']],
                  interpretation='Internal matched development evidence; no claim of Top770 equivalence. Incomplete runs are not completed gates.')
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    for run in runs:
        print(run['file'],run['cases'],run['aggregate'])


if __name__ == '__main__': main()
