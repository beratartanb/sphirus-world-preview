# w_garment3.py (write, gated): (1) re-import the side-taken-in top and shorts over the project copies (same asset names, so the player
# Blueprint keeps pointing at them); (2) kinematic secondary motion for the garment hems: a Material Parameter Collection carries the
# pawn velocity and a smoothed copy (written by the face Anim Blueprint event graph, w_cloth_drive.py); both fabric materials add a small
# world position offset on the lower part of the garment: inertia = (smoothed - actual) velocity, a little drag, a faint flutter.
# This is NOT a cloth simulation (no Chaos Cloth class is exposed to Python in this build); it is bounded to a few centimetres by design.
import unreal as u
E = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); mel = u.MaterialEditingLibrary
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
D = '/Game/Sphirus/CharacterLab/VF2_20261124/Garments'
sk = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel')
R = u.Paths.convert_relative_path_to_full(u.Paths.project_saved_dir()) + 'UE59Work/vf2c/fit/'
for name, f, mi in (('SKM_Sph_RetroTop_VF2', 'retro_top_vf3.fbx', 'MI_Sph_RetroTop_VF2'), ('SKM_Sph_CuffedShorts_VF2', 'cshorts_vf3.fbx', 'MI_Sph_CuffedShorts_VF2')):
    b0 = u.load_asset(D + '/' + name).get_bounds()
    t = u.AssetImportTask(); t.filename = R + f; t.destination_path = D; t.destination_name = name; t.automated = True; t.save = False; t.replace_existing = True
    o = u.FbxImportUI(); o.import_mesh = True; o.import_as_skeletal = True; o.mesh_type_to_import = u.FBXImportType.FBXIT_SKELETAL_MESH; o.skeleton = sk
    o.import_materials = False; o.import_textures = False; o.import_animations = False; o.create_physics_asset = False; o.automated_import_should_detect_type = False
    sd = o.skeletal_mesh_import_data; sd.set_editor_property('update_skeleton_reference_pose', False); sd.set_editor_property('use_t0_as_ref_pose', False); sd.set_editor_property('import_morph_targets', False)
    sd.set_editor_property('normal_import_method', u.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS); t.options = o; AT.import_asset_tasks([t])
    m = u.load_asset(D + '/' + name); b = m.get_bounds(); ms = list(m.materials); mat = u.load_asset(D + '/' + mi)
    for x in ms: x.material_interface = mat
    m.materials = ms
    print('G3', name, 'bounds extent x %.1f -> %.1f, z origin %.1f -> %.1f' % (b0.box_extent.x, b.box_extent.x, b0.origin.z, b.origin.z), 'verts', u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem).get_num_verts(m, 0), [x.material_interface.get_name() for x in m.materials], 'skel', m.skeleton.get_name())
    assert abs(b.origin.z - b0.origin.z) < 4 and abs(b.box_extent.z - b0.box_extent.z) < 4, 'scale/axis mismatch'
    print('G3 saved', name, E.save_loaded_asset(m, False))
# ---- parameter collection
MP = D + '/MPC_Sph_Cloth'
mpc = u.load_asset(MP) if E.does_asset_exist(MP) else AT.create_asset('MPC_Sph_Cloth', D, u.MaterialParameterCollection, u.MaterialParameterCollectionFactoryNew())
ps = []
for n in ('Vel', 'VelSmooth'):
    p = u.CollectionVectorParameter(); p.set_editor_property('parameter_name', n); p.set_editor_property('default_value', u.LinearColor(0, 0, 0, 0)); ps.append(p)
