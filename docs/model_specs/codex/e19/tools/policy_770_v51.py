"""Experimental V51C: frozen V49F opening plus committed D29 routes."""
from docs.model_specs.codex.e19.tools.policy_770_v49f import install as previous,adapt
from docs.model_specs.codex.e19.tools.committed_routes_v51c import install as committed

def install(core):
    previous(core)
    committed(core)
