#!/bin/bash
# navsheet.sh <session> <step nn> <tag> : L | C | R strip of one navigation look -> scratchpad xr2/nav_<session>/strip_<nn>.png
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/xr2/nav_$1"
bash "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/ExteriorWorld_XR2_20261031/sheet.sh" $SC/strip_$2.png 3 640 "adim $2 ($3): sol -55 | orta | sag +55" $SC/nav$2_$3_L.png:"sol" $SC/nav$2_$3_C.png:"orta" $SC/nav$2_$3_R.png:"sag" | tail -1 | cut -c1-20
