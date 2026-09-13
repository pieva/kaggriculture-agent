"""Verify full-run invariants and deterministic replay parity of the real loader."""
import contextlib
import copy
import gzip
import io
import json
import subprocess
from compare_q0_pastures import ROOT, BASE, CAND, ART, OUT, digest

def main():
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
    rows = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(ART.glob('*.json'))]
    assert {(r['seed'], r['seat']) for r in rows} == {(s, p) for s in range(180911301, 180911308) for p in (0, 1)}
    assert subprocess.check_output(['git', 'diff', '--', str(BASE)], cwd=ROOT) == b''
    for r in rows:
        s = r['seat']
        assert r['checks']['mix'] == {'COW': 8, 'SHEEP': 9}
        assert r['checks']['escapes'] == 0 and r['checks']['baseline_plan_parity'] == 719
        assert r['hashes'] == dict(baseline=digest(BASE), candidate=digest(CAND))
        assert all(l['cash_parity_errors'] == 0 for l in r['ledgers'])
        days = r['ledgers'][s]['daily']
        # Wool sale quantities are widened globally; their lockstep pricing
        # can differ before D11 even when worker actions are still identical.
        buys = lambda item: sum(d['bought_units'].get('BUY_ANIMAL:'+item, 0) for d in days)
        assert (buys('COW'), buys('SHEEP'), buys('GOOSE')) == (8, 9, 0)
        for item in ('MILK', 'WOOL', 'EGG'):
            assert sum(d['harvested'].get(item,0) for d in days) == sum(d['sold_units'].get(item,0) for d in days)
            assert all(r['terminal'][s][k].get(item,0) == 0 for k in ('shed','carried','tile_yield_units'))
    game = json.load(gzip.open(ART / '180911301_0.replay.json.gz', 'rt', encoding='utf-8'))
    candidate = get_last_callable(CAND.read_text(encoding='utf-8'))
    control = get_last_callable(BASE.read_text(encoding='utf-8'))
    for i in range(719):
        obs = game['steps'][i][0]['observation']
        before = copy.deepcopy(obs)
        action = candidate(obs, game['configuration'])
        assert action == game['steps'][i+1][0]['action']
        assert action == candidate(obs, game['configuration']) and obs == before
        if i < 240:
            old = control(obs, game['configuration'])
            assert (action['farmer'], action['hands']) == (old['farmer'], old['hands'])
    terminal_action = candidate(dict(day=30,hour=0), {})
    assert terminal_action == {'farmer':['PASS'],'hands':[],'market':[]}
    verification = dict(games=len(rows), seeds=7, roles=2, real_loader='agent',
        replay_action_parity=719, repeated_call_parity=719, observation_mutations=0,
        unchanged_first_ten_days_worker_batches=240, baseline_unchanged=True,
        early_market_scope='Wool SELL limits change before D11 too; no claim of identical early cash or market actions.',
        day10_cash_deltas=[dict(seed=r['seed'],seat=r['seat'],delta=r['daily'][r['seat']][9]['cash']-r['daily'][1-r['seat']][9]['cash']) for r in rows],
        accounting_side_transitions=len(rows)*2*719, cash_errors=0, candidate_escapes=0,
        all_animal_output_sold=True, confirmation_seeds_used=False,
        residual='Two carried fertilizer units in candidate terminal states; no residual milk, wool or eggs.',
        hashes=dict(baseline=digest(BASE),candidate=digest(CAND)))
    (OUT/'VERIFICATION.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
    print(json.dumps(verification),flush=True)

if __name__ == '__main__': main()
