# m_fp_mode.py (in-memory experiment, NOT saved): FootPlacement pelvis height mode in ABP_Sph_GASP. builtins.FPM = enum name.
import unreal as u, builtins
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP')
n = u.find_object(None, '/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP:AnimGraph.AnimGraphNode_FootPlacement_0')
nd = n.get_editor_property('node'); ps = nd.get_editor_property('pelvis_settings')
before = str(ps.get_editor_property('pelvis_height_mode'))
ps.set_editor_property('pelvis_height_mode', getattr(u.PelvisHeightMode, getattr(builtins, 'FPM', 'FRONT_PLANTED_FEET_UPHILL_FRONT_FEET_DOWNHILL')))
for k, v in (getattr(builtins, 'FPX', None) or {}).items(): ps.set_editor_property(k, v)
nd.set_editor_property('pelvis_settings', ps); n.set_editor_property('node', nd)
u.BlueprintEditorLibrary.compile_blueprint(a)
rb = u.find_object(None, '/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP:AnimGraph.AnimGraphNode_FootPlacement_0').get_editor_property('node').get_editor_property('pelvis_settings').export_text()
print('FPMODE before', before, 'after', rb[:300], 'status', a.get_editor_property('status') if hasattr(a, 'get_editor_property') else '')
