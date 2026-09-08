from pathlib import Path
src=Path('docs/model_specs/codex/e19/tools/run_daily_routes_770_v31.py')
s=src.read_text(encoding='utf-8')
s=s.replace('    install(policy.core)', '''    install(policy.core)
    diag=[]
    original_certificate=policy.core._day_route_certificate
    def cert(worker,job,services=None):
        ok=original_certificate(worker,job,services)
        c=policy.core
        if c.day in [20,21]:
            diag.append(dict(day=c.day+1,hour=c.hour+1,ok=ok,kind=job['kind'],target=job['target'],commands=[x[0] for x in job['steps']],remaining=c.remaining,services=services,active=deepcopy(c.active)))
        return ok
    policy.core._day_route_certificate=cert''')
s=s.replace("result=dict(succession_log=", "result=dict(admission_diagnostic=diag,succession_log=")
s=s.replace("cases=[('daily_routes_v31',180903001,0)] if '--screen' in sys.argv else [('daily_routes_v31',s,t) for s in range(180903001,180903004) for t in (0,1)]", "cases=[('daily_routes_v31_diagnostic',180903001,0)]")
# In-process run avoids pickling dynamically loaded functions.
s=s.replace("with ProcessPoolExecutor(max_workers=2) as pool:list(pool.map(run,cases))", "for case in cases:run(case)")
exec(compile(s,str(src),'exec'),dict(__file__=str(src.resolve()),__name__='__main__'))
