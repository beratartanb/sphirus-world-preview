#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V244_20261101; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib244.sh
: manifests already made
: idle manifest already made
for S in L R; do
  out=$(SHME_KIND=write SHME_OWNER=v244 SHME_MANIFEST=$M/v244_lat.json bash $RUN $REQ/glat244_$S.py v244glat$S 1800)
  echo "[gen $S] skipped $(echo "$out" | grep -a -c G244L_SKIP) clamped $(echo "$out" | grep -a 'G244L_STEPS' | grep -a -c "\[('") ok $(echo "$out" | grep -a -c '^G244L ') $(echo "$out" | grep -a 'REFUSED\|Traceback\|Error:' | head -2 | cut -c1-200)" >> $O
done
"$PY" - <<'PYE' >> $O
import json
keep = []; rep = {}
for s in 'LR':
    try: d = json.load(open('Saved/Codex/SHME_V244_20261101/gen244_latstop_%s_write.json' % s))
    except Exception as e: print('[clips] no write json', s, e); continue
    for n, c in d['clips'].items():
        rep[n] = (c.get('saved'), c.get('planted_drift'), c.get('foot_err'), c.get('guard_fail', '')[:40])
        if c.get('saved') and c['planted_drift'] <= 8.0 and c['foot_err'] <= 8.0: keep.append('/Game/GraceRanger/SHME/Animations/V244/' + n)
open('Saved/Codex/SHME_V244_20261101/data/latstop244_clips.json', 'w').write(json.dumps(keep)); print('[clips] keep', len(keep), 'of', len(rep), 'rejected', [k for k, v in rep.items() if ('/Game/GraceRanger/SHME/Animations/V244/' + k) not in keep])
PYE
echo "[latdb] $(SHME_KIND=write SHME_OWNER=v244 SHME_MANIFEST=$M/v244_lat.json bash $RUN $REQ/ldb244_req.py v244ldb 900 | grep -a 'LDB244 \|REFUSED\|Error' | grep -o '"entries": \[[^]]*\]\|REFUSED.*\|Error.*' | cut -c1-900)" >> $O
echo "[idle] $(SHME_KIND=write SHME_OWNER=v244 SHME_MANIFEST=$M/v244_idle.json bash $RUN $REQ/gidle244.py v244gidle 900 | grep -a 'G244I \|REFUSED\|Error' | cut -c1-400)" >> $O
echo "[idledb] $(SHME_KIND=write SHME_OWNER=v244 SHME_MANIFEST=$M/v244_idle.json bash $RUN $REQ/idb244_req.py v244idb 600 | grep -a 'IDB244 \|REFUSED\|Error' | grep -o '"entries": \[[^]]*\]\|REFUSED.*\|Error.*' | cut -c1-300)" >> $O
echo GEN244_DONE >> $O
WARM=1 ab c1 "j41_rl_p04:lat4 j41_rl_p10:lat4 j42_lr_p10:lat4 w42_id:idl4 w43_idle:idl4 taps:idl4 jstart:idl4 j40_rlw:idl4 gait:idl4 j42_lr_p10:all4 taps:all4"
echo C1_DONE >> $O
