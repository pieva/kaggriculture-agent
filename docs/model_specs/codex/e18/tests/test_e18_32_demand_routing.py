"""Route certificates and day-independent admission; no public replay fixture."""
from collections import Counter
from copy import deepcopy

import pytest

from docs.model_specs.codex.e18.tools.e18_32_demand_routing_controller import DemandRoutingController as Controller
from docs.model_specs.codex.e18.tools.e18_32_claim_routing_controller import ClaimRoutingController
from docs.model_specs.codex.e18.tools.e18_32_reservation_routing_controller import ReservationRoutingController


def action(op,target=(3,4),**arguments):
    return dict(opcode=op,position=list(target),arguments=arguments)


def policy(day=5):
    rows=[]
    for w,target in enumerate([(3,4),(3,3),(4,3)]):
        for i,op in enumerate(['FEED','CARE','COLLECT_FERTILIZER']):
            rows.append(dict(day=day,turn=5+i,worker=w,step=(day-1)*24+4+i,
                             **action(op,target)))
    p=dict(trajectory=rows,daily=[dict(day=day,planned_hands=5)],
           treatment_config={'progressive_cows':True})
    c=Controller(p)
    tiles=[[None]*10 for _ in range(10)]
    for target in [(3,4),(3,3),(4,3)]:
        x,y=target
        tiles[y][x]=dict(kind='PASTURE',animal='COW',fed_today=False,cared_today=False,
                         fertilizer_available=True,yield_units=0)
    obs=dict(day=day-1,hour=0,farms=[dict(tiles=tiles,money=1000,hands=[],farmer=[4,4])],
             private={'shed':{'WHEAT':3},'seeds':{},'inventories':[{}]})
    c.demand_observation=obs
    return c,obs


@pytest.mark.parametrize('day',[1,5,10,15,20,30])
def test_equivalent_workload_has_equivalent_roster_at_every_day(day):
    c,obs=policy(day)
    before=deepcopy(obs)
    c._new_day(day)
    assert c.daily_hands[day]==0  # nine services + short travel fit the farmer
    assert day in c.repacked_days
    assert obs==before
    c._new_day(day)
    assert len(c.routing_log)==1


def test_obligations_and_feed_units_survive_reassignment():
    c,obs=policy()
    c._new_day(5)
    rows=[r for (d,_),rs in c.routes.items() if d==5 for r in rs]
    assert Counter(r['opcode'] for r in rows)['FEED']==3
    assert sum(r['arguments']['units'] for r in rows if r['opcode']=='PICKUP')==3
    assert max(r['turn'] for r in rows)<=22
    assert any(r['opcode']=='DROP' for r in rows)


def test_locked_land_does_not_make_a_false_capacity_certificate():
    c,obs=policy()
    obs['farms'][0]['tiles'][4][3]='LOCKED'
    c._new_day(5)
    assert c.daily_hands[5]==5
    assert 5 not in c.repacked_days


def test_advanced_cows_enter_workload_and_are_not_double_reserved():
    c,obs=policy()
    target=(4,4)
    c.advanced.add(target)
    c.pasture_plan[target]=(10,'COW')
    obs['farms'][0]['tiles'][4][4]=dict(kind='PASTURE',animal='COW',fed_today=False,
                                      cared_today=False,fertilizer_available=True,yield_units=0)
    c._new_day(5)
    assert c._pending_requirements(5,'pickup')['WHEAT']==4
    assert c._extra_feed(5)==0


def test_infeasible_big_bundle_is_rejected_not_truncated():
    bundles=[((0,0),[action('WATER',(0,0)) for _ in range(30)])]
    assert Controller._pack(bundles,12) is None


def test_full_return_route_is_counted_for_revenue_but_not_pure_water():
    start=(4,4)
    assert Controller._cost([((0,0),[action('HARVEST',(0,0))])],start)==18
    assert Controller._cost([((0,0),[action('WATER',(0,0))])],start)==9


