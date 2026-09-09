"""Read-only decision telemetry: wraps actual calls, never re-runs the planner."""
from collections import Counter
from copy import deepcopy


def closure(function):
    return dict(zip(function.__code__.co_freevars,
                    (c.cell_contents for c in (function.__closure__ or ()))))


class Diagnostic:
    def __init__(self, policy):
        self.policy = policy
        self.rows = []
        self.attempts = []
        self.offers = []
        core = policy.core
        prepare, services, certificate = core._prepare_steps, core._services, core._day_route_certificate
        self.route_prepare = prepare

        def observed_prepare(worker, target, commands, **kwargs):
            steps = prepare(worker, target, commands, **kwargs)
            state = closure(prepare)
            queues = state.get('queues', {})
            owners = [w for w, q in queues.items() if tuple(target) in q]
            self.attempts.append(dict(worker=worker, target=target, commands=deepcopy(commands),
                accepted=steps is not None, steps=None if steps is None else len(steps),
                owners=owners, queue=deepcopy(queues.get(worker, []))))
            return steps

        def observed_services():
            result = services()
            self.offers = deepcopy(result)
            return result

        def observed_certificate(worker, job, offers=None):
            ok = certificate(worker, job, offers)
            self.attempts.append(dict(worker=worker,target=job['target'],
                certificate=ok,kind=job['kind']))
            return ok

        core._prepare_steps = observed_prepare
        core._services = observed_services
        core._day_route_certificate = observed_certificate

    def __call__(self, obs, cfg):
        self.attempts, self.offers = [], []
        action = self.policy(obs, cfg)
        core = self.policy.core
        farm = obs['farms'][obs['player']]
        positions = [farm['farmer'], *farm['hands']]
        commands = [action['farmer'], *action['hands']]
        for worker, pos in enumerate(positions):
            if worker >= len(commands) or commands[worker] != ['PASS']:
                continue
            opening = obs['day'] < self.policy.assisted_days
            job = None if opening else core.active.get(worker)
            attempts = [r for r in self.attempts if r['worker'] == worker]
            if opening:
                reason = 'opening_teacher_or_governor'
            elif job:
                reason = 'waiting_observed_input'
            elif any(r.get('certificate') is False for r in attempts):
                reason = 'admission_certificate_rejection'
            elif any(r.get('accepted') is False and r.get('owners') for r in attempts):
                reason = 'reservation_rejection_present_not_proven_causal'
            elif attempts:
                reason = 'prepare_rejection_resources_time_or_policy'
            else:
                reason = 'no_offer_unknown_useful_work'
            self.rows.append(dict(day=obs['day']+1,hour=obs['hour']+1,worker=worker,
                position=pos,remaining=min(cfg.get('turnsPerDay',24)-obs['hour'],
                    cfg.get('episodeSteps',720)-1-obs['day']*cfg.get('turnsPerDay',24)-obs['hour']),
                reason=reason,inventory=obs['private']['inventories'][worker],
                job=deepcopy(job),active={} if opening else deepcopy(core.active),
                offers=self.offers,attempts=attempts,
                route_state={} if opening else deepcopy(core.daily_route_state)))
        return action


def summary(rows):
    return dict(total=len(rows),causes=dict(Counter(r['reason'] for r in rows)),
        daily=[dict(day=d,total=sum(r['day']==d for r in rows),
                    causes=dict(Counter(r['reason'] for r in rows if r['day']==d)),
                    workers=dict(Counter(str(r['worker']) for r in rows if r['day']==d)))
               for d in range(1,31)])


def main():
    import argparse, gzip, hashlib, json, runpy
    from pathlib import Path
    parser=argparse.ArgumentParser()
    parser.add_argument('--episode',type=int,default=106843637)
    parser.add_argument('--original',type=Path,default=Path('C:/Users/pietr/Projects/kaggriculture-agent'))
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[5]
    base=root/'docs/model_specs/codex/e19'
    cohort=json.loads((base/'reports/v48_external_pass_update_20260908/cohort.json').read_text())
    entry=next(g for g in cohort['games'] if g['episode']==args.episode)
    path=root/entry['raw_path']
    if not path.exists(): path=args.original/entry['raw_path']
    raw=path.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==entry['sha256']
    replay=json.loads(raw); seat=entry['seat']
    policy=runpy.run_path(str(root/'submission/submission_codex_e18_770_v48_external.py'))['create_agent']({'player_position':seat})
    instrument=Diagnostic(policy)
    mismatches=[]
    for i in range(1,len(replay['steps'])):
        obs=deepcopy(replay['steps'][i-1][seat]['observation'])
        obs['player']=seat
        obs['step']=i-1
        got=instrument(obs,replay['configuration'])
        if got!=replay['steps'][i][seat]['action']: mismatches.append(i)
    out=base/'reports/pass_reduction_v49_20260909'
    out.mkdir(parents=True,exist_ok=True)
    detail=root/'scratch/v49'/f'diagnostic_{args.episode}.json.gz'
    detail.parent.mkdir(parents=True,exist_ok=True)
    with gzip.open(detail,'wt',encoding='utf-8') as f:json.dump(instrument.rows,f)
    result=dict(episode=args.episode,replay_sha256=entry['sha256'],calls=719,
        mismatches=mismatches,detail=str(detail.relative_to(root)),**summary(instrument.rows))
    (out/f'diagnostic_{args.episode}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:result[k] for k in ['episode','calls','mismatches','total','causes']}),flush=True)


if __name__=='__main__':main()
