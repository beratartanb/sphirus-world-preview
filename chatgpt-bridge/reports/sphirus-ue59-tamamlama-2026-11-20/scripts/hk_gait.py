# hk_gait.py (prelude): per-frame gait state of the pawn + driver clip curves -> row['hook'] (no writes)
import builtins
def _hk(pw, ai, st, w_):
    o={}
    for k in ('GR_TempoOn','GR_TempoAct','GR_BrakeHold','GR_HoldT','GR_Back','GR_GaitSel','GR_Gait','GR_Pace','GR_HomeContext','GR_Load2H','SphContextSpeedScale'):
        try:
            v=pw.get_editor_property(k); o[k]=round(float(v),3) if isinstance(v,float) else (bool(v) if isinstance(v,bool) else int(v))
        except Exception: o[k]=None
    try: o['cv']=[round(float(ai.get_curve_value(n)),2) for n in ('contact_l','contact_r','movedata_speed')]
    except Exception as e: o['cv']=None
    try:
        m=[c for c in pw.get_components_by_class(__import__('unreal').ActorComponent) if c.get_name()=='SphMotion'][0]
        o['m']=[round(float(m.get_editor_property(n)),2) for n in ('StK','StT','BrakeDecel','BrakeLatchSpeed','StartT','TurnCap')]
    except Exception as e: o['m']=None
    return o
builtins.VID_TICKHOOK=_hk
