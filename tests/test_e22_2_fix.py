"""Regression checks for observed E22.2 financing, seed and storage failures."""
import copy
import runpy
import unittest
from pathlib import Path

NS = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'submission/submission_codex_e22_2_fix_v1.py'))


def observation(day, hour):
    hands = [[0, 0] for _ in NS['_PLAN'][day * 24 + hour]['hands']]
    farm = dict(farmer=[4, 4], hands=hands, hires_today=len(hands), money=10000,
                tiles=[[None for _ in range(10)] for _ in range(10)])
    return dict(day=day, hour=hour, player=0, farms=[farm],
                private=dict(shed={}, seeds={}, inventories=[{} for _ in range(len(hands) + 1)]))


class E22FixTests(unittest.TestCase):
    def call(self, obs):
        before = copy.deepcopy(obs)
        action = NS['agent'](obs, {})
        self.assertEqual(obs, before, 'The agent must not mutate observations')
        self.assertEqual(action, NS['Agent']()(obs, {}), 'Recovery must survive a fresh loader')
        self.assertLessEqual(len(action['market']), 10)
        return action

    def test_d2_finances_all_three_hires_after_farmer_pickup(self):
        obs = observation(1, 0)
        obs['farms'][0]['money'] = 3
        obs['private']['shed'] = {'WHEAT': 3}
        action = self.call(obs)
        self.assertEqual(action['market'], [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE']])
        self.assertEqual(action['farmer'], ['PICKUP', 'WHEAT'])

    def test_does_not_sell_the_unit_already_picked_up(self):
        obs = observation(1, 0)
        obs['farms'][0]['money'] = 3
        obs['private']['shed'] = {'WHEAT': 1}
        self.assertEqual(self.call(obs)['market'], [['HIRE'], ['HIRE'], ['HIRE']])

    def test_emergency_grain_sale_recovers_cow_feed_without_route_drift(self):
        obs = observation(1, 12)
        obs['farms'][0]['hands'][1] = [4, 4]
        cow = dict(kind='PASTURE', animal='COW', fed_today=False, cared_today=True)
        obs['farms'][0]['tiles'][4][4] = cow
        obs['private']['shed'] = {'WHEAT': 4}
        self.assertEqual(self.call(obs)['hands'][1], ['PICKUP', 'WHEAT', 2])
        obs['hour'] = 13
        obs['private']['inventories'][2] = {'WHEAT': 2}
        self.assertEqual(self.call(obs)['hands'][1], ['FEED'])
        obs['hour'] = 14
        cow['fed_today'] = True
        obs['private']['inventories'][2] = {'WHEAT': 1}
        self.assertEqual(self.call(obs)['hands'][1], ['WEST'])

    def test_weed_is_removed_then_planting_retried(self):
        obs = observation(7, 16)
        obs['farms'][0]['hands'][6] = [9, 2]
        obs['farms'][0]['tiles'][2][9] = {'kind': 'WEED'}
        obs['private']['seeds'] = {'STRAWBERRY': 10}
        self.assertEqual(self.call(obs)['hands'][6], ['DIG'])
        obs['hour'] += 1
        obs['farms'][0]['tiles'][2][9] = None
        self.assertEqual(self.call(obs)['hands'][6], ['PLANT', 'STRAWBERRY'])

    def test_idle_slot_clears_weed_before_scheduled_plant_and_water(self):
        obs = observation(7, 15)
        obs['farms'][0]['hands'][6] = [9, 2]
        obs['farms'][0]['tiles'][2][9] = {'kind': 'WEED'}
        self.assertEqual(self.call(obs)['hands'][6], ['DIG'])
        obs['hour'] = 16
        obs['farms'][0]['tiles'][2][9] = None
        obs['private']['seeds'] = {'STRAWBERRY': 10}
        self.assertEqual(self.call(obs)['hands'][6], ['PLANT', 'STRAWBERRY'])
        obs['hour'] = 17
        obs['farms'][0]['tiles'][2][9] = dict(kind='PLANT', crop='STRAWBERRY', watered_today=False)
        self.assertEqual(self.call(obs)['hands'][6], ['WATER'])

    def test_seed_shortfall_keeps_affordable_plants_instead_of_atomic_failure(self):
        obs = observation(0, 15)
        obs['private']['seeds'] = {'MELON': 1}
        action = self.call(obs)
        self.assertEqual(sum(c[:2] == ['PLANT', 'MELON'] for c in [action['farmer']] + action['hands']), 1)

    def test_overflow_sales_preserve_feeding_reserve(self):
        obs = observation(25, 23)
        obs['private']['shed'] = {'WHEAT': 70, 'WOOL': 7}
        obs['private']['inventories'][0] = {'WOOL': 40}
        action = self.call(obs)
        sold = sum(c[2] for c in action['market'] if len(c) > 2 and c[0] == 'SELL')
        wheat = sum(c[2] for c in action['market'] if len(c) > 2 and c[:2] == ['SELL', 'WHEAT'])
        self.assertGreaterEqual(sold, 17)
        self.assertLessEqual(wheat, 46)

    def test_final_idle_worker_delivers_fertilizer_and_sells_it(self):
        obs = observation(29, 22)
        obs['farms'][0]['hands'][7] = [5, 4]
        obs['private']['inventories'][8] = {'FERTILIZER': 1}
        action = self.call(obs)
        self.assertEqual(action['hands'][7], ['DROP'])
        self.assertIn(['SELL', 'FERTILIZER', 1000], action['market'])

    def test_d16_wheat_replant_finishes_with_watering(self):
        obs = observation(15, 21)
        obs['farms'][0]['hands'][9] = [9, 0]
        obs['farms'][0]['tiles'][0][9] = dict(kind='PLANT', crop='WHEAT', planted_day=12, yield_units=2, watered_today=False)
        action = self.call(obs)
        self.assertEqual(action['hands'][9], ['HARVEST'])
        self.assertEqual(sum(c[2] for c in action['market'] if c[:2] == ['BUY_SEED', 'WHEAT']), 2)
        obs['hour'] = 22
        obs['farms'][0]['tiles'][0][9] = None
        obs['private']['seeds'] = {'WHEAT': 3}
        action = self.call(obs)
        self.assertEqual(action['hands'][9], ['PLANT', 'WHEAT'])
        self.assertFalse(any(c[:2] == ['BUY_SEED', 'WHEAT'] for c in action['market']))
        obs['hour'] = 23
        obs['farms'][0]['tiles'][0][9] = dict(kind='PLANT', crop='WHEAT', planted_day=15, yield_units=1, watered_today=False)
        self.assertEqual(self.call(obs)['hands'][9], ['WATER'])

    def test_strawberry_is_watered_before_day_without_a_visit(self):
        obs = observation(20, 9)
        obs['farms'][0]['hands'][6] = [8, 2]
        obs['farms'][0]['tiles'][2][8] = dict(kind='PLANT', crop='STRAWBERRY', planted_day=6, yield_units=2, watered_today=False)
        self.assertEqual(self.call(obs)['hands'][6], ['WATER'])


if __name__ == '__main__':
    unittest.main()
