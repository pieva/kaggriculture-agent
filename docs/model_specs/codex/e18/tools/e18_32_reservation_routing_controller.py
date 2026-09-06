"""Exclusive batch pickup reservations for planned AND active worker routes."""
from collections import Counter

from docs.model_specs.codex.e18.tools.e18_32_claim_routing_controller import ClaimRoutingController


class ReservationRoutingController(ClaimRoutingController):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.batch_stock=Counter()

    def _observe(self,day,turn,farm,private):
        super()._observe(day,turn,farm,private)
        self.batch_stock=Counter(private['shed'])
        # Active jobs own their next acknowledged pickup before any legacy
        # route can spend it. Completed pickups are already in inventories.
        for job in self.active.values():
            cmd,_=job['steps'][job['index']]
            if cmd[0]=='PICKUP':
                self.batch_stock[cmd[1]]-=min(self.batch_stock[cmd[1]],cmd[2])

    def _planned_or_recovery(self,row,farm,private,worker,key):
        if row['opcode']!='PICKUP':
            return super()._planned_or_recovery(row,farm,private,worker,key)
        snapshot=dict(private)
        snapshot['shed']=dict(+self.batch_stock)
        cmd,emitted=super()._planned_or_recovery(row,farm,snapshot,worker,key)
        if cmd[0]=='PICKUP':
            assert cmd[2]<=self.batch_stock[cmd[1]]
            self.batch_stock[cmd[1]]-=cmd[2]
            self.ready_metrics['exclusively_reserved_pickup_units']+=cmd[2]
        return cmd,emitted
