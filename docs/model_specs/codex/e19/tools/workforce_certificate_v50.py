"""D29 hiring bounded by a complete observed-service route packing."""
from collections import Counter
from docs.model_specs.codex.e19.tools.daily_routes_770_v48 import pack_routes,route_cost,inputs,distance


def spawn(worker,board):
    # Engine hand indexes start at one, with a repeating 2x2 spawn pattern.
    mid=board//2-1
    return (mid+worker%2,mid+(worker//2)%2)


def certified_hands(core,offers,maximum):
    claims={tuple(j['target']) for j in core.active.values() if j['kind']!='DELIVER'}
    visits={tuple(o[0]):o for o in offers if o[4] in {'SERVICE','BIOLOGICAL'} and tuple(o[0]) not in claims}
    demand=Counter()
    for offer in visits.values():demand.update(inputs(offer[1]))
    for job in core.active.values():demand.update(inputs([c for c,p in job['steps']]))
    stock=Counter(core.private['shed'])
    for inventory in core.private['inventories']:stock.update(inventory)
    # Planned purchases are not observed inventory. Retain the baseline when
    # the full service input requirement is not already present.
    if demand-stock:return maximum,None
    for count in range(maximum+1):
        starts=[core.positions[0]]+[spawn(w,len(core.farm['tiles'])) for w in range(1,count+1)]
        inventories=[Counter(core.private['inventories'][0])]+[Counter() for _ in range(count)]
        budgets=[core.remaining-1]*(count+1)
        job=core.active.get(0)
        if job:
            budgets[0]-=len(job['steps'])
            for cmd,pos in job['steps']:
                if cmd[0] in {'NORTH','SOUTH','EAST','WEST'}:starts[0]=pos
                elif cmd[0]=='PICKUP':inventories[0][cmd[1]]+=cmd[2]
                elif cmd[0] in {'FEED','FERTILIZE','PLACE'}:inventories[0].subtract(inputs([cmd]))
                elif cmd[0]=='DROP':inventories[0].clear()
        if min(budgets)<0:continue
        routes,unassigned=pack_routes(starts,inventories,core.sheds,list(visits.values()),core.remaining-1,budgets)
        if unassigned:continue
        pickups=Counter()
        for w,route in enumerate(routes):
            need=Counter()
            for offer in route:need.update(inputs(offer[1]))
            pickups.update(need-inventories[w])
        if job:
            for cmd,pos in job['steps']:
                if cmd[0]=='PICKUP':pickups[cmd[1]]+=cmd[2]
        if pickups-Counter(core.private['shed']):continue
        costs=[]
        for w,route in enumerate(routes):
            cost=route_cost(starts[w],route,core.sheds,inventories[w])
            outputs=any(c[0] in {'HARVEST','COLLECT_FERTILIZER'} for o in route for c in o[1])
            outputs=outputs or bool(w==0 and job and any(c[0] in {'HARVEST','COLLECT_FERTILIZER'} for c,p in job['steps']))
            if outputs or inventories[w]:
                end=route[-1][0] if route else starts[w]
                cost+=min(distance(end,s) for s in core.sheds)+1
            costs.append(cost)
        if all(cost<=budget for cost,budget in zip(costs,budgets)):
            return count,dict(costs=costs,budgets=budgets,visits=len(visits))
    return maximum,None


def install(core):
    original=core._market_orders
    core.v50_staffing_log=[]
    def market():
        orders=original()
        maximum=sum(o==['HIRE'] for o in orders)
        if core.day!=28 or core.hour!=0 or len(core.positions)!=1 or maximum<1:return orders
        count,evidence=certified_hands(core,core._services(),maximum)
        core.v50_staffing_log.append(dict(day=29,original=maximum,chosen=count,evidence=evidence))
        remaining=count;result=[]
        for order in orders:
            if order==['HIRE']:
                if remaining:result.append(order);remaining-=1
            else:result.append(order)
        return result
    core._market_orders=market
