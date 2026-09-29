"""SHCB rebase onto BR_Neutral v5: base(pose) = native posed + A_v(pose)*BR_bind_delta + upperarm_out helper shift.
SHC (crease-targeted Taubin) + a2 anatomy (outward normals, fixed) recomputed on that base; output morph_data_br_shcb.json."""
import sys, json
sys.path.insert(0, '.')
import shcb_design as SD
from shc_combo import *
from shc_design import affines, lin_A, mulA
BR = json.loads((C.parent/'CharacterFinal_20260929'/'br_morph_v6.json').read_text())
ND = {}
for v, d in BR['Body']['BR_Neutral'].items(): ND[int(v)] = d
for v, d in BR['Head']['BR_Neutral'].items():
    ci = cid('Head', int(v))
    if ci not in ND: ND[ci] = d
_orig = SD.base_hfix
def base_br(pose, k):
    P = _orig(pose, k); af = affines(pose)
    for v, d in ND.items():
        pd = mulA(lin_A(v, af), d); P[v] = [P[v][i]+pd[i] for i in range(3)]
    return P
SD.base_hfix = base_br
_S = SD.S
class _P:  # redirect output file names
    pass
import builtins
orig_write = Path.write_text
def main():
    SD.main()
    import shutil
    shutil.copy(S/'morph_data_shcb.json', C.parent/'CharacterFinal_20260929'/'morph_data_br_shcb.json')
    shutil.copy(S/'design_shcb.json', C.parent/'CharacterFinal_20260929'/'design_br_shcb.json')
if __name__ == '__main__':
    import shutil
    bk = S/'morph_data_shcb.accepted.json'
    if not bk.exists(): shutil.copy(S/'morph_data_shcb.json', bk); shutil.copy(S/'design_shcb.json', S/'design_shcb.accepted.json')
    main()
    shutil.copy(bk, S/'morph_data_shcb.json'); shutil.copy(S/'design_shcb.accepted.json', S/'design_shcb.json')
