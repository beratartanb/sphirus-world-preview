"""probe233_startdbs.py (measure): ABP CDO values of every PoseSearchDatabase variable whose name contains Start / SHM28 / StartTransfer."""
import unreal as u, json
bp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase')
cdo = u.get_default_object(bp.generated_class())
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out = {}
for v in [str(x) for x in B.list_variables(bp)]:
    if any(k in v for k in ('Start', 'SHM28', 'StandBack')):
        try:
            x = cdo.get_editor_property(v); out[v] = x.get_name() if hasattr(x, 'get_name') else x
        except Exception as e: out[v] = 'err ' + str(e)[:60]
print('STARTDBS233 ' + json.dumps(out, default=str))
