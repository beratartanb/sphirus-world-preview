"""Queue BEFORE build_funcs.py: rebuild SHM_UpdateBodyTargets only (V2.26 T3c)."""
import builtins
builtins.SHM_ONLY = {"SHM_UpdateBodyTargets"}
print("SHM_ONLY", sorted(builtins.SHM_ONLY))
