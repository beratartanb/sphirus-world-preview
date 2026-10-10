#!/bin/bash
# gd17_lookB.sh <face path> <binding tag> : GD17 reference look = the GD15 final look (read-only GD15 Looks): FlatThick brows auburn-dark (MI_GD15_BrowS_auburnDark)
# raised via brow source proxy unless CUSTOMBROW is set, S_Thin lashes, iris h6, skin s1t5 (f5 texture), body s1, hair h75c. Bindings / groom duplicates -> GD17 folder.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD17_Identity_20261010; L=/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks
DSK="$L/MI_GD15_Face_{lod}_${LB_SKIN:-s1t5}"; [ -n "${LB_SKINP:-}" ] && DSK="$LB_SKINP"
BROW=M_FlatThick BROWMAT=$L/MI_GD15_BrowS_auburnDark BROWDS=_sa EYE="$L/MI_GD15_Eye{s}_${LB_EYE:-h6}" SKIN="$DSK" BODY=$L/MI_GD15_Body_s1 bash $W/tools/gd17_look.sh "$1" "$2"
