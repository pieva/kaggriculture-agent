"""Build isolated E23 portfolios on E22's repaired executor and fixed routes."""
import argparse,ast,base64,hashlib,json,runpy,zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
SOURCE=Path('C:/Users/pietr/.codex/worktrees/756c/kaggriculture-agent/submission')
OUT=ROOT/'docs/model_specs/codex/e23/reports/tournament4_v1'
BASES={'E22G':('submission_codex_e22_1_q2_grano_v1.py','5db3ef642ddf8cac5a8797ee92baea40a7caa6ab9eb1908db482b7fdc3c4b18a'),
       'E22S':('submission_codex_e22_2_fix_q2_grano_v1.py','c6b6dcaa7480df647a288ec8c4333ed0a7b34a44cee1a068e9946d94209a1c3a')}

PRELUDES='''
_TARGETS = TARGETS_VALUE
_EVOLVED = EVOLVED_VALUE
_SERVICE = {'FEED', 'CARE', 'HARVEST', 'COLLECT_FERTILIZER', 'PASS'}

class PublishedAgent:
    def __init__(self, context=None): pass
    def __call__(self, obs, cfg=None):
        day,hour=int(obs['day']),int(obs['hour'])
        i=day*24+hour
        if not 0<=i<len(_PLAN):
            return {'farmer':['PASS'],'hands':[],'market':[]}
        action=copy.deepcopy(_PLAN[i])
        farm=obs['farms'][int(obs['player'])]
        projected={}
        for w,(pos,cmd) in enumerate(zip([farm['farmer']]+farm['hands'],[action['farmer']]+action['hands'])):
            xy=tuple(pos)
            if xy not in _TARGETS or not cmd or cmd[0] not in _SERVICE:continue
            if xy not in projected:projected[xy]=copy.deepcopy(farm['tiles'][pos[1]][pos[0]])
            tile=projected[xy]
            if not isinstance(tile,dict) or not tile.get('animal'):continue
            inv=obs['private']['inventories'][w]
            op='PASS'
            if day<29 and not tile.get('fed_today') and inv.get('WHEAT',0):
                op='FEED';tile['fed_today']=True
            elif xy in _EVOLVED and tile.get('yield_units',0):
                op='HARVEST';tile['yield_units']=0
            elif day<29 and not tile.get('cared_today'):
                op='CARE';tile['cared_today']=True
            elif tile.get('yield_units',0):
                op='HARVEST';tile['yield_units']=0
            elif tile.get('fertilizer_available'):
                op='COLLECT_FERTILIZER';tile['fertilizer_available']=False
            cmd[:]=[op]
        for order in action['market']:
            if len(order)>2 and order[0]=='SELL' and order[1] in CLEAR_PRODUCTS:
                order[2]=100
        return action

'''


def main():
    global OUT
    parser=argparse.ArgumentParser();parser.add_argument('--five',action='store_true');args=parser.parse_args()
    if args.five:OUT=OUT.parent/'tournament5_v1'
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={}
    plans={}
    for key,(name,sha) in BASES.items():
        source=SOURCE/name;raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()==sha
        dest=ROOT/'submission'/name
        if dest.exists():assert dest.read_bytes()==raw
        else:dest.write_bytes(raw)
        plans[key]=runpy.run_path(str(source))['_PLAN']
        manifest[key]=dict(path=str(dest),sha256=sha,status='frozen published control',submission=56228842 if key=='E22G' else 56231638)
    # Retain E22S's observation-based executor, without its original goose conversion.
    source=(SOURCE/BASES['E22S'][0]).read_text(encoding='utf-8')
    executor=source[source.index('class Agent(PublishedAgent):'):]
    executor=executor.replace('E22.2 fix Q2 Grano v1:', 'E23 evolution v1:')
    variants=[
        ('E23G','E22G',[(217,'market',1,'SHEEP','COW'),(222,'hands',2,'SHEEP','COW'),(229,'hands',2,'SHEEP','COW')],{(6,2)},{(6,2)},('MILK',)),
        ('E23S','E22S',[(169,'market',3,'COW','SHEEP'),(170,'hands',2,'COW','SHEEP'),(177,'hands',2,'COW','SHEEP'),(176,'market',0,'COW','SHEEP'),(177,'hands',4,'COW','SHEEP'),(179,'hands',5,'COW','SHEEP'),(182,'hands',5,'COW','SHEEP')],{(4,1),(3,2),(2,3),(6,4),(5,2)},{(6,4),(5,2)},('WOOL',))]
    if args.five:variants.append(('E23M','E22S',[(169,'market',3,'COW','SHEEP'),(170,'hands',2,'COW','SHEEP'),(177,'hands',2,'COW','SHEEP')],{(4,1),(3,2),(2,3),(6,4)},{(6,4)},('WOOL',)))
    for label,base,changes,targets,evolved,clear in variants:
        plan=json.loads(json.dumps(plans[base]))
        for i,field,w,old,new in changes:
            assert plan[i][field][w][1]==old,(i,field,w,plan[i][field][w])
            plan[i][field][w][1]=new
        encoded=base64.b64encode(zlib.compress(json.dumps(plan,separators=(',',':')).encode())).decode()
        pre=PRELUDES.replace('TARGETS_VALUE',repr(targets)).replace('EVOLVED_VALUE',repr(evolved)).replace('CLEAR_PRODUCTS',repr(clear))
        text=f'"""{label}: local E23 v1, fixed portfolio on repaired E22 routes. No future information."""\nimport base64,zlib,json,copy\n_PLAN=json.loads(zlib.decompress(base64.b64decode({encoded!r})))\n'+pre+executor
        name={'E23G':'submission_codex_e23_1_geese_v1.py','E23S':'submission_codex_e23_2_sheep_v1.py','E23M':'submission_codex_e23_3_7c10s_v1.py'}[label]
        dest=ROOT/'submission'/name;ast.parse(text)
        if dest.exists():assert dest.read_text(encoding='utf-8')==text,'Existing frozen bundle would change'
        else:dest.write_text(text,encoding='utf-8')
        manifest[label]=dict(path=str(dest),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='local candidate',parent=base,
          mix={'E23G':{'COW':9,'SHEEP':5,'GOOSE':3},'E23S':{'COW':6,'SHEEP':11},'E23M':{'COW':7,'SHEEP':10}}[label],
          plan_edits=changes,targets=sorted(targets),evolved=sorted(evolved),clear_products=clear,
          scope='Portfolio at first placement; adapt stationary services; clear modified product in existing sale windows; shared E22S repairs. No route or hiring changes, no Q3/tomato. Sheep (5,2) keeps E22 D8 H15 rather than replay H16.')
        assert plan[648:]==plans[base][648:],'Q2 wheat and closure remain encoded'
        if label=='E23M':manifest[label]['scope']='Intermediate portfolio: only (6,4) becomes SHEEP at D8 H10; (5,2) remains COW. Same services/executor/sale rule as E23S on the evolved tile; all E22S routes, hires and crops retained, including Q2 wheat.'
    (OUT/'BUNDLES.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
