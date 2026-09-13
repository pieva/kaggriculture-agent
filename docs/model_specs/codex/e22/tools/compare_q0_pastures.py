"""Serial paired engine runs, real file loader, and cash-verified daily KPI."""
import argparse
import contextlib
import gzip
import hashlib
import io
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
BASE = ROOT / 'submission/submission_codex_e22_s56165462_observed_v1.py'
CAND = ROOT / 'submission/submission_codex_e22_q0_8c9s_internal_v1.py'
OUT = ROOT / 'docs/model_specs/codex/e22/reports/q0_8c9s_v1'
ART = ROOT / 'docs/model_specs/codex/e22/artifacts/q0_8c9s_v1'
INTERVENTION = 'Three Q0 pastures; 3 geese replaced by sheep; state-aware service and wool sales. Other routes, cow/sheep placements, grain orders, hires and crops retain E22 calendar.'
CANDIDATE_CHECKS = None

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def snapshots(game, seat):
    result = []
    for day in range(1, 31):
        obs = game['steps'][day * 24 - 1][seat]['observation']
        farm, private = obs['farms'][seat], obs['private']
        animals = Counter(t['animal'] for row in farm['tiles'] for t in row
                          if isinstance(t, dict) and t.get('animal'))
        carried = Counter()
        for inv in private['inventories']: carried.update(inv)
        result.append(dict(day=day, cash=farm['money'], animals=dict(animals),
                           shed=private['shed'], carried=dict(carried)))
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['exposed', 'confirmation'], default='exposed')
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); ART.mkdir(parents=True, exist_ok=True)
    hashes = {'baseline': digest(BASE), 'candidate': digest(CAND)}
    protocol = dict(hashes=hashes, control_submission=56206528, arm='8C9S',
                    exposed_seeds=list(range(180911301, 180911308)),
                    confirmation_seeds=list(range(180912401, 180912408)), seats=[0, 1],
                    method='Direct paired head-to-head; serial simulations; actual file loader; shared endogenous market.',
                    intervention=INTERVENTION,
                    limits='Not a 6C10S replica or a pasture-only causal estimate; no rating estimate; no publication.')
    protocol_path = OUT / 'PROTOCOL.json'
    if protocol_path.exists(): assert json.loads(protocol_path.read_text()) == protocol
    else: protocol_path.write_text(json.dumps(protocol, indent=2), encoding='utf-8')
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
        from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit, end_state
    assert get_last_callable(CAND.read_text(encoding='utf-8')).__name__ == 'agent'
    assert get_last_callable(BASE.read_text(encoding='utf-8')).__name__ == 'agent'
    pairs = [(s, seat) for s in protocol[args.phase + '_seeds'] for seat in (0, 1)]
    if args.limit: pairs = pairs[:args.limit]
    for seed, seat in pairs:
        path = ART / f'{seed}_{seat}.json'
        if path.exists():
            assert json.loads(path.read_text())['hashes'] == hashes
            continue
        agents = [str(BASE), str(BASE)]; agents[seat] = str(CAND)
        env = make('kaggriculture', configuration=dict(seed=seed, episodeSteps=720, turnsPerDay=24), debug=False)
        env.run(agents); game = env.toJSON()
        assert len(game['steps']) == 720 and all(s['status'] == 'DONE' for s in game['steps'][-1])
        ledgers = [audit(game, s) for s in (0, 1)]
        daily = [snapshots(game, s) for s in (0, 1)]
        final = game['steps'][-1][seat]['observation']['farms'][seat]
        targets = [final['tiles'][y][x] for x, y in [(4, 1), (3, 2), (2, 3)]]
        checks = dict(targets=targets, mix=daily[seat][-1]['animals'],
                      escapes=len(ledgers[seat]['animal_escapes']),
                      min_cash=min(st[seat]['observation']['farms'][seat]['money'] for st in game['steps']),
                      baseline_plan_parity=0)
        ns = {}; exec(BASE.read_text(encoding='utf-8'), ns)
        checks['baseline_plan_parity'] = sum(game['steps'][i+1][1-seat]['action'] == ns['_PLAN'][i] for i in range(719))
        assert checks['baseline_plan_parity'] == 719
        row = dict(seed=seed, seat=seat, phase=args.phase, hashes=hashes,
                   rewards=game['rewards'], margin=game['rewards'][seat]-game['rewards'][1-seat],
                   ledgers=ledgers, daily=daily, terminal=[end_state(game, s) for s in (0, 1)], checks=checks)
        if CANDIDATE_CHECKS is not None:
            row['calendar_checks'] = CANDIDATE_CHECKS(game, seat)
        with gzip.open(path.with_suffix('.replay.json.gz'), 'wt', encoding='utf-8') as f:
            json.dump(game, f, separators=(',', ':'))
        path.write_text(json.dumps(row, separators=(',', ':')), encoding='utf-8')
        print('RESULT', seed, seat, row['rewards'], row['margin'], checks['mix'], 'escapes', checks['escapes'], flush=True)
        assert all(t.get('kind') == 'PASTURE' and t.get('animal') == 'SHEEP' for t in targets), checks
        assert checks['mix'] == {'COW': 8, 'SHEEP': 9} and checks['escapes'] == 0, checks
        assert hashes == {'baseline': digest(BASE), 'candidate': digest(CAND)}
    rows = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(ART.glob('*.json'))]
    (OUT / 'RESULTS.json').write_text(json.dumps(rows, separators=(',', ':')), encoding='utf-8')

if __name__ == '__main__': main()
