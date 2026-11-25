"""gen_handmade3.py (Blender 5.3, -b --python): round 3 of the house's handmade props - the mask maker's WORKING kit that the workshop lacked:
a drying rack for masks, a clay face form on its board, a paint board with mixed earth pigments, a jar of brushes, a glue pot with its brush,
a heap of torn linen strips. Same helpers, units, slot names and export as Tools/Interior_20261111/gen_handmade.py (its first 72 lines are reused).
Output: SourceAssets/Handmade_20261125/<name>.fbx + preview PNGs + handmade.json"""
import os
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Interior_20261111', 'gen_handmade.py')
L = open(SRC, encoding='utf8').read().split('\n')
exec('\n'.join(L[5:72]))                                   # imports + helpers (mat, new_obj, act, finish, cyl, box, lathe)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'SourceAssets', 'Handmade_20261125')
os.makedirs(os.path.join(OUT, 'preview'), exist_ok=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
INFO.clear(); rr = random.Random(1125)
OCHRE = (.56, .36, .10, 1); OXIDE = (.38, .12, .08, 1); BONE = (.80, .76, .66, 1); BLACK = (.06, .055, .05, 1); VERD = (.20, .34, .28, 1); WET = (.45, .40, .33, 1)

# ---------------------------------------------------------------- drying rack: two A-frames, three rails, pegs; masks hang on the pegs (placed in the level)
bm = bmesh.new()
for sx in (-41, 41):
    cyl(bm, 1.7, 1.5, (sx, -15, 0), (sx, -1.5, 118), 8, mi=0); cyl(bm, 1.7, 1.5, (sx, 15, 0), (sx, 1.5, 118), 8, mi=0); cyl(bm, 1.2, 1.2, (sx, -9.5, 40), (sx, 9.5, 40), 6, mi=0)
for z, y in ((112, 0.0), (78, -5.2), (46, -9.2)):
    box(bm, (0, y, z), (88, 2.2, 4.2), 0)
    for i in range(4):
        x = -30 + 20 * i; cyl(bm, .7, .55, (x, y - 1.0, z + .6), (x, y - 5.2, z + 2.4), 6, mi=0)
ob = new_obj('SM_HM_MaskDryRack', bm, ['Oak']); finish(ob, smooth=False)

# ---------------------------------------------------------------- clay face form on an oak board (the positive the masks are laid over)
bm = bmesh.new(); box(bm, (0, 0, 1.0), (30, 36, 2.0), 0)
seg = 22; rings = []
for k in range(9):
    t = k / 8.0; ph = t * math.pi / 2; rw = 9.6 * math.cos(ph) ** .8; rl = 12.6 * math.cos(ph) ** .8; z = 2.0 + 8.4 * math.sin(ph)
    ring = []
    for i in range(seg):
        a = 2 * math.pi * i / seg; x = rw * math.cos(a); y = rl * math.sin(a) * (1.0 if math.sin(a) > 0 else .82)        # narrower at the chin end
        dz = 2.6 * math.exp(-((x / 2.0) ** 2 + ((y + 1.0) / 4.6) ** 2)) * (1 - t * .2)                                     # nose ridge
        dz -= 1.1 * (math.exp(-(((x - 4.2) / 2.0) ** 2 + ((y - 3.4) / 1.6) ** 2)) + math.exp(-(((x + 4.2) / 2.0) ** 2 + ((y - 3.4) / 1.6) ** 2)))   # eye hollows
        ring.append(bm.verts.new((x, y, z + dz * (0.35 + 0.65 * t))))
    rings.append(ring)
for k in range(8):
    for i in range(seg):
        f = bm.faces.new((rings[k][i], rings[k][(i + 1) % seg], rings[k + 1][(i + 1) % seg], rings[k + 1][i])); f.material_index = 1
f = bm.faces.new(rings[-1]); f.material_index = 1
ob = new_obj('SM_HM_MaskForm', bm, ['Oak', 'Clay']); finish(ob)

# ---------------------------------------------------------------- paint board: oak offcut, five mixed pigments (vertex colour), a palette knife
bm = bmesh.new(); box(bm, (0, 0, .9), (34, 22, 1.8), 0)
blobs = [(-11, 4, 3.6, OCHRE), (-3, 6, 3.0, OXIDE), (5, 5, 2.6, BONE), (11.5, 3, 2.2, BLACK), (-7, -4.5, 2.4, VERD), (3, -3.5, 4.4, (.47, .24, .10, 1))]
BL = []
for x, y, r, c in blobs:
    v0 = len(bm.verts); lathe(bm, [(r, 1.82), (r * .82, 2.05), (r * .45, 2.22), (0.05, 2.18)], 10, 1)
    bm.verts.ensure_lookup_table()
    for v in bm.verts[v0:]:
        a = math.atan2(v.co.y, v.co.x); k = 1 + .18 * math.sin(3 * a + x) + .1 * math.sin(5 * a); v.co = Vector((x + v.co.x * k, y + v.co.y * k * .9, v.co.z))
    BL.append((x, y, r * 1.35, c))
box(bm, (12, -6.5, 2.1), (9.5, 1.5, .25), 2, Matrix.Rotation(.5, 4, 'Z')); cyl(bm, .55, .5, (16.2, -4.3, 2.1), (22.5, -0.9, 2.3), 6, mi=0)
def pb_col(p, v):
    for x, y, r, c in BL:
        if (v.co.x - x) ** 2 + (v.co.y - y) ** 2 < r * r and v.co.z > 1.81: return c
    return (1, 1, 1, 1)
ob = new_obj('SM_HM_PaintBoard', bm, ['Oak', 'Tint', 'Iron']); finish(ob, vcol=pb_col)

# ---------------------------------------------------------------- brush jar: clay jar, seven brushes and a stirring stick
bm = bmesh.new(); lathe(bm, [(0.05, .3), (4.6, .3), (5.4, 1.2), (6.0, 6.5), (5.6, 11.5), (5.0, 13.0), (5.3, 13.6), (4.7, 13.6), (4.4, 12.6), (5.0, 11.0), (5.2, 6.5), (4.4, 1.8), (0.05, 1.8)], 16, 0)
TIPS = [OCHRE, OXIDE, BONE, BLACK, VERD, OXIDE, WET]
for i in range(7):
    a = 2 * math.pi * i / 7 + rr.uniform(-.25, .25); r0 = rr.uniform(.6, 2.6); ln = rr.uniform(15, 22); lean = rr.uniform(2.2, 5.0)
    b0 = Vector((math.cos(a) * r0, math.sin(a) * r0, 2.0)); b1 = Vector((math.cos(a) * (r0 + lean), math.sin(a) * (r0 + lean), 2.0 + ln)); d = (b1 - b0).normalized()
    cyl(bm, .36, .42, b0, b1, 6, mi=1); cyl(bm, .46, .46, b1, b1 + d * 1.6, 6, mi=2); cyl(bm, .5, .12, b1 + d * 1.6, b1 + d * (4.4 + rr.uniform(0, 1.2)), 6, mi=3)
tipz = []
def bj_col(p, v):
    if p.material_index != 3: return (1, 1, 1, 1)
    a = math.atan2(v.co.y, v.co.x) % (2 * math.pi); return TIPS[int(a / (2 * math.pi) * 7 + .5) % 7]
ob = new_obj('SM_HM_BrushJar', bm, ['Clay', 'Oak', 'Iron', 'Tint']); finish(ob, vcol=bj_col)

# ---------------------------------------------------------------- glue pot: small iron pot on three feet, skin of hide glue, a flat brush across the rim
bm = bmesh.new(); lathe(bm, [(0.05, 1.6), (5.0, 1.6), (6.6, 3.0), (7.2, 6.5), (6.6, 9.6), (6.9, 10.1), (6.2, 10.1), (5.9, 9.2), (6.4, 6.5), (5.8, 3.4), (0.05, 2.6)], 16, 0)
lathe(bm, [(0.05, 8.3), (5.95, 8.3), (6.1, 8.5)], 16, 1)
for k in range(3):
    a = 2 * math.pi * k / 3; cyl(bm, .8, .5, (math.cos(a) * 4.4, math.sin(a) * 4.4, 2.2), (math.cos(a) * 5.6, math.sin(a) * 5.6, 0), 6, mi=0)
cyl(bm, .5, .6, (-9.5, 1.5, 10.6), (2.0, -.6, 10.4), 6, mi=2); box(bm, (4.2, -1.0, 10.3), (4.6, 2.6, .7), 1, Matrix.Rotation(-.18, 4, 'Z'))
ob = new_obj('SM_HM_GluePot', bm, ['Iron', 'Tint', 'Oak']); finish(ob, vcol=lambda p, v: (.50, .36, .16, 1) if p.material_index == 1 else (1, 1, 1, 1))

# ---------------------------------------------------------------- linen strips: a loose heap of torn strips, some hanging over the edge
bm = bmesh.new()
for i in range(16):
    a = rr.uniform(0, math.pi); cx = rr.uniform(-7, 7); cy = rr.uniform(-5, 5); ln = rr.uniform(14, 26); w = rr.uniform(1.6, 2.6); z0 = .25 + i * .22; n = 7; d = Vector((math.cos(a), math.sin(a), 0)); s = Vector((-d.y, d.x, 0)); prev = None
    for j in range(n + 1):
        t = j / n - .5; p = Vector((cx, cy, z0)) + d * (t * ln) + s * (1.4 * math.sin(t * 5 + i)); p.z = z0 + .9 * math.sin(j * 1.9 + i) ** 2 - (4.5 * max(0, abs(t) - .38) if i % 4 == 0 else 0)
        pa = bm.verts.new(p + s * w / 2); pb = bm.verts.new(p - s * w / 2)
        if prev: bm.faces.new((prev[0], prev[1], pb, pa))
        prev = (pa, pb)
ob = new_obj('SM_HM_LinenStrips', bm, ['Linen']); finish(ob)
act(ob); mo = ob.modifiers.new('s', 'SOLIDIFY'); mo.thickness = .12; bpy.ops.object.modifier_apply(modifier='s')
INFO[ob.name]['tris'] = sum(len(p.vertices) - 2 for p in ob.data.polygons)

exec('\n'.join(L[254:]))                                   # previews + FBX + handmade.json (uses OUT / INFO)
