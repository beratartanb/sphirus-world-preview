#!/bin/bash
# pfr_chain.sh <job> [<job> ...] : Pine Forest redesign editor jobs through the gated runner (owner pfr, lock held by this session).
#   views:<tag>:<lit|clay>:<stations.json>   pie job - xr2_views.py (real player camera, HighResShot 1920x1080) -> Saved/Codex/PineForestRedesign_20261104/cap/views_<tag>
#   walk:<tag>:<A|B>:<lit|clay>:<csv 0|1>     pie job - xr_walk.py along route A / B, game camera frames (JPG) at real speed -> cap/walk_<tag>
#   job:<kind>:<script.py>[:<timeout>]        any job of kind measure|pie|control|write (write needs PFR_MANIFEST)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad"
MY="/c/Users/berat/AppData/Local/Temp/claude/bbc6f8fdff1f8341/58bc34ab-b0fd-4574-9259-4850d781d32b/scratchpad"; mkdir -p "$MY/pfr"
WD=$(cygpath -m "$PWD"); D=Saved/Codex/PineForestRedesign_20261104; DW=$(cygpath -m "$PWD/$D"); T=Tools/PineForestRedesign_20261104
M="${PFR_MANIFEST:-Saved/Codex/SHME_V233_20261027/checkpoint/manifests/pfr_map.json}"
waitst() { for i in $(seq 1 1200); do grep -q -E '"state": "(done|error)"' "$1" 2>/dev/null && break; sleep 5; done; cat "$1"; echo; sleep 6; }
for j in "$@"; do
  IFS=: read -r k a b c d <<< "$j"
  case $k in
    views)
      # HighResShot cannot write to a path with spaces (project folder): stills go to the scratchpad, then are copied into the pass folder
      O=$MY/pfr/views_$a; rm -rf "${O:?}"; mkdir -p "$O"; OW=$(cygpath -m "$O"); C=""; [ "$b" = clay ] && C="'viewmode lightingonly'"
      printf "import builtins, json\nbuiltins.XR2_VIEWS = json.load(open(r'%s/%s'))\nbuiltins.XR2_OUT = r'%s'\nbuiltins.XR2_CMDS = [%s]\nexec(compile(open(r'%s/Tools/ExteriorWorld_XR2_20261031/xr2_views.py', encoding='utf-8').read(), 'xr2_views.py', 'exec'), {'__name__': '__job__'})\n" "$WD" "$c" "$OW" "$C" "$WD" > "$MY/pfr/views_req.py"
      echo "[views $a $b] $(SHME_KIND=pie SHME_OWNER=pfr bash Tools/SHME_V2_20261014/run_v2.sh "$MY/pfr/views_req.py" pfrviews 120 | tail -1 | cut -c1-200)"; waitst "$O/views_status.json"
      rm -rf "$D/cap/views_$a"; mkdir -p "$D/cap"; cp -r "$O" "$D/cap/views_$a"; echo "copied $(ls "$D/cap/views_$a" | grep -c png) stills";;
    walk)
      IFS=: read -r k a r v c <<< "$j"; O=$D/cap/walk_$a; rm -rf "${O:?}"; mkdir -p "$O"; C=""; [ "$v" = clay ] && C="'viewmode lightingonly'"; PB=False; [ "$c" = 1 ] && PB=True
      TR=$("/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" -I -c "import sys;sys.path.insert(0,'Tools/ExteriorWorld_XR2_20261031');import xr2_layout as L;R=L.ROUTE_A if '$r'=='A' else L.ROUTE_B;print(R, L.poly_len(R))")
      PTS=${TR% *}; LEN=${TR##* }
      printf "import builtins\nbuiltins.TRAILWALK_OUT = r'%s/cap/walk_%s'\nbuiltins.XR_TRAIL = %s\nbuiltins.TRAILWALK_S0 = 0.001\nbuiltins.TRAILWALK_SEG = %s\nbuiltins.TRAILWALK_STATIONS = []\nbuiltins.TRAILWALK_PANS = ()\nbuiltins.XR_HOUSE_STATIONS = ()\nbuiltins.XR_CMDS = [%s]\nbuiltins.XR_PASSB = %s\nexec(compile(open(r'%s/Tools/ExteriorRedesign_20261031/xr_walk.py', encoding='utf-8').read(), 'xr_walk.py', 'exec'), {'__name__': '__job__'})\n" "$DW" "$a" "$PTS" "$LEN" "$C" "$PB" "$WD" > "$MY/pfr/walk_req.py"
      echo "[walk $a $r $v csv$c] $(SHME_KIND=pie SHME_OWNER=pfr bash Tools/SHME_V2_20261014/run_v2.sh "$MY/pfr/walk_req.py" pfrwalk 120 | tail -1 | cut -c1-200)"; waitst "$O/trailwalk_status.json";;
    job)
      TO=${d:-600}
      if [ "$a" = write ]; then echo "[job write $b] $(SHME_KIND=write SHME_OWNER=pfr SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh "$b" pfr_$(basename "$b" .py) "$TO" | head -c 1500)"
      else echo "[job $a $b] $(SHME_KIND=$a SHME_OWNER=pfr bash Tools/SHME_V2_20261014/run_v2.sh "$b" pfr_$(basename "$b" .py) "$TO" | head -c 1500)"; fi;;
  esac
done
echo PFR_CHAIN_DONE
