"""Unified current obligations, short-horizon procurement and executable growth.

No inherited calendar-dependent market overrides: one ledger is used on every
day. Crop targets/routes and daily roster targets remain the experimental control.
"""
from collections import Counter

from docs.model_specs.codex.e18.tools.e18_31_assignment_controller import FIB, SHED_ACCESS
from docs.model_specs.codex.e18.tools.e18_31_obligation_controller import ObligationController

SEEDS={'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}
ANIMALS={'COW':400,'SHEEP':500}


class UnifiedInvestmentController(ObligationController):
    def _investment_inflight(self):
        # Lock unsettled money, not the entire transport/placement mission. After
        # the purchase is observed, the new balance can fund another free worker.
        return any(j['purchase'] and j['index']==0 for j in self.active.values())

    def _market_orders(self, observation, day, turn):
        farm,private=observation['farms'][self.seat],observation['private']
        prices=observation['market']['prices']
        available=Counter(private['shed'])
        seed_stock=Counter(private['seeds'])
        for worker,(cmd,_) in enumerate(self.selected):
            if cmd[0]=='PICKUP':
                available[cmd[1]]-=min(available[cmd[1]],cmd[2])
            elif cmd[0]=='PLANT':
                seed_stock[cmd[1]]-=1
            elif cmd[0]=='DROP' and self._position(farm,worker) in SHED_ACCESS:
                available.update(self._inventory(private,worker))
        available=+available
        current=self._pending_requirements(day,'pickup')
        current_seeds=self._pending_requirements(day,'seed')
        tomorrow=Counter(self.requirements.get(day+1,{}).get('pickup',{})) if day<30 else Counter()
        tomorrow_seeds=Counter(self.requirements.get(day+1,{}).get('seed',{})) if day<30 else Counter()
        tomorrow['COW']-=sum(self.pasture_plan[c][0]==day+1 for c in self.advanced)
        booked_extra_feed=0
        for job in self.active.values():
            for index,(cmd,_) in enumerate(job['steps'][job['index']:],start=job['index']):
                if cmd[0]=='PICKUP' and not (index==job['index'] and job.get('emitted')):
                    current[cmd[1]]+=cmd[2]
                    if cmd[1]=='WHEAT' and job['target'] in self.advanced:
                        booked_extra_feed+=1
        current['WHEAT']+=max(0,self._extra_feed(day)-booked_extra_feed)
        tomorrow['WHEAT']+=self._extra_feed(day+1) if day<30 else 0
        reserve=current+tomorrow
        owned=Counter(private['shed'])
        for inv in private['inventories']:
            owned.update(inv)
        owned.update(t['animal'] for row in farm['tiles'] for t in row if isinstance(t,dict) and t.get('animal'))

        sales=[]
        for item,price in prices.items():
            quantity=max(0,available[item]-reserve[item])
            if quantity:
                sales.append(['SELL',item,quantity])
        sales.sort(key=lambda o:(-prices[o[1]]*o[2],o[1]))
        target_hands=self.daily_hands.get(day,0)
        missing=max(0,target_hands-len(farm['hands']))
        sale_limit=10-min(10,missing) if missing else 4
        if farm['money']<sum(FIB[len(farm['hands']):target_hands]) and sales:
            sale_limit=max(1,sale_limit)
        orders=sales[:min(4,sale_limit)]
        budget=float(farm['money'])
        for order in orders:
            budget+=order[2]*prices[order[1]]*.9
            available[order[1]]-=order[2]

        # Hiring is a daily route prerequisite, not a mid-month policy switch.
        # Late retries are allowed only while the missing route can still run.
        for worker in range(len(farm['hands'])+1,target_hands+1):
            # Slots are append-only identities: an empty legacy route does not
            # permit skipping this hire if later slots have obligations. It also
            # remains capacity for newly admitted livestock missions.
            if turn+1>=24:
                break
            cost=FIB[worker-1]
            if len(orders)>=10 or budget<cost:
                break
            orders.append(['HIRE'])
            budget-=cost

        def buy(op,item,wanted,*,floor=0):
            nonlocal budget
            if wanted<=0 or len(orders)>=10:
                return 0
            cost=SEEDS[item] if op=='BUY_SEED' else ANIMALS[item] if op=='BUY_ANIMAL' else prices[item]*1.1
            quantity=min(int(wanted),max(0,int((budget-floor)//cost)))
            if op=='BUY_ANIMAL':
                quantity=min(quantity,max(0,{'COW':9,'SHEEP':5}[item]-owned[item]))
            if quantity<=0:
                return 0
            orders.append([op,item,quantity])
            budget-=quantity*cost
            (seed_stock if op=='BUY_SEED' else available)[item]+=quantity
            if op=='BUY_ANIMAL':
                owned[item]+=quantity
            return quantity

        # Fund current biological/service commitments before discretionary growth.
        buy('BUY_PRODUCT','WHEAT',max(0,current['WHEAT']-available['WHEAT']))
        for crop,n in sorted(current_seeds.items()):
            buy('BUY_SEED',crop,max(0,n-seed_stock[crop]))
        for species in ANIMALS:
            buy('BUY_ANIMAL',species,max(0,current[species]-available[species]))
        floor=sum(FIB[:self.daily_hands.get(day+1,0)]) if day<30 else 0

        # The next quadrant is purchased for an actual near-term service target,
        # not merely because a numbered day has been reached.
        unlocked=len(farm['unlocked_quadrants'])
        if unlocked<3 and len(orders)<10:
            quadrant=('NE','SW')[unlocked-1]
            needed_land=any(r['day'] in {day,day+1} and r['opcode'] in {'PLANT','BUILD_PASTURE','PLACE'}
                and ('NW' if r['position'][0]<5 and r['position'][1]<5 else
                     'NE' if r['position'][0]>=5 and r['position'][1]<5 else
                     'SW' if r['position'][0]<5 else 'SE')==quadrant
                for r in self.plan['trajectory'])
            land_cost=1000*(2**(unlocked-1))
            if needed_land and budget>=land_cost+floor:
                orders.append(['BUY_LAND'])
                budget-=land_cost

        proposed=self.general_purchase
        if proposed is not None:
            species=next(c[1] for c,_ in proposed['steps'] if c[0]=='PLACE')
            required=Counter(proposed['procure_required'])
            deficits={k:max(0,n-available[k]+current[k]) for k,n in required.items()}
            quote=sum((ANIMALS[k] if k in ANIMALS else prices[k]*1.1)*n for k,n in deficits.items())
            needed_orders=sum(n>0 for n in deficits.values())
            # Reserve new maintenance along with payroll. Already acknowledged
            # feeds are not liabilities, and existing animals are not bought twice.
            maintenance=2*prices['WHEAT']*1.1
            if (len(orders)+needed_orders<=10 and owned[species]+deficits.get(species,0)<= {'COW':9,'SHEEP':5}[species]
                and budget>=quote+floor+maintenance):
                for item,n in deficits.items():
                    buy('BUY_ANIMAL' if item in ANIMALS else 'BUY_PRODUCT',item,n)
                proposed.update(before={},emitted=True)
                self.active[proposed['key']]=proposed
                self.mission_log.append(proposed)
                self.runtime_daily[day]['missions_started']+=1
                self.expansion_log.append(dict(day=day,hour=turn,event='purchase_admitted',target=proposed['target'],reserve=floor+maintenance))
            else:
                self.assignment_metrics['investment_budget_rejected']+=1

        # JIT next-day continuity after current obligations and executable growth.
        buy('BUY_PRODUCT','WHEAT',max(0,reserve['WHEAT']-available['WHEAT']),floor=floor)
        for crop,n in sorted((current_seeds+tomorrow_seeds).items()):
            buy('BUY_SEED',crop,max(0,n-seed_stock[crop]),floor=floor)
        # Overnight staging is limited to the next planned placement, once a full
        # new pickup/build/place/feed/care mission cannot fit today (six steps min).
        if 24-turn<6:
            for species in ANIMALS:
                buy('BUY_ANIMAL',species,max(0,reserve[species]-available[species]),floor=floor)
        return orders
