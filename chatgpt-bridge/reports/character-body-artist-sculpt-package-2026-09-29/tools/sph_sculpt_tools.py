"""SPHIRUS sculpt helper panel (3D View > Sidebar (N) > SPHIRUS).
Registered automatically when the file is opened with 'Auto Run Python Scripts' allowed; otherwise open the Text Editor,
select SPH_TOOLS.py and press Run Script once. The helpers only change masks / visibility / which object is shown.
They never move vertices."""
import bpy, os, json
import numpy as np

OBJ = 'SPH_BR_ArtistSculpt'
REGIONS = ['NECK_COLLAR', 'SHOULDERS', 'CHEST_RIBCAGE', 'BREASTS', 'ABDOMEN', 'UPPER_BACK', 'LOWER_BACK', 'PELVIS_HIPS',
           'GLUTES', 'THIGHS', 'KNEES', 'CALVES_ANKLES', 'UPPER_ARMS', 'ELBOWS_FOREARMS']

def sob(): return bpy.data.objects.get(OBJ)
def group_weights(ob, name):
    gi = ob.vertex_groups[name].index; w = np.zeros(len(ob.data.vertices), np.float32)
    for v in ob.data.vertices:
        for g in v.groups:
            if g.group == gi: w[v.index] = g.weight
    return w
def base_mask(ob):
    a = np.zeros(len(ob.data.vertices), np.float32); ob.data.attributes['sph_mask_backup'].data.foreach_get('value', a); return a
def set_mask(ob, m):
    mode = ob.mode
    if mode == 'SCULPT': bpy.ops.object.mode_set(mode='OBJECT')
    at = ob.data.attributes.get('.sculpt_mask') or ob.data.attributes.new('.sculpt_mask', 'FLOAT', 'POINT')
    at.data.foreach_set('value', np.clip(m, 0, 1).astype(np.float32)); ob.data.update()
    if mode == 'SCULPT': bpy.ops.object.mode_set(mode='SCULPT')
def ensure_state(ob):
    kb = ob.data.shape_keys.key_blocks
    for n in ('ACCEPTED_B2', 'BR_NEUTRAL', 'SCULPT_BASE'): kb[n].lock_shape = True
    kb['BR_NEUTRAL'].value = 0; kb['SCULPT_BASE'].value = 0; kb['ARTIST_SCULPT'].value = 1
    ob.active_shape_key_index = list(kb.keys()).index('ARTIST_SCULPT')
def rehide_head(ob):
    mode = ob.mode
    if mode == 'SCULPT': bpy.ops.object.mode_set(mode='OBJECT')
    me = ob.data; fs = np.zeros(len(me.polygons), np.int32); me.attributes['.sculpt_face_set'].data.foreach_get('value', fs)
    hide = fs == 100; me.polygons.foreach_set('hide', hide)
    T = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', T); T = T.reshape(-1, 3)
    vis = np.zeros(len(me.vertices), bool); vis[T[~hide].ravel()] = True; me.vertices.foreach_set('hide', ~vis)
    ed = np.zeros(len(me.edges)*2, np.int32); me.edges.foreach_get('vertices', ed); ed = ed.reshape(-1, 2)
    me.edges.foreach_set('hide', ~(vis[ed[:, 0]] & vis[ed[:, 1]])); me.update()
    if mode == 'SCULPT': bpy.ops.object.mode_set(mode='SCULPT')

class SPH_OT_restore(bpy.types.Operator):
    bl_idname = 'sph.restore_protection'; bl_label = 'Restore Protection (mask + hidden head + key state)'
    def execute(self, ctx):
        ob = sob(); ensure_state(ob); rehide_head(ob); set_mask(ob, base_mask(ob))
        for n in ('SPH_LOCKED_HEAD_DISPLAY',): bpy.data.objects[n].hide_viewport = False
        ob.hide_viewport = False; ob.hide_set(False)
        self.report({'INFO'}, 'Protection restored'); return {'FINISHED'}
class SPH_OT_isolate(bpy.types.Operator):
    bl_idname = 'sph.isolate_region'; bl_label = 'Isolate Region'
    region: bpy.props.EnumProperty(items=[(r, r.replace('_', ' ').title(), '') for r in REGIONS])
    def execute(self, ctx):
        ob = sob(); ensure_state(ob)
        m = np.maximum(base_mask(ob), 1.0-group_weights(ob, self.region)); set_mask(ob, m)
        self.report({'INFO'}, f'Only {self.region} is sculptable (feathered edges). Locks still active.'); return {'FINISHED'}
