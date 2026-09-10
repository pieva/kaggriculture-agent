"""Inverse sale-order evidence from own observations and previously emitted actions."""
from collections import Counter
from copy import deepcopy
from itertools import product

def witness(before,after,action,cfg,engine):
    seat=before['player'];orders=action.get('market',[])[:cfg.get('maxMarketOrdersPerTurn',10)]
    if any(not o or o[0] not in ['SELL','BUY_PRODUCT','BUY_SEED','HIRE'] for o in orders):return dict(status='unsupported_own_orders')
    sells=[(i,o) for i,o in enumerate(orders) if o[0] in ['SELL','BUY_PRODUCT']]
    if not any(o[1]=='STRAWBERRY' for _,o in sells):return dict(status='no_own_strawberry')
    if len({o[1] for _,o in sells})!=len(sells):return dict(status='duplicate_own_item')
    farm=deepcopy(before['farms'][seat]);private=deepcopy(before['private']);board=cfg.get('boardSize',10);cap=cfg.get('shedCapacity',100)
    commands=[action.get('farmer',['PASS']),*action.get('hands',[])]
    demand=Counter(c[1] for c in commands if c and c[0]=='PLANT');blocked={c for c,n in demand.items() if n>private['seeds'].get(c,0)}
    for w,c in enumerate(commands):engine._apply_unit_action(farm,private,w,['PASS'] if c and c[0]=='PLANT' and c[1] in blocked else c,board,before['day'],cfg.get('turnsPerDay',24),cap)
    hire_count=after['farms'][seat]['hires_today']-farm['hires_today']
    if hire_count<0:return dict(status='day_boundary')
    hires=sum(engine._hire_cost(farm['hires_today']+i,cfg.get('farmHandCostMult',engine.FARM_HAND_COST_MULT)) for i in range(hire_count))
    fixed_cost=0
    for item,rule in engine.CROPS.items():
        bought=after['private']['seeds'].get(item,0)-private['seeds'].get(item,0)
        if bought<0:return dict(status='inconsistent_seeds')
        fixed_cost+=bought*rule['seed']
    revenue=after['farms'][seat]['money']-farm['money']+hires+fixed_cost
    consume=Counter();step=before['day']*cfg.get('turnsPerDay',24)+before['hour']
    if step%cfg.get('townShopSellInterval',4)==0:
        for shop in before['town']['unlocked_shops']:
            products=engine.SHOPS[shop]
            for item in products:consume[item]+=2 if len(products)==1 else 1
    if step%cfg.get('townCenterSellInterval',24)==0:consume.update(engine.TOWN_CENTER_PRODUCTS)
    options=[];detail=[];max_orders=cfg.get('maxMarketOrdersPerTurn',10)
    for index,o in sells:
        item=o[1];q=private['shed'].get(item,0)-after['private']['shed'].get(item,0)
        sign=1 if o[0]=='SELL' else -1
        if sign*q<0 or abs(q)>o[2]:return dict(status='inconsistent_own_quantity')
        inv=before['market']['inventory'][item];last=after['market']['inventory'][item]+consume[item]
        other=last-inv-q
        if other<0 and item not in ['WHEAT','FERTILIZER']:return dict(status='inconsistent_competing_supply')
        price=lambda stock:engine.market_price(item,stock,before['market'].get('params'))
        if price(inv+max(q,0)+max(other,0))<=1:return dict(status='floor_unidentifiable')
        possibilities=[]
        for category,slots in [('before',list(range(index))),('same',[index]),('after',list(range(index+1,max_orders)))]:
            if not slots:continue
            other_sign=1 if other>=0 else -1
            value=sign*sum(price(inv+sign*j+(other if category=='before' else other_sign*min(j,abs(other)) if category=='same' else 0)-(sign<0)) for j in range(abs(q)))
            possibilities.append((value,slots))
        options.append(possibilities);detail.append(dict(item=item,own_index=index,own_units=q,competing_units=other,operation=o[0]))
    strawberry=next(i for i,d in enumerate(detail) if d['item']=='STRAWBERRY')
    if detail[strawberry]['own_units']==0 or detail[strawberry]['competing_units']==0:return dict(status='no_joint_strawberry_sale')
    positions=set();matches=0
    for combo in product(*options):
        if sum(x[0] for x in combo)==revenue:
            matches+=1;positions.update(combo[strawberry][1])
    if not matches:return dict(status='no_revenue_explanation',revenue=revenue,items=detail)
    label='first' if positions=={0} else 'not_first' if 0 not in positions else None
    return dict(status='identified' if label else 'ambiguous',label=label,possible_positions=sorted(positions),matching_combinations=matches,revenue=revenue,items=detail)

def forecast(evidence):
    labels=[e['label'] for e in evidence if e['status']=='identified']
    return labels[0] if len(labels)>=2 and len(set(labels))==1 else 'abstain'
