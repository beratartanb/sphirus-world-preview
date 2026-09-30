"""SPHIRUS soft-tissue pose correctives (PROCEDURAL; bind space, cm; UE axes x = character left, y = front, z = up).
One morph per RV driver curve (ue_rv_drivers.py), baked on the body and driven continuously by the PoseDriver RBF:
  RV_Bend30/60/90   breasts: gravity change relative to the chest wall  d = K*m*(0, sinA, 1-cosA) (root pinned by m -> 0),
                    slight lateral spread; abdomen: lower-abdomen compression bulge + soft navel-line crease; flank bulge
  RV_Arm090/120/150/180_s  breast on the raised side lifts / flattens, axillary tail stretches with the arm
  RV_ArmFwd_s       arms forward: slight medial compression of the breasts
  RV_Twist_l/_r     restrained soft-tissue lag opposite the chest rotation (breasts)
  RV_Hip075_s / RV_Hip110_s  glute projection reduces and spreads, fold opens, glute-ham compresses; deep flexion adds
                    hamstring / inner-thigh spread
usage: blender -b --factory-startup --python blender_softtissue_morphs.py -- <sculpt_package_v6.json.gz> <out.json>"""
import sys, json, gzip, math
import numpy as np
a = sys.argv[sys.argv.index('--')+1:]; PKG, OUT = a
P = json.loads(gzip.open(PKG, 'rb').read()); NB = P['NB']; X = np.asarray(P['br_neutral'])[:NB]; T = np.asarray(P['body']['triangles'])
W8 = P['weights']
def chain(pre): return np.asarray([sum(x for b, x in W8[v].items() if b.startswith(pre)) for v in range(NB)])
arm = chain(('upperarm', 'lowerarm', 'hand')); leg = chain(('thigh', 'calf', 'foot'))
# outward vertex normals (UE winding -> flip)
fnm = -np.cross(X[T[:, 1]]-X[T[:, 0]], X[T[:, 2]]-X[T[:, 0]]); N = np.zeros_like(X)
for k in range(3): np.add.at(N, T[:, k], fnm)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
AP = P['breast_apex']; APEX = {'l': np.asarray(AP['l']), 'r': np.asarray(AP['r'])}
def breast_mass(s):
    A = APEX[s]; C = A+np.array([0.0, -2.0, -1.5]); d = X-C
    g = np.exp(-((d[:, 0]/5.4)**2+(d[:, 1]/4.2)**2+(d[:, 2]/5.2)**2))
    root_y = A[1]-5.8; forward = sstep((X[:, 1]-root_y)/4.5)            # 0 at the chest wall (root stays attached), 1 at the mass
    side = sstep((np.sign(A[0])*X[:, 0]-0.8)/1.6)                        # zero across the sternal plane
    return g*forward*side*(arm < 0.25)
M = {s: breast_mass(s) for s in 'lr'}; MB = M['l']+M['r']
out = {'Body': {}, 'Head': {}}
def put(name, D):
    D = np.asarray(D); mag = np.linalg.norm(D, axis=1); ids = np.nonzero(mag > 0.002)[0]
    out['Body'][name] = {str(int(i)): [round(float(x), 5) for x in D[i]] for i in ids}
    print(name, 'verts', len(ids), 'max cm', round(float(mag.max()), 3))
