"""Verify the repaired bundle against its saved episodes, without new games."""
import gzip,hashlib,json,sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
BASE=Path(__file__).resolve().parent

def nested_errors(root):
    seen=set(); found=[]
    def visit(obj,path):
        if id(obj) in seen:return
        seen.add(id(obj))
        attrs=getattr(obj,'__dict__',{})
        for key in ('error_count','fallback_count','last_exception'):
            if attrs.get(key):found.append([path,key,attrs[key]])
        for key,value in attrs.items():
            if key in ('core','parent','original_provider','base_policy','policy') or key.endswith('_instance'):
                visit(value,path+'.'+key)
    visit(root,'agent')
    return found

def main():
    revision=3
    bundle=BASE/f'artifacts/repaired774_v{revision}.py'
    results=[]
    for path in sorted((BASE/f'artifacts/repair774_v{revision}').glob('*_18091130[13].json')):
        meta=json.loads(path.read_text())
        raw=gzip.decompress(path.with_suffix('.replay.json.gz').read_bytes())
        assert hashlib.sha256(raw).hexdigest()==meta['replay_sha256']
        replay=json.loads(raw)
        seat=meta['agents'].index('Repair774')
        ns={'__name__':'_verify_repair'}
        exec(compile(bundle.read_text(encoding='utf-8'),'<standalone>','exec'),ns)
        old_ns={'__name__':'_verify_opening'}
        exec(compile((BASE/'artifacts/fixed774_reconstruction.py').read_text(encoding='utf-8'),'<frozen774>','exec'),old_ns)
        old_policy=old_ns['create_agent']({'player_position':seat})
        prefix_mismatch=[]
        mismatch=[]; invalid_services=[]; topology=[]; maximum=0; uncovered=[]; sowings=0
        for i in range(719):
            obs=deepcopy(replay['steps'][i][seat]['observation'])
            # Kaggle stores shared observation fields only on seat zero.
            obs={'step':replay['steps'][i][0]['observation']['step'],**obs}
            action=ns['agent'](obs,deepcopy(replay['configuration']))
            if i<264 and old_policy(deepcopy(obs),deepcopy(replay['configuration']))!=action:
                prefix_mismatch.append(i)
            if action!=replay['steps'][i+1][seat]['action']:mismatch.append(i)
            farm=obs['farms'][seat]
            positions=[farm['farmer'],*farm['hands']]
            commands=[action['farmer'],*action['hands']]
            for worker,cmd in enumerate(commands):
                if positions[worker]==[4,7] and cmd[0] in ('BUILD_PASTURE','PLACE','FEED','CARE','COLLECT_FERTILIZER'):
                    invalid_services.append([i,worker,cmd])
                if positions[worker]==[4,7] and cmd[0]=='PLANT' and i+2<720:
                    after=replay['steps'][i+1][seat]['observation']['farms'][seat]['tiles'][7][4]
                    watered=replay['steps'][i+2][seat]['observation']['farms'][seat]['tiles'][7][4]
                    if isinstance(after,dict) and after.get('kind')=='PLANT':
                        sowings+=1
                        if not isinstance(watered,dict) or not watered.get('watered_today'):uncovered.append(i)
        policy=ns['_REPAIR774_ACTIVE'][seat][1]
        for i,state in enumerate(replay['steps']):
            obs=state[seat]['observation'];farm=obs['farms'][seat];counts=[0]*4;animals=0
            for y,row in enumerate(farm['tiles']):
                for x,t in enumerate(row):
                    if isinstance(t,dict):
                        animals+=bool(t.get('animal'))
                        if t.get('kind')=='PASTURE':counts[int(x>=5)+2*int(y>=5)]+=1
            maximum=max(maximum,animals)
            if any(c>cap for c,cap in zip(counts,[7,7,4,0])):topology.append([i,counts])
        kpi=json.loads(path.with_suffix('.kpi.json').read_text())
        s=kpi['sides'][seat]; other=kpi['sides'][1-seat]
        finalobs=replay['steps'][-1][seat]['observation']
        private=finalobs['private']
        residual={a:private['shed'].get(a,0)+sum(inv.get(a,0) for inv in private['inventories']) for a in ['COW','SHEEP','GOOSE']}
        bought=Counter()
        for d in s['ledger']['daily']:
            bought.update({a:v for a,v in d['bought_units'].items() if a.startswith('BUY_ANIMAL:')})
        first=ns['agent']({'step':0,**deepcopy(replay['steps'][0][seat]['observation'])},replay['configuration'])
        reset=first==replay['steps'][1][seat]['action'] and ns['_REPAIR774_ACTIVE'][seat][1] is not policy
        findings=[]
        checks={'public_parity':not mismatch,'reset':reset,'topology':not topology and counts==[7,7,4,0],
                'no_animal_commands_on_target':not invalid_services,'max18_animals':maximum<=18,
                'final_portfolio':s['kpi'][-1]['animals']=={'COW':8,'SHEEP':9,'GOOSE':1},
                'no_unused_animals':not any(residual.values()),'no_nested_errors':not nested_errors(policy),
                'routes_rejoined':not policy.detours and policy.metrics['rejoins']==policy.metrics['excursions_removed'],
                'cash_parity':s['ledger']['cash_parity_errors']==0,'no_escapes':not s['ledger']['animal_escapes']}
        if revision>=2:
            checks['unchanged_D1_D11']=not prefix_mismatch
            checks['target_sowing_watered_next_turn']=not uncovered
            checks['no_target_starvation']=not any(e['position']==[4,7] for e in s['crop_starvation'])
        results.append({'source':path.name,'seat':seat,'checks':checks,'reward':s['reward'],'opponent_reward':other['reward'],
                        'margin':s['reward']-other['reward'],'bought':bought,'residual':residual,'metrics':policy.metrics,
                        'mismatches':mismatch,'invalid_services':invalid_services,'nested_errors':nested_errors(policy),
                        'target_sowings':sowings,'uncovered_sowings':uncovered,
                        'crop_starvation':s['crop_starvation'],'final_kpi':s['kpi'][-1]})
    assert len(results) in (2,4)
    out=BASE/f'reports/repair774_v{revision}';out.mkdir(exist_ok=True)
    (out/'VERIFICATION.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k not in ('crop_starvation','final_kpi')} for r in results],indent=2))
    assert all(all(r['checks'].values()) for r in results),'See saved verification failures'

if __name__=='__main__':main()
