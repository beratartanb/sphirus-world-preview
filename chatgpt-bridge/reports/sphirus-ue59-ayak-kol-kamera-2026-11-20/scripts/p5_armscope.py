exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# p5_armscope.py (write, gated) on ABP_Sph_Body_GASP (2026-11-19 evening).
# A  RELAX scope: RelA (slow-down relax) fired on any deceleration (sprint stops, turn slow-downs, reversals, landings). Its target
#    is now x gate = input held (|last movement input| x4, clamp) x travel along the input (cos 0.5..0.8 -> 0..1) x (1 - AirA):
#    it acts on "run/jog -> walk while forward input is held". MoveA target x (1 - AirA): jump/fall arms untouched.
# B  FOREARM term for the run->walk transition: probe_r2w.py shows both Neutral and Relaxed Run_to_Walk clips bend the elbow to
#    95-130 deg and lift the hand to chest height (+2.6 / -6 cm vs spine_05; walk loop -32 cm, elbow 150) while the root slows
#    313 -> 192 cm/s. PForeL/R += VD_ForeL/R x RelA x ArmW (opens the elbow only in that gated slow-down; 0 = inert).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'
# (fresh editor session required: no in-memory leftovers)
a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]; assert 'AirA' in have and 'RelA' in have and 'PForeL' in have, [h for h in have if 'Air' in h or 'Fore' in h]
assert 'VD_ForeL' not in have, 'already built (reload failed?)'
assert 'One' in have, [h for h in have if h.lower().startswith('one')]
for n in ('VD_ForeL','VD_ForeR'): B.add_variable(a,n,'Vector')
L.compile_blueprint(a)
for n in ('VD_ForeL','VD_ForeR'):
    try: B.set_variable_instance_editable(a,n,True)
    except Exception as e: print('IE?',n,e)
def build(a):
    g=Gr(a); N=[pn(x) for x in B.find_nodes(g.g)]; ins=lambda p:[str(x.name) for x in info(p).input_pins]
    F=lambda name,**k:(g.fn(M+name,**k),'ReturnValue')
    def consumers(ep): return [(q,str(ip.name)) for q in N for ip in info(q).input_pins if ep in src((q,str(ip.name)))]
    def setnode(var): return [p for p in N if var in ins(p) and 'execute' in ins(p)]
    def interp_of(var):
        s=setnode(var); assert len(s)==1,(var,s)
        fi=src((s[0],var)); assert len(fi)==1,fi; fi=fi[0][0]
        tg=src((fi,'Target')); assert len(tg)==1,tg
        return fi,tg[0]
    pawn=(g.fn('/Script/Engine.AnimInstance:TryGetPawnOwner'),'ReturnValue')
    inp=(g.fn('/Script/Engine.Pawn:GetLastMovementInputVector',self=pawn),'ReturnValue')
    vel=(g.fn('/Script/Engine.Actor:GetVelocity',self=pawn),'ReturnValue')
    air=F('Subtract_DoubleDouble',A=g.get('One'),B=g.get('AirA'))
    held=F('FClamp',Value=F('Multiply_DoubleDouble',A=F('VSizeXY',A=inp),B=4.0),Min=0.0,Max=1.0)
    cosv=F('Dot_VectorVector',A=F('Vector_Normal2D',A=vel),B=F('Vector_Normal2D',A=inp))
    along=F('FClamp',Value=F('Divide_DoubleDouble',A=F('Subtract_DoubleDouble',A=cosv,B=0.5),B=0.3),Min=0.0,Max=1.0)
    gate=F('Multiply_DoubleDouble',A=F('Multiply_DoubleDouble',A=held,B=along),B=air)
    fi,tg=interp_of('RelA'); disconnect((fi,'Target')); connect(F('Multiply_DoubleDouble',A=tg,B=gate),(fi,'Target'))
    fi,tg=interp_of('MoveA'); disconnect((fi,'Target')); connect(F('Multiply_DoubleDouble',A=tg,B=air),(fi,'Target'))
    # relax PSpine5 set = the PSpine5 setter whose exec comes from a PArmR setter
    cand=[p for p in setnode('PSpine5') if any('PArmR' in ins(s[0]) for s in src((p,'execute')))]; assert len(cand)==1,cand
    last=cand[0]; T=consumers((last,'then')); print('after relax PSpine5',T)
    for x in T: disconnect(x)
    t=(last,'then')
    for nm in ('ForeL','ForeR'):
        r=g.fn(M+'BreakRotator',InRot=g.get('P'+nm))
        base=F('MakeVector',X=(r,'Roll'),Y=(r,'Pitch'),Z=(r,'Yaw'))
        add=F('Multiply_VectorFloat',A=F('Multiply_VectorFloat',A=g.get('VD_'+nm),B=g.get('RelA')),B=g.get('ArmW'))
        v=F('Add_VectorVector',A=base,B=add); br=g.fn(M+'BreakVector',InVec=v)
        t=g.set('P'+nm,(g.fn(M+'MakeRotator',Roll=(br,'X'),Pitch=(br,'Y'),Yaw=(br,'Z')),'ReturnValue'),t)
    for x in T: connect(t,x)
    print('ARMSCOPE built')
run(P,build)
print('DONE')
