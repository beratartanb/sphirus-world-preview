# transcode.py (Blender, background): re-encode an mp4 at a lower quality factor so it fits the GitHub blob API.
# Args: in.mp4 out.mp4 [crf preset, default LOW]. Same resolution, frame rate and frame count; picture quality drops, timing does not.
import bpy, sys
a = sys.argv[sys.argv.index('--') + 1:]; src, out = a[0], a[1]; crf = a[2] if len(a) > 2 else 'LOW'
sc = bpy.context.scene; se = sc.sequence_editor_create()
strips = se.strips if hasattr(se, 'strips') else se.sequences
st = strips.new_movie('m', src, 1, 1); el = st.elements[0]
sc.render.resolution_x = el.orig_width; sc.render.resolution_y = el.orig_height; sc.render.resolution_percentage = 100
fps = round(st.fps) if hasattr(st, 'fps') else 30
sc.render.fps = fps; sc.frame_start = 1; sc.frame_end = st.frame_final_duration
(setattr(sc.render.image_settings, 'media_type', 'VIDEO') if hasattr(sc.render.image_settings, 'media_type') else None)
sc.render.image_settings.file_format = 'FFMPEG'; sc.render.ffmpeg.format = 'MPEG4'; sc.render.ffmpeg.codec = 'H264'
sc.render.ffmpeg.constant_rate_factor = crf; sc.render.ffmpeg.gopsize = 15; sc.render.filepath = out
bpy.ops.render.render(animation=True)
