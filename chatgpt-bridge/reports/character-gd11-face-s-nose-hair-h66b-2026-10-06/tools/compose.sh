#!/bin/bash
# compose.sh <label> <m2|r3> <hair tag in HairQ> [none] : locked brow M_SlightArch + S_Thin + k10/e2; face m2 (M bindings) or r3 (R bindings); hair from GD11_HairQ_20261006 bound to that face
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; L=$1; FK=$2; HT=$3; T=Tools/CharacterLookdev_20260930; R=Saved/Codex/GD11_FaceS_20261006; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/b05832b1-23f7-44dd-a92f-e1907201ea47/scratchpad"
if [ $FK = m2 ]; then F=/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005/Face/SKM_G11RM_Face_m2; BP=/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005/Face/Bindings/GB_G11RM; BS=m2h48a; HB=/Game/Sphirus/CharacterLab/GD11_HairQ_20261006/Face/Bindings/GB_G11RQ; HS=m2$HT
else F=/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Face/SKM_G11RR_Face_$FK; BP=/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Face/Bindings/GB_G11RR; BS=${FK}h48a; HB=$BP; HS=$FK$HT; fi
BROW=M_SlightArch FACE=$F NOBIND=1 BINDPFX=$BP BSUF=$BS HAIR=gm:h48a SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rr_face_run.sh x >/dev/null
MSYS_NO_PATHCONV=1 "$PY" - "$HT" "$HB" "$HS" <<'PYE'
import json, sys, os
p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); t, hb, hs = sys.argv[1:4]; V = '/Game/Sphirus/CharacterLab/GD11_HairQ_20261006'
for part in ('Main', 'Loose'): d['grooms']['Hair'+part].update(groom=V+'/Hair/GR_LK_Hair_%s_%s' % (part, t), binding='%s_Hair%s_%s' % (hb, part, hs))
d['save_prefixes'] = ['/Game/Sphirus/CharacterLab/GD11_FaceR_20261006']; d['studio_folder'] = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Studio'
bad = [x for v in d['grooms'].values() for x in (v['binding'], v['groom']) if not os.path.exists(x.replace('/Game/', 'Content/')+'.uasset')]
json.dump(d, open(p, 'w'), indent=1); print('QA', 'OK' if not bad else 'MISSING '+str(bad), d['face'].split('/')[-1], {k: v['binding'].split('/')[-1] for k, v in d['grooms'].items()})
PYE
bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 >/dev/null
mkdir -p $R/prov; { echo "import builtins; builtins.G11RO_PROV = {'label': '$L', 'candidate': '$FK + M_SlightArch + $HT + k10/e2', 'out': r'$(cygpath -w "$(pwd)/$R/prov/$L.json")'}"; cat $T/ue_g11ro_provenance.py; } > "$SC/prov_$L.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/prov_$L.py" prov 300 | grep -o "G11RO_PROV" | head -1
[ "${4:-std}" = none ] && exit 0
V="('front', [0, 125, 159, -90, 0], 15, 'studio'), ('q3L', [64.468, 113.297, 160.141, -122.0, 1.0], 15, 'studio'), ('q3R', [-64.468, 113.297, 160.141, -58.0, 1.0], 15, 'studio'), ('profL', [125, 3, 160, 180, 0], 15, 'studio'), ('profR', [-125, 3, 160, 0, 0], 15, 'studio'), ('back', [0, -125, 159, 90, 0], 15, 'rearR'), ('rear3qR', [-88, -88, 161, 45, 0], 15, 'rearR'), ('rear3qL', [88, -88, 161, 135, 0], 15, 'rearL'), ('napeB', [0, -80, 156, 90, 0], 12, 'rearR'), ('fcfront', [0, 62, 160.0, -90, 0], 22.0, 'studio'), ('fcq3', [-25.4, 50.8, 160.5, -58.0, 1.0], 24.0, 'studio'), ('fcq3L', [25.4, 50.8, 160.5, -122.0, 1.0], 24.0, 'studio'), ('eyes', [0, 40, 163.0, -90, 0], 14.0, 'studio')"
bash $T/gd11r_capcases.sh $L "[dict(name='$L'+'_'+n+sfx, view='custom', cam=c, fov=fv, garments=True, materials='real', light=li, animation=None, time=0, light_target_z=163, hide=h) for n, c, fv, li in ($V) for sfx, h in (('', []), ('_main', ['HairLoose']))]" | grep -E "DONE|ERROR"
