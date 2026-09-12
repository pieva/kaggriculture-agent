"""Count historical CARE requests at the spot-price floor, not causal wasted work."""
import gzip,hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'docs/model_specs/codex/e20'
rows=[];totals=Counter()
for path in sorted((BASE/'artifacts/e20_1_confirmation').glob('E20.1_E18_*.replay.json.gz')):
    with gzip.open(path,'rb') as f:raw=f.read()
    replay=json.loads(raw);counts=Counter()
    for i in range(457,720):
        o=replay['steps'][i-1][0]['observation'];action=replay['steps'][i][0]['action'];farm=o['farms'][0]
        for worker,command in enumerate([action.get('farmer',[]),*action.get('hands',[])]):
            if command!=['CARE']:continue
            x,y=[farm['farmer'],*farm['hands']][worker];tile=farm['tiles'][y][x]
            if not isinstance(tile,dict) or not tile.get('animal'):continue
            counts['care_requests']+=1
            counts['care_before_feed']+=not tile.get('fed_today',False)
            counts['already_cared']+=bool(tile.get('cared_today'))
            product={'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG'}[tile['animal']]
            counts['care_at_floor']+=o['market']['prices'][product]==1
    rows.append(dict(source=path.relative_to(ROOT).as_posix(),replay_sha256=hashlib.sha256(raw).hexdigest(),counts=dict(counts)))
    totals.update(counts)
assert len(rows)==7
(BASE/'reports/e20_2/INITIAL_DIAGNOSIS.json').write_text(json.dumps(dict(scope='D20-D30, seven exposed seeds, E20.1 against E18 seat zero; requests, not marginal yield estimates',rows=rows,totals=dict(totals)),indent=2)+'\n')
print(dict(totals))
