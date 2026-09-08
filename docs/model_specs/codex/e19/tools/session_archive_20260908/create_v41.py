from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
for name in ['biological_plan_770','daily_routes_770','daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(p/f'{name}_v40.py').read_text(encoding='utf-8').replace('_v40','_v41').replace('V40','V41')
    if name=='daily_routes_770':
        s=s.replace("core._tile(t).get('animal') and any(c[0] in {'FEED','CARE'} for c in cmds)","core._tile(t).get('animal') and core._tile(t).get('consecutive_unfed',0)>=1 and not core._tile(t).get('fed_today') and any(c[0]=='FEED' for c in cmds)")
    (p/f'{name}_v41.py').write_text(s,encoding='utf-8')
