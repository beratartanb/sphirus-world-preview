#!/bin/bash
# diag_corr.sh: why does the test corridor (L_Sph_MoveTest) render black in PIE captures? (first run: HighResShot without UI
# is entirely black -> the world itself renders black, not a UI overlay). Loads the map, starts PIE, prints lights / sky /
# fog / actors / view target / cine state (each guarded), takes a UI window shot and a no-UI high-res shot, reloads the house map.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
. Tools/Grip_20261106/g.sh
F=Saved/Codex/Day_20261107/frames
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep LOADED | cut -c1-160
AA(){ powershell.exe -NoProfile -Command "(New-Object -ComObject WScript.Shell).AppActivate('sphirus') | Out-Null"; }
AA; PS; NOTHR; W 8
DX "[rel(k) for k in ('W','A','S','D','C','SpaceBar','LeftShift')]; at(-200,0,100,0,-12)
def T(k,f):
    try: print(k,f())
    except Exception as e: print(k,'ERR',str(e)[:100])
cm=PC.player_camera_manager; GA=u.GameplayStatics.get_all_actors_of_class
T('FADE',lambda:(cm.get_editor_property('fade_amount'),cm.get_editor_property('fade_color')))
T('WIDGETS',lambda:[w.get_class().get_name()+':'+str(w.get_visibility()) for w in u.WidgetBlueprintLibrary.get_all_widgets_of_class(W,u.UserWidget,False)])
T('LIGHTS',lambda:[(a.get_class().get_name(),a.get_actor_label(),round(a.get_component_by_class(u.LightComponent).get_editor_property('intensity'),2)) for a in GA(W,u.Light)])
T('SKY',lambda:[(a.get_class().get_name(),a.get_actor_label()) for a in GA(W,u.SkyLight)+GA(W,u.SkyAtmosphere)+GA(W,u.ExponentialHeightFog)+GA(W,u.VolumetricCloud)])
T('PPV',lambda:[(a.get_actor_label(),a.get_editor_property('unbound'),a.get_editor_property('blend_weight')) for a in GA(W,u.PostProcessVolume)])
T('VIEW',lambda:(PC.get_view_target().get_name(),str(cm.get_camera_location()),str(cm.get_camera_rotation()),cm.get_fov_angle()))
T('CINE',lambda:[(c.get_name(),c.is_active(),c.get_editor_property('current_aperture'),c.get_editor_property('focus_settings').get_editor_property('manual_focus_distance'),c.get_editor_property('post_process_blend_weight')) for c in PW.get_components_by_class(u.CineCameraComponent)])
T('CAMS',lambda:[(c.get_name(),c.is_active()) for c in PW.get_components_by_class(u.CameraComponent)])
T('WP',lambda:(W.get_editor_property('world_type') if False else None, [a.get_actor_label() for a in GA(W,u.WorldPartitionMiniMap)]))
T('ACTORS',lambda:(len(GA(W,u.Actor)),sorted(set(a.get_class().get_name() for a in GA(W,u.Actor)))[:40]))
T('SM',lambda:[(a.get_actor_label(),str(a.get_actor_location())) for a in GA(W,u.StaticMeshActor)][:8])
T('PAWN',lambda:(str(PW.get_actor_location()),PW.mesh.is_visible(),[c.get_name() for c in PW.get_components_by_class(u.SkeletalMeshComponent) if c.is_visible()]))
T('EXPO',lambda:cm.get_editor_property('default_fov'))" 8 | grep -E "^(FADE|WIDGETS|LIGHTS|SKY|PPV|VIEW|CINE|CAMS|WP|ACTORS|SM|PAWN|EXPO)|Error|Traceback"
W 2; UI $F/corr_ui.png; HR $F/corr_hr.png 1510x922
W 2; PE
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -E "LOADED|Error" | cut -c1-160
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --factory-startup --python Tools/Day_20261107/sharp.py -- "$PWD/$F/corr_ui.png" "$PWD/$F/corr_hr.png" 2>&1 | grep SHARP
