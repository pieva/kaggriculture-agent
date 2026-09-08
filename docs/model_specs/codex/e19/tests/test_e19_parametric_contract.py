import json
from copy import deepcopy
from pathlib import Path

from docs.model_specs.codex.e18.tools.e18_33_common_policy import Profile
from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[3]


def test_only_local_capacity_changes_from_frozen_770_profile():
    reference=json.loads((BASE.parent/'e18/configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V2_BOOTSTRAP.json').read_text())
    actual=json.loads((BASE/'configs/CODEX_E19_1_662_V1.json').read_text())
    expected=deepcopy(reference)
    expected['pastures']['uniform_capacity_per_quadrant']=6
    assert actual==expected
    profile=Profile.from_config(actual)
    assert list(profile.pasture_budgets(['NW','NE','SW','SE']).values())==[6,6,2,0]
    assert profile.species_targets()=={'COW':9,'SHEEP':5}


def test_frozen_bundle_core_is_identical_to_770_control():
    a=json.loads((ROOT/'submission/submission_codex_e18_33_770_v24_candidate.manifest.json').read_text())
    b=json.loads((ROOT/'submission/submission_codex_e19_1_662_v1.manifest.json').read_text())
    assert a['core_sha256']==b['core_sha256']


def test_pending_bulk_feed_pickup_reserves_stock_until_observed():
    controller=CommonController.__new__(CommonController)
    controller.private={'inventories':[{},{}]}
    controller.active={0:{'steps':[(['PICKUP','WHEAT',3],(4,4)),(['FEED'],(3,4))]},
                       1:{'steps':[(['PICKUP','WHEAT',1],(4,4)),(['FEED'],(4,3))]}}
    assert controller._requirements()[0]['WHEAT']==4
    controller.private['inventories'][0]={'WHEAT':3}
    controller.active[0]['steps'].pop(0)
    assert controller._requirements()[0]['WHEAT']==1


def test_v2_662_and_770_share_corrected_core():
    a=json.loads((ROOT/'submission/submission_codex_e19_control_770_v2.manifest.json').read_text())
    b=json.loads((ROOT/'submission/submission_codex_e19_1_662_v2.manifest.json').read_text())
    assert a['core_sha256']==b['core_sha256']
