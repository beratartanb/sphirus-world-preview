# VF2B read-only audit: player Blueprint components, meshes, materials, cloth, physics, grooms.
import unreal as u, re
P = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
hb = u.load_asset(P); sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); B = u.SubobjectDataBlueprintFunctionLibrary
out = []
print('A parent', hb.generated_class().get_super_class().get_name() if hasattr(hb.generated_class(),'get_super_class') else '?')
for h in sds.k2_gather_subobject_data_for_blueprint(hb):
    d = B.get_data(h); o = B.get_object(d)
    if not o: continue
    n = o.get_name().replace('_GEN_VARIABLE', ''); cn = o.get_class().get_name()
    line = 'A comp %s [%s]' % (n, cn)
    if isinstance(o, u.SkeletalMeshComponent):
        sk = o.get_editor_property('skeletal_mesh_asset') if hasattr(o,'get_editor_property') else None
        try: sk = o.get_skeletal_mesh_asset()
        except Exception: pass
        ac = o.get_editor_property('anim_class')
        line += ' mesh=%s anim=%s vis=%s' % (sk.get_path_name() if sk else None, ac.get_name() if ac else None, o.get_editor_property('visible'))
        if sk:
            try:
                pa = sk.get_editor_property('physics_asset'); line += ' phys=%s' % (pa.get_name() if pa else None)
            except Exception as e: line += ' phys?'
            try:
                ca = sk.get_editor_property('mesh_clothing_assets'); line += ' cloth=%d' % len(ca)
            except Exception as e: line += ' cloth?%s' % str(e)[:40]
            try:
                line += ' lods=%d' % u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem).get_lod_count(sk)
                line += ' v0=%d' % u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem).get_num_verts(sk, 0)
            except Exception as e: pass
            mats = [(str(m.get_editor_property('material_slot_name')), m.get_editor_property('material_interface').get_path_name() if m.get_editor_property('material_interface') else None) for m in sk.get_editor_property('materials')]
            line += '\n    meshmats=%s' % mats
        ov = [m.get_path_name() if m else None for m in o.get_editor_property('override_materials')]
        if ov: line += '\n    overrides=%s' % ov
    elif cn == 'GroomComponent':
        g = o.get_editor_property('groom_asset'); b = o.get_editor_property('binding_asset')
        line += ' groom=%s bind=%s %s' % (g.get_path_name() if g else None, b.get_name() if b else None, re.search(r'bEnableSimulation=\w+', o.get_editor_property('simulation_settings').export_text()).group(0))
        line += ' mats=%s' % [m.get_name() if m else None for m in o.get_materials()]
    elif isinstance(o, u.StaticMeshComponent):
        sm = o.get_editor_property('static_mesh'); line += ' sm=%s' % (sm.get_path_name() if sm else None)
    try:
        ap = o.get_editor_property('attach_parent'); 
        if ap: line += ' parent=%s' % ap.get_name().replace('_GEN_VARIABLE','')
    except Exception: pass
    print(line)
print('A level', u.EditorLevelLibrary.get_editor_world().get_name(), 'dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()], [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
