# b3b_child.py (write) on BP_Sph_GASP_B (Sphirus player copy, parent = BP_Sph_GASPCharacter):
#  1. child BeginPlay / OnLanded call the parent's GASP chains first (Sph_GASPBeginPlay / Sph_GASPLanded).
#  2. single movement owner: the Sphirus capsule-contract setters (SetMaxWalkSpeed / SetMaxAcceleration /
#     SetBrakingDecelerationWalking) are bypassed; GASP UpdateMovement_PreCMC owns CMC speed/accel/braking/friction/rotation.
#  3. Sphirus gait input -> GASP gait request: after GR_GaitSel is computed, CharacterInputState =
#     {WantsToWalk = GaitSel==0, WantsToSprint = GaitSel==2} (W = walk, Shift = run, Shift held = sprint).
#  4. driver mesh = GASP UEFN mannequin + ABP_Sph_GASP (hidden); visible MetaHuman body = ABP_Sph_Body_GASP (UEFN->MH).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; PC='/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter.BP_Sph_GASPCharacter_C:'
def outs_of(N,ep): return [(q,str(ip.name)) for q in N for ip in info(q).input_pins if ep in src((q,str(ip.name)))]
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    for ev,fnn in (('OlayBeginPlay','Sph_GASPBeginPlay'),('OlayOnLanded','Sph_GASPLanded')):
        e=[p for p in N if tp(p).endswith(ev)]; assert len(e)==1,(ev,e); e=e[0]
        T=outs_of(N,(e,'then')); print('EVENT',ev,'targets',len(T))
        for t in T: disconnect(t)
        c=g.call(PC+fnn,(e,'then'))
        for t in T: connect(c,t)
    n=0
    for p in N:
        t=tp(p)
        if t in ('|SetMaxWalkSpeed','|SetMaxAcceleration','|SetBrakingDecelerationWalking'):
            S=src((p,'execute')); T=outs_of(N,(p,'then')); disconnect((p,'execute'))
            for t_ in T: disconnect(t_)
            for s in S:
                for t_ in T: connect(s,t_)
            n+=1; print('BYPASS',t,len(S),'->',len(T))
    assert n==3,n
    gs=[p for p in N if 'GR_GaitSel' in ins(p) and 'execute' in ins(p)]; assert len(gs)==1,gs; gs=gs[0]
    T=outs_of(N,(gs,'then'))
    for t_ in T: disconnect(t_)
    mk=g.pos(B.create_node(g.g,'İşlevsellikler|Yapı|MakeSPlayerInputState',(0,0)))
    mi=ins(mk); print('MAKE pins',mi)
    ww=[x for x in mi if x.startswith('WantsToWalk')][0]; ws=[x for x in mi if x.startswith('WantsToSprint')][0]
    connect((g.fn(M+'EqualEqual_IntInt',A=g.get('GR_GaitSel'),B=0),'ReturnValue'),(mk,ww))
    connect((g.fn(M+'EqualEqual_IntInt',A=g.get('GR_GaitSel'),B=2),'ReturnValue'),(mk,ws))
    sn=g.e.add_set_member_variable_node('CharacterInputState',''); assert sn,'setter'; sn=g.pos(sn)
    so=[x for x in ins(sn) if x not in ('execute','self')]; print('SET pins',so)
    connect((mk,[str(x.name) for x in info(mk).output_pins][0]),(sn,so[0])); connect((gs,'then'),(sn,'execute'))
    for t_ in T: connect((sn,'then'),t_)
    print('GAIT->InputState wired',len(T))
run(P,build)
bp=u.load_asset(P); cdo=u.get_default_object(bp.generated_class())
m=cdo.get_editor_property('mesh'); m.set_editor_property('skeletal_mesh_asset',u.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin'))
m.set_editor_property('anim_class',u.load_object(None,'/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP_C'))
print('MESH',m.get_editor_property('skeletal_mesh_asset').get_name(),m.get_editor_property('anim_class').get_name(),'hidden',m.get_editor_property('hidden_in_game'),'loc',m.get_editor_property('relative_location'),'rot',m.get_editor_property('relative_rotation'),'vbat',m.get_editor_property('visibility_based_anim_tick_option'))
scs=u.get_engine_subsystem(u.SubobjectDataSubsystem); SD=u.SubobjectDataBlueprintFunctionLibrary
for h in scs.k2_gather_subobject_data_for_blueprint(bp):
    d=SD.get_data(h); o=SD.get_object(d); n=str(SD.get_variable_name(d))
    if o and n=='Manny':
        o.set_editor_property('anim_class',u.load_object(None,'/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.ABP_Sph_Body_GASP_C')); print('MANNY anim',o.get_editor_property('anim_class').get_name(),'loc',o.get_editor_property('relative_location'),'rot',o.get_editor_property('relative_rotation'))
L.compile_blueprint(bp); print('ERR',errs(bp)); assert EA.save_loaded_asset(bp,False); print('DONE')
