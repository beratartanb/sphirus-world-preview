# q_mmcfg.py (measure): dump the motion-matching configuration actually in the project - the driver's PoseHistory collector
# node (trajectory generation / prediction), the MotionMatching node settings, the schema channels and each database's
# settings - to find out why a fresh search prefers the slow start-clip poses at steady walking/running speed.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
import re
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]
for n in B.find_nodes(ag):
    cn=n.get_class().get_name()
    if 'HistoryCollector' in cn or 'MotionMatching' in cn or 'PoseSearch' in cn:
        t=str(n.get_editor_property('node').export_text()); t=re.sub(r'\(X=-?[0-9.]+,Y=-?[0-9.]+,Z=-?[0-9.]+\)','(v)',t)
        print('NODE',cn,len(t)); print(t[:3000])
sch=u.load_asset('/Game/Sphirus/Player/MM/PSS_Sph_Loco'); print('SCHEMA skeleton',sch.get_editor_property('skeleton').get_name() if sch.get_editor_property('skeleton') else None)
for k in ('sample_rate','data_preprocessor','mirror_data_table','number_of_principal_components','add_data_padding'):
    try: print(' ',k,sch.get_editor_property(k))
    except Exception as e: print(' ',k,'ERR',str(e)[:60])
try:
    for c in sch.get_editor_property('channels'):
        try: print('CHANNEL',c.get_class().get_name(),str(c.export_text())[:1200] if hasattr(c,'export_text') else '')
        except Exception as e: print('CHANNEL',c.get_class().get_name(),'ERR',str(e)[:80])
        for k in ('weight','sample_times','samples','debug_color','bone','use_character_speed_multiplier','trajectory_speed_multiplier','sample_role'):
            try: print('   ',k,c.get_editor_property(k))
            except Exception: pass
except Exception as e: print('CHANNELS ERR',str(e)[:100])
for n in ('PSD_Sph_Loco2','PSD_Sph_Walk','PSD_Sph_Jog','PSD_Sph_Run'):
    db=u.load_asset('/Game/Sphirus/Player/MM/'+n)
    out={}
    for k in ('continuing_pose_cost_bias','base_cost_bias','looping_cost_bias','pose_prune_similarity_threshold','exclude_from_database_parameters','additional_extrapolation_time','normalization_set','mirror_type','pose_search_mode','kdtree_max_distance'):
        try: out[k]=str(db.get_editor_property(k))[:60]
        except Exception: pass
    print('DB',n,db.get_num_animation_assets(),out)
# pawn movement
bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); cdo=u.get_default_object(bp.generated_class()); cm=cdo.get_editor_property('character_movement')
print('CMC',{k:str(cm.get_editor_property(k)) for k in ('max_walk_speed','max_acceleration','braking_deceleration_walking','rotation_rate','orient_rotation_to_movement','use_controller_desired_rotation','ground_friction','braking_friction_factor')})
print('PAWN',{k:str(cdo.get_editor_property(k)) for k in ('use_controller_rotation_yaw',)})
for c in cdo.get_editor_property('mesh'),:
    print('MESH',c.get_editor_property('relative_rotation'),c.get_editor_property('relative_location'),c.get_editor_property('skeletal_mesh_asset'))
