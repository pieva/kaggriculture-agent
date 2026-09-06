import pytest

from docs.model_specs.codex.e18.tools.e18_31_obligation_controller import ObligationController


@pytest.mark.parametrize('day',[4,8,15,20])
def test_served_early_animal_is_not_a_second_current_day_purchase(day):
    row=dict(day=day+2,turn=3,worker=0,step=0,opcode='PLACE',position=[5,4],arguments={'animal':'COW'})
    a=ObligationController(dict(trajectory=[row],daily=[],treatment_config={'progressive_cows':True}))
    a.advanced={(5,4)}
    farm=dict(tiles=[[None]*10 for _ in range(10)])
    farm['tiles'][4][5]={'kind':'PASTURE','animal':'COW','fed_today':True}
    a.procurement_observation=dict(day=day-1,farms=[farm],private={'inventories':[{}]})
    assert a._extra_feed(day)==0
    assert a._extra_feed(day+1)==1
    farm['tiles'][4][5]['fed_today']=False
    assert a._extra_feed(day)==1


def test_feed_already_carried_or_emitted_is_not_bought_twice():
    row=dict(day=10,turn=3,worker=0,step=0,opcode='PLACE',position=[5,4],arguments={'animal':'COW'})
    a=ObligationController(dict(trajectory=[row],daily=[],treatment_config={'progressive_cows':True}))
    a.advanced={(5,4)}
    farm=dict(tiles=[[None]*10 for _ in range(10)])
    farm['tiles'][4][5]={'kind':'PASTURE','animal':'COW','fed_today':False}
    p={'inventories':[{'WHEAT':1}]}
    a.procurement_observation=dict(day=7,farms=[farm],private=p)
    a.active={'feed':dict(target=(5,4),worker=0,steps=[(['FEED'],(5,4))],index=0)}
    a.selected=[(['EAST'],None)]
    assert a._extra_feed(8)==0
    p['inventories'][0]={}
    a.selected=[(['PICKUP','WHEAT',1],None)]
    assert a._extra_feed(8)==0
    a.selected=[(['EAST'],None)]
    assert a._extra_feed(8)==1


@pytest.mark.parametrize('day',[5,10,20,29])
def test_additional_care_uses_the_same_margin_guard_every_day(day):
    a=ObligationController(dict(trajectory=[],daily=[],treatment_config={'progressive_cows':True}))
    farm=dict(farmer=[4,4],hands=[],tiles=[[None]*10 for _ in range(10)])
    farm['tiles'][4][4]={'kind':'PASTURE','animal':'COW','fed_today':True,
                        'cared_today':False,'fertilizer_available':False,'yield_units':0}
    private=dict(shed={},inventories=[{}],seeds={})
    a.selected=[(['PASS'],None)]
    low=a._offers_for_worker(day,4,0,farm,private,{'MILK':20,'WHEAT':30,'FERTILIZER':70})
    high=a._offers_for_worker(day,4,0,farm,private,{'MILK':200,'WHEAT':30,'FERTILIZER':70})
    assert not low
    assert high[0]['claimed_ops']==['CARE']
