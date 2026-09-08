from docs.model_specs.codex.e19.tools.biological_plan_770_v17 import biological_calendar,compact_owners

def test_berry_calendar_crosses_handover_without_losing_productions():
    rules={'STRAWBERRY':dict(ongoing=True,first_yield_day=10,interval=2,max_yield=4)}
    c=biological_calendar(dict(crop='STRAWBERRY',planted_day=11),rules)
    assert c['productions']==[21,23,25,27]
    assert c['fertilizer_days']==[20,22,24,26]

def test_annual_last_harvest_is_capped_by_actual_horizon():
    rules={'WHEAT':dict(ongoing=False,first_yield_day=2,max_yield_day=4)}
    assert biological_calendar(dict(crop='WHEAT',planted_day=26),rules)['last_harvest']==29

def test_compact_areas_cover_observed_tiles_using_actual_workers():
    tiles={(x,y):None for y in range(5) for x in range(5)}
    owners=compact_owners(tiles,4)
    assert set(owners)==set(tiles) and set(owners.values())==set(range(4))
    assert max(list(owners.values()).count(w) for w in range(4))<=7
    assert set(compact_owners(tiles,1).values())=={0}
