"""V50 candidate J: V49F opening plus input-aware D29 routes and staffing."""
from docs.model_specs.codex.e19.tools.policy_770_v49f import install as previous,adapt
from docs.model_specs.codex.e19.tools.input_routes_v50 import install as routes
from docs.model_specs.codex.e19.tools.workforce_certificate_v50h import install as staffing


def install(core):
    previous(core)
    routes(core)
    staffing(core)
