"""Negative/positive self-test of validate_sculpt.py and SPH_TOOLS operators on scratch copies (never the delivered file).
blender -b <pristine.blend> --python selftest_validator.py -- <package> <validator> <tools> <out.json>"""
import bpy, sys, json
import numpy as np
a = sys.argv[sys.argv.index('--')+1:]; PKG, VAL, TOOLS, OUT = a
g = {'__name__': 'v'}; exec(compile(open(VAL).read(), VAL, 'exec'), g); P = g['load_pkg'](PKG)
exec(compile(open(TOOLS).read(), TOOLS, 'exec'), {'__name__': '__main__'})
SRC = bpy.data.filepath
def fresh():
    bpy.ops.wm.open_mainfile(filepath=SRC, load_ui=False)
    ob = bpy.data.objects['SPH_BR_ArtistSculpt']
    if ob.mode != 'OBJECT': bpy.context.view_layer.objects.active = ob; bpy.ops.object.mode_set(mode='OBJECT')
    return ob
def key_move(ob, ids, vec):
    k = ob.data.shape_keys.key_blocks['ARTIST_SCULPT']; co = np.zeros(len(k.data)*3, np.float32); k.data.foreach_get('co', co); co = co.reshape(-1, 3)
    co[ids] += np.asarray(vec, np.float32); k.data.foreach_set('co', co.ravel()); ob.data.update()
def run(name, fn):
    ob = fresh(); fn(ob); R = g['validate'](P)
    bad = {k: c['result'] for k, c in R['checks'].items() if c['result'] != 'PASS'}
    res[name] = {'overall': R['overall'], 'non_pass': bad, 'disp': R['metrics'].get('disp_mm'), 'proportions_drift': {k: v['drift_vs_BR_mm'] for k, v in R['metrics'].get('proportions', {}).items() if abs(v['drift_vs_BR_mm']) > 0.05}}
    print(name, R['overall'], list(bad)[:6], flush=True)
res = {}
face = [int(u) for u in P['groups']['FACE_LOCK']][:50]; seam = [int(u) for u in P['groups']['SEAM_LOCK']][:3]
lab = P['region_label']; br = [u for u, x in enumerate(lab) if x == 'BREASTS']; gl = [u for u, x in enumerate(lab) if x == 'GLUTES']
wbr = {int(u): w for u, w in P['groups']['BREASTS'].items()}
run('pristine', lambda ob: None)
run('face_lock_moved_0.5mm', lambda ob: key_move(ob, face, (0, -0.0005, 0)))
run('seam_moved_0.3mm', lambda ob: key_move(ob, seam, (0.0003, 0, 0)))
def soft(ob):  # plausible small sculpt: 2 mm smooth-weighted forward fullness on the breast region (Blender -Y = UE front)
    k = ob.data.shape_keys.key_blocks['ARTIST_SCULPT']; co = np.zeros(len(k.data)*3, np.float32); k.data.foreach_get('co', co); co = co.reshape(-1, 3)
    for u, w in wbr.items(): co[u, 1] -= 0.002*w*w
    k.data.foreach_set('co', co.ravel()); ob.data.update()
run('plausible_2mm_breast_fullness', soft)
run('big_grab_25mm_glutes', lambda ob: key_move(ob, gl, (0, 0.025, 0)))
def uv(ob): ob.data.uv_layers['UVMap'].data[10].uv = (0.5, 0.5)
run('uv_edited', uv)
run('modifier_added', lambda ob: ob.modifiers.new('Sub', 'SUBSURF'))
def ref_key(ob):
    k = ob.data.shape_keys.key_blocks['BR_NEUTRAL']; k.lock_shape = False; k.data[100].co.x += 0.01
run('reference_key_edited', ref_key)
def topo(ob):
    import bmesh
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.verts.ensure_lookup_table(); bmesh.ops.delete(bm, geom=[bm.verts[5]], context='VERTS'); bm.to_mesh(ob.data); bm.free()
run('vertex_deleted', topo)
def wrongkey(ob): ob.data.shape_keys.key_blocks['ARTIST_SCULPT'].value = 0.5
run('artist_value_0.5', wrongkey)
# tools: isolate then restore must return the exact backup mask and re-hide the head
ob = fresh(); bpy.context.view_layer.objects.active = ob
bpy.ops.object.mode_set(mode='SCULPT'); bpy.ops.sph.isolate_region(region='GLUTES')
m = np.zeros(len(ob.data.vertices), np.float32); ob.data.attributes['.sculpt_mask'].data.foreach_get('value', m)
bk = np.zeros_like(m); ob.data.attributes['sph_mask_backup'].data.foreach_get('value', bk)
iso_free = int((m < 0.5).sum())
ob.data.polygons.foreach_set('hide', np.zeros(len(ob.data.polygons), bool)); ob.data.attributes['.sculpt_mask'].data.foreach_set('value', np.zeros_like(m))
bpy.ops.sph.restore_protection()
m2 = np.zeros_like(m); ob.data.attributes['.sculpt_mask'].data.foreach_get('value', m2)
hid = np.zeros(len(ob.data.polygons), bool); ob.data.polygons.foreach_get('hide', hid)
res['tools'] = {'isolate_glutes_unmasked_verts': iso_free, 'restore_mask_exact': bool(np.array_equal(m2, bk)), 'restore_hidden_polys': int(hid.sum())}
print('tools', res['tools'])
open(OUT, 'w').write(json.dumps(res, indent=1))
