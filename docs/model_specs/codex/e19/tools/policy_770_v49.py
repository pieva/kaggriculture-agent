"""Complete V49 source entry point; frozen V48 plus two bounded corrections."""
from docs.model_specs.codex.e19.tools.daily_route_scheduler_770_v48 import install as install_v48
from docs.model_specs.codex.e19.tools.workload_770_v49 import install as install_changes


def install(core):
    install_v48(core)
    install_changes(core)
