"""Parity of a frozen common-core candidate, including the actual file loader."""
import argparse
import hashlib
import importlib
import json
import runpy
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


def verify_case(case):
    bundle, profile, seed, seat = case
    from kaggle_environments import make
    from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController
    from docs.model_specs.codex.e18.tools.run_e18_30_mission_gate import opponent_policy
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    module = runpy.run_path(bundle)
    source = CommonController(json.loads(Path(profile).read_text()), engine.market_price, engine.MARKET_PARAMS, seat)
    actions, timings = [], []
    def checked(obs, cfg):
        expected = source(obs, cfg)
        start = time.perf_counter()
        actual = module['agent'](obs, cfg)
        timings.append(time.perf_counter()-start)
        assert expected == actual, (seed, seat, obs.get('step'), 'action mismatch')
        actions.append(actual)
        return actual
    cfg = dict(seed=seed, episodeSteps=720, turnsPerDay=24)
    env = make('kaggriculture', configuration=cfg, debug=False)
    other = opponent_policy('E18.16', seed, 1-seat)
    env.run([checked,other] if seat == 0 else [other,checked])
    assert len(actions) == 719 and all(s.status == 'DONE' for s in env.state)
    terminal = env.steps[-1][seat].observation
    for policy in (source, module['_ACTIVE'][seat][1]):
        policy.acknowledge_terminal(terminal)
        assert policy.error_count == 0
    file_env = make('kaggriculture', configuration=cfg, debug=False)
    other = opponent_policy('E18.16', seed, 1-seat)
    file_env.run([bundle,other] if seat == 0 else [other,bundle])
    assert [step[seat].action for step in file_env.steps[1:]] == actions
    assert all(s.status == 'DONE' for s in file_env.state)
    assert file_env.state[seat].reward == env.state[seat].reward
    result = dict(seed=seed, seat=seat, identical_actions=len(actions),
        kaggle_file_loader_parity=True, reward=env.state[seat].reward,
        incomplete_missions=source.incomplete_missions,
        max_call_seconds=max(timings), mean_call_seconds=sum(timings)/len(timings))
    print(json.dumps(result), flush=True)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--profile', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--seeds', type=int, nargs='+', default=[180903001,180903005])
    p.add_argument('--seats', type=int, nargs='+', default=[0,1])
    args = p.parse_args()
    assert not args.output.exists()
    manifest = json.loads(args.bundle.with_suffix('.manifest.json').read_text())
    for path, digest in manifest['sources'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
    assert hashlib.sha256(args.bundle.read_bytes()).hexdigest() == manifest['submission_sha256']
    assert json.loads(args.profile.read_text()) == manifest['profile']
    report = dict(passed=False, matches=[], failures=[], submission_sha256=manifest['submission_sha256'],
                  holdout_consumed=False, uploaded=False)
    cases = [(str(args.bundle.resolve()),str(args.profile.resolve()),seed,seat) for seed in args.seeds for seat in args.seats]
    with ProcessPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(verify_case,c): c for c in cases}
        for f in as_completed(futures):
            try: report['matches'].append(f.result())
            except Exception as exc: report['failures'].append(dict(case=futures[f],error=repr(exc)))
            args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    report['passed'] = not report['failures'] and len(report['matches']) == len(cases)
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if not report['passed']: raise SystemExit(1)


if __name__ == '__main__': main()
