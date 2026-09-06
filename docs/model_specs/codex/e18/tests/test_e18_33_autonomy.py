import json
from pathlib import Path
from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController

CONFIG=json.loads((Path(__file__).resolve().parents[1]/'configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V3_AUTONOMY.json').read_text())

def test_full_initial_cycle_and_cash_are_required_not_a_calendar():
    c=CommonController(CONFIG,None,{})
    c.day=25; c.hour=0; c.farm={'money':300}; c.maintenance_floor=200
    c._owned=lambda:{'COW':2,'SHEEP':2}
    c.previous_day_cash_delta=10
    c.bootstrap_first_cycle={(4,3),(3,3)}
    c.bootstrap_renewed={(4,3)}
    c._bootstrap_transition()
    assert not c.bootstrap_done # Late date does not release assistance.
    c.day=4; c.bootstrap_renewed.add((3,3)); c.farm['money']=199
    c._bootstrap_transition()
    assert not c.bootstrap_done
    c.farm['money']=300; c.previous_day_cash_delta=-1
    c._bootstrap_transition()
    assert not c.bootstrap_done
    c.previous_day_cash_delta=1
    c._bootstrap_transition()
    assert c.bootstrap_done # Early release is allowed from observed conditions.
    c.day=5; c.farm['money']=0; c._bootstrap_transition()
    assert c.bootstrap_done # No reactivation / day-dependent second policy.
