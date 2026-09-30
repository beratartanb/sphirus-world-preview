"""Map a reference image's frame (solved weak-perspective camera in recon.json) into a UE capture camera -> crop rectangle
(fractions) that shows the same world extent as the reference image. usage: python id_ref_frame.py <recon.json> <view> <W> <H> '<cam json>' <fov>"""
import json, sys, math
rc, vk, W, H, cam, fov = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), json.loads(sys.argv[5]), float(sys.argv[6])
c = json.load(open(rc))['cams'][vk]; R, s, t = c['R'], c['s'], c['t']
dot = lambda a, b: sum(x*y for x, y in zip(a, b)); depth = dot(R[2], [0, 10, 160])
def world(px, py):
    u, v = (px-t[0])/s, (py-t[1])/s; return [R[0][k]*u+R[1][k]*v+R[2][k]*depth for k in range(3)]
x, y, z, yaw, pit = cam; cy, sy, cp, sp = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pit)), math.sin(math.radians(pit))
f = (cy*cp, sy*cp, sp); r = (-sy, cy, 0.0); u = (-cy*sp, -sy*sp, cp); tt = math.tan(math.radians(fov)/2)
def proj(p):
    v = [p[0]-x, p[1]-y, p[2]-z]; d = dot(v, f); return 0.5+0.5*dot(v, r)/d/tt, 0.5-0.5*dot(v, u)/d/tt
(x0, y0), (x1, y1) = proj(world(0, 0)), proj(world(W, H)); print('%.4f|%.4f|%.4f|%.4f' % (x0, y0, x1, y1))
