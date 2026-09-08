from pathlib import Path
b=Path('docs/model_specs/codex/e19/tools')
s=(b/'daily_routes_770_v35.py').read_text(encoding='utf-8')
start=s.index('            late=False\n            if urgent:')
end=s.index('            rescue=',start)
block=s[start:end]
body=block.split('            if urgent:\n',1)[1]
body='\n'.join(line[8:] if line.startswith('        ') else line for line in body.splitlines())
helper='    def deadline_late(target):\n'+body+'\n        return late\n'
helper=helper.replace('target=tuple(target)','target=tuple(target)')
s=s[:start]+'            late=deadline_late(target) if urgent else False\n'+s[end:]
s=s.replace('    def offers_with_routes():',helper+'    def offers_with_routes():')
s=s.replace("if isinstance(tile,dict) and tile.get('kind')=='PLANT' and tile.get('consecutive_unwatered',0)>=1 and not tile.get('watered_today'):","if isinstance(tile,dict) and tile.get('kind')=='PLANT' and tile.get('consecutive_unwatered',0)>=1 and not tile.get('watered_today') and (core.remaining<=6 or deadline_late(tuple(target))):")
s=s.replace("elif isinstance(tile,dict) and tile.get('animal') and tile.get('consecutive_unfed',0)>=1 and not tile.get('fed_today'):","elif isinstance(tile,dict) and tile.get('animal') and tile.get('consecutive_unfed',0)>=1 and not tile.get('fed_today') and (core.remaining<=6 or deadline_late(tuple(target))):")
(b/'daily_routes_770_v37.py').write_text(s,encoding='utf-8')
for name in ['daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(b/f'{name}_v35.py').read_text(encoding='utf-8').replace('_v35','_v37')
    (b/f'{name}_v37.py').write_text(s,encoding='utf-8')
