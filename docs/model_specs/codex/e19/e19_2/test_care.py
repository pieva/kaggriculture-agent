"""Biological boundary cases: care is stored after the coming production."""
import ast
from pathlib import Path
HERE=Path(__file__).resolve().parent
ns={}
for path,name in [(HERE/'sources_v51c/portfolio_workforce_v16.py','care_value'),(HERE/'biological_plan_v52d.py','productive_care_value')]:
    tree=ast.parse(path.read_text(encoding='utf-8'))
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),'exec'),ns)
rule=dict(first_yield_day=3,interval=3,max_held=3,product='WOOL')
tile=dict(placed_day=0,pending_care_bonus=2,cared_today=False)
quote=lambda *args:100
value=ns['productive_care_value']
assert value(tile,3,29,rule,quote)==0, 'Saturated bonus, next refresh is not production'
assert value(tile,2,29,rule,quote)==100, 'Production consumes bonus before current care is stored'
assert value(dict(tile,pending_care_bonus=1),3,29,rule,quote)==100
assert value(dict(tile,cared_today=True),2,29,rule,quote)==0
assert value(tile,26,27,rule,quote)==0, 'No future production can benefit from current care'
assert tile['pending_care_bonus']==2, 'Observation must remain unchanged'
print('6 care boundary checks passed')
