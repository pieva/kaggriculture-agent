"""Deterministic bounded route search, with the day planner's short fallback."""
from docs.model_specs.codex.e19.tools.portfolio_day_plan_v14 import install as install_day_plan


def install(core):
    install_day_plan(core)
    certificate=core._day_route_certificate
    state=None
    calls=0
    def bounded_certificate(worker,job,services=None):
        nonlocal state,calls
        now=(core.day,core.hour)
        if state!=now:state,calls=now,0
        # Four route alternatives per observed worker; elapsed wall time never
        # changes policy decisions or reproducibility across machines.
        limit=max(16,4*len(core.positions))
        if calls>=limit:
            core.metrics['portfolio_certificate_budget_exhausted']+=1
            return False
        calls+=1
        core.metrics['portfolio_certificate_evaluations']+=1
        return certificate(worker,job,services)
    core._day_route_certificate=bounded_certificate
