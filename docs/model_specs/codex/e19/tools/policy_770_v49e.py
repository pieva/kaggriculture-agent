"""770 opening: remove a paid worker with no scheduled work in frozen D2.

The logical fourth hand becomes physical hand three for this one day. No
synthetic observations or assumed future game states are given to the policy.
"""
from docs.model_specs.codex.e19.tools.daily_route_scheduler_770_v48 import install


class OpeningWithoutIdleHand:
    def __init__(self,policy):
        self.policy=policy
        self.enabled=False
        teacher=policy.teacher.codex_e18_capacity_governed_instance.base_policy.codex_e17_batched_cluster_routing_instance.base_policy.codex_e17_true_reactive_instance.base_policy.codex_e17_instance.base_policy.codex_v9_instance
        routine=teacher.__call__.__func__.__globals__['ROUTINE_ACTIONS']
        assert routine[24]['market']==[['HIRE']]*4
        assert all(len(a['hands'])==4 and a['hands'][2]==['PASS'] for a in routine[25:48])

    def __getattr__(self,name):return getattr(self.policy,name)

    def __call__(self,observation,configuration):
        action=self.policy(observation,configuration)
        if observation['day']!=1:return action
        if observation['hour']==0:
            farm=observation['farms'][observation['player']]
            self.enabled=(configuration.get('turnsPerDay',24)==24
                and configuration.get('boardSize',10)==10
                and configuration.get('episodeSteps',720)==720
                and not farm['hands'] and farm['money']>=7*configuration.get('farmHandCostMult',1)
                and action['market']==[['HIRE']]*4 and not action['hands'])
            if self.enabled:return dict(action,market=[['HIRE']]*3)
        elif self.enabled:
            # The removed logical worker is dormant for all remaining D2 ticks.
            # Fail visibly if the frozen routine/overrides ever contradict this.
            assert len(action['hands'])==4 and action['hands'][2]==['PASS']
            assert len(observation['farms'][observation['player']]['hands'])==3
            return dict(action,hands=action['hands'][:2]+action['hands'][3:])
        return action


def adapt(policy):return OpeningWithoutIdleHand(policy)
