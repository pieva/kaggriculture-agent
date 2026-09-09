from collections import Counter
from docs.model_specs.codex.e19.tools.committed_routes_v51c import compile_route,pack_exact

def offer(target,commands):return (target,commands,8,1,'SERVICE')

def test_compile_bulk_input_and_exact_return():
    route=[offer((2,0),[['FEED']]),offer((3,0),[['FEED'],['HARVEST']])]
    steps=compile_route((0,0),{},[(0,0)],route,lambda t,c:True)
    assert steps[0]==(['PICKUP','WHEAT',2],(0,0))
    assert len(steps)==11 and steps[-1]==(['DROP'],(0,0))
    assert [p for c,p in steps if c[0]=='FEED']==[(2,0),(3,0)]

def test_shared_grain_not_double_reserved():
    routes,missing=pack_exact([(0,0),(0,0)],[{},{}],[(0,0)],
        [offer((1,0),[['FEED']]),offer((0,1),[['FEED']])],[3,3],Counter(WHEAT=1),lambda t,c:False)
    assert len(missing)==1 and sum(map(len,routes))==1

def test_carried_grain_stays_with_worker_and_active_budget_is_zero():
    route=offer((1,0),[['FEED']])
    routes,missing=pack_exact([(0,0),(0,0)],[{'WHEAT':1},{}],[(0,0)],[route],[0,10],{},lambda t,c:False)
    assert missing==[route] and not any(routes)

def test_return_cost_blocks_route_without_time():
    route=offer((2,0),[['HARVEST']])
    routes,missing=pack_exact([(0,0)],[{}],[(0,0)],[route],[5],{},lambda t,c:True)
    assert missing==[route]
    routes,missing=pack_exact([(0,0)],[{}],[(0,0)],[route],[6],{},lambda t,c:True)
    assert not missing and len(compile_route((0,0),{},[(0,0)],routes[0],lambda t,c:True))==6