def test_ready_milk_of_non_advanced_cows_is_not_missing_from_demand():
    c,obs=policy()
    obs['farms'][0]['tiles'][4][3]['yield_units']=6
    bundles=c._bundles(5,obs['farms'][0])
    assert any(r['opcode']=='HARVEST' for t,rows in bundles if t==(3,4) for r in rows)


def test_release_completed_service_while_delivery_is_still_running():
    c,obs=policy()
    c.__class__=ClaimRoutingController
    target=(3,4)
    job=dict(worker=0,target=target,claimed_ops=['FEED','COLLECT_FERTILIZER'],
             steps=[(['FEED'],target),(['COLLECT_FERTILIZER'],target),(['EAST'],(4,4)),(['DROP'],(4,4))],
             index=2,emitted=False)
    c.active['test']=job
    c._observe(5,10,obs['farms'][0],obs['private'])
    assert job['claimed_ops']==[]
    assert c.active['test'] is job  # delivery/inventory obligation remains
    assert c.ready_metrics['completed_service_claims_released']==2


def test_emission_alone_does_not_release_unconfirmed_service():
    c,obs=policy()
    c.__class__=ClaimRoutingController
    target=(3,4)
    c.active['test']=dict(worker=0,target=target,claimed_ops=['FEED'],
             steps=[(['FEED'],target),(['EAST'],(4,4))],index=0,emitted=True,before={'WHEAT':1})
    c._observe(5,10,obs['farms'][0],obs['private'])
    assert c.active['test']['claimed_ops']==['FEED']


def test_finance_dependency_bounds_drop_time_not_just_total_work():
    target=(3,4)
    bundles=[(target,[action('HARVEST',target)]),((0,0),[action('WATER',(0,0))])]
    result=Controller._pack(bundles,2,{target},5)
    assert result is not None
    for segment,start in zip(result[2],result[3]):
        if any(t==target for t,_ in segment):
            assert Controller._cost(segment,start)<=5


def test_two_workers_cannot_pick_up_the_same_unit_in_one_batch():
    c,obs=policy()
    c.__class__=ReservationRoutingController
    farm,private=obs['farms'][0],obs['private']
    farm['hands']=[[4,4]]
    private['shed']={'WHEAT':1}
    private['inventories']=[{},{}]
    c.batch_stock=Counter({'WHEAT':1})
    row=dict(day=5,turn=2,worker=0,step=97,**action('PICKUP',(4,4),item='WHEAT',units=1))
    c.routes[(5,0)]=[row]
    c.routes[(5,1)]=[deepcopy(row)]
    before=deepcopy(obs)
    first,_=c._planned_or_recovery(row,farm,private,0,(5,0))
    second,_=c._planned_or_recovery(c.routes[(5,1)][0],farm,private,1,(5,1))
    assert first==['PICKUP','WHEAT',1]
    assert second==['PASS']
    assert c.cursors[(5,1)]==0
    assert obs==before


def test_active_mission_pickup_has_exclusive_stock_before_legacy_queues():
    c,obs=policy()
    c.__class__=ReservationRoutingController
    c.active['test']=dict(worker=0,target=(3,4),claimed_ops=['FEED'],
                         steps=[(['PICKUP','WHEAT',2],(4,4)),(['FEED'],(3,4))],index=0,emitted=False)
    c._observe(5,2,obs['farms'][0],obs['private'])
    assert c.batch_stock['WHEAT']==1


@pytest.mark.parametrize('day',[2,8,17,29])
def test_unfunded_feed_requires_resource_cycle_not_just_shorter_geometry(day):
    c,obs=policy(day)
    obs['farms'][0]['money']=25
    obs['private']['shed']={'WHEAT':1}
    c._new_day(day)
    assert c.daily_hands[day]==5
    assert c.ready_metrics['fallback_unfunded_maintenance']==1
