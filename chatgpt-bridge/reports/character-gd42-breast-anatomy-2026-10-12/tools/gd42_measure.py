"""GD42: planar-section widths / depths of the current neutral (LK) and a candidate morph at anatomical heights, with the reference values
from the shape plan (reference silhouette, landmark-aligned, in our cm). usage: blender -b --python gd42_measure.py -- <pkg> <lk> <plan.json> <morph.json> <label>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from gd42_lib import Body
a = sys.argv[sys.argv.index('--')+1:]; PKG, LKJ, PLAN, MJ, LAB = a[:5]; pl = json.load(open(PLAN)); zg = np.asarray(pl['z'])
B0 = Body(PKG, LKJ); B1 = Body(PKG, LKJ, extra=MJ); z_crotch = pl['landmarks_our_z']['crotch']
def meas(B, zz):
    noarm = B.arm < 0.3; x = B.XR[:, 0]
    if zz >= z_crotch: f, b, xm, xn = B.extents(zz, noarm); return xm-xn, f-b
    f, b, xm, xn = B.extents(zz, noarm & (x > 0)); return xm-xn, f-b
def ref(zz): i = int(np.argmin(np.abs(zg-zz))); return pl['W_ref_cm'][i], pl['D_ref_cm'][i]
print('MEASURE %-14s %5s | %6s %6s %6s | %6s %6s %6s' % ('region', 'z', 'W_lk', 'W_'+LAB, 'W_ref', 'D_lk', 'D_'+LAB, 'D_ref'))
for nm, zz in (('ribcage', 120), ('waist', 112), ('navel', 104), ('pelvis', 96), ('hip', 90), ('upper thigh', 74), ('mid thigh', 64), ('low thigh', 56), ('knee', 46), ('calf', 36), ('low calf', 24), ('ankle', 14)):
    w0, d0 = meas(B0, zz); w1, d1 = meas(B1, zz); wr, dr = ref(zz)
    print('MEASURE %-14s %5.0f | %6.1f %6.1f %6.1f | %6.1f %6.1f %6.1f' % (nm, zz, w0, w1, wr, d0, d1, dr))
