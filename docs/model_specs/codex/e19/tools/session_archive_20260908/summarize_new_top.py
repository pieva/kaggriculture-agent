import sys,json
from pathlib import Path
from statistics import mean
sys.path.insert(0,str(Path.cwd()))
B=Path('docs/model_specs/codex/e19');O=B/'reports/new_top_v48_20260908'
ps=json.loads((O/'profiles.json').read_text(encoding='utf-8'))
groups={'V48':[json.loads(p.read_text(encoding='utf-8'))['sides']['candidate'] for p in sorted((B/'artifacts/derived/portfolio_succession_20260907').glob('daily_routes_v48_*.json'))]}
for name in ['Subin An','Matthew Huang','Suliman Tadros']:groups[name]=[p for p in ps if p['name']==name]
rows={}
for name,g in groups.items():
 row={'n':len(g),'cash':mean(p['terminal']['cash'] for p in g)}
 for a,b in [(1,11),(15,25),(26,30)]:
  s=[d for p in g for d in p['daily'][a-1:b]];o=[d for p in g for d in p['operational_daily'][a-1:b]];f=[d for p in g for d in p['ledger']['daily'][a-1:b]]
  row[f'D{a}-{b}']={k:mean(d[k] for d in s) for k in ['crop_tiles','people','occupied_livestock_tiles']}
  row[f'D{a}-{b}'].update({k:mean(d[k] for d in o) for k in ['PASS','MOVE','weed_tiles','verified_animal_losses']})
  row[f'D{a}-{b}'].update({k:mean(d['executed_actions'].get(k,0) for d in f) for k in ['WATER','FEED','CARE']})
  row[f'D{a}-{b}']['hire_cash']=mean(d['hire_cash'] for d in f)
 rows[name]=row
(O/'phase_summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows,indent=2))
