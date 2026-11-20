exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# c_abp_int.py (in-memory build; saved later by the gated write job): ABP_Sph_GASP.Get_MMInterruptMode also interrupts the
# continuing pose when RotationMode changed since the last frame (orient-to-movement <-> strafe). Without it a "turn around" start
# picked in the one non-strafing frame after S is pressed stayed selected for 0.4 s because the same clip is also in the strafe DB.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/GASP/ABP_Sph_GASP'; a=u.load_asset(P)
fg=[g for g in B.list_graphs(a) if str(g).split(':')[-1].split("'")[0]=='Get_MMInterruptMode']; assert len(fg)==1
g=Gr(a); g.g=fg[0]; g.e=GE(g.g)
nodes=list(B.find_nodes(g.g)); N=[pn(x) for x in nodes]
# remove leftovers of the first attempt (byte compare + its unconnected getters)
for n,p in zip(nodes,N):
    i=info(p); t=str(i.type_id)
    if 'NotEqual_ByteByte' in t or 'Bayt' in t or (('RotationMode' in ' '.join(str(x.name) for x in i.output_pins)) ): 
        try: B.delete_node(n); print('DEL',str(p)[-30:])
        except Exception as e: print('DELERR',e)
nodes=list(B.find_nodes(g.g)); N=[pn(x) for x in nodes]
sel=[p for p in N if 'K2Node_Select' in str(p)]; assert len(sel)==1,sel
s=src((sel[0],'Index')); assert len(s)==1,s; assert 'BooleanOR' not in str(info(s[0][0]).type_id) or True
ne=[p for p in N if 'K2Node_EnumInequality' in str(p)]; tid=info(ne[0]).type_id; print('TID',str(tid)[:120])
nn=B.create_node(g.g,tid,(900,1500)); nn=pn(nn)
connect(g.get('RotationMode'),(nn,'A')); connect(g.get('RotationMode_LastFrame'),(nn,'B'))
orn=(g.fn(M+'BooleanOR',A=s[0],B=(nn,'ReturnValue')),'ReturnValue')
disconnect((sel[0],'Index')); connect(orn,(sel[0],'Index'))
L.compile_blueprint(a); e=errs(a); print('ERR',e); assert not e
print('INT built', [ (str(q[0])[-28:],q[1]) for q in src((sel[0],'Index'))])
