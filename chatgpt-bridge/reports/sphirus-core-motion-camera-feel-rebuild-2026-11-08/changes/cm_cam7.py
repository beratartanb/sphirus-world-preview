# cm_cam7.py: closer follow camera with a living response (user: "too far, lost the soft approach/recede").
# - Arm: indoor 85-115, outdoor 105-140 (was 85-125 / 120-165); speed adds up to +12 (was +18) and the arm eases at 2.2/s so
#   acceleration shows as a short recede, braking as a slow approach.
# - Spring arm: position lag 7/s with 45 cm max, rotation lag 14/s (small mass feel), probe 10.
# - Action mode (look input ignored): arm 70, shoulder 34, height +8, pitch -18 (hands and object in frame, closer).
# - Pitch target pin found by its -22 literal, arm/shoulder/Z selects by the IsLookInputIgnored feed.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); n=0
    for p in N:
        t=tp(p)
        if t.endswith('Lerp') or t.endswith('|Lerp'):
            a,b=pv(p,'A'),pv(p,'B')
            if (a,b)==('85.0','125.0'): value((p,'B'),115.0); n+=1
            if (a,b)==('120.0','165.0'): value((p,'A'),105.0); value((p,'B'),140.0); n+=1
        if 'Multiply_DoubleDouble' in t or t.endswith('float*float'):
            if pv(p,'B')=='18.0': value((p,'B'),12.0); n+=1
        if t.endswith('FInterpTo') and pv(p,'InterpSpeed')=='3.0' and any('TargetArmLength' in tp(s[0]) for s in src((p,'Current'))): value((p,'InterpSpeed'),2.2); n+=1
        if t.endswith('SelectFloat') and any('IsLookInputIgnored' in tp(s[0]) for s in src((p,'bPickA'))):
            a=pv(p,'A'); m={'38.0':34.0,'10.0':8.0,'90.0':70.0}.get(a)
            if m is not None: value((p,'A'),m); n+=1
        if t.endswith('MakeRotator') and pv(p,'Pitch')=='-22.0': value((p,'Pitch'),-18.0); n+=1
    print('CHANGED',n); assert n>=7,n
run(PP,build)
bp=u.load_asset(PP); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); SB=u.SubobjectDataBlueprintFunctionLibrary
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o=SB.get_object(SB.get_data(h))
    if o and isinstance(o,u.SpringArmComponent):
        c=SB.get_object_for_blueprint(SB.get_data(h),bp)
        for k,v in (('enable_camera_lag',True),('camera_lag_speed',7.0),('camera_lag_max_distance',45.0),('enable_camera_rotation_lag',True),('camera_rotation_lag_speed',14.0),('probe_size',10.0)): c.set_editor_property(k,v)
        print('ARM set')
L.compile_blueprint(bp); assert EA.save_loaded_asset(bp,False); print('DONE')
