from copy import deepcopy
from types import SimpleNamespace

from docs.model_specs.codex.e19.tools.assisted_start import AssistedStart


class FakeCore:
    def __init__(self, capacity=6):
        self.seat=0
        self.bootstrap_done=False
        self.calls=0
        self.profile=SimpleNamespace(pasture_budgets=lambda order:{q:capacity for q in order})
    def __call__(self,obs,cfg):
        self.calls+=1
        assert self.bootstrap_done
        return {'farmer':['PASS'],'hands':[],'market':[]}


def observation():
    tiles=[[None for _ in range(10)] for _ in range(10)]
    for x in range(5):tiles[0][x]={'kind':'PASTURE'}
    return {'day':6,'hour':2,'farms':[{'tiles':tiles,'farmer':[0,1],
            'hands':[[1,1]],'unlocked_quadrants':['NW']}]}


def test_simultaneous_builds_reserve_capacity_without_mutating_teacher():
    action={'farmer':['BUILD_PASTURE'],'hands':[['BUILD_PASTURE']],'market':[]}
    policy=AssistedStart(lambda *args:action,FakeCore())
    obs=observation();before=deepcopy(obs)
    result=policy(obs,{})
    assert result['farmer']==['BUILD_PASTURE']
    assert result['hands']==[['PASS']]
    assert action['hands']==[['BUILD_PASTURE']]
    assert obs==before


def test_capacity_is_parameterized():
    action={'farmer':['BUILD_PASTURE'],'hands':[['BUILD_PASTURE']],'market':[]}
    policy=AssistedStart(lambda *args:action,FakeCore(7))
    assert policy(observation(),{})==action


def test_handover_is_after_all_d11_actions_and_never_restarts_bootstrap():
    calls=[]
    def teacher(obs,cfg):
        calls.append(obs['day'])
        return {'farmer':['WATER'],'hands':[],'market':[]}
    core=FakeCore();policy=AssistedStart(teacher,core)
    obs=observation();obs.update(day=10,hour=23)
    assert policy(obs,{})['farmer']==['WATER']
    assert core.calls==0
    obs.update(day=11,hour=0)
    policy(obs,{});policy(obs,{})
    assert calls==[10] and core.calls==2 and core.bootstrap_done
    assert sum(e['event']=='HANDOVER' for e in policy.events)==1
