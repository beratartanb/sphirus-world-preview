# probe_saved6.py (read-only): round-6 values as loaded from disk after a relaunch
import unreal as u
o=[]
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); c=u.get_default_object(a.generated_class())
for n in ('PlantSettings_Default','PlantSettings_Stops'): o.append(n+' '+c.get_editor_property(n).export_text()[:118])
p=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
o.append('player '+str({k:round(float(p.get_editor_property(k)),2) for k in ('CT_RetD','CT_KneelClr','CT_TripV','CT_TripH','CT_FallRate','CT_FallTf','CT_StandOff','CT_KneeSeeV','CT_HandOff','PS_KeepRun','PS_LuK','PS_LuMax')}))
m=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
o.append('motion '+str({k:m.get_editor_property(k) for k in ('KRelax','StBoostMax','StBoostDur','StBoostOn')})+' idle '+str([m.get_editor_property('Idle%d'%i).get_name()[-3:] for i in range(5)]))
for n in ('SphF_am_InjuredBelly_DropToFloor','SphF_am_InjuredBelly_DropToFloor_GetUp'):
    s=u.load_asset('/Game/Sphirus/Player/Anim/Fall/'+n); o.append('%s len %.2f rm %s lock %s forced %s'%(n,s.get_play_length(),u.AnimationLibrary.is_root_motion_enabled(s),u.AnimationLibrary.get_root_motion_lock_type(s),u.AnimationLibrary.is_root_motion_lock_forced(s)))
print('SAVED6'); print('\n'.join(o)); open(u.Paths.project_dir()+'Saved/UE59Work/r6/saved6.txt','w',encoding='utf8').write('\n'.join(o))
