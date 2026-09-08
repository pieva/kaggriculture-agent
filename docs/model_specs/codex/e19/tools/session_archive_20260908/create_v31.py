from pathlib import Path
b=Path('docs/model_specs/codex/e19/tools')
s=(b/'daily_routes_770_v30.py').read_text(encoding='utf-8')
s=s.replace("rescue=(commands==[['HARVEST']] and harvest_due", "rescue=(any(cmd[0]=='HARVEST' for cmd in commands) and harvest_due")
(b/'daily_routes_770_v31.py').write_text(s,encoding='utf-8')
s=(b/'daily_route_scheduler_770_v30.py').read_text(encoding='utf-8').replace('daily_routes_770_v30','daily_routes_770_v31')
(b/'daily_route_scheduler_770_v31.py').write_text(s,encoding='utf-8')
s=(b/'run_daily_routes_770_v30.py').read_text(encoding='utf-8').replace('_v30','_v31')
(b/'run_daily_routes_770_v31.py').write_text(s,encoding='utf-8')
