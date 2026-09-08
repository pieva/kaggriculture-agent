from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
for name in ['biological_plan_770','daily_routes_770','daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(p/f'{name}_v46.py').read_text(encoding='utf-8').replace('_v46','_v47').replace('V46','V47')
    (p/f'{name}_v47.py').write_text(s,encoding='utf-8')
f=p/'daily_routes_770_v47.py';s=f.read_text(encoding='utf-8')
s=s.replace('def protected_visit(offer):', '''def final_water_deadline(day,tile,commands):
    return (27<=day<29 and isinstance(tile,dict) and tile.get('kind')=='PLANT'
            and tile.get('consecutive_unwatered',0)>=1 and not tile.get('watered_today')
            and any(c[0]=='WATER' for c in commands) and not any(c[0] in {'PLANT','DIG'} for c in commands))


def protected_visit(offer):''')
needle="        ready=tuple(sorted(t for t in pending"
s=s.replace(needle,"        current=[(t,cmds,8,v,k) if final_water_deadline(core.day,core._tile(t),cmds) else (t,cmds,p,v,k) for t,cmds,p,v,k in current]\n"+needle)
s=s.replace('            queue=[] if rescue else queues.get(worker,[])','            rescue=rescue or final_water_deadline(core.day,tile,commands)\n            queue=[] if rescue else queues.get(worker,[])')
f.write_text(s,encoding='utf-8')
