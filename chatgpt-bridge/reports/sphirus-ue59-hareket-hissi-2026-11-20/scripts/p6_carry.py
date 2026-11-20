exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# p6_carry.py (write, gated) on ABP_Sph_Body_GASP - 2026-11-20: carriage per gait.
# Diagnosis (an_carry.py / an_head.py, C_walk, C_tempo, H_k1):
#  - upper-arm abduction visible vs driver: walk 8.9 / 17.8, tempo 9.9 / 18.3, run 21.5 / 31.1, sprint 22.2 / 38.4 deg; hands cross
#    the body midline in run. Owners: VR_Arm pitch -/+7 x RunA (2026-11-12 posture) + VW_Arm -/+3 x MoveA (2026-11-19 walk relax),
#    MoveA = 1 at every speed above 150.
#  - RunA = clamp((speed-a)/b) reached only 0.57 at the 415 run, so the run trunk correction (VR_Spine) was half strength exactly
#    where the source clip (Neutral run, authored for 500) leans most: chest 20 deg forward of idle, neck line 37 deg.
#  - walk: chest as idle but neck_01 pitched 20 deg forward (neck line 22.6 vs idle 12.0): no walk channel on the neck.
# Change:  RunA target = clamp((speed - RunLo)/(RunFull - RunLo))   (RunLo 200, RunFull 415)
#          PNeck1 += VW_Neck1 x MoveA x ArmW ; PHead += VW_Head x MoveA x ArmW   (new vectors, default 0 = inert)
# Values are stored by p6_values.py after runtime screening.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'
a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]; assert 'VW_Neck1' not in have,'already built'
assert 'MoveA' in have and 'PNeck1' in have and 'PHead' in have and 'VD_ForeR' in have
for n in ('VW_Neck1','VW_Head'): B.add_variable(a,n,'Vector')
for n in ('RunLo','RunFull'): B.add_variable(a,n,'float')
L.compile_blueprint(a)
for n in ('VW_Neck1','VW_Head','RunLo','RunFull'):
    try: B.set_variable_instance_editable(a,n,True)
    except Exception as e: print('IE?',n,e)
d=u.get_default_object(a.generated_class()); d.set_editor_property('RunLo',200.0); d.set_editor_property('RunFull',415.0)
def build(a):
    g=Gr(a); N=[pn(x) for x in B.find_nodes(g.g)]; ins=lambda p:[str(x.name) for x in info(p).input_pins]
    F=lambda name,**k:(g.fn(M+name,**k),'ReturnValue')
    def consumers(ep): return [(q,str(ip.name)) for q in N for ip in info(q).input_pins if ep in src((q,str(ip.name)))]
    def setnode(var): return [p for p in N if var in ins(p) and 'execute' in ins(p)]
    # RunA target
    s=setnode('RunA'); assert len(s)==1,s
    fi=src((s[0],'RunA')); assert len(fi)==1,fi; fi=fi[0][0]
    pawn=(g.fn('/Script/Engine.AnimInstance:TryGetPawnOwner'),'ReturnValue')
    sp=F('VSizeXY',A=(g.fn('/Script/Engine.Actor:GetVelocity',self=pawn),'ReturnValue'))
    tgt=F('FClamp',Value=F('Divide_DoubleDouble',A=F('Subtract_DoubleDouble',A=sp,B=g.get('RunLo')),B=F('FMax',A=F('Subtract_DoubleDouble',A=g.get('RunFull'),B=g.get('RunLo')),B=1.0)),Min=0.0,Max=1.0)
    disconnect((fi,'Target')); connect(tgt,(fi,'Target'))
    # neck / head walk terms appended after the VD_Fore chain (PForeR setter fed by the PForeL setter)
    cand=[p for p in setnode('PForeR') if any('PForeL' in ins(x[0]) and any('PSpine5' in ins(y[0]) for y in src((x[0],'execute'))) for x in src((p,'execute')))]; assert len(cand)==1,cand
    last=cand[0]; T=consumers((last,'then')); print('after PForeR',T)
    for x in T: disconnect(x)
    t=(last,'then')
    for nm in ('Neck1','Head'):
        r=g.fn(M+'BreakRotator',InRot=g.get('P'+nm))
        base=F('MakeVector',X=(r,'Roll'),Y=(r,'Pitch'),Z=(r,'Yaw'))
        add=F('Multiply_VectorFloat',A=F('Multiply_VectorFloat',A=g.get('VW_'+nm),B=g.get('MoveA')),B=g.get('ArmW'))
        v=F('Add_VectorVector',A=base,B=add); br=g.fn(M+'BreakVector',InVec=v)
        t=g.set('P'+nm,(g.fn(M+'MakeRotator',Roll=(br,'X'),Pitch=(br,'Y'),Yaw=(br,'Z')),'ReturnValue'),t)
    for x in T: connect(t,x)
    print('CARRY built')
run(P,build)
a=u.load_asset(P); d=u.get_default_object(a.generated_class()); d.set_editor_property('RunLo',200.0); d.set_editor_property('RunFull',415.0)
L.compile_blueprint(a)
try: print('SAVE',EA.save_loaded_asset(a,False))
except Exception as e: print('SAVE_EXC',repr(e)[:160])
d=u.get_default_object(u.load_asset(P).generated_class()); print('DEF',d.get_editor_property('RunLo'),d.get_editor_property('RunFull'),d.get_editor_property('VW_Neck1'))
print('DONE')
