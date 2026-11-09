# sharp.py (Blender): Laplacian sharpness of regions (centre and four corners of the game viewport) for each image given.
import bpy, sys, numpy as np
a=sys.argv[sys.argv.index('--')+1:]
X0,Y0,X1,Y1=5,168,1515,1090
def lapvar(g):
    l=-4*g[1:-1,1:-1]+g[:-2,1:-1]+g[2:,1:-1]+g[1:-1,:-2]+g[1:-1,2:]; return float((l*l).mean())
for f in a:
    im=bpy.data.images.load(f); w,h=im.size; px=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4); px=px[::-1]
    g=px[...,0]*.3+px[...,1]*.59+px[...,2]*.11
    cx,cy=(X0+X1)//2,(Y0+Y1)//2; R=130
    regs={'center':g[cy-R:cy+R,cx-R:cx+R],'tl':g[Y0+40:Y0+40+2*R,X0+40:X0+40+2*R],'tr':g[Y0+40:Y0+40+2*R,X1-40-2*R:X1-40],'bl':g[Y1-40-2*R:Y1-40,X0+40:X0+40+2*R],'br':g[Y1-40-2*R:Y1-40,X1-40-2*R:X1-40]}
    r={k:round(lapvar(v)*1e4,2) for k,v in regs.items()}; r['mean']=round(float(g[Y0:Y1,X0:X1].mean()),3) if h>=Y1 and w>=X1 else round(float(g.mean()),3)
    print('SHARP',f.split('/')[-1],r)
