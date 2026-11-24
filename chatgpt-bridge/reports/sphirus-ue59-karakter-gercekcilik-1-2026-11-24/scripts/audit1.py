import unreal as u
o=[]; W=o.append
bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player')
sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); hs=sds.k2_gather_subobject_data_for_blueprint(bp); seen=set()
for h in hs:
    d=sds.k2_find_subobject_data_from_handle(h); ob=u.SubobjectDataBlueprintFunctionLibrary.get_object(d)
    if not ob or ob.get_name() in seen: continue
    seen.add(ob.get_name()); c=ob.get_class().get_name()
    if isinstance(ob,u.SkeletalMeshComponent):
        sm=ob.get_editor_property('skeletal_mesh_asset'); ac=ob.get_editor_property('anim_class')
        W('SKM %s | mesh %s | anim %s | visible %s | leader? | castshadow %s'%(ob.get_name(), sm.get_path_name() if sm else None, ac.get_name() if ac else None, ob.get_editor_property('visible'), ob.get_editor_property('cast_shadow')))
        if sm:
            try: W('    physasset %s | postprocess %s | lods %d | morphs %d'%(sm.get_editor_property('physics_asset').get_path_name() if sm.get_editor_property('physics_asset') else None, sm.get_editor_property('post_process_anim_blueprint'), u.EditorSkeletalMeshLibrary.get_lod_count(sm) if hasattr(u,'EditorSkeletalMeshLibrary') else -1, len(sm.get_editor_property('morph_targets'))))
            except Exception as e: W('    meshinfo err '+repr(e)[:120])
            for i,m in enumerate(sm.get_editor_property('materials')):
                mi=m.get_editor_property('material_interface'); W('    mat[%d] %s -> %s'%(i,m.get_editor_property('material_slot_name'), mi.get_path_name() if mi else None))
        ov=ob.get_editor_property('override_materials')
        for i,m in enumerate(ov):
            if m: W('    override[%d] %s'%(i,m.get_path_name()))
    elif c.startswith('GroomComponent'):
        g=ob.get_editor_property('groom_asset'); b=ob.get_editor_property('binding_asset')
        W('GROOM %s | asset %s | binding %s | attach %s'%(ob.get_name(), g.get_path_name() if g else None, b.get_path_name() if b else None, ob.get_editor_property('attachment_name') if True else ''))
        try: W('    simsettings '+ob.get_editor_property('simulation_settings').export_text()[:500])
        except Exception as e: W('    simsettings err '+repr(e)[:100])
        try: W('    physics_asset %s'%ob.get_editor_property('physics_asset'))
        except Exception as e: pass
        if g:
            for pn_ in ('hair_groups_physics','hair_groups_rendering','hair_groups_lod','hair_groups_interpolation','enable_simulation_cache'):
                try:
                    v=g.get_editor_property(pn_)
                    if isinstance(v,(list,u.Array)):
                        for i,x in enumerate(v): W('    %s[%d] %s'%(pn_,i,x.export_text()[:900]))
                    else: W('    %s %s'%(pn_,v))
                except Exception as e: W('    %s err %s'%(pn_,repr(e)[:80]))
            try:
                for i,x in enumerate(g.get_editor_property('hair_groups_materials')): W('    groommat[%d] %s -> %s'%(i,x.get_editor_property('slot_name'),x.get_editor_property('material').get_path_name() if x.get_editor_property('material') else None))
            except Exception as e: W('    groommat err '+repr(e)[:80])
    else:
        if c not in ('SceneComponent',): W('OTHER %s (%s)'%(ob.get_name(),c))
open(u.Paths.project_dir()+'Saved/UE59Work/cr1/audit1.txt','w',encoding='utf8').write('\n'.join(o)); print('AUDIT1',len(o))
