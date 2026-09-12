"""Read-only, paired descriptive analysis; no new agent or engine runs."""
import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'docs/model_specs/codex/e20'
OUT = BASE / 'reports/livestock_routine_20260912'
PHASES = {'D1-11': (1, 11), 'D12-19': (12, 19), 'D20-29': (20, 29), 'D30': (30, 30)}


def main():
    cases, sources = [], {}
    for p in sorted((BASE / 'artifacts/e20_2_confirmation').glob('*.kpi.json')):
        data = json.loads(p.read_text(encoding='utf-8'))
        if {s['name'] for s in data['sides']} != {'E18', 'E20.2'}:
            continue
        raw = gzip.decompress(p.with_name(p.name.replace('.kpi.json', '.replay.json.gz')).read_bytes())
        assert hashlib.sha256(raw).hexdigest() == data['replay_sha256']
        replay = json.loads(raw)
        assert len(replay['steps']) == 720
        sources[p.relative_to(ROOT).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
        for side in data['sides']:
            seat = side['seat']
            routines = defaultdict(dict)
            for step in range(1, 720):
                previous = replay['steps'][step - 1][seat]['observation']
                action = replay['steps'][step][seat]['action']
                day, hour = (step - 1) // 24 + 1, (step - 1) % 24 + 1
                farm = previous['farms'][seat]
                actors = [farm['farmer']] + farm['hands']
                cmds = [action.get('farmer', ['PASS'])] + action.get('hands', [])
                for worker, (pos, cmd) in enumerate(zip(actors, cmds)):
                    if cmd and cmd[0] in ['FEED', 'CARE']:
                        routines[day][(worker, hour)] = (cmd[0], tuple(pos))
            for phase, (lo, hi) in PHASES.items():
                daily = side['kpi'][lo-1:hi]
                ledger = side['ledger']['daily'][lo-1:hi]
                animal_days = sum(x['occupied_livestock_tiles'] for x in daily)
                requests = {a: sum(x['requested_actions'].get(a, 0) for x in ledger) for a in ['PASS', 'MOVE', 'FEED', 'CARE']}
                executed = {a: sum(x['executed_actions'].get(a, 0) for x in ledger) for a in ['FEED', 'CARE', 'WATER', 'HARVEST']}
                slots = sum(sum(x['requested_actions'].values()) for x in ledger)
                comparable = repeated = affinity_count = affinity_repeat = 0
                for day in range(lo + 1, hi + 1):
                    for key, value in routines[day].items():
                        comparable += 1
                        repeated += routines[day-1].get(key) == value
                    today = {(key[0], *value) for key,value in routines[day].items()}
                    yesterday = {(key[0], *value) for key,value in routines[day-1].items()}
                    affinity_count += len(today)
                    affinity_repeat += len(today & yesterday)
                cases.append(dict(seed=data['seed'], seat=seat, model=side['name'], phase=phase,
                    animals=animal_days/len(daily), crop_tiles=mean(x['crop_tiles'] for x in daily),
                    people=mean(x['people'] for x in daily), animal_days=animal_days,
                    **requests, **{a+'_executed': n for a,n in executed.items()},
                    pass_share=requests['PASS']/slots, move_share=requests['MOVE']/slots,
                    feed_per_animal_day=executed['FEED']/animal_days,
                    care_per_animal_day=executed['CARE']/animal_days,
                    feed_success=executed['FEED']/requests['FEED'] if requests['FEED'] else None,
                    care_success=executed['CARE']/requests['CARE'] if requests['CARE'] else None,
                    repeated_service_share=repeated/comparable if comparable else None,
                    repeated_worker_tile_service_share=affinity_repeat/affinity_count if affinity_count else None,
                    hire_cash=sum(x['hire_cash'] for x in ledger),
                    livestock_sales=sum(sum(x['sales_cash'].get(a,0) for a in ['MILK','WOOL','EGG','FERTILIZER']) for x in ledger),
                    wheat_purchase=sum(x['purchase_cash'].get('BUY_PRODUCT:WHEAT',0) for x in ledger),
                    starvation_events=sum(lo <= x['service_day'] <= hi for x in side['crop_starvation'])))
    summary = []
    for phase in PHASES:
        for model in ['E18','E20.2']:
            group = [x for x in cases if x['phase']==phase and x['model']==model]
            summary.append(dict(phase=phase,model=model,**{k:mean(x[k] for x in group if x[k] is not None) if any(x[k] is not None for x in group) else None for k in group[0] if k not in ['seed','seat','model','phase']}))
    OUT.mkdir(exist_ok=True)
    payload = dict(matches=14, seeds=7, summary=summary, cases=cases, sources=sources,
        definitions={'animal_day':'Occupied livestock count at daily KPI checkpoint; descriptive exposure, not exact within-day feed obligation.',
        'pass_share':'Explicit requested PASS / all ledger requested worker actions; not salary efficiency.',
        'repeated_service_share':'Among FEED/CARE requests, same operation by same worker index at same hour and coordinate on preceding day within phase. New hires at that hour excluded if absent in pre-action state. Requests, not successful services. Worker indices across days are schedule slots, not persistent individuals.',
        'repeated_worker_tile_service_share':'Same worker index, coordinate and FEED/CARE operation as preceding day, regardless of hour; unique combinations per day. Describes assignment persistence, not causal efficiency.',
        'starvation_events':'Verified crop disappearance from crop_service_audit; different from snapshot water stress.'})
    (OUT/'ANALYSIS.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
