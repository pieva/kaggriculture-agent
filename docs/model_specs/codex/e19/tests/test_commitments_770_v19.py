from docs.model_specs.codex.e19.tools.commitments_770_v19 import stable_tie,commitment_rank


def test_renewal_precedes_separate_harvest():
    tile={'kind':'PLANT','consecutive_unwatered':0}
    renewal=commitment_rank(tile,[['HARVEST'],['PLANT','WHEAT'],['WATER']],'NEW_ROTATION',4,0)
    harvest=commitment_rank(tile,[['HARVEST']],'SERVICE',4,0)
    assert renewal>harvest


def test_empty_pasture_is_a_commitment_without_overriding_survival():
    fill=commitment_rank({'kind':'PASTURE'},[['PLACE','COW'],['FEED'],['CARE']],'NEW_ANIMAL',0,0)
    emergency=commitment_rank({'consecutive_unfed':1},[['FEED']],'SERVICE',3,0)
    assert emergency>fill>commitment_rank({},[['CARE']],'SERVICE',2,0)


def test_waiting_work_gets_bounded_promotion():
    old=commitment_rank({},[['PLANT','WHEAT']],'NEW_CROP',0,1000)
    assert old>commitment_rank({},[['CARE']],'SERVICE',2,0)
    assert old<commitment_rank({'consecutive_unwatered':1},[['WATER']],'SERVICE',3,0)
    assert old==commitment_rank({},[['PLANT','WHEAT']],'NEW_CROP',0,24)


def test_tie_is_repeatable_changes_seed_and_ignores_hour():
    args=(12,3,(2,5),'SERVICE',[['CARE']])
    assert stable_tie(10,*args)==stable_tie(10,*args)
    assert stable_tie(10,*args)!=stable_tie(11,*args)
    assert 0<=stable_tie(10,*args)<1


def test_jitter_cannot_cross_preceding_score_components():
    assert (8,0,-10,1,0,0)>(7,1,-1,100,48,0.9999)
    assert (5,0,-2,1,0,0)>(5,0,-3,100,48,0.9999)
