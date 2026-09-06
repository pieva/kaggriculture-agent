"""Internal-only E18.31 diagnostic/ablation gate. No public reference is loaded."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path

from docs.model_specs.codex.e18.tools import run_e18_30_mission_gate as gate


def traced(base):
    class Traced(base):
        instance = None

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            Traced.instance = self
            self.focus_trace = []
            self.deadline_trace = []
            self.towns = []
            self.market_focus = []
            self.pass_reasons = [Counter() for _ in range(30)]

        def __call__(self, obs, config=None):
            day, hour = obs['day'] + 1, obs['hour'] + 1
            farm, private = obs['farms'][self.seat], obs['private']
            action = super().__call__(obs, config)
            if hour==1:
                self.towns.append(deepcopy(obs.get('town',{})))
            if 12<=day<=14:
                self.market_focus.append(dict(day=day,hour=hour,money=farm['money'],
                    shed=deepcopy(private['shed']),orders=deepcopy(action['market']),
                    pending_pickup=dict(self._pending_requirements(day,'pickup')),
                    commands=deepcopy(action)))
            if hour >= 20:
                risks = []
                for y,row in enumerate(farm['tiles']):
                    for x,tile in enumerate(row):
                        if isinstance(tile,dict) and tile.get('kind')=='PLANT' and not tile.get('watered_today') and tile.get('consecutive_unwatered',0)>=1:
                            risks.append(dict(position=[x,y],tile=deepcopy(tile)))
                if risks:
                    self.deadline_trace.append(dict(day=day,hour=hour,risks=risks,
                        commands=deepcopy(action),positions=[farm['farmer'],*farm['hands']],
                        remaining={str(w):deepcopy(self._remaining_rows(day,w)) for w in range(len(farm['hands'])+1)},
                        active=deepcopy(list(self.active.values()))))
            waits = []
            for worker, command in enumerate([action['farmer'], *action['hands']]):
                if command[0] != 'PASS':
                    continue
                remaining = self._remaining_rows(day, worker)
                reason = ('queue_exhausted' if not remaining else
                          'scheduled_wait' if remaining[0]['turn'] > hour else
                          'blocked_' + remaining[0]['opcode'])
                self.pass_reasons[day - 1][reason] += 1
                if 5 <= day <= 10:
                    waits.append(dict(worker=worker, reason=reason,
                        position=self._position(farm, worker),
                        inventory=dict(self._inventory(private, worker)),
                        next=deepcopy(remaining[0]) if remaining else None))
            if 5 <= day <= 10:
                placed = Counter(t['animal'] for row in farm['tiles'] for t in row
                                 if isinstance(t, dict) and t.get('animal'))
                self.focus_trace.append(dict(day=day, hour=hour,
                    money=farm['money'], hands=len(farm['hands']),
                    planned_hands=self.daily_hands[day],
                    unlocked=farm['unlocked_quadrants'],
                    placed=dict(placed), shed=deepcopy(private['shed']),
                    seeds=deepcopy(private['seeds']), action=deepcopy(action),
                    passes=waits))
            return action
    return Traced


def run_case(variant, opponent, seed, seat):
    original = gate.MissionRuntimeController
    if variant == 'BASELINE':
        base = original
    elif variant == 'OBLIGATION':
        from docs.model_specs.codex.e18.tools.e18_31_obligation_controller import ObligationController
        base = ObligationController
    elif variant == 'UNIFIED':
        from docs.model_specs.codex.e18.tools.e18_31_unified_investment_controller import UnifiedInvestmentController
        base = UnifiedInvestmentController
    else:
        from docs.model_specs.codex.e18.tools.e18_31_assignment_controller import AssignmentController
        base = AssignmentController
    cls = traced(base)
    def factory(plan, seat, unused):
        return cls(plan, seat, 'CROP_POOL' if variant == 'BASELINE' else variant)
    gate.MissionRuntimeController = factory
    try:
        result = gate.run_one('CROP_POOL', opponent, seed, seat)
        agent = cls.instance
        result.update(variant=variant, version='E18.30 V2' if variant == 'BASELINE' else 'E18.31 '+variant,
                      focus_trace=agent.focus_trace,
                      deadline_trace=agent.deadline_trace,
                      towns=agent.towns, market_focus=agent.market_focus,
                      pass_reasons=[dict(c) for c in agent.pass_reasons],
                      assignment_metrics=dict(getattr(agent, 'assignment_metrics', {})),
                      expansion_log=getattr(agent, 'expansion_log', []))
        return result
    finally:
        gate.MissionRuntimeController = original


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--variants', nargs='+', default=['BASELINE'])
    parser.add_argument('--opponents', nargs='+', default=['E18.16'])
    parser.add_argument('--seeds', nargs='+', type=int, default=[180903001])
    parser.add_argument('--seats', nargs='+', type=int, default=[0, 1])
    parser.add_argument('--jobs', type=int, default=2, choices=[1, 2])
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    assert set(args.seeds) <= set(range(180903001, 180903008))
    assert args.label.replace('_', '').isalnum()
    output = gate.DERIVED / f'E18_31_ASSIGNMENT_GATE_{args.label}.json'
    assert not output.exists(), output
    sources = [Path(__file__), Path(gate.__file__), Path(__file__).with_name('e18_30_mission_runtime.py')]
    candidate = Path(__file__).with_name('e18_31_assignment_controller.py')
    if candidate.exists():
        sources.append(candidate)
    if 'OBLIGATION' in args.variants:
        sources.append(Path(__file__).with_name('e18_31_obligation_controller.py'))
    if 'UNIFIED' in args.variants:
        sources.extend([Path(__file__).with_name('e18_31_obligation_controller.py'),
                        Path(__file__).with_name('e18_31_unified_investment_controller.py')])
    payload = dict(complete=False, holdout_consumed=False, matches=[], failures=[],
                   source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
    cases = [(v,o,s,p) for v in args.variants for o in args.opponents for s in args.seeds for p in args.seats]
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        pending = {pool.submit(run_case, *c): c for c in cases}
        for future in as_completed(pending):
            try:
                payload['matches'].append(future.result())
            except Exception as exc:
                payload['failures'].append(dict(case=pending[future], error=repr(exc)))
                print(repr(exc), flush=True)
            output.write_text(json.dumps(payload, indent=2)+'\n', encoding='utf-8')
    payload['complete'] = not payload['failures'] and len(payload['matches']) == len(cases)
    output.write_text(json.dumps(payload, indent=2)+'\n', encoding='utf-8')
    print(output, flush=True)
    if not payload['complete']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
