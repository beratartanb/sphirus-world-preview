# c_turnch9.py (control job, in-memory; saved later by a gated write job) - round 9: project Relaxed chooser 'Stand Runs' row
# PSD_Relaxed_Stand_Run_F_Turns -> project copy PSD_Sph_R_Run_F_Turns (own schema PSS_Sph_R_Turns). builtins.R9TW sets the trajectory weight.
import unreal as u, builtins
V='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Run_F_Turns.PSD_Relaxed_Stand_Run_F_Turns'
T='/Game/Sphirus/Player/GASP/DB/PSD_Sph_R_Run_F_Turns.PSD_Sph_R_Run_F_Turns'
d=u.load_asset('/Game/Sphirus/Player/GASP/DB/PSD_Sph_R_Run_F_Turns'); s=u.load_asset('/Game/Sphirus/Player/GASP/DB/PSS_Sph_R_Turns'); assert d and s
W=getattr(builtins,'R9TW',None)
if W is not None:
    for c in s.get_editor_property('channels'):
        if c.get_class().get_name()=='PoseSearchFeatureChannel_Trajectory': c.set_editor_property('weight',float(W))
assert d.get_editor_property('schema')==s
u.load_asset('/Game/Sphirus/Player/GASP/Choosers/CHT_Sph_PoseSearchDatabases_Relaxed')
o=u.find_object(None,'/Game/Sphirus/Player/GASP/Choosers/CHT_Sph_PoseSearchDatabases_Relaxed.CHT_Sph_PoseSearchDatabases_Relaxed:Stand Runs'); assert o
back=bool(getattr(builtins,'R9TURN_VENDOR',False)); A,B_=(T,V) if back else (V,T)
rs=list(o.get_editor_property('results_structs')); n=0
for r in rs:
    t=r.export_text()
    if A in t: assert r.import_text(t.replace(A,B_)); n+=1
if n: o.set_editor_property('results_structs',rs)
txt=' '.join(r.export_text() for r in o.get_editor_property('results_structs'))
print('TURNCH9 changed',n,'project in rows',txt.count(T),'vendor in rows',txt.count(V),'W',[c.get_editor_property('weight') for c in s.get_editor_property('channels') if c.get_class().get_name()=='PoseSearchFeatureChannel_Trajectory'])
