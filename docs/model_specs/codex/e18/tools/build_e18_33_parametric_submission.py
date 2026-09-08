"""Build an isolated common-core candidate; build does not authorize promotion."""
import argparse
import ast
import hashlib
import importlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]


def build(profile, output, version):
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    from agricola.core.state import CROPS
    from docs.model_specs.codex.e18.tools.e18_33_common_policy import Profile
    config = json.loads(profile.read_text())
    Profile.from_config(config).validate_board(10)
    nodes = ast.parse('import math\nfrom collections import Counter, defaultdict\n'
                      'from copy import deepcopy\nfrom dataclasses import dataclass\nfrom math import ceil\n').body
    constants = dict(CROPS=CROPS, MARKET_PARAMS=engine.MARKET_PARAMS,
                     PRICE_FLOOR=engine.PRICE_FLOOR, HINGE_GAIN=engine.HINGE_GAIN)
    nodes += ast.parse('\n'.join(f'{k} = {v!r}' for k, v in constants.items())).body
    engine_path = Path(engine.__file__)
    nodes += [n for n in ast.parse(engine_path.read_text()).body
              if isinstance(n, ast.FunctionDef) and n.name in {'_shape', 'market_price'}]
    sources = [profile, engine_path, BASE/'tools/e18_33_common_policy.py',
               BASE/'tools/e18_33_common_controller.py', Path(__file__)]
    for path in sources[2:4]:
        for node in ast.parse(path.read_text()).body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            nodes.append(node)
    hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    nodes += ast.parse(f'''
MODEL_VERSION = {version!r}
SOURCE_HASHES = {hashes!r}
PROFILE = {config!r}

def create_agent(run_context=None):
    return CommonController(deepcopy(PROFILE), market_price, MARKET_PARAMS,
                            int((run_context or {{}}).get('player_position', 0)))

_ACTIVE = {{}}

def agent(observation, configuration=None):
    seat = int(observation.get('player', 0))
    step = int(observation.get('step', observation['day']*24+observation['hour']))
    previous = _ACTIVE.get(seat)
    policy = create_agent({{'player_position': seat}}) if previous is None or step <= previous[0] else previous[1]
    _ACTIVE[seat] = (step, policy)
    return policy(observation, configuration or {{}})
''').body
    source = ast.unparse(ast.Module(body=nodes, type_ignores=[]))+'\n'
    compile(source, str(output), 'exec')
    assert not any(s in source for s in ('from docs.', 'from agricola', 'read_text('))
    assert not output.exists(), 'Preserve frozen bundles; use a distinct version'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(source, encoding='utf-8', newline='\n')
    manifest = dict(version=version, profile=config, sources=hashes,
                    core_sha256={p.name: hashes[str(p)] for p in sources[2:4]},
                    submission=str(output), submission_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                    status='LOCAL_CANDIDATE_REQUIRES_PARITY_AND_ACCEPTANCE', uploaded=False)
    output.with_suffix('.manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--profile', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--version', required=True)
    args = p.parse_args()
    build(args.profile.resolve(), args.output.resolve(), args.version)
