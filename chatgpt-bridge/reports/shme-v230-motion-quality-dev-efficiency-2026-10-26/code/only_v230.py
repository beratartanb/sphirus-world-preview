"""Queue BEFORE build_funcs.py: rebuild SHM_UpdateRouting (V2.30 low-speed reversal class) + SHM_UpdateCameraV21 (null-safe inspection)."""
import builtins
builtins.SHM_ONLY = {"SHM_UpdateRouting", "SHM_UpdateCameraV21"}
print("SHM_ONLY", sorted(builtins.SHM_ONLY))
