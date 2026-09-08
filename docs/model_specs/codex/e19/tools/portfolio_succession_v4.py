"""Observation-driven crop succession experiment on the frozen common core.

Forecasts are conditional valuations, never spendable future income. No Top
coordinates, crop quotas or calendar phases enter the policy.
"""
from collections import Counter
from functools import lru_cache
from math import ceil


def succession_options(day, final_day, rules, quote, action_cost):
    """Compare each first crop with a common continuation value for its plot.

    A plot is released the day after its last harvest. Ongoing crops can be
    removed after any production; removal costs an extra action. Daily service
    includes an estimated move, plus harvest and shared delivery work.
    """
    @lru_cache(None)
    def choices(start):
        options = {}
        for name, rule in rules.items():
            first = start + rule['first_yield_day']
            if first > final_day:
                continue
            ends = (range(first, min(final_day, start+rule['max_yield_day'])+1)
                    if not rule['ongoing'] else
                    range(first, min(final_day,first+(rule['max_yield']-1)*rule['interval'])+1,rule['interval']))
            for end in ends:
                if rule['ongoing']:
                    flows = [(d,1) for d in range(first,end+1,rule['interval'])]
                else:
                    waters = max(0,end-start-ceil(rule['max_yield_day']/2)+1)
                    flows = [(end,min(rule['max_yield'],1+waters))]
                fertilizer_cost=0
                fertilizer_actions=0
                if rule['ongoing']:
                    boosted=[]
                    covered=-1
                    for d,n in flows:
                        if d-1>covered:
                            events=[(when,units) for when,units in flows if d<=when<=d+2]
                            benefit=sum(quote(name,when,2*units)-quote(name,when,units) for when,units in events)
                            cost=quote('FERTILIZER',d-1,1)
                            if benefit>cost+2*action_cost:
                                covered=d+1
                                fertilizer_cost+=cost
                                fertilizer_actions+=2
                        boosted.append((d,2*n if d-1<=covered else n))
                    flows=boosted
                revenue = sum(quote(name,d,n) for d,n in flows)
                work = 1 + 2*(end-start+1) + 3*len(flows) + int(rule['ongoing']) + fertilizer_actions
                profit = revenue-rule['seed']-fertilizer_cost-action_cost*work
                continuation = best(end+1)
                total = profit+continuation
                row = dict(crop=name,end=end,gain=profit,revenue=revenue,work=work,
                           total=total,continuation=continuation,fertilizer_cost=fertilizer_cost)
                if name not in options or total>options[name]['total']:
                    options[name]=row
        return options

    @lru_cache(None)
    def best(start):
        if start>final_day:
            return 0.0
        return max([best(start+1)]+[v['total'] for v in choices(start).values()])

    waiting = best(day+1)
    return {c:dict(v,admission_value=v['total']/max(1,final_day-day+1) if v['gain']>0 else 0, waiting_value=waiting) for c,v in choices(day).items()}


