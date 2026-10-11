#!/bin/bash
# gd38_evalchain.sh : evaluation assembly BP_GD38_Character_T38 + L_GD38_Eval_T38 (new names, refuses to overwrite), evalqa harness setup, captures
# of the saved level (refS + hs), pixel comparison with the harness captures of the same composition and rest pose (t38e_xlid60_ref), PIE readback.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD38_Identity_20261011; T=$N/tools; R=Tools/OutfitHome_20260929/run_of.sh; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
bash $T/gd38_memguard.sh 26 | tail -1
echo "== ASSEMBLY"; MSYS_NO_PATHCONV=1 bash $R "$(Wp $T/ue_gd38_assembly.py)" gd38-asm 1200 | grep -oE "GD38_ASSEMBLY_OK.*|Traceback.*|AssertionError.*|Error.*" | head -5
[ -f $N/data/assembly_check.json ] || { echo ASM_STOP; exit 2; }
echo "== EVALQA"; MSYS_NO_PATHCONV=1 bash $R "$(Wp $T/ue_gd38_evalqa.py)" gd38-evalqa 600 | grep -oE "GD38_EVALQA.*|LK_QA.*|Traceback.*|AssertionError.*" | head -5
echo "== BP CAPTURES"; bash $T/gd38_bpcaps.sh t38bp refS,hs | grep -E "DONE|ERROR|TIMEOUT"
echo "== CMP"; mkdir -p $N/bd/cmp; CMPB=t38e_xlid60_ref "$B" -b --factory-startup --python "$(Wp $T/gd38_cmp.py)" -- "$(Wp $N/ue)" "$(Wp $N/ue)" t38bp "$(Wp $N/data/cmp_bp_vs_harness.txt)" "$(Wp $N/bd/cmp)" 2>&1 | grep -iE "error|trace" | head -3; cat $N/data/cmp_bp_vs_harness.txt
echo "== PIE"; MSYS_NO_PATHCONV=1 bash $R "$(Wp $T/ue_gd38_pie.py)" gd38-pie 600 | grep -oE "GD38_PIE_DONE.*|Traceback.*" | head -3
sleep 20; "/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" -c "
import json; d=json.load(open('$N/data/pie_check.json')); r=d.get('readback',{}); print('PIE instances', d.get('n_instances'), 'error', d.get('error'))
for k,v in r.get('skeletal',{}).items(): print('  SK', k, v.get('mesh'), 'lod', v.get('predicted_lod'), v.get('anim_to_play',''), {c:round(x,2) for c,x in v.get('curves',{}).items()} if v.get('curves') else '')
for k,v in r.get('grooms',{}).items(): print('  GR', k, {a:b for a,b in v.items() if a in ('groom','binding','visible')})" 2>&1 | head -20
echo EVALCHAIN_DONE
