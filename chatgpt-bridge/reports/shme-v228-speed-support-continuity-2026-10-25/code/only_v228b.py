"""Queue BEFORE build_funcs.py: rebuild SHM_UpdateCameraV21 only (V2.28 I5 snap fix)."""
import builtins
builtins.SHM_ONLY = {"SHM_UpdateCameraV21"}
print("SHM_ONLY", sorted(builtins.SHM_ONLY))
