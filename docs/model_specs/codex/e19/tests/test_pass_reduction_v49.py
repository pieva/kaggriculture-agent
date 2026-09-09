"""Biological boundaries and isolated runtime installation regression tests."""
from pathlib import Path
import runpy
import unittest
from docs.model_specs.codex.e19.tools.local_service_770_v49 import useful_commands
from docs.model_specs.codex.e19.tools.workload_770_v49 import sowing_has_horizon, install

ROOT=Path(__file__).resolve().parents[5]


class PassReductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory=staticmethod(runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_v48_external.py'))['create_agent'])
        cls.rules=cls.factory().core.__call__.__func__.__globals__

    def useful(self,tile,cmds,day):
        return useful_commands(tile,cmds,day,29,self.rules,lambda item,side,n:n*10)

    def test_no_hiring_for_impossible_sowing_horizon(self):
        crops=self.rules['CROPS']
        self.assertTrue(sowing_has_horizon(27,29,list(crops),crops))
        self.assertFalse(sowing_has_horizon(28,29,list(crops),crops))
        self.assertTrue(sowing_has_horizon(28,30,['WHEAT'],crops))
        self.assertFalse(sowing_has_horizon(22,29,['STRAWBERRY'],crops))

    def test_spent_perennial_and_fertilizer_collection_are_not_work(self):
        tile=dict(kind='PLANT',crop='STRAWBERRY',planted_day=0,yield_units=0,
                  watered_today=False,consecutive_unwatered=1)
        self.assertEqual(self.useful(tile,[['WATER'],['FERTILIZE'],['COLLECT_FERTILIZER']],20),[])

    def test_critical_growing_plant_gets_water_without_premature_harvest(self):
        tile=dict(kind='PLANT',crop='WHEAT',planted_day=12,yield_units=1,
                  watered_today=False,consecutive_unwatered=1)
        self.assertEqual(self.useful(tile,[['WATER'],['HARVEST']],13),[['WATER']])

    def test_terminal_water_requires_collectable_visit(self):
        tile=dict(kind='PLANT',crop='WHEAT',planted_day=25,yield_units=4,
                  watered_today=False,consecutive_unwatered=1)
        self.assertEqual(self.useful(tile,[['WATER']],29),[])
        self.assertEqual(self.useful(tile,[['WATER'],['HARVEST']],29),[['WATER'],['HARVEST']])

    def test_care_requires_feed_and_future_bonus(self):
        tile=dict(kind='PASTURE',animal='COW',placed_day=0,yield_units=0,
                  fed_today=False,cared_today=False,pending_care_bonus=0)
        self.assertEqual(self.useful(tile,[['CARE']],12),[])
        self.assertEqual(self.useful(tile,[['FEED'],['CARE']],12),[['FEED'],['CARE']])
        self.assertEqual(self.useful(tile,[['FEED'],['CARE']],29),[])

    def test_install_preserves_engine_namespace_and_baseline_instance(self):
        baseline=self.factory();candidate=self.factory()
        baseline_type=type(baseline.core)
        install(candidate.core)
        self.assertEqual(candidate.core.__call__.__func__.__globals__['CROPS'],self.rules['CROPS'])
        self.assertIs(type(baseline.core),baseline_type)
        self.assertNotEqual(type(candidate.core),baseline_type)
        self.assertFalse(hasattr(baseline.core,'v49_recovery_log'))

    def test_d_preserves_dispatcher_services_and_reservations(self):
        from docs.model_specs.codex.e19.tools.workload_770_v49d import install as install_d
        core=self.factory().core
        before=(type(core),core._prepare_steps,core._services,core._day_route_certificate)
        install_d(core)
        after=(type(core),core._prepare_steps,core._services,core._day_route_certificate)
        self.assertEqual(before,after)
        self.assertFalse(hasattr(core,'v49_recovery_log'))


if __name__=='__main__':unittest.main()
