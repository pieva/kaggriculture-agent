"""Attribute frozen opening PASS to the embedded routine, without future inputs."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909'


def main():
    cohort=json.loads((ROOT/'docs/model_specs/codex/e19/reports/v48_external_pass_update_20260908/cohort.json').read_text())
    entry=next(g for g in cohort['games'] if g['episode']==106843637)
    path=ROOT/entry['raw_path']
    if not path.exists():path=Path('C:/Users/pietr/Projects/kaggriculture-agent')/entry['raw_path']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
    replay=json.loads(path.read_text());seat=entry['seat']
    policy=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_v48_external.py'))['create_agent']({'player_position':seat})
    routine_agent=policy.teacher.codex_e18_capacity_governed_instance.base_policy.codex_e17_batched_cluster_routing_instance.base_policy.codex_e17_true_reactive_instance.base_policy.codex_e17_instance.base_policy.codex_v9_instance
    namespace=routine_agent.__call__.__func__.__globals__
    routine=namespace['ROUTINE_ACTIONS']
    rows=[]
    for i in range(1,265):
        obs=replay['steps'][i-1][seat]['observation'];recorded=replay['steps'][i][seat]['action']
        actions=[recorded['farmer'],*recorded['hands']]
        original=[routine[i-1]['farmer'],*routine[i-1]['hands']]
        for w,pos in enumerate([obs['farms'][seat]['farmer'],*obs['farms'][seat]['hands']]):
            if actions[w]!=['PASS']:continue
            reason='present_in_frozen_routine' if w<len(original) and original[w]==['PASS'] else 'added_by_opening_overrides'
            rows.append(dict(day=obs['day']+1,hour=obs['hour']+1,worker=w,position=pos,reason=reason,
                routine_command=original[w] if w<len(original) else None))
    result=dict(episode=entry['episode'],replay_sha256=entry['sha256'],routine_sha256=namespace['ROUTINE_SHA256'],
        semantics='Provenance of PASS in the fixed action table; not a certificate of biological inevitability.',
        total=len(rows),causes=dict(Counter(r['reason'] for r in rows)),rows=rows)
    (OUT/'opening_attribution.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}))


if __name__=='__main__':main()