class SPH_OT_compare(bpy.types.Operator):
    bl_idname = 'sph.compare'; bl_label = 'Compare'
    state: bpy.props.EnumProperty(items=[('SCULPT', 'My sculpt', ''), ('REF_ACCEPTED_B2', 'Accepted B2', ''), ('REF_BR_NEUTRAL', 'BR_Neutral (start)', ''), ('SIDE', 'Side by side', '')])
    def execute(self, ctx):
        ob = sob(); lc = ctx.view_layer.layer_collection.children['SPH_REFERENCE_READONLY']
        if ctx.object and ctx.object.mode == 'SCULPT' and self.state != 'SCULPT': bpy.ops.object.mode_set(mode='OBJECT')
        for n, dx in (('REF_ACCEPTED_B2', -1.0), ('REF_BR_NEUTRAL', 1.0)): bpy.data.objects[n].location.x = dx
        if self.state == 'SCULPT':
            lc.hide_viewport = True; ob.hide_set(False); ctx.view_layer.objects.active = ob; bpy.ops.object.mode_set(mode='SCULPT')
        elif self.state == 'SIDE':
            lc.hide_viewport = False; ob.hide_set(False)
        else:
            lc.hide_viewport = False; bpy.data.objects[self.state].location.x = 0.0; ob.hide_set(True)
            other = 'REF_BR_NEUTRAL' if self.state == 'REF_ACCEPTED_B2' else 'REF_ACCEPTED_B2'; bpy.data.objects[other].hide_set(True)
            bpy.data.objects[self.state].hide_set(False)
        if self.state in ('SCULPT', 'SIDE'):
            for n in ('REF_ACCEPTED_B2', 'REF_BR_NEUTRAL'): bpy.data.objects[n].hide_set(False)
        return {'FINISHED'}
class SPH_OT_toggle(bpy.types.Operator):
    bl_idname = 'sph.toggle_collection'; bl_label = 'Toggle'
    coll: bpy.props.StringProperty()
    def execute(self, ctx):
        lc = ctx.view_layer.layer_collection.children[self.coll]; lc.hide_viewport = not lc.hide_viewport; return {'FINISHED'}
class SPH_OT_validate(bpy.types.Operator):
    bl_idname = 'sph.validate'; bl_label = 'Validate Sculpt (read-only)'
    def execute(self, ctx):
        ob = sob(); vp = ob.get('sph_validator'); pk = ob.get('sph_package_path')
        if ctx.object and ctx.object.mode == 'SCULPT': bpy.ops.object.mode_set(mode='OBJECT'); back = True
        else: back = False
        g = {'__name__': 'sph_validator'}; exec(compile(open(vp).read(), vp, 'exec'), g)
        R = g['validate'](g['load_pkg'](pk)); txt = g['summary'](R)
        out = os.path.splitext(bpy.data.filepath)[0]+'_validation.json' if bpy.data.filepath else None
        if out: open(out, 'w').write(json.dumps(R, indent=1))
        t = bpy.data.texts.get('SPH_LAST_VALIDATION') or bpy.data.texts.new('SPH_LAST_VALIDATION'); t.from_string(txt)
        ctx.scene['sph_last_validation'] = R['overall']
        if back: bpy.ops.object.mode_set(mode='SCULPT')
        self.report({'INFO'} if R['overall'] != 'FAIL' else {'ERROR'}, 'Validation: '+R['overall']+' (details in Text Editor: SPH_LAST_VALIDATION)')
        return {'FINISHED'}

class SPH_PT_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = 'SPHIRUS'; bl_label = 'SPHIRUS Artist Sculpt'
    def draw(self, ctx):
        L = self.layout; ob = sob()
        if ob is None: L.label(text='SPH_BR_ArtistSculpt missing!'); return
        kb = ob.data.shape_keys.key_blocks; ak = ob.active_shape_key
        ok = ak is not None and ak.name == 'ARTIST_SCULPT' and abs(kb['ARTIST_SCULPT'].value-1) < 1e-6
        box = L.box(); box.label(text=('Sculpting ARTIST_SCULPT' if ok else 'WRONG KEY/STATE - press Restore'), icon='CHECKMARK' if ok else 'ERROR')
        box.label(text='Last validation: '+str(ctx.scene.get('sph_last_validation', 'not run')))
        L.operator('sph.restore_protection', icon='LOCKED')
        col = L.column(align=True); col.label(text='Isolate one region:')
        grid = col.grid_flow(columns=2, align=True)
        for r in REGIONS: grid.operator('sph.isolate_region', text=r.replace('_', ' ').title()).region = r
        col.operator('sph.restore_protection', text='Clear isolation (keep locks)')
        col = L.column(align=True); col.label(text='Compare:')
        row = col.row(align=True)
        for s, t in (('SCULPT', 'Sculpt'), ('REF_BR_NEUTRAL', 'Start'), ('REF_ACCEPTED_B2', 'B2'), ('SIDE', 'Side')): row.operator('sph.compare', text=t).state = s
        col = L.column(align=True); col.label(text='Overlays:')
        for c, t in (('SPH_GUIDES_REFERENCE_ONLY', 'Anatomy guides'), ('SPH_MEASURE_RINGS', 'Measurement rings'), ('SPH_SKELETON_REFERENCE', 'Bind skeleton')):
            col.operator('sph.toggle_collection', text=t).coll = c
        L.separator(); L.operator('sph.validate', icon='CHECKBOX_HLT')

CLASSES = (SPH_OT_restore, SPH_OT_isolate, SPH_OT_compare, SPH_OT_toggle, SPH_OT_validate, SPH_PT_panel)
def register():
    for c in CLASSES:
        try: bpy.utils.unregister_class(c)
        except Exception: pass
        bpy.utils.register_class(c)
if __name__ in ('__main__', 'SPH_TOOLS', 'SPH_TOOLS.py'): register()
