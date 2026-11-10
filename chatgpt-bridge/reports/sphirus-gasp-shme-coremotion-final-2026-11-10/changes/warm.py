import unreal as u, time
t=time.time()
for p in ['/Game/Sphirus/Player/GASP/BP_Sph_GASP_B.BP_Sph_GASP_B_C','/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP_C','/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.ABP_Sph_Body_GASP_C']:
    c=u.load_object(None,p); print('WARM',p.split('.')[-1],bool(c),round(time.time()-t,1))
