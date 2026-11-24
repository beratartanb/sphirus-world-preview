# hk_r9.py (prelude, read-only): hk_pose3 + MM query trajectory (future samples, actor-relative) and blend-stack anim/time. No property writes.
import builtins, unreal as _u
exec(open(_u.Paths.project_dir()+'Tools/UE59_20261122/hk_pose3.py',encoding='utf8').read())
_base=builtins.VID_TICKHOOK
_once={'n':0}
def _hk9(pw, ai, st, w_):
    o=_base(pw, ai, st, w_)
    o.pop('pq',None)
    try:
        b=o.get('bs') or ''; i=b.find('Animations/'); o['bs']=b[i:i+90] if i>=0 else b[:60]
    except Exception: pass
    try:
        tj=None
        for nm in ('Trajectory','TransformTrajectory','PoseSearchTrajectory'):
            try: tj=ai.get_editor_property(nm); break
            except Exception: tj=None
        if tj is not None:
            sm=tj.get_editor_property('samples'); a=pw.get_actor_location(); out=[]
            for s_ in sm:
                ts=float(s_.get_editor_property('time_in_seconds')) if hasattr(s_,'time_in_seconds') or True else 0
                p=s_.get_editor_property('position'); out.append([round(ts,2),round(p.x-a.x,0),round(p.y-a.y,0)])
            o['tj']=out
    except Exception as e:
        if _once['n']<3: o['tjerr']=repr(e)[:200]; _once['n']+=1
    try:
        m9=[c for c in pw.get_components_by_class(_u.ActorComponent) if c.get_name()=='SphMotion'][0]
        o['cs']=[round(float(m9.get_editor_property('ClipSp')),1),round(float(ai.get_editor_property('SphSelTime')),3)]
    except Exception as e: o['cserr']=repr(e)[:120]
    return o
builtins.VID_TICKHOOK=_hk9
