from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
for name in ['biological_plan_770','daily_routes_770','daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(p/f'{name}_v45.py').read_text(encoding='utf-8').replace('_v45','_v46').replace('V45','V46')
    s=s.replace('core.day>=27','core.day>=29').replace('core.day<27','core.day<29').replace('self.day<27','self.day<29')
    (p/f'{name}_v46.py').write_text(s,encoding='utf-8')
f=p/'biological_plan_770_v46.py';s=f.read_text(encoding='utf-8')
s=s.replace('from collections import Counter','from collections import Counter\nfrom docs.model_specs.codex.e19.tools.portfolio_workforce_v16 import care_value')
s=s.replace("if not t.get('cared_today'):commands.append(['CARE'])", "if not t.get('cared_today') and (core.day<27 or care_value(t,core.day,core.final_day,r,core._quote)>0):commands.append(['CARE'])")
f.write_text(s,encoding='utf-8')
