from pathlib import Path
b=Path('docs/model_specs/codex/e19/tools')
s=(b/'daily_routes_770_v34.py').read_text(encoding='utf-8')
old="            rescue=(any(cmd[0]=='HARVEST' for cmd in commands) and harvest_due(tile,core.day,core.turns)) or (commands in [[['WATER']],[['FEED']]] and isinstance(tile,dict) and (commands==[['WATER']] and tile.get('consecutive_unwatered',0)>=1 or commands==[['FEED']] and tile.get('consecutive_unfed',0)>=1))"
new="""            urgent=(commands in [[['WATER']],[['FEED']]] and isinstance(tile,dict) and
                    (commands==[['WATER']] and tile.get('consecutive_unwatered',0)>=1 or
                     commands==[['FEED']] and tile.get('consecutive_unfed',0)>=1))
            late=False
            if urgent:
                assigned=next((w for w,q in queues.items() if target in q),None)
                if assigned is None:late=True
                else:
                    q=queues[assigned];prefix=q[:q.index(target)+1]
                    pos=core.positions[assigned];inv=Counter(core.private['inventories'][assigned]);elapsed=0
                    job=core.active.get(assigned)
                    if job:
                        elapsed=len(job['steps'])
                        if job['steps']:pos=job['steps'][-1][1]
                        for cmd,p in job['steps']:
                            if cmd[0]=='PICKUP':inv[cmd[1]]+=cmd[2]
                            elif cmd[0] in {'FEED','FERTILIZE','PLACE'}:inv.subtract(inputs([cmd]))
                            elif cmd[0]=='DROP':inv.clear()
                    late=elapsed+route_cost(pos,[contracts[p] for p in prefix],core.sheds,inv)>=core.remaining
            rescue=(any(cmd[0]=='HARVEST' for cmd in commands) and harvest_due(tile,core.day,core.turns)) or (urgent and (late or core.remaining<=6))"""
assert old in s
s=s.replace(old,new)
(b/'daily_routes_770_v35.py').write_text(s,encoding='utf-8')
for name in ['daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(b/f'{name}_v34.py').read_text(encoding='utf-8').replace('_v34','_v35').replace('V34 early','V35 projected')
    (b/f'{name}_v35.py').write_text(s,encoding='utf-8')
