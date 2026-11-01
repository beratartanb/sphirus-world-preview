"""xr3_board_spawn.py (WRITE job under the map manifest; NEVER saves): asset lineup board as EDITOR actors (label XR3_Board_*, folder
XR3_Board) on a plate far outside the play area (x -200 m, y +200 m, z +60 m), one group per row 40 m apart; writes the player-camera
view list for xr2_views.py (one station per group, framed by the tallest mesh). builtins.XR3_MODE 'spawn' | 'destroy'.
Output: data/board_views.json, data/board_layout.json"""
import unreal as u, json, pathlib, math, builtins
PJ = pathlib.Path(u.Paths.project_dir()); D = PJ / 'Saved/Codex/ExteriorIdentity_XR3_20261031/data'
MODE = getattr(builtins, 'XR3_MODE', 'spawn')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
A = u.get_editor_subsystem(u.EditorActorSubsystem)
if MODE == 'destroy':
    n = 0
    for a in A.get_all_level_actors():
        if a.get_actor_label().startswith('XR3_Board'):
            A.destroy_actor(a); n += 1
    print('XR3_BOARD destroyed', n)
else:
  GROUPS = json.loads((D / 'board_groups.json').read_text())
  BX, BY, BZ, ROW = -20000.0, 20000.0, 6000.0, 4000.0
  cube = u.load_asset('/Engine/BasicShapes/Cube')
  plate = A.spawn_actor_from_class(u.StaticMeshActor, u.Vector(BX, BY + ROW * len(GROUPS) / 2, BZ - 50), u.Rotator(0, 0, 0))
  plate.static_mesh_component.set_static_mesh(cube); plate.set_actor_scale3d(u.Vector(250.0, ROW * (len(GROUPS) + 1) / 100.0, 1.0))
  plate.set_actor_label('XR3_Board_Plate'); plate.set_folder_path('XR3_Board')
  views = []; layout = []
  for gi, g in enumerate(GROUPS):
      y = BY + ROW * gi; x = BX - 1500.0; xs = []; hmax = 100.0; rec = {'name': g['name'], 'items': []}
      for mesh, label, sc in g['items']:
          m = u.load_asset(mesh)
          if not m:
              rec['items'].append({'mesh': mesh, 'label': label, 'missing': True}); continue
          b = m.get_bounds(); w = max(b.box_extent.x, b.box_extent.y) * sc; h = b.box_extent.z * 2 * sc
          x += w + 150.0
          a = A.spawn_actor_from_class(u.StaticMeshActor, u.Vector(x, y, BZ - (b.origin.z - b.box_extent.z) * sc), u.Rotator(0, 0, 0))
          a.static_mesh_component.set_static_mesh(m); a.set_actor_scale3d(u.Vector(sc, sc, sc)); a.set_actor_label('XR3_Board_%02d_%s' % (gi, label.replace(' ', '_')))
          a.set_folder_path('XR3_Board'); xs.append(x); hmax = max(hmax, h); x += w
          rec['items'].append({'mesh': mesh, 'label': label, 'scale': sc, 'w_m': round(2 * w / 100, 1), 'h_m': round(h / 100, 1)})
      if not xs:
          layout.append(rec); continue
      cx = (min(xs) + max(xs)) / 2; span = max(xs) - min(xs) + 500
      dist = max(span / (2 * math.tan(math.radians(30))), hmax / (2 * math.tan(math.radians(20))), 500.0) + 300.0
      pitch = max(-20.0, min(8.0, -math.degrees(math.atan2(hmax * 0.45 - 160, dist)) + 2))
      views.append({'name': g['name'], 'pawn': [round(cx), round(y + dist)], 'yaw': -90.0, 'pitch': round(pitch, 1)})
      rec.update({'dist_m': round(dist / 100, 1), 'hmax_m': round(hmax / 100, 1)}); layout.append(rec)
  (D / 'board_views.json').write_text(json.dumps(views)); (D / 'board_layout.json').write_text(json.dumps(layout, indent=1))
  print('XR3_BOARD spawned groups', len(layout), 'views', len(views))
