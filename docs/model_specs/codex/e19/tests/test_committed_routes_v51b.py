from collections import Counter
from types import SimpleNamespace
from docs.model_specs.codex.e19.tools.committed_routes_v51c import install

def core_for(day=28):
    offers=[((1,0),[['WATER'],['HARVEST']],6,10,'SERVICE'),((1,0),[['HARVEST']],5,5,'SERVICE')]
    return SimpleNamespace(day=day,hour=1,remaining=23,positions=[(0,0),(0,0)],sheds=[(0,0)],
        private={'shed':{},'inventories':[{},{}]},active={},
        _services=lambda:offers,_bootstrap_transition=lambda:None,
        _requirements=lambda:(Counter(),Counter()),_portfolio_return_required=lambda t,c:True,
        _market_orders=lambda:[['SELL','WHEAT',1],['HIRE']])

def test_full_yield_visit_survives_bare_harvest_fallback():
    core=core_for();install(core);core._bootstrap_transition()
    commands=[c for job in core.active.values() for c,p in job['steps']]
    assert ['WATER'] in commands and ['HARVEST'] in commands
    assert commands.index(['WATER'])<commands.index(['HARVEST'])
    assert not core._services()
    assert core._market_orders()==[['SELL','WHEAT',1]]

def test_outside_d29_no_committed_jobs_or_market_changes():
    core=core_for(27);install(core);core._bootstrap_transition()
    assert not core.active and len(core._services())==2
    assert core._market_orders()==[['SELL','WHEAT',1],['HIRE']]
