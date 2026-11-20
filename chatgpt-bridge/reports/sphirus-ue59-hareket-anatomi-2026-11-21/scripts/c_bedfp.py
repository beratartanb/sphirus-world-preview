# c_bedfp.py (control job, in-memory; saved later by a gated write job) - 2026-11-21 round 4.
# Bed: the lying pose of A_Sph_Bed fits the bed (pelvis 567.7 vs duvet top ~560), but the GASP FootPlacement node traced the bed /
# station collision under the lying feet as "ground" and lifted the whole body 76 cm (she lay in the air). FootPlacement alpha is
# now 1 - curve 'SphNoFootIK' (absent curve = 0 = unchanged everywhere else); A_Sph_Bed carries the curve while she is on the bed.
import unreal as u
P='/Game/Sphirus/Player/GASP/ABP_Sph_GASP'; a=u.load_asset(P); T=u.BlueprintToolset
g=[x for x in T.list_graphs(a) if x.get_name()=='AnimGraph'][0]
fp=[n for n in T.find_nodes(g) if n.get_class().get_name()=='AnimGraphNode_FootPlacement']; assert len(fp)==1
nd=fp[0].get_editor_property('node')
print('BEFORE',nd.get_editor_property('alpha_input_type'),nd.get_editor_property('alpha'),nd.get_editor_property('alpha_curve_name'),nd.get_editor_property('alpha_scale_bias_clamp').export_text()[:200])
nd.set_editor_property('alpha_input_type',u.AnimAlphaInputType.CURVE); nd.set_editor_property('alpha_curve_name','SphNoFootIK')
sb=nd.get_editor_property('alpha_scale_bias_clamp')
for k,v in (('scale',-1.0),('bias',1.0),('b_clamp_result',True),('clamp_min',0.0),('clamp_max',1.0),('b_map_range',False),('b_interp_result',False)):
    try: sb.set_editor_property(k,v)
    except Exception as e: print('SB?',k,str(e)[:80])
nd.set_editor_property('alpha_scale_bias_clamp',sb); fp[0].set_editor_property('node',nd)
u.BlueprintEditorLibrary.compile_blueprint(a)
nd=[n for n in T.find_nodes([x for x in T.list_graphs(u.load_asset(P)) if x.get_name()=='AnimGraph'][0]) if n.get_class().get_name()=='AnimGraphNode_FootPlacement'][0].get_editor_property('node')
print('AFTER',nd.get_editor_property('alpha_input_type'),nd.get_editor_property('alpha_curve_name'),nd.get_editor_property('alpha_scale_bias_clamp').export_text()[:260])
s=u.load_asset('/Game/Sphirus/Player/Anim/Bed/A_Sph_Bed'); L=u.AnimationLibrary; n='SphNoFootIK'; d=s.get_play_length()
if L.does_curve_exist(s,n,u.RawCurveTrackTypes.RCT_FLOAT): L.remove_curve(s,n,False)
L.add_curve(s,n,u.RawCurveTrackTypes.RCT_FLOAT,False)
L.add_float_curve_keys(s,n,[0.0,0.7,1.2,d-1.2,d-0.6,d],[0.0,0.0,1.0,1.0,0.0,0.0])
print('CURVE',L.does_curve_exist(s,n,u.RawCurveTrackTypes.RCT_FLOAT),d,'status',str(a.get_editor_property('status')))
