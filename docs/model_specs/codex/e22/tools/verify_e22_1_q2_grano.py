"""Real-file-loader regression of frozen E22.1 wheat variant, then direct matches."""
import contextlib
import gzip
import hashlib
import io
import json
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e22/reports/e22_1_q2_grano_v1'
ART=ROOT/'docs/model_specs/codex/e22/artifacts/e22_1_q2_grano_v1'
SOURCE=OUT.parent/'external_e22_2_20260914'
BASE=ROOT/'submission/submission_codex_e22_1_pollai.py'
CAND=ROOT/'submission/submission_codex_e22_1_q2_grano_v1.py'


def savegz(path,data):
    with gzip.open(path,'wt',encoding='utf-8') as f:json.dump(data,f,separators=(',',':'))


def main():
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
        from docs.model_specs.codex.e22.tools.analyze_external_20260914 import enrich
    ART.mkdir(parents=True,exist_ok=True)
    sha=hashlib.sha256(CAND.read_bytes()).hexdigest()
    assert sha==json.loads((OUT/'BUILD.json').read_text())['sha256']
    cand=get_last_callable(CAND.read_text());base=get_last_callable(BASE.read_text())
    assert cand.__name__==base.__name__=='agent'
    cohort=[g for g in json.loads((SOURCE/'COHORT.json').read_text()) if g['submission']==56206528]
    expected=json.loads((OUT.parent/'e22_1_q2_coop_20260914/CROP_COUNTERFACTUALS.json').read_text())
    protocol=dict(candidate_sha256=sha,baseline_submission=56206528,diagnostic_episodes=[g['episode'] for g in cohort],direct_seeds=list(range(180911301,180911308)),seats=[0,1],reserved_seeds_used=[],method='20 actual candidate file-loader games against recorded opponents; 14 direct real-policy games. No rating inference.')
    (OUT/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2))
    rows=[]
    for g in cohort:
        dest=OUT/f"diagnostic_{g['episode']}.json"
        if dest.exists():
            row=json.loads(dest.read_text());assert row['sha256']==sha;rows.append(row);continue
        raw=(ROOT/g['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256']
        replay=json.loads(raw);seat=g['seat']
        def recorded(obs,cfg):return replay['steps'][int(obs['day'])*24+int(obs['hour'])+1][1-seat]['action']
        env=make('kaggriculture',configuration=dict(replay['configuration'],seed=replay['info']['seed']),debug=False)
        agents=[recorded,recorded];agents[seat]=str(CAND);env.run(agents);game=env.toJSON()
        assert len(game['steps'])==720 and all(s['status']=='DONE' for s in game['steps'][-1])
        for i,step in enumerate(game['steps']):step[0]['observation']['step']=i
        p=enrich(game,seat,cand)
        b=json.loads((SOURCE/'profiles'/f"56206528_{g['episode']}.json").read_text())['own']
        prior=next(r for r in expected if r['episode']==g['episode'])['arms'][1]
        assert game['rewards'][seat]==prior['cash']
        assert game['rewards'][1-seat]==prior['opponent_cash']
        assert not p['policy_differences'] and p['ledger']['cash_parity_errors']==0
        assert p['totals']['harvested'].get('WHEAT',0)==b['totals']['harvested'].get('WHEAT',0)+2
        assert p['totals']['sold_units'].get('WHEAT',0)==b['totals']['sold_units'].get('WHEAT',0)+2
        assert len(p['ledger']['animal_escapes'])==len(b['ledger']['animal_escapes'])
        assert game['steps'][-1][seat]['observation']['private']==prior['final_private']
        row=dict(kind='diagnostic',episode=g['episode'],seat=seat,sha256=sha,rewards=game['rewards'],cash_delta=prior['cash_delta'],escaped=len(p['ledger']['animal_escapes']),cash_errors=0,policy_differences=0,target_extra_wheat=2)
        dest.write_text(json.dumps(row,indent=2));savegz(ART/f"diagnostic_{g['episode']}.profile.json.gz",p)
        savegz(ART/f"diagnostic_{g['episode']}.replay.json.gz",game)
        rows.append(row);print('DIAGNOSTIC',g['episode'],row['cash_delta'],flush=True)
    for seed in range(180911301,180911308):
        for seat in (0,1):
            dest=OUT/f'direct_{seed}_{seat}.json'
            if dest.exists():
                row=json.loads(dest.read_text());assert row['sha256']==sha;rows.append(row);continue
            env=make('kaggriculture',configuration=dict(seed=seed,episodeSteps=720,turnsPerDay=24),debug=False)
            agents=[str(BASE),str(BASE)];agents[seat]=str(CAND);env.run(agents);game=env.toJSON()
            assert len(game['steps'])==720 and all(s['status']=='DONE' for s in game['steps'][-1])
            for i,step in enumerate(game['steps']):step[0]['observation']['step']=i
            ps=[enrich(game,j,cand if j==seat else base) for j in range(2)]
            assert all(not p['policy_differences'] and p['ledger']['cash_parity_errors']==0 for p in ps)
            f=game['steps'][-1][seat]['observation']['farms'][seat]
            mix=dict(Counter(t['animal'] for line in f['tiles'] for t in line if isinstance(t,dict) and t.get('animal')))
            target=[e for e in ps[seat]['harvest_events'] if e['x']==3 and e['y']==7 and e['day']==30]
            assert len(target)==1 and target[0]['gain']=={'WHEAT':2}
            assert mix=={'COW':8,'SHEEP':6,'GOOSE':3} and not ps[seat]['ledger']['animal_escapes']
            row=dict(kind='direct',seed=seed,seat=seat,sha256=sha,rewards=game['rewards'],margin=game['rewards'][seat]-game['rewards'][1-seat],mix=mix,cash_errors=0,policy_differences=0,target_extra_wheat=2)
            dest.write_text(json.dumps(row,indent=2));savegz(ART/f'direct_{seed}_{seat}.profiles.json.gz',ps)
            savegz(ART/f'direct_{seed}_{seat}.replay.json.gz',game)
            rows.append(row);print('DIRECT',seed,seat,row['margin'],flush=True)
    assert len(rows)==34
    assert hashlib.sha256(CAND.read_bytes()).hexdigest()==sha
    (OUT/'RESULTS.json').write_text(json.dumps(rows,indent=2))


if __name__=='__main__':main()
