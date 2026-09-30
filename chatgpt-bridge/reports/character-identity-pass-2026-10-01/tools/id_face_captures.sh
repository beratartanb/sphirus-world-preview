#!/bin/bash
# id_face_captures.sh <prefix> <face sfx | rv | fm_c> <hair tag> [sets clay,real,hair,rig] : IDENTITY-pass face gate captures.
# Cameras: reffront / refclose = the weak-perspective cameras SOLVED for the reference front / close-3/4 images (so candidate and
# reference share the head pose), + front3q / side (profile) / front (standard lookdev head cams). clay = neutral clay, no grooms;
# real = skin, brows + lashes, no hair; hair = full; rig = 23 RigLogic cases x reffront / refclose.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; P=$1; FACE=$2; HT=$3; SETS=${4:-clay,real,hair}; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; C=Saved/Codex/CharacterLookdev_20260930/captures
"$PY" - "$FACE" "$HT" <<'PYE'
import json, sys
face, ht = sys.argv[1], sys.argv[2]; p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); H = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Hair/'
if face == 'rv':
    d['face'] = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Body/SKM_RV_FaceMesh'; B = None
    d['grooms']['HairMain'] = {'groom': H+f'GR_LK_Hair_Main_{ht}', 'binding': H+f'GR_LK_Hair_Main_{ht}_Binding', 'attach': 'Head'}
    d['grooms']['HairLoose'] = {'groom': H+f'GR_LK_Hair_Loose_{ht}', 'binding': H+f'GR_LK_Hair_Loose_{ht}_Binding', 'attach': 'Head'}
    d['grooms']['Eyebrows']['binding'] = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Hair/RV_Eyebrows_M_Slit_Binding'; d['grooms']['Eyelashes']['binding'] = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Hair/RV_Eyelashes_L_Curl_Binding'
else:
    if face.startswith('fm_'): s = face[3:]; d['face'] = f'/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Face/SKM_FM_FaceMesh_{s}'; B, pre = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Face/Bindings/', 'GB_FM'
    else: s = face; d['face'] = f'/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Face/SKM_ID_FaceMesh_{s}'; B, pre = '/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Face/Bindings/', 'GB_ID'
    gm = json.load(open('Saved/Codex/CharacterIdentity_20260930/hair_grooms.json')) if ht.startswith('id') else None
    d['grooms']['HairMain'] = {'groom': gm['main'] if gm else H+f'GR_LK_Hair_Main_{ht}', 'binding': B+f'{pre}_HairMain_{s}', 'attach': 'Head'}
    d['grooms']['HairLoose'] = {'groom': gm['loose'] if gm else H+f'GR_LK_Hair_Loose_{ht}', 'binding': B+f'{pre}_HairLoose_{s}', 'attach': 'Head'}
    d['grooms']['Eyebrows'] = {'groom': '/Game/MetaHumans/MH_MainCharacter/Grooms/Eyebrows_M_Slit', 'binding': B+f'{pre}_Eyebrows_{s}', 'attach': 'Head'}; d['grooms']['Eyelashes']['binding'] = B+f'{pre}_Eyelashes_{s}'
import os
if os.environ.get('ID_BROW') and face not in ('rv',) and not face.startswith('fm_'):
    st = os.environ['ID_BROW']; d['grooms']['Eyebrows'] = {'groom': f'/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Grooms/GR_ID_Eyebrows_{st}', 'binding': B+f'GB_ID_Brow{st}_{s}', 'attach': 'Head'}
json.dump(d, open(p, 'w'), indent=1); print('QA face ->', d['face'].split('/')[-1], d['grooms']['HairMain']['binding'].split('/')[-1])
PYE
bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1
run() { "$PY" -c "import json; S=$2; json.dump({'label':'$1','cases':S}, open('$C/capture_request.json','w'), indent=1)"; rm -f "$C/$1_results.json" "$C/$1_error.txt"
  bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_lk_capture.py")" lk-cap 120 | tail -1 >/dev/null
  until [ -f "$C/$1_results.json" ] || [ -f "$C/$1_error.txt" ]; do sleep 2; done; [ -f "$C/$1_error.txt" ] && { echo "ERROR $1"; head -c 600 "$C/$1_error.txt"; } || echo "DONE $1"; }
CAMS="{'reffront': ([0.95, 129.7, 170.3, -90.4, -3.8], 15), 'refclose': ([-91.0, 88.6, 143.3, -42.6, 8.6], 15), 'front3q': ([-88, 90, 159, -45, 0], 15), 'side': ([-125, 3, 159, 0, 0], 15), 'front': ([0, 125, 159, -90, 0], 15), 'back': ([0, -125, 159, 90, 0], 15), 'top': ([0, 40, 215, -90, -50], 20)}"
[[ $SETS == *clay* ]] && run ${P}_clay "[dict(name='${P}_clay_'+k, view='custom', cam=c, fov=f, garments=True, materials='clay', hair=False, light='studio', animation=None, time=0, light_target_z=160, hide=['Eyebrows', 'Eyelashes']) for k, (c, f) in $CAMS.items()]"
[[ $SETS == *real* ]] && run ${P}_real "[dict(name='${P}_real_'+k, view='custom', cam=c, fov=f, garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=160, hide=['HairMain', 'HairLoose']) for k, (c, f) in $CAMS.items()]"
[[ $SETS == *hair* ]] && run ${P}_hair "[dict(name='${P}_hair_'+k, view='custom', cam=c, fov=f, garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=160) for k, (c, f) in $CAMS.items()]"
[[ $SETS == *rig* ]] && run ${P}_rig "[dict(name='${P}_rig_'+c['name']+'_'+k, view='custom', cam=cam, fov=fov, garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=160, hide=['HairMain', 'HairLoose'], face_anim=J['animation'], face_time=c['time']) for J in [json.load(open('Saved/Codex/CharacterFaceMatch_20260930/fm_face_cases.json'))] for c in J['cases'] for k, cam, fov in (('front', [0, 62, 159.5, -90, 0], 20), ('3q', [-44, 44, 159.5, -45, 0], 20))]"
exit 0
