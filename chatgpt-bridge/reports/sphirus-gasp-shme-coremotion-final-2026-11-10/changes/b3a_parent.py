# b3a_parent.py (write) on BP_Sph_GASPCharacter (Sphirus copy of GASP SandboxCharacter_CMC):
#  1. callable entry points for a child that overrides BeginPlay/OnLanded: custom events Sph_GASPBeginPlay and
#     Sph_GASPLanded wired into the SAME chains as the parent's BeginPlay / OnLanded (exec inputs accept several links).
#  2. GASP camera/input setup off: EventPossessed_Client -> SetupCamera link broken (SetupCamera -> SetupInput chain), so
#     the Sphirus camera (Cine) and Sphirus IMC stay the only camera/input owners; GASP camera components not auto-active.
#  3. driver mesh anim class -> ABP_Sph_GASP (Sphirus copy of the GASP AnimBP).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id)
    one=lambda f:[p for p in N if f(tp(p))]
    bpn=one(lambda t:t.endswith('OlayBeginPlay')); assert len(bpn)==1; bpn=bpn[0]
    tgt=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (bpn,'then') in src((q,str(ip.name)))]; assert len(tgt)==1,tgt
    ce=g.e.add_custom_event_node('Sph_GASPBeginPlay'); assert ce; ce=g.pos(ce); connect((ce,'then'),tgt[0]); print('CE BeginPlay ->',tgt[0][0].split('.')[-1])
    ol=one(lambda t:t.endswith('OlayOnLanded')); assert len(ol)==1; ol=ol[0]
    t2=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (ol,'then') in src((q,str(ip.name)))]; assert len(t2)==1,t2
    ce2=g.pos(g.e.add_custom_event_node('Sph_GASPLanded')); connect((ce2,'then'),t2[0]); print('CE Landed ->',t2[0][0].split('.')[-1])
    sc=one(lambda t:t.endswith('SetupCamera') and t.startswith('Kamera')); assert len(sc)==1,sc; s=src((sc[0],'execute')); print('SetupCamera exec from',s); disconnect((sc[0],'execute'))
run(P,build)
bp=u.load_asset(P); C=bp.generated_class(); cdo=u.get_default_object(C)
abp=u.load_object(None,'/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP_C'); assert abp
m=cdo.get_editor_property('mesh'); m.set_editor_property('anim_class',abp); print('MESH anim',m.get_editor_property('anim_class').get_name())
scs=u.get_engine_subsystem(u.SubobjectDataSubsystem); SD=u.SubobjectDataBlueprintFunctionLibrary
for h in scs.k2_gather_subobject_data_for_blueprint(bp):
    d=SD.get_data(h); o=SD.get_object(d); n=str(SD.get_variable_name(d))
    if o and n in ('GameplayCamera','Camera(NotUsedByDefault)'):
        o.set_editor_property('auto_activate',False); print('AUTOACT off',n)
L.compile_blueprint(bp); print('ERR',errs(bp)); assert EA.save_loaded_asset(bp,False); print('DONE')
