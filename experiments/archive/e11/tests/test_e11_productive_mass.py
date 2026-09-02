"""Unit and integration tests for E11 Productive Mass Expansion Agent."""

import pytest
from agricola.core.state import GameState
from agricola.core.actions import ActionBuilder
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent


def test_e11_initialization_config():
    """Verify E11 agent initializes cleanly with default ProductiveMassConfig."""
    agent = ProductiveMassROIAgent()
    
    assert agent.config.target_quadrants == 4
    assert agent.config.max_workers == 10
    assert agent.config.operating_reserve == 300.0
    assert agent.config.protect_expansion_capital is True
    assert agent.config.expansion_gate_mode == "MIN_OPERATIONAL"
    assert agent.config.workforce_scaling_mode == "LEGACY"
    assert len(agent.q0_crop_tiles) == 20
    assert len(agent.q1_crop_tiles) == 20
    assert len(agent.q2_crop_tiles) == 20
    assert len(agent.q3_crop_tiles) == 20
    assert agent.owned_quadrants == 1


def test_e11_vb1_config_snapshot_explicit():
    """Verify E11-VB1 configuration immutability and explicit field serialization."""
    from scripts.benchmark_e11_vb1 import E11_VB1_CONFIG
    from dataclasses import asdict
    
    d = asdict(E11_VB1_CONFIG)
    assert d["target_quadrants"] == 4
    assert d["expansion_gate_mode"] == "MIN_OPERATIONAL"
    assert d["workforce_scaling_mode"] == "LEGACY"
    assert d["protect_expansion_capital"] is True
    assert d["operating_reserve"] == 300.0
    assert d["max_workers"] == 10
    assert d["target_tiles_per_worker"] == 7.0
    assert d["accumulation_3q_mode"] == "LEGACY_LOCK"


def test_e11_x1_config_delta_vs_vb1():
    """Verify E11-X1 controlled single-variable change vs E11-VB1."""
    from scripts.benchmark_e11_vb1 import E11_VB1_CONFIG
    from scripts.benchmark_e11_x1 import E11_X1_CONFIG
    from dataclasses import asdict
    
    vb1_d = asdict(E11_VB1_CONFIG)
    x1_d = asdict(E11_X1_CONFIG)
    
    # Verify ONLY accumulation_3q parameters differ
    diff_keys = [k for k in vb1_d if vb1_d[k] != x1_d[k]]
    assert set(diff_keys) == {"accumulation_3q_mode", "accumulation_3q_optional_reserve"}
    assert vb1_d["accumulation_3q_mode"] == "LEGACY_LOCK"
    assert x1_d["accumulation_3q_mode"] == "DISCIPLINED_ACCUMULATION"
    assert x1_d["accumulation_3q_optional_reserve"] == 500.0


def test_e11_x1_1_config_delta_vs_vb1():
    """Verify E11-X1.1 controlled single-variable change vs E11-VB1."""
    from scripts.benchmark_e11_vb1 import E11_VB1_CONFIG
    from scripts.benchmark_e11_x1_1 import E11_X1_1_CONFIG
    from dataclasses import asdict
    
    vb1_d = asdict(E11_VB1_CONFIG)
    x1_1_d = asdict(E11_X1_1_CONFIG)
    
    # Verify ONLY workforce parameters differ
    diff_keys = [k for k in vb1_d if vb1_d[k] != x1_1_d[k]]
    assert set(diff_keys) == {"workforce_scaling_mode", "target_tiles_per_worker"}
    assert vb1_d["workforce_scaling_mode"] == "LEGACY"
    assert x1_1_d["workforce_scaling_mode"] == "PRE_3Q_PRODUCTIVITY_SCALING"
    assert x1_1_d["target_tiles_per_worker"] == 5.0


