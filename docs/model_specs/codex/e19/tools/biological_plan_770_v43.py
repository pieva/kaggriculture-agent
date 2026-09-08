"""770-only V43: staggered strawberry watering; refresh on observed land and staffing; stable plot intentions and compact daily responsibilities to D25.

The assisted opening remains the control through D11. Dates below are engine
dates (zero based). From D26 the observed-state V16 closure resumes.
"""
from collections import Counter
from docs.model_specs.codex.e19.tools.portfolio_scheduler_v16 import install as install_previous


def biological_calendar(tile, rules, final_day=29):
    if tile.get('animal'):
        rule=rules[tile['animal']]
        start=tile['placed_day']
        return dict(first=start+rule['first_yield_day'],
                    productions=list(range(start+rule['first_yield_day'],final_day+1,rule['interval'])),
                    daily=['FEED','CARE','COLLECT_FERTILIZER'])
    rule=rules[tile['crop']];start=tile['planted_day']
    first=start+rule['first_yield_day']
    productions=([d for d in range(first,first+rule['interval']*rule['max_yield'],rule['interval']) if d<=final_day]
                 if rule['ongoing'] else [min(start+rule['max_yield_day'],final_day)])
    return dict(first=first,productions=productions,
                fertilizer_days=[d-1 for d in productions if rule['ongoing']],
                last_harvest=productions[-1] if productions else None)


def exhausted_perennial(tile, rules, day):
    if not isinstance(tile,dict) or tile.get('kind')!='PLANT':return False
    r=rules[tile['crop']]
    return (r['ongoing'] and tile.get('yield_units',0)==0
            and day>=tile['planted_day']+r['first_yield_day']+(r['max_yield']-1)*r['interval'])


def compact_owners(tiles, workers):
    """Balanced contiguous pieces of a serpentine walk; actual workers only."""
    ordered=sorted(tiles,key=lambda p:(p[1],p[0] if p[1]%2==0 else -p[0]))
    weights=[4 if isinstance(tiles[p],dict) and tiles[p].get('animal') else 2 for p in ordered]
    total=sum(weights);used=0;owners={}
    for p,w in zip(ordered,weights):
        owners[p]=min(workers-1,int((used+w/2)*workers/max(1,total)))
        used+=w
    return owners


