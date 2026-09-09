"""Antigravity V4 3Q strategy package."""

from agricola.strategy.antigravity.agent_e17_native_3q import (
    AntigravityE17Native3QAgent,
    MODEL_SPEC_VERSION as E17_NATIVE_MODEL_SPEC_VERSION,
    create_agent as create_e17_native_agent,
)
from agricola.strategy.antigravity.agent_c2_3q_v4 import (
    AntigravityC2_3Q_V4_Agent,
    create_agent,
)
from agricola.strategy.antigravity.antigravity_3q_high_density_v4 import (
    AntigravityThreeQHighDensityPolicy,
    V4_SPEC_VERSION,
    create_v4_agent,
)
from agricola.strategy.antigravity.antigravity_e17_native_3q import (
    AntigravityE17NativeThreeQPolicy,
)

from agricola.strategy.antigravity.antigravity_e19_hybrid_livestock_v1 import (
    AntigravityE19HybridLivestockPolicy,
    POLICY_VERSION as E19_HYBRID_MODEL_SPEC_VERSION,
    create_antigravity_e19_agent,
)

__all__ = [
    "AntigravityE17Native3QAgent",
    "AntigravityE17NativeThreeQPolicy",
    "AntigravityC2_3Q_V4_Agent",
    "AntigravityThreeQHighDensityPolicy",
    "AntigravityE19HybridLivestockPolicy",
    "E17_NATIVE_MODEL_SPEC_VERSION",
    "V4_SPEC_VERSION",
    "E19_HYBRID_MODEL_SPEC_VERSION",
    "create_e17_native_agent",
    "create_agent",
    "create_v4_agent",
    "create_antigravity_e19_agent",
]
