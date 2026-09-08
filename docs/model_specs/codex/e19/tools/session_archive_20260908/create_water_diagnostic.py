from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
s=(p/'run_daily_routes_770_v48.py').read_text(encoding='utf-8')
s=s.replace("OUT=BASE/'artifacts/derived/portfolio_succession_20260907'","OUT=BASE/'artifacts/derived/residual_water_770_20260908'")
s=s.replace('        return a\n', '''        if 26<=obs['day']<=28:
            c=policy.core
            trace.append(dict(probe=True,day=obs['day']+1,hour=obs['hour']+1,
                tiles=deepcopy(c.farm['tiles']),positions=deepcopy(c.positions),
                inventories=deepcopy(c.private['inventories']),shed=deepcopy(c.private['shed']),
                active=deepcopy(c.active),commands=deepcopy(a),remaining=c.remaining,
                route_state=deepcopy(c.daily_route_state),metric_delta=dict(Counter(c.metrics)-before)))
        return a
''')
a=s.index('    cases=');b=s.index('\n    with ProcessPoolExecutor',a)
s=s[:a]+"    cases=[('daily_routes_v48_diagnostic',180903003,0)]"+s[b:]
(p/'run_residual_water_diagnostic_v48.py').write_text(s,encoding='utf-8')
