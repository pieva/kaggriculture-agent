"""Observed D29 workload certificate for each incremental hiring batch."""
from collections import Counter
from docs.model_specs.codex.e19.tools.daily_routes_770_v48 import route_cost,inputs,distance
from docs.model_specs.codex.e19.tools.closed_routes_v50 import pack_routes
from docs.model_specs.codex.e19.tools.workforce_certificate_v50 import spawn


def certified_additions(core,offers,maximum,orders):
    claims={tuple(j['target']) for j in core.active.values() if j['kind']!='DELIVER'}
    visits={tuple(o[0]):o for o in offers if o[4] in {'SERVICE','BIOLOGICAL'} and tuple(o[0]) not in claims}
    warehouse=Counter(core.private['shed'])
    for order in orders:
        if order[0]=='SELL':warehouse[order[1]]-=order[2]
    existing=len(core.positions)
    for count in range(maximum+1):
        starts=list(core.positions)+[spawn(w,len(core.farm['tiles'])) for w in range(existing,existing+count)]
        inventories=[Counter(i) for i in core.private['inventories']]+[Counter() for _ in range(count)]
        budgets=[core.remaining-1]*(existing+count)
        committed_pickups=Counter();outputs=set()
        for w,job in core.active.items():
            budgets[w]-=len(job['steps'])
            for cmd,pos in job['steps']:
                if cmd[0] in {'NORTH','SOUTH','EAST','WEST'}:starts[w]=pos
                elif cmd[0]=='PICKUP':inventories[w][cmd[1]]+=cmd[2];committed_pickups[cmd[1]]+=cmd[2]
                elif cmd[0] in {'FEED','FERTILIZE','PLACE'}:inventories[w].subtract(inputs([cmd]))
                elif cmd[0]=='DROP':inventories[w].clear()
                elif cmd[0] in {'HARVEST','COLLECT_FERTILIZER'}:outputs.add(w)
        if min(budgets)<0:continue
        routes,unassigned=pack_routes(starts,inventories,core.sheds,list(visits.values()),core.remaining-1,budgets,initial_outputs=outputs)
        if unassigned:continue
        pickups=Counter(committed_pickups);costs=[]
        for w,route in enumerate(routes):
            need=Counter()
            for offer in route:need.update(inputs(offer[1]))
            pickups.update(need-inventories[w])
            cost=route_cost(starts[w],route,core.sheds,inventories[w])
            if w in outputs or inventories[w] or any(c[0] in {'HARVEST','COLLECT_FERTILIZER'} for o in route for c in o[1]):
                end=route[-1][0] if route else starts[w]
                cost+=min(distance(end,s) for s in core.sheds)+1
            costs.append(cost)
        if pickups-warehouse:continue
        if all(cost<=budget for cost,budget in zip(costs,budgets)):
            return count,dict(existing=existing,costs=costs,budgets=budgets,visits=len(visits),pickups=dict(pickups))
    return maximum,None


def install(core):
    original=core._market_orders
    core.v50_staffing_log=[]
    def market():
        orders=original();maximum=sum(o==['HIRE'] for o in orders)
        if core.day!=28 or maximum<1:return orders
        count,evidence=certified_additions(core,core._services(),maximum,orders)
        core.v50_staffing_log.append(dict(day=29,hour=core.hour+1,original=maximum,chosen=count,evidence=evidence))
        remaining=count;result=[]
        for order in orders:
            if order==['HIRE']:
                if remaining:result.append(order);remaining-=1
            else:result.append(order)
        return result
    core._market_orders=market
