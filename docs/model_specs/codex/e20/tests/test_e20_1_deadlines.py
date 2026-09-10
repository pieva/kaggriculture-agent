from docs.model_specs.codex.e20.tools.policy import productive_water_deadline
from docs.model_specs.codex.e20.tools.policy import care_can_add_yield

RULES={'WHEAT':dict(first_yield_day=2,max_yield_day=4,ongoing=False),
       'STRAWBERRY':dict(first_yield_day=4,interval=2,max_yield=3,ongoing=True)}

def test_protects_surviving_productive_crop_only():
    tile=dict(kind='PLANT',crop='WHEAT',planted_day=10,consecutive_unwatered=1,
              watered_today=False,max_lifespan_step=15*24,yield_units=1)
    assert productive_water_deadline(12,tile,[['WATER']],RULES)
    assert not productive_water_deadline(10,tile,[['WATER']],RULES)
    assert not productive_water_deadline(14,tile,[['WATER'],['HARVEST']],RULES)
    assert not productive_water_deadline(12,tile|{'watered_today':True},[['WATER']],RULES)
    assert not productive_water_deadline(12,tile,[['DIG'],['PLANT','WHEAT'],['WATER']],RULES)

def test_exhausted_perennial_is_not_rescued():
    tile=dict(kind='PLANT',crop='STRAWBERRY',planted_day=4,consecutive_unwatered=1,
              watered_today=False,max_lifespan_step=-1,yield_units=0)
    assert productive_water_deadline(11,tile,[['WATER']],RULES)
    assert not productive_water_deadline(13,tile,[['WATER']],RULES)

def test_care_bonus_saturation_and_nightly_consumption():
    cow=dict(placed_day=11,pending_care_bonus=5,cared_today=False)
    rule=dict(first_yield_day=8,interval=2,max_held=6)
    assert not care_can_add_yield(cow,17,29,rule)  # No production tonight: bonus already full.
    assert care_can_add_yield(cow,18,29,rule)  # Tonight consumes old bonus; today's care is stored afterwards.
    assert care_can_add_yield(cow|{'pending_care_bonus':4},17,29,rule)
    assert not care_can_add_yield(cow|{'pending_care_bonus':0},28,29,rule)

def test_replay_restores_shared_clock_without_crossing_private_state():
    from docs.model_specs.codex.e20.tools.verify_revision import observation_at
    replay=dict(configuration={'turnsPerDay':24},steps=[[
        {'observation':dict(step=25,day=1,hour=1,private={'seat':0})},
        {'observation':dict(day=1,hour=1,private={'seat':1})}]])
    obs=observation_at(replay,0,1)
    assert obs['step']==25 and obs['private']=={'seat':1}
    assert 'step' not in replay['steps'][0][1]['observation']
