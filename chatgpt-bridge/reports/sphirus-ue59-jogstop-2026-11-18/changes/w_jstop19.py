# w_jstop19.py (write, gated, manifest ue59_m19_jstop): fit the stop selection to Sphirus gait speeds.
# Root cause: the Stand Idles sub-chooser picks the stop database by Speed2D at the first idle frame with GASP Relaxed bands
# (walk stops 20-170, run stops 170-400, sprint stops 400+). Sphirus walks 180 and jogs 415, so every jog release fell in the
# sprint band (deep Relaxed sprint stop, 29-32 cm pelvis drop) and walk releases fell in the run band.
# 1) CHT_Sph_PoseSearchDatabases_Relaxed:Stand Idles Speed2D bands -> 20-200 / 200-440 / 440+ (Sphirus-owned chooser copy)
# 2) ABP_Sph_GASP remap: drop Relaxed_Stand_Run_Stops -> Dense and Relaxed_Stand_Walk_Stops -> Dense, so the gentle Relaxed
#    run (375 cm/s) / walk stops that fit the PhysBrake deceleration are used (runtime A/B T11 C1 vs C2).
# 3) discard the unsaved bias test copies (never saved, not on disk).
import unreal as u, re
L = u.BlueprintEditorLibrary; EAL = u.EditorAssetLibrary
CP = '/Game/Sphirus/Player/GASP/Choosers/CHT_Sph_PoseSearchDatabases_Relaxed'
ch = u.load_asset(CP); s = u.find_object(None, CP + '.CHT_Sph_PoseSearchDatabases_Relaxed:Stand Idles')
cols = list(s.get_editor_property('columns_structs')); t = cols[0].export_text(); assert 'Speed2D' in t
old = '(Min=20.000000,Max=170.000000),(Min=170.000000,Max=400.000000),(Min=400.000000,Max=999'
new = '(Min=20.000000,Max=200.000000),(Min=200.000000,Max=440.000000),(Min=440.000000,Max=999'
assert t.count(old) == 1, 'bands not at shipped values'
cols[0].import_text(t.replace(old, new)); s.modify(); s.set_editor_property('columns_structs', cols); ch.modify()
t2 = s.get_editor_property('columns_structs')[0].export_text(); assert new in t2; print('BANDS', re.search(r'RowValues=\(\(Max=20\.000000\),(.*?bNoMax=True\))', t2).group(1))
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); c = u.get_default_object(a.generated_class())
ks = list(c.get_editor_property('CM_Keys')); vs = list(c.get_editor_property('CM_Vals'))
drop = ('PSD_Relaxed_Stand_Run_Stops', 'PSD_Relaxed_Stand_Walk_Stops')
keep = [(k, v) for k, v in zip(ks, vs) if k.get_name() not in drop]; assert len(keep) == len(ks) - 2, (len(ks), len(keep))
c.set_editor_property('CM_Keys', [k for k, _ in keep]); c.set_editor_property('CM_Vals', [v for _, v in keep])
L.compile_blueprint(a); assert 'UP_TO_DATE' in str(a.get_editor_property('status'))
print('REMAP', len(ks), '->', len(u.get_default_object(a.generated_class()).get_editor_property('CM_Keys')))
assert EAL.save_loaded_asset(a, False); assert EAL.save_loaded_asset(ch, False); print('SAVED')
for tag in ('B05', 'B15', 'B40'):
    p = '/Game/Sphirus/Player/GASP/DB/Test/PSD_Sph_R_Sprint_Stops_' + tag
    o = u.find_object(None, p + '.PSD_Sph_R_Sprint_Stops_' + tag)
    if o: print('DISCARD', tag, EAL.delete_loaded_asset(o))
print('DIRTY', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]); print('DONE')
