# mkvid.py (Blender, background): PNG window shots -> MP4 (H.264, 30 fps), cropped to the game viewport.
# Args: out.mp4 fps x0 y0 x1 y1 dir_with_pngs [label]
import bpy, sys, os
a=sys.argv[sys.argv.index('--')+1:]; out=a[0]; fps=int(a[1]); x0,y0,x1,y1=map(int,a[2:6]); d=a[6]
files=sorted(f for f in os.listdir(d) if f.lower().endswith('.png'))
img=bpy.data.images.load(os.path.join(d,files[0])); W,H=img.size
sc=bpy.context.scene; sc.render.resolution_x=x1-x0; sc.render.resolution_y=y1-y0; sc.render.resolution_percentage=100
sc.render.fps=fps; sc.frame_start=1; sc.frame_end=len(files)
(setattr(sc.render.image_settings,'media_type','VIDEO') if hasattr(sc.render.image_settings,'media_type') else None); sc.render.image_settings.file_format='FFMPEG'; sc.render.ffmpeg.format='MPEG4'; sc.render.ffmpeg.codec='H264'; sc.render.ffmpeg.constant_rate_factor='MEDIUM'; sc.render.ffmpeg.gopsize=15
sc.render.filepath=out
if not sc.sequence_editor: sc.sequence_editor_create()
se=sc.sequence_editor
strip=(se.strips if hasattr(se,'strips') else se.sequences).new_image(name='shots',filepath=os.path.join(d,files[0]),channel=1,frame_start=1)
for f in files[1:]: strip.elements.append(f)
strip.crop.min_x=x0; strip.crop.max_x=W-x1; strip.crop.min_y=H-y1; strip.crop.max_y=y0
bpy.ops.render.render(animation=True)
print('VIDEO',out,len(files),'frames',(x1-x0),'x',(y1-y0))
