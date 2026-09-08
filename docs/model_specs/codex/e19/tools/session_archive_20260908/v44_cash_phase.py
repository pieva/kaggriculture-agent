import json
from pathlib import Path
from statistics import mean
p=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
for v in ['v41','v44']:
    ps=[json.loads((p/f'daily_routes_{v}_{s}_{t}.json').read_text(encoding='utf-8'))['sides']['candidate'] for s in range(180903001,180903004) for t in (0,1)]
    print(v,'daily keys',list(ps[0]['daily'][24]))
    print('cash checkpoints',[(d,mean(x['daily'][d-1]['money'] for x in ps)) for d in [20,25,30]])
    print('final crops',[x['daily'][29]['crops'] for x in ps])
