from pathlib import Path
b=Path('docs/model_specs/codex/e19/tools')
s=(b/'daily_routes_770_v35.py').read_text(encoding='utf-8')
s=s.replace('        current=services()', '''        current=services()
        # Preserve the full productive visit ahead of its one-command fallback.
        def deadline(offer):
            target,commands,priority,value,kind=offer
            tile=core._tile(target)
            urgent=isinstance(tile,dict) and any(
                cmd[0]=='WATER' and tile.get('consecutive_unwatered',0)>=1 or
                cmd[0]=='FEED' and tile.get('consecutive_unfed',0)>=1 for cmd in commands)
            return (target,commands,9 if urgent else priority,value,kind)
        current=[deadline(o) for o in current]''')
(b/'daily_routes_770_v36.py').write_text(s,encoding='utf-8')
for name in ['daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(b/f'{name}_v35.py').read_text(encoding='utf-8').replace('_v35','_v36').replace('(12*int(priority==8)', '(15*int(priority==9)+12*int(priority==8)')
    (b/f'{name}_v36.py').write_text(s,encoding='utf-8')
