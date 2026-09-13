"""E22 diagnosis: frozen replay suffix, fixed opponent, isolated closure probes."""
import copy
import hashlib
import importlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace as NS

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
SOURCE = ROOT / 'data/replays/json/e22_closure_20260913/108491899.json'
OUT = ROOT / 'docs/model_specs/codex/e22/reports/closure_108491899'


def run():
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    from docs.model_specs.codex.e20.tools.operational_calendar_v44 import Agent
    raw = SOURCE.read_bytes()
    replay = json.loads(raw)
    policy = Agent({'player_position': 1})
    worker_matches = 0
    market_differences = []
    for i in range(719):
        actual = policy(copy.deepcopy(replay['steps'][i][1]['observation']), replay['configuration'])
        expected = replay['steps'][i + 1][1]['action']
        assert actual['farmer'] == expected['farmer'] and actual['hands'] == expected['hands'], i
        worker_matches += 1
        if actual['market'] != expected['market']:
            market_differences.append(i)
    results = []
    for mode in ('control', 'tomatoes', 'wheat', 'last_delivery', 'combined'):
        initial = replay['steps'][708]
        farms = copy.deepcopy(initial[0]['observation']['farms'])
        market = copy.deepcopy(initial[0]['observation']['market'])
        states = [NS(observation=NS(farms=farms, market=market,
                    town=copy.deepcopy(initial[0]['observation']['town']),
                    private=copy.deepcopy(initial[s]['observation']['private']))) for s in range(2)]
        env = NS(configuration=NS(**replay['configuration']))
        jobs = {9: (3, 7), 10: (4, 8)}
        phase = {w: 'harvest' for w in jobs}
        changes = []
        checked = 0
        for i in range(708, 719):
            hour = i % 24 + 1
            for s in range(2):
                states[s].action = copy.deepcopy(replay['steps'][i + 1][s]['action'])
            own = states[1].action
            if mode in ('tomatoes', 'combined'):
                for w, target in jobs.items():
                    pos = tuple(engine._farmer_position(farms[1], w))
                    if phase[w] == 'harvest':
                        cmd = policy.move(pos, target) or ['HARVEST']
                        if cmd == ['HARVEST']:
                            phase[w] = 'deliver'
                    elif phase[w] == 'deliver':
                        shed = min(((4, 4), (5, 4), (4, 5), (5, 5)), key=lambda p: abs(p[0]-pos[0])+abs(p[1]-pos[1]))
                        cmd = policy.move(pos, shed) or ['DROP']
                        if cmd == ['DROP']:
                            phase[w] = 'done'
                    else:
                        cmd = ['PASS']
                    assert own['hands'][w-1] == ['PASS'], (i, w)
                    own['hands'][w-1] = cmd
                    changes.append(dict(hour=hour, worker=w, action=cmd))
                n = states[1].observation.private['shed'].get('TOMATO', 0)
                if n and not any(o[:2] == ['SELL', 'TOMATO'] for o in own['market']):
                    own['market'].append(['SELL', 'TOMATO', n])
            if mode in ('wheat', 'combined') and hour == 18:
                assert engine._farmer_position(farms[1], 4) == [2, 5]
                assert own['hands'][3] == ['WATER']
                own['hands'][3] = ['HARVEST']
            for s, state in enumerate(states):
                commands = [state.action['farmer'], *state.action['hands']]
                assert not any(c[0] == 'PLANT' for c in commands)
                for w, cmd in enumerate(commands):
                    engine._apply_unit_action(farms[s], state.observation.private, w, cmd, 10, 29, 24, 100)
            # Ex-post feasibility probe: final sale includes deterministic current-turn deliveries.
            # This is not a submitted policy or a claim of live opponent response.
            if i == 718 and mode in ('wheat', 'last_delivery', 'combined'):
                items = ('WHEAT',) if mode == 'wheat' else ('WHEAT', 'WOOL')
                for item in items:
                    n = states[1].observation.private['shed'].get(item, 0)
                    existing = next((o for o in own['market'] if o[:2] == ['SELL', item]), None)
                    if existing is not None:
                        existing[2] = n
                    elif n:
                        own['market'].append(['SELL', item, n])
            assert all(len(s.action['market']) <= 10 for s in states)
            engine._process_market(states, env)
            engine._town_consume(env, states, i)
            for farm in farms:
                engine._decay_plants(farm, i)
            if mode == 'control':
                expected = replay['steps'][i+1]
                assert farms == expected[0]['observation']['farms'], ('farms', i)
                assert market == expected[0]['observation']['market'], ('market', i)
                for s in range(2):
                    assert states[s].observation.private == expected[s]['observation']['private'], ('private', i, s)
                checked += 1
        crops = [dict(x=x, y=y, crop=t['crop'], units=t['yield_units'])
                 for y, row in enumerate(farms[1]['tiles']) for x, t in enumerate(row)
                 if isinstance(t, dict) and t.get('crop') and t.get('yield_units')]
        results.append(dict(mode=mode, cash=[f['money'] for f in farms],
                            own_delta=farms[1]['money']-replay['rewards'][1],
                            shed={k:v for k,v in states[1].observation.private['shed'].items() if v},
                            crops=crops, verified_control_states=checked, tomato_routes=changes))
    report = dict(episode=108491899, seed=replay['info']['seed'], source=str(SOURCE.relative_to(ROOT)),
                  sha256=hashlib.sha256(raw).hexdigest(), worker_action_parity=worker_matches,
                  market_order_differences=market_differences,
                  caveat='Fixed recorded opponent actions; ex-post diagnostic, not a policy evaluation. Market order parity with source not asserted.',
                  results=results)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'AUDIT.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps([dict(mode=x['mode'], cash=x['cash'], delta=x['own_delta']) for x in results]))


if __name__ == '__main__':
    run()
