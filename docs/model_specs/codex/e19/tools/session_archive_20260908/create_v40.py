from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
for name in ['biological_plan_770','daily_routes_770','daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(p/f'{name}_v39.py').read_text(encoding='utf-8').replace('_v39','_v40').replace('V39','V40')
    (p/f'{name}_v40.py').write_text(s,encoding='utf-8')
f=p/'daily_routes_770_v40.py';s=f.read_text(encoding='utf-8')
s=s.replace('def pack_routes(','''def protected_visit(offer):
    return offer[2]==8


def protected_order(route):
    seen_other=False
    for offer in route:
        if protected_visit(offer):
            if seen_other:return False
        else:seen_other=True
    return True


def pack_routes(''')
s=s.replace('                cost=route_cost(start,candidate,sheds,inventories[w])','                if not protected_order(candidate):continue\n                cost=route_cost(start,candidate,sheds,inventories[w])')
s=s.replace('        if core.day>=25:return current','''        if core.day>=25:return current
        current=[(t,cmds,8,v,k) if isinstance(core._tile(t),dict) and core._tile(t).get('animal') and any(c[0] in {'FEED','CARE'} for c in cmds) else (t,cmds,p,v,k) for t,cmds,p,v,k in current]''')
s=s.replace('            queue=[] if rescue else queues.get(worker,[])', '''            rescue=rescue or (isinstance(tile,dict) and tile.get('animal') and tile.get('consecutive_unfed',0)>=1 and not tile.get('fed_today') and any(c[0]=='FEED' for c in commands))
            queue=[] if rescue else queues.get(worker,[])''')
f.write_text(s,encoding='utf-8')
f=p/'daily_route_dispatch_770_v40.py';s=f.read_text(encoding='utf-8')
s=s.replace('(9*int(priority==7)+6*int(priority==6)+3*int(priority==3)', '(12*int(priority==8)+9*int(priority==7)+6*int(priority==6)+3*int(priority==3)',1)
f.write_text(s,encoding='utf-8')
