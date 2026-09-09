"""Complete V49C source entry point; frozen V48 plus two bounded corrections."""
from docs.model_specs.codex.e19.tools.daily_route_scheduler_770_v48 import install as install_v48
from docs.model_specs.codex.e19.tools.local_service_770_v49c import install as install_changes


def install(core):
    install_v48(core)
    install_changes(core)
