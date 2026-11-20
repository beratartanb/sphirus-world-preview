# recode.py (Blender, background): movie -> shorter / smaller H.264. Args: in.mp4 out.mp4 first_frame last_frame percent
import bpy, sys
import traceback
try:
    a=sys.argv[sys.argv.index('--')+1:]; src=a[0]; out=a[1]; f0=int(a[2]); f1=int(a[3]); pc=int(a[4])
    sc=bpy.context.scene
    if not sc.sequence_editor: sc.sequence_editor_create()
    se=sc.sequence_editor; strips=(se.strips if hasattr(se,'strips') else se.sequences)
    st=strips.new_movie(name='m',filepath=src,channel=1,frame_start=1)
    el=st.elements[0]; sc.render.resolution_x=2*int(el.orig_width*pc/200); sc.render.resolution_y=2*int(el.orig_height*pc/200); sc.render.resolution_percentage=100; st.transform.scale_x=pc/100.0; st.transform.scale_y=pc/100.0
    sc.render.fps=30; sc.frame_start=max(1,f0); sc.frame_end=min(f1,st.frame_final_duration)
    (setattr(sc.render.image_settings,'media_type','VIDEO') if hasattr(sc.render.image_settings,'media_type') else None)
    sc.render.image_settings.file_format='FFMPEG'; sc.render.ffmpeg.format='MPEG4'; sc.render.ffmpeg.codec='H264'; sc.render.ffmpeg.constant_rate_factor='MEDIUM'
    sc.render.filepath=out; bpy.ops.render.render(animation=True); print('RECODE',out)
except Exception:
    open(sys.argv[sys.argv.index('--')+2]+'.err.txt','w').write(traceback.format_exc())
