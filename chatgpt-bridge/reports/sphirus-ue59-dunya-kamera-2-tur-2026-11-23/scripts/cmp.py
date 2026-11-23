# cmp.py <out prefix> <rows per sheet> <tag1,tag2,...> <view1,view2,...>: grid, columns = tags, rows = views. A tag may be "a|b" (fallback folder).
import sys, os; sys.path.insert(0,'Tools/R2G_20261123/deps')
from PIL import Image, ImageDraw
out=sys.argv[1]; rp=int(sys.argv[2]); tags=sys.argv[3].split(','); views=sys.argv[4].split(',')
B='Saved/UE59Work/r2g/shots/'; cw=1600//len(tags); ch=cw*9//16
def find(t,v):
    for f in t.split('|'):
        p=B+f+'/'+v+'.png'
        if os.path.exists(p): return p
for s in range(0,len(views),rp):
    vs=views[s:s+rp]; S=Image.new('RGB',(cw*len(tags),ch*len(vs))); d=ImageDraw.Draw(S)
    for r,v in enumerate(vs):
        for c,t in enumerate(tags):
            p=find(t,v)
            if not p: continue
            S.paste(Image.open(p).convert('RGB').resize((cw,ch)),(c*cw,r*ch)); lb=t.split('|')[0]+' '+v
            d.rectangle([c*cw,r*ch,c*cw+7*len(lb)+8,r*ch+14],fill=(0,0,0)); d.text((c*cw+4,r*ch+1),lb,fill=(255,255,0))
    S.save('%s_%d.jpg'%(out,s//rp),quality=87); print('%s_%d.jpg'%(out,s//rp))
