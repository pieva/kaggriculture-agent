from docs.model_specs.codex.e19.tools.daily_routes_770_v22 import route_cost,pack_routes,renewal_commands

def offer(x,commands):return ((x,0),commands,3,1,'SERVICE')

def test_one_depot_pickup_covers_multiple_feed_visits():
    route=[offer(1,[['FEED'],['CARE']]),offer(2,[['FEED'],['CARE']])]
    assert route_cost((0,0),route,[(0,0)],{})==7
    assert route_cost((0,0),route,[(0,0)],{'WHEAT':2})==6

def test_all_visits_are_accounted_and_routes_fit_observed_workers():
    offers=[offer(x,[['WATER']]) for x in [1,2,3,20]]
    routes,unassigned=pack_routes([(0,0),(4,0)],[{},{}],[(0,0)],offers,4)
    assert len(routes)==2
    assert len(unassigned)==1 and unassigned[0][0]==(20,0)
    assert sorted(o[0] for route in routes for o in route)==[(1,0),(2,0),(3,0)]
    assert all(route_cost(start,route,[(0,0)],{})<=4 for start,route in zip([(0,0),(4,0)],routes))

def test_renewal_preserves_old_yield_water_and_new_seedling_water():
    assert renewal_commands([['WATER'],['HARVEST']],[['HARVEST'],['PLANT','WHEAT'],['WATER']])==[['WATER'],['HARVEST'],['PLANT','WHEAT'],['WATER']]

def test_route_assignment_is_reproducible():
    args=([(0,0),(4,0)],[{},{}],[(0,0)],[offer(1,[['WATER']]),offer(3,[['WATER']])],4)
    assert pack_routes(*args)==pack_routes(*args)


def test_new_worker_receives_work_without_double_booking_active_worker():
    routes,unassigned=pack_routes([(1,0),(2,0)],[{},{}],[(0,0)],[offer(2,[['WATER']])],4,[0,4])
    assert not routes[0] and routes[1] and not unassigned
