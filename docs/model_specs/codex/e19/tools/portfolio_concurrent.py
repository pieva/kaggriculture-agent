"""Allow certified investment alongside nonurgent daily service."""
from docs.model_specs.codex.e19.tools.portfolio_batched import install as install_batched


def install(core):
    install_batched(core)
    services=core._services
    def deadline_services():
        result=[]
        for target,commands,priority,value,kind in services():
            if kind=='BIOLOGICAL':
                tile=core._tile(target)
                urgent=any(c[0]=='FEED' and tile.get('consecutive_unfed',0)>=1 or
                           c[0]=='WATER' and tile.get('consecutive_unwatered',0)>=1
                           for c in commands)
                priority=3 if urgent else 2
            result.append((target,commands,priority,value,kind))
        return result
    core._services=deadline_services
