from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
for name in ['biological_plan_770','daily_routes_770','daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(p/f'{name}_v41.py').read_text(encoding='utf-8').replace('_v41','_v44').replace('V41','V44')
    (p/f'{name}_v44.py').write_text(s,encoding='utf-8')
f=p/'daily_routes_770_v44.py';s=f.read_text(encoding='utf-8')
s=s.replace("if queue and contracts.get(queue[0],(None,None,None,None,None))[4]=='NEW_CROP':queue=[]", "queue=[p for p in queue if p==target or not str(contracts.get(p,(None,None,None,None,''))[4]).startswith('NEW_')]")
f.write_text(s,encoding='utf-8')
