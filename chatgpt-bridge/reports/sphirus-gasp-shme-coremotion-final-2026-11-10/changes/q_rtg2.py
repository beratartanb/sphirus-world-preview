import unreal as u
for rp in ['/Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH','/Game/Sphirus/Player/Rig/RTG_Sph_Core_to_MH2']:
    r=u.load_asset(rp); rc=u.IKRetargeterController.get_controller(r); n=rc.get_num_retarget_ops(); print('==',rp.split('/')[-1],'ops',n)
    for i in range(n):
        nm=rc.get_op_name(i); print('  OP',i,nm,'enabled',rc.get_retarget_op_enabled(i))
        try:
            oc=rc.get_op_controller(i); print('     ctrl',type(oc).__name__,[m for m in dir(oc) if m.startswith('get_')][:12])
            try:
                s=oc.get_settings(); print('     SET',str(s.export_text())[:900])
            except Exception as e: print('     SET ERR',str(e)[:120])
        except Exception as e: print('     OPC ERR',str(e)[:120])
    try:
        for cs in rc.get_all_chain_settings(): print('  CHS',str(cs.export_text())[:300])
    except Exception as e: print('  CHS ERR',str(e)[:200])
