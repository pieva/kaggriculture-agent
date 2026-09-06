"""General admission contracts, independent of opponents and calendar targets."""
from copy import deepcopy

import pytest

from docs.model_specs.codex.e18.tools.e18_31_assignment_controller import AssignmentController


def fixture(day=8, *, shed=None, rows=None):
    placement = dict(day=day+1, turn=3, worker=0, step=day*24+3,
                     opcode='PLACE', position=[5,4], arguments={'animal':'COW'})
    agent = AssignmentController(dict(trajectory=[placement, *(rows or [])], daily=[],
                                     treatment_config={'progressive_cows':True}))
    farm = dict(farmer=[4,4], hands=[], tiles=[[None]*10 for _ in range(10)])
    private = dict(shed=shed or {}, inventories=[{}], seeds={})
    agent.selected = [(['PASS'],None)]
    return agent, farm, private


def offers(agent, farm, private, day=8, turn=4):
    return agent._offers_for_worker(day,turn,0,farm,private,{'WHEAT':30,'FERTILIZER':90,'MILK':150})


@pytest.mark.parametrize('day',[1,5,8,15,20])
def test_cow_investment_uses_identical_prerequisites_across_days(day):
    a,f,p = fixture(day,shed={'COW':1,'WHEAT':1})
    jobs = offers(a,f,p,day)
    cow = next(j for j in jobs if j['op']=='ACTIVATE_COW')
    assert not cow['purchase']
    ops = [s[0][0] for s in cow['steps']]
    assert ops.index('PLACE') < ops.index('FEED') < ops.index('CARE')
    assert cow['fence']==23


def test_owned_cow_needs_only_incremental_feed_not_another_animal_purchase():
    a,f,p = fixture(shed={'COW':1})
    job = next(j for j in offers(a,f,p) if j['op']=='ACTIVATE_COW')
    assert job['purchase']
    assert job['procurement']=={'COW':0,'WHEAT':1}


def test_locked_land_is_not_an_executable_investment():
    a,f,p = fixture(shed={'COW':1,'WHEAT':1})
    f['tiles'][4][5]='LOCKED'
    assert not any(j['op']=='ACTIVATE_COW' for j in offers(a,f,p))


def test_no_late_purchase_without_route_time_to_feed_and_care():
    a,f,p = fixture(shed={'COW':1,'WHEAT':1})
    assert not any(j['op']=='ACTIVATE_COW' for j in offers(a,f,p,turn=21))


def test_do_not_steal_feed_from_an_existing_worker_obligation():
    row = dict(day=8,turn=5,worker=1,step=173,opcode='PICKUP',
               position=[4,4],arguments={'item':'WHEAT','units':1})
    a,f,p = fixture(shed={'COW':1,'WHEAT':1},rows=[row])
    job = next(j for j in offers(a,f,p) if j['op']=='ACTIVATE_COW')
    assert job['purchase'] and job['procurement']['WHEAT']==1


def test_emitting_owner_blocks_a_duplicate_same_snapshot_service():
    a,f,p = fixture()
    f['tiles'][4][4]={'kind':'PASTURE','animal':'COW','fed_today':True,
                      'cared_today':True,'fertilizer_available':True,'yield_units':0}
    a.selected=[(['COLLECT_FERTILIZER'],None)]
    assert not any(j['target']==(4,4) for j in offers(a,f,p))


@pytest.mark.parametrize('day',[1,10,20,30])
def test_carried_revenue_delivery_has_no_half_month_switch(day):
    a,f,p = fixture(day)
    p['inventories']=[{'MILK':2}]
    job = next(j for j in offers(a,f,p,day) if j['op']=='DELIVER')
    assert job['steps']==[(['DROP'],(4,4))]


def test_placement_is_not_confirmed_by_emission_alone():
    a,f,p = fixture(shed={'COW':1,'WHEAT':1})
    job = next(j for j in offers(a,f,p) if j['op']=='ACTIVATE_COW')
    job['index']=next(i for i,s in enumerate(job['steps']) if s[0][0]=='PLACE')
    job.update(emitted=True,before={'COW':1})
    a.active[job['key']]=job
    f['tiles'][4][5]={'kind':'PASTURE'}
    a._observe(8,10,f,p)
    assert not a.advanced
    job['emitted']=True
    f['tiles'][4][5]={'kind':'PASTURE','animal':'COW'}
    a._observe(8,11,f,p)
    assert (5,4) in a.advanced


def test_mission_does_not_mutate_the_observed_farm():
    a,f,p = fixture(shed={'COW':1,'WHEAT':1})
    before=deepcopy((f,p))
    offers(a,f,p)
    assert (f,p)==before


def test_early_placement_removes_only_its_own_workers_animal_pickup():
    rows = [dict(day=9,turn=2,worker=w,step=194,opcode='PICKUP',
                 position=[4,4],arguments={'item':'COW','units':1}) for w in [0,1]]
    rows.append(dict(day=9,turn=8,worker=1,step=200,opcode='PLACE',
                     position=[5,3],arguments={'animal':'COW'}))
    a,_,_ = fixture(rows=rows)
    a.advanced.add((5,3))
    a._new_day(9)
    assert any(r['opcode']=='PICKUP' for r in a.routes[(9,0)])
    assert not any(r['opcode']=='PICKUP' for r in a.routes[(9,1)])
