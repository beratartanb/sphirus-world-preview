# c_house4.py (control job, house map loaded, in-memory): hub wake/bed camera aims at the body on the mattress (z 572, was 648 for
# the floating pose); mask bench inspection framing defaults.
import unreal as u
hub=[a for a in u.EditorLevelLibrary.get_all_level_actors() if a.get_class().get_name()=='BP_GR_DayHub_C']; assert len(hub)==1
print('HUB aim was',hub[0].get_editor_property('GR_CamAim'),'loc',hub[0].get_editor_property('GR_CamLoc'))
hub[0].set_editor_property('GR_CamAim',u.Vector(1222,770,572)); hub[0].modify()
d=u.get_default_object(u.load_asset('/Game/GraceRanger/SF/MaskJob/BP_GR_MaskBench').generated_class())
for k,v in (('GR_InB',58.0),('GR_InS',40.0),('GR_InH',62.0),('GR_InW',0.85)):
    try: d.set_editor_property(k,v)
    except Exception as e: print('MB?',k,str(e)[:60])
for a in u.EditorLevelLibrary.get_all_level_actors():
    if a.get_class().get_name()=='BP_GR_MaskBench_C':
        for k,v in (('GR_InB',58.0),('GR_InS',40.0),('GR_InH',62.0),('GR_InW',0.85)):
            try: a.set_editor_property(k,v)
            except Exception as e: print('MBI?',k,str(e)[:60])
        print('BENCH',a.get_actor_label(),a.get_actor_location(),a.get_editor_property('GR_InB'))
print('HOUSE4 aim',hub[0].get_editor_property('GR_CamAim'),'dirty',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]+[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
