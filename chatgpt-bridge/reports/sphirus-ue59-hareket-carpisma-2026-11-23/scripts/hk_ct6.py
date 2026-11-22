# hk_ct6.py (prelude): hk_pose3 + contact v2 log (row.hook.ct / ct6) ; builtins.CT_FAT = forced fatigue 0..1 ; builtins.CT_CARRY = True forces
# the two-hand load state (GR_Load2H) ; builtins.CT_SET = {var: value} written once to the pawn on the first tick (forced-parameter tests).
import builtins, unreal as _u2
exec(open(_u2.Paths.project_dir()+'Tools/UE59_20261122/hk_pose3.py',encoding='utf8').read())
_base=builtins.VID_TICKHOOK; _stt={'done':False}
_CT=('CT_State','CT_Class','CT_DB','CT_Prox','CT_Graze','CT_VnPrev','CT_LastS','CT_LastV','CT_LastC','CT_LastL','CT_Count','CT_LockT','CT_ReachA','CT_CapT')
_C6=('CT_Pend','CT_Kind','CT_Sup','CT_Room','CT_DBk','CT_DSh','CT_Flat','CT_Sep','CT_Since')
def _hk2(pw, ai, st, w_):
    if not _stt['done']:
        _stt['done']=True
        for k_,v_ in (getattr(builtins,'CT_SET',None) or {}).items():
            try: pw.set_editor_property(k_,v_)
            except Exception as e: _stt['seterr']=repr(e)[:120]
    o=_base(pw, ai, st, w_)
    try:
        if getattr(builtins,'CT_CARRY',None): pw.set_editor_property('GR_CarryActive',True)
        o['ct']=[round(float(pw.get_editor_property(n)),2) for n in _CT]; o['ct6']=[round(float(pw.get_editor_property(n)),2) for n in _C6]; o['obj']=str(pw.get_editor_property('CT_ObjN'))
        m=[c for c in pw.get_components_by_class(_u2.ActorComponent) if c.get_name()=='SphMotion'][0]
        f=getattr(builtins,'CT_FAT',None)
        if f is not None: m.set_editor_property('Fat',float(f))
        try: o['duck']=[bool(pw.get_editor_property('CT_Duck')),bool(pw.get_editor_property('is_crouched'))]
        except Exception as e: o['duck']=repr(e)[:80]
        o['ctm']=[round(float(m.get_editor_property(n)),2) for n in ('CtCap','ReachA','CtA','Fat','E')]; o['seterr']=_stt.get('seterr')
    except Exception as e: o['cterr']=repr(e)[:120]
    return o
builtins.VID_TICKHOOK=_hk2
