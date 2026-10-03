#!/bin/bash
# gd11rb_combo.sh <label> <face asset> <HAIR key:tag> <bindings prefix path> <bsuf> <cases-kind: whole|haircu> : compose (no binding) + capture
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; T=Tools/CharacterLookdev_20260930
L=$1; FACE=$2 NOBIND=1 BINDPFX=$4 BSUF=$5 HAIR=$3 SKIN=g11k9 GD3_EYES_TAG=e2 SETS=none CAPP=g11rbtmp bash $T/gd11rb_face_run.sh x 2>&1 | grep -E "COMP4"
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" -c "
import json, os; d=json.load(open('Saved/Codex/CharacterLookdev_20260930/qa_config.json')); bad=[v['binding'] for v in d['grooms'].values() if not os.path.exists(v['binding'].replace('/Game/','Content/')+'.uasset')]
print('BINDINGS_OK' if not bad else 'MISSING_BINDINGS '+str(bad))"
bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 >/dev/null
C32="[-64.468, 113.297, 160.141, -58.0, 1.0]"
if [ "$6" == "whole" ]; then CAMS="(('front', [0, 125, 159, -90, 0], 15), ('q3', $C32, 15), ('side', [-125, 3, 159, 0, 0], 15), ('side2', [125, 3, 159, 180, 0], 15), ('back', [0, -125, 159, 90, 0], 15), ('top', [0, 40, 215, -90, -50], 20), ('rear3q', [88, -88, 161, 135, 0], 15))"; LIGHTS="('studio',)"
else CAMS="(('forehead', [0, 125, 169.8, -90, 0], 6.0), ('topfront', [0, 62, 196, -90, -26], 13.0), ('hairline3q', [-64.468, 113.297, 167.5, -58.0, 0.0], 8.0), ('proftop', [-125, 4, 166.5, 0, 0], 11.0), ('temple', $C32, 9.0), ('rear3q', [88, -88, 161, 135, 0], 12.0), ('bun', [0, -118, 159.5, 90, 0], 9.0))"; LIGHTS="('studio', 'grazing')"; fi
bash $T/gd11r_capcases.sh $L "[dict(name='$L'+'_'+li+'_'+n, view='custom', cam=c, fov=f, garments=True, materials='real', light=li, animation=None, time=0, light_target_z=163) for n, c, f in $CAMS for li in $LIGHTS]"
