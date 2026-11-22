#!/bin/bash
# run1.sh <label> <x> <y> <z> <yaw> <plan> [extra prelude] : one recording on the CURRENT map with the saved player (no profile override),
# new recorder fields (vidm_patch). VSHOT=1 keeps screenshots (video); default data-only real time. VSIDE="(d,ang,h,..)" diagnostic camera.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; export VWAIT=${VWAIT:-1500}
rm -f "Saved/Codex/Grip_20261106/rec/$1.json"   # a stale json made vc59 stop PIE at once (recorder left registered)
USHA=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40)
NS0="import builtins; builtins.VID_MOTION={}; builtins.VID_ABP={}; builtins.VID_CAM={}; builtins.VIDC_CAMVARS=(); builtins.VID_BODY={}; builtins.VID_BODYSEQ={}; builtins.VID_PAWN={}; builtins.VID_REFPOSE=None; builtins.VID_NECK=True; builtins.VID_VARDT=None; builtins.VID_NODIL=False; builtins.VID_DILMAX=4.0; builtins.VID_TICKHOOK=None; "
[ -n "$VSIDE" ] && NS0="${NS0}builtins.VID_SIDE=$VSIDE; " || NS0="${NS0}builtins.VID_SIDE=None; "
[ -n "$VSHOT" ] && NS0="${NS0}builtins.VID_NOSHOT=False; builtins.VID_DIL=False; builtins.VID_FPS=30.0; " || NS0="${NS0}builtins.VID_NOSHOT=True; builtins.VID_DIL=True; builtins.VID_FPS=${DFPS:-60.0}; "
bash Tools/UE59_20261118/vc59.sh "$1" $2 $3 $4 $5 "$6" "${NS0}${7:-pass}" 2>&1 | grep -E "VIDREC|FRAMES|mp4|LOADSLOT"
h=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); [ "$h" = "$USHA" ] && echo "SLOT_OK $h" || echo "SLOT_CHANGED $h"
ls -la Saved/Codex/Grip_20261106/rec/$1.json 2>/dev/null | awk '{print $5,$9}'