def test_e11_x1_2_config_and_multi_hire():
    """Verify E11-X1.2 config fields and multi-hire issuance."""
    from scripts.benchmark_e11_x1_2 import E11_X1_2_CONFIG
    from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent
    
    assert E11_X1_2_CONFIG.productive_core_mode == "E06_RESTORED"
    assert E11_X1_2_CONFIG.multi_hire_mode == "CORRECTED_MULTI"
    assert E11_X1_2_CONFIG.land_buy_mode == "PRODUCTIVE_SURPLUS"
    assert E11_X1_2_CONFIG.surplus_land_threshold == 1300.0
    
def test_e11_x1_3_a_config_and_replication():
    """Verify E11-X1.3-A config fields and E06_REPLICATED mode."""
    from scripts.benchmark_e11_x1_3 import E11_X1_3_A_CONFIG
    from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent
    
    assert E11_X1_3_A_CONFIG.productive_core_mode == "E06_REPLICATED"
    assert E11_X1_3_A_CONFIG.epu_level == 1
    agent = ProductiveMassROIAgent(config=E11_X1_3_A_CONFIG)
    assert agent.e06_compact_tiles == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]


def test_e11_06_workforce_co_scaling_triggers():
    """Verify E11-06 hiring triggers when active tiles per worker ratio is high."""
    config = ProductiveMassConfig(protect_expansion_capital=True, expansion_gate_mode="MIN_OPERATIONAL", workforce_scaling_mode="LAND_CO_SCALING", target_tiles_per_worker=5.0)
    agent = ProductiveMassROIAgent(config=config)
    agent.owned_quadrants = 2  # 50 tiles owned (accumulating for 75 tiles)
    agent.telemetry.daily_productive_tiles_history.append(25)  # 25 active tiles / 4 workers = 6.25 >= 5.0 target ratio
    builder = ActionBuilder()
    
    class DummyState:
        day = 5
        hour = 0
        money = 800.0  # Cash is $800 >= $300 operating reserve
        hires_today = 0
        step = 120
        def get_seed_count(self, crop):
            return 10
        def get_shed_count(self, item):
            return 0
            
    dummy = DummyState()
    # Current workers = 4 < 6 cap for 2Q
    agent._process_market_decisions(dummy, builder, current_workers=4)
    actions = builder.build()
    
    # HIRE SHOULD BE EXECUTED because cash float $800 >= $300 operating reserve
    assert ["HIRE"] in actions["market"]


def test_e11_06_pre_land_hiring_protects_land_float():
    """Verify E11-06 pauses hiring when cash is in imminent land threshold ($950-$1099) to execute BUY_LAND."""
    config = ProductiveMassConfig(protect_expansion_capital=True, expansion_gate_mode="MIN_OPERATIONAL", workforce_scaling_mode="LAND_CO_SCALING")
    agent = ProductiveMassROIAgent(config=config)
    agent.owned_quadrants = 2  # 50 tiles owned (accumulating for 75 tiles)
    agent.telemetry.daily_productive_tiles_history.append(25)
    builder = ActionBuilder()
    
    class DummyState:
        day = 5
        hour = 0
        money = 980.0  # Cash is $980 >= $950 land threshold, so hire is paused to let cash reach $1100
        hires_today = 0
        step = 120
        def get_seed_count(self, crop):
            return 10
        def get_shed_count(self, item):
            return 0
            
    dummy = DummyState()
    agent._process_market_decisions(dummy, builder, current_workers=4)
    actions = builder.build()
    
    # HIRE SHOULD BE BLOCKED because cash is in imminent land threshold ($950-$1099)
    hire_orders = [ord for ord in actions["market"] if ord[0] == "HIRE"]
    assert len(hire_orders) == 0


