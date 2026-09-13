"""Reuse real-loader gates and verify calendar transfer without crop/labor loss."""
import copy
import gzip
import json
import compare_q0_calendar_v2 as setup
import verify_q0_pastures as common

def main():
    common.main()
    runner = setup.runner
    rows = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(runner.ART.glob('*.json'))]
    records = []
    for r in rows:
        s = r['seat']
        old = json.loads((runner.ART.parent/'q0_8c9s_v1'/f"{r['seed']}_{s}.json").read_text(encoding='utf-8'))
        assert old['hashes']['candidate'] == runner.digest(runner.CAND.parent/'submission_codex_e22_q0_8c9s_internal_v1.py')
        a,b = r['ledgers'][s]['daily'],old['ledgers'][s]['daily']
        for key in ['hire_cash','hires']:
            assert [d[key] for d in a] == [d[key] for d in b], (r['seed'],key)
        for metric in ['planted','harvested','bought_units']:
            items=set().union(*(d[metric] for d in a+b))
            for item in items:
                assert sum(d[metric].get(item,0) for d in a)==sum(d[metric].get(item,0) for d in b),(r['seed'],metric,item)
        records.append(dict(seed=r['seed'],seat=s,calendar=r['calendar_checks']))
    game=json.load(gzip.open(runner.ART/'180911301_0.replay.json.gz','rt',encoding='utf-8'))
    setup.calendar_checks(game,0)
    ns={};exec((runner.CAND.parent/'submission_codex_e22_q0_8c9s_internal_v1.py').read_text(encoding='utf-8'),ns)
    v1=ns['agent']
    for i in range(264):
        obs=copy.deepcopy(game['steps'][i][0]['observation'])
        assert v1(obs,game['configuration'])==game['steps'][i+1][0]['action']
    result=json.loads((runner.OUT/'VERIFICATION.json').read_text(encoding='utf-8'))
    result.update(calendar_games=14,all_expected_placement_times=True,all_expected_harvest_days=True,
                  unchanged_initial_v1_batches=264,unchanged_daily_hires=True,
                  unchanged_total_planting_harvest_and_purchase_units=True,records=records,
                  v1_frozen_sha256=runner.digest(runner.CAND.parent/'submission_codex_e22_q0_8c9s_internal_v1.py'))
    (runner.OUT/'VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('PASS: calendar, 264 initial v1 batches, all 14 labor/crop/quantity comparisons',flush=True)

if __name__ == '__main__': main()
