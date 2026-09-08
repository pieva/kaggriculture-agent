from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
for name in ['biological_plan_770','daily_routes_770','daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(p/f'{name}_v41.py').read_text(encoding='utf-8').replace('_v41','_v43').replace('V41','V43')
    (p/f'{name}_v43.py').write_text(s,encoding='utf-8')
f=p/'daily_routes_770_v43.py';s=f.read_text(encoding='utf-8')
s=s.replace('            queue=[] if rescue else queues.get(worker,[])', '''            water_deadline=(isinstance(tile,dict) and tile.get('kind')=='PLANT' and tile.get('consecutive_unwatered',0)>=1 and not tile.get('watered_today') and any(c[0]=='WATER' for c in commands) and not any(c[0] in {'PLANT','DIG'} for c in commands))
            if water_deadline:
                assigned=next((w for w,q in queues.items() if target in q),None)
                late=assigned is None
                if assigned is not None:
                    prefix=queues[assigned][:queues[assigned].index(target)+1]
                    route=[contracts[t] for t in prefix if t in contracts]
                    active=core.active.get(assigned,{})
                    active_steps=active.get('steps',[])
                    start=active_steps[-1][1] if active_steps else core.positions[assigned]
                    estimate=len(active_steps)+route_cost(start,route,core.sheds,core.private['inventories'][assigned])
                    late=estimate>=max(0,core.remaining-2)
                rescue=rescue or late
            queue=[] if rescue else queues.get(worker,[])''')
f.write_text(s,encoding='utf-8')
