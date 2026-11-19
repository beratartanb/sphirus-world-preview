# w_doorradius_revert.py (write, gated, 2026-11-20): revert of w_doorradius.py - CustomCollisionRadius back to 0.0 (default 60 cm sphere) on the two lower doors; the 36 cm candidate did not fix the wrong-door E and made the WC door untargetable (M_doors, M_doorw).
# with the store door as TargetInteractionActor in 233/244 frames, E still opened the WC door (M_doorc). Instance CustomCollisionRadius
# 36 cm on both doors removes the overlap (72 < 77 cm). Only these two door instances in L_GR_CurrentHouseContent change.
import unreal as u
w = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); EA = u.EditorAssetLibrary
done = []
for a in u.GameplayStatics.get_all_actors_of_class(w, u.Actor):
    if a.get_actor_label() in ('SPH_Door_LowerStoreDoor', 'SPH_Door_LowerWCDoor'):
        a.modify(); a.set_editor_property('CustomCollisionRadius', 0.0)
        try: a.rerun_construction_scripts()
        except Exception as e: print('RERUN?', str(e)[:80])
        sp = [round(c.get_editor_property('sphere_radius'), 1) for c in a.get_components_by_class(u.SphereComponent)]
        done.append((a.get_actor_label(), a.get_editor_property('CustomCollisionRadius'), sp, a.get_outer().get_outer().get_path_name()))
print('DOORS', done)
lv = u.load_asset('/Game/GraceRanger/Maps/L_GR_CurrentHouseContent')
pk = [p for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()]
print('DIRTYMAPS', [p.get_name() for p in pk])
ok = u.EditorLoadingAndSavingUtils.save_packages([p for p in pk if p.get_name().endswith('L_GR_CurrentHouseContent')], True)
print('SAVED', ok)
