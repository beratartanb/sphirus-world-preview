import unreal as u
for P in ('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player','/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'):
    a=u.load_asset(P)
    try: st=str(a.get_editor_property('status'))
    except Exception as e: st='?'+str(e)[:40]
    print('BPSTAT',P.split('/')[-1],st)
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
