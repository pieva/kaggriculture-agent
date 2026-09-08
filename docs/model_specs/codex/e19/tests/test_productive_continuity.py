from types import SimpleNamespace
from docs.model_specs.codex.e19.tools.productive_continuity import install

def make_core(day=12,cash=1000):
    services=[((1,1),[['FEED'],['CARE'],['COLLECT_FERTILIZER']],2,100,'SERVICE'),
              ((2,2),[['WATER'],['FERTILIZE']],1,80,'SERVICE'),
              ((3,3),[['HARVEST']],0,50,'SERVICE')]
    return SimpleNamespace(_services=lambda:services,_day_route_certificate=lambda w,j,s:s,
        _tile=lambda t:{'crop':'WHEAT'} if t==(3,3) else {},day=day,final_day=29,
        farm={'money':cash},maintenance_floor=100)

def test_certificate_keeps_nonurgent_biological_work():
    c=make_core();install(c)
    rows=c._day_route_certificate(0,{})
    assert [r[1] for r in rows]==[[['FEED']],[['WATER']]]
    assert [r[2] for r in rows]==[2,1]
    assert ['CARE'] in c._services()[0][1]

def test_renewal_requires_time_and_observed_funds():
    for day,cash,expected in [(12,1000,True),(27,1000,False),(12,109,False)]:
        c=make_core(day,cash);install(c,True)
        assert (['PLANT','WHEAT'] in c._services()[2][1])==expected

def test_renewal_is_ordered_after_harvest():
    c=make_core();install(c,True)
    assert c._services()[2][1]==[['HARVEST'],['PLANT','WHEAT'],['WATER']]
