"""Paired real-engine prefix experiment. Keep the real 720-step horizon."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
OUT = ROOT/'docs/model_specs/codex/e19/artifacts/derived/assisted_start_20260907'


def run_case(topology,seed,seat,verify_baseline=False):
    from kaggle_environments import make
    from docs.model_specs.codex.e19.tools.assisted_start import AssistedStart
    from docs.model_specs.codex.e19.tools.run_paired_kpi_v4d import detail, BUNDLES
    from docs.model_specs.codex.e18.tools.run_e18_27_d10_d15_cashflow_gate import opponent_policy
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
    corepath=ROOT/'submission'/BUNDLES[topology]
    core=runpy.run_path(str(corepath))['create_agent']({'player_position':seat})
    shadow=None
    bundlepath=None
    if verify_baseline:
        assisted=core
    else:
        model='e18_770' if topology=='770' else 'e19_662'
        bundlepath=ROOT/'submission'/f'submission_codex_{model}_assisted_start_v1_candidate.py'
        assisted=runpy.run_path(str(bundlepath))['create_agent']({'player_position':seat})
        shadow=AssistedStart(opponent_policy('E18.2/V4D',seed,seat),core)
    opponent=opponent_policy('E18.2/V4D',seed,1-seat)
    policies=[assisted,opponent] if seat==0 else [opponent,assisted]
    env=make('kaggriculture',configuration={'episodeSteps':720,'turnsPerDay':24,'seed':seed},debug=False)
    env.reset(2)
    for step in range(264):
        # Use the SAME shared/hidden-field projection as Kaggle's agent runner.
        actions=[p(deepcopy(env._Environment__get_shared_state(i).observation),env.configuration) for i,p in enumerate(policies)]
        if shadow is not None:
            assert actions[seat]==shadow(deepcopy(env._Environment__get_shared_state(seat).observation),env.configuration), ('source_bundle_parity',step)
        env.step(actions)
        assert all(s.status=='ACTIVE' for s in env.state)
    replay=env.toJSON()
    assert len(replay['steps'])==265
    # audit accepts a terminal valuation; here it is explicitly prefix cash,
    # never a game reward. Actual environment status remains ACTIVE.
    partial=deepcopy(replay)
    partial['rewards']=[s['observation']['farms'][i]['money'] for i,s in enumerate(replay['steps'][-1])]
    sides={}
    for label,position in [('assisted',seat),('v4d',1-seat)]:
        ledger=audit(partial,position)
        ledger['cash_parity_steps_both_players']=264
        ledger['daily']=ledger['daily'][:11]
        daily=[]
        for day in range(1,12):
            row=snapshot(replay,day,position)
            row.update(detail(replay['steps'][day*24-1][position]['observation'],position))
            row['settled_cash']=replay['steps'][day*24][position]['observation']['farms'][position]['money']
            daily.append(row)
        sides[label]=dict(daily=daily,ledger=ledger,prefix_cash=partial['rewards'][position])
    if verify_baseline:
        old=json.loads((ROOT/'docs/model_specs/codex/e19/artifacts/derived/paired_kpi_v4d_20260907'/f'{topology}_{seed}_{seat}.json').read_text())
        for newlabel,oldlabel in [('assisted','parametric'),('v4d','v4d')]:
            for newrow,oldrow in zip(sides[newlabel]['daily'],old['sides'][oldlabel]['daily']):
                assert all(newrow[k]==v for k,v in oldrow.items()), (newlabel,newrow,oldrow)
            assert sides[newlabel]['ledger']['daily']==old['sides'][oldlabel]['ledger']['daily'][:11]
        print(json.dumps(dict(baseline_prefix_parity=True,topology=topology,seed=seed,seat=seat)),flush=True)
        OUT.mkdir(parents=True,exist_ok=True)
        (OUT/f'parity_{topology}_{seed}_{seat}.json').write_text(json.dumps(dict(passed=True,batches=264,comparison='both farms: all daily fields and reconstructed flows D1-D11'))+'\n')
        return
    # Verify the target cap at EVERY state, including simultaneous builds.
    violations=[]
    for step,states in enumerate(replay['steps']):
        farm=states[seat]['observation']['farms'][seat]
        counts={q:0 for q in ('NW','NE','SW','SE')}
        for y,row in enumerate(farm['tiles']):
            for x,t in enumerate(row):
                if isinstance(t,dict) and t.get('kind')=='PASTURE':
                    counts[('N' if y<5 else 'S')+('W' if x<5 else 'E')]+=1
        budgets=core.profile.pasture_budgets(farm['unlocked_quadrants'])
        if any(n>budgets.get(q,0) for q,n in counts.items()): violations.append(step)
    assert not violations,violations
    # One dependent handover call verifies interface only, not D12 economics.
    handover_action=assisted(env._Environment__get_shared_state(seat).observation,env.configuration)
    assert handover_action==shadow(deepcopy(env._Environment__get_shared_state(seat).observation),env.configuration)
    assert assisted.handed_over and assisted.core.bootstrap_done and assisted.core.error_count==0
    assert set(handover_action)=={'farmer','hands','market'}
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [bundlepath,corepath,ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py',Path(__file__),Path(__file__).with_name('assisted_start.py')]}
    result=dict(topology=topology,seed=seed,seat=seat,scope='D1-D11; D12 interface smoke only',
                configuration=replay['configuration'],executed_batches=264,game_finished=False,
                sources=hashes,sides=sides,capacity_violations=violations,events=assisted.events,
                handover_interface_pass=True,
                source_bundle_action_parity=265,
                actions_sha256=hashlib.sha256(json.dumps([s[seat]['action'] for s in replay['steps'][1:]],sort_keys=True).encode()).hexdigest())
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f'{topology}_{seed}_{seat}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(topology=topology,seed=seed,seat=seat,cash=result['sides']['assisted']['prefix_cash'],reference=result['sides']['v4d']['prefix_cash'],filters=len(assisted.events)-1)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify-baseline',action='store_true');p.add_argument('--seeds',type=int,nargs='+',default=[180903001]);p.add_argument('--seats',type=int,nargs='+',default=[0]);p.add_argument('--topologies',nargs='+',default=['770','662']);a=p.parse_args()
    for topology in a.topologies:
        for seed in a.seeds:
            for seat in a.seats:run_case(topology,seed,seat,a.verify_baseline)
