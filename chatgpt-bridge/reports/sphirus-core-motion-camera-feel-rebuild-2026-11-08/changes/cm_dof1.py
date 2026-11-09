# cm_dof1.py: real depth-of-field with a gaze-driven focus distance, without touching PostProcessSettings struct pins
# (those crash this editor's Python). A CineCameraComponent 'Cine' replaces the plain camera as the active view:
#  - same place on the spring arm, same post-process block (vignette, fringe, grain, EdgeSoft blendable) copied over;
#  - FOV: the existing SetFieldOfView call is mirrored onto Cine;
#  - focus: every tick the focus distance is the visibility trace along the camera axis (120-3000 cm, 1500 when nothing),
#    or the distance to the right hand while an action holds the look input; smoothed by the camera itself (speed 5);
#  - aperture f/9 in free roam (light separation), f/4 during actions (hands and object sharp, background soft).
# Progress goes to Saved/Codex/Day_20261107/dof_progress.txt.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
_LF=open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/dof_progress.txt','w')
def P(*a):
    print(*a); print(*a,file=_LF); _LF.flush()
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; CC='/Script/CinematicCamera.CineCameraComponent:'
bp=u.load_asset(PP); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); SB=u.SubobjectDataBlueprintFunctionLibrary
hs={}
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o=SB.get_object(SB.get_data(h))
    if o: hs[o.get_name().replace('_GEN_VARIABLE','')]=h
P('COMPS',sorted(hs)[:20])
if 'Cine' not in hs:
    r=sds.add_new_subobject(u.AddNewSubobjectParams(parent_handle=hs['SpringArm'],new_class=u.CineCameraComponent,blueprint_context=bp)); P('REN',sds.rename_subobject(r[0],'Cine'))
    hs={}
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        o=SB.get_object(SB.get_data(h))
        if o: hs[o.get_name().replace('_GEN_VARIABLE','')]=h
cam=SB.get_object_for_blueprint(SB.get_data(hs['Camera']),bp); cine=SB.get_object_for_blueprint(SB.get_data(hs['Cine']),bp)
cine.set_editor_property('relative_location',cam.get_editor_property('relative_location')); cine.set_editor_property('relative_rotation',cam.get_editor_property('relative_rotation'))
cine.set_editor_property('post_process_settings',cam.get_editor_property('post_process_settings')); cine.set_editor_property('post_process_blend_weight',1.0)
cine.set_editor_property('constrain_aspect_ratio',False); cine.set_editor_property('current_aperture',9.0); cine.set_editor_property('auto_activate',True)
fs=cine.get_editor_property('focus_settings'); fs.set_editor_property('focus_method',u.CameraFocusMethod.MANUAL); fs.set_editor_property('manual_focus_distance',1500.0); fs.set_editor_property('smooth_focus_changes',True); fs.set_editor_property('focus_smoothing_interp_speed',5.0); cine.set_editor_property('focus_settings',fs)
cam.set_editor_property('auto_activate',False)
P('CINE set; cam auto_activate',cam.get_editor_property('auto_activate'))
L.compile_blueprint(bp); P('STEP comps compiled')
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id)
    fov=[p for p in N if (tp(p).endswith('SetFieldofView') or tp(p).endswith('SetFieldOfView')) and src((p,'execute'))]; P('FOV nodes',len(fov)); assert len(fov)==1; fov=fov[0]
    outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (fov,'then') in src((q,str(ip.name)))]
    for d_ in outs: disconnect(d_)
    cine=lambda:g.get('Cine')
    t=g.call('/Script/Engine.CameraComponent:SetFieldOfView',(fov,'then'),self=cine(),InFieldOfView=g.get('GR_CamFov'))
    act=(g.fn('/Script/Engine.Controller:IsLookInputIgnored',self=(g.fn('/Script/Engine.Pawn:GetController'),'ReturnValue')),'ReturnValue')
    cl=(g.fn('/Script/Engine.SceneComponent:K2_GetComponentLocation',self=cine()),'ReturnValue')
    fw=(g.fn('/Script/Engine.SceneComponent:GetForwardVector',self=cine()),'ReturnValue')
    end=(g.fn(M+'Add_VectorVector',A=cl,B=(g.fn(M+'Multiply_VectorVector',A=fw,B=(g.fn(M+'MakeVector',X=3000.0,Y=3000.0,Z=3000.0),'ReturnValue')),'ReturnValue')),'ReturnValue')
    lt=g.fn('/Script/Engine.KismetSystemLibrary:LineTraceSingle',Start=cl,End=end,TraceChannel='TraceTypeQuery1',bTraceComplex=False,DrawDebugType='None',bIgnoreSelf=True); connect(t,(lt,'execute')); t=(lt,'then')
    bh=g.fn('/Script/Engine.GameplayStatics:BreakHitResult',Hit=(lt,'OutHit'))
    free=(g.fn(M+'SelectFloat',A=(bh,'Distance'),B=1500.0,bPickA=(lt,'ReturnValue')),'ReturnValue')
    hand=(g.fn('/Script/Engine.SceneComponent:GetSocketLocation',self=g.get('Manny'),InSocketName='hand_r'),'ReturnValue')
    hd=(g.fn(M+'Vector_Distance',V1=cl,V2=hand),'ReturnValue')
    dist=(g.fn(M+'FClamp',Value=(g.fn(M+'SelectFloat',A=hd,B=free,bPickA=act),'ReturnValue'),Min=120.0,Max=3000.0),'ReturnValue')
    mk=pn(B.create_node(g.g,'İşlevsellikler|Yapı|MakeCameraFocusSettings',u.IntPoint(0,5000))); pins=[str(x.name) for x in info(mk).input_pins]; P('MAKEFOCUS pins',pins)
    connect(dist,(mk,'ManualFocusDistance')); P('STEP dist connected')
    value((mk,'bSmoothFocusChanges'),True); value((mk,'FocusSmoothingInterpSpeed'),5.0); P('STEP bools set')
    try: value((mk,'FocusMethod'),'Manual'); P('STEP method set')
    except Exception as e: P('METHOD_ERR',str(e)[:120])
    outp=[str(x.name) for x in info(mk).output_pins][0]; P('STEP outpin',outp)
    sf=g.fn(CC+'SetFocusSettings',self=cine()); P('STEP sf node',[str(x.name) for x in info(sf).input_pins]); connect((mk,outp),(sf,'NewFocusSettings')); connect(t,(sf,'execute')); t=(sf,'then'); P('STEP focus wired')
    t=g.call(CC+'SetCurrentAperture',t,self=cine(),NewCurrentAperture=(g.fn(M+'SelectFloat',A=4.0,B=9.0,bPickA=act),'ReturnValue')); P('STEP aperture wired')
    for d_ in outs: connect(t,d_)
    P('STEP graph wired',len(outs))
run(PP,build); P('DONE')
