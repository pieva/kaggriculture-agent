import ast
import runpy
from pathlib import Path
from docs.model_specs.codex.e19.tools.portfolio_logistics import install

ROOT=Path(__file__).resolve().parents[5]


def make_core():
    core=runpy.run_path(str(ROOT/'submission/submission_codex_e19_control_770_v2.py'))['create_agent']({'player_position':0})
    install(core)
    core.day=12;core.final_day=29;core.remaining=4;core.maintenance_floor=10
    core.active={};core.positions=[(0,0)]*13;core.sheds=[(4,4)]
    core.private={'shed':{},'inventories':[{} for _ in range(13)]}
    core.farm={'money':1000,'tiles':[[{'kind':'PLANT','crop':'WHEAT','yield_units':4}]]}
    return core


def test_late_harvest_uses_real_overnight_transfer_but_not_on_final_day():
    c=make_core()
    assert c._prepare_steps(0,(0,0),[['HARVEST']])==[(['HARVEST'],(0,0))]
    c.day=c.final_day
    assert c._prepare_steps(0,(0,0),[['HARVEST']]) is None


def test_capacity_risk_requires_an_actual_return_route():
    c=make_core();c.private['shed']={'WHEAT':96}
    assert c._prepare_steps(0,(0,0),[['HARVEST']]) is None


def test_small_deliveries_are_batched_and_terminal_wheat_is_included():
    c=make_core();c.private['inventories'][0]={'MILK':1}
    assert not c._portfolio_delivery_needed(0)
    c.private['inventories'][0]={'MILK':8}
    assert c._portfolio_delivery_needed(0)
    c.day=c.final_day;c.private['inventories'][0]={'WHEAT':1}
    assert c._portfolio_delivery_needed(0)


def test_official_engine_transfer_discards_only_capacity_overflow():
    source=ROOT/'.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py'
    node=next(n for n in ast.parse(source.read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef) and n.name=='_drop_inventories_to_shed')
    scope={}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),scope)
    private={'shed':{'WHEAT':95},'inventories':[{'MILK':8}]}
    scope['_drop_inventories_to_shed'](private,100)
    assert private=={'shed':{'WHEAT':95,'MILK':5},'inventories':[{}]}
