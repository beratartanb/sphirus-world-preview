"""Queue BEFORE build_funcs.py: rebuild SHM_UpdateState (V2.29 effort) and SHM_UpdateCameraV21 (V2.29 walk framing knobs) only."""
import builtins
builtins.SHM_ONLY = {"SHM_UpdateState", "SHM_UpdateCameraV21"}
print("SHM_ONLY", sorted(builtins.SHM_ONLY))
