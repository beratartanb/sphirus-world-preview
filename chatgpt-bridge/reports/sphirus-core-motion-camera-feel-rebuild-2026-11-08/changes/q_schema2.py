# q_schema2.py (measure): dump the project pose-search schema PSS_Sph_Loco (channels), the four project databases and
# the vendor Core Motion schema (first one found) with explicit property names (the generic dir() dump crashed the editor).
import unreal as u
AR=u.AssetRegistryHelpers.get_asset_registry(); AL=u.AnimationLibrary
SCH=('skeletons','skeleton','sample_rate','data_preprocessor','mirror_data_table','number_of_principal_components','add_data_padding','number_of_permutations','permutations_time_interval','permutations_time_offset','default_estimated_speed','estimated_speed_curve_name')
CHP=('weight','sample_times','samples','bone','origin_bone','sample_role','input_query_pose','use_character_speed_multiplier','trajectory_speed_multiplier','component_stripping','position_weight','velocity_weight','heading_weight','heading_axis','position_tolerance','curve_name','sub_channels','debug_color','label','event_tag','velocity_threshold')
DBP=('schema','continuing_pose_cost_bias','base_cost_bias','looping_cost_bias','pose_prune_similarity_threshold','exclude_from_database_parameters','additional_extrapolation_time','normalization_set','mirror_type','pose_search_mode','kd_tree_max_leaf_size','kd_tree_query_num_neighbors','skip_search_if_possible','tags','vptree_query_num_neighbors','disable_ddc_cache')
def props(o,names,ml=600):
    for k in names:
        try:
            v=o.get_editor_property(k); s=str(v); print('    ',k,'=',s[:ml])
        except Exception: pass
def schema(p):
    o=u.load_asset(p); print('SCHEMA',p); props(o,SCH)
    try:
        for i,c in enumerate(o.get_editor_property('channels')):
            print('  CH',i,c.get_class().get_name()); props(c,CHP)
            try:
                for j,s in enumerate(c.get_editor_property('sub_channels')): print('    SUB',j,s.get_class().get_name()); props(s,CHP)
            except Exception: pass
    except Exception as e: print('  CH ERR',str(e)[:100])
schema('/Game/Sphirus/Player/MM/PSS_Sph_Loco')
names=[str(a.package_name) for a in AR.get_assets_by_class(u.TopLevelAssetPath('/Script/PoseSearch','PoseSearchSchema'),True)]; print('ALL_SCHEMAS',names)
vend=[n for n in names if '/Sphirus/' not in n]
if vend: schema(vend[0])
for n in ('PSD_Sph_Loco2','PSD_Sph_Walk','PSD_Sph_Jog','PSD_Sph_Run'):
    db=u.load_asset('/Game/Sphirus/Player/MM/'+n); print('DB',n,db.get_num_animation_assets()); props(db,DBP,200)
C='/Game/Sphirus/Player/Anim/Core/'
for n in ('af_Loco_Walk_Fwd_Start','af_Loco_Walk_Fwd_Stop','af_Loco_Walk_Fwd'):
    a=u.load_asset(C+n)
    for tr in [str(t) for t in AL.get_animation_notify_track_names(a)]:
        for e in AL.get_animation_notify_events_for_track(a,tr):
            s=str(e); i=s.find('duration'); j=s.find('trigger_time_offset'); print('EV',n,tr,s[i:i+28] if i>=0 else '-',s[j:j+38] if j>=0 else '-')
print('Q_DONE')