def install(core):
    from docs.model_specs.codex.e19.tools.productive_continuity import install as essential
    essential(core)
    namespace=core.__call__.__func__.__globals__
    rules={c:namespace['CROPS'][c] for c in core.profile.crops}
    # Average observed-price wage budget at the configured maximum staffing.
    a,b,total=1,1,0
    for _ in range(core.profile.maximum_hands):
        total+=a
        a,b=b,a+b
    original_growth=core._growth
    original_services=core._services
    acknowledge=core._acknowledge
    proposed_ends={}
    planted_ends={}
    core.portfolio_planted_ends=planted_ends
    memo={}

    def acknowledge_planting():
        for worker,(command,target,before) in list(core.previous.items()):
            if command[0]=='PLANT':
                tile=core._tile(target)
                if isinstance(tile,dict) and tile.get('crop')==command[1] and tile.get('planted_day')==core.day:
                    end=proposed_ends.get((tuple(target),command[1],core.day))
                    if end is not None:planted_ends[(tuple(target),core.day)]=end
        acknowledge()
    core._acknowledge=acknowledge_planting

    def services():
        result=[]
        for target,commands,priority,value,kind in original_services():
            tile=core._tile(target)
            end=planted_ends.get((tuple(target),tile.get('planted_day')))
            if end is not None and core.day>=end and tile.get('yield_units',0)>0 and ['HARVEST'] not in commands:
                commands=commands+[['HARVEST']]
                value+=core._quote(tile['crop'],'SELL',tile['yield_units'])
            result.append((target,commands,priority,value,kind))
        represented={tuple(r[0]) for r in result}
        claims={tuple(j['target']) for j in core.active.values() if j['kind']!='DELIVER'}
        for y,row in enumerate(core.farm['tiles']):
            for x,tile in enumerate(row):
                target=(x,y)
                if target in represented or target in claims or not isinstance(tile,dict) or tile.get('kind')!='PLANT':
                    continue
                end=planted_ends.get((target,tile['planted_day']))
                if end is not None and core.day>=end and tile.get('yield_units',0)>0:
                    result.append((target,[['HARVEST']],0,core._quote(tile['crop'],'SELL',tile['yield_units']),'SERVICE'))
        return result
    core._services=services

    def plan():
        # Active seeds change marginal supply even before PLANT is observed.
        _,reserved=core._requirements()
        key=(core.day,core.hour,tuple(sorted(reserved.items())))
        if key in memo:
            return memo[key]
        memo.clear()
        scheduled={c:Counter() for c in rules}
        for row in core.farm['tiles']:
            for tile in row:
                if not isinstance(tile,dict) or tile.get('kind')!='PLANT':
                    continue
                c=tile['crop'];rule=rules[c];planted=tile['planted_day']
                scheduled[c][core.day]+=tile.get('yield_units',0)
                if rule['ongoing']:
                    for i in range(rule['max_yield']):
                        d=planted+rule['first_yield_day']+i*rule['interval']
                        if d>core.day:scheduled[c][d]+=1
                else:
                    end=planted+rule['max_yield_day']
                    if end>core.day:
                        remaining_waters=max(0,end-max(core.day,planted+ceil(rule['max_yield_day']/2)-1))
                        scheduled[c][end]+=min(remaining_waters,max(0,rule['max_yield']-tile.get('yield_units',0)))
        for c,n in reserved.items():
            rule=rules[c]
            if rule['ongoing']:
                for i in range(rule['max_yield']):
                    scheduled[c][core.day+rule['first_yield_day']+i*rule['interval']]+=n
            else:
                scheduled[c][core.day+rule['max_yield_day']]+=n*(1+rule['max_yield_day']-ceil(rule['max_yield_day']/2)+1)
        animals=sum(bool(t.get('animal')) for row in core.farm['tiles'] for t in row if isinstance(t,dict))
        params=core.market.get('params',core.market_params)

        @lru_cache(None)
        def quote(c,d,n):
            if c=='FERTILIZER':
                return core._quote(c,'BUY',n)
            supply=sum(v for when,v in scheduled[c].items() if when<=d)
            inventory=core.market['inventory'][c]+supply
            if c=='WHEAT':
                # Feeding is a demand sink in our conditional market scenario.
                # Do not credit it as available cash or assume opponent actions.
                inventory-=animals*max(0,d-core.day)
            prices=[core.market_price(c,inventory+i,params) for i in range(n)]
            return core.envelope.conservative(c,'SELL',prices)
        options=succession_options(core.day,core.final_day,rules,quote,
            total*core.hire_mult/max(1,core.turns*(core.profile.maximum_hands+1)))
        memo[key]=options
        core.portfolio_latest=options
        return options

    def growth(cash_free):
        options=plan()
        # Replace the old single-cycle eligibility filter as well as the score.
        core.crop_values={c:dict(core.crop_values[c],gain=options.get(c,{}).get('admission_value',0)) for c in rules}
        result=[]
        for target,commands,priority,value,kind in original_growth(cash_free):
            if kind=='NEW_CROP':
                crop=next(c[1] for c in commands if c[0]=='PLANT')
                value=options.get(crop,{}).get('admission_value',0)
                if value<=0:
                    core.metrics['portfolio_reject_value']+=1
                    continue
                proposed_ends[(tuple(target),crop,core.day)]=options[crop]['end']
            result.append((target,commands,priority,value,kind))
        # Offer an entire replacement mission alongside the standalone harvest.
        # NEW_ routes use the existing day certificate and reserve shared seeds.
        positive=[r for r in options.values() if r['admission_value']>0]
        if positive:
            next_crop=max(positive,key=lambda r:(r['admission_value'],r['crop']))['crop']
            if cash_free>=rules[next_crop]['seed']:
                for target,commands,priority,value,kind in services():
                    tile=core._tile(target)
                    if tile.get('kind')!='PLANT' or ['HARVEST'] not in commands:
                        continue
                    rule=rules[tile['crop']]
                    last=tile['planted_day']+rule['first_yield_day']+(rule['max_yield']-1)*rule['interval']
                    end=planted_ends.get((tuple(target),tile['planted_day']),last)
                    if rule['ongoing'] and core.day<end:
                        continue
                    renewal=commands+([['DIG']] if rule['ongoing'] else [])+[['PLANT',next_crop],['WATER']]
                    result.append((target,renewal,priority,value+options[next_crop]['admission_value'],'NEW_ROTATION'))
                    proposed_ends[(tuple(target),next_crop,core.day)]=options[next_crop]['end']
        return result

    core._growth=growth
    core.portfolio_latest={}
