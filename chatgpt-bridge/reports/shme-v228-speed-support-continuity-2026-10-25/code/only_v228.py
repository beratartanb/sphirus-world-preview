"""Queue BEFORE build_funcs.py: rebuild SHM_UpdateBodyTargets (V2.28 true-edge landing shift) and SHM_UpdateCameraV21 (V2.28 inspection identity) only."""
import builtins
builtins.SHM_ONLY = {"SHM_UpdateBodyTargets", "SHM_UpdateCameraV21"}
print("SHM_ONLY", sorted(builtins.SHM_ONLY))
