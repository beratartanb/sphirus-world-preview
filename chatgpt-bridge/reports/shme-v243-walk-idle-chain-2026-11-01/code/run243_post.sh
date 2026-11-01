#!/bin/bash
# after I5: regenerate the lateral family with a real closing-step lift (close_apex 8 / apex_min 6; FootPlacement held the 4 cm close step as planted -> 32 cm pop), rebuild DB, re-test p10, then 60 FPS + real time for latgl and idlg, back to 30.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V243_20261101; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
for i in $(seq 1 120); do grep -q I5_DONE $D/chain.out 2>/dev/null && break; sleep 30; done; sleep 15
source $D/lib243.sh
echo "[gen L2] $(SHME_KIND=write SHME_OWNER=v243 SHME_MANIFEST=$M/v243_lat.json bash Tools/SHME_V2_20261014/run_v2.sh /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243/glat_write_L2.py v243glatL 1200 | grep -a -c G242L_SKIP) skipped" >> $O
echo "[gen R2] $(SHME_KIND=write SHME_OWNER=v243 SHME_MANIFEST=$M/v243_lat.json bash Tools/SHME_V2_20261014/run_v2.sh /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243/glat_write_R2.py v243glatR 1200 | grep -a -c G242L_SKIP) skipped" >> $O
"$PY" - <<'PYE'
import json
keep = []
for s in 'LR':
    d = json.load(open('Saved/Codex/SHME_V242_20261101/gen242_latstop_%s_write.json' % s))
    for n, c in d['clips'].items():
        if c.get('saved') and c['planted_drift'] <= 8.0 and c['foot_err'] <= 8.0: keep.append('/Game/GraceRanger/SHME/Animations/V242/' + n)
open('Saved/Codex/SHME_V242_20261101/data/latstop_LR_clips.json', 'w').write(json.dumps(keep)); print('keep', len(keep))
PYE
echo "[DB] $(SHME_KIND=write SHME_OWNER=v243 SHME_MANIFEST=$M/v243_lat.json bash Tools/SHME_V2_20261014/run_v2.sh /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/ldb_req_LR.py v243ldb 600 | grep -a -c 'LDB242 ') built" >> $O
WARM=1 ab t2 "j41_rl_p10:latgl j41_rl_p04:latgl j42_lr_p10:latgl"
relaunch f60 60; WARM=1 ab f60 "j41_rl_p04:o j41_rl_p04:latgl w42_id:idlg w42_id:o"
relaunch freal real; WARM=1 ab freal "j41_rl_p04:latgl w42_id:idlg"
relaunch fend 30
echo POST243_DONE >> $O
