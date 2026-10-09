"""GD14 Blender SCULPT session (real Blender sculpt brushes, GUI session - background Blender has no 3D-view region for brush strokes).
Builds the DNA-order skin (verts 0..24048, DNA triangles) from a head npy, enters Sculpt Mode and executes a stroke program with the real brush
assets (bpy.ops.sculpt.brush_stroke, override_location=True: dab centres on the surface; radius locked in SCENE units; Blender mesh X-symmetry
about the face midline when 'sym'). Writes the sculpted head npy (non-skin parts unchanged) + a per-stroke log.
Stroke program json: [{"brush": "Draw|Inflate|Smooth|Clay Strips|Clay|Crease Polish|Pinch/Magnify|Flatten/Contrast|Grab|Layer|Blob|Scrape/Fill",
  "dir": "ADD|SUBTRACT", "r": radius_cm, "s": strength, "pts": [[x,y,z] cm project frame | vertex id int], "sym": true, "passes": 1,
  "target_mm": optional (repeat passes until max |d| in the stroke zone reaches it, max 'passes'), "note": "why"}]
usage: blender --factory-startup --python gd15_bsculpt.py -- <head.npy> <topo.npz> <strokes.json> <out.npy> <log.json>"""
import bpy, sys, json, traceback, math, numpy as np, mathutils
from bpy_extras import view3d_utils
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); TP = np.load(a[1]); PROG = json.load(open(a[2])); OUT, LOG = a[3], a[4]
NS = 24049; MX = -0.23; res = {'strokes': []}; ST = {}
def _mir(p):
    if isinstance(p, dict) and 'fp' in p: q = dict(p); q['fp'] = [2*MX-p['fp'][0], p['fp'][1]]; return q
    if isinstance(p, dict) and 'sp' in p: q = dict(p); q['side'] = -p['side']; return q
    if isinstance(p, (list, tuple)): return [2*MX-p[0], p[1], p[2]]
    raise ValueError('vertex-id points cannot be mirrored: %r' % (p,))
# 2026-10-09: Blender mesh X-mirror misses on this asymmetric face (mirrored dab lands off the surface) -> explicit mirrored stroke,
# snapped to the other side's own surface; every stroke runs with Blender symmetry OFF
_P = []
for s_ in PROG:
    a_ = dict(s_); a_['sym'] = False; _P.append(a_)
    if s_.get('sym', True):
        b_ = dict(s_); b_['sym'] = False; b_['pts'] = [_mir(p) for p in s_['pts']]; b_['note'] = '[mirror] '+s_.get('note', '')
        if s_.get('delta'): b_['delta'] = [-s_['delta'][0], s_['delta'][1], s_['delta'][2]]
        if s_.get('view_dir'): b_['view_dir'] = [-s_['view_dir'][0], s_['view_dir'][1], s_['view_dir'][2]]
        _P.append(b_)
PROG = _P
ESS = 'brushes/essentials_brushes-mesh_sculpt.blend/Brush/'
def to_b(P): P = np.asarray(P, float).copy(); P[..., 0] = -(P[..., 0]-MX); return P*0.01         # project cm -> Blender m, midline at x=0
def from_b(B): P = np.asarray(B, float)/0.01; P[..., 0] = -P[..., 0]+MX; return P
def ctx():
    win = bpy.context.window_manager.windows[0]; area = next(a_ for a_ in win.screen.areas if a_.type == 'VIEW_3D'); region = next(r for r in area.regions if r.type == 'WINDOW')
    return win, area, region
def finish():
    json.dump(res, open(LOG, 'w'), indent=1); bpy.ops.wm.quit_blender()
def getV(ob):
    n = len(ob.data.vertices); V = np.empty(n*3); ob.data.vertices.foreach_get('co', V); return V.reshape(-1, 3)
