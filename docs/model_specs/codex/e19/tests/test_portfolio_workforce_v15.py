from docs.model_specs.codex.e19.tools.portfolio_workforce_v15 import impossible_harvest,care_value

def test_dead_crop_releases_worker_before_arrival():
    job={'steps':[(['EAST'],(1,0)),(['HARVEST'],(1,0))]}
    assert impossible_harvest(job,{'kind':'WEED'})
    assert not impossible_harvest(job,{'kind':'PLANT','yield_units':2})

def test_completed_harvest_does_not_cancel_pending_replant():
    job={'steps':[(['PLANT','WHEAT'],(1,0)),(['WATER'],(1,0))]}
    assert not impossible_harvest(job,None)

def test_empty_harvest_releases_worker():
    assert impossible_harvest({'steps':[(['HARVEST'],(0,0))]}, {'kind':'PLANT','yield_units':0})

def test_care_requires_a_future_production_after_bonus_stored():
    rule=dict(first_yield_day=2,interval=2,max_held=5,product='MILK')
    tile=dict(placed_day=0,pending_care_bonus=0)
    assert care_value(tile,2,4,rule,lambda *a:100)==50
    assert care_value(tile,3,4,rule,lambda *a:100)==0
    assert care_value(dict(tile,cared_today=True),2,4,rule,lambda *a:100)==0
