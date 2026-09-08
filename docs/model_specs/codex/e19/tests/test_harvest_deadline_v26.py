from docs.model_specs.codex.e19.tools.daily_routes_770_v26 import harvest_due,pack_routes

def test_last_full_day_and_overdue_are_reserved():
    t=dict(kind='PLANT',crop='WHEAT',yield_units=3,max_lifespan_step=384)
    assert not harvest_due(t,14)
    assert harvest_due(t,15)
    assert harvest_due(t,16)

def test_empty_or_unlimited_life_does_not_create_collection():
    assert not harvest_due(dict(kind='PLANT',yield_units=0,max_lifespan_step=384),16)
    assert not harvest_due(dict(kind='PLANT',yield_units=2,max_lifespan_step=-1),16)
    assert not harvest_due(dict(kind='WEED'),16)

def test_deadline_harvest_gets_capacity_before_optional_visit():
    urgent=((2,0),[['HARVEST']],6,1,'SERVICE')
    optional=((0,1),[['WATER']],2,1,'SERVICE')
    routes,unassigned=pack_routes([(0,0)],[{}],[(0,0)],[optional,urgent],3)
    assert routes==[[urgent]]
    assert unassigned==[optional]
