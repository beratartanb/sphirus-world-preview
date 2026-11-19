# vscale.py (Blender background): -- <out.mp4> <in.mp4> <percent>: re-encode at the SOURCE fps with a smaller frame size.
import bpy, sys
a = sys.argv[sys.argv.index('--') + 1:]; out, src, pc = a[0], a[1], int(a[2])
sc = bpy.context.scene; sc.sequence_editor_create(); S = sc.sequence_editor.strips if hasattr(sc.sequence_editor, 'strips') else sc.sequence_editor.sequences
m = S.new_movie(name='m', filepath=src, channel=1, frame_start=1)
sc.render.resolution_x = m.elements[0].orig_width; sc.render.resolution_y = m.elements[0].orig_height; sc.render.resolution_percentage = pc
sc.render.fps = int(round(m.fps)); sc.render.fps_base = 1.0; sc.frame_start = 1; sc.frame_end = m.frame_final_duration
(setattr(sc.render.image_settings, 'media_type', 'VIDEO') if hasattr(sc.render.image_settings, 'media_type') else None)
sc.render.image_settings.file_format = 'FFMPEG'; sc.render.ffmpeg.format = 'MPEG4'; sc.render.ffmpeg.codec = 'H264'; sc.render.ffmpeg.constant_rate_factor = 'MEDIUM'
sc.render.filepath = out; bpy.ops.render.render(animation=True)
