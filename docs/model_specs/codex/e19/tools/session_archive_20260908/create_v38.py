from pathlib import Path
b=Path('docs/model_specs/codex/e19/tools')
s=(b/'biological_plan_770_v25.py').read_text(encoding='utf-8')
old="if not t.get('watered_today') and (rules['needs_water'](t,core.day) or fertilize):commands.append(['WATER'])"
new="if not t.get('watered_today') and (rules['needs_water'](t,core.day) or fertilize or t['crop']=='STRAWBERRY' and (x+y+core.day)%2==0):commands.append(['WATER'])"
assert old in s;s=s.replace(old,new)
s=s.replace('770-only V25:', '770-only V38: staggered strawberry watering;')
(b/'biological_plan_770_v38.py').write_text(s,encoding='utf-8')
s=(b/'daily_routes_770_v31.py').read_text(encoding='utf-8').replace('biological_plan_770_v25','biological_plan_770_v38')
(b/'daily_routes_770_v38.py').write_text(s,encoding='utf-8')
s=(b/'daily_route_scheduler_770_v31.py').read_text(encoding='utf-8').replace('daily_routes_770_v31','daily_routes_770_v38')
(b/'daily_route_dispatch_770_v38.py').write_text(s,encoding='utf-8')
s=(b/'daily_route_scheduler_770_v33.py').read_text(encoding='utf-8').replace('daily_route_scheduler_770_v31','daily_route_dispatch_770_v38').replace('daily_routes_770_v31','daily_routes_770_v38')
(b/'daily_route_scheduler_770_v38.py').write_text(s,encoding='utf-8')
s=(b/'run_daily_routes_770_v33.py').read_text(encoding='utf-8').replace('_v33','_v38').replace('daily_routes_770_v31','daily_routes_770_v38').replace('daily_route_scheduler_770_v31','daily_route_dispatch_770_v38').replace('biological_plan_770_v25','biological_plan_770_v38').replace('V26 planned harvest deadlines','V38 staggered biological service')
(b/'run_daily_routes_770_v38.py').write_text(s,encoding='utf-8')