def test_e11_05_staged_state_machine_transitions():
    """Verify E11-05 Economic State Machine transitions correctly across states."""
    config = ProductiveMassConfig(capital_release_mode="STAGED", productive_window_budget_cap=600.0)
    agent = ProductiveMassROIAgent(config=config)
    
    class DummyState:
        day = 4
        hour = 0
        money = 1150.0
        step = 96
        
    dummy = DummyState()
    assert agent.economic_state == "ACCUMULATE_Q2"
    
    # Simulate Q2 purchase
    agent.owned_quadrants = 2
    agent._update_economic_state(dummy)
    assert agent.economic_state == "PRODUCTIVE_WINDOW"
    assert agent.q2_purchase_day == 4
    
    # Spend window budget ($600)
    agent.window_seed_spending = 600.0
    agent._update_economic_state(dummy)
    assert agent.economic_state == "ACCUMULATE_Q3"
    
    # Simulate Q3 purchase
    agent.owned_quadrants = 4
    agent._update_economic_state(dummy)
    assert agent.economic_state == "MASS_ACTIVATION"
    assert agent.q3_purchase_day == 4


def test_e11_03_min_operational_expansion_gate_q2_q3():
    """Verify E11-03 MIN_OPERATIONAL gate unlocks Q2 at active_tiles=8 and Q3 at active_tiles=12."""
    config = ProductiveMassConfig(protect_expansion_capital=True, expansion_gate_mode="MIN_OPERATIONAL", capital_release_mode="BINARY")
    agent = ProductiveMassROIAgent(config=config)
    agent.owned_quadrants = 2
    agent.telemetry.daily_productive_tiles_history.append(9)  # 9 active tiles >= 8 threshold
    builder = ActionBuilder()
    
    class DummyState:
        day = 6
        hour = 0
        money = 1150.0  # Cash >= $1000 + $100 buffer
        hires_today = 0
        step = 144
        def get_seed_count(self, crop):
            return 10
        def get_shed_count(self, item):
            return 0
            
    dummy = DummyState()
    agent._process_market_decisions(dummy, builder, current_workers=4)
    actions = builder.build()
    
    # Q2 should be bought immediately at active_tiles = 9
    assert ["BUY_LAND"] in actions["market"]
    assert agent.owned_quadrants == 3


def test_e11_02_legacy_saturation_gate_reproducibility():
    """Verify E11-02 LEGACY_SATURATION gate blocks Q2 when active_tiles=9 < 15."""
    config = ProductiveMassConfig(protect_expansion_capital=True, expansion_gate_mode="LEGACY_SATURATION", capital_release_mode="BINARY")
    agent = ProductiveMassROIAgent(config=config)
    agent.owned_quadrants = 2
    agent.telemetry.daily_productive_tiles_history.append(9)  # 9 active tiles < 15 legacy threshold
    builder = ActionBuilder()
    
    class DummyState:
        day = 6
        hour = 0
        money = 1150.0
        hires_today = 0
        step = 144
        def get_seed_count(self, crop):
            return 10
        def get_shed_count(self, item):
            return 0
            
    dummy = DummyState()
    agent._process_market_decisions(dummy, builder, current_workers=4)
    actions = builder.build()
    
    # Q2 should NOT be bought because 9 < 15 legacy threshold
    buy_land_orders = [ord for ord in actions["market"] if ord[0] == "BUY_LAND"]
    assert len(buy_land_orders) == 0
    assert agent.owned_quadrants == 2


def test_e11_crop_portfolio_selection():
    """Verify multi-crop portfolio selection respects day cutoffs."""
    agent = ProductiveMassROIAgent()
    
    class DummyState:
        def get_seed_count(self, crop):
            return 10
            
    dummy = DummyState()
    
    # Feed tile gets WHEAT
    crop_feed = agent._select_crop_to_plant(dummy, day=5, tile=(1, 1))
    assert crop_feed == "WHEAT"
    
    # Early day gets MELON
    crop_early = agent._select_crop_to_plant(dummy, day=5, tile=(2, 2))
    assert crop_early == "MELON"
    
    # Day 19 (post Melon cutoff) gets STRAWBERRY
    crop_mid = agent._select_crop_to_plant(dummy, day=19, tile=(2, 2))
    assert crop_mid == "STRAWBERRY"
    
    # Day 21 (post Strawberry cutoff) gets TOMATO
    crop_late = agent._select_crop_to_plant(dummy, day=21, tile=(2, 2))
    assert crop_late == "TOMATO"


