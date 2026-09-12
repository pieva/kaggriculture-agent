"""Read-only replay audit: public entrypoint parity and topology-filter effects.

No new episodes or seeds. The frozen candidate is never modified.
"""
import gzip, hashlib, json, time
from copy import deepcopy
from pathlib import Path

BASE = Path(__file__).resolve().parent

def main():
    bundle = BASE / 'artifacts/fixed774_reconstruction.py'
    replay_path = BASE / 'artifacts/fixed774/Fixed774_E18_180911301.replay.json.gz'
    replay = json.loads(gzip.decompress(replay_path.read_bytes()))
    source = bundle.read_text(encoding='utf-8')
    ns = {'__name__': '_audit_public774'}  # intentionally no __file__
    exec(compile(source, '<standalone774>', 'exec'), ns)
    changes, mismatches, runtimes = [], [], []
    # Wrap the inherited filter only to record its before/after commands.
    cls = ns['_e18_2'].CodexE17TopologyCap662Agent
    original = cls._filter_unit_actions
    def traced(self, action, observation):
        before = deepcopy(action)
        result = original(self, action, observation)
        farm = observation['farms'][observation['player']]
        positions = [farm['farmer'], *farm['hands']]
        old = [before.get('farmer', ['PASS']), *before.get('hands', [])]
        new = [action.get('farmer', ['PASS']), *action.get('hands', [])]
        for worker, (a, b) in enumerate(zip(old, new)):
            if a != b:
                changes.append(dict(day=observation['day']+1, hour=observation['hour']+1,
                                    worker=worker, position=positions[worker], before=a, after=b))
        return result
    cls._filter_unit_actions = traced
    for i in range(719):
        obs = deepcopy(replay['steps'][i][0]['observation'])
        start = time.perf_counter()
        action = ns['agent'](obs, deepcopy(replay['configuration']))
        runtimes.append(time.perf_counter()-start)
        if action != replay['steps'][i+1][0]['action']:
            mismatches.append(i)
    policy = ns['_FIXED774_ACTIVE'][0][1]
    topology_violations = []
    for i, step in enumerate(replay['steps']):
        counts = [0]*4
        for y, row in enumerate(step[0]['observation']['farms'][0]['tiles']):
            for x, tile in enumerate(row):
                if isinstance(tile,dict) and tile.get('kind') == 'PASTURE':
                    counts[int(x>=5)+2*int(y>=5)] += 1
        if any(a>b for a,b in zip(counts,[7,7,4,0])):
            topology_violations.append(dict(step=i, counts=counts))
    final = []
    for seat in range(2):
        obs = replay['steps'][-1][seat]['observation']
        animals = {}
        for row in obs['farms'][seat]['tiles']:
            for tile in row:
                if isinstance(tile,dict) and tile.get('animal'):
                    species = tile['animal']; animals[species] = animals.get(species,0)+1
        final.append(dict(seat=seat, animals=animals, private=obs['private']))
    # A reset to step zero must discard the prior episode's controller.
    first = ns['agent'](deepcopy(replay['steps'][0][0]['observation']), replay['configuration'])
    reset_ok = first == replay['steps'][1][0]['action'] and ns['_FIXED774_ACTIVE'][0][1] is not policy
    result = dict(bundle_sha256=hashlib.sha256(bundle.read_bytes()).hexdigest(),
                  public_entrypoint_calls=719, mismatches=mismatches, max_seconds=max(runtimes),
                  reset_ok=reset_ok, topology_violations=topology_violations,
                  filter_changes=changes, terminal_filter_changes=[c for c in changes if c['day']>=29],
                  final=final, telemetry=policy.core.telemetry_snapshot(),
                  model_version=ns['MODEL_VERSION'], build_metadata=ns['BUILD_METADATA'])
    out=BASE/'reports/audit_fixed774'; out.mkdir(exist_ok=True)
    (out/'AUDIT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    assert not mismatches and not topology_violations and reset_ok
    print(json.dumps({k:v for k,v in result.items() if k not in ['telemetry','filter_changes','final']},indent=2))

if __name__=='__main__': main()
