# q_vendor.py (measure): the vendor Core Motion schema / database / anim blueprint for MCPaul, and our driver mesh
# orientation, to compare trajectory space, heading axis, bones, weights and node settings with PSS_Sph_Loco.
import unreal as u, re
AR=u.AssetRegistryHelpers.get_asset_registry()
SCH=('skeletons','sample_rate','data_preprocessor','number_of_permutations','permutations_time_offset','permutations_time_interval')
CHP=('weight','sample_times','samples','bone','origin_bone','sample_role','input_query_pose','use_character_speed_multiplier','trajectory_speed_multiplier','component_stripping','heading_axis','label','curve_name')
def props(o,names,ind='    ',ml=500):
    for k in names:
        try:
            v=o.get_editor_property(k); s=str(v)
            if k in ('bone','origin_bone'):
                try: s=str(v.get_editor_property('bone_name'))
                except Exception: pass
            if k=='samples':
                try: s=str([(round(float(x.get_editor_property('offset')),2),int(x.get_editor_property('flags')),round(float(x.get_editor_property('weight')),2)) for x in v])
                except Exception as e: s='ERR '+str(e)[:60]
            print(ind,k,'=',s[:ml])
        except Exception: pass
def schema(p):
    o=u.load_asset(p); print('SCHEMA',p); props(o,SCH)
    for i,c in enumerate(o.get_editor_property('channels')):
        print('  CH',i,c.get_class().get_name()); props(c,CHP)
        try:
            for j,s in enumerate(c.get_editor_property('sub_channels')): print('    SUB',j,s.get_class().get_name()); props(s,CHP,'       ')
        except Exception: pass
names=[str(a.package_name) for a in AR.get_assets_by_class(u.TopLevelAssetPath('/Script/PoseSearch','PoseSearchSchema'),True)]
vend=[n for n in names if 'Core_Motion' in n or 'CoreMotion' in n]; print('VENDOR_SCHEMAS',vend)
for p in vend[:2]: schema(p)
schema('/Game/Sphirus/Player/MM/PSS_Sph_Loco')
dbs=[str(a.package_name) for a in AR.get_assets_by_class(u.TopLevelAssetPath('/Script/PoseSearch','PoseSearchDatabase'),True) if 'Core_Motion' in str(a.package_name)]; print('VENDOR_DBS',dbs[:12])
abps=[str(a.package_name) for a in AR.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine','AnimBlueprint'),True) if 'Core_Motion' in str(a.package_name)]; print('VENDOR_ABPS',abps[:12])
exec(open(u.Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
for p in abps[:3]:
    d=u.load_asset(p)
    for g in B.list_graphs(d):
        for n in B.find_nodes(g):
            cn=n.get_class().get_name()
            if 'HistoryCollector' in cn or 'MotionMatching' in cn:
                t=str(n.get_editor_property('node').export_text()); t=re.sub(r'\(X=-?[0-9.]+,Y=-?[0-9.]+,Z=-?[0-9.]+\)','(v)',t); print('VNODE',p.split('/')[-1],cn,t[:1400])
bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); cdo=u.get_default_object(bp.generated_class())
m=cdo.get_editor_property('mesh'); print('DRIVER_MESH',m.get_editor_property('relative_rotation'),m.get_editor_property('relative_location'),m.get_editor_property('skeletal_mesh_asset'),m.get_editor_property('visibility_based_anim_tick_option'))
print('Q_DONE')
