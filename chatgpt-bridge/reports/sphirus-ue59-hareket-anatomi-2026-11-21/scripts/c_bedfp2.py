# c_bedfp2.py (control job, in-memory; replaces the alpha-by-curve attempt of c_bedfp.py which had no effect at runtime).
# FootPlacement keeps its constant alpha 1; its own disable curves are named instead: pelvis offset (DisablePelvisCurveName) and
# both legs (DisableLegCurveName / DisableLockCurveName) = 'SphNoFootIK'. A_Sph_Bed carries that curve while she is on the bed
# (the clip has no contact curves, so FootPlacement treated the lying feet as planted and lifted the body onto the traced surface).
import unreal as u
P='/Game/Sphirus/Player/GASP/ABP_Sph_GASP'; a=u.load_asset(P); T=u.BlueprintToolset
def node():
    g=[x for x in T.list_graphs(u.load_asset(P)) if x.get_name()=='AnimGraph'][0]
    return [x for x in T.find_nodes(g) if x.get_class().get_name()=='AnimGraphNode_FootPlacement'][0]
n=node(); nd=n.get_editor_property('node'); s=nd.export_text()
assert s.count('SpeedCurveName="contact_r")')==1 and s.count('SpeedCurveName="contact_l")')==1 and s.count('DisablePelvisCurveName=""')==1, 'unexpected node text'
s=s.replace('SpeedCurveName="contact_r")','SpeedCurveName="contact_r",DisableLockCurveName="SphNoFootIK",DisableLegCurveName="SphNoFootIK")')
s=s.replace('SpeedCurveName="contact_l")','SpeedCurveName="contact_l",DisableLockCurveName="SphNoFootIK",DisableLegCurveName="SphNoFootIK")')
s=s.replace('DisablePelvisCurveName=""','DisablePelvisCurveName="SphNoFootIK"')
nd.import_text(s); nd.set_editor_property('alpha_input_type',u.AnimAlphaInputType.FLOAT); nd.set_editor_property('alpha',1.0); nd.set_editor_property('alpha_curve_name','None')
sb=nd.get_editor_property('alpha_scale_bias_clamp'); sb.set_editor_property('scale',1.0); sb.set_editor_property('bias',0.0); nd.set_editor_property('alpha_scale_bias_clamp',sb)
n.set_editor_property('node',nd); u.BlueprintEditorLibrary.compile_blueprint(a)
t=node().get_editor_property('node').export_text()
import re
print('BEDFP2',re.findall(r'LegDefinitions=\(.{0,420}',t)[0][:420]); print('PELVIS',re.findall(r'DisablePelvisCurveName="[^"]*"',t),re.findall(r'AlphaInputType=[A-Za-z]*|,Alpha=[0-9.]*|Scale=[-0-9.]*,Bias=[-0-9.]*',t)[:4],str(u.load_asset(P).get_editor_property('status')))
