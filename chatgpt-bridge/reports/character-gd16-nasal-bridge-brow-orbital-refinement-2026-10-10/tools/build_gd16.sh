#!/bin/bash
# build_gd16.sh : documented reproduction chain of GD16 G16 (final candidate). Every step writes NEW names only (guards refuse existing assets).
# start = GD15 G15 sculpt (data/head_G15S.npy, from SourceAssets/Characters/GD15_IdentityMaster_20261009/data)
# Blender stages (this script with --blender-stage rebuilds them into data/*_rebuild.npy and compares with the stored heads):
#  N1b  real brushes (GUI): profile-view Grab radix back, Draw ADD nasal bridge, infratip/columella grab, dorsum smooth   (ops/N1b.json)
#  N2   infratip + columella lift grabs                                                                                    (ops/N2add.json)
#  N3   front-view rigid alar-lobule narrowing + dome narrowing + infratip                                                 (ops/N3add.json)
#  N4   alar narrowing pass 2 + alar flare / lobule mild deflate                                                           (ops/N4add.json)
#  N6   lobule plateau lift 1.5 mm, masked to the nose (upper lip 0.000 mm)                                                (ops/N6add.json, gd13_sculpt.py)
#  B3   supraorbital ridge plateau field back 1.6 mm + right radix flank back 1.3 mm + displacement relax (gd13_sculpt.py ops/B3move.json)
#       then real Smooth brushes on corrugator / glabella / field edge                                                     (ops/B2smooth.json)
#  G16S technical commissure repair: blend displacement rigid vs GD14 W9 inside 2 small spheres (0 flipped triangles)    (gd16_rigidcorner.py)
#  brow c4: reference stations (data/brow_stations_v2.json, measured on the user's front panel) -> 3D via the solved front camera
#       (gd16_browproj.py) -> custom groom (gd16_brow.py, env below) -> Alembic
# UE stages (editor runner + gd16_memguard.sh):
#  1 MHC_GD15_G15 duplicated to MHC_GD16_G15base (ue_gd16_mhc.py op dup; GD15 untouched)
#  2 gd16_final16.sh: fit + 2 residual-feedback fits -> MHC_GD16_G16; auto-rig -> SKM_GD16_Face_g16 + DNA; custom brow c4 import
#    (ue_gd16_brow_import.py: MI_Hair-based MI_GD15_BrowS_auburnDark, width 0.0095, tip 0.5, stable rasterization) bound to the face;
#    look (h75c hair, S_Thin lashes, iris h6, skin s1t5); captures front + studio; GD15 G15 recaptured with the same look
#  3 boards: make_gd16_final.sh
set -e; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD16_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009; Wp() { cygpath -w "$(pwd)/$1"; }
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
[ "${1:-}" = "--blender-stage" ] || { echo "UE steps are listed above; run them one by one. --blender-stage rebuilds the Blender sculpt + brow stages"; exit 0; }
D=$W/data; R=_rebuild
bs() { timeout 1500 "$B" --factory-startup --python "$(Wp $W/tools/gd16_bsculpt.py)" -- "$(Wp $D/head_$1.npy)" "$(Wp $D/head_topo.npz)" "$(Wp $W/ops/$2)" "$(Wp $D/head_$3.npy)" "$(Wp $W/bs_$3.json)" >/dev/null 2>&1; echo "BS $3"; }
sc() { "$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $D/head_$1.npy)" "$(Wp $W/ops/$2)" "$(Wp $D/head_$3.npy)" 2>&1 | grep "^OP" | cut -c1-80; }
bs G15S N1b.json N1b$R; bs N1b$R N2add.json N2$R; bs N2$R N3add.json N3$R; bs N3$R N4add.json N4$R; sc N4$R N6add.json N6$R; sc N6$R B3move.json B3m$R; bs B3m$R B2smooth.json B3$R
"$B" -b --factory-startup --python "$(Wp $W/tools/gd16_rigidcorner.py)" -- "$(Wp $D/head_B3$R.npy)" "$(Wp $D/head_w9_postrig.npy)" "$(Wp $D/head_G16S$R.npy)" "[[-2.25,12.0,155.5,0.15,0.45],[-2.41,12.19,155.42,0.10,0.26]]" 2>&1 | grep RIGID
"$B" -b --factory-startup --python-expr "
import numpy as np
D=r'$(Wp $D)'
for a, b in (('N6', 'N6_rebuild'), ('B3', 'B3_rebuild'), ('G16S', 'G16S_rebuild')):
    X=np.load(D+r'\head_%s.npy' % a); Y=np.load(D+r'\head_%s.npy' % b); d=np.linalg.norm(X-Y,axis=1)*10; print('REBUILD %-5s vs stored: max %.3f mm, mean %.4f mm' % (a, d.max(), d.mean()))" 2>&1 | grep REBUILD
"$B" -b --factory-startup --python "$(Wp $W/tools/gd16_browproj.py)" -- "$(Wp $D/head_B3.npy)" "$(Wp $D/Ec_cams.json)" "$(Wp $D/brow_stations_v2.json)" "$(Wp $D/brow3d_v2_B3$R.json)" 2>&1 | grep -c BROWPROJ >/dev/null
mkdir -p $W/brow/c4$R; BR_ROOT_LO=-0.15 BR_ROOT_HI=0.88 BR_HEAD_ANG=62 BR_BODY_UP=18 BR_BODY_DOWN=-16 BR_HEADLEN=0.52 BR_LEN=0.6 BR_N=2300 BR_SEED=13 "$B" -b --factory-startup --python "$(Wp $W/tools/gd16_brow.py)" -- "$(Wp $D/head_B3.npy)" "$(Wp $D/brow3d_v2_B3$R.json)" "$(Wp $W/brow/c4$R)" 2>&1 | grep -c BROW_OK >/dev/null
"$B" -b --factory-startup --python-expr "
import numpy as np
A=np.load(r'$(Wp $W/brow/c4/strands.npz)')['main']; Bb=np.load(r'$(Wp $W/brow/c4$R/strands.npz)')['main']; print('REBUILD brow c4 strands', A.shape, Bb.shape, 'max diff %.4f cm' % (np.abs(A-Bb).max() if A.shape == Bb.shape else -1))" 2>&1 | grep REBUILD
