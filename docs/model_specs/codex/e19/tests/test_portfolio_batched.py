import runpy
from pathlib import Path
from docs.model_specs.codex.e19.tools.portfolio_batched import install


def test_combined_service_keeps_short_fallback_and_counts_feed_once():
    root=Path(__file__).resolve().parents[5]
    core=runpy.run_path(str(root/'submission/submission_codex_e19_control_770_v2.py'))['create_agent']({'player_position':0})
    core.__class__=type('CertificateProbe',(core.__class__,),{'_day_route_certificate':lambda self,w,j,s:s})
    core._services=lambda:[((0,0),[['FEED'],['CARE'],['HARVEST']],3,200,'SERVICE')]
    core._quote=lambda c,op,n:10*n
    core.day=12
    core.final_day=29
    core.active={}
    core.farm={'tiles':[[{'kind':'PASTURE','animal':'COW','yield_units':2}]]}
    install(core)
    offers=core._services()
    biological=[r for r in offers if r[4]=='BIOLOGICAL']
    assert [r[1] for r in biological]==[[['FEED'],['CARE'],['HARVEST']],[['FEED']]]
    assert len(core._day_route_certificate(0,{},offers))==1
    assert core._day_route_certificate(0,{},offers)[0][1]==[['FEED']]
