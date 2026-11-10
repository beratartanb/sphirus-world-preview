# q_abp.py (read-only): GASP ABP copy - anim graph node list, cvar reads (anim set / LOD), chooser tables, breath additive skeleton.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
import collections
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); print('SKEL',a.get_editor_property('target_skeleton').get_path_name())
for g in B.list_graphs(a):
    if g.get_name() not in ('AnimGraph','Update_MotionMatching','EnableSteering','Update_PropertiesFromCharacter','Update_EssentialValues'): continue
    print('== GRAPH',g.get_name())
    for n in B.find_nodes(g):
        i=info(pn(n)); t=str(i.type_id); cls=type(n).__name__
        vals=[]
        for x in i.input_pins:
            try:
                v=str(B.get_pin_value(x.pin_id))
                if v not in ('','None','0','0.0','False'): vals.append('%s=%s'%(x.name,v[:40]))
            except Exception: pass
        print('  ',cls[:40],'|',t[:70],'|',vals[:6])
c=collections.Counter()
for g in B.list_graphs(a):
    for n in B.find_nodes(g):
        for x in info(pn(n)).input_pins:
            try:
                v=str(B.get_pin_value(x.pin_id))
                if 'DDCvar' in v or 'DDCVar' in v: c[v]+=1
            except Exception: pass
print('CVARS',dict(c))
b=u.load_asset('/Game/GraceRanger/SHME/Animations/Exertion/A_SHM_Breath_Additive'); print('BREATH skel',b.get_editor_property('skeleton').get_path_name(),'len',b.get_play_length(),'add',b.get_editor_property('additive_anim_type'))
m=u.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin'); print('UEFN skel',m.get_editor_property('skeleton').get_path_name())
