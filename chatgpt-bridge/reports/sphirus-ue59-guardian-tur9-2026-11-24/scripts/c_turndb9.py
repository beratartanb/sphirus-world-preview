# c_turndb9.py (control job, in-memory build; saved later by a gated write job with --new) - round 9.
# Project-owned copy of the Relaxed run-turn database with its own schema, so the trajectory / pose balance of turn entry can be set
# without touching the vendor schema PSS_Relaxed_Pivots (shared by every vendor pivot database). Same 8 vendor clips (referenced, not copied).
# builtins.R9TW = trajectory channel weight (vendor 10). The project Relaxed chooser is re-pointed to the copy.
import unreal as u, builtins
EA=u.EditorAssetLibrary; V='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/'
SS=V+'Schemas/PSS_Relaxed_Pivots'; SD=V+'Databases/Relaxed/PSD_Relaxed_Stand_Run_F_Turns'
TS='/Game/Sphirus/Player/GASP/DB/PSS_Sph_R_Turns'; TD='/Game/Sphirus/Player/GASP/DB/PSD_Sph_R_Run_F_Turns'
s=u.load_asset(TS) if EA.does_asset_exist(TS) else EA.duplicate_asset(SS,TS); assert s
W=float(getattr(builtins,'R9TW',4.0))
for c in s.get_editor_property('channels'):
    if c.get_class().get_name()=='PoseSearchFeatureChannel_Trajectory': c.set_editor_property('weight',W)
d=u.load_asset(TD) if EA.does_asset_exist(TD) else EA.duplicate_asset(SD,TD); assert d
d.set_editor_property('schema',s)
names=[d.get_animation_asset(i).get_path_name() for i in range(d.get_num_animation_assets())]
print('TURNDB9 schema',d.get_editor_property('schema').get_path_name(),'W',W,'n',len(names),[n.rsplit('.',1)[-1] for n in names])
c=u.load_asset('/Game/Sphirus/Player/GASP/Choosers/CHT_Sph_PoseSearchDatabases_Relaxed'); objs=[c]
for k in ('nested_choosers','nested_objects'):
    try: objs+=list(c.get_editor_property(k))
    except Exception as e: print('TURNDB9 noprop',k)
n=0
for o in objs:
    try: rs=list(o.get_editor_property('results_structs'))
    except Exception: continue
    ch=False
    for r in rs:
        t=r.export_text()
        if 'PSD_Relaxed_Stand_Run_F_Turns' in t:
            assert r.import_text(t.replace(SD+'.PSD_Relaxed_Stand_Run_F_Turns',TD+'.PSD_Sph_R_Run_F_Turns')); ch=True; n+=1
    if ch: o.set_editor_property('results_structs',rs)
left=sum(1 for o in objs for r in (list(o.get_editor_property('results_structs')) if hasattr(o,'get_editor_property') else []) if 'PSD_Relaxed_Stand_Run_F_Turns' in r.export_text())
print('TURNDB9 chooser rows changed',n,'objects',len(objs),'still vendor',left)
