"""GD14 feasibility probe: can Blender's REAL sculpt brushes (bpy.ops.sculpt.brush_stroke with Draw / Inflate / Smooth brush assets) be driven
in a GUI session (not -b: background has no 3D-view region for strokes)? Builds a subdivided sphere, enters Sculpt Mode, frames it in a
VIEW_3D area (timer 1), then after a real redraw runs one Draw stroke across the front (timer 2), measures the displacement, writes JSON, quits.
usage: blender --factory-startup --python gd14_sculpt_gui_probe.py -- <out.json>"""
import bpy, sys, json, traceback, numpy as np, mathutils
from bpy_extras import view3d_utils
OUT = sys.argv[sys.argv.index('--')+1]
res = {'steps': []}; ST = {}
def ctx():
    win = bpy.context.window_manager.windows[0]; area = next(a for a in win.screen.areas if a.type == 'VIEW_3D'); region = next(r for r in area.regions if r.type == 'WINDOW')
    return win, area, region
def finish():
    open(OUT, 'w').write(json.dumps(res, indent=1)); bpy.ops.wm.quit_blender()
def setup():
    try:
        for o in list(bpy.data.objects): bpy.data.objects.remove(o)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=64, radius=1.0); ob = bpy.context.active_object; ST['ob'] = ob.name
        n = len(ob.data.vertices); V0 = np.empty(n*3); ob.data.vertices.foreach_get('co', V0); ST['V0'] = V0.reshape(-1, 3)
        bpy.context.preferences.view.smooth_view = 0
        win, area, region = ctx()
        with bpy.context.temp_override(window=win, area=area, region=region):
            bpy.ops.view3d.view_axis(type='FRONT'); bpy.ops.view3d.view_selected()
            bpy.ops.object.mode_set(mode='SCULPT'); res['steps'].append('sculpt_mode')
            bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Draw'); res['steps'].append('brush_draw_asset')
        bpy.app.timers.register(stroke, first_interval=1.5)
    except Exception: res['err'] = traceback.format_exc()[-1500:]; finish()
    return None
def stroke():
    try:
        ob = bpy.data.objects[ST['ob']]; win, area, region = ctx(); rv3d = area.spaces.active.region_3d
        br = bpy.context.tool_settings.sculpt.brush; res['brush'] = br.name if br else None
        if br: br.size = 60; br.strength = 0.8
        pts = []; locs = []
        for t in np.linspace(-0.4, 0.4, 25):
            w = ob.matrix_world @ mathutils.Vector((t, -(1-t*t-0.01)**0.5, 0.1)); p = view3d_utils.location_3d_to_region_2d(region, rv3d, w); pts.append((p.x, p.y)); locs.append(tuple(w))
        res['pts0'] = pts[0]; res['region'] = [region.width, region.height]
        S = [{'name': '', 'location': locs[i], 'mouse': p, 'mouse_event': p, 'is_start': i == 0, 'pressure': 1.0, 'size': 60.0, 'time': float(i)*0.02, 'x_tilt': 0.0, 'y_tilt': 0.0} for i, p in enumerate(pts)]
        with bpy.context.temp_override(window=win, area=area, region=region):
            res['props'] = [p.identifier for p in bpy.ops.sculpt.brush_stroke.get_rna_type().properties]; res['elem_props'] = [p.identifier for p in bpy.types.OperatorStrokeElement.bl_rna.properties]
            res['poll'] = bpy.ops.sculpt.brush_stroke.poll(); r = bpy.ops.sculpt.brush_stroke(stroke=S, mode='NORMAL', override_location=True); res['stroke_result'] = list(r)
            res['ups_size'] = getattr(bpy.context.tool_settings.sculpt.unified_paint_settings, 'size', None); res['ups_use'] = getattr(bpy.context.tool_settings.sculpt.unified_paint_settings, 'use_unified_size', None); res['br_strength'] = br.strength; res['br_dir'] = getattr(br, 'direction', None); res['sculpt_tool'] = getattr(br, 'sculpt_brush_type', getattr(br, 'sculpt_tool', None))
            bpy.ops.object.mode_set(mode='OBJECT')
        n = len(ob.data.vertices); V1 = np.empty(n*3); ob.data.vertices.foreach_get('co', V1); d = np.linalg.norm(V1.reshape(-1, 3)-ST['V0'], axis=1)
        res['moved_verts'] = int((d > 1e-5).sum()); res['max_disp'] = float(d.max())
    except Exception: res['err'] = traceback.format_exc()[-1500:]
    finish(); return None
bpy.app.timers.register(setup, first_interval=2.0)
