"""Queue BEFORE build_funcs.py: SHM_UpdateCameraV21 only (B1 retry after the GetPathName node failure; Routing + BodyTargets already built in this editor)."""
import builtins
builtins.SHM_ONLY = {"SHM_UpdateCameraV21"}
print("SHM_ONLY", sorted(builtins.SHM_ONLY))
