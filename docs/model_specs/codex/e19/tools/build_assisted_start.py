"""Freeze two local assisted candidates with the same governor and V2 core."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]


def build():
    governor=Path(__file__).with_name('assisted_start.py')
    teacher=ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'
    for topology,base in [('770','submission_codex_e19_control_770_v2.py'),('662','submission_codex_e19_1_662_v2.py')]:
        core=ROOT/'submission'/base
        model='e18_770' if topology=='770' else 'e19_662'
        output=ROOT/'submission'/f'submission_codex_{model}_assisted_start_v1_candidate.py'
        source='''"""Local assisted-start experiment. D1-D11 verified; later economy unvalidated."""
import sys
import types

def _load(name, source):
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(compile(source, name, 'exec'), module.__dict__)
    return module
'''
        source+=f"\n_TEACHER = _load('_assisted_{topology}_teacher', {teacher.read_text(encoding='utf-8')!r})\n"
        source+=f"_CORE = _load('_assisted_{topology}_core', {core.read_text(encoding='utf-8')!r})\n"
        source+=governor.read_text(encoding='utf-8')
        source+=f"\nMODEL_VERSION = 'CODEX-{model.upper()}-ASSISTED-START-V1-CANDIDATE'\n"
        source+='''
def create_agent(run_context=None):
    return AssistedStart(_TEACHER.create_agent(run_context), _CORE.create_agent(run_context))

_ACTIVE = {}
def agent(observation, configuration=None):
    seat = int(observation.get('player', 0))
    step = observation['day'] * (configuration or {}).get('turnsPerDay', 24) + observation['hour']
    previous = _ACTIVE.get(seat)
    policy = create_agent({'player_position': seat}) if previous is None or step <= previous[0] else previous[1]
    _ACTIVE[seat] = (step, policy)
    return policy(observation, configuration or {})
'''
        compile(source,str(output),'exec')
        assert not output.exists(), 'Frozen candidates are immutable'
        output.write_text(source,encoding='utf-8',newline='\n')
        core_manifest=json.loads(core.with_suffix('.manifest.json').read_text())
        manifest=dict(topology=topology,status='LOCAL_D11_EXPERIMENT_NOT_PUBLISHED',uploaded=False,
                      assisted_days=11,mechanism='Historical V4D teacher with observed target-cap filter; frozen common V2 core from D12',
                      profile=core_manifest['profile'],core_sha256=core_manifest['core_sha256'],
                      sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [teacher,core,governor,Path(__file__)]},
                      submission_sha256=hashlib.sha256(output.read_bytes()).hexdigest())
        output.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(output)


if __name__=='__main__':build()
