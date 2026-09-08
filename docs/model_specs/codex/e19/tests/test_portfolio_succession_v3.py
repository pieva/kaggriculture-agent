from docs.model_specs.codex.e19.tools.portfolio_succession_v3 import succession_options


def annual(first, last, seed=0):
    return dict(seed=seed,first_yield_day=first,max_yield_day=last,
                interval=0,max_yield=1,ongoing=False)


def test_two_short_cycles_beat_one_larger_receipt():
    rules={'SHORT':annual(1,1),'LONG':annual(3,3)}
    rows=succession_options(0,3,rules,lambda c,d,n: n*(10 if c=='SHORT' else 17),0)
    assert rows['SHORT']['total']==20
    assert rows['SHORT']['continuation']==10
    assert rows['LONG']['total']==17
    assert rows['SHORT']['admission_value']>rows['LONG']['admission_value']


def test_horizon_excludes_unharvestable_crop_and_no_future_credit():
    rows=succession_options(8,9,{'SHORT':annual(1,1),'LONG':annual(3,3)},lambda c,d,n:10*n,0)
    assert set(rows)=={'SHORT'}
    assert rows['SHORT']['end']==9 and rows['SHORT']['continuation']==0
    assert succession_options(9,9,{'SHORT':annual(1,1)},lambda *args:1000,0)=={}


def test_future_production_date_changes_best_successor():
    rules={'A':annual(1,1),'B':annual(1,1)}
    def quote(c,d,n):
        return n*(20 if (c=='A' and d==1) or (c=='B' and d==3) else 1)
    rows=succession_options(0,3,rules,quote,0)
    assert rows['A']['total']==40 and rows['A']['continuation']==20


def test_recurring_work_can_make_a_cycle_uneconomic():
    rows=succession_options(0,3,{'A':annual(3,3,seed=10)},lambda c,d,n:20*n,2)
    assert rows['A']['gain']<0 and rows['A']['admission_value']<0


def test_ongoing_crop_may_exit_before_its_last_biological_production():
    rules={'BERRY':dict(seed=0,first_yield_day=1,max_yield_day=1,interval=2,max_yield=3,ongoing=True),
           'ROOT':annual(1,1)}
    def quote(c,d,n):
        return n*(20 if c=='BERRY' and d==1 else 50 if c=='ROOT' and d==3 else 0)
    rows=succession_options(0,5,rules,quote,0)
    assert rows['BERRY']['end']==1
    assert rows['BERRY']['continuation']==50


def test_scheduled_early_harvest_remains_visible_after_water():
    import runpy
    from pathlib import Path
    from docs.model_specs.codex.e19.tools.portfolio_succession_v3 import install
    root=Path(__file__).resolve().parents[5]
    core=runpy.run_path(str(root/'submission/submission_codex_e19_control_770_v2.py'))['create_agent']({'player_position':0})
    core._services=lambda:[]
    core._quote=lambda c,op,n:10*n
    install(core)
    core.day=2
    core.active={}
    core.farm={'tiles':[[{'kind':'PLANT','crop':'WHEAT','planted_day':0,'yield_units':2,'watered_today':True}]]}
    core.portfolio_planted_ends[((0,0),0)]=2
    assert core._services()==[((0,0),[['HARVEST']],0,20,'SERVICE')]
    core.active={0:{'kind':'SERVICE','target':(0,0)}}
    assert core._services()==[]


def test_fertilizer_requires_positive_incremental_value():
    rules={'BERRY':dict(seed=0,first_yield_day=1,max_yield_day=1,interval=2,max_yield=2,ongoing=True)}
    def cheap(c,d,n):return n*(5 if c=='FERTILIZER' else 10)
    def expensive(c,d,n):return n*(100 if c=='FERTILIZER' else 10)
    good=succession_options(0,3,rules,cheap,0)['BERRY']
    bad=succession_options(0,3,rules,expensive,0)['BERRY']
    assert good['fertilizer_cost']>0 and good['revenue']==40
    assert bad['fertilizer_cost']==0 and bad['total']==20
