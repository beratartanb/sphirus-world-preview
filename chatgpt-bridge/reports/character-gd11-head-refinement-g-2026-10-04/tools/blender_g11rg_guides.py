"""GD11 refinement G: editable hair guides <-> .blend.
export : guides.json -> .blend with one COLLECTION per guide group (nape_to_bun, back_to_bun, side_to_bun, top_to_bun, front_to_bun, bun_loops,
         nape_free, behind_ear, front_side_frame, temple_veil, ear_lock, ...), one POLY curve object per guide (name = guide key), metadata in the
         object's custom property 'meta' (JSON). Bun loop groups also expose 'c_off_x/y/z', 'r', 'turn' as editable custom properties.
         The build head (DNA-order npy) is added as a reference mesh (collection 'reference_head', not exported back).
import : .blend -> guides.json (control points read back from the splines; bun groups from their custom properties).
Rebuild only the edited groups with: SPH_GUIDES_IN=<guides.json> + the same build_env.txt (all random draws stay identical).
usage: blender -b --factory-startup --python blender_g11rg_guides.py -- export <guides.json> <out.blend> <head.npy>
       blender -b <in.blend> --python blender_g11rg_guides.py -- import <out guides.json>"""
import bpy, sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
a = sys.argv[sys.argv.index('--')+1:]; MODE = a[0]
if MODE == 'export':
    G = json.load(open(a[1])); OUTB = a[2]; HEAD = a[3]
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    cols = {}
    def col(name):
        if name not in cols: c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); cols[name] = c
        return cols[name]
    n = 0
    for key, g in G.items():
        if not isinstance(g, dict) or 'ctrl' not in g: continue
        cu = bpy.data.curves.new(key, 'CURVE'); cu.dimensions = '3D'; sp = cu.splines.new('POLY'); P = g['ctrl']; sp.points.add(len(P)-1)
        for i, p in enumerate(P): sp.points[i].co = (p[0], p[1], p[2], 1.0)
        cu.bevel_depth = 0.04 if g['group'] != 'bun_loops' else 0.02
        ob = bpy.data.objects.new(key, cu); col(g['group']).objects.link(ob)
        ob['meta'] = json.dumps({k: v for k, v in g.items() if k != 'ctrl'})
        if g['group'] == 'bun_loops':
            ob['c_off_x'], ob['c_off_y'], ob['c_off_z'] = g['c_off']; ob['r'] = g['r']; ob['turn'] = g['turn']
        n += 1
    from gd_common import head_topology
    X = np.load(HEAD)[:24049]; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]
    me = bpy.data.meshes.new('build_head'); me.from_pydata([tuple(v) for v in X], [], [tuple(t[::-1]) for t in TT]); me.update()
    hob = bpy.data.objects.new('build_head', me); col('reference_head').objects.link(hob)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUTB)); print('GUIDES_EXPORT', n, sorted(cols))
else:
    OUTJ = a[1]; out = {'note': 'imported from '+bpy.data.filepath}
    for c in bpy.data.collections:
        if c.name == 'reference_head': continue
        for ob in c.objects:
            if ob.type != 'CURVE': continue
            meta = json.loads(ob.get('meta', '{}')); sp = ob.data.splines[0]; M = np.array(ob.matrix_world)
            P = [list((M@np.array([p.co[0], p.co[1], p.co[2], 1.0]))[:3]) for p in sp.points]
            d = {**meta, 'group': c.name, 'ctrl': [[round(float(v), 4) for v in p] for p in P]}
            if c.name == 'bun_loops': d.update(c_off=[float(ob['c_off_x']), float(ob['c_off_y']), float(ob['c_off_z'])], r=float(ob['r']), turn=float(ob['turn'])); d.pop('ctrl')
            out[ob.name] = d
    json.dump(out, open(OUTJ, 'w'), indent=0); print('GUIDES_IMPORT', len(out)-1)
