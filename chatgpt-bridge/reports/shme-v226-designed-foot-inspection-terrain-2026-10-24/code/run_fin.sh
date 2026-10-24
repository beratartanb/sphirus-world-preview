#!/bin/bash
# V2.26 final chain (sequential). Decisions come from the environment when started:
#   REV=rv32|none      reversal candidate to sweep / promote (PSD_SHM226 databases)
#   TER=m6|te6|none    terrain candidate (m6 = T3g lift margin 6; te6 = + landing shift)
#   ZOOM=0|1           InspectZoomOn promotion (B = 0, C = 1)
# Stages: 1 FPS sweeps (20 / 60 / 120, fixed step) of the chosen reversal vs production | 2 real time: cold start (no warm-up), hitch run,
# second request | 3 promotion -> clean reopen verify -> final evidence in production mode (fixed 30 + real time) | 4 full-frame captures
O=Saved/Codex/SHME_V226_20261024/run_fin.out; source "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V226_20261024/lib226.sh"
REV=${REV:-none}; TER=${TER:-none}; ZOOM=${ZOOM:-0}
echo "FIN start $(date +%T) REV=$REV TER=$TER ZOOM=$ZOOM" >> $O
RV=""; [ "$REV" != none ] && RV="j24_ph0:$REV j24_sw_ph2:$REV j24_ph3:$REV"
# ---- 0 terrain pre-stage: the landing shift on the real routes (must stay silent on rolling ground) -> TER decision te6x / m6
if [ "$TER" = auto ]; then
  export WARM=1; relaunch pre 30; ab pre "map_r1:te6x map_r2:te6x map_r3:te6x ter_drop_walk:te6x ter_drop_jog:te6x ter_step2:te6x"
  TER=$("$PY" - <<'PYX'
import json
E='Saved/Codex/SHME_V1_20260925/Evidence/'; mx=0.0
for lab in ('v226pre_map_r1_te6x_r1','v226pre_map_r2_te6x_r1','v226pre_map_r3_te6x_r1'):
    try: R=[r for r in json.load(open(E+lab+'.json')) if isinstance(r,dict) and r.get('t') is not None]
    except Exception: print('m6'); raise SystemExit
    for r in R:
        for k in ('cv_SwingShiftTL','cv_SwingShiftTR'):
            try: mx=max(mx,abs(float(r.get(k) or 0)))
            except Exception: pass
print('te6x' if mx < 1.0 else 'm6')
PYX
)
  echo "TER decided: $TER" >> $O
fi
# ---- 1 FPS sweeps
for F in 20 60 120; do
  export WARM=1; relaunch f$F $F
  ab s$F "j24_ph0:o j24_sw_ph2:o j24_ph3:o $RV j24_ovl120:o ${REV:+j24_ovl120:$REV}"
done
echo S_DONE >> $O
# ---- 2 real time: cold start (first run after a fresh editor, no warm-up), hitch, second request
relaunch rt real; export WARM=0
ab cold "j24_ph0:${REV/none/o}"
export WARM=1
ab rt "j24_sw_ph2:${REV/none/o} j24_dbl:${REV/none/o} j24_rel:${REV/none/o} ins_ws:o ter_drop_walk:${TER/none/o}"
echo RT_DONE >> $O
# ---- 3 promotion + verify + final evidence
relaunch pr 30
bash $R $D/req/probes_remove.py prm 600 > $D/probes_remove_fin.out 2>&1; bash $R $D/req/probes_r12.py pr12 600 > $D/probes_r12_fin.out 2>&1; grep -aE "PROBE226|Traceback" $D/probes_r12_fin.out | cut -c1-600 >> $O
"$PY" - <<PYX > $D/req/promo_fin.py
import json
extra = {} if '$TER' == 'none' else ({'SwingLiftMargin': 6.0, 'StepEdgeMin': 10.0} if '$TER' == 'te6x' else {'SwingLiftMargin': 6.0})
extra['InspectRadius'] = 12.0   # 12 cm gaze query + 12 cm probe spheres: two masks 29 cm apart separable
d = {'StepPrep': False, 'Inspect': True, 'InspectZoom': bool(int('$ZOOM')), 'Reversal226': '$REV' == 'rv32', 'StepEdge': '$TER' in ('te6', 'te6x')}
print("import builtins\nbuiltins.V226_PROMO = %r\nbuiltins.V226_PROMO_SAVE = True\nbuiltins.V226_PROMO_EXTRA = %r\nexec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/promote226.py', encoding='utf8').read(), {'__name__': 'p226'})" % (d, extra))
PYX
bash $R $D/req/promo_fin.py promo 600 > $D/promo_fin.out 2>&1; grep -aE "PROMO226|Traceback" $D/promo_fin.out | cut -c1-1500 >> $O
grep -q '"saved": true' $D/promo_fin.out || { echo PROMO_FAILED >> $O; exit 1; }
relaunch vf 30
"$PY" - <<PYX > $D/req/verify_fin.py
print("import builtins\nbuiltins.V225_EXP = {'Reversal': False, 'StepPrepEnabled': False, 'CamInspectEnabled': True}\nbuiltins.V226_EXP = {'Reversal226': %r, 'StepEdgeOn': %r, 'InspectZoomOn': %r, 'Probes': True, 'SwingLiftMargin': ('$TER' != 'none') and 6.0 or 10.5}\nexec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/verify_prod226.py', encoding='utf8').read(), {'__name__': 'v226'})" % ('$REV' == 'rv32', '$TER' in ('te6', 'te6x'), bool(int('$ZOOM'))))
PYX
bash $R $D/req/verify_fin.py verify 600 > $D/verify_fin.out 2>&1; grep -aE "ALL_OK|NOT_OK|Traceback" $D/verify_fin.out | cut -c1-400 >> $O
relaunch fin 30; export WARM=1
ab fin "j24_sw_ph0:o j24_sw_ph2:o j24_ph0:o j24_ph3:o j24_rel:o j24_dbl:o j24_ad_ph0:o j24_m180w:o j23_m180:o r_cutrev_r:o s23_jstart:o taps:o ins_ws:o ins_ws2:o ins_qa:o ter_drop_walk:o ter_drop_walkB:o ter_drop_jog:o ter_step2:o ter_bump_walk:o d_walk:o d_jog:o map_r1:o map_r2:o map_r3:o"
relaunch finrt real; export WARM=0
ab finrt "map_r2:o"
echo FIN_EVIDENCE_DONE >> $O
# ---- 4 full-frame captures (viewport fitted to a multiple of 64)
relaunch cap 30; export WARM=1 CAPV="o"
capf() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); export CAP_START=$1 CAP_SECS=$2; TAG=$3 JOBS="$4" EXTRA_VARS="$(cat $D/vars226.sh; cat $D/req/cap226.sh)" bash Tools/SHME_V226_20261024/ab_safe226.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE" >> $O; }
capf 3.6 7.0 capfin "j24_sw_ph2:oS j24_sw_ph2:oG j24_ph3:oS j24_ph0:oD"
capf 3.0 8.0 capfin "ins_ws:oG ins_ws:oD ins_ws2:oG"
capf 10.5 6.0 capfin "ter_drop_walk:oS ter_drop_walk:oG"
capf 3.0 12.0 capfin "map_r2:oG"
echo CAP_DONE >> $O
echo FIN_DONE >> $O
