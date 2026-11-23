# apply_facade.py: facade material language of this pass, idempotent (actor-level material overrides only; no mesh or material asset is edited).
# Ground-floor outer walls on the rear / east / west faces carried MI_EX_CladdingAged (grey boards) while the pond front is lime plaster.
# CFG ground='lime' puts the same owned lime+oak instance on those slots; gables='cladding' moves the aged boards up to the two gable ends.
import unreal as u, builtins
CFG={'ground':'lime','gables':'keep'}; CFG.update(getattr(builtins,'R2G_FACADE',None) or {})
M='/Game/GraceRanger/Environment/Exterior20260921/Materials/'
LIME=u.load_asset(M+'MI_EX_Integration_OuterLimeOak'); CLAD=u.load_asset(M+'MI_EX_CladdingAged')
GROUND=('Architecture_01_GROUND_G_East','Architecture_01_GROUND_G_Forest','Architecture_01_GROUND_G_West','Architecture_Scene_Collection_G_East','Architecture_Scene_Collection_G_Forest')
print('FACADE mats',LIME is not None,CLAD is not None)
n=0; TOUCHED=set()
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if str(a.get_folder_path())!='House/Architecture': continue
    lb=a.get_actor_label(); c=a.get_component_by_class(u.StaticMeshComponent)
    if not c: continue
    mesh=c.get_editor_property('static_mesh')
    if not mesh: continue
    base=[sm.material_interface for sm in mesh.static_materials]
    if lb in GROUND:
        want=LIME if CFG['ground']=='lime' else CLAD
        if c.get_material(1)!=want: a.modify(); c.modify(); c.set_material(1,want); TOUCHED.add(a.get_outer().get_outermost())
        n+=1; print('FACADE ground',lb,c.get_material(0).get_name(),c.get_material(1).get_name())
    if 'UPPER_ENVELOPE' in lb and ('Gable' in mesh.get_name() or abs(a.get_actor_bounds(False)[1].z)>200):
        want=CLAD if CFG['gables']=='cladding' else base[0]
        if c.get_material(0)!=want: a.modify(); c.modify(); c.set_material(0,want); TOUCHED.add(a.get_outer().get_outermost())
        print('FACADE gable',lb,mesh.get_name(),c.get_material(0).get_name())
print('FACADE slots',n)
builtins.R2G_FACADE_PKGS=list(TOUCHED); print('FACADE touched packages',[p.get_name() for p in TOUCHED])
