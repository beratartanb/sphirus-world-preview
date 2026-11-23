# pairs.py <out.jpg> <labelA> <dirA> <labelB> <dirB> <frame,frame,...> [cellw]: before/after rows from two recordings of the SAME input plan
# (frames are editor-window screenshots; cropped to the PIE viewport 5,168..1515,1090). Inspection aid; stills are not motion evidence.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deps'))
from PIL import Image, ImageDraw
out, la, da, lb, db, fr = sys.argv[1:7]; cw = int(sys.argv[7]) if len(sys.argv) > 7 else 640; fr = [int(x) for x in fr.split(',')]
BOX = (5, 168, 1515, 1090); ch = int(cw * (BOX[3] - BOX[1]) / (BOX[2] - BOX[0])) + 18
S = Image.new('RGB', (2 * cw, len(fr) * ch), (20, 20, 20)); d = ImageDraw.Draw(S)
for r, f in enumerate(fr):
    for c, (lab, dd) in enumerate(((la, da), (lb, db))):
        p = os.path.join(dd, 'ScreenShot%05d.png' % f)
        if not os.path.isfile(p): d.text((c * cw + 4, r * ch + 3), '%s frame %d missing' % (lab, f), fill=(255, 120, 120)); continue
        i = Image.open(p).convert('RGB').crop(BOX).resize((cw, ch - 18), Image.LANCZOS); S.paste(i, (c * cw, r * ch + 18))
        d.text((c * cw + 4, r * ch + 3), '%s  t=%.0f s (frame %d)' % (lab, f / 30.0, f), fill=(255, 255, 255))
S.save(out, quality=88); print('PAIRS', out, S.size)
