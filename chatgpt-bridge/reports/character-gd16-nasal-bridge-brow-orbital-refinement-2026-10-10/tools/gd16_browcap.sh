#!/bin/bash
# gd16_browcap.sh <brow tag> <face tag> <sets> [width] : import + bind custom brow brow/<tag>/brow_main.abc to GD16/Face/SKM_GD16_Face_<face tag>, compose the GD16
# reference look with that brow (CUSTOMBROW) and capture label c<face tag><brow tag> (front light)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD16_Identity_20261010; G=/Game/Sphirus/CharacterLab/GD16_IdentityMaster_20261010; BT=$1; FT=$2; Wp() { cygpath -w "$(pwd)/$1"; }
FACE=$G/Face/SKM_GD16_Face_$FT
{ echo "import builtins; builtins.GD16_BROW = {'abc': r'$(Wp $W/brow/$BT/brow_main.abc)', 'tag': '$BT', 'face': '$FACE', 'facetag': '$FT', 'width': ${4:-0.011}, 'tip': ${5:-0.6}, 'shadow': 1.0, 'mi': '/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_BrowS_auburnDark'}"; cat $W/tools/ue_gd16_brow_import.py; } > $W/jobs/browimp_${BT}_$FT.py
MSYS_NO_PATHCONV=1 bash Tools/OutfitHome_20260929/run_of.sh $W/jobs/browimp_${BT}_$FT.py gd16-browimp-$BT 900 | grep -oE "GD16_BROW.{0,300}|Traceback.*|AssertionError.*"
CUSTOMBROW=$G/Grooms/GR_GD16_BrowCustom_$BT CUSTOMBROW_BIND=$G/Face/Bindings/GB_GD16_EyebrowsCustom_${BT}_$FT bash $W/tools/gd16_lookB.sh $FACE ${FT}cb 2>&1 | grep -E "COMP|READY|Trace" | cut -c1-200
LIGHT=front bash $W/tools/gd16_caps.sh c$FT$BT ${3:-refnh,ref} | grep -E "DONE|ERROR"
