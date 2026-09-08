from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
for name in ['biological_plan_770','daily_routes_770','daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(p/f'{name}_v44.py').read_text(encoding='utf-8').replace('_v44','_v45').replace('V44','V45')
    s=s.replace('core.day>=25','core.day>=27').replace('core.day<25','core.day<27').replace('self.day<25','self.day<27')
    (p/f'{name}_v45.py').write_text(s,encoding='utf-8')
f=p/'biological_plan_770_v45.py';s=f.read_text(encoding='utf-8')
needle="            tile=core._tile(pos)\n"
s=s.replace(needle,needle+"""            if core.day>=25:
                choices=[c for c in ['WHEAT','CARROT'] if core.day+rules['CROPS'][c]['max_yield_day']<=core.final_day-1 and rules['CROPS'][c]['seed']<=cash]
                if not choices:continue
                intended=max(choices,key=lambda c:(core._quote(c,'SELL',rules['CROPS'][c]['max_yield'])-rules['CROPS'][c]['seed'])/(rules['CROPS'][c]['max_yield_day']+1))
""")
f.write_text(s,encoding='utf-8')
