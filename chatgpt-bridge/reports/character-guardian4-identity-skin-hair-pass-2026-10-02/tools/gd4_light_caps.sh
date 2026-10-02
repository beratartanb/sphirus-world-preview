#!/bin/bash
# gd4_light_caps.sh <prefix> : QA lighting A-E on the CURRENT qa composition (face real + hair): A studio, B grazing, C grazing_top, D gameplay (sun+sky), E interior; front + ~33 deg 3/4
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; P=$1; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; C=Saved/Codex/CharacterLookdev_20260930/captures
CF=$("$PY" -c "import json; c=json.load(open('Saved/Codex/CharacterGuardian_20261001/camfit_close.json')); print([round(c['origin'][0],3), round(c['origin'][1],3), round(c['origin'][2],3), c['yaw'], c['pitch']])")
"$PY" -c "import json; S=[dict(name='${P}_'+L+'_'+k, view='custom', cam=c, fov=15, garments=True, materials='real', hair=True, light=m, animation=None, time=0, light_target_z=160) for L, m in (('A_studio','studio'),('B_grazing','grazing'),('C_grazingtop','grazing_top'),('D_gameplay','gameplay'),('E_interior','interior')) for k, c in (('front',[0.95, 129.7, 170.3, -90.4, -3.8]),('3q',$CF))]; json.dump({'label':'$P','cases':S}, open('$C/capture_request.json','w'), indent=1)"
rm -f "$C/${P}_results.json" "$C/${P}_error.txt"; bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_lk_capture.py")" lk-cap 120 | tail -1 >/dev/null
until [ -f "$C/${P}_results.json" ] || [ -f "$C/${P}_error.txt" ]; do sleep 2; done; [ -f "$C/${P}_error.txt" ] && { echo "ERROR $P"; head -c 600 "$C/${P}_error.txt"; } || echo "DONE $P"
