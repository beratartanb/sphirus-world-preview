# cm_traj1.py (write): the search could not tell "I have been walking" from "I just started": the schema's only past
# trajectory sample was -0.05 s (weight 0.3), so at steady speed it cycled inside the acceleration window of the start
# clips (body matched Walk_Fwd_Start 0.7-1.2 s / Run_Fwd_Start 0.6-1.2 s, loops never played). Adds past samples at
# -0.6 and -0.3 s, raises the trajectory channel weight, and lengthens the driver's trajectory history to cover 1 s.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from editor_toolset.toolsets.object import ObjectTools as O
import json,re
_LF=open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/traj_progress.txt','w')
def P(*a):
    print(*a); print(*a,file=_LF); _LF.flush()
S='/Game/Sphirus/Player/MM/PSS_Sph_Loco'; s=u.load_asset(S)
ch=[c for c in s.get_editor_property('channels') if c.get_class().get_name()=='PoseSearchFeatureChannel_Trajectory'][0]
cur=O.get_properties(ch,['Samples','Weight']); P('CUR',str(cur)[:1500])
cur=json.loads(cur) if isinstance(cur,str) else cur
samples=cur.get('Samples') or cur.get('samples'); assert samples and len(samples)>=3, cur
tmpl=json.loads(json.dumps(samples[-1]))   # keep the flags of an existing sample
def smp(off,w):
    d=json.loads(json.dumps(tmpl))
    for k in list(d):
        if k.lower()=='offset': d[k]=off
        if k.lower()=='weight': d[k]=w
    return d
new=[smp(-0.6,0.8),smp(-0.3,1.0),smp(-0.05,0.3),smp(0.0,1.0),smp(0.35,1.0),smp(0.7,1.0),smp(1.0,1.2)]
P('SET',O.set_properties(ch,json.dumps({'Samples':new,'Weight':1.3})))
P('NEW',str(O.get_properties(ch,['Samples','Weight']))[:1500])
assert EA.save_loaded_asset(s,False); P('STEP schema saved')
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]; n_=0
for n in B.find_nodes(ag):
    if 'HistoryCollector' in n.get_class().get_name():
        nd=n.get_editor_property('node'); t=str(nd.export_text())
        t=re.sub(r'TrajectoryHistoryCount=\d+','TrajectoryHistoryCount=26',t); t=re.sub(r'PoseCount=\d+','PoseCount=4',t)
        nd.import_text(t); n.set_editor_property('node',nd); n_+=1
assert n_==1; L.compile_blueprint(d); P('ERR_D',errs(d)); assert not errs(d); assert EA.save_loaded_asset(d,False); P('STEP driver saved')
for n in ('PSD_Sph_Loco2','PSD_Sph_Walk','PSD_Sph_Jog','PSD_Sph_Run','PSD_Sph_Crouch'):
    p='/Game/Sphirus/Player/MM/'+n
    if EA.does_asset_exist(p): EA.save_loaded_asset(u.load_asset(p),False)
P('DONE')
