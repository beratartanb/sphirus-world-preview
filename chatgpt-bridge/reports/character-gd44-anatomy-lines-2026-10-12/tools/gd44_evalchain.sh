#!/bin/bash
# gd44_evalchain.sh : body-review assembly BP_GD44_Character_Body + L_GD44_Eval_Body (no garments), evalqa harness on the saved level, full-body
# captures of the saved BP (CAM_BODY_*), pixel comparison with the harness captures of the same composition (body region), PIE readback.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD44_Lines_20261012; T=$N/tools; R=Tools/OutfitHome_20260929/run_of.sh; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
bash Saved/Codex/GD38_Identity_20261011/tools/gd38_memguard.sh 26 | tail -1
echo "== ASSEMBLY"; MSYS_NO_PATHCONV=1 bash $R "$(Wp $T/ue_gd44_assembly.py)" gd44-asm 1200 | grep -oE "GD44_ASSEMBLY_OK.*|Traceback.*|AssertionError.*|Error.*" | head -5
[ -f $N/data/assembly_check.json ] || { echo ASM_STOP; exit 2; }
echo "== EVALQA"; MSYS_NO_PATHCONV=1 bash $R "$(Wp $T/ue_gd44_evalqa.py)" gd44-evalqa 600 | grep -oE "GD44_EVALQA.{0,300}|Traceback.*|AssertionError.*" | head -3
echo "== BP CAPTURES"; bash $T/gd44_bpcaps.sh g44bp body | grep -E "DONE|ERROR|TIMEOUT"
echo "== CMP"; "$B" -b --factory-startup --python-expr "
import sys, glob; sys.path.insert(0, r'$(Wp Saved/Codex/GD13_Identity_20261009/tools)'); import gd13_img as gi, numpy as np
U=r'$(cygpath -m "$(pwd)/$N/ue")'; bp=sorted(glob.glob(U+'/g44bp_body_front_custom*.png')); hs=sorted(glob.glob(U+'/g44_real_front_after*.png')); print('CMPFILES', [f.rsplit('/',1)[-1] for f in bp+hs])
A=gi.load(bp[0])[...,:3]; H=gi.load(hs[0])[...,:3]; r=(slice(420,1560), slice(450,1150)); d=np.abs(A[r]-H[r]); print('CMP body region (z<~150 cm) mean |d| %.4f p95 %.4f px>0.05 %.2f %%' % (d.mean(), np.percentile(d,95), 100*(d.max(-1)>0.05).mean()))
gi.save(U+'/../r/cmp_bp_vs_harness_front.png', np.concatenate([A[r], H[r], np.clip(d*5,0,1)],1)); print('CMP_OK')" 2>&1 | grep -E "CMP"
echo "== PIE"; MSYS_NO_PATHCONV=1 bash $R "$(Wp $T/ue_gd44_pie.py)" gd44-pie 600 | grep -oE "GD44_PIE_DONE.*|Traceback.*" | head -3
sleep 20; "/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" -c "
import json; d=json.load(open('$N/data/pie_check.json')); r=d.get('readback',{}); print('PIE instances', d.get('n_instances'), 'error', d.get('error'))
for k,v in r.get('skeletal',{}).items(): print('  SK', k, v.get('mesh'), 'lod', v.get('predicted_lod'), v.get('anim_to_play',''), {c:round(x,2) for c,x in v.get('curves',{}).items()} if v.get('curves') else '')
for k,v in r.get('grooms',{}).items(): print('  GR', k, {a:b for a,b in v.items() if a in ('groom','binding','visible')})" 2>&1 | head -12
echo EVALCHAIN_DONE