def setup():
    try:
        for o in list(bpy.data.objects): bpy.data.objects.remove(o)
        L, S, T, MI = TP['loops'], TP['start'], TP['total'], TP['mat']; F = L.reshape(-1, 3); keep = (F < NS).all(1); F = F[keep]
        me = bpy.data.meshes.new('GD14_Skin'); me.from_pydata(to_b(X[:NS]).tolist(), [], F[:, ::-1].tolist()); me.update()   # 2026-10-09 FIX: DNA winding is INWARD -> reversed so normals point OUT (ADD = outward); W3..W8 strokes ran inverted
        ob = bpy.data.objects.new('GD14_Skin', me); bpy.context.scene.collection.objects.link(ob); bpy.context.view_layer.objects.active = ob; ob.select_set(True); ST['ob'] = ob.name
        ST['V0'] = getV(ob); bpy.context.preferences.view.smooth_view = 0
        win, area, region = ctx()
        with bpy.context.temp_override(window=win, area=area, region=region):
            bpy.ops.view3d.view_axis(type='FRONT'); bpy.ops.view3d.view_selected(); bpy.ops.object.mode_set(mode='SCULPT')
        bpy.app.timers.register(run, first_interval=1.5)
    except Exception: res['err'] = traceback.format_exc()[-1500:]; finish()
    return None
def surf(ob, p):
    """snap a project-frame point (or vertex id) to the closest skin vertex position (Blender m)"""
    V = getV(ob)
    if isinstance(p, int): return V[p]
    if isinstance(p, dict) and 'fp' in p:   # front projection: front-most skin vertex at project (x, z) (+ optional dy cm along +y after snapping)
        P = from_b(V); x0, z0 = p['fp']; w = p.get('w', 0.15); m = (np.abs(P[:, 0]-x0) < w) & (np.abs(P[:, 2]-z0) < w) & (P[:, 1] > 3)
        i = np.where(m)[0][np.argmax(P[m, 1])]; return V[i]
    if isinstance(p, dict) and 'sp' in p:   # side projection: outer-most skin vertex at project (y, z) on side sgn(x - MX) = p['side']
        P = from_b(V); y0, z0 = p['sp']; w = p.get('w', 0.15); m = (np.abs(P[:, 1]-y0) < w) & (np.abs(P[:, 2]-z0) < w) & (np.sign(P[:, 0]-MX) == p['side'])
        i = np.where(m)[0][np.argmax(np.abs(P[m, 0]-MX))]; return V[i]
    q = to_b(np.asarray(p, float)); return V[np.argmin(((V-q)**2).sum(1))]
def densify(P, step):
    out = [P[0]]
    for p, q in zip(P[:-1], P[1:]):
        k = max(1, int(math.ceil(np.linalg.norm(q-p)/step)))
        for t in range(1, k+1): out.append(p+(q-p)*t/k)
    return np.array(out)
