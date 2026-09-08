from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
for name in ['biological_plan_770','daily_routes_770','daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    source=(p/f'{name}_v38.py').read_text(encoding='utf-8')
    (p/f'{name}_v39.py').write_text(source.replace('_v38','_v39').replace('V38','V39'),encoding='utf-8')
f=p/'biological_plan_770_v39.py'
s=f.read_text(encoding='utf-8')
s=s.replace('\ndef compact_owners', '''
def exhausted_perennial(tile, rules, day):
    if not isinstance(tile,dict) or tile.get('kind')!='PLANT':return False
    r=rules[tile['crop']]
    return (r['ongoing'] and tile.get('yield_units',0)==0
            and day>=tile['planted_day']+r['first_yield_day']+(r['max_yield']-1)*r['interval'])


def compact_owners''')
s=s.replace("            if core.day+rules['CROPS'][intended]['first_yield_day']>core.final_day:", """            # Reserve one day after mature yield for collection and delivery.
            if core.day+rules['CROPS'][intended]['first_yield_day']>core.final_day:
                choices=[c for c in ['WHEAT','CARROT'] if core.day+rules['CROPS'][c]['max_yield_day']<=core.final_day-1 and rules['CROPS'][c]['seed']<=cash]
                if choices:
                    intended=max(choices,key=lambda c:(core._quote(c,'SELL',rules['CROPS'][c]['max_yield'])-rules['CROPS'][c]['seed'])/(rules['CROPS'][c]['max_yield_day']+1))
            if core.day+rules['CROPS'][intended]['first_yield_day']>core.final_day:""")
s=s.replace("                    if tile.get('yield_units',0)<=0:continue\n                    commands=[['HARVEST']]+([['DIG']] if r['ongoing'] else [])", "                    if tile.get('yield_units',0)<=0 and not exhausted_perennial(tile,rules['CROPS'],core.day):continue\n                    commands=([['HARVEST']] if tile.get('yield_units',0)>0 else [])+([['DIG']] if r['ongoing'] else [])")
f.write_text(s,encoding='utf-8')
f=p/'daily_routes_770_v39.py';s=f.read_text(encoding='utf-8')
s='from docs.model_specs.codex.e19.tools.biological_plan_770_v39 import exhausted_perennial\n'+s
s=s.replace("if kind!='NEW_ROTATION' or target not in visits:continue", "if kind!='NEW_ROTATION' or (target not in visits and not exhausted_perennial(core._tile(target),rules['CROPS'],core.day)):continue")
s=s.replace("renewal_commands(visits[target][1],commands)", "renewal_commands(visits[target][1] if target in visits and not exhausted_perennial(core._tile(target),rules['CROPS'],core.day) else [],commands)")
s=s.replace("elif target in by_target and isinstance(tile,dict) and tile.get('kind')=='PLANT' and tile.get('yield_units',0)>0:", "elif isinstance(tile,dict) and tile.get('kind')=='PLANT' and ((target in by_target and tile.get('yield_units',0)>0) or exhausted_perennial(tile,core.__call__.__func__.__globals__['CROPS'],core.day)):")
f.write_text(s,encoding='utf-8')
