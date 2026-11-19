# sbs.py (Blender, background): two recordings side by side at the SOURCE frame rate (2026-11-19: was fixed 30 fps, which played 60 fps sources at half speed), left = before, right = after. Args: out.mp4 left.mp4 right.mp4
import bpy, sys
import traceback
try:
    a = sys.argv[sys.argv.index('--') + 1:]; out, l, r = a[0], a[1], a[2]
    sc = bpy.context.scene; sc.sequence_editor_create(); se = sc.sequence_editor; S = se.strips if hasattr(se, 'strips') else se.sequences
    s1 = S.new_movie(name='L', filepath=l, channel=1, frame_start=1); s2 = S.new_movie(name='R', filepath=r, channel=2, frame_start=1)
    W, H = s1.elements[0].orig_width, s1.elements[0].orig_height
    sc.render.resolution_x = 2 * W - (2 * W) % 4; sc.render.resolution_y = H - H % 4; sc.render.resolution_percentage = 50; fl = float(getattr(s1, 'fps', 30.0) or 30.0); fr = float(getattr(s2, 'fps', 30.0) or 30.0); assert abs(fl - fr) < 0.01, ('fps mismatch', fl, fr); sc.render.fps = int(round(fl)); sc.render.fps_base = 1.0
    sc.frame_start = 1; sc.frame_end = min(s1.frame_final_duration, s2.frame_final_duration)
    s1.transform.offset_x = -W / 2.0; s2.transform.offset_x = W / 2.0
    (setattr(sc.render.image_settings, 'media_type', 'VIDEO') if hasattr(sc.render.image_settings, 'media_type') else None)
    sc.render.image_settings.file_format = 'FFMPEG'; sc.render.ffmpeg.format = 'MPEG4'; sc.render.ffmpeg.codec = 'H264'; sc.render.ffmpeg.constant_rate_factor = 'MEDIUM'
    sc.render.filepath = out; bpy.ops.render.render(animation=True)
except Exception:
    open(sys.argv[sys.argv.index('--') + 1] + '.err.txt', 'w').write(traceback.format_exc())
