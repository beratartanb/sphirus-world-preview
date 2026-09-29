"""Far-LOD helper equivalence: body LOD2-3 / face LOD4-7 carry no effective upperarm_out skinning, so the SHCB helper
shift cannot reach them through the rig. Add the helper's LOD0 surface effect (w_out(v) * shift, bind space via
A_v^-1) to the SHCB morph deltas, then project onto those LODs only (same closest-point transfer)."""
import sys, json, math, gzip
sys.path.insert(0, '.')
from shc_combo import *
from shc_design import affines, lin_A, solve3
D = json.load(open(C.parent/'CharacterFinal_20260929'/'morph_data_br_shcb.json'))
SHIFT = {'150': 2.0, '165': 3.0, '180': 3.5}
POSE = {'150': 'elev_150', '165': 'elev_165', '180': 'elev_180'}
out = {'Body': {}, 'Head': {}}
for side in 'lr':
    sg = 1 if side == 'l' else -1
    for k in ['150', '165', '180']:
        af = affines(POSE[k]); name = f'SHC_{k}_{side}'
        for part in ['Body', 'Head']:
            m = {int(v): d for v, d in D[part][name].items()}; P = PARTS[part]
            for vi, w in enumerate(P['w']):
                wo = w.get(f'upperarm_out_{side}', 0.0)
                if wo <= 0: continue
                ci = vi if part == 'Body' else cid('Head', vi)
                bd = solve3(lin_A(ci, af), [sg*SHIFT[k]*wo, 0.0, 0.0])
                d = m.get(vi, [0.0, 0.0, 0.0]); m[vi] = [d[i]+bd[i] for i in range(3)]
            out[part][name] = {str(v): d for v, d in m.items()}
        print(side, k, 'body verts', len(out['Body'][name]), 'head verts', len(out['Head'][name]), flush=True)
(C.parent/'CharacterFinal_20260929'/'morph_data_br_hfx.json').write_text(json.dumps(out))
