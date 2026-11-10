# q_ctx.py (read-only probe, no save): can a chooser table's context class be changed from Python?
import unreal as u
t=u.load_asset('/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/CHT_PoseSearchDatabases_Dense')
C=u.load_object(None,'/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP_C')
print('HAS ContextObjectTypeClass',hasattr(u,'ContextObjectTypeClass'))
print('IS doc',(u.InstancedStruct.__doc__ or '')[:400])
try:
    s=u.ContextObjectTypeClass(); print('S props',[p for p in dir(s) if not p.startswith('_')][:20])
    s.set_editor_property('class_',C) if hasattr(s,'class_') else s.set_editor_property('class',C)
except Exception as e: print('S ERR',str(e)[:200])
for how in ('ctor','assign'):
    try:
        if how=='ctor': inst=u.InstancedStruct(s)
        else: inst=u.InstancedStruct(); inst.assign(s) if hasattr(inst,'assign') else None
        print('INST',how,str(inst.export_text())[:200])
        t.set_editor_property('context_data',[inst]); print('AFTER',how,str(t.get_editor_property('context_data')[0].export_text())[:200])
    except Exception as e: print('INST ERR',how,str(e)[:200])
