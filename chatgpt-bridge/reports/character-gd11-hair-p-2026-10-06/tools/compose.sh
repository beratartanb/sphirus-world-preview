#!/bin/bash
# compose.sh <label> <hair: h51a|h5Xa> [caps: std|none] : locked face package (m2 + M DNA + M_SlightArch/S_Thin M bindings + k10/e2) + the given hair.
# h51a uses the revert bindings GB_G11RV_*_m2h51a (O grooms, unchanged); P tags use GD11_HairP_20261006 grooms + GB_G11RP_*_m2<tag>. Editor-read provenance per label.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; L=$1; HT=$2; T=Tools/CharacterLookdev_20260930; R=Saved/Codex/GD11_HairP_20261006; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/b05832b1-23f7-44dd-a92f-e1907201ea47/scratchpad"; M=/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005
BROW=M_SlightArch FACE=$M/Face/SKM_G11RM_Face_m2 NOBIND=1 BINDPFX=$M/Face/Bindings/GB_G11RM BSUF=m2h48a HAIR=gm:h48a SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11ro_face_run.sh x >/dev/null
"$PY" - "$HT" <<'PYE'
import json, sys, os
p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); V = '/Game/Sphirus/CharacterLab/GD11_HairP_20261006'; t = sys.argv[1]
for part in ('Main', 'Loose'):
    if t == 'h51a': d['grooms']['Hair'+part].update(groom='/Game/Sphirus/CharacterLab/GD11_HeadRefinementO_20261005/Hair/GR_LK_Hair_%s_h51a' % part, binding='/Game/Sphirus/CharacterLab/GD11_RevertM_20261006/Face/Bindings/GB_G11RV_Hair%s_m2h51a' % part)
    else: d['grooms']['Hair'+part].update(groom=V+'/Hair/GR_LK_Hair_%s_%s' % (part, t), binding=V+'/Face/Bindings/GB_G11RP_Hair%s_m2%s' % (part, t))
d['save_prefixes'] = [V]; d['studio_folder'] = V+'/Studio'
bad = [x for v in d['grooms'].values() for x in (v['binding'], v['groom']) if not os.path.exists(x.replace('/Game/', 'Content/')+'.uasset')]
json.dump(d, open(p, 'w'), indent=1); print('QA', t, 'OK' if not bad else 'MISSING '+str(bad), d['face'].split('/')[-1], d['grooms']['Eyebrows']['groom'].split('/')[-1])
PYE
bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 >/dev/null
mkdir -p $R/prov; { echo "import builtins; builtins.G11RO_PROV = {'label': '$L', 'candidate': 'm2 + M_SlightArch + $HT + k10/e2', 'out': r'$(cygpath -w "$(pwd)/$R/prov/$L.json")'}"; cat $T/ue_g11ro_provenance.py; } > "$SC/prov_$L.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/prov_$L.py" prov 300 | grep -o "G11RO_PROV" | head -1
[ "${3:-std}" = none ] && exit 0
V="('front', [0, 125, 159, -90, 0], 15), ('q3R', [-64.468, 113.297, 160.141, -58.0, 1.0], 15), ('q3L', [64.468, 113.297, 160.141, -122.0, 1.0], 15), ('profR', [-125, 3, 160, 0, 0], 15), ('profL', [125, 3, 160, 180, 0], 15), ('rear3qR', [-88, -88, 161, 45, 0], 15), ('rear3qL', [88, -88, 161, 135, 0], 15), ('back', [0, -125, 159, 90, 0], 15), ('tmR', [-52, 40, 165, -37.5, 0], 13), ('tmL', [52, 40, 165, -142.5, 0], 13), ('earR', [-66, -6, 162.5, 5, 0], 12), ('earL', [66, -6, 162.5, 175, 0], 12), ('napeB', [0, -70, 158, 90, 0], 14), ('bunR', [-50, -50, 161.5, 45, 0], 14), ('bunL', [50, -50, 161.5, 135, 0], 14)"
bash $T/gd11r_capcases.sh $L "[dict(name='$L'+'_'+n+sfx, view='custom', cam=c, fov=fv, garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=163, hide=h) for n, c, fv in ($V) for sfx, h in (('', []), ('_main', ['HairLoose']))]" | grep -E "DONE|ERROR"
