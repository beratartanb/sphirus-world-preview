# cm_traj2.py (write): second attempt at the schema's past trajectory samples (ObjectTools.set_properties refused the
# struct array; only the channel weight 1.3 took). Builds the samples as Python structs:
#   -0.6 s PositionXY w0.8, -0.3 s PositionXY+FacingXY w1.0, then the existing -0.05 / 0 / 0.35 / 0.7 / 1.0 samples.
# Flags (EPoseSearchTrajectoryFlags): PositionXY=32, FacingDirectionXY=128 (existing samples use 32/144/160/176/4).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from editor_toolset.toolsets.object import ObjectTools as O
_LF=open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/traj2_progress.txt','w')
def P(*a):
    print(*a); print(*a,file=_LF); _LF.flush()
S='/Game/Sphirus/Player/MM/PSS_Sph_Loco'; s=u.load_asset(S)
ch=[c for c in s.get_editor_property('channels') if c.get_class().get_name()=='PoseSearchFeatureChannel_Trajectory'][0]
arr=list(ch.get_editor_property('samples')); t=arr[0]; P('TYPE',type(t).__name__,len(arr))
for k in ('offset','weight','flags','normalization_group','debug_color'):
    try: P(' ',k,t.get_editor_property(k))
    except Exception as e: P(' ',k,'ERR',str(e)[:80])
def mk(off,w,flags):
    x=type(t)()
    try: x.copy_from(t) if hasattr(x,'copy_from') else None
    except Exception: pass
    x.set_editor_property('offset',off); x.set_editor_property('weight',w)
    try: x.set_editor_property('flags',flags)
    except Exception as e:
        P('FLAGS_ERR',str(e)[:100]); x.set_editor_property('flags',t.get_editor_property('flags'))
    return x
new=[mk(-0.6,0.8,32),mk(-0.3,1.0,160)]+arr
ch.set_editor_property('samples',new); ch.set_editor_property('weight',1.3); s.modify()
P('NEW',str(O.get_properties(ch,['Samples','Weight']))[:1200])
assert len(ch.get_editor_property('samples'))==7
assert EA.save_loaded_asset(s,False); P('STEP schema saved')
for n in ('PSD_Sph_Loco2','PSD_Sph_Walk','PSD_Sph_Jog','PSD_Sph_Run','PSD_Sph_Crouch'):
    p='/Game/Sphirus/Player/MM/'+n
    if EA.does_asset_exist(p): EA.save_loaded_asset(u.load_asset(p),False)
P('DONE')