# ---- forward bend
ab = np.exp(-((X[:, 0]/8.5)**2+((X[:, 2]-99.5)/6.0)**2))*sstep((N[:, 1]-0.2)/0.4)*(arm < 0.2)*(leg < 0.6)
crease = np.exp(-(X[:, 0]/9.0)**2)*np.exp(-((X[:, 2]-105.0)/1.0)**2)*sstep((N[:, 1]-0.3)/0.4)*(arm < 0.2)
flank = np.exp(-((np.abs(X[:, 0])-13.5)/2.2)**2)*np.exp(-((X[:, 2]-102.5)/4.0)**2)*(arm < 0.2)*(leg < 0.5)
flank_dir = np.stack([np.sign(X[:, 0]), np.zeros(NB), np.zeros(NB)], 1)
for A, nm in ((30, 'RV_Bend30'), (60, 'RV_Bend60'), (90, 'RV_Bend90')):
    r = math.radians(A); D = np.zeros_like(X)
    g = np.array([0.0, math.sin(r), 1.0-math.cos(r)]); KB = float(__import__('os').environ.get('SPH_ST_BEND_K', '1.15')); D += KB*MB[:, None]*g[None, :]
    D += 0.18*(KB/1.15)*math.sin(r)*MB[:, None]*np.stack([np.sign(X[:, 0]), np.zeros(NB), np.zeros(NB)], 1)
    D += math.sin(r)*(0.45*ab[:, None]*N+np.array([0, 0, -0.18])[None, :]*ab[:, None])
    D += -0.28*math.sin(r)**1.5*crease[:, None]*N
    D += 0.22*math.sin(r)*flank[:, None]*flank_dir
    put(nm, D)
# ---- arms raised / forward (per side)
for s in 'lr':
    sg = 1 if s == 'l' else -1; m = M[s]
    ax = np.exp(-((sg*X[:, 0]-14.5)/2.2)**2-((X[:, 2]-129.0)/3.0)**2)*sstep((N[:, 1]+0.2)/0.6)*(arm < 0.3)   # axillary tail
    for e, k in ((90, 0.2), (120, 0.4), (150, 0.8), (180, 1.0)):
        D = k*(m[:, None]*np.array([0.08*sg, -0.28, 0.95])[None, :]+0.35*ax[:, None]*np.array([0.35*sg, -0.1, 0.6])[None, :])
        put(f'RV_Arm{e:03d}_{s}', D)
    put(f'RV_ArmFwd_{s}', 0.45*MB[:, None]*np.stack([-np.sign(X[:, 0])*0.7, np.full(NB, 0.12), np.zeros(NB)], 1)*(1 if True else 0))
# ---- twist: lag opposite the chest rotation about the vertical axis
yc = 4.0
for s, sgn in (('l', 1.0), ('r', -1.0)):
    tan = np.stack([-(X[:, 1]-yc), X[:, 0], np.zeros(NB)], 1); tan /= np.maximum(np.linalg.norm(tan, axis=1), 1e-6)[:, None]
    put(f'RV_Twist_{s}', -sgn*0.45*MB[:, None]*tan)
# ---- hip flexion / deep squat (per side)
for s in 'lr':
    sg = 1 if s == 'l' else -1; back = sstep((-N[:, 1]-0.2)/0.4)
    gl = np.exp(-(((X[:, 0]-sg*8.3)/5.6)**2+((X[:, 2]-83.5)/6.2)**2))*back*(sg*X[:, 0] > -1.0)
    fold = np.exp(-(((X[:, 0]-sg*7.0)/5.0)**2+((X[:, 2]-77.0)/1.8)**2))*back
    ham = np.exp(-(((X[:, 0]-sg*9.5)/4.5)**2+((X[:, 2]-67.0)/5.5)**2))*back*(leg > 0.5)
    inner = np.exp(-(((X[:, 0]-sg*4.0)/2.5)**2+((X[:, 2]-70.0)/6.0)**2))*sstep((-sg*N[:, 0]-0.2)/0.5)*(leg > 0.5)
    lat = np.stack([np.full(NB, float(sg)), np.zeros(NB), np.zeros(NB)], 1)
    for k, nm in ((1.0, f'RV_Hip075_{s}'), (1.7, f'RV_Hip110_{s}')):
        D = k*(-0.55*gl[:, None]*N+0.28*gl[:, None]*lat+0.45*fold[:, None]*N)
        if k > 1.2: D += 0.35*ham[:, None]*N+0.3*inner[:, None]*(-lat*1.0)*(-1)
        put(nm, D)
json.dump(out, open(OUT, 'w')); print('SOFT_OK', len(out['Body']))
