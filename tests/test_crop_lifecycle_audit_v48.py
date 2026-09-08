from copy import deepcopy
from docs.model_specs.codex.e19.tools.crop_lifecycle_audit_v48 import crop_service_audit


def event(tile, day=27, hour=23):
    before={'day':day,'hour':hour,'farms':[{'tiles':[[tile]]}], 'private':{'seeds':{}}}
    after=deepcopy(before)
    after['day']+=1
    after['farms'][0]['tiles']=[[{'kind':'WEED'}]]
    replay={'configuration':{},'steps':[[{'observation':before}],
        [{'observation':after,'action':{'farmer':[]}}]]}
    return crop_service_audit(replay,0)[0]


def strawberry(units=0, planted=11, expiry=672):
    return dict(kind='PLANT',crop='STRAWBERRY',planted_day=planted,
                watered_today=False,consecutive_unwatered=1,yield_units=units,
                max_lifespan_step=expiry,fertilized_until_day=-1)


def test_spent_harvested_plant_is_not_productive_loss():
    e=event(strawberry())
    assert e['physical_cause']=='water_refresh'
    assert not e['productive_loss']
    assert e['last_production_day']==28


def test_future_yield_requires_protection():
    e=event(strawberry(planted=13,expiry=-1))
    assert e['future_production'] and e['productive_loss']


def test_held_yield_is_distinct_from_future_yield():
    e=event(strawberry(units=1))
    assert e['productive_loss'] and not e['future_production']
    assert e['held_units_after_actions']==1


def test_decay_precedes_water_refresh():
    e=event(strawberry(expiry=671))
    assert e['physical_cause']=='decay'
    assert not e['productive_loss']
