"""Workbench previews of the delivered sculpt file from the 5 sculpt cameras (plain + guides), no save.
blender -b <file.blend> --python render_previews.py -- <out_dir>"""
import bpy, sys, os
out = sys.argv[sys.argv.index('--')+1]; os.makedirs(out, exist_ok=True)
sc = bpy.context.scene; ob = bpy.data.objects['SPH_BR_ArtistSculpt']
if ob.mode != 'OBJECT': bpy.context.view_layer.objects.active = ob; bpy.ops.object.mode_set(mode='OBJECT')
sc.render.resolution_x = 720; sc.render.resolution_y = 1280; sc.render.image_settings.file_format = 'PNG'
sc.render.film_transparent = False; sc.display.shading.background_type = 'VIEWPORT' if hasattr(sc.display.shading, 'background_type') else None
G = bpy.data.collections['SPH_GUIDES_REFERENCE_ONLY']
for guides in (False, True):
    G.hide_render = not guides
    for cam in sorted((o for o in bpy.data.objects if o.type == 'CAMERA'), key=lambda o: o.name):
        sc.camera = cam; sc.render.filepath = os.path.join(out, f"{cam.name}{'_GUIDES' if guides else ''}.png")
        bpy.ops.render.render(write_still=True); print('rendered', sc.render.filepath)