def install(core):
    install_previous(core)
    services,growth,prepare=core._services,core._growth,core._prepare_steps
    certificate=core._day_route_certificate
    rules=core.__call__.__func__.__globals__
    plans={};stamp=None;owners={};intentions={}
    core.biological_plan={}
    def observe_plan():
        nonlocal stamp,owners
        signature=(core.day, tuple(sorted(core.farm["unlocked_quadrants"])), len(core.positions))
        if stamp==signature:return
        stamp=signature
        tiles={(x,y):t for y,row in enumerate(core.farm['tiles']) for x,t in enumerate(row) if t!='LOCKED'}
        owners=compact_owners(tiles,len(core.positions))
        for pos,tile in tiles.items():
            if isinstance(tile,dict) and tile.get('crop'):
                intentions.setdefault(pos,tile['crop'])
        # Plan the full 61-plot 770 crop allocation from the successful opening
        # proportions. Quotas are intentions, not unobserved funded plantings.
        targets={'WHEAT':23,'STRAWBERRY':38}
        counts=Counter(intentions.values())
        for pos,tile in sorted(tiles.items(),key=lambda kv:(kv[0][1],kv[0][0])):
            if pos in intentions or isinstance(tile,dict) and (tile.get('animal') or tile.get('kind') in {'PASTURE','COOP'}):continue
            crop=max(targets,key=lambda c:(targets[c]-counts[c],c))
            if counts[crop]<targets[crop]:intentions[pos]=crop;counts[crop]+=1
        calendar=[]
        for pos,t in tiles.items():
            if isinstance(t,dict) and (t.get('crop') or t.get('animal')):
                calendar.append(dict(position=pos,worker=owners[pos],kind=t.get('crop',t.get('animal')),
                                     **biological_calendar(t,{**rules['CROPS'],**rules['ANIMALS']},core.final_day)))
        core.biological_plan=dict(day=core.day+1,mode='planned' if core.day<25 else 'closure',
            areas=[dict(position=p,worker=w) for p,w in owners.items()],calendar=calendar,
            crop_intentions=[dict(position=p,crop=c) for p,c in intentions.items()])
    def planned_services():
        observe_plan()
        if core.day>=25:return services()
        claims={tuple(j['target']) for j in core.active.values() if j['kind']!='DELIVER'}
        result=[]
        for y,row in enumerate(core.farm['tiles']):
            for x,t in enumerate(row):
                pos=(x,y)
                if pos in claims or not isinstance(t,dict):continue
                commands=[];priority=2;value=1
                if t.get('animal'):
                    r=rules['ANIMALS'][t['animal']]
                    if not t.get('fed_today'):commands.append(['FEED'])
                    if not t.get('cared_today'):commands.append(['CARE'])
                    if t.get('yield_units',0):commands.append(['HARVEST']);value+=core._quote(r['product'],'SELL',t['yield_units'])
                    if t.get('fertilizer_available'):commands.append(['COLLECT_FERTILIZER'])
                    if not t.get('fed_today'):priority=3
                elif t.get('kind')=='PLANT':
                    r=rules['CROPS'][t['crop']];age=core.day-t['planted_day']
                    cal=biological_calendar(t,rules['CROPS'],core.final_day)
                    fertilize=(r['ongoing'] and core.day in cal['fertilizer_days'] and t.get('fertilized_until_day',-1)<core.day)
                    req,_=core._requirements()
                    if fertilize and core.private['shed'].get('FERTILIZER',0)>req['FERTILIZER']:commands.append(['FERTILIZE'])
                    if not t.get('watered_today') and (rules['needs_water'](t,core.day) or fertilize or t['crop']=='STRAWBERRY' and (x+y+core.day)%2==0):commands.append(['WATER'])
                    if t.get('yield_units',0) and age>=r['first_yield_day'] and (r['ongoing'] or age>=r['max_yield_day']):
                        commands.append(['HARVEST']);value+=core._quote(t['crop'],'SELL',t['yield_units'])
                        if not r['ongoing'] or t.get('max_lifespan_step',-1)>=0:priority=4
                    if t.get('consecutive_unwatered',0) and not t.get('watered_today'):priority=3
                if commands:result.append((pos,commands,priority,value,'SERVICE'))
        return result
    def planned_growth(cash):
        observe_plan()
        offers=growth(cash)
        if core.day>=25:return offers
        result=[o for o in offers if o[4]=='NEW_ANIMAL']
        claims={tuple(j['target']) for j in core.active.values() if j['kind']!='DELIVER'}
        for pos,intended in intentions.items():
            if pos in claims:continue
            tile=core._tile(pos)
            # Reserve one day after mature yield for collection and delivery.
            if core.day+rules['CROPS'][intended]['first_yield_day']>core.final_day:
                choices=[c for c in ['WHEAT','CARROT'] if core.day+rules['CROPS'][c]['max_yield_day']<=core.final_day-1 and rules['CROPS'][c]['seed']<=cash]
                if choices:
                    intended=max(choices,key=lambda c:(core._quote(c,'SELL',rules['CROPS'][c]['max_yield'])-rules['CROPS'][c]['seed'])/(rules['CROPS'][c]['max_yield_day']+1))
            if core.day+rules['CROPS'][intended]['first_yield_day']>core.final_day:
                result.extend(o for o in offers if tuple(o[0])==pos and o[4]!='NEW_ANIMAL')
                continue
            if cash<rules['CROPS'][intended]['seed']:continue
            commands=[];kind='NEW_CROP';priority=0
            if tile is not None:
                if not isinstance(tile,dict):continue
                if tile.get('kind')=='WEED':commands=[['DIG']]
                elif tile.get('kind')=='PLANT':
                    r=rules['CROPS'][tile['crop']]
                    cal=biological_calendar(tile,rules['CROPS'],core.final_day)
                    if core.day<(cal['last_harvest'] or core.final_day):continue
                    if tile.get('yield_units',0)<=0 and not exhausted_perennial(tile,rules['CROPS'],core.day):continue
                    commands=([['HARVEST']] if tile.get('yield_units',0)>0 else [])+([['DIG']] if r['ongoing'] else [])
                    kind='NEW_ROTATION';priority=4
                else:continue
            commands += [['PLANT',intended],['WATER']]
            core.portfolio_proposed_ends[(pos,intended,core.day)]=biological_calendar(dict(crop=intended,planted_day=core.day),rules['CROPS'],core.final_day)['last_harvest']
            result.append((pos,commands,priority,1,kind))
        return result
    def planned_prepare(worker,target,commands,**kwargs):
        steps=prepare(worker,target,commands,**kwargs)
        if steps is None or core.day>=25:return steps
        # Fill for the worker's compact area when a depot visit is already due.
        req=kwargs.get('requirements')
        if req is None:req=core._requirements()[0]
        for index,(cmd,pos) in enumerate(steps):
            if cmd[:2]==['PICKUP','WHEAT']:
                need=sum(bool(w==worker and isinstance(core._tile(p),dict) and core._tile(p).get('animal') and not core._tile(p).get('fed_today')) for p,w in owners.items())
                free=core.private['shed'].get('WHEAT',0)-req['WHEAT']
                steps[index]=(['PICKUP','WHEAT',max(cmd[2],min(need,free))],pos)
        return steps
    core._services=planned_services
    core._growth=planned_growth
    core._prepare_steps=planned_prepare
    core._planned_owner=lambda target:owners.get(tuple(target),-1)
    def planned_certificate(worker,job,offers=None):
        if core.day>=25:return certificate(worker,job,offers)
        offers=planned_services() if offers is None else offers
        required=[(t,[c for c in cmds if c[0] in {'FEED','WATER'}],p,v,'BIOLOGICAL') for t,cmds,p,v,k in offers if any(c[0] in {'FEED','WATER'} for c in cmds)]
        return certificate(worker,job,required)
    core._day_route_certificate=planned_certificate
