# i2_indoor_speed.py (write) on BP_HybridA_Player: right after CharacterInputState is set from GR_GaitSel,
# SphContextSpeedScale = GR_HomeContext>0.5 ? 0.75 : 1.0 (indoors: walk only, at the old 150 cm/s house pace).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; V='SphContextSpeedScale'
def outs_of(N,ep): return [(q,str(ip.name)) for q in N for ip in info(q).input_pins if ep in src((q,str(ip.name)))]
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; ins=lambda p:[str(x.name) for x in info(p).input_pins]
    assert not [p for p in N if V in ins(p)],'already wired'
    sn=[p for p in N if 'CharacterInputState' in ins(p) and 'execute' in ins(p)]; assert len(sn)==1,sn; sn=sn[0]
    T=outs_of(N,(sn,'then')); print('after InputState',len(T))
    for t in T: disconnect(t)
    home=(g.fn(M+'Greater_DoubleDouble',A=g.get('GR_HomeContext'),B=0.5),'ReturnValue')
    sel=g.fn(M+'SelectFloat',bPickA=home); value((sel,'A'),0.75); value((sel,'B'),1.0)
    tail=g.set(V,(sel,'ReturnValue'),(sn,'then'))
    for t in T: connect(tail,t)
    print('CTX speed wired')
run(P,build); print('DONE')
