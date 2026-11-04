"""board_pfr.py (WRITE job under the map manifest; NEVER saves): Pine Forest palette lineup as editor actors (label PFR_Board_*, folder
PFR_Board) on a plate far outside the play area (x -200 m, y +200 m, z +60 m), one group per row 40 m apart, and an editor-camera
capture of every row (1920x1080, transient CameraActor; no PIE). builtins.PFR_BOARD_MODE 'spawn' (spawn + capture) | 'destroy'.
Output: Saved/Codex/PineForestRedesign_20261104/ref/board/<group>.png, board_layout.json"""
import unreal as u, json, pathlib, math, builtins, time
PJ = pathlib.Path(u.Paths.project_dir()); D = PJ / 'Saved/Codex/PineForestRedesign_20261104/ref/board'; D.mkdir(parents=True, exist_ok=True)
MODE = getattr(builtins, 'PFR_BOARD_MODE', 'spawn')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
A = u.get_editor_subsystem(u.EditorActorSubsystem)
if MODE == 'destroy':
    n = 0
    for a in A.get_all_level_actors():
        if a.get_actor_label().startswith('PFR_Board'):
            A.destroy_actor(a); n += 1
    print('PFR_BOARD destroyed', n)
else:
    P = '/Game/PineForestPack/Meshes/'
    GROUPS = [
        ('canopy_pines', [(P + 'Trees/SM_PineTree01', 'Pine01 26m', 1.0), (P + 'Trees/SM_PineTree02', 'Pine02 22m', 1.0), (P + 'Trees/SM_PineTree03', 'Pine03 28m', 1.0), (P + 'Trees/SM_PineTree04', 'Pine04 39m', 1.0), (P + 'Trees/SM_PineTree05', 'Pine05 19m', 1.0), (P + 'Trees/SM_PineTree06', 'Pine06 13m', 1.0), (P + 'Trees/SM_PineTree07', 'Pine07 21m', 1.0)]),
        ('mid_trees', [(P + 'Trees/LowPoly/SM_PineTreeLow01', 'Low01', 1.0), (P + 'Trees/LowPoly/SM_PineTreeLowMed01', 'LowMed01', 1.0), (P + 'Trees/LowPoly/SM_PineTreeLowMed02', 'LowMed02', 1.0), (P + 'Trees/SM_SonoTreeTall01', 'SonoTall', 1.0), (P + 'Trees/SM_SonoTree01', 'SonoTree', 1.0), ('/Game/Fishermans_Cabin/Meshes/Foliage/Tree/SM_Fir_Tree_03', 'FIR03 (current)', 1.0), ('/Game/Calysto/World/Vegetation/Meshes/SM_Black_Spruce_01', 'BlackSpruce', 1.0)]),
        ('young', [(P + 'Trees/SM_Pine_Juvenile_01', 'Juvenile', 1.0), (P + 'Trees/LowPoly/SM_PineTreeLowSmall01', 'LowSmall', 1.0), (P + 'Plants/SM_SonoSapling01', 'Sapling01', 1.0), (P + 'Plants/SM_SonoSapling02', 'Sapling02', 1.0), (P + 'Plants/SM_SonoSapling03', 'Sapling03', 1.0), ('/Game/Calysto/World/Vegetation/Meshes/SM_Young_Black_Spruce_02', 'YoungSpruce (current)', 1.0)]),
        ('bushes', [(P + 'Plants/SM_Bush01', 'Bush01', 1.0), (P + 'Plants/SM_Bush02', 'Bush02', 1.0), (P + 'Plants/SM_Bush03', 'Bush03', 1.0), (P + 'Plants/SM_BushB01', 'BushB01', 1.0), (P + 'Plants/SM_Bush_SalixElag01', 'Salix01', 1.0), (P + 'Plants/SM_Bush_SalixElag02', 'Salix02', 1.0), ('/Game/Fishermans_Cabin/Meshes/Foliage/Bush/SM_Bush_02', 'FC Bush02 (current)', 1.0), ('/Game/Fishermans_Cabin/Meshes/Foliage/Bush/SM_Bush_06', 'FC Bush06 (current)', 1.0)]),
        ('floor_litter', [(P + 'DeadLeaves/SM_DeadLeaves01', 'DL01', 1.0), (P + 'DeadLeaves/SM_DeadLeaves02', 'DL02 (current)', 1.0), (P + 'DeadLeaves/SM_DeadLeaves03', 'DL03', 1.0), (P + 'DeadLeaves/SM_DeadLeaves04', 'DL04', 1.0), (P + 'DeadLeaves/SM_DeadBranch01', 'DeadBranch', 1.0), (P + 'Trees/LowPoly/SM_FallenBranches01', 'FallenBr01', 1.0), (P + 'TerrainPatches/SM_PineAcorn01', 'Cone', 2.0), (P + 'Particle/SM_DeadPineNeedle01', 'Needle', 3.0)]),
        ('floor_patches', [(P + 'TerrainPatches/SM_PineGroundPatch01', 'GP01', 1.0), (P + 'TerrainPatches/SM_PineGroundPatch02', 'GP02', 1.0), (P + 'TerrainPatches/SM_PineGroundPatch03', 'GP03', 1.0), (P + 'TerrainPatches/SM_PineGroundPatch06', 'GP06', 1.0), (P + 'TerrainPatches/SM_RockyGround01', 'Rocky01', 1.0), (P + 'TerrainPatches/SM_ForestTrailPatches01', 'Trail01', 1.0), (P + 'TerrainPatches/SM_ForestTrailPatches02', 'Trail02', 1.0)]),
        ('moss_cover', [(P + 'Moss/SM_MossLeaf_01', 'MossLeaf01', 3.0), (P + 'Moss/SM_MossLeaf_02', 'MossLeaf02', 3.0), (P + 'Moss/SM_MossLeaf_03', 'MossLeaf03', 3.0), (P + 'Moss/SM_MossLeaf_04', 'MossLeaf04', 3.0), (P + 'Moss/SM_MossClump01', 'MossClump', 3.0), (P + 'GroundCover/SM_WeedA_01', 'WeedA01', 1.0), (P + 'GroundCover/SM_GroundCover02', 'GC02', 1.0), (P + 'GroundCover/SM_IvyBed01', 'IvyBed', 1.0), (P + 'GroundCover/SM_Mushroom01', 'Mush01', 2.0), (P + 'GroundCover/SM_MushroomHanging01', 'MushHang', 2.0)]),
        ('deadwood', [(P + 'TerrainPatches/SM_PineDeadTrunk01', 'DeadTrunk01', 1.0), (P + 'TerrainPatches/SM_PineDeadTrunk02', 'DeadTrunk02', 1.0), (P + 'TerrainPatches/SM_PineDeadTrunk04', 'DeadTrunk04', 1.0), (P + 'TerrainPatches/SM_FallenTree01', 'FallenTree', 1.0), (P + 'Props/SM_TrunkPile01', 'TrunkPile', 1.0), (P + 'TerrainPatches/SM_TreeStump01', 'Stump01', 1.0), (P + 'TerrainPatches/SM_TreeStump02', 'Stump02', 1.0)]),
        ('rocks', [(P + 'Cliffs/SM_PineGroundRock01', 'GRock01', 1.0), (P + 'Cliffs/SM_PineGroundRock02', 'GRock02', 1.0), (P + 'Cliffs/SM_PineGroundRock03', 'GRock03', 1.0), (P + 'Cliffs/SM_PineGroundRock04', 'GRock04', 1.0), (P + 'Cliffs/SM_PineGroundRock06', 'GRock06', 1.0), (P + 'Rocks/SM_PineStone01', 'Stone01', 1.0), (P + 'Rocks/SM_PineStone02', 'Stone02', 1.0), (P + 'Rocks/SM_SmallStones01', 'Small01', 1.0)]),
        ('cliffs', [(P + 'Cliffs/SM_CliffRock01', 'Cliff01', 1.0), (P + 'Cliffs/SM_CliffRock02', 'Cliff02', 1.0), (P + 'Cliffs/SM_CliffRockCurve01', 'Curve01', 1.0), (P + 'Cliffs/SM_PineCliff02', 'PineCliff02', 1.0), (P + 'Cliffs/SM_PineCliff03', 'PineCliff03', 1.0), (P + 'Cliffs/SM_ForestEmbankment01', 'Embankment', 1.0), ('/Game/Environment_Set/Environment/Rocks/Models/SM_Big_Rock_01', 'ES BigRock01', 1.0), ('/Game/Environment_Set/Environment/Rocks/Models/SM_Middle_Rock_01', 'ES MidRock01', 1.0)]),
        ('ferns_grass', [(P + 'Plants/SM_Fern01', 'Fern01', 1.0), (P + 'Plants/SM_Fern02', 'Fern02', 1.0), (P + 'Plants/SM_Fern03', 'Fern03', 1.0), (P + 'Plants/SM_FernLong01', 'FernLong01', 1.0), (P + 'Plants/SM_FernLong02', 'FernLong02', 1.0), (P + 'Plants/SM_FernWild01', 'FernWild01', 1.0), (P + 'Plants/SM_FernWide_01', 'FernWide', 1.0), (P + 'Grass/SM_GrassSmall01', 'GrassS', 1.0), (P + 'Grass/SM_GrassMedium01', 'GrassM', 1.0), (P + 'Grass/SM_GrassSmallSparse01', 'GrassSparse', 1.0)]),
    ]
    BX, BY, BZ, ROW = -20000.0, 20000.0, 6000.0, 4000.0
    cube = u.load_asset('/Engine/BasicShapes/Cube')
    plate = A.spawn_actor_from_class(u.StaticMeshActor, u.Vector(BX, BY + ROW * len(GROUPS) / 2, BZ - 50), u.Rotator(0, 0, 0))
    plate.static_mesh_component.set_static_mesh(cube); plate.set_actor_scale3d(u.Vector(300.0, ROW * (len(GROUPS) + 1) / 100.0, 1.0))
    plate.set_actor_label('PFR_Board_Plate'); plate.set_folder_path('PFR_Board')
    shots = []; layout = []
    for gi, (gname, items) in enumerate(GROUPS):
        y = BY + ROW * gi; x = BX - 1500.0; xs = []; hmax = 100.0; rec = {'name': gname, 'items': []}
        for mesh, label, sc in items:
            m = u.load_asset(mesh)
            if not m:
                rec['items'].append({'mesh': mesh, 'label': label, 'missing': True}); continue
            b = m.get_bounds(); w = max(b.box_extent.x, b.box_extent.y) * sc; h = b.box_extent.z * 2 * sc
            x += w + 150.0
            a = A.spawn_actor_from_class(u.StaticMeshActor, u.Vector(x, y, BZ - (b.origin.z - b.box_extent.z) * sc), u.Rotator(0, 0, 0))
            a.static_mesh_component.set_static_mesh(m); a.set_actor_scale3d(u.Vector(sc, sc, sc)); a.set_actor_label('PFR_Board_%02d_%s' % (gi, label.replace(' ', '_')))
            a.set_folder_path('PFR_Board'); xs.append(x); hmax = max(hmax, h); x += w
            rec['items'].append({'mesh': mesh, 'label': label, 'scale': sc, 'w_m': round(2 * w / 100, 1), 'h_m': round(h / 100, 1)})
        if not xs:
            layout.append(rec); continue
        cx = (min(xs) + max(xs)) / 2; span = max(xs) - min(xs) + 500
        dist = max(span / (2 * math.tan(math.radians(40))), hmax / (2 * math.tan(math.radians(24))), 400.0) + 200.0
        camz = BZ + max(160.0, hmax * 0.45); pitch = -math.degrees(math.atan2(camz - BZ - hmax * 0.45, dist))
        shots.append({'name': gname, 'loc': [cx, y + dist, camz], 'rot': [round(pitch, 1), -90.0], 'fov': 80.0})
        if hmax > 800:    # trees: a second, close shot of the trunk bases
            shots.append({'name': gname + '_base', 'loc': [cx, y + 900.0, BZ + 160.0], 'rot': [-8.0, -90.0], 'fov': 80.0})
        rec.update({'dist_m': round(dist / 100, 1), 'hmax_m': round(hmax / 100, 1)}); layout.append(rec)
    (D / 'board_layout.json').write_text(json.dumps(layout, indent=1))
    # capture with a transient camera (editor render), then leave the board for the destroy job
    cam = A.spawn_actor_from_class(u.CameraActor, u.Vector(0, 0, 0)); cam.set_actor_label('PFR_Board_Cam'); cc = cam.camera_component; cc.set_editor_property('constrain_aspect_ratio', False)
    st = {'i': 0, 'phase': 'pos', 't': time.monotonic()}

    def tick(dt):
        try:
            now = time.monotonic()
            if st['i'] >= len(shots):
                u.unregister_slate_post_tick_callback(builtins.PFR_BOARD_H); (D / 'board_done').write_text('ok'); return
            s = shots[st['i']]; fn = D / (s['name'] + '.png')
            if st['phase'] == 'pos':
                cam.set_actor_location_and_rotation(u.Vector(*s['loc']), u.Rotator(pitch=s['rot'][0], yaw=s['rot'][1], roll=0), False, True); cc.set_editor_property('field_of_view', s['fov']); st.update(phase='warm', t=now)
            elif st['phase'] == 'warm' and now - st['t'] > (10.0 if st['i'] == 0 else 2.0):
                if fn.exists(): fn.unlink()
                u.AutomationLibrary.take_high_res_screenshot(1920, 1080, str(fn), camera=cam, delay=0.5); st.update(phase='shoot', t=now)
            elif st['phase'] == 'shoot' and ((fn.exists() and fn.stat().st_size > 0 and now - st['t'] > 2.0) or now - st['t'] > 60):
                st.update(i=st['i'] + 1, phase='pos', t=now)
        except Exception as ex:
            u.unregister_slate_post_tick_callback(builtins.PFR_BOARD_H); (D / 'board_done').write_text('error ' + repr(ex)[:200])
    if (D / 'board_done').exists(): (D / 'board_done').unlink()
    builtins.PFR_BOARD_H = u.register_slate_post_tick_callback(tick)
    print('PFR_BOARD spawned groups', len(layout), 'shots', len(shots))
