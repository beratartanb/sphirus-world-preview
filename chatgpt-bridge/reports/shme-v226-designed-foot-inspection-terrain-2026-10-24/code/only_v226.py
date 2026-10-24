"""Queue BEFORE build_funcs.py: rebuild SHM_UpdateBodyTargets (T3a/T3b) and SHM_UpdateCameraV21 (I3/I4)."""
import builtins
builtins.SHM_ONLY = {"SHM_UpdateBodyTargets", "SHM_UpdateCameraV21"}
print("SHM_ONLY", sorted(builtins.SHM_ONLY))
