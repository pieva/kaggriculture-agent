from __future__ import annotations

from docs.model_specs.codex.e18.tools.e18_22_wheat_jit_d1_controller import (
    WheatJitD1Controller,
)
from docs.model_specs.codex.e18.tools.e18_23_sw_unlock_liquidity_controller import (
    SwUnlockLiquidityController,
)


def test_only_static_policy_change_is_one_day_earlier_activation() -> None:
    assert WheatJitD1Controller.activation_day == 11
    assert SwUnlockLiquidityController.activation_day == 10
    assert (
        SwUnlockLiquidityController.procurement_horizon_days
        == WheatJitD1Controller.procurement_horizon_days
        == 1
    )
