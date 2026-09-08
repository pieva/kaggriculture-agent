"""Deterministic daily insertion routes for full observed service visits.

Route budgets include travel, commands and depot pickups. They do not assume
future hires. Current-day routes are held until completed or invalidated.
"""
from collections import Counter
from docs.model_specs.codex.e19.tools.biological_plan_770_v18 import install as install_previous


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


def pack_routes(positions,inventories,sheds,offers,budget):
    routes=[[] for _ in positions];unassigned=[]
    for offer in sorted(offers,key=lambda o:(-o[2],o[0])):
        choices=[]
        for w,start in enumerate(positions):
            old=route_cost(start,routes[w],sheds,inventories[w])
            for slot in range(len(routes[w])+1):
                candidate=routes[w][:slot]+[offer]+routes[w][slot:]
                cost=route_cost(start,candidate,sheds,inventories[w])
                if cost<=budget:choices.append((cost-old,cost,w,slot,candidate))
        if not choices:unassigned.append(offer);continue
        _,_,w,slot,route=min(choices,key=lambda c:c[:4]);routes[w]=route
    return routes,unassigned


def renewal_commands(service,renewal):
    # Water that increases the OLD crop's final yield precedes its harvest;
    # the WATER after PLANT belongs to the NEW crop and must remain too.
    return [c for c in service if c[0] in {'WATER','FERTILIZE'}]+renewal


def install(core):
    install_previous(core)
    services,growth,prepare=core._services,core._growth,core._prepare_steps
    day=None;queues={};contracts={};overrides={}
    core.daily_route_log=[]
    core.daily_route_state={}
    def offers_with_routes():
        nonlocal day,queues,contracts,overrides
        current=services()
        if core.day>=25:return current
        if day!=core.day:
            day=core.day
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
                crop=next(c[1] for c in commands if c[0]=='PLANT')
                cost=rules['CROPS'][crop]['seed']
                if cost>budget:continue
                budget-=cost
                overrides[target]=(target,renewal_commands(visits[target][1],commands),priority,value,kind)
            visits.update(overrides)
            # One tick of slack for procurement becoming observed.
            routes,unassigned=pack_routes(core.positions,core.private['inventories'],core.sheds,list(visits.values()),max(0,core.remaining-1))
            queues={w:[tuple(o[0]) for o in route] for w,route in enumerate(routes)}
            contracts={tuple(o[0]):o for route in routes for o in route}
            record=dict(day=day+1,workers=len(routes),budget=core.remaining-1,
                routes=[dict(worker=w,cost=route_cost(core.positions[w],route,core.sheds,core.private['inventories'][w]),visits=[dict(target=o[0],commands=o[1],kind=o[4]) for o in route]) for w,route in enumerate(routes)],
                unassigned=[dict(target=o[0],commands=o[1],kind=o[4]) for o in unassigned])
            core.daily_route_log.append(record)
        claimed={tuple(j['target']) for j in core.active.values() if j['kind']!='DELIVER'}
        by_target={tuple(o[0]):o for o in current}
        for target,o in overrides.items():
            if target in claimed:continue
            tile=core._tile(target)
            if o[4]=='NEW_ANIMAL':
                if isinstance(tile,dict) and tile.get('kind')=='PASTURE' and not tile.get('animal'):by_target[target]=o
            elif target in by_target and isinstance(tile,dict) and tile.get('kind')=='PLANT' and tile.get('yield_units',0)>0:
                by_target[target]=o
        for w,queue in queues.items():
            while queue and (queue[0] not in by_target or queue[0] in claimed):queue.pop(0)
        core.daily_route_state=dict(day=core.day+1,remaining={str(w):list(q) for w,q in queues.items()})
        return list(by_target.values())
    def route_prepare(worker,target,commands,**kwargs):
        if core.day<25:
            target=tuple(target)
            queue=queues.get(worker,[])
            owner=next((w for w,q in queues.items() if target in q),None)
            if owner is not None and (owner!=worker or not queue or queue[0]!=target):return None
            if queue and target!=queue[0]:return None
            contract=contracts.get(target)
            if contract and contract[4]=='NEW_ROTATION' and any(c[0]=='HARVEST' for c in commands):
                if commands!=contract[1]:return None
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
