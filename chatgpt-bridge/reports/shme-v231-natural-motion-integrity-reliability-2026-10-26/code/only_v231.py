"""Queue BEFORE build_funcs.py: SHM_UpdateRouting (V2.31 forward low-speed reversal in jog mode) + SHM_UpdateBodyTargets (V2.31 T5 step-up lift compensation) + SHM_UpdateCameraV21 (V2.31 inspection resolver use)."""
import builtins
builtins.SHM_ONLY = {"SHM_UpdateBodyTargets", "SHM_UpdateCameraV21", "SHM_UpdateRouting"}
print("SHM_ONLY", sorted(builtins.SHM_ONLY))
