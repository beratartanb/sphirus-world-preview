import bpy, sys, os
a = sys.argv[sys.argv.index('--') + 1:]
out = a[0]
sc = bpy.context.scene
se = sc.sequence_editor_create()
for spec in a[1:]:
    path, times = spec.split('|')
    name = os.path.splitext(os.path.basename(path))[0]
    strips = se.strips if hasattr(se, 'strips') else se.sequences
    for s in list(strips):
        strips.remove(s)
    st = strips.new_movie('m', path, 1, 1)
    fps = st.fps if hasattr(st, 'fps') else 24.0
    el = st.elements[0]
    sc.render.resolution_x = el.orig_width // 2
    sc.render.resolution_y = el.orig_height // 2
    sc.render.resolution_percentage = 100
    st.transform.scale_x = 0.5
    st.transform.scale_y = 0.5
    sc.render.image_settings.file_format = 'JPEG'
    sc.render.image_settings.quality = 85
    for t in times.split(','):
        f = max(1, min(st.frame_final_duration, int(float(t) * fps) + 1))
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out, '%s_%s.jpg' % (name, t.replace('.', '_')))
        bpy.ops.render.render(write_still=True)
        print('FR', name, t, f, fps, st.frame_final_duration)
