"""Focused original-engine trace for the D2 feed regression, not a new cohort."""
import json
from pathlib import Path
from copy import deepcopy

from kaggle_environments import make
from docs.model_specs.codex.e18.tools.e18_31_unified_investment_controller import UnifiedInvestmentController
from docs.model_specs.codex.e18.tools.e18_32_reservation_routing_controller import ReservationRoutingController
from docs.model_specs.codex.e18.tools.run_e18_30_mission_gate import PLAN,opponent_policy,DERIVED


def run(base):
    agent=base(json.loads(PLAN.read_text()),0)
    trace=[]
    def policy(obs,config):
        result=agent(obs,config)
        if obs['day']==1:
            trace.append(dict(hour=obs['hour']+1,money=obs['farms'][0]['money'],
                positions=[obs['farms'][0]['farmer'],*obs['farms'][0]['hands']],
                private=deepcopy(obs['private']),action=result,
                rows={str(w):deepcopy(agent._remaining_rows(2,w)[:2]) for w in range(len(obs['farms'][0]['hands'])+1)}))
        return result
    env=make('kaggriculture',configuration={'seed':180903001,'episodeSteps':720,'turnsPerDay':24},debug=False)
    env.run([policy,opponent_policy('E18.16',180903001,1)])
    return dict(controller=base.__name__,trace=trace)


if __name__=='__main__':
    result=[run(UnifiedInvestmentController),run(ReservationRoutingController)]
    target=DERIVED/'E18_32_D2_FEED_TRACE_20260906.json'
    assert not target.exists()
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    for case in result:
        print(case['controller'])
        for t in case['trace']:
            print(t['hour'],t['money'],t['private']['shed'].get('WHEAT',0),t['action'],flush=True)
