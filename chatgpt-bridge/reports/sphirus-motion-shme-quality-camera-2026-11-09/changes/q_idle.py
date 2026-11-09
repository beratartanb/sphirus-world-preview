# q_idle.py (measure): the idle path of ABP_Sph_Driver - idle sequence players (asset, length, loop, rate, start),
# the idle gate blend node (blend time), the idle-related event graph literals (StillTime threshold), and the idle clips
# in the gait databases (lengths) - to explain the "same short weight-shift repeating" complaint.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
import re
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]
for n in B.find_nodes(ag):
    cn=n.get_class().get_name()
    if cn in ('AnimGraphNode_SequencePlayer','AnimGraphNode_BlendListByBool','AnimGraphNode_ApplyAdditive','AnimGraphNode_LayeredBoneBlend','AnimGraphNode_Slot'):
        t=str(n.get_editor_property('node').export_text()); t=re.sub(r'\(X=-?[0-9.]+,Y=-?[0-9.]+,Z=-?[0-9.]+\)','(v)',t)
        print('ANODE',cn,re.sub(r'Sequence=.*?\.(\w+)\'','Sequence=\\1 ',t)[:700])
C='/Game/Sphirus/Player/Anim/Core/'
for p in ('af_Stand_Idle_01','af_Stand_Idle_02_WeightShift','af_Stand_Idle_TurnL045','af_Loco_Walk_Fwd','af_Loco_Jog_Fwd','af_Loco_Run_Fwd','af_Loco_Walk_Fwd_Start','af_Loco_Walk_Fwd_Stop'):
    a=u.load_asset(C+p)
    if a: print('CLIP',p,round(float(a.get_play_length()),2),'s loop?',a.get_editor_property('loop') if hasattr(a,'loop') else '?','rate',a.get_editor_property('rate_scale'),'rootmotion',a.get_editor_property('enable_root_motion'))
AR=u.AssetRegistryHelpers.get_asset_registry(); idles=[str(a.asset_name) for a in AR.get_assets_by_path('/Game/Sphirus/Player/Anim/Core',False) if 'Idle' in str(a.asset_name) or 'Stand' in str(a.asset_name)]; print('IDLE_CLIPS',idles)
eg=B.get_graph(d,'EventGraph'); N=[pn(x) for x in B.find_nodes(eg)]; tp=lambda p:str(info(p).type_id)
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
for p in N:
    t=tp(p)
    if 'StillTime' in t or 'Idle' in t or 'Breath' in t:
        print('ENODE',t[-60:],{str(x.name):pv(p,str(x.name)) for x in info(p).input_pins if str(x.name) not in ('execute','self')})
print('Q_DONE')
