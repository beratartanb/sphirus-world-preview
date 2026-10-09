#!/bin/bash
# build_gd15.sh : documented reproduction chain of GD15 G15 (final candidate). Every step writes NEW names only (guards refuse existing assets).
# UE steps (editor runner + gd15_memguard.sh before each MHC edit set):
# 0  start = GD14 W9 MHC state                      -> duplicate MHC_GD15_M0 (ue_gd15_mhc.py op dup)
# 1  MetaHuman region preset libraries on a throwaway probe of M0 (ue_gd15_regblend.py): nose [13], mouth [16], eyes [7,8], lower cheek [14,15],
#    cheek [9,10,14,15] -> mhc/rb/<prefix>_<preset>.f32 (region blends are exactly linear in the weight: verified 0.00 mm)
# 2  compose MHC_GD15_C8 = M0 + nose Sunita 1.0 + mouth Etta 0.5:  gd15_compose.sh C8 "[[[13], 'Sunita', 1.0], [[16], 'Etta', 0.5]]"
# 3  MetaHuman Creator lid landmarks:                gd15_step.sh MHC_GD15_C8 MHC_GD15_C8L tgt_L1.json C8L 12   -> data/head_C8L.npy
# Blender stages (this script with --blender-stage rebuilds them into data/*_rebuild.npy and compares with the stored heads):
# 4  real sculpt brushes, GUI session (ops/E3.json; outward-corrected winding)            -> head_C8LE3
# 5  upper-lid rotation over the eyeball, 1.1 mm (gd13_sculpt.py ops/LR2.json)            -> head_C8LE3LR2
# 6  mouth preset split: Etta upper 0.2 / lower 0.45 replaces Etta 0.5 (gd15_mouthsplit.py) -> head_C9EUL = LR2 + (split - C8LE3)
# 7  anterior malar fat pad + mid-cheek soft-tissue fill (gd13_sculpt.py ops/SF3.json)     -> head_C9S3a
# 8  technical repairs: canthus local blend to W9, commissure rigid blend displacement (gd15_rigidcorner.py), canthus blend to E -> head_C9S4
# 9  remove the brow-lowering grabs (ops/E3brow.json re-run on C8L, delta subtracted: the reference brow sits HIGHER)  -> head_C9S5 = head_G15S
# UE again:
# 10 transfer + rig + look + captures:  BROWSRC_D=-0.07 BROWSRC_TAG=u07 gd15_final15.sh data/head_G15S.npy G15 MHC_GD15_C8L
#    (fit + 2 residual-feedback fits -> MHC_GD15_G15; auto-rig -> SKM_GD15_Face_g15 + DNA; look B: h75c, FlatThick auburn-dark brows raised 0.7 mm
#     source-proxy [face untouched], S_Thin lashes, iris h6, skin s1t5 = f5 texture [gd15_skintex.py ops/skin_f5.json])
# 11 boards: make_gd15_final.sh
set -e; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD15_Identity_20261009; G=Saved/Codex/GD13_Identity_20261009; Wp() { cygpath -w "$(pwd)/$1"; }
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
[ "${1:-}" = "--blender-stage" ] || { echo "UE steps are listed above; run them one by one. --blender-stage rebuilds steps 4-9 from data/head_C8L.npy"; exit 0; }
D=$W/data; R=_rebuild
timeout 1500 "$B" --factory-startup --python "$(Wp $W/tools/gd15_bsculpt.py)" -- "$(Wp $D/head_C8L.npy)" "$(Wp $D/head_topo.npz)" "$(Wp $W/ops/E3.json)" "$(Wp $D/head_C8LE3$R.npy)" "$(Wp $W/bs_C8LE3$R.json)" >/dev/null 2>&1
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $D/head_C8LE3$R.npy)" "$(Wp $W/ops/LR2.json)" "$(Wp $D/head_C8LE3LR2$R.npy)" 2>&1 | grep "^OP"
"$B" -b --factory-startup --python "$(Wp $W/tools/gd15_mouthsplit.py)" -- "$(Wp $D/head_C8LE3$R.npy)" "$(Wp $W/mhc/probe_base.f32)" "$(Wp $W/mhc/rb/mouth_Etta.f32)" 0.5 "$(Wp $W/mhc/rb/mouth_Etta.f32)" 0.2 0.45 "$(Wp $D/head_C8LE3m_EUL$R.npy)" 2>&1 | grep MOUTHSPLIT
"$B" -b --factory-startup --python-expr "
import numpy as np
D=r'$(Wp $D)'; C=np.load(D+r'\head_C8LE3$R.npy'); L=np.load(D+r'\head_C8LE3LR2$R.npy'); M=np.load(D+r'\head_C8LE3m_EUL$R.npy'); np.save(D+r'\head_C9EUL$R.npy', L+(M-C)); print('C9EUL ok')" 2>&1 | grep ok
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $D/head_C9EUL$R.npy)" "$(Wp $W/ops/SF3.json)" "$(Wp $D/head_C9S3a$R.npy)" 2>&1 | grep "^OP"
"$B" -b --factory-startup --python "$(Wp $W/tools/gd15_foldrepair.py)" -- "$(Wp $D/head_C9S3a$R.npy)" "$(Wp $D/head_w9_postrig.npy)" "$(Wp $D/head_C9S3$R.npy)" "[[-4.65, 10.72, 162.24, 0.12, 0.4], [-1.78, 11.42, 162.15, 0.1, 0.35]]" 2>&1 | grep REPAIR
"$B" -b --factory-startup --python-expr "
import numpy as np
D=r'$(Wp $D)'; L=lambda f: np.fromfile(f,np.float32).reshape(-1,3).astype(float); P=L(r'$(Wp $W/mhc/probe_base.f32)'); E=L(r'$(Wp $W/mhc/rb/mouth_Etta.f32)')
X=np.load(D+r'\head_C9S3$R.npy'); dM=np.load(D+r'\head_C9EUL$R.npy')-np.load(D+r'\head_C8LE3LR2$R.npy'); np.save(D+r'\head_C9S3_nomouth$R.npy', X-dM-0.5*(E-P)); print('NB ok')" 2>&1 | grep ok
"$B" -b --factory-startup --python "$(Wp $W/tools/gd15_rigidcorner.py)" -- "$(Wp $D/head_C9S3$R.npy)" "$(Wp $D/head_C9S3_nomouth$R.npy)" "$(Wp $D/head_C9S3rcb$R.npy)" "[[-2.72, 12.28, 155.44, 0.2, 0.65], [2.30, 12.2, 155.4, 0.2, 0.65]]" 2>&1 | grep RIGID
"$B" -b --factory-startup --python "$(Wp $W/tools/gd15_foldrepair.py)" -- "$(Wp $D/head_C9S3rcb$R.npy)" "$(Wp $D/head_E.npy)" "$(Wp $D/head_C9S4$R.npy)" "[[-4.65, 10.72, 162.25, 0.08, 0.3]]" 2>&1 | grep REPAIR
timeout 900 "$B" --factory-startup --python "$(Wp $W/tools/gd15_bsculpt.py)" -- "$(Wp $D/head_C8L.npy)" "$(Wp $D/head_topo.npz)" "$(Wp $W/ops/E3brow.json)" "$(Wp $D/head_C8Lbrow$R.npy)" "$(Wp $W/bs_C8Lbrow$R.json)" >/dev/null 2>&1
"$B" -b --factory-startup --python-expr "
import numpy as np
D=r'$(Wp $D)'; A=np.load(D+r'\head_C8L.npy'); Bh=np.load(D+r'\head_C8Lbrow$R.npy'); X=np.load(D+r'\head_C9S4$R.npy'); Y=X-(Bh-A); np.save(D+r'\head_G15S$R.npy', Y)
S=np.load(D+r'\head_G15S.npy'); d=np.linalg.norm(Y-S,axis=1)*10; print('REBUILD vs stored G15S: max %.3f mm, mean %.4f mm' % (d.max(), d.mean()))" 2>&1 | grep REBUILD
