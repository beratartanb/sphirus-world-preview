#!/bin/bash
# brow_diag.sh : F4ab + h45b (J bindings) nose-root diagnosis captures WITH and WITHOUT the eyebrow groom, studio + grazing + balanced front light; provenance recorded.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; T=Tools/CharacterLookdev_20260930; SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/b05832b1-23f7-44dd-a92f-e1907201ea47/scratchpad"
F4=/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab; JB=/Game/Sphirus/CharacterLab/GD11_HeadRefinementJ_20261005/Face/Bindings/GB_G11RJ; L=g11rlBROW
FACE=$F4 NOBIND=1 BINDPFX=$JB BSUF=f4abh45b HAIR=gj:h45b SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rl_face_run.sh x | grep COMP4
bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 >/dev/null
{ echo "import builtins; builtins.G11RL_PROV = {'label': '$L', 'candidate': 'F4ab + h45b (J bindings) + k10; brow groom hidden in *_nobrow cases', 'out': r'$(cygpath -w "$(pwd)/Saved/Codex/GD11_HeadRefinementL_20261005/prov/$L.json")'}"; cat $T/ue_g11rl_provenance.py; } > "$SC/prov_$L.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/prov_$L.py" prov 300 | grep -o "G11RL_PROV.*" | cut -c1-300
CAMS="(('noseroot', [-15.5, 48.7, 162.0, -66, 0], 9.0), ('fcq3', [-25.4, 50.8, 160.5, -58.0, 1.0], 24.0), ('fcfront', [0, 62, 160.0, -90, 0], 22.0), ('fcprofR', [-58, 7, 160.0, 0, 0], 22.0))"
bash $T/gd11r_capcases.sh $L "[dict(name='$L'+'_'+li+'_'+n+sfx, view='custom', cam=c, fov=f, garments=True, materials='real', light=li, animation=None, time=0, light_target_z=163, hide=h) for n, c, f in $CAMS for li in ('studio', 'grazing', 'front') for sfx, h in (('', []), ('_nobrow', ['Eyebrows']))]"
