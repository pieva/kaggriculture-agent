"""Release initial commitments on installation, without a maturity calendar."""
import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController
from docs.model_specs.codex.e18.tools.e18_33_common_policy import Profile

BASE = Path(__file__).resolve().parents[1]
CONFIG = json.loads((BASE/'configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V7_INITIAL_PORTFOLIO.json').read_text())


def test_schema_and_reject_missing_or_invalid_weights():
    schema = json.loads((BASE/'configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V3.schema.json').read_text())
    Draft202012Validator(schema).validate(CONFIG)
    for weights in ({'WHEAT':1}, {'WHEAT':True,'MELON':2}, {'WHEAT':0,'MELON':2}):
        bad = deepcopy(CONFIG)
        bad['bootstrap']['crop_mix_weights'] = weights
        with pytest.raises(ValueError):
            Profile.from_config(bad)


def test_targets_frozen_from_initial_available_area_and_release_on_installation():
    c = CommonController(CONFIG, None, {})
    c.day = c.hour = 0
    c.farm = dict(tiles=[[None]*5+['LOCKED']*5 for _ in range(5)]+[['LOCKED']*10 for _ in range(5)])
    c._bootstrap_transition()
    assert c.bootstrap_crop_targets == {'MELON':14, 'WHEAT':7}
    # Acquiring land does not enlarge or restart this initial commitment set.
    for y in range(5): c.farm['tiles'][y][5:] = [None]*5
    c._bootstrap_transition()
    assert sum(c.bootstrap_crop_targets.values()) == 21
    tiles = ([dict(crop='MELON') for _ in range(14)]+[dict(crop='WHEAT') for _ in range(7)]
             +[dict(animal='COW') for _ in range(2)]+[dict(animal='SHEEP') for _ in range(2)])
    for i, tile in enumerate(tiles): c.farm['tiles'][i//5][i%5] = tile
    c._bootstrap_transition()
    assert c.bootstrap_done  # No harvest or maturity was necessary.
    c.day = 15
    c._bootstrap_transition()
    assert len([e for e in c.events if e['event'] == 'bootstrap_retired']) == 1


def test_same_initial_governance_with_alternate_local_capacity():
    alternate = deepcopy(CONFIG)
    alternate['pastures']['uniform_capacity_per_quadrant'] = 6
    a, b = Profile.from_config(CONFIG), Profile.from_config(alternate)
    assert a.bootstrap_crop_weights == b.bootstrap_crop_weights
    assert a.species_targets() == b.species_targets()
    assert list(b.pasture_budgets(['NW','NE','SW']).values()) == [6,6,2]
