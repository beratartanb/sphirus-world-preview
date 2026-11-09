# frame.py (Blender 5.2, background): extract single frames from an mp4 as PNG.
#   blender --background --factory-startup --python frame.py -- <in.mp4> <out_prefix> <frame> [<frame> ...]
# Writes <out_prefix>_<frame>.png for each 1-based frame index via the video sequencer.
import bpy,sys
a=sys.argv[sys.argv.index('--')+1:]; src=a[0]; pre=a[1]; frames=[int(x) for x in a[2:]]
sc=bpy.context.scene
if not sc.sequence_editor: sc.sequence_editor_create()
st=sc.sequence_editor.strips.new_movie('v',src,1,1)
sc.render.resolution_x=st.elements[0].orig_width; sc.render.resolution_y=st.elements[0].orig_height; sc.render.resolution_percentage=100
sc.render.image_settings.media_type='IMAGE'; sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGB'
for f in frames:
    sc.frame_set(f); sc.render.filepath='%s_%d.png'%(pre,f); bpy.ops.render.render(write_still=True); print('FRAME',sc.render.filepath)
