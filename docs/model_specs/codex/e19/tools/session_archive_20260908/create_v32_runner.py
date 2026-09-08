from pathlib import Path
b=Path('docs/model_specs/codex/e19/tools')
s=(b/'run_daily_routes_770_v31.py').read_text(encoding='utf-8').replace('daily_route_scheduler_770_v31','daily_route_scheduler_770_v32').replace('daily_routes_v31','daily_routes_v32')
s=s.replace('result=dict(succession_log=', 'result=dict(renewal_certificate_log=policy.core.renewal_certificate_log,succession_log=')
s=s.replace("Path(__file__).with_name('daily_route_scheduler_770_v32.py')", "Path(__file__).with_name('daily_route_scheduler_770_v32.py'),Path(__file__).with_name('daily_route_scheduler_770_v31.py')")
(b/'run_daily_routes_770_v32.py').write_text(s,encoding='utf-8')
