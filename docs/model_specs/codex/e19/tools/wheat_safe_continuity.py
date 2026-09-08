"""Keep expiring wheat below biological emergencies in the scheduler."""
import ast
from pathlib import Path
from types import MethodType
from docs.model_specs.codex.e19.tools.wheat_continuity import install as install_deadline

def install(core):
    install_deadline(core)
    services=core._services
    def ranked_services():
        out=[]
        for target,commands,priority,value,kind in services():
            tile=core._tile(target)
            if tile.get('crop')=='WHEAT' and ['HARVEST'] in commands and core.day-tile['planted_day']>=4:
                # Rank 4 denotes an economic expiry, NOT a biological emergency.
                priority=3 if not tile.get('watered_today') and tile.get('consecutive_unwatered',0)>=1 else 4
            out.append((target,commands,priority,value,kind))
        return out
    core._services=ranked_services
    root=Path(__file__).resolve().parents[5]
    source=ast.parse((root/'submission/submission_codex_e19_control_770_v2.py').read_text(encoding='utf-8'))
    cls=next(n for n in source.body if isinstance(n,ast.ClassDef) and n.name=='CommonController')
    method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__call__')
    replacements=0
    for node in ast.walk(method):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='score' for t in node.targets):
            assert isinstance(node.value,ast.Tuple)
            assert ast.unparse(node.value.elts[0])=='int(priority == 3)'
            node.value.elts[0]=ast.parse('2 * int(priority == 3) + int(priority == 4)',mode='eval').body
            replacements+=1
    assert replacements==1
    namespace={}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[method],type_ignores=[])),str(__file__),'exec'),core.__call__.__func__.__globals__,namespace)
    # Special methods resolve on the class. Give only this instance a subclass.
    core.__class__=type('WheatSafeController',(core.__class__,),{'__call__':namespace['__call__']})
