"""fpprobe232.py (editor job, read-only): the ABP FootPlacement node settings (pelvis / plant / interpolation / trace) as exported text,
and which of its pins are bound to functions. Prints FPPROBE232 {...}."""
import unreal as u, json, re, sys, pathlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Saved/Codex/GraceRanger_QA_20260914/Scripts'))
from qa_graph import pn, info, obj
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase')
out = {}
for g in B.list_graphs(bp):
    for n in B.find_nodes(g):
        if 'AnimGraphNode_FootPlacement' in n.get_name():
            t = n.get_editor_property('node').export_text()
            for k in ('PelvisSettings', 'PlantSettings', 'InterpolationSettings', 'TraceSettings', 'FootDefinitions'):
                m = re.search(k + r'=\((.*?)\)(,[A-Z]|$)', t)
                out[n.get_name() + '.' + k] = m.group(1)[:900] if m else None
            out[n.get_name() + '.bindings'] = [p.name for p in info(pn(n)).input_pins if p.connected_pins][:20]
print('FPPROBE232 ' + json.dumps(out, default=str))
