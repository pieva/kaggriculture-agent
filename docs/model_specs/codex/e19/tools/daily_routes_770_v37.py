"""Deterministic daily insertion routes for full observed service visits.

Route budgets include travel, commands and depot pickups. They do not assume
future hires. Current-day routes are held until completed or invalidated.
"""
from collections import Counter
from docs.model_specs.codex.e19.tools.biological_plan_770_v25 import install as install_previous


def distance(a,b):return abs(a[0]-b[0])+abs(a[1]-b[1])


def inputs(commands):
    result=Counter()
    for c in commands:
        if c[0]=='FEED':result['WHEAT']+=1
        elif c[0]=='FERTILIZE':result['FERTILIZER']+=1
        elif c[0]=='PLACE':result[c[1]]+=1
    return result


def route_cost(start, route, sheds, inventory):
    need=Counter()
    for offer in route:need.update(inputs(offer[1]))
    missing=need-Counter(inventory)
    pos=start;cost=0
    if missing and route:
        pos=min(sheds,key=lambda s:(distance(start,s)+distance(s,route[0][0]),s))
        cost=distance(start,pos)+len(missing)
    for target,commands,*rest in route:
        cost+=distance(pos,target)+len(commands);pos=target
    return cost


def pack_routes(positions,inventories,sheds,offers,budget,budgets=None):
    routes=[[] for _ in positions];unassigned=[]
    for offer in sorted(offers,key=lambda o:(-o[2],o[0])):
        choices=[]
        for w,start in enumerate(positions):
            old=route_cost(start,routes[w],sheds,inventories[w])
            for slot in range(len(routes[w])+1):
                candidate=routes[w][:slot]+[offer]+routes[w][slot:]
                cost=route_cost(start,candidate,sheds,inventories[w])
                if cost<=(budget if budgets is None else budgets[w]):choices.append((cost-old,cost,w,slot,candidate))
        if not choices:unassigned.append(offer);continue
        _,_,w,slot,route=min(choices,key=lambda c:c[:4]);routes[w]=route
    return routes,unassigned


def renewal_commands(service,renewal):
    # Water that increases the OLD crop's final yield precedes its harvest;
    # the WATER after PLANT belongs to the NEW crop and must remain too.
    return [c for c in service if c[0] in {'WATER','FERTILIZE'}]+renewal


def harvest_due(tile, day, turns=24):
    """Reserve collection on the last full day before decay, or overdue."""
    return (isinstance(tile,dict) and tile.get('kind')=='PLANT'
            and tile.get('yield_units',0)>0 and tile.get('max_lifespan_step',-1)>=0
            and tile['max_lifespan_step'] <= (day+1)*turns)


