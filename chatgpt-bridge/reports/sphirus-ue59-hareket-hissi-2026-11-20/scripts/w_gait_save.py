# w_gait_save.py (write, gated): tempo map + gait defaults (c_tempomap.py), IA_Sph_Pace key (X / pad right shoulder), save the three packages.
import unreal as u
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/c_tempomap.py',encoding='utf8').read())
imc=u.load_asset('/Game/GraceRanger/Input/IMC_GR_SFGameplay'); ia=u.load_asset('/Game/Sphirus/Player/Input/IA_Sph_Pace'); assert imc and ia
def keys():
    try: mp=imc.get_editor_property('default_key_mappings').get_editor_property('mappings')
    except Exception: mp=imc.get_editor_property('mappings')
    return [(m.get_editor_property('action').get_name() if m.get_editor_property('action') else None, str(m.get_editor_property('key').get_editor_property('key_name'))) for m in mp]
have=keys()
for kn in ('X','Gamepad_RightShoulder'):
    assert not any(k==kn for a_,k in have if a_!='IA_Sph_Pace'), ('key in use',kn)
    if ('IA_Sph_Pace',kn) not in have:
        k=u.Key(); k.set_editor_property('key_name',kn); imc.map_key(ia,k)
print('PACE',[x for x in keys() if x[0]=='IA_Sph_Pace'])
for p in ('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player','/Game/Sphirus/Player/GASP/ABP_Sph_GASP','/Game/GraceRanger/Input/IMC_GR_SFGameplay'):
    a=u.load_asset(p)
    try: print('SAVE',p.split('/')[-1],u.EditorAssetLibrary.save_loaded_asset(a,False))
    except Exception as e: print('SAVE_EXC',p.split('/')[-1],repr(e)[:120])
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