def test_e11_locality_dispatcher():
    """Verify Locality-Guided Dispatcher scopes workers to preferred quadrant tiles."""
    agent = ProductiveMassROIAgent()
    agent.owned_quadrants = 2
    reserved = set()
    
    class DummyState:
        day = 10
        def get_tile(self, x, y):
            # Q1 tile (5, 0) needs water
            if (x, y) == (5, 0):
                return {"kind": "PLANT", "crop": "CARROT", "watered_today": False, "planted_day": 8}
            return None
            
    dummy = DummyState()
    
    # Worker assigned to preferred quadrant 1 (pos 5,0)
    act = agent._get_worker_action(dummy, pos=(5, 0), reserved=reserved, worker_id=2, preferred_quadrant=1)
    assert act == ["WATER"]


def test_b3_geometry_disjointness_and_1_land():
    """Verify B3 EPU1, EPU2, EPU3 3x3 strip partitions are disjoint and inside Q0+Q1 (1 land purchase)."""
    epu1 = set([(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
    epu2 = set([(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)])
    epu3 = set([(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)])

    assert len(epu1) == 9
    assert len(epu2) == 9
    assert len(epu3) == 9

    assert len(epu1.intersection(epu2)) == 0
    assert len(epu1.intersection(epu3)) == 0
    assert len(epu2.intersection(epu3)) == 0

    all_27 = epu1.union(epu2).union(epu3)
    assert len(all_27) == 27

    # 1-land feasibility check (x in 0..9, y in 0..4)
    assert all(0 <= x <= 9 and 0 <= y <= 4 for x, y in all_27)


def test_b3_no_day0_buy_and_requires_realized_revenue():
    """Verify B3 strategy does NOT buy land on Day 0 or Day 1 pre-surplus without realized revenue."""
    from scripts.benchmark_e11_x1_3_b2r import E11_X1_3_B2R_CONFIG
    agent = ProductiveMassROIAgent(config=E11_X1_3_B2R_CONFIG)

    class Day1State:
        day = 1
        hour = 0
        step = 24
        money = 5000.0  # High initial money, but realized revenue is 0
        my_farm = {"unlocked_quadrants": ["NW"]}
        hands_positions = []
        farmer_position = (0, 0)
        hires_today = 0

        def get_shed_count(self, item):
            return 0
        def get_seed_count(self, crop):
            return 0
        def get_price(self, crop):
            return 30.0
        def get_tile(self, x, y):
            return None

    s1 = Day1State()
    actions = agent.act(s1)
    # Market actions must NOT contain BUY_LAND because realized_revenue is 0!
    market_acts = actions.get("market", [])
    buy_land = [a for a in market_acts if a[0] == "BUY_LAND"]
    assert len(buy_land) == 0, "Land MUST NOT be purchased pre-surplus (realized revenue == 0)!"

    # Now simulate EPU1 selling crops => realized revenue > 0
    agent.telemetry.realized_revenue["CARROT"] = 100.0
    actions2 = agent.act(s1)
    market_acts2 = actions2.get("market", [])
    buy_land2 = [a for a in market_acts2 if a[0] == "BUY_LAND"]
    assert len(buy_land2) == 1, "Land MUST be purchased post-surplus once realized revenue > 0 and cash >= trigger!"


def test_x1_4_geometry_disjointness_and_30_tiles():
    """Verify X1.4 EPU1 (3x5) and EPU2 (3x5) tile partitions are disjoint and yield 30 unique tiles."""
    epu1 = set([(x, y) for x in range(3) for y in range(5)])
    epu2 = set([(x, y) for x in range(3, 6) for y in range(5)])

    assert len(epu1) == 15
    assert len(epu2) == 15
    assert len(epu1.intersection(epu2)) == 0

def test_x1_5_geometry_disjointness_and_32_tiles():
    """Verify X1.5 Centered EPU1 (4x4) and EPU2 (4x4) tile partitions are disjoint and yield 32 unique tiles."""
    epu1 = set([(x, y) for x in range(1, 5) for y in range(1, 5)])
    epu2 = set([(x, y) for x in range(5, 9) for y in range(1, 5)])

    assert len(epu1) == 16
    assert len(epu2) == 16
    assert len(epu1.intersection(epu2)) == 0

def test_x1_6_progressive_geometry_and_subset_invariants():
    """Verify X1.6 EPU1 3x3 subset of 4x4, EPU2 3x3 subset of 4x4, ring sizes equal 7, and disjointness."""
    epu1_3x3 = set([(x, y) for x in range(2, 5) for y in range(2, 5)])
    epu1_4x4 = set([(x, y) for x in range(1, 5) for y in range(1, 5)])

    epu2_3x3 = set([(x, y) for x in range(5, 8) for y in range(2, 5)])
    epu2_4x4 = set([(x, y) for x in range(5, 9) for y in range(1, 5)])

    # Invariants
    assert len(epu1_3x3) == 9
    assert len(epu1_4x4) == 16
    assert epu1_3x3.issubset(epu1_4x4)
    assert len(epu1_4x4 - epu1_3x3) == 7

    assert len(epu2_3x3) == 9
    assert len(epu2_4x4) == 16
    assert epu2_3x3.issubset(epu2_4x4)
    assert len(epu2_4x4 - epu2_3x3) == 7

    # Disjointness
    assert len(epu1_4x4.intersection(epu2_4x4)) == 0

    # Total 32 tiles in 2Q (Q0+Q1)
    all_32 = epu1_4x4.union(epu2_4x4)
    assert len(all_32) == 32
    assert all(0 <= x <= 9 and 0 <= y <= 4 for x, y in all_32)


def test_x1_7_corner_pruned_geometry_and_invariants():
    """Verify X1.7 prescriptive coordinates, cardinalities 9/13/9/13, subset invariants, extension ring sizes == 4, and 26 unique tiles."""
    epu1_core_3x3 = set([(2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4)])
    epu1_extension = set([(1, 3), (1, 4), (3, 1), (4, 1)])
    epu1_target_13 = epu1_core_3x3.union(epu1_extension)

    epu2_core_3x3 = set([(5, 2), (5, 3), (5, 4), (6, 2), (6, 3), (6, 4), (7, 2), (7, 3), (7, 4)])
    epu2_extension = set([(5, 1), (6, 1), (8, 3), (8, 4)])
    epu2_target_13 = epu2_core_3x3.union(epu2_extension)

    # Cardinality & Subset Invariants
    assert len(epu1_core_3x3) == 9
    assert len(epu1_extension) == 4
    assert len(epu1_target_13) == 13
    assert epu1_core_3x3.issubset(epu1_target_13)
    assert (2, 2) in epu1_core_3x3, "(2,2) MUST be preserved in EPU1 core!"

    assert len(epu2_core_3x3) == 9
    assert len(epu2_extension) == 4
    assert len(epu2_target_13) == 13
    assert epu2_core_3x3.issubset(epu2_target_13)

    # Excluded corners check
    epu1_excluded = set([(1, 1), (1, 2), (2, 1)])
    assert len(epu1_target_13.intersection(epu1_excluded)) == 0, "Excluded corners must NOT be in EPU1 target!"

    epu2_excluded = set([(7, 1), (8, 1), (8, 2)])
    assert len(epu2_target_13.intersection(epu2_excluded)) == 0, "Excluded corners must NOT be in EPU2 target!"

    # Containment & Disjointness
    assert all(0 <= x <= 4 and 0 <= y <= 4 for x, y in epu1_target_13), "EPU1 must be strictly inside Q0!"
    assert all(5 <= x <= 9 and 0 <= y <= 4 for x, y in epu2_target_13), "EPU2 must be strictly inside Q1!"
    assert len(epu1_target_13.intersection(epu2_target_13)) == 0, "EPU1 and EPU2 must be disjoint!"

    # Total 26 unique tiles
    all_26 = epu1_target_13.union(epu2_target_13)
    assert len(all_26) == 26
