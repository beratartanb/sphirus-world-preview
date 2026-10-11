#!/bin/bash
# make_gd37_process.sh : process boards of the GD37 lip / nose target design (Blender clay in the solved reference cameras: GD36 K36 post-rig,
# M1 border-ridge only, N1 + mouth line / lower nose, N2 final target) + the profile contour overlay.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD37_Identity_20261011; P=$N/bd/parts; O=$N/bd/process; mkdir -p $P $O
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; m() { cygpath -m "$(pwd)/$1"; }; w() { cygpath -w "$(pwd)/$1"; }
"$PY" - "$(m $N/r)" "$(m $P)" "$(m $N/bd/spec_process.json)" <<'PYE'
import json, sys, os
R, P, OUT = sys.argv[1:4]; S = []
ZOOM = {'prof_faceL': [30, 400, 370, 740], 'q3_faceR': [560, 380, 900, 720], 'front': [370, 430, 680, 740]}
for v, r in ZOOM.items():
    S.append(dict(src='REF:'+v, rect=r, w=320, out=f'{P}/p_ref_{v}.jpg'))
    for nm in ('K36PM', 'M1', 'N1', 'N2'):
        f = f'{R}/{nm}_REF_{v}_clayA.png'
        if os.path.exists(f): S.append(dict(src=f, rect=r, w=320, out=f'{P}/p_{nm}_{v}.jpg'))
json.dump(S, open(OUT, 'w')); print('SPEC', len(S))
PYE
"$B" -b --factory-startup --python "$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools/gd13_parts.py)" -- "$(w $N/bd/spec_process.json)" 2>&1 | grep -oE "PARTS_OK.*"
row() { local r=""; for it in "$@"; do f=${it%%|*}; [ -f $P/$f ] && r="${r:+$r, }$(w $P/$f)|${it#*|}"; done; echo "$r"; }
BD() { "$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(w $O/$1)" "$2" $3 "${@:4}" >/dev/null; }
rows=(); for v in prof_faceL q3_faceR front; do rows+=("$(row "p_ref_$v.jpg|REF $v" "p_K36PM_$v.jpg|GD36 kil" "p_M1_$v.jpg|M1 sinir sirti" "p_N1_$v.jpg|N1 + agiz cizgisi + burun" "p_N2_$v.jpg|N2 secilen hedef")"); done
BD 01_KIL_ADAYLARI.jpg "01 Kil adaylari (cozulmus referans kameralari) - REF / GD36 / M1 / N1 / N2" 320 "${rows[@]}"
cp $N/meas/contour_N2.jpg $O/02_PROFIL_KONTUR_REF_GD36_N1_N2.jpg; cp $N/data/head_N2_class.png $O/03_VERMILION_SINIFLAMA_N2.png 2>/dev/null
ls $O
