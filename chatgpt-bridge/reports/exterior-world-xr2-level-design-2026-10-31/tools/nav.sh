#!/bin/bash
# nav.sh <session tag> <cmd> [args] : one player-view navigation command (xr2_nav.py); waits for it and prints the result.
#   start x y yaw | look tag | go yaw metres | turn yaw | stop        stills land in scratchpad xr2/nav_<session>
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad"
S=$1; shift; O=$SC/xr2/nav_$S; mkdir -p $O; WD=$(cygpath -m "$PWD"); OW=$(cygpath -m "$O")
case $1 in start) A="('start', $2, $3, $4)"; K=pie;; tp) A="('start', $2, $3, $4)"; K=control;; look) A="('look', '$2')"; K=control;; go) A="('go', $2, $3)"; K=control;; turn) A="('turn', $2)"; K=control;; cmd) A="('cmd', '$2 $3')"; K=control;; stop) A="('stop',)"; K=control;; esac
printf "import builtins\nbuiltins.XR2_NAV_OUT = r'%s'\nbuiltins.XR2_NAV_CMD = %s\nexec(compile(open(r'%s/Tools/ExteriorWorld_XR2_20261031/xr2_nav.py', encoding='utf-8').read(), 'xr2_nav.py', 'exec'), {'__name__': '__job__'})\n" "$OW" "$A" "$WD" > $SC/xr2/nav_req.py
rm -f $O/nav_status.json
SHME_KIND=$K SHME_OWNER=xr2 bash Tools/SHME_V2_20261014/run_v2.sh $SC/xr2/nav_req.py xr2nav 120 | tail -1 | cut -c1-120
for i in $(seq 1 240); do grep -q -E '"state": "(ready|stopped|error)"' $O/nav_status.json 2>/dev/null && break; sleep 2; done
"/c/Program Files/Blender Foundation/Blender 5.2/5.2/python/bin/python.exe" -c "
import json,sys;d=json.load(open(sys.argv[1]));l=d.get('last') or {};l.pop('path',None);print(d['state'],json.dumps(l),d.get('err',''))" $O/nav_status.json
