"""State-driven productive idle capacity and executable livestock investments.

One admission rule on every day: observed prerequisites, exclusive resources,
complete route before the next obligation, observed acknowledgement. The inherited
crop programme remains a control, not a reference/opponent trajectory to fit.
"""
from __future__ import annotations

from collections import Counter

from docs.model_specs.codex.e18.tools.e18_30_mission_runtime import (
    MissionRuntimeController, MOVES, SHED_ACCESS, distance, route,
)

CROP_DATA = {
    'WHEAT': (2, 4, 6, 0), 'CARROT': (2, 3, 4, 0),
    'MELON': (10, 12, 6, 0), 'STRAWBERRY': (10, 10, 4, 2),
    'TOMATO': (8, 8, 4, 1),
}
FIB = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144)


class AssignmentController(MissionRuntimeController):
    def __init__(self, plan, seat=0, variant='COMBINED', reference_plan=None):
        super().__init__(plan, seat, 'CROP_POOL', reference_plan)
        if variant not in {'TASKS', 'COWS', 'COMBINED'}:
            raise ValueError(variant)
        self.assignment_variant = variant
        self.assignment_metrics = Counter()
        self.expansion_log = []
        self.advanced = set()
        self.pasture_plan = {
            tuple(r['position']): (r['day'], r['arguments']['animal'])
            for r in plan['trajectory'] if r['opcode'] == 'PLACE'
        }
        self.general_purchase = None

    def _candidate_jobs(self, *args):
        # Replace the old surplus-only pool, without changing its frozen source.
        return None

    def _planned_or_recovery(self, row, farm, private, worker, key):
        target, op = tuple(row['position']), row['opcode']
        tile = self._tile(farm, target)
        if op == 'DIG' and (key[0], target) in self.plant_confirmed and isinstance(tile,dict) and tile.get('planted_day')==key[0]-1:
            self._advance(key)
            return ['PASS'],None
        if op == 'PLANT' and getattr(self,'assignment_clock',(0,0))[1] >= 24:
            # A seed placed in the final executable batch cannot receive its
            # first WATER in a later batch. Do not turn lateness into a death.
            return ['PASS'],None
        if op == 'DIG' and any(j['op']=='PLANT_WATER' and j['target']==target for j in self.active.values()):
            return ['PASS'],None
        if op in {'BUILD_PASTURE', 'PLACE'} and target in self.advanced and isinstance(tile, dict) and tile.get('animal') == 'COW':
            self._advance(key)
            return ['PASS'], None
        if any(j['target'] == target and op in j['claimed_ops'] for j in self.active.values()):
            return ['PASS'], None
        return super()._planned_or_recovery(row, farm, private, worker, key)

    def _new_day(self, day):
        if day != self.pool_day:
            # Remove only pickups corresponding to an acknowledged earlier placement.
            for key, rows in self.routes.items():
                if key[0] != day:
                    continue
                # A pickup supplies a particular worker's placement bundle, not
                # an interchangeable aggregate. Leave the missing cow on its
                # actual owner's route even when other cows were placed early.
                credit = sum(r['opcode']=='PLACE' and tuple(r['position']) in self.advanced
                             for r in rows)
                for row in rows:
                    if credit and row['opcode'] == 'PICKUP' and row['arguments'].get('item') == 'COW':
                        n = min(credit, row['arguments'].get('units', 1))
                        row['arguments']['units'] -= n
                        credit -= n
                        if not row['arguments']['units']:
                            row['opcode'] = 'PASS'
        super()._new_day(day)

    def _remaining_horizon(self, day, turn, requirement_kind, *, horizon_days):
        result = super()._remaining_horizon(day, turn, requirement_kind, horizon_days=horizon_days)
        if requirement_kind == 'pickup':
            result['COW'] -= sum(day < self.pasture_plan[c][0] <= day + horizon_days for c in self.advanced)
        return +result

    def _remaining(self, day, turn, requirement_kind, *, include_tomorrow):
        result = super()._remaining(day, turn, requirement_kind, include_tomorrow=include_tomorrow)
        if requirement_kind == 'pickup' and include_tomorrow:
            result['COW'] -= sum(self.pasture_plan[c][0] == day + 1 for c in self.advanced)
        return +result

    @staticmethod
    def _walk(steps, start, target):
        pos = start
        for command in route(start, target):
            dx, dy = MOVES[command[0]]
            pos = (pos[0] + dx, pos[1] + dy)
            steps.append((command, pos))

    def _observe(self, day, turn, farm, private):
        self._confirmed, self._cancelled = set(), set()
        for key, job in list(self.active.items()):
            if not job.get('emitted'):
                continue
            cmd, target = job['steps'][job['index']]
            op = cmd[0]
            inv = self._inventory(private, job['worker'])
            tile = self._tile(farm, target)
            before = job['before']
            if op in MOVES:
                ok = self._position(farm, job['worker']) == target
            elif op == 'PICKUP':
                ok = inv[cmd[1]] >= before.get(cmd[1], 0) + cmd[2]
            elif op == 'DROP':
                ok = not inv
            elif op == 'DIG':
                ok = tile is None
            elif op == 'PROCURE':
                ok = all(private['shed'].get(k,0) >= n for k,n in job['procure_required'].items())
            elif op == 'BUILD_PASTURE':
                ok = isinstance(tile, dict) and tile.get('kind') == 'PASTURE'
            elif op == 'PLACE':
                ok = isinstance(tile, dict) and tile.get('animal') == cmd[1]
                if ok:
                    if cmd[1]=='COW':
                        self.advanced.add(target)
                    self.expansion_log.append(dict(day=day, hour=turn, target=target, event='placed',species=cmd[1]))
            elif op == 'PLANT':
                ok = isinstance(tile,dict) and tile.get('crop')==cmd[1] and tile.get('planted_day')==day-1
                if ok:
                    self.plant_confirmed.add((day,target))
            elif op in {'FEED', 'CARE', 'WATER'}:
                ok = isinstance(tile, dict) and tile.get({'FEED':'fed_today','CARE':'cared_today','WATER':'watered_today'}[op], False)
            elif op == 'FERTILIZE':
                ok = isinstance(tile, dict) and tile.get('fertilized_until_day', -1) >= day + 1
            elif op in {'COLLECT_FERTILIZER', 'HARVEST'}:
                ok = sum(inv.values()) > sum(before.values())
            else:
                raise ValueError(op)
            # Idempotent acknowledgement: another legitimate worker may finish a
            # service after the offer snapshot. Do not retry an exhausted tile.
            if op == 'COLLECT_FERTILIZER' and isinstance(tile,dict) and not tile.get('fertilizer_available'):
                ok = True
            if op == 'HARVEST' and isinstance(tile,dict) and not tile.get('yield_units',0):
                ok = True
            if op == 'WATER' and (not isinstance(tile,dict) or tile.get('kind') != 'PLANT'):
                ok = True
            job['emitted'] = False
            if ok:
                self.runtime_daily[day]['ack_' + op] += 1
                job['index'] += 1
                if job['index'] == len(job['steps']):
                    self.runtime_daily[day]['missions_completed'] += 1
                    job['phase'], job['ack_turn'] = 'DONE', turn
                    del self.active[key]
            else:
                self.assignment_metrics['unacknowledged_' + op] += 1

    def _row_pending(self, day, op, target):
        return any(r['opcode'] == op and tuple(r['position']) == target
                   for (d, w) in self.routes if d == day for r in self._remaining_rows(day, w))

    def _extra_feed(self, day):
        return sum(self.pasture_plan[c][0] > day for c in self.advanced)

    def _investment_inflight(self):
        return any(j['purchase'] for j in self.active.values())

    def _offers_for_worker(self, day, turn, worker, farm, private, prices):
        pos = self._position(farm, worker)
        inv = self._inventory(private, worker)
        pending = self._remaining_rows(day, worker)
        if pending and pending[0]['turn'] <= turn:
            return []
        fence = min(23, pending[0]['turn'] - 1) if pending else 23
        origin = pos if pending else None
        claims = {j['target'] for j in self.active.values()}
        claims.update(self._position(farm,w) for w,(cmd,_) in enumerate(self.selected)
                      if cmd[0] not in {*MOVES, 'PASS', 'PICKUP', 'DROP'})
        offers = []

        def add(kind, target, service, inputs=None, output=False, value=1, safety=False, purchase=False):
            if target in claims:
                return
            inputs = Counter(inputs or {})
            reserved = Counter()
            reserved['WHEAT'] = self._pending_requirements(day, 'pickup')['WHEAT']
            for j in self.active.values():
                for cmd, _ in j['steps'][j['index']:]:
                    if cmd[0] == 'PICKUP':
                        reserved[cmd[1]] += cmd[2]
            for cmd, _ in self.selected:
                if cmd[0] == 'PICKUP':
                    reserved[cmd[1]] += cmd[2]
            needed = inputs - inv
            deficits = {k:max(0,n-private['shed'].get(k,0)+reserved[k]) for k,n in needed.items()}
            if any(v for k,v in deficits.items() if not (purchase and k in {'COW','SHEEP','WHEAT'})):
                return
            steps = []
            p = pos
            if purchase:
                steps.append((['PROCURE'], pos))
            if needed:
                shed = min(SHED_ACCESS, key=lambda s: distance(p, s) + distance(s, target))
                self._walk(steps, p, shed)
                p = shed
                for item, n in sorted(needed.items()):
                    steps.append((['PICKUP', item, n], p))
            self._walk(steps, p, target)
            for cmd in service:
                steps.append((cmd, target))
            p = target
            if output:
                shed = min(SHED_ACCESS, key=lambda s: distance(p, s) + (distance(s, origin) if origin else 0))
                self._walk(steps, p, shed)
                steps.append((['DROP'], shed))
                p = shed
            if origin is not None:
                self._walk(steps, p, origin)
            if not steps or turn + len(steps) - 1 > fence:
                return
            key = f'{day}:{kind}:{target}:{worker}:{turn}'
            offers.append(dict(key=key, day=day, op=kind, target=target, worker=worker,
                steps=steps, index=0, phase='OUT', origin=origin, fence=fence,
                start_turn=turn, claimed_ops=sorted({c[0] for c in service}),
                score=(int(safety), value/max(1, len(steps)), -len(steps)),
                purchase=purchase, emitted=False,
                procure_required=dict(needed), procurement=deficits))

        # Carried revenue is unavailable for investment until delivered. A worker
        # whose queue is finished is not required to wait for overnight auto-drop.
        if inv and self.assignment_variant != 'COWS':
            shed = min(SHED_ACCESS, key=lambda s: distance(pos, s))
            add('DELIVER', shed, [['DROP']], value=sum(prices.get(k, 0)*n for k,n in inv.items()))
        if inv:
            return offers
        for y, row in enumerate(farm['tiles']):
            for x, tile in enumerate(row):
                target = (x, y)
                if not isinstance(tile, dict) or target in claims:
                    continue
                animal = tile.get('animal')
                if animal:
                    needs_feed = not tile.get('fed_today') and not self._row_pending(day, 'FEED', target)
                    service = []
                    inputs = {}
                    if needs_feed:
                        service.append(['FEED'])
                        inputs['WHEAT'] = 1
                    if not tile.get('cared_today') and not self._row_pending(day, 'CARE', target):
                        service.append(['CARE'])
                    if self.assignment_variant != 'COWS':
                        if tile.get('fertilizer_available'):
                            service.append(['COLLECT_FERTILIZER'])
                        if tile.get('yield_units', 0) > 0:
                            service.append(['HARVEST'])
                    if service:
                        output = any(c[0] in {'HARVEST', 'COLLECT_FERTILIZER'} for c in service)
                        value = prices.get({'COW':'MILK','SHEEP':'WOOL'}[animal], 1)*tile.get('yield_units', 0)
                        value += prices.get('FERTILIZER', 0)*any(c[0]=='COLLECT_FERTILIZER' for c in service)
                        add('ANIMAL_SERVICE', target, service, inputs, output, max(value, 100), needs_feed)
                elif tile.get('kind') == 'PLANT' and self.assignment_variant != 'COWS':
                    water_owners = [w for (d,w) in self.routes if d==day
                                    if any(r['opcode']=='WATER' and tuple(r['position'])==target for r in self._remaining_rows(day,w))]
                    water_risk = bool(water_owners) and min(self._water_eta(day,turn,w,target,farm,self.selected) for w in water_owners) > (23 if day==30 else 24)
                    if not tile.get('watered_today') and (not water_owners or water_risk) and not self._row_pending(day,'PLANT',target):
                        # Only a genuine biological obligation or yield window,
                        # never WATER for the sake of replacing a PASS.
                        crop = CROP_DATA[tile['crop']]
                        age = day - 1 - tile['planted_day']
                        if tile.get('consecutive_unwatered', 0) >= 1 or (not crop[3] and (crop[1]+1)//2 <= age <= crop[1]):
                            add('WATER', target, [['WATER']], value=100, safety=tile.get('consecutive_unwatered', 0)>=1)
        # Keep the predecessor's safety improvement: transfer PLANT and its first
        # WATER together if the original owner cannot finish before refresh.
        emitted_seeds = Counter(c[1] for c,_ in self.selected if c[0]=='PLANT')
        for j in self.active.values():
            for c,_ in j['steps'][j['index']:]:
                if c[0]=='PLANT':
                    emitted_seeds[c[1]] += 1
        for d, owner in self.routes:
            if d != day:
                continue
            rows = self._remaining_rows(day,owner)
            for i,r in enumerate(rows):
                if r['opcode'] != 'PLANT':
                    continue
                target = tuple(r['position'])
                tile = self._tile(farm,target)
                crop = r['arguments']['crop']
                following = next((s for s in rows[i+1:] if s['opcode'] not in {*MOVES,'PASS'}),None)
                preparation = any(s['opcode']=='DIG' and tuple(s['position'])==target for s in rows[:i])
                if (following and following['opcode']=='WATER' and tuple(following['position'])==target
                    and (tile is None or isinstance(tile,dict) and (tile.get('kind')=='WEED' or preparation and tile.get('kind')=='PLANT'))
                    and private['seeds'].get(crop,0) > emitted_seeds[crop]
                    and self._water_eta(day,turn,owner,target,farm,self.selected) > (23 if day==30 else 24)):
                    service = ([['DIG']] if tile is not None else []) + [['PLANT',crop],['WATER']]
                    add('PLANT_WATER',target,service,value=1000,safety=True)
        if self.assignment_variant != 'TASKS':
            for target, (planned_day, species) in self.pasture_plan.items():
                if self._row_pending(day, 'PLACE', target):
                    continue
                tile = self._tile(farm, target)
                # Sheep expansion is not retuned here; repair an already-built
                # but unoccupied planned sheep pasture using the same job rules.
                if species != 'COW' and not (isinstance(tile,dict) and tile.get('kind')=='PASTURE' and not tile.get('animal')):
                    continue
                if tile is not None and not (isinstance(tile, dict) and tile.get('kind') in {'WEED', 'PASTURE'} and not tile.get('animal')):
                    continue
                if 30 - day < 8:  # biological payback horizon, not a phase policy
                    continue
                service = []
                if isinstance(tile, dict) and tile.get('kind') == 'WEED':
                    service.append(['DIG'])
                if tile is None or tile.get('kind') == 'WEED':
                    service.append(['BUILD_PASTURE'])
                service += [['PLACE',species], ['FEED'], ['CARE']]
                purchase = private['shed'].get(species,0) == 0 or private['shed'].get('WHEAT',0) <= self._pending_requirements(day,'pickup')['WHEAT']
                if purchase and (self.general_purchase is not None or self._investment_inflight()):
                    continue
                add('ACTIVATE_COW' if species=='COW' else 'RESTOCK_SHEEP', target, service, {species:1, 'WHEAT':1}, value=800, safety=False, purchase=purchase)
        return offers

    def _prepare(self, observation, configuration):
        self.general_purchase = None
        self.assignment_clock = (observation['day']+1,observation['hour']+1)
        # Reuse baseline selection/ack plumbing, but not its day-gated mission
        # generation. Active general workers are excluded from legacy execution.
        super()._prepare(observation, configuration)
        day, turn = observation['day']+1, observation['hour']+1
        farm, private = observation['farms'][self.seat], observation['private']
        prices = observation['market']['prices']
        # Dynamic harvesting invalidates the old oracle DROP contents. Market
        # finance can use only the inventory actually being delivered now.
        for w,(cmd,row) in enumerate(self.selected):
            if cmd[0]=='DROP':
                self.selected[w] = (cmd, {'opcode':'DROP',
                    'position':list(self._position(farm,w)),
                    'arguments':{'expected_items':dict(self._inventory(private,w))}})
        drop_room = self.shed_capacity - sum(private['shed'].values())
        drop_room -= sum(sum(self._inventory(private,w).values()) for w,(c,_) in enumerate(self.selected) if c[0]=='DROP')
        for worker in range(len(self.selected)):
            running = next((j for j in self.active.values() if j['worker']==worker), None)
            if running is None and self.selected[worker][0][0] == 'PASS':
                offers = self._offers_for_worker(day, turn, worker, farm, private, prices)
                if offers:
                    running = max(offers, key=lambda j: j['score'])
                    if running['purchase']:
                        # Admission is completed by the market budget below.
                        self.general_purchase = running
                        continue
                    self.active[running['key']] = running
                    self.mission_log.append(running)
                    self.runtime_daily[day]['missions_started'] += 1
            if running is None:
                continue
            cmd, target = running['steps'][running['index']]
            if cmd[0] == 'DROP' and sum(self._inventory(private,worker).values()) > drop_room:
                self.assignment_metrics['delivery_capacity_wait'] += 1
                continue
            if cmd[0] == 'DROP':
                drop_room -= sum(self._inventory(private,worker).values())
            running['before'] = dict(self._inventory(private,worker))
            running['emitted'] = True
            row = {'opcode':'DROP', 'position':list(target), 'arguments':{'expected_items':running['before']}} if cmd[0]=='DROP' else None
            self.selected[worker] = (cmd, row)
            self.runtime_daily[day]['extra_'+cmd[0]] += 1

    def _market_orders(self, observation, day, turn):
        orders = super()._market_orders(observation, day, turn)
        farm, private = observation['farms'][self.seat], observation['private']
        prices = observation['market']['prices']
        claims = Counter()
        for job in self.active.values():
            for cmd,_ in job['steps'][job['index']:]:
                if cmd[0]=='PICKUP':
                    claims[cmd[1]] += cmd[2]
        protected = []
        for order in orders:
            if order[0]=='SELL' and claims[order[1]]:
                n = max(0,order[2]-claims[order[1]])
                if n:
                    protected.append(['SELL',order[1],n])
            else:
                protected.append(order)
        orders = protected
        extra = self._extra_feed(day) + (self._extra_feed(day+1) if day<30 else 0)
        if extra:
            # Additional placed animals create real feed obligations even before
            # the old calendar notices them. Never finance growth by selling feed.
            orders = [o for o in orders if o[:2] != ['SELL','WHEAT']]
            needed = self._remaining(day,turn,'pickup',include_tomorrow=day<30)['WHEAT'] + extra
            needed += sum(cmd[2] for cmd,_ in self.selected if cmd[:2]==['PICKUP','WHEAT'])
            already = sum(o[2] for o in orders if o[:2]==['BUY_PRODUCT','WHEAT'])
            shortage = max(0,needed-private['shed'].get('WHEAT',0)-already)
            if shortage and len(orders)<10:
                orders.append(['BUY_PRODUCT','WHEAT',shortage])
        proposed = self.general_purchase
        if proposed is not None:
            species = next(c[1] for c,_ in proposed['steps'] if c[0]=='PLACE')
            buys = [[('BUY_ANIMAL' if k in {'COW','SHEEP'} else 'BUY_PRODUCT'),k,n]
                    for k,n in proposed['procurement'].items() if n]
            owned = sum(t.get('animal')==species for row in farm['tiles'] for t in row if isinstance(t,dict))
            owned += private['shed'].get(species,0) + sum(i.get(species,0) for i in private['inventories'])
            owned += sum(o[2] for o in orders if o[:2]==['BUY_ANIMAL',species])
            cost = self._estimated_cost([o for o in orders if o[0]!='SELL'], observation, farm['hires_today'], len(farm['unlocked_quadrants']))
            revenue = sum(min(o[2],private['shed'].get(o[1],0))*prices[o[1]]*.9 for o in orders if o[0]=='SELL')
            tomorrow_hands = self.daily_hands.get(day+1,0)
            reserve = sum(FIB[:tomorrow_hands])
            # Existing feed is procured by the ordinary obligation ledger. Do
            # not reserve that entire baseline cost a second time against the
            # marginal investment. Reserve the additional animal's feed here.
            reserve += 2*prices['WHEAT']*1.1
            invest_cost = sum({'COW':400,'SHEEP':500}.get(o[1],prices['WHEAT']*1.1)*o[2] for o in buys)
            if owned + proposed['procurement'].get(species,0) <= {'COW':9,'SHEEP':5}[species] and len(orders)+len(buys)<=10 and farm['money']+revenue-cost >= invest_cost+reserve:
                orders.extend(buys)
                proposed.update(before={}, shed_before=private['shed'].get('COW',0), emitted=True)
                self.active[proposed['key']] = proposed
                self.mission_log.append(proposed)
                self.runtime_daily[day]['missions_started'] += 1
                self.expansion_log.append(dict(day=day,hour=turn,event='purchase_admitted',cash=farm['money'],reserve=reserve,target=proposed['target']))
            else:
                self.assignment_metrics['investment_budget_rejected'] += 1
        return orders
