# draw_plan.py: draws trace_plan.json as plan images (north/forest up, x right). Architecture hits white, other actors coloured by folder group.
import sys, json, collections; sys.path.insert(0,'Tools/R2G_20261123/deps')
from PIL import Image, ImageDraw
T=json.load(open('Saved/UE59Work/r2g2/trace_plan.json')); A=json.load(open('Saved/UE59Work/r2g2/actors.json',encoding='utf8'))['actors']
fold={a['label']:(a.get('folder') or 'None') for a in A if 'label' in a}
cls={a['label']:a.get('cls') for a in A if 'label' in a}
S=1.0; X0,Y0=-120,-260; Wd,Hd=1760,1820
def col(lb):
    f=fold.get(lb,'?')
    if f.startswith('House/Architecture'): return (235,235,235)
    if 'Door' in f or 'Door' in (cls.get(lb) or ''): return (255,60,60)
    if f.startswith('GameplaySF'): return (255,210,0)
    if f.startswith('LIVED'): return (90,200,120)
    if f.startswith('House/'): return (90,160,255)
    if f.startswith('EXTERIOR') or f.startswith('PFR'): return (200,120,60)
    return (190,90,200)
for z,H in T.items():
    im=Image.new('RGB',(Wd,Hd),(18,18,22)); d=ImageDraw.Draw(im)
    for gx in range(0,1601,100): d.line([(gx-X0,0),(gx-X0,Hd)],fill=(40,40,48)); d.text((gx-X0+2,2),str(gx),fill=(120,120,130))
    for gy in range(-200,1501,100): d.line([(0,gy-Y0),(Wd,gy-Y0)],fill=(40,40,48)); d.text((2,gy-Y0+2),str(gy),fill=(120,120,130))
    for x,y,lb in H:
        c=col(lb); px,py=x-X0,y-Y0; d.rectangle([px-1,py-1,px+1,py+1],fill=c)
    im.save('Saved/UE59Work/r2g2/plan/trace_z%s.png'%z)
    cnt=collections.Counter(lb for _,_,lb in H if not fold.get(lb,'').startswith('House/Architecture'))
    print(z, len(H), cnt.most_common(12))
