"""Reconstruct the published policy on its observations, assert action parity.

No counterfactual opponent, new replay selection, or black-box cause inference.
"""
import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path

from docs.model_specs.codex.e18.tools.e18_31_unified_investment_controller import UnifiedInvestmentController

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[3]


def main():
    plan=json.loads((BASE/'artifacts/derived/E18_28_FULL_SEASON_C_PLAN_V1.json').read_text())
    corpus=json.loads((BASE/'artifacts/derived/E18_31_EXTERNAL_SUBMISSION_FIRST6_20260906.json').read_text())
    results=[]
    for profile in corpus['profiles']:
        episode,seat=profile['episode_id'],profile['seat']
        path=ROOT/f'data/replays/json/{episode}.json'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==profile['sha256']
        replay=json.loads(path.read_text())
        agent=UnifiedInvestmentController(deepcopy(plan),seat)
        days=[dict(day=d,reasons=Counter(),actions=Counter(),slots=0,pass_snapshots=[]) for d in range(1,31)]
        for i,state in enumerate(replay['steps'][:-1]):
            obs=state[seat]['observation']
            actual=agent(obs,replay['configuration'])
            expected=replay['steps'][i+1][seat]['action']
            assert actual==expected,(episode,i,'source/public parity failure',actual,expected)
            day,hour=obs['day']+1,obs['hour']+1
            farm,private=obs['farms'][seat],obs['private']
            row=days[day-1]
            waiting=[]
            for w,cmd in enumerate([actual['farmer'],*actual['hands']]):
                row['slots']+=1
                row['actions'][cmd[0]]+=1
                if cmd[0]!='PASS':
                    continue
                pending=agent._remaining_rows(day,w)
                reason=('queue_exhausted' if not pending else 'scheduled_wait'
                        if pending[0]['turn']>hour else 'blocked_'+pending[0]['opcode'])
                row['reasons'][reason]+=1
                waiting.append(dict(worker=w,position=agent._position(farm,w),reason=reason,
                                    inventory=dict(agent._inventory(private,w)),next=pending[0] if pending else None))
            if waiting and day<=10:
                tiles=[t for r in farm['tiles'] for t in r if isinstance(t,dict)]
                row['pass_snapshots'].append(dict(hour=hour,money=farm['money'],hands=len(farm['hands']),
                    crops=dict(Counter(t['crop'] for t in tiles if t.get('kind')=='PLANT')),
                    animals=dict(Counter(t['animal'] for t in tiles if t.get('animal'))),
                    animal_services_left=dict(Counter({'FEED':sum(not t.get('fed_today') for t in tiles if t.get('animal')),
                        'CARE':sum(not t.get('cared_today') for t in tiles if t.get('animal')),
                        'COLLECT_FERTILIZER':sum(bool(t.get('fertilizer_available')) for t in tiles if t.get('animal'))})),
                    waiting=waiting))
        assert agent.error_count==0
        results.append(dict(episode_id=episode,opponent=profile['opponent'],replay_sha256=profile['sha256'],
                            identical_batches=719,daily=days))
        print(episode,'parity 719/719',dict(sum((d['reasons'] for d in days[4:10]),Counter())),flush=True)
    output=BASE/'artifacts/derived/E18_32_PUBLISHED_PASS_ROOT_AUDIT_20260906.json'
    assert not output.exists()
    payload=dict(published_submission=56050866,results=results,
                 note='Queue labels explain immediate dispatch conditions, not all economically avoidable idle time.',
                 source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    output.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
