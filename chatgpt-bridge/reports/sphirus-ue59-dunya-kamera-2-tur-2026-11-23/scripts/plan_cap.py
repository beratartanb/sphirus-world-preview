# plan_cap.py (control, nothing saved): orthographic top-down captures cut at a height. Spawns a transient SceneCapture2D, exports PNG, destroys it.
# Output: Saved/UE59Work/r2g2/plan/<name>.png . The map is left dirty in memory by the spawn; reload the map from disk afterwards.
import unreal as u, builtins, os
EAS=u.get_editor_subsystem(u.EditorActorSubsystem)
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
D=u.Paths.project_dir()+'Saved/UE59Work/r2g2/plan'; os.makedirs(D,exist_ok=True)
JOBS=getattr(builtins,'R2G_PLAN',None) or [
 ('g_cut330', 760, 690, 330, 2000, 2000, 1500, 'base'),
 ('u_cut680', 760, 690, 680, 2000, 2000, 1500, 'base'),
 ('site',     1500, 1500, 3000, 9000, 2000, 2000, 'final'),
 ('site_near',900, 900, 3000, 4200, 2000, 2000, 'final'),
]
a=EAS.spawn_actor_from_class(u.SceneCapture2D,u.Vector(0,0,0),u.Rotator(pitch=-90,yaw=-90,roll=0))
a.set_actor_label('ZZ_R2G_PLANCAP_TRANSIENT')
c=a.capture_component2d
try:
    for (nm,x,y,zc,ow,pw,ph,src) in JOBS:
        rt=u.RenderingLibrary.create_render_target2d(w,pw,ph,u.TextureRenderTargetFormat.RTF_RGBA8)
        c.set_editor_property('projection_type',u.CameraProjectionMode.ORTHOGRAPHIC)
        c.set_editor_property('ortho_width',float(ow))
        c.set_editor_property('texture_target',rt)
        c.set_editor_property('capture_source',u.SceneCaptureSource.SCS_BASE_COLOR if src=='base' else u.SceneCaptureSource.SCS_FINAL_COLOR_LDR)
        c.set_editor_property('capture_every_frame',False); c.set_editor_property('capture_on_movement',False)
        H=3000.0
        a.set_actor_location(u.Vector(x,y,zc+H),False,False)
        if src=='base':
            c.set_editor_property('override_custom_near_clipping_plane',True); c.set_editor_property('custom_near_clipping_plane',H)
        else:
            c.set_editor_property('override_custom_near_clipping_plane',False)
        c.capture_scene()
        u.RenderingLibrary.export_render_target(w,rt,D,nm+'.png')
        print('CAP',nm,os.path.exists(D+'/'+nm+'.png'))
finally:
    EAS.destroy_actor(a)
