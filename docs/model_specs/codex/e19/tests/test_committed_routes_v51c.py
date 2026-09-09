from collections import Counter
from types import SimpleNamespace
from docs.model_specs.codex.e19.tools.committed_routes_v51c import install

def test_hires_cover_full_water_harvest_visits_with_actual_spawn():
    offers=[((x,4),[['WATER'],['HARVEST']],6,10,'SERVICE') for x in [3,4,5]]
    core=SimpleNamespace(day=28,hour=1,remaining=23,positions=[(4,4)]*7,sheds=[(4,4)],
        farm={'tiles':[[None]*10 for _ in range(10)]},private={'shed':{},'inventories':[{} for _ in range(7)]},active={},
        _services=lambda:offers,_bootstrap_transition=lambda:None,
        _requirements=lambda:(Counter(),Counter()),_portfolio_return_required=lambda t,c:True,
        _market_orders=lambda:[['HIRE']]*6)
    install(core)
    assert core._market_orders()==[['HIRE']]
    assert core.v51_log[-1]['pending_visits']==3
