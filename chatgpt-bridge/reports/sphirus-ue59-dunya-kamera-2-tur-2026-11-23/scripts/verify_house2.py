import unreal as u
acts={a.get_actor_label():a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()}
print('VH n actors',len(acts))
for lb in ('Architecture_01_GROUND_G_Forest','Architecture_Scene_Collection_G_East','Architecture_03_UPPER_ENVELOPE_Envelope_EastGable','Architecture_01_GROUND_G_Lake'):
    a=acts.get(lb)
    if not a: print('VH MISSING',lb); continue
    cs=a.get_components_by_class(u.StaticMeshComponent); c=cs[0] if cs else None
    m=c.get_editor_property('static_mesh') if c else None
    print('VH',lb,'comps',len(cs),'mesh',m.get_name() if m else None,'nmat',c.get_num_materials() if c else None,[x.get_name() if x else None for x in (c.get_materials() if c else [])],'ovr',[x.get_name() if x else None for x in (c.get_editor_property('override_materials') if c else [])])
