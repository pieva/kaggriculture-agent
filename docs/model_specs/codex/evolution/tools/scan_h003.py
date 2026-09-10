"""H003 one-transition counterfactual, simultaneous opponent action held fixed."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.evolution.tools.market_order import reorder
from docs.model_specs.codex.evolution.tools.branch_replay import canonical
BASE=ROOT/'docs/model_specs/codex/evolution';SOURCE=ROOT/'docs/model_specs/codex/e20/artifacts/e20_1_confirmation';OUT=BASE/'reports/H003'
def main():
    from kaggle_environments import make
    rows=[]
    for p in sorted(SOURCE.glob('*.json')):
        if '.kpi.' in p.name:continue
        meta=json.loads(p.read_text())
        with gzip.open(p.with_suffix('.replay.json.gz'),'rb') as f:raw=f.read()
        assert hashlib.sha256(raw).hexdigest()==meta['replay_sha256'];r=json.loads(raw)
        actions=[s['action'] for s in r['steps'][457]]
        def env():return make('kaggriculture',configuration=copy.deepcopy(r['configuration']),info=copy.deepcopy(r['info']),steps=copy.deepcopy(r['steps'][:457]))
        c=env();c.step(copy.deepcopy(actions));assert canonical(c.state)==canonical(r['steps'][457])
        for seat,model in enumerate(meta['agents']):
            altered,reason=reorder(actions[seat]);modified=copy.deepcopy(actions);modified[seat]=altered
            if reason=='reordered':
                t=env();t.step(modified);after=t.state
            else:after=c.state
            delta=[after[0]['observation']['farms'][s]['money']-c.state[0]['observation']['farms'][s]['money'] for s in [0,1]]
            rows.append(dict(model=model,seed=meta['seed'],seat=seat,opponent=meta['agents'][1-seat],reason=reason,delta_cash=delta[seat],delta_margin=delta[seat]-delta[1-seat],action_before=actions[seat],action_after=altered,source_sha256=meta['replay_sha256']))
    assert len(rows)==84
    (OUT/'ONE_STEP.json').write_text(json.dumps(dict(rows=rows,verified_source_transitions=42),indent=2)+'\n')
    for m in ['E18','E19','E20.1']:
        rr=[r for r in rows if r['model']==m and r['reason']=='reordered']
        print(m,len(rr),sum(r['delta_cash'] for r in rr)/len(rr) if rr else 0,flush=True)
if __name__=='__main__':main()
