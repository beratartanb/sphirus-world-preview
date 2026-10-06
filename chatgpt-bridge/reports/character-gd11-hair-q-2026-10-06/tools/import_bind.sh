#!/bin/bash
# import_bind.sh <tag> : import an already built P hair tag into GD11_HairQ_20261006 and bind it to m2 (two jobs: create, re-save built)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; t=$1; T=Tools/CharacterLookdev_20260930
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/b05832b1-23f7-44dd-a92f-e1907201ea47/scratchpad"
SKIP_BUILD=1 bash $T/gd11rq_hair_cycle.sh $t x 2>&1 | grep -E "HAIR_DONE|Traceback|ERROR" | cut -c1-200
for rs in False True; do { echo "import builtins; builtins.G11RQ_BIND = {'tag': '$t', 'resave': $rs}"; cat $T/ue_g11rq_bind.py; } > "$SC/rq_bind_$t.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/rq_bind_$t.py" rqbind 1800 | grep -o "G11RQ_BIND.*\|Traceback.*\|Error.*" | cut -c1-420; done
ls -la Content/Sphirus/CharacterLab/GD11_HairQ_20261006/Face/Bindings/ | grep "m2$t" | awk '{print $5, $9}'
