from docs.model_specs.codex.e18.tools.e18_31_unified_investment_controller import UnifiedInvestmentController


def setup(rows=(), hands=0, money=1000):
    a=UnifiedInvestmentController(dict(trajectory=list(rows),daily=[{'day':1,'planned_hands':hands}],
                                      treatment_config={'progressive_cows':True}))
    f=dict(farmer=[4,4],hands=[],tiles=[[None]*10 for _ in range(10)],
           money=money,hires_today=0,unlocked_quadrants=['NW'])
    p=dict(shed={},seeds={},inventories=[{}])
    obs=dict(day=0,hour=0,farms=[f],private=p,market={'prices':{'WHEAT':30,'MILK':160,'FERTILIZER':100}})
    a.selected=[(['PASS'],None)]
    return a,obs


def row(op,day,worker,**args):
    return dict(day=day,turn=2,worker=worker,step=(day-1)*24+2,
                opcode=op,position=[4,4],arguments=args)


def test_append_only_roster_cannot_stop_at_an_empty_legacy_slot():
    a,obs=setup([row('CARE',1,3)],hands=3)
    orders=a._market_orders(obs,1,1)
    assert orders.count(['HIRE'])==3


def test_distant_planned_cow_is_not_speculatively_purchased():
    a,obs=setup([row('PICKUP',5,1,item='COW',units=1),row('PLACE',5,1,animal='COW')])
    assert not any(o[0]=='BUY_ANIMAL' for o in a._market_orders(obs,1,1))


def test_overnight_staging_has_a_real_next_day_placement_obligation():
    a,obs=setup([row('PICKUP',5,1,item='COW',units=1),row('PLACE',5,1,animal='COW')])
    assert ['BUY_ANIMAL','COW',1] in a._market_orders(obs,4,20)
    assert not any(o[0]=='BUY_ANIMAL' for o in a._market_orders(obs,3,20))


def test_today_feed_is_funded_before_an_additional_animal():
    a,obs=setup([row('PICKUP',1,1,item='WHEAT',units=6),
                row('PICKUP',1,1,item='COW',units=2)],money=500)
    orders=a._market_orders(obs,1,1)
    assert ['BUY_PRODUCT','WHEAT',6] in orders
    assert not any(o[0]=='BUY_ANIMAL' for o in orders)


def test_only_unsettled_purchase_locks_another_investment():
    a,_=setup()
    a.active={'first':{'purchase':True,'index':0}}
    assert a._investment_inflight()
    a.active['first']['index']=1
    assert not a._investment_inflight()
