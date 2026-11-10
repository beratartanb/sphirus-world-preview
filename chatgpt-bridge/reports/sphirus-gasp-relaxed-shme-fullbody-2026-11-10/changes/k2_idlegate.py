# k2_idlegate.py (write) on AC_Sph_Motion: no idle breaks while an interaction owns the player.
# Stations / bed / mask bench lock the player with Controller.SetIgnoreMoveInput -> the idle still-time only accumulates
# when the controller does NOT ignore move input (in addition to: still, no input, on ground, no montage, IdleEnabled).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/Motion/AC_Sph_Motion'
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    assert not [p for p in N if tp(p).endswith('IsMoveInputIgnored')],'already gated'
    sets=[p for p in N if 'IdleTime' in ins(p) and 'execute' in ins(p)]
    cand=[]
    for p in sets:
        s=src((p,'IdleTime'))
        if s and tp(s[0][0]).endswith('SelectFloat') and src((s[0][0],'bPickA')): cand.append(s[0][0])
    assert len(cand)==1,cand; sel=cand[0]; still=src((sel,'bPickA'))[0]; disconnect((sel,'bPickA'))
    cst=[p for p in N if tp(p).endswith('CastToCharacter')][0]; asc=(cst,'AsCharacter')
    ctl=(g.fn('/Script/Engine.Pawn:GetController',self=asc),'ReturnValue')
    ig=(g.fn('/Script/Engine.Controller:IsMoveInputIgnored',self=ctl),'ReturnValue')
    ok=(g.fn(M+'BooleanAND',A=still,B=(g.fn(M+'Not_PreBool',A=ig),'ReturnValue')),'ReturnValue')
    connect(ok,(sel,'bPickA')); print('IDLE gate wired')
run(P,build); print('DONE')
