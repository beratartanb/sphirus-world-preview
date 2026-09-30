#!/bin/bash
# fm_face_captures.sh <prefix> <face: rv | fm_<suffix>> [hair_tag] [sets] : switch the QA composition to the given face (and its bindings), then
# capture the facial-rig set (23 RigLogic cases x front/3q close cams) and/or the head likeness set (front/3q/side/close, hair + no-hair + clay)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; P=$1; FACE=$2; HT=${3:-v14k}; SETS=${4:-rig,head}; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; C=Saved/Codex/CharacterLookdev_20260930/captures
"$PY" - "$FACE" "$HT" <<'EOF'
import json, sys
face, ht = sys.argv[1], sys.argv[2]; p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p))
H = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Hair/'; B = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Face/Bindings/'
if face == 'rv':
    d['face'] = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Body/SKM_RV_FaceMesh'
    d['grooms']['HairMain'] = {'groom': H+f'GR_LK_Hair_Main_{ht}', 'binding': H+f'GR_LK_Hair_Main_{ht}_Binding', 'attach': 'Head'}
    d['grooms']['HairLoose'] = {'groom': H+f'GR_LK_Hair_Loose_{ht}', 'binding': H+f'GR_LK_Hair_Loose_{ht}_Binding', 'attach': 'Head'}
    d['grooms']['Eyebrows']['binding'] = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Hair/RV_Eyebrows_M_Slit_Binding'
    d['grooms']['Eyelashes']['binding'] = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Hair/RV_Eyelashes_L_Curl_Binding'
else:
    sfx = face.split('_', 1)[1]; d['face'] = f'/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Face/SKM_FM_FaceMesh_{sfx}'
    d['grooms']['HairMain'] = {'groom': H+f'GR_LK_Hair_Main_{ht}', 'binding': B+f'GB_FM_HairMain_{sfx}', 'attach': 'Head'}
    d['grooms']['HairLoose'] = {'groom': H+f'GR_LK_Hair_Loose_{ht}', 'binding': B+f'GB_FM_HairLoose_{sfx}', 'attach': 'Head'}
    d['grooms']['Eyebrows']['binding'] = B+f'GB_FM_Eyebrows_{sfx}'; d['grooms']['Eyelashes']['binding'] = B+f'GB_FM_Eyelashes_{sfx}'
json.dump(d, open(p, 'w'), indent=1); print('QA face ->', d['face'].split('/')[-1], d['grooms']['HairMain']['binding'].split('/')[-1])
EOF
bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup-$RANDOM 300 | tail -1
run() { "$PY" -c "import json; S=$2; json.dump({'label':'$1','cases':S}, open('$C/capture_request.json','w'), indent=1)"; rm -f "$C/$1_results.json" "$C/$1_error.txt"
  bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_lk_capture.py")" lk-cap-$RANDOM 120 | tail -1 >/dev/null
  until [ -f "$C/$1_results.json" ] || [ -f "$C/$1_error.txt" ]; do sleep 2; done; [ -f "$C/$1_error.txt" ] && { echo "ERROR $1"; head -c 600 "$C/$1_error.txt"; } || echo "DONE $1"; }
if [[ $SETS == *rig* ]]; then
  run ${P}_rig "[dict(name='${P}_rig_'+c['name']+'_'+k, view='custom', cam=cam, fov=fov, garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=158, face_anim=J['animation'], face_time=c['time']) for J in [json.load(open('Saved/Codex/CharacterFaceMatch_20260930/fm_face_cases.json'))] for c in J['cases'] for k, cam, fov in (('front', [0, 62, 159.5, -90, 0], 20), ('3q', [-44, 44, 159.5, -45, 0], 20))]"
fi
if [[ $SETS == *head* ]]; then
  run ${P}_head "[dict(name='${P}_'+v+'_'+k, view='custom', cam=c, fov=f, garments=True, materials=('clay' if v == 'clay' else 'real'), light='studio', animation=None, time=0, light_target_z=158, **({'hide': ['HairMain','HairLoose']} if v == 'nohair' else {}), **({'hair': False} if v == 'clay' else {})) for v in ('hair', 'nohair', 'clay') for k, (c, f) in {'front': ([0, 125, 159, -90, 0], 15), 'front3q': ([-88, 90, 159, -45, 0], 15), 'side': ([125, 3, 159, 180, 0], 15), 'close': ([-40, 62, 160, -57, -2], 13)}.items()]"
fi
