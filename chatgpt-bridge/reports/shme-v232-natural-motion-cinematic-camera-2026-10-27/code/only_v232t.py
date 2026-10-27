"""Queue BEFORE build_funcs.py: SHM_UpdateBodyTargets only (V2.32 T6 swing target lowered by the pelvis lag after a step-up)."""
import builtins
builtins.SHM_ONLY = {"SHM_UpdateBodyTargets"}
print("SHM_ONLY", sorted(builtins.SHM_ONLY))
