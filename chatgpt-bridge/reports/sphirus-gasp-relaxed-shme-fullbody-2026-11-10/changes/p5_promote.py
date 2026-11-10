# p5_promote.py (write): promote the verified candidate B to the production player defaults.
#   ABP_Sph_GASP.SphRelaxed = True                                   (GASP Relaxed family via the Sphirus chooser copy)
#   BP_Sph_GASPCharacter / BP_HybridA_Player speeds = Relaxed clip root speeds: walk 165, run 375, sprint 585 (all directions)
#   AC_Sph_Motion: PhysBrake = True, BodyOn = True, Idle0..4 = M_Relaxed_Stand_Idle_Break v01,v02,v03,v05,v07
#   BP_HybridA_Player indoor context scale literal 0.75 -> 150/165 (house pace stays 150 cm/s)
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
SP={'WalkSpeeds':u.Vector(165,165,165),'RunSpeeds':u.Vector(375,375,375),'SprintSpeeds':u.Vector(585,585,585)}
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); u.get_default_object(a.generated_class()).set_editor_property('SphRelaxed',True)
L.compile_blueprint(a); assert not errs(a); assert EA.save_loaded_asset(a,False)
m=u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion'); mc=u.get_default_object(m.generated_class())
mc.set_editor_property('PhysBrake',True); mc.set_editor_property('BodyOn',True)
for i,n in enumerate((1,2,3,5,7)): mc.set_editor_property('Idle%d'%i,u.load_asset('/Game/Characters/UEFN_Mannequin/Animations/Idle/M_Relaxed_Stand_Idle_Break_v0%d'%n))
L.compile_blueprint(m); assert not errs(m); assert EA.save_loaded_asset(m,False)
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); gcd=u.get_default_object(g.generated_class())
for k,v in SP.items(): gcd.set_editor_property(k,v)
L.compile_blueprint(g); assert not errs(g); assert EA.save_loaded_asset(g,False)
P='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def build(bp):
    gr=Gr(bp); N=[pn(x) for x in B.find_nodes(gr.g)]; ins=lambda p:[str(x.name) for x in info(p).input_pins]
    st=[p for p in N if 'SphContextSpeedScale' in ins(p) and 'execute' in ins(p)]; assert len(st)==1; s=src((st[0],'SphContextSpeedScale')); sel=s[0][0]
    print('SEL',str(info(sel).type_id)); value((sel,'A'),round(150.0/165.0,4)); print('INDOOR scale set')
run(P,build)
bp=u.load_asset(P); pc=u.get_default_object(bp.generated_class())
for k,v in SP.items(): pc.set_editor_property(k,v)
# component template on the character keeps class defaults unless overridden: report what the template holds
scs=u.get_engine_subsystem(u.SubobjectDataSubsystem); SD=u.SubobjectDataBlueprintFunctionLibrary
for B_ in (g,bp):
    for h in scs.k2_gather_subobject_data_for_blueprint(B_):
        d=SD.get_data(h); o=SD.get_object(d)
        if o and str(SD.get_variable_name(d))=='SphMotion':
            for k in ('PhysBrake','BodyOn'): o.set_editor_property(k,True)
            for i,n in enumerate((1,2,3,5,7)): o.set_editor_property('Idle%d'%i,u.load_asset('/Game/Characters/UEFN_Mannequin/Animations/Idle/M_Relaxed_Stand_Idle_Break_v0%d'%n))
            print('TPL',B_.get_name(),o.get_editor_property('PhysBrake'),o.get_editor_property('BodyOn'),o.get_editor_property('Idle0').get_name())
L.compile_blueprint(g); assert EA.save_loaded_asset(g,False)
L.compile_blueprint(bp); e=errs(bp); print('ERR',e); assert not e; assert EA.save_loaded_asset(bp,False)
print('SPEEDS',pc.get_editor_property('WalkSpeeds'),pc.get_editor_property('RunSpeeds'),pc.get_editor_property('SprintSpeeds'),'RELAXED',u.get_default_object(a.generated_class()).get_editor_property('SphRelaxed'))
print('DONE')
