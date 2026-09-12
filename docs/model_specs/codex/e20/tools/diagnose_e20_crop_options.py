"""Read existing marginal crop valuations, requiring exact recorded actions."""
import gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.verify_revision import observation_at
BASE=ROOT/'docs/model_specs/codex/e20'
def main():
    rows=[]
    for seed in [180911301,180911303]:
        p=BASE/'artifacts/e20_2_confirmation'/f'E20.2_E18_{seed}.replay.json.gz'
        with gzip.open(p,'rt') as f:r=json.load(f)
        ns={'__name__':'_crop_trace'};bundle=ROOT/'submission/submission_codex_e20_772_e20v32_candidate.py'
        exec(compile(bundle.read_text(encoding='utf-8'),str(bundle),'exec'),ns)
        agent=ns['create_agent']({'player_position':0})
        for i in range(600):
            obs=observation_at(r,i,0);a=agent(obs,r['configuration']);assert a==r['steps'][i+1][0]['action'],(seed,i)
            if obs['day']>=11 and obs['hour']==12:
                rows.append(dict(seed=seed,day=obs['day']+1,prices=obs['market']['prices'],shops=obs['town']['unlocked_shops'],options=getattr(agent.core,'portfolio_latest',{})))
        assert agent.core.error_count==0
    out=BASE/'reports/e20_2_confirmation/CROP_OPTIONS.json';out.write_text(json.dumps(dict(action_parity_per_seed=600,rows=rows),indent=2)+'\n',encoding='utf-8')
    for v in rows:print(v['seed'],v['day'],{k:round(x['total']) for k,x in v['options'].items()},flush=True)
if __name__=='__main__':main()