def install(core):
    install_previous(core)
    services,growth,prepare=core._services,core._growth,core._prepare_steps
    day=None;queues={};contracts={};overrides={};staff=None;checkpoint=None;land=None
    pending={};ready_stamp=None
    core.succession_log=[]
    core.daily_route_log=[]
    core.daily_route_state={}
    def deadline_late(target):
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
        return late
    def offers_with_routes():
        nonlocal day,queues,contracts,overrides,staff,checkpoint,land,ready_stamp
        current=services()
        # A due harvest is an existing obligation, never contingent on funding
        # or certifying a replacement crop. Optional inputs cannot delay it.
        current=[(t,[['HARVEST']],6,v,'SERVICE') if harvest_due(core._tile(t),core.day,core.turns) and any(c[0]=='HARVEST' for c in cmds) else (t,cmds,p,v,k) for t,cmds,p,v,k in current]
        # Persist the next visit independently of harvest admission. The
        # previous planting identity prevents a renewed tile being renewed twice.
        for y,row in enumerate(core.farm['tiles']):
            for x,tile in enumerate(row):
                target=(x,y)
                if harvest_due(tile,core.day,core.turns) and target not in pending:
                    pending[target]=(tile['crop'],tile['planted_day'])
                    core.succession_log.append(dict(day=core.day+1,event='reserved',target=target))
        for target,identity in list(pending.items()):
            tile=core._tile(target)
            if isinstance(tile,dict) and tile.get('kind')=='PLANT' and (tile['crop'],tile['planted_day'])!=identity:
                del pending[target]
                core.succession_log.append(dict(day=core.day+1,event='observed_replant',target=target))
        if core.day>=25:return current
        ready=tuple(sorted(t for t in pending if core._tile(t) is None or isinstance(core._tile(t),dict) and core._tile(t).get('kind')=='WEED'))
        observed_land=tuple(sorted(core.farm["unlocked_quadrants"]))
        if day!=core.day or staff!=len(core.positions) or checkpoint!=core.hour//6 or land!=observed_land or ready!=ready_stamp:
            ready_stamp=ready
            land=observed_land
            day=core.day;staff=len(core.positions);checkpoint=core.hour//6
            req,seeds=core._requirements()
            cash=core.farm['money']-max(core.maintenance_floor,core.feed_reserve)
            proposals=growth(cash)
            visits={tuple(o[0]):o for o in current};overrides={}
            budget=cash
            owned=core._owned();targets=core.profile.species_targets()
            rules=core.__call__.__func__.__globals__
            # Complete the existing empty structures, without buying new land.
            for o in proposals:
                target,commands,priority,value,kind=o
                if kind!='NEW_ANIMAL' or target in overrides:continue
                tile=core._tile(target)
                species=next(c[1] for c in commands if c[0]=='PLACE')
                price=rules['ANIMALS'][species]['cost']
                if not isinstance(tile,dict) or tile.get('kind')!='PASTURE' or tile.get('animal'):continue
                if owned[species]>=targets[species] or price>budget:continue
                owned[species]+=1;budget-=price
                overrides[target]=(target,commands,3,value,kind)
            for o in proposals:
                target,commands,priority,value,kind=o
                if kind!='NEW_ROTATION' or target not in visits:continue
                # Due annual harvests may include a certified same-visit successor.
                crop=next(c[1] for c in commands if c[0]=='PLANT')
                cost=rules['CROPS'][crop]['seed']
                if cost>budget:continue
                budget-=cost
                overrides[target]=(target,renewal_commands(visits[target][1],commands),7 if harvest_due(core._tile(target),core.day,core.turns) else priority,value,kind)
            # Replanting a released plot is part of the route workload, not
            # merely a low-ranked alternative outside its worker's queue.
            for o in proposals:
                target,commands,priority,value,kind=o
                if target not in ready or kind!='NEW_CROP':continue
                crop=next(c[1] for c in commands if c[0]=='PLANT')
                cost=rules['CROPS'][crop]['seed']
                if cost>budget:continue
                budget-=cost
                overrides[target]=(target,commands,4,value,kind)
            visits.update(overrides)
            # One tick of slack for procurement becoming observed.
            starts=list(core.positions)
            inventories=[Counter(inv) for inv in core.private['inventories']]
            budgets=[max(0,core.remaining-1) for _ in starts]
            for w,job in core.active.items():
                budgets[w]=max(0,budgets[w]-len(job['steps']))
                if job['steps']:starts[w]=job['steps'][-1][1]
                for cmd,pos in job['steps']:
                    if cmd[0]=='PICKUP':inventories[w][cmd[1]]+=cmd[2]
                    elif cmd[0] in {'FEED','FERTILIZE','PLACE'}:
                        inventories[w].subtract(inputs([cmd]))
                    elif cmd[0]=='DROP':inventories[w].clear()
            routes,unassigned=pack_routes(starts,inventories,core.sheds,list(visits.values()),max(0,core.remaining-1),budgets)
            queues={w:[tuple(o[0]) for o in route] for w,route in enumerate(routes)}
            contracts={tuple(o[0]):o for route in routes for o in route}
            record=dict(day=day+1,hour=core.hour+1,workers=len(routes),budget=core.remaining-1,
                routes=[dict(worker=w,cost=route_cost(starts[w],route,core.sheds,inventories[w]),available=budgets[w],visits=[dict(target=o[0],commands=o[1],kind=o[4]) for o in route]) for w,route in enumerate(routes)],
                unassigned=[dict(target=o[0],commands=o[1],kind=o[4]) for o in unassigned])
            core.daily_route_log.append(record)
        claimed={tuple(j['target']) for j in core.active.values() if j['kind']!='DELIVER'}
        by_target={tuple(o[0]):o for o in current}
        for target,o in overrides.items():
            if target in claimed:continue
            tile=core._tile(target)
            if o[4]=='NEW_ANIMAL':
                if isinstance(tile,dict) and tile.get('kind')=='PASTURE' and not tile.get('animal'):by_target[target]=o
            elif o[4]=='NEW_CROP' and target in ready:
                by_target[target]=o
            elif target in by_target and isinstance(tile,dict) and tile.get('kind')=='PLANT' and tile.get('yield_units',0)>0:
                by_target[target]=o
        for w,queue in queues.items():
            while queue and (queue[0] not in by_target or queue[0] in claimed):queue.pop(0)
        core.daily_route_state=dict(day=core.day+1,remaining={str(w):list(q) for w,q in queues.items()})
        result=list(by_target.values())
        # Failure to admit a successor must never prevent the due harvest.
        for o in current:
            if o[2]==6 and overrides.get(tuple(o[0]),(None,None,None,None,None))[4]=='NEW_ROTATION':
                result.append(o)
        if core.day<25:
            for target,o in by_target.items():
                tile=core._tile(target)
                if isinstance(tile,dict) and tile.get('kind')=='PLANT' and tile.get('consecutive_unwatered',0)>=1 and not tile.get('watered_today') and (core.remaining<=6 or deadline_late(tuple(target))):
                    result.append((target,[['WATER']],8,1,'SERVICE'))
                elif isinstance(tile,dict) and tile.get('animal') and tile.get('consecutive_unfed',0)>=1 and not tile.get('fed_today') and (core.remaining<=6 or deadline_late(tuple(target))):
                    result.append((target,[['FEED']],8,1,'SERVICE'))
        return result
    def route_prepare(worker,target,commands,**kwargs):
        if core.day<25:
            target=tuple(target)
            tile=core._tile(target)
            urgent=(commands in [[['WATER']],[['FEED']]] and isinstance(tile,dict) and
                    (commands==[['WATER']] and tile.get('consecutive_unwatered',0)>=1 or
                     commands==[['FEED']] and tile.get('consecutive_unfed',0)>=1))
            late=deadline_late(target) if urgent else False
            rescue=(any(cmd[0]=='HARVEST' for cmd in commands) and harvest_due(tile,core.day,core.turns)) or (urgent and (late or core.remaining<=6))
            queue=[] if rescue else queues.get(worker,[])
            owner=None if rescue else next((w for w,q in queues.items() if target in q),None)
            # A provisional replant reservation must not block executable
            # services while its own funding/capacity certificate is pending.
            planting=any(cmd[0]=='PLANT' for cmd in commands)
            if not planting:
                if queue and contracts.get(queue[0],(None,None,None,None,None))[4]=='NEW_CROP':queue=[]
                if owner is not None and contracts.get(target,(None,None,None,None,None))[4]=='NEW_CROP':owner=None
            if owner is not None and (owner!=worker or not queue or queue[0]!=target):return None
            if queue and target!=queue[0]:return None
            contract=contracts.get(target)
            if contract and contract[4]=='NEW_ROTATION' and any(c[0]=='HARVEST' for c in commands):
                if commands!=contract[1] and not (commands==[['HARVEST']] and harvest_due(tile,core.day,core.turns)):return None
            if contract and contract[4]=='NEW_ANIMAL' and any(c[0]=='PLACE' for c in commands):
                if [c for c in commands if c[0]=='PLACE']!=[c for c in contract[1] if c[0]=='PLACE']:return None
        steps=prepare(worker,target,commands,**kwargs)
        if steps is None or core.day>=25:return steps
        demand=Counter()
        for p in queues.get(worker,[]):demand.update(inputs(contracts[p][1]))
        demand-=Counter(core.private['inventories'][worker])
        req=kwargs.get('requirements')
        if req is None:req=core._requirements()[0]
        for i,(cmd,pos) in enumerate(steps):
            if cmd[0]=='PICKUP' and cmd[1] in {'WHEAT','FERTILIZER'}:
                free=core.private['shed'].get(cmd[1],0)-req[cmd[1]]
                steps[i]=(['PICKUP',cmd[1],max(cmd[2],min(demand[cmd[1]],free))],pos)
        return steps
    core._services=offers_with_routes
    core._prepare_steps=route_prepare
