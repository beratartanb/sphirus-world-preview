# c3_indoor.py (write) on BP_Sph_GASP_B: keep the house rule of the Sphirus player (indoors = walk only):
# WantsToWalk = GaitSel==0 OR GR_HomeContext>0.5 ; WantsToSprint = GaitSel==2 AND NOT GR_HomeContext>0.5.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/GASP/BP_Sph_GASP_B'
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]
    mk=[p for p in N if str(info(p).type_id).endswith('MakeSPlayerInputState')]; assert len(mk)==1,mk; mk=mk[0]
    ins=[str(x.name) for x in info(mk).input_pins]; ww=[x for x in ins if x.startswith('WantsToWalk')][0]; ws=[x for x in ins if x.startswith('WantsToSprint')][0]
    home=(g.fn(M+'Greater_DoubleDouble',A=g.get('GR_HomeContext'),B=0.5),'ReturnValue')
    a=src((mk,ww)); disconnect((mk,ww)); connect((g.fn(M+'BooleanOR',A=a[0],B=home),'ReturnValue'),(mk,ww))
    b=src((mk,ws)); disconnect((mk,ws)); connect((g.fn(M+'BooleanAND',A=b[0],B=(g.fn(M+'Not_PreBool',A=home),'ReturnValue')),'ReturnValue'),(mk,ws))
    print('INDOOR rule wired')
run(P,build); print('DONE')
