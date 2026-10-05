#!/bin/bash
# brow_eval.sh : on the SAME m2 face + h48a hair + k10: A = current brow M_SlightArch, B = brow hidden, C = library alternatives (M_Natural, Soft, S_FlatThin, M_Fine).
# Bindings for each brow are created in the N candidate (GB_G11RN_Eyebrows<BROW>_m2h48a); hair/lash bindings duplicated into N with the same suffix. Provenance recorded per set.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; T=Tools/CharacterLookdev_20260930; N=/Game/Sphirus/CharacterLab/GD11_HeadRefinementN_20261005; ND=Saved/Codex/GD11_HeadRefinementN_20261005
FM=/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005/Face/SKM_G11RM_Face_m2; BP=$N/Face/Bindings/GB_G11RN; SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/b05832b1-23f7-44dd-a92f-e1907201ea47/scratchpad"
CAMS="(('fcfront', [0, 62, 160.0, -90, 0], 22.0), ('fcq3', [-25.4, 50.8, 160.5, -58.0, 1.0], 24.0), ('fcq3L', [25.4, 50.8, 160.5, -122.0, 1.0], 24.0), ('noseroot', [-15.5, 48.7, 162.0, -66, 0], 9.0), ('eyes', [0, 52, 162.3, -90, 0], 9.0), ('front', [0, 125, 159, -90, 0], 15))"
for b in M_SlightArch M_Natural Soft S_FlatThin M_Fine; do
  BROW=$b FACE=$FM HAIR=gm:h48a BSUF=m2h48a SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rn_face_run.sh m2 | grep -E "GD_LB|REFUSE|Traceback" | cut -c1-120
  BROW=$b FACE=$FM NOBIND=1 BINDPFX=$BP BSUF=m2h48a HAIR=gm:h48a SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rn_face_run.sh x | grep COMP4
  bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 >/dev/null
  L=g11rnBROW_$b
  { echo "import builtins; builtins.G11RN_PROV = {'label': '$L', 'candidate': 'm2 + h48a + k10, eyebrow groom GR_GD_Eyebrows_$b (binding GB_G11RN_Eyebrows${b}_m2h48a)', 'out': r'$(cygpath -w "$(pwd)/$ND/prov/$L.json")'}"; cat $T/ue_g11rn_provenance.py; } > "$SC/prov_$L.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/prov_$L.py" prov 300 | grep -o "G11RN_PROV"
  H="[]"; [ "$b" == "M_SlightArch" ] && H2="('_nobrow', ['Eyebrows'])," || H2=""
  bash $T/gd11r_capcases.sh $L "[dict(name='$L'+'_'+li+'_'+n+sfx, view='custom', cam=c, fov=f, garments=True, materials='real', light=li, animation=None, time=0, light_target_z=163, hide=h) for n, c, f in $CAMS for li in ('studio', 'front') for sfx, h in (('', []), $H2)]" | grep -E "DONE|ERROR"
done
echo BROW_EVAL_END
