"""Antigravity isolated strategy package."""

from agricola.strategy.antigravity.config import AntigravityConfig
from agricola.strategy.antigravity.agent import AntigravityROIAgent
from agricola.strategy.antigravity.c2_config import AntigravityC2Config
from agricola.strategy.antigravity.c2_policy import AntigravityC2Policy
from agricola.strategy.antigravity.agent_c2 import AntigravityC2Agent
from agricola.strategy.antigravity.c2_50k_config import AntigravityC2_50K_Config
from agricola.strategy.antigravity.antigravity_compact_q0 import (
    AntigravityC2_50K_Policy,
    ANTIGRAVITY_CROP_PLAN,
    ANTIGRAVITY_CROP_POSITIONS,
    ANTIGRAVITY_CROP_ZONES,
    ANTIGRAVITY_PASTURE_POSITIONS,
    ANTIGRAVITY_COHORT_OFFSET,
)
from agricola.strategy.antigravity.agent_c2_50k import (
    AntigravityC2_50K_Agent,
    create_agent,
)

from agricola.strategy.antigravity.c2_75k_config import AntigravityC2_75K_Config
from agricola.strategy.antigravity.antigravity_dual_q0_q1 import (
    AntigravityDualQPolicy,
    DUAL_ROLE_SEQUENCE,
    Q1_CROP_POSITIONS,
    Q1_CROP_ZONES,
    Q1_PASTURE_POSITIONS,
)
from agricola.strategy.antigravity.agent_c2_75k import (
    AntigravityC2_75K_Agent,
    create_agent as create_dual_agent,
)

__all__ = [
    "AntigravityConfig",
    "AntigravityROIAgent",
    "AntigravityC2Config",
    "AntigravityC2Policy",
    "AntigravityC2Agent",
    "AntigravityC2_50K_Config",
    "AntigravityC2_50K_Policy",
    "AntigravityC2_50K_Agent",
    "AntigravityC2_75K_Config",
    "AntigravityDualQPolicy",
    "AntigravityC2_75K_Agent",
    "create_agent",
    "create_dual_agent",
    "ANTIGRAVITY_CROP_PLAN",
    "ANTIGRAVITY_CROP_POSITIONS",
    "ANTIGRAVITY_CROP_ZONES",
    "ANTIGRAVITY_PASTURE_POSITIONS",
    "ANTIGRAVITY_COHORT_OFFSET",
    "DUAL_ROLE_SEQUENCE",
    "Q1_CROP_POSITIONS",
    "Q1_CROP_ZONES",
    "Q1_PASTURE_POSITIONS",
]


