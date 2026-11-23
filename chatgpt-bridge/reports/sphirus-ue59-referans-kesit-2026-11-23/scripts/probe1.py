# probe1.py (measure, read-only): live project state for the reference-to-game pass. Writes Saved/UE59Work/r2g/probe1.txt
import unreal as u, collections
O=[]
def P(*a): O.append(' '.join(str(x) for x in a))
try: P('ENGINE', u.SystemLibrary.get_engine_version())
except Exception as e: P('ENGINE_ERR', e)
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
P('WORLD', w.get_path_name())
ws=w.get_world_settings()
for k in ('default_game_mode',):
    try: P('WS', k, ws.get_editor_property(k))
    except Exception as e: P('WS_ERR', k, e)
gs=u.get_default_object(u.GameMapsSettings)
for k in ('global_default_game_mode','game_default_map','editor_startup_map','game_instance_class'):
    try: P('GMS', k, gs.get_editor_property(k))
    except Exception as e: P('GMS_ERR', k, e)
def gm_info(path):
    try:
        gm=u.load_asset(path); c=u.get_default_object(gm.generated_class())
        P('GM', path, 'pawn', c.get_editor_property('default_pawn_class'), 'pc', c.get_editor_property('player_controller_class'))
        return c.get_editor_property('default_pawn_class')
    except Exception as e: P('GM_ERR', path, e)
pc=gm_info('/Game/GraceRanger/BP_GM_GR_GraceRanger')
try:
    o=ws.get_editor_property('default_game_mode')
    if o: P('WS_GM_PAWN', u.get_default_object(o).get_editor_property('default_pawn_class'))
except Exception as e: P('WSGM_ERR', e)
# levels
try:
    for l in u.EditorLevelUtils.get_levels(w): P('LEVEL', l.get_outermost().get_name())
except Exception as e: P('LEVELS_ERR', e)
# actors
acts=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
cnt=collections.Counter(a.get_class().get_name() for a in acts)
P('ACTORS', len(acts)); P('CLASSES', dict(cnt.most_common(70)))
KEY=('Light','Sky','Fog','PostProcess','Water','Landscape','PlayerStart','UDS','Ultra','Atmos','Volumetric','Reson','Lens','Wind','Foliage','PCG','Biome','Door','Fire','Mask','Bench','Day','Station','Camera')
for a in acts:
    cn=a.get_class().get_name()
    if any(k.lower() in cn.lower() or k.lower() in a.get_actor_label().lower() for k in KEY):
        l=a.get_actor_location(); r=a.get_actor_rotation()
        P('ACT', cn, '|', a.get_actor_label(), '| lvl', a.get_outer().get_outermost().get_name().split('/')[-1], '| loc %.0f %.0f %.0f rot p%.0f y%.0f' % (l.x,l.y,l.z,r.pitch,r.yaw), '| hid', a.is_hidden_ed())
# pawn components
def comp_dump(path):
    try:
        bp=u.load_asset(path); P('BP', path, 'parent', u.BlueprintEditorLibrary.get_blueprint_parent_class(bp) if hasattr(u.BlueprintEditorLibrary,'get_blueprint_parent_class') else bp.get_editor_property('parent_class') if False else '?')
        sub=u.get_engine_subsystem(u.SubobjectDataSubsystem); hs=sub.k2_gather_subobject_data_for_blueprint(bp)
        for h in hs:
            d=u.SubobjectDataBlueprintFunctionLibrary.get_data(h); ob=u.SubobjectDataBlueprintFunctionLibrary.get_object(d)
            if ob is None: continue
            s='  COMP %s (%s)' % (ob.get_name(), ob.get_class().get_name())
            for k in ('skeletal_mesh_asset','anim_class','groom_asset','binding_asset','relative_location','target_arm_length','socket_offset','field_of_view','child_actor_class'):
                try:
                    v=ob.get_editor_property(k)
                    if v is not None: s+=' | %s=%s' % (k, v.get_path_name() if hasattr(v,'get_path_name') else v)
                except Exception: pass
            try: s+=' | vis=%s' % ob.get_editor_property('visible')
            except Exception: pass
            P(s)
    except Exception as e: P('BP_ERR', path, repr(e)[:300])
for p in ('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player','/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'): comp_dump(p)
# camera + motion vars
def vars_dump(path, tag):
    try:
        a=u.load_asset(path); d=u.get_default_object(a.generated_class()); o=[]
        for n in sorted(dir(d)):
            if n.startswith('_'): continue
            try: v=d.get_editor_property(n)
            except Exception: continue
            if isinstance(v,(float,int,bool,str,u.Vector,u.Vector2D,u.Rotator,u.Name)): o.append('%s=%s' % (n, v))
        P(tag, len(o)); [P('  '+x) for x in o]
    except Exception as e: P(tag+'_ERR', repr(e)[:300])
vars_dump('/Game/Sphirus/Player/Camera/AC_Sph_Camera','CAMVARS')
# assets of interest
ar=u.AssetRegistryHelpers.get_asset_registry()
for kw in ('Reson','Sanri','Percep','Halluc','XR5','Break'):
    res=[str(a.package_name) for a in ar.get_all_assets() if kw.lower() in str(a.asset_name).lower() and str(a.package_name).startswith('/Game/')]
    P('FIND', kw, len(res), res[:40])
for root in ('/Game/Sphirus','/Game/GraceRanger','/Game/Grooms','/Game/Outfits','/Game/EditableCharacters'):
    res=ar.get_assets_by_path(root, recursive=True); c=collections.Counter(str(a.asset_class_path.asset_name) for a in res)
    P('TREE', root, len(res), dict(c.most_common(14)))
open(u.Paths.project_dir()+'Saved/UE59Work/r2g/probe1.txt','w',encoding='utf8').write('\n'.join(O)); print('PROBE1', len(O))
