# hk_fall9.py (prelude, read-only): hk_ct6 + the visible body's layer inputs (row.hook.bl) and PS_FW, to find which layer bends the lying pose.
import builtins, unreal as _u9
exec(open(_u9.Paths.project_dir()+'Tools/UE59_20261123/hk_ct6.py',encoding='utf8').read())
_b9=builtins.VID_TICKHOOK; _BL=('ChestRot','SpineRot3','SpineRot5','PSpine3','PSpine5','PNeck1','PHead','PArmL','PArmR','PForeL','PJ_Spine3','PJ_Spine5','PL_Spine3','PL_Spine5','PH_Level','HeadA','RAR','RAL','PalmAR','PalmAL','FootAR','FootAL','FootTR')
def _hk9f(pw, ai, st, w_):
    o=_b9(pw, ai, st, w_)
    try:
        bi=None
        for c in pw.get_components_by_class(_u9.SkeletalMeshComponent):
            a_=c.get_anim_instance()
            if a_ and 'ABP_Sph_Body_GASP' in a_.get_class().get_name(): bi=a_; break
        d={}
        for n in _BL:
            v=bi.get_editor_property(n)
            d[n]=[round(v.pitch,1),round(v.yaw,1),round(v.roll,1)] if isinstance(v,_u9.Rotator) else ([round(v.x,1),round(v.y,1),round(v.z,1)] if isinstance(v,_u9.Vector) else round(float(v),2))
        o['bl']=d
    except Exception as e: o['bl']=repr(e)[:160]
    try: o['fw']=round(float(pw.get_editor_property('PS_FW')),2)
    except Exception as e: o['fw']=None
    return o
builtins.VID_TICKHOOK=_hk9f
