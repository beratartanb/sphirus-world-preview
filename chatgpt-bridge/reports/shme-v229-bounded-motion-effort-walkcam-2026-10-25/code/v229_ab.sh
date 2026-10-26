#!/bin/bash
# v226_ab.sh : V2.26 A/B driver. base "o" = the SAVED PRODUCTION run in qa_pie state_mode "production" (no flags of any kind); every other
# variant is state_mode "candidate" = production + its explicit AF (abp_flags) / SX (shme_flags) / BF (behavior_flags) / PF (pbi_flags) /
# CON (console + extra request keys). Variants come from EXTRA_VARS (bash; declare MODE/AF/SX/BF/PF/CON maps). Runs whose effective state
# differs between start and end are reported INVALID_STATE by qa_pie (summary line shows it).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; V212=Tools/SHME_V212_20261017; L=Saved/Codex/SHME_V229_20261025/ab_$(date +%H%M%S).log
ON='"console":["a.AnimNode.OrientationWarping.Enable 1","a.AnimNode.StrideWarping.Enable 1","a.AnimNode.FootPlacement.Enable 1","a.AnimNode.LegIK.Enable 1"]'
declare -A BF SX PF AF PRE POST CON MODE
MODE[o]=production; AF[o]=""; SX[o]="{}"; BF[o]=""; PF[o]=""; CON[o]="$ON"
[ -n "$EXTRA_VARS" ] && eval "$EXTRA_VARS"
TAG="${TAG:-a}"
source $V21/v21_lib.sh; MG=0; REL=0
req_extra() { local v=$1; local x=",\"state_mode\":\"${MODE[$v]:-candidate}\""; [ -n "${BF[$v]}" ] && x="$x,\"behavior_flags\":{${BF[$v]}}"; [ -n "${PF[$v]}" ] && x="$x,\"pbi_flags\":{${PF[$v]}}"; [ -n "${AF[$v]}" ] && x="$x,${AF[$v]}"; x="$x,${CON[$v]:-$ON}"; echo "$x"; }
warm() { bash $V212/v212_run.sh "v212_warm_$(date +%H%M%S)" wdiag "{}" "$(req_extra o)" 2>&1 | tail -1 | tee -a "$L"; }
[ -n "$WARM" ] && [ "$WARM" != 0 ] && warm
for J in $JOBS; do IFS=: read SC VA RP <<< "$J"; RP=${RP:-1}
  [ -z "${MODE[$VA]}" ] && [ "$VA" != o ] && { echo "UNKNOWN VARIANT $VA" | tee -a "$L"; continue; }
  LBL="v229${TAG}_${SC}_${VA}_r$RP"; [ -n "$RESUME" ] && [ -f "Saved/Codex/SHME_V212_20261017/Reports/$LBL.txt" ] && continue
  for TRY in 1 2; do
    echo "== $LBL $(date +%T)" | tee -a "$L"
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w Tools/SHME_V218_20261019/unminimize.ps1)" 2>/dev/null | tee -a "$L"
    [ -n "${PRE[$VA]}" ] && bash $V2/run_v2.sh "${PRE[$VA]}" "pre_$VA" 300 | grep -a -E "^PRE|PRE[A-Z0-9_]* " | tail -1 | tee -a "$L"
    bash $V212/v212_run.sh "$LBL" "$SC" "${SX[$VA]:-{\}}" "$(req_extra $VA)" 2>&1 | tail -1 | tee -a "$L"
    [ -n "${POST[$VA]}" ] && bash $V2/run_v2.sh "${POST[$VA]}" "post_$VA" 300 | grep -a -E "^POST|POST[A-Z0-9_]* " | tail -1 | tee -a "$L"
    tasklist 2>/dev/null | grep -qi UnrealEditor.exe && { MG=$((MG+1)); mem_guard "$L" a$MG warm || exit 1; break; }
    echo "EDITOR_GONE after $LBL" | tee -a "$L"; REL=$((REL+1)); [ $REL -gt 5 ] && { echo "TOO_MANY_RELAUNCHES" | tee -a "$L"; exit 1; }
    bash $V2/v2_editor_launch.sh "shmv226_r$REL" 2>&1 | tail -2 | tee -a "$L"
    tasklist 2>/dev/null | grep -qi UnrealEditor.exe || { echo "RELAUNCH_FAILED" | tee -a "$L"; exit 1; }
    export LR_LOG="shmv226_r$REL.log"; warm
  done
done
echo "AB226_DONE $(date +%T)" | tee -a "$L"