mpc.set_editor_property('vector_parameters', ps); print('G3 mpc params', [str(p.get_editor_property('parameter_name')) for p in mpc.get_editor_property('vector_parameters')], 'saved', E.save_loaded_asset(mpc, False))
# ---- world position offset stage on both fabric materials
def add_wpo(mat, z_top, z_bot, tag):
    if mel.get_material_property_input_node(mat, u.MaterialProperty.MP_WORLD_POSITION_OFFSET): print('G3', tag, 'WPO already present'); return
    X = 600; Y = 1400
    def ex(cls, dx, dy): return mel.create_material_expression(mat, cls, X + dx, Y + dy)
    def cn(v, dx, dy):
        e = ex(u.MaterialExpressionConstant, dx, dy); e.set_editor_property('r', v); return e
    def sc(n, v, dx, dy):
        e = ex(u.MaterialExpressionScalarParameter, dx, dy); e.set_editor_property('parameter_name', n); e.set_editor_property('default_value', v); e.set_editor_property('group', 'VF2 Motion'); return e
    def op(cls, a, b, dx, dy, ao='', bo=''):
        e = ex(cls, dx, dy); assert mel.connect_material_expressions(a, ao, e, 'A'); assert mel.connect_material_expressions(b, bo, e, 'B'); return e
    def cp(n, dx, dy):
        e = ex(u.MaterialExpressionCollectionParameter, dx, dy); e.set_editor_property('collection', mpc); e.set_editor_property('parameter_name', n); return e
    def m3(a, dx, dy):
        e = ex(u.MaterialExpressionComponentMask, dx, dy); e.set_editor_property('r', True); e.set_editor_property('g', True); e.set_editor_property('b', True); e.set_editor_property('a', False); assert mel.connect_material_expressions(a, '', e, ''); return e
    MUL, ADD, SUB, DIV = u.MaterialExpressionMultiply, u.MaterialExpressionAdd, u.MaterialExpressionSubtract, u.MaterialExpressionDivide
    vel = m3(cp('Vel', 0, 0), 250, 0); vs = m3(cp('VelSmooth', 0, 200), 250, 200)
    inert = op(MUL, op(SUB, vs, vel, 450, 100), sc('MotionInertia', 0.008, 450, 260), 620, 120)                     # cm of offset per cm/s of velocity lag
    drag = op(MUL, vel, sc('MotionDrag', -0.0018, 450, 380), 620, 320)
    off = op(ADD, inert, drag, 780, 200)
    # bound the length to MotionMax cm
    dd = ex(u.MaterialExpressionDotProduct, 900, 320); mel.connect_material_expressions(off, '', dd, 'A'); mel.connect_material_expressions(off, '', dd, 'B')
    ln = ex(u.MaterialExpressionSquareRoot, 1020, 320); mel.connect_material_expressions(dd, '', ln, '')
    mx = sc('MotionMax', 2.2, 900, 460); mn = ex(u.MaterialExpressionMin, 1140, 380); mel.connect_material_expressions(ln, '', mn, 'A'); mel.connect_material_expressions(mx, '', mn, 'B')
    lim = op(MUL, off, op(DIV, mn, op(ADD, ln, cn(0.001, 1140, 520), 1260, 440), 1380, 400), 1500, 220)
    # faint flutter so a standing figure is not frozen: two sines on world position
    tm = ex(u.MaterialExpressionTime, 0, 700); wp = ex(u.MaterialExpressionWorldPosition, 0, 800)
    wz = ex(u.MaterialExpressionComponentMask, 200, 800); wz.set_editor_property('r', True); wz.set_editor_property('g', False); wz.set_editor_property('b', False); wz.set_editor_property('a', False); mel.connect_material_expressions(wp, '', wz, '')
    ph = op(ADD, op(MUL, tm, cn(1.7, 200, 650), 360, 680), op(MUL, wz, cn(0.21, 360, 860), 500, 820), 640, 740); sn = ex(u.MaterialExpressionSine, 780, 740); mel.connect_material_expressions(ph, '', sn, '')
    fv = ex(u.MaterialExpressionConstant3Vector, 780, 880); fv.set_editor_property('constant', u.LinearColor(0.6, 0.8, 0.15, 1)); fl = op(MUL, op(MUL, fv, sn, 940, 800), sc('MotionFlutter', 0.12, 940, 940), 1100, 820)
    tot = op(ADD, lim, fl, 1660, 400)
    # hem mask from the pre-skinned (reference pose) height: 0 at z_top, 1 at z_bot
    psk = ex(u.MaterialExpressionPreSkinnedPosition, 0, 1100); pz = ex(u.MaterialExpressionComponentMask, 200, 1100); pz.set_editor_property('r', False); pz.set_editor_property('g', False); pz.set_editor_property('b', True); pz.set_editor_property('a', False)
    mel.connect_material_expressions(psk, '', pz, '')
    zt = sc('MotionZTop', z_top, 200, 1220); zb = sc('MotionZBottom', z_bot, 200, 1320)
    mk = ex(u.MaterialExpressionSaturate, 760, 1160); mel.connect_material_expressions(op(DIV, op(SUB, zt, pz, 420, 1140), op(SUB, zt, zb, 420, 1280), 600, 1180), '', mk, '')
    mk2 = op(MUL, mk, mk, 900, 1160)
    out = op(MUL, tot, mk2, 1820, 600); assert mel.connect_material_property(out, '', u.MaterialProperty.MP_WORLD_POSITION_OFFSET)
    mel.recompile_material(mat); print('G3', tag, 'WPO stage added, expressions', mel.get_num_material_expressions(mat))
fm = u.load_asset(D + '/M_Sph_Fabric_VF2'); add_wpo(fm, 128.0, 104.0, 'top'); print('G3 saved fabric', E.save_loaded_asset(fm, False))
sm = u.load_asset(D + '/M_Sph_CuffedShorts_VF2'); add_wpo(sm, 96.0, 76.0, 'shorts'); print('G3 saved shorts mat', E.save_loaded_asset(sm, False))
for n in ('MI_Sph_RetroTop_VF2', 'MI_Sph_CuffedShorts_VF2'):
    x = u.load_asset(D + '/' + n); mel.update_material_instance(x); print('G3 saved', n, E.save_loaded_asset(x, False))
print('G3 dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
