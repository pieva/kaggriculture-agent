"""Demand-sized routing over unchanged daily crop commitments.

One rule for all days: merge complete tile bundles, include actual early animals,
admit a smaller roster only with a route certificate and recovery/growth slack.
No release-day target, opponent, replay, or benchmark data is consulted.
"""
from collections import Counter, defaultdict
from copy import deepcopy

from docs.model_specs.codex.e18.tools.e18_31_unified_investment_controller import UnifiedInvestmentController
from docs.model_specs.codex.e18.tools.e18_31_assignment_controller import FIB, MOVES, SHED_ACCESS, distance


class DemandRoutingController(UnifiedInvestmentController):
    def __init__(self, plan, seat=0, variant='DEMAND', reference_plan=None):
        super().__init__(deepcopy(plan),seat,reference_plan=reference_plan)
        self.ready_variant=variant
        self.ready_metrics=Counter()
        self.routing_log=[]
        self.repacked_days=set()
        self.demand_observation=None

    @staticmethod
    def _inputs(bundles):
        needed=Counter()
        for _,rows in bundles:
            for row in rows:
                op=row['opcode']
                if op=='FEED':
                    needed['WHEAT']+=1
                elif op=='FERTILIZE':
                    needed['FERTILIZER']+=1
                elif op=='PLACE':
                    needed[row['arguments']['animal']]+=1
        return needed

    @staticmethod
    def _cost(bundles,start):
        if not bundles:
            return 0
        cost=len(DemandRoutingController._inputs(bundles))
        pos=start
        output=False
        for target,rows in bundles:
            cost+=distance(pos,target)+len(rows)
            pos=target
            output=output or any(r['opcode'] in {'HARVEST','COLLECT_FERTILIZER'} for r in rows)
        if output:
            cost+=min(distance(pos,s) for s in SHED_ACCESS)+1
        return cost

    @staticmethod
    def _spawns(hands):
        occupancy=Counter({(4,4):1})
        starts=[(4,4)]
        for _ in range(hands):
            p=min(SHED_ACCESS,key=lambda s:(occupancy[s],SHED_ACCESS.index(s)))
            occupancy[p]+=1
            starts.append(p)
        return starts

    @classmethod
    def _pack(cls,bundles,hands):
        starts=cls._spawns(hands)
        candidates=[]
        # Deterministic geometry/workload orderings, never seeded by a day or
        # simulator seed. Two turns per route remain available for recovery.
        orders=[sorted(bundles,key=lambda b:(len(b[1]),min(distance(b[0],s) for s in SHED_ACCESS),b[0]),reverse=True),
                sorted(bundles,key=lambda b:(b[0][1],b[0][0])),
                sorted(bundles,key=lambda b:(-b[0][1],b[0][0])),
                sorted(bundles,key=lambda b:(b[0][0],b[0][1])),
                sorted(bundles,key=lambda b:(-b[0][0],b[0][1]))]
        for ordered in orders:
            segments=[[] for _ in starts]
            costs=[0]*len(starts)
            feasible=True
            for bundle in ordered:
                choices=[]
                for w,start in enumerate(starts):
                    for insertion in range(len(segments[w])+1):
                        segment=[*segments[w][:insertion],bundle,*segments[w][insertion:]]
                        cost=cls._cost(segment,start)
                        capacity=21 if w<=10 else 19
                        if cost<=capacity:
                            choices.append((cost-costs[w],cost,w,insertion,segment))
                if not choices:
                    feasible=False
                    break
                _,cost,w,_,segment=min(choices,key=lambda c:c[:4])
                segments[w]=segment
                costs[w]=cost
            if feasible:
                candidates.append((sum(costs),max(costs),segments,starts))
        return min(candidates,key=lambda c:c[:2]) if candidates else None

    def _bundles(self,day,farm):
        grouped=defaultdict(list)
        for (d,_),rows in sorted(self.routes.items()):
            if d!=day:
                continue
            for row in rows:
                op=row['opcode']
                if op in {*MOVES,'PASS','PICKUP','DROP'}:
                    continue
                target=tuple(row['position'])
                tile=self._tile(farm,target)
                if tile=='LOCKED':
                    return None
                if op in {'PLACE','BUILD_PASTURE'} and isinstance(tile,dict) and tile.get('animal'):
                    continue
                grouped[target].append(deepcopy(row))
        # Early investments have already changed the biological workload. They
        # must enter the route certificate, not be wished into its spare hours.
        for target in sorted(self.advanced):
            tile=self._tile(farm,target)
            if not isinstance(tile,dict) or not tile.get('animal'):
                continue
            rows=grouped[target]
            ops={r['opcode'] for r in rows}
            for op,field in [('FEED','fed_today'),('CARE','cared_today')]:
                if not tile.get(field) and op not in ops:
                    rows.append(dict(opcode=op,position=list(target),arguments={}))
            for op,field in [('COLLECT_FERTILIZER','fertilizer_available'),('HARVEST','yield_units')]:
                if tile.get(field) and op not in ops:
                    rows.append(dict(opcode=op,position=list(target),arguments={}))
        return list(grouped.items())

    def _materialize(self,day,segments,starts):
        routes={}
        for w,(bundles,start) in enumerate(zip(segments,starts)):
            steps=[]
            p=start
            for item,n in sorted(self._inputs(bundles).items()):
                steps.append((['PICKUP',item,n],p))
            rows=[]
            for cmd,target in steps:
                rows.append(dict(opcode=cmd[0],arguments={'item':cmd[1],'units':cmd[2]},position=list(target)))
            output=False
            for target,actions in bundles:
                steps=[]
                self._walk(steps,p,target)
                rows.extend(dict(opcode=c[0],arguments={},position=list(t)) for c,t in steps)
                rows.extend(deepcopy(actions))
                p=target
                output=output or any(r['opcode'] in {'HARVEST','COLLECT_FERTILIZER'} for r in actions)
            if output:
                shed=min(SHED_ACCESS,key=lambda s:(distance(p,s),s))
                steps=[]
                self._walk(steps,p,shed)
                rows.extend(dict(opcode=c[0],arguments={},position=list(t)) for c,t in steps)
                rows.append(dict(opcode='DROP',position=list(shed),arguments={'expected_items':{}}))
            for index,row in enumerate(rows):
                turn=(2 if w<=10 else 4)+index
                row.update(day=day,worker=w,turn=turn,step=(day-1)*24+turn-1)
            routes[(day,w)]=rows
        return routes

    def _new_day(self,day):
        fresh=day!=self.pool_day
        super()._new_day(day)
        if not fresh or self.demand_observation is None:
            return
        obs=self.demand_observation
        farm,private=obs['farms'][self.seat],obs['private']
        bundles=self._bundles(day,farm)
        old_hands=self.daily_hands.get(day,0)
        if bundles is None:
            self.ready_metrics['fallback_locked_dependency']+=1
            return
        # Leave a complete free route for executable livestock growth. No
        # arbitrary headcount floor tied to a benchmark or calendar checkpoint.
        growth=any(self._tile(farm,t) is None or isinstance(self._tile(farm,t),dict)
                   and self._tile(farm,t).get('kind') in {'WEED','PASTURE'}
                   and not self._tile(farm,t).get('animal')
                   for t,(_,species) in self.pasture_plan.items() if species=='COW')
        growth=bool(growth and farm['money']+sum(private['shed'].get(s,0)*400 for s in ['COW'])>=400)
        selected=None
        for hands in range(old_hands):
            packed=self._pack(bundles,hands)
            if packed:
                total,max_used,segments,starts=packed
                target=hands+int(growth)
                if target>=old_hands:
                    break
                if growth:
                    segments.append([])
                    starts=self._spawns(target)
                selected=(target,total,max_used,segments,starts)
                break
        if selected is None:
            self.ready_metrics['fallback_no_strict_capacity_gain']+=1
            return
        target,total,max_used,segments,starts=selected
        replacement=self._materialize(day,segments,starts)
        before=Counter((tuple(r['position']),r['opcode'],json_key(r['arguments'])) for _,rows in bundles for r in rows)
        after=Counter((tuple(r['position']),r['opcode'],json_key(r['arguments'])) for rows in replacement.values()
                      for r in rows if r['opcode'] not in {*MOVES,'PICKUP','DROP'})
        assert before==after,'No tile obligation may vanish during packing'
        for key in list(self.routes):
            if key[0]==day:
                self.routes[key]=[]
        self.routes.update(replacement)
        self.daily_hands[day]=target
        self.repacked_days.add(day)
        self.ready_metrics['repacked_days']+=1
        self.ready_metrics['avoided_hires']+=old_hands-target
        self.routing_log.append(dict(day=day,old_hands=old_hands,new_hands=target,
            certified_actions=total,maximum_route=max_used,growth_route=growth,
            nominal_payroll_saved=sum(FIB[target:old_hands])))

    def _extra_feed(self,day):
        if day in self.repacked_days:
            # Repacked FEED pickups already include every advanced animal.
            return 0
        return super()._extra_feed(day)

    def _prepare(self,observation,configuration):
        self.demand_observation=observation
        super()._prepare(observation,configuration)


def json_key(value):
    return repr(sorted(value.items()))
