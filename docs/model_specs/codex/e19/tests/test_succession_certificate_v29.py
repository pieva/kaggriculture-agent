import ast
from pathlib import Path
from types import SimpleNamespace

def test_certificate_keeps_existing_water_and_candidate_water_only():
    source=Path(__file__).parents[1]/'tools/daily_route_scheduler_770_v29.py'
    tree=ast.parse(source.read_text(encoding='utf-8'))
    install=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='install')
    method=next(n for n in install.body if isinstance(n,ast.FunctionDef) and n.name=='mission_certificate')
    existing=((1,0),[['WATER']],3,1,'SERVICE')
    hypothetical=((2,0),[['PLANT','WHEAT'],['WATER']],4,1,'NEW_CROP')
    weed=((3,0),[['DIG'],['PLANT','WHEAT'],['WATER']],4,1,'NEW_CROP')
    tiles={(1,0):dict(kind='PLANT',crop='WHEAT'),(2,0):None,(3,0):dict(kind='WEED')}
    received=[]
    def certificate(w,j,s):
        received.append((j,s));return True
    scope=dict(core=SimpleNamespace(_tile=lambda t:tiles[t]),certificate=certificate)
    exec(compile(ast.Module(body=[method],type_ignores=[]),str(source),'exec'),scope)
    job=dict(kind='NEW_CROP',target=(2,0),steps=[(['PLANT','WHEAT'],(2,0)),(['WATER'],(2,0))])
    assert scope['mission_certificate'](0,job,[existing,hypothetical,weed])
    assert received[0][1]==[existing]
    assert received[0][0]['steps'][-1][0]==['WATER']
