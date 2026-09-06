import json
from copy import deepcopy
from pathlib import Path
import pytest
from docs.model_specs.codex.e18.tools.e18_33_common_policy import Profile,pasture_candidates
from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController

BASE=Path(__file__).resolve().parents[1]
CONFIG=json.loads((BASE/'configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V2_BOOTSTRAP.json').read_text())

def test_bootstrap_is_small_explicit_and_has_no_date_or_quadrant():
    p=Profile.from_config(CONFIG)
    assert dict(p.bootstrap_animals)=={'COW':2,'SHEEP':2}
    assert p.bootstrap_crops==('WHEAT','CARROT')
    for key in ('day','Q0','coordinates','reset_on_land_purchase'):
        bad=deepcopy(CONFIG); bad['bootstrap'][key]=1
        with pytest.raises(ValueError): Profile.from_config(bad)

def test_bootstrap_does_not_reactivate_on_land_purchase_or_day():
    c=CommonController(CONFIG,None,{})
    c.day=3; c.hour=5; c.positions=[(4,4)]
    c.farm={'tiles':[[None]*10 for _ in range(10)]}
    c.private={'inventories':[{'CARROT':4}]}
    c.active={0:dict(kind='SERVICE',target=(4,4),steps=[(['HARVEST'],(4,4))])}
    c.previous={0:(['HARVEST'],(4,4),{})}
    c._acknowledge()
    assert c.bootstrap_done
    c.day=7; c.farm['unlocked_quadrants']=['NW','NE']
    c._acknowledge()
    assert c.bootstrap_done
    assert len([e for e in c.events if e['event']=='bootstrap_retired'])==1

def test_no_refilling_an_inherited_pasture_outside_zero_quota():
    c=deepcopy(CONFIG)
    farm=dict(tiles=[['LOCKED']*10 for _ in range(10)],unlocked_quadrants=['NW','NE','SW'])
    farm['tiles'][5][4]={'kind':'PASTURE'}
    assert not pasture_candidates(farm,Profile.from_config(c))
    c['pastures']['target']=15
    assert pasture_candidates(farm,Profile.from_config(c))==[(4,5)]
