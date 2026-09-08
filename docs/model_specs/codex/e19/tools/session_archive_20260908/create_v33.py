from pathlib import Path
b=Path('docs/model_specs/codex/e19/tools')
s=(b/'daily_route_scheduler_770_v32.py').read_text(encoding='utf-8')
s=s.replace("if c[0]=='FEED' and tile.get('animal')", "if c[0] in {'FEED','CARE'} and tile.get('animal')")
s=s.replace('same observed FEED/WATER obligations', 'observed FEED/WATER obligations plus animal CARE')
(b/'daily_route_scheduler_770_v33.py').write_text(s,encoding='utf-8')
s=(b/'run_daily_routes_770_v32.py').read_text(encoding='utf-8').replace('_v32','_v33')
(b/'run_daily_routes_770_v33.py').write_text(s,encoding='utf-8')
