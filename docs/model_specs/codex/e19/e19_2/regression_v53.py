"""Replay the known D26 starvation state, changing only the V53 guard at D26."""
import copy,gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT));HERE=Path(__file__).resolve().parent
from fixes_v53 import install
def main():
    from kaggle_environments import make
    r=json.load(gzip.open(HERE/'artifacts/v52d/180911301_0.replay.json.gz','rt',encoding='utf-8'))
    results=[]
    for fixed in [False,True]:
        ns={};exec((ROOT/'submission/archive/e19_rejected/submission_codex_e19_2_770_v52d.py').read_text(encoding='utf-8'),ns)
        agent=ns['create_agent']({'player_position':0})
        for i in range(600):agent(copy.deepcopy(r['steps'][i][0]['observation']),r['configuration'])
        if fixed:install(agent.core)
        env=make('kaggriculture',configuration=r['configuration'],steps=copy.deepcopy(r['steps'][:601]),debug=False)
        actions=[]
        for i in range(600,624):
            action=agent(copy.deepcopy(env.state[0]['observation']),r['configuration']);actions.append(action)
            env.step([action,copy.deepcopy(r['steps'][i+1][1]['action'])])
        tile=env.state[0]['observation']['farms'][0]['tiles'][4][7]
        match=sum(a==r['steps'][i+601][0]['action'] for i,a in enumerate(actions))
        results.append(dict(fixed=fixed,target_tile=tile,control_action_matches=match,actions=actions))
        print('REGRESSION',fixed,'tile',tile,'control matches',match,flush=True)
    assert results[0]['control_action_matches']==24,'Control must reproduce the recorded D26 actions'
    assert not results[0]['target_tile'].get('animal'),'Recorded control escape must be reproduced'
    assert results[1]['target_tile'].get('animal')=='SHEEP','Fix must preserve the threatened sheep'
    dest=HERE/'reports/v53/STARVATION_REGRESSION.json'
    dest.write_text(json.dumps(dict(method='Known V52D state after identical warm-up. Guard installed only from D26; opponent actions fixed for 24 ticks. Diagnostic, not a ranking match.',results=results),indent=2),encoding='utf-8')
if __name__=='__main__':main()
