"""Invariant checks backed by actual development replays; no extra simulations."""
import gzip
import json
from pathlib import Path
import sys
import pytest
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.policy import create_agent,VARIANTS

def test_profile_and_parent_isolation():
    import runpy
    p=create_agent({'player_position':0},'E20v18')
    assert p.core.profile.pasture_budgets(['NW','NE','SW'])=={'NW':7,'NE':7,'SW':2}
    assert p.core.profile.species_targets()=={'COW':10,'SHEEP':6}
    assert p.profile.target==14  # Frozen governor through D11.
    assert p.core.e20_reserved=={(4,5):'COW',(4,6):'SHEEP'}
    parent=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_v48_external.py'))['create_agent']({'player_position':1})
    assert parent.core.profile.target==14
    assert not hasattr(parent.core,'e20_reserved')
    assert p.core.profile.target==16

def test_replays_opening_and_topology():
    base=ROOT/'docs/model_specs/codex/e20/artifacts'
    if not (base/'baseline/E19_E18_180903001.replay.json.gz').exists():
        pytest.skip('Generate local baseline/development replays before the replay contract check')
    with gzip.open(base/'baseline/E19_E18_180903001.replay.json.gz','rt') as f:control=json.load(f)
    paths=sorted((base/'development').glob('E20*_E18_180903001.replay.json.gz'))
    assert paths
    control_actions=[s[0]['action'] for s in control['steps'][1:265]]
    for path in paths:
        with gzip.open(path,'rt') as f:replay=json.load(f)
        assert [s[0]['action'] for s in replay['steps'][1:265]]==control_actions,path.name
        assert len(replay['steps'])==720
        for step in replay['steps']:
            farm=step[0]['observation']['farms'][0]
            counts=[0,0,0]
            for y,row in enumerate(farm['tiles']):
                for x,tile in enumerate(row):
                    if isinstance(tile,dict) and tile.get('kind')=='PASTURE':
                        q=(0 if x<5 else 1) if y<5 else 2
                        counts[q]+=1
            assert all(n<=cap for n,cap in zip(counts,[7,7,2])),(path.name,counts)
        assert counts==[7,7,2],path.name

def test_reservations_are_e18_plots():
    e18=json.loads((ROOT/'docs/model_specs/codex/e18/configs/CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1.json').read_text())
    legal={tuple(p) for p in e18['dense_pasture_targets'] if p[1]>=5}
    for variant,cfg in VARIANTS.items():
        assert len(set(cfg['positions']))==2
        assert set(cfg['positions'])<=legal,variant

@pytest.mark.parametrize('variant',['e20v18','e20v28'])
def test_standalone_factory_needs_no_source_files(variant):
    import runpy
    from unittest.mock import patch
    bundle=runpy.run_path(str(ROOT/f'submission/submission_codex_e20_772_{variant}_candidate.py'))
    with patch('builtins.open',side_effect=AssertionError('Standalone attempted file access')), \
         patch('io.open',side_effect=AssertionError('Standalone attempted io file access')), \
         patch.object(Path,'open',side_effect=AssertionError('Standalone attempted Path file access')):
        p=bundle['create_agent']({'player_position':1})
    assert p.core.seat==1
    assert p.core.e20_reserved=={(4,5):'COW',(4,6):'SHEEP'}