def run():
    try:
        ob = bpy.data.objects[ST['ob']]; win, area, region = ctx(); ts = bpy.context.tool_settings; ups = ts.sculpt.unified_paint_settings
        ups.use_unified_size = False; ups.use_unified_strength = False
        for k, s in enumerate(PROG):
            with bpy.context.temp_override(window=win, area=area, region=region):
                bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', relative_asset_identifier=ESS+s['brush'])
            br = ts.sculpt.brush; br.use_locked_size = 'SCENE'; br.unprojected_size = 2*s['r']*0.01; br.strength = s.get('s', 0.3)   # Blender 5: size = DIAMETER
            if hasattr(br, 'direction') and s.get('dir'):
                try: br.direction = s['dir']
                except Exception: pass
            ob.data.use_mirror_x = bool(s.get('sym', True))
            ctr = np.array([surf(ob, p) for p in s['pts']]); path = densify(ctr, s['r']*0.01*0.2) if len(ctr) > 1 else ctr
            if s.get('delta'):   # Grab / Elastic / Snake Hook: one anchor on the surface, the stroke travels by delta (project cm -> Blender m, x flipped)
                dl = np.asarray(s['delta'], float)*0.01*np.array([-1, 1, 1]); nst = int(s.get('steps', 12)); path = np.array([ctr[0]+dl*t/nst for t in range(nst+1)])
            V0 = getV(ob); zone = np.zeros(len(V0), bool)
            for p in path: zone |= ((V0-p)**2).sum(1) < (s['r']*0.01*1.05)**2
            if s.get('sym', True):
                for p in path*np.array([-1, 1, 1]): zone |= ((V0-p)**2).sum(1) < (s['r']*0.01*1.05)**2
            npass = 0; dmax = 0.0
            for it in range(int(s.get('passes', 1))):
                ptsb = [mathutils.Vector(p) for p in path]
                rv3d = area.spaces.active.region_3d; E = []
                # aim the view along the OUTWARD surface normal at the stroke (raycasts must hit this surface, not the head interior / back)
                Vn = getV(ob); c0 = path.mean(0); near = np.argsort(((Vn-c0)**2).sum(1))[:12]; Nn = np.array([ob.data.vertices[int(i)].normal for i in near]).mean(0)
                hc = to_b(np.array([MX, 2.0, 160.0])); Nn = Nn if np.dot(Nn, c0-hc) > 0 else -Nn; Nn = Nn/np.linalg.norm(Nn)
                if s.get('view_dir'): Nn = np.asarray(s['view_dir'], float)*np.array([-1, 1, 1]); Nn = Nn/np.linalg.norm(Nn)
                rv3d.view_perspective = 'ORTHO'; rv3d.view_location = mathutils.Vector(c0); rv3d.view_rotation = mathutils.Vector((0, 0, 1)).rotation_difference(mathutils.Vector(Nn)); rv3d.view_distance = 0.5; rv3d.update()
                for i, p in enumerate(ptsb):
                    m = view3d_utils.location_3d_to_region_2d(region, rv3d, ob.matrix_world @ p) or mathutils.Vector((region.width/2, region.height/2))
                    E.append({'name': '', 'location': tuple(ob.matrix_world @ p), 'mouse': (m.x, m.y), 'mouse_event': (m.x, m.y), 'is_start': i == 0, 'pressure': 1.0, 'size': 50.0, 'time': float(i)*0.02, 'x_tilt': 0.0, 'y_tilt': 0.0})
                with bpy.context.temp_override(window=win, area=area, region=region):
                    r = bpy.ops.sculpt.brush_stroke(stroke=E, mode='NORMAL', override_location=True)
                    bpy.ops.object.mode_set(mode='OBJECT'); bpy.ops.object.mode_set(mode='SCULPT')
                npass += 1; V1 = getV(ob); dmax = float(np.linalg.norm(V1-V0, axis=1).max())*1000.0
                if s.get('target_mm') and dmax >= s['target_mm']: break
            V1 = getV(ob); d = np.linalg.norm(V1-V0, axis=1)*1000.0
            res['strokes'].append({'k': k, 'brush': s['brush'], 'brush_active': br.name, 'note': s.get('note', ''), 'passes': npass, 'max_mm': round(float(d.max()), 3), 'moved': int((d > 0.01).sum()), 'outside_zone_max_mm': round(float(d[~zone].max()) if (~zone).any() else 0.0, 3), 'result': list(r), 'path0_cm': from_b(path[0]).round(2).tolist(), 'moved_ctr_cm': from_b(V0[d > 0.01*d.max()].mean(0)).round(2).tolist() if d.max() > 0 else None, 'moved_r_cm': round(float(np.linalg.norm(V0[d > 0.01*d.max()]-V0[d > 0.01*d.max()].mean(0), axis=1).max())*100, 2) if d.max() > 0 else None})
        with bpy.context.temp_override(window=win, area=area, region=region): bpy.ops.object.mode_set(mode='OBJECT')
        Y = X.copy(); Y[:NS] = from_b(getV(ob)); np.save(OUT, Y); d = np.linalg.norm(Y-X, axis=1)*10.0
        res['total_max_mm'] = round(float(d.max()), 3); res['total_moved'] = int((d > 0.01).sum()); res['out'] = OUT
    except Exception: res['err'] = traceback.format_exc()[-2000:]
    finish(); return None
bpy.app.timers.register(setup, first_interval=2.0)
