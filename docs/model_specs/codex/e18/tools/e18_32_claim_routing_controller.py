"""Release service obligations on observed completion, not at delivery end."""
from docs.model_specs.codex.e18.tools.e18_32_demand_routing_controller import DemandRoutingController


class ClaimRoutingController(DemandRoutingController):
    def _observe(self,day,turn,farm,private):
        super()._observe(day,turn,farm,private)
        for job in self.active.values():
            remaining={cmd[0] for cmd,target in job['steps'][job['index']:]
                       if target==job['target']}
            old=set(job['claimed_ops'])
            job['claimed_ops']=sorted(old & remaining)
            self.ready_metrics['completed_service_claims_released']+=len(old-set(job['claimed_ops']))
