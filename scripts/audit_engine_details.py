"""Test and audit all engine contract mechanisms directly."""

import inspect
import hashlib
from kaggle_environments.envs.kaggriculture import kaggriculture as kag

# 1. Verify Manifest Hash
manifest_lines = [
    ".venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA\t5621f9e36c001c9d1a5fa7832cb46551cb480ad00a2005b2e4539554a7ba8add",
    ".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md\te1a80501a7b02a212eaac9370ada4129a64e0ee6cb3cbc790f3d77d22863fe22",
    ".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md\t3081e52baf8eb2da5d861acc63a3636ce29425f6bdb79a67036ba234ac4ade00",
    ".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json\ta82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867",
    ".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py\tbc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e",
]
manifest_str = "\n".join(manifest_lines)
computed_agg = hashlib.sha256(manifest_str.encode("utf-8")).hexdigest()
print(f"Computed Aggregate SHA: {computed_agg}")
print(f"Expected Aggregate SHA: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d")
print(f"Hash matches exactly: {computed_agg == '4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d'}")

# 2. Inspect _daily_refresh_animals
print("\n=== ANIMAL REFRESH LOGIC ===")
src_anim = inspect.getsource(kag._daily_refresh_animals)
print(src_anim)

# 3. Inspect _daily_refresh_plants & _decay_plants
print("\n=== PLANT REFRESH & DECAY LOGIC ===")
src_plant = inspect.getsource(kag._daily_refresh_plants)
print(src_plant)
src_decay = inspect.getsource(kag._decay_plants)
print(src_decay)

# 4. Inspect _drop_inventories_to_shed & DROP / PLACE in _apply_unit_action
print("\n=== DROP INVENTORIES TO SHED ===")
src_drop = inspect.getsource(kag._drop_inventories_to_shed)
print(src_drop)
