# sheet.py <out.jpg> <cols> <cellw> <img...> : labelled contact sheet (inspection aid only, letterboxed, no stretching)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deps'))
from PIL import Image, ImageDraw
out, cols, cw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); fs = sys.argv[4:]
ims = [Image.open(f).convert('RGB') for f in fs]; ch = max(int(cw * i.height / i.width) for i in ims) + 18
rows = (len(ims) + cols - 1) // cols; S = Image.new('RGB', (cols * cw, rows * ch), (20, 20, 20)); d = ImageDraw.Draw(S)
for n, (f, i) in enumerate(zip(fs, ims)):
    h = int(cw * i.height / i.width); x, y = (n % cols) * cw, (n // cols) * ch
    S.paste(i.resize((cw, h), Image.LANCZOS), (x, y + 18)); d.text((x + 4, y + 3), os.path.splitext(os.path.basename(f))[0], fill=(255, 255, 255))
S.save(out, quality=88); print('SHEET', out, S.size)
