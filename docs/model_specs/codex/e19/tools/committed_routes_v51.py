"""D29: admit and execute the same complete observed service routes."""
from collections import Counter
from docs.model_specs.codex.e19.tools.daily_routes_770_v48 import inputs, distance, protected_order

MANDATORY={'FEED','CARE','WATER','HARVEST'}
MOVES={'NORTH':(0,-1),'SOUTH':(0,1),'WEST':(-1,0),'EAST':(1,0)}


def compile_route(start, inventory, sheds, route, return_required):
    """Compile exact pickups and movements; no fair-share or future inventory."""
    if not route:return []
    pos=tuple(start);steps=[];need=Counter()
    for offer in route:need.update(inputs(offer[1]))
    need-=Counter(inventory)
    def travel(dest):
        nonlocal pos
        for axis,negative,positive in [(0,'WEST','EAST'),(1,'NORTH','SOUTH')]:
            while pos[axis]!=dest[axis]:
                cmd=negative if pos[axis]>dest[axis] else positive
                dx,dy=MOVES[cmd];pos=(pos[0]+dx,pos[1]+dy)
                steps.append(([cmd],pos))
    if need:
        travel(min(sheds,key=lambda s:(distance(pos,s)+distance(s,route[0][0]),s)))
        steps.extend((['PICKUP',item,n],pos) for item,n in sorted(need.items()))
    for target,commands,*_ in route:
        travel(target);steps.extend((list(c),pos) for c in commands)
    if any(return_required(o[0],o[1]) for o in route if any(c[0] in {'HARVEST','COLLECT_FERTILIZER'} for c in o[1])):
        travel(min(sheds,key=lambda s:(distance(pos,s),s)));steps.append((['DROP'],pos))
    return steps


def pack_exact(positions,inventories,sheds,offers,budgets,warehouse,return_required):
    routes=[[] for _ in positions];used=Counter();unassigned=[]
    def demand(route,w):
        need=Counter()
        for o in route:need.update(inputs(o[1]))
        return need-Counter(inventories[w])
    def steps(w,route):return compile_route(positions[w],inventories[w],sheds,route,return_required)
    for offer in sorted(offers,key=lambda o:(-int(o[2]==8),-int(bool(inputs(o[1]))),-o[2],o[0])):
        choices=[]
        for w in range(len(positions)):
            if budgets[w]<=0:continue
            old=len(steps(w,routes[w]));oldneed=demand(routes[w],w)
            for slot in range(len(routes[w])+1):
                route=routes[w][:slot]+[offer]+routes[w][slot:]
                if not protected_order(route):continue
                need=used-oldneed+demand(route,w)
                if any(n>warehouse.get(k,0) for k,n in need.items()):continue
                cost=len(steps(w,route))
                if cost<=budgets[w]:choices.append((cost-old,cost,w,slot,route,need))
        if not choices:unassigned.append(offer);continue
        _,_,w,_,route,used=min(choices,key=lambda c:c[:4]);routes[w]=route
    return routes,unassigned


def install(core):
    bootstrap,services,market=core._bootstrap_transition,core._services,core._market_orders
    core.v51_log=[]
    def booked():
        return {tuple(pos) for j in core.active.values() if j.get('v51') for cmd,pos in j['steps'] if cmd[0] in MANDATORY or cmd[0] in {'FERTILIZE','COLLECT_FERTILIZER'}}
    def available():
        offers=services()
        if core.day!=28:return offers
        claimed=booked()
        return [o for o in offers if tuple(o[0]) not in claimed]
    core._services=available
    def plan():
        bootstrap()
        if core.day!=28 or len(core.positions)<2:return
        offers=available();required={}
        for t,commands,p,v,k in offers:
            if k not in {'SERVICE','BIOLOGICAL'}:continue
            commands=[c for c in commands if c[0] in MANDATORY]
            if commands:required[tuple(t)]=(t,commands,p,v,k)
        budgets=[0 if w in core.active else max(0,core.remaining-1) for w in range(len(core.positions))]
        stock=Counter(core.private['shed'])-core._requirements()[0]
        routes,missing=pack_exact(core.positions,core.private['inventories'],core.sheds,list(required.values()),budgets,stock,core._portfolio_return_required)
        for w,route in enumerate(routes):
            if not route:continue
            steps=compile_route(core.positions[w],core.private['inventories'][w],core.sheds,route,core._portfolio_return_required)
            assert len(steps)<=budgets[w]
            core.active[w]=dict(target=route[-1][0],steps=steps,kind='SERVICE',v51=True)
        core.v51_log.append(dict(day=29,hour=core.hour+1,workers=len(routes),assigned=sum(map(len,routes)),unassigned=len(missing),steps=[len(core.active[w]['steps']) if route else 0 for w,route in enumerate(routes)]))
    core._bootstrap_transition=plan
    def orders():
        result=market()
        if core.day!=28 or len(core.positions)<2:return result
        remaining=[o for o in available() if o[4] in {'SERVICE','BIOLOGICAL'} and any(c[0] in MANDATORY for c in o[1])]
        if not remaining:
            core.v51_log.append(dict(day=29,hour=core.hour+1,suppressed_hires=sum(o==['HIRE'] for o in result)))
            return [o for o in result if o!=['HIRE']]
        return result
    core._market_orders=orders
