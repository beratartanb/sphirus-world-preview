# c_tempomap.py: tempo database map + gait defaults. In-memory when run as a control job; the same file is the write job body
# (packages saved by the caller's manifest). Keys = ABP_Sph_GASP.CM_Keys (+ Run F pivots / Run stops, identity in normal mode).
import unreal as u
R='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_'; C='/Game/Sphirus/Player/GASP/CM/DB/PSD_CM_Jog_'
abp=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); ac=u.get_default_object(abp.generated_class())
K=list(ac.get_editor_property('CM_Keys')); V=list(ac.get_editor_property('CM_Vals'))
for extra in ('Run_F_Pivots','Run_Stops'):
    a=u.load_asset(R+extra); assert a
    if a not in K: K.append(a); V.append(a)
TV=[]
D={'F':'F','B':'B','LL':'L','RL':'R'}
for k,v in zip(K,V):
    n=k.get_name().replace('PSD_Relaxed_Stand_',''); t=v
    p=n.split('_')
    if p[0]=='Run' and len(p)==3 and p[1] in D and p[2] in ('Loops','Starts','Pivots'): t=u.load_asset(C+D[p[1]]+'_'+p[2])
    if n=='Run_Stops': t=u.load_asset(C+'Stops')
    assert t, n
    TV.append(t)
ac.set_editor_property('CM_Keys',K); ac.set_editor_property('CM_Vals',V)
bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); pc=u.get_default_object(bp.generated_class())
pc.set_editor_property('GR_NormVals',V); pc.set_editor_property('GR_TempoVals',TV)
import builtins
G=getattr(builtins,'GAIT_DEFAULTS',None) or {'GR_KTempoRun':0.67,'GR_KTempoBack':0.78,'GR_HoldMax':0.9}
for k_,v_ in G.items(): pc.set_editor_property(k_,v_)
print('TEMPOMAP',len(K),len(V),len(TV),[ (k.get_name()[19:],t.get_name()[4:]) for k,v,t in zip(K,V,TV) if t!=v])
print('DEF',{k_:pc.get_editor_property(k_) for k_ in G})
