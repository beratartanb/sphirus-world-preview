# sheet2.py <dir> <out prefix> [cols] [cell w] [names...]: labelled contact sheets (cols x 2 per sheet) from PNG stills.
import sys, os, glob; sys.path.insert(0,'Tools/R2G_20261123/deps')
from PIL import Image, ImageDraw
d,out=sys.argv[1],sys.argv[2]; cols=int(sys.argv[3]) if len(sys.argv)>3 else 2; cw=int(sys.argv[4]) if len(sys.argv)>4 else 800
names=sys.argv[5:] or sorted(os.path.basename(p)[:-4] for p in glob.glob(d+'/*.png'))
ch=cw*9//16; per=cols*2
for i in range(0,len(names),per):
    S=Image.new('RGB',(cw*cols,ch*2),(0,0,0)); dr=ImageDraw.Draw(S)
    for j,n in enumerate(names[i:i+per]):
        p=d+'/'+n+'.png'
        if not os.path.exists(p): continue
        im=Image.open(p).convert('RGB').resize((cw,ch)); x,y=(j%cols)*cw,(j//cols)*ch; S.paste(im,(x,y))
        dr.rectangle([x,y,x+9*len(n)+8,y+16],fill=(0,0,0)); dr.text((x+4,y+2),n,fill=(255,255,0))
    S.save('%s_%d.jpg'%(out,i//per),quality=88); print('%s_%d.jpg'%(out,i//per))
