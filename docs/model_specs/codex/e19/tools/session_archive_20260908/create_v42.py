from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
for name in ['biological_plan_770','daily_routes_770','daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(p/f'{name}_v41.py').read_text(encoding='utf-8').replace('_v41','_v42').replace('V41','V42')
    (p/f'{name}_v42.py').write_text(s,encoding='utf-8')
f=p/'daily_routes_770_v42.py';s=f.read_text(encoding='utf-8')
s=s.replace('def protected_visit(offer):', '''def urgent_biological_visit(tile, commands):
    if not isinstance(tile,dict):return False
    if tile.get('animal'):
        return tile.get('consecutive_unfed',0)>=1 and not tile.get('fed_today') and any(c[0]=='FEED' for c in commands)
    return (tile.get('kind')=='PLANT' and tile.get('consecutive_unwatered',0)>=1
            and not tile.get('watered_today') and any(c[0]=='WATER' for c in commands)
            and not any(c[0] in {'PLANT','DIG'} for c in commands))


def protected_visit(offer):''')
s=s.replace("isinstance(core._tile(t),dict) and core._tile(t).get('animal') and core._tile(t).get('consecutive_unfed',0)>=1 and not core._tile(t).get('fed_today') and any(c[0]=='FEED' for c in cmds)","urgent_biological_visit(core._tile(t),cmds)")
s=s.replace("(isinstance(tile,dict) and tile.get('animal') and tile.get('consecutive_unfed',0)>=1 and not tile.get('fed_today') and any(c[0]=='FEED' for c in commands))","urgent_biological_visit(tile,commands)")
f.write_text(s,encoding='utf-8')
