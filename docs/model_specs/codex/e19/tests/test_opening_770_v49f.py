from copy import deepcopy
from pathlib import Path
import runpy
import unittest
from docs.model_specs.codex.e19.tools.policy_770_v49f import adapt

ROOT=Path(__file__).resolve().parents[5]


class OpeningTests(unittest.TestCase):
    def setup_policy(self):
        real=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_v48_external.py'))['create_agent']()
        class Fake:
            teacher=real.teacher
            core=real.core
            action=None
            def __call__(self,obs,cfg):return deepcopy(self.action)
        fake=Fake()
        return fake,adapt(fake)

    def test_spawn_relocation_and_deadhead_removal_preserve_all_jobs(self):
        fake,policy=self.setup_policy()
        teacher=fake.teacher.codex_e18_capacity_governed_instance.base_policy.codex_e17_batched_cluster_routing_instance.base_policy.codex_e17_true_reactive_instance.base_policy.codex_e17_instance.base_policy.codex_v9_instance
        routine=teacher.__call__.__func__.__globals__['ROUTINE_ACTIONS']
        observed=[]
        for hour in range(24):
            fake.action=routine[24+hour]
            obs=dict(day=1,hour=hour,player=0,farms=[dict(money=22,hands=[] if hour==0 else [[5,4],[4,5],[5,5]])])
            observed.append(policy(obs,{}))
        self.assertEqual(observed[0]['market'],[['HIRE']]*3)
        self.assertEqual(observed[1]['hands'][2],['WEST'])
        self.assertEqual(observed[2]['hands'][2],['NORTH'])
        self.assertEqual([a['hands'][2] for a in observed[3:]], [a['hands'][3] for a in routine[25:46]])
        self.assertEqual(observed[11]['hands'][1],['PASS'])
        self.assertEqual(observed[13]['hands'][1],['PASS'])
        self.assertEqual(policy.delayed,[['PASS'],['PASS']])
        for worker,physical in [(0,0),(1,1),(3,2)]:
            old=[a['hands'][worker] for a in routine[25:48] if a['hands'][worker][0] not in {'NORTH','SOUTH','WEST','EAST','PASS'}]
            new=[a['hands'][physical] for a in observed[1:] if a['hands'][physical][0] not in {'NORTH','SOUTH','WEST','EAST','PASS'}]
            self.assertEqual(old,new)

    def test_incompatible_setup_keeps_original_hires(self):
        for cfg,money in [({'boardSize':12},22),({},6),({'turnsPerDay':12},22)]:
            fake,policy=self.setup_policy()
            fake.action=dict(farmer=['PASS'],hands=[],market=[['HIRE']]*4)
            obs=dict(day=1,hour=0,player=0,farms=[dict(money=money,hands=[])])
            self.assertEqual(policy(obs,cfg),fake.action)
            self.assertFalse(policy.enabled)


if __name__=='__main__':unittest.main()
