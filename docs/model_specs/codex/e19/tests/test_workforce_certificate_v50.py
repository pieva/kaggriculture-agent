from types import SimpleNamespace
from docs.model_specs.codex.e19.tools.workforce_certificate_v50 import certified_hands,spawn,install
from docs.model_specs.codex.e19.tools.supplied_routes_v50 import pack_routes
from docs.model_specs.codex.e19.tools.closed_routes_v50 import closed_cost
from docs.model_specs.codex.e19.tools.workforce_certificate_v50h import certified_additions
from docs.model_specs.codex.e19.tools.optional_fertilizer_v50 import install as omit_optional


def core():
    return SimpleNamespace(active={},positions=[(4,4)],remaining=24,
        private={'inventories':[{}],'shed':{}},farm={'tiles':[[None]*10 for _ in range(10)]},
        sheds=[(4,4)],day=28,hour=0)


def test_engine_spawn_order():
    assert [spawn(w,10) for w in range(1,9)]==[(5,4),(4,5),(5,5),(4,4)]*2


def test_no_work_does_not_need_hands():
    count,proof=certified_hands(core(),[],12)
    assert count==0 and proof['visits']==0


def test_missing_input_keeps_baseline():
    c=core()
    count,proof=certified_hands(c,[((5,4),[['FEED']],3,1,'SERVICE')],12)
    assert count==12 and proof is None


def test_active_harvest_requires_return_even_without_queued_visits():
    c=core();c.remaining=5;c.positions=[(9,9)]
    c.active={0:dict(target=(9,9),kind='SERVICE',steps=[(['HARVEST'],(9,9))])}
    count,proof=certified_hands(c,[],12)
    assert count==12 and proof is None


def test_only_d29_initial_hiring_is_changed():
    c=core();c.day=27;c._market_orders=lambda:[['HIRE'],['SELL_PRODUCT','CARROT',1]]
    c._services=lambda:[]
    install(c)
    assert c._market_orders()==[['HIRE'],['SELL_PRODUCT','CARROT',1]]
    c.day=28
    assert c._market_orders()==[['SELL_PRODUCT','CARROT',1]]


def test_carried_grain_cannot_be_used_by_another_worker():
    offer=((2,0),[['FEED']],3,1,'SERVICE')
    routes,missing=pack_routes([(0,0),(2,0)],[{'WHEAT':1},{}],[(0,0)],[offer],12,warehouse={})
    assert not missing and routes[0]==[offer] and routes[1]==[]


def test_depot_grain_is_not_double_reserved():
    offers=[((1,0),[['FEED']],3,1,'SERVICE'),((0,1),[['FEED']],3,1,'SERVICE')]
    routes,missing=pack_routes([(0,0),(0,0)],[{},{}],[(0,0)],offers,12,warehouse={'WHEAT':1})
    assert len(missing)==1 and sum(map(len,routes))==1


def test_return_is_included_in_insertion_cost():
    route=[((3,0),[['HARVEST']],6,1,'SERVICE')]
    assert closed_cost((0,0),route,[(0,0)],{})==8


def test_required_work_excludes_optional_fertilizer_but_keeps_water():
    c=core();c._portfolio_return_required=lambda *args:False
    count,proof=certified_additions(c,[((4,4),[['FERTILIZE'],['WATER']],2,1,'SERVICE')],12,[])
    assert count==0 and proof['visits']==1 and proof['pickups']=={}


def test_sales_are_removed_from_available_service_inputs():
    c=core();c._portfolio_return_required=lambda *args:False;c.private['shed']={'WHEAT':1}
    count,proof=certified_additions(c,[((4,4),[['FEED']],3,1,'SERVICE')],12,[['SELL','WHEAT',1]])
    assert count==12 and proof is None


def test_optional_collection_removed_before_route_reservations():
    offers=[((4,4),[['FEED'],['COLLECT_FERTILIZER']],3,5,'SERVICE'),((5,4),[['COLLECT_FERTILIZER']],2,1,'SERVICE')]
    def wrapper(services):
        def route_services():return services()
        return route_services
    c=core();c._quote=lambda *args:1;c._services=wrapper(lambda:offers)
    omit_optional(c)
    assert c._services()==[((4,4),[['FEED']],3,4,'SERVICE')]
    c.day=27
    assert c._services()==offers
