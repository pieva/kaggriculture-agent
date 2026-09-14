"""Reproduce frozen episodes with recorded opponent commands; not a rating test."""
import argparse
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
OUT = ROOT / 'docs/model_specs/codex/e22/reports/e22_2_fix_v1'
ART = ROOT / 'docs/model_specs/codex/e22/artifacts/e22_2_fix_v1'
BASE = ROOT / 'submission/submission_codex_e22_2_pascoli.py'
FIX = ROOT / 'submission/submission_codex_e22_2_fix_v1.py'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--recorded-baseline', action='store_true', help='Reuse the already audited published replay instead of rerunning its frozen policy.')
    args = parser.parse_args()
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    from docs.model_specs.codex.e22.tools.analyze_external_20260914 import enrich
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    assert hashlib.sha256(BASE.read_bytes()).hexdigest() == 'df6991a5619f09e91bef6b6ac7034ade10f87c59e577d49c19cf197cd5cd2dcd'
    policies = {arm: get_last_callable(path.read_text()) for arm, path in [('published', BASE), ('fix', FIX)]}
    assert all(p.__name__ == 'agent' for p in policies.values())
    hashes = {arm: hashlib.sha256(path.read_bytes()).hexdigest() for arm, path in [('published', BASE), ('fix', FIX)]}
    cohort = json.loads((OUT.parent / 'external_e22_2_20260914/COHORT.json').read_text())
    selected = [g for g in cohort if g['submission'] == 56212495 and (args.all or g['episode'] in (108729054, 108777186, 108691652, 108751380))]
    rows = []
    for g in selected:
        raw = (ROOT / g['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == g['sha256']
        replay = json.loads(raw)
        seat = g['seat']
        commands = [s[1-seat]['action'] for s in replay['steps'][1:]]
        def recorded(obs, cfg):
            return commands[int(obs['day']) * 24 + int(obs['hour'])]
        for arm, path in [('published', BASE), ('fix', FIX)]:
            dest = OUT / f"{g['episode']}_{arm}.json"
            if dest.exists():
                row = json.loads(dest.read_text())
                require_rerun = arm == 'published' and not args.recorded_baseline and row.get('source') == 'recorded and previously audited'
                if row['hash'] == hashes[arm] and not require_rerun:
                    rows.append(row)
                    continue
            reuse = arm == 'published' and args.recorded_baseline
            if reuse:
                game = replay
            else:
                cfg = dict(replay['configuration'], seed=replay['info']['seed'])
                env = make('kaggriculture', configuration=cfg, debug=False)
                agents = [recorded, recorded]
                agents[seat] = str(path)
                env.run(agents)
                game = env.toJSON()
            assert len(game['steps']) == 720 and all(s['status'] == 'DONE' for s in game['steps'][-1])
            if arm == 'published' and not reuse:
                assert game['rewards'] == replay['rewards'], (g['episode'], game['rewards'], replay['rewards'])
                assert all(game['steps'][i+1][seat]['action'] == replay['steps'][i+1][seat]['action'] for i in range(719))
            for i, step in enumerate(game['steps']):
                step[0]['observation']['step'] = i
            if reuse:
                p = json.loads((OUT.parent / 'external_e22_2_20260914/profiles' / f"56212495_{g['episode']}.json").read_text())['own']
            else:
                p = enrich(game, seat, policies[arm])
            assert not p['policy_differences']
            final = game['steps'][-1][seat]['observation']
            mix = Counter(t['animal'] for r in final['farms'][seat]['tiles'] for t in r if isinstance(t, dict) and t.get('animal'))
            products = ('MILK', 'WOOL', 'EGG')
            residual = {item: final['private']['shed'].get(item, 0) + sum(inv.get(item, 0) for inv in final['private']['inventories']) for item in products}
            lost = {item: p['totals']['harvested'].get(item, 0) - p['totals']['sold_units'].get(item, 0) - residual[item] for item in products}
            missing = []
            for i, step in enumerate(game['steps'][:-1]):
                f = step[seat]['observation']['farms'][seat]
                count = len(game['steps'][i+1][seat]['action'].get('hands', []))
                if count > len(f['hands']):
                    missing.append(i)
            row = dict(episode=g['episode'], seat=seat, arm=arm, hash=hashes[arm], rewards=game['rewards'], mix=dict(mix), escaped=len(p['ledger']['animal_escapes']), unfed=len(p['unfed']), failed=dict(Counter(a['command'][0] for a in p['failed_actions'])), missing_workers=missing, animal_product_lost=lost, residual=residual, terminal=p['terminal'], totals=p['totals'])
            row['source'] = 'recorded and previously audited' if reuse else 'local engine replay'
            assert hashlib.sha256(path.read_bytes()).hexdigest() == hashes[arm]
            dest.write_text(json.dumps(row, indent=2))
            with gzip.open(ART / f"{g['episode']}_{arm}.replay.json.gz", 'wt', encoding='utf-8') as f:
                json.dump(game, f, separators=(',', ':'))
            with gzip.open(ART / f"{g['episode']}_{arm}.profile.json.gz", 'wt', encoding='utf-8') as f:
                json.dump(p, f, separators=(',', ':'))
            rows.append(row)
            print('RESULT', g['episode'], arm, game['rewards'], dict(mix), 'lost', lost, 'unfed', row['unfed'], 'failed', row['failed'], flush=True)
    (OUT / 'RESULTS.json').write_text(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
