#!/bin/bash
# xr2_chain.sh <job> [<job> ...] : XR2 editor jobs in order through the gated runner (owner xr2, single lock).
#   look:<NEUTRAL|restore|V1|V2|V3>      write job (map manifest) - look_variant.py on the existing look owners, in memory
#   apply:<dryrun|apply|restore>:<var>   write job (map manifest) - xr2_apply.py; the chain stops when it does not report ok
#   probe:<tag>                          pie job - xr2_probe.py with data/probes.json -> cap/probe_<tag>
#   views:<tag>:<clay|lit>               pie job - xr2_views.py with data/views.json -> scratchpad xr2/views_<tag>
#   walk:<tag>:<A|B>:<clay|lit>:<csv 0|1>  pie job - R1 xr_walk.py along route A (veranda -> glade) or B (house SE -> saddle): game-camera
#                                        frames (video) at normal speed; csv 1 adds the csvprofile pass -> scratchpad xr2/walk_<tag>
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad"
SCW=$(cygpath -m "$SC"); WD=$(cygpath -m "$PWD"); D=Saved/Codex/ExteriorWorld_XR2_20261031; M="Saved/Codex/SHME_V233_20261027/checkpoint/manifests/vmp_map.json"
T=Tools/ExteriorWorld_XR2_20261031; mkdir -p $SC/xr2
waitst() { for i in $(seq 1 720); do grep -q -E '"state": "(done|error)"' "$1" 2>/dev/null && break; sleep 5; done; cat "$1"; echo; sleep 10; }
for j in "$@"; do
  IFS=: read -r k a b <<< "$j"
  case $k in
    look)
      if [ "$a" = NEUTRAL ] || [ "$a" = TRIAL2 ]; then cp $SC/look_${a}_req.py $SC/xr2/look_req.py; else printf "import builtins\nbuiltins.LOOK_VARIANT = '%s'\nexec(compile(open(r'%s/Tools/AIToolingEval_20261031/look_variant.py', encoding='utf-8').read(), 'look_variant.py', 'exec'), {'__name__': '__job__'})\n" "$a" "$WD" > $SC/xr2/look_req.py; fi
      echo "[look $a] $(SHME_KIND=write SHME_OWNER=xr2 SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh $SC/xr2/look_req.py xr2look 600 | tail -1 | cut -c1-200)";;
    apply)
      ST=build; SK=False; [ "$a" = dress ] && { a=apply; ST=dress; }; [ "$a" = resume ] && { a=apply; SK=True; }
      printf "import builtins\nbuiltins.XR2_MODE = '%s'\nbuiltins.XR2_VARIANT = '%s'\nbuiltins.XR2_STAGE = '$ST'\nbuiltins.XR2_SKIP_HEIGHT = $SK\nexec(compile(open(r'%s/$T/xr2_apply.py', encoding='utf-8').read(), 'xr2_apply.py', 'exec'), {'__name__': '__job__'})\n" "$a" "$b" "$WD" > $SC/xr2/apply_req.py
      F=$D/design/apply_${a}_$b.json; rm -f $F
      echo "[apply $a $b] $(SHME_KIND=write SHME_OWNER=xr2 SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh $SC/xr2/apply_req.py xr2apply 600 | tail -1 | cut -c1-300)"
      for i in $(seq 1 120); do [ -f "$F" ] && break; sleep 3; done; head -c 700 "$F"; echo
      grep -q '"ok": true' "$F" || { echo "APPLY FAILED - chain stops"; exit 1; };;
    probe)
      O=$D/cap/probe_$a; rm -rf $O
      printf "import builtins, json\nbuiltins.XR2_PROBES = json.load(open(r'%s/$D/data/probes.json'))\nbuiltins.XR2_OUT = r'%s/$O'\nbuiltins.XR2_DIL = 4.0\nexec(compile(open(r'%s/$T/xr2_probe.py', encoding='utf-8').read(), 'xr2_probe.py', 'exec'), {'__name__': '__job__'})\n" "$WD" "$WD" "$WD" > $SC/xr2/probe_req.py
      echo "[probe $a] $(SHME_KIND=pie SHME_OWNER=xr2 bash Tools/SHME_V2_20261014/run_v2.sh $SC/xr2/probe_req.py xr2probe 120 | tail -1)"; waitst $O/probe_status.json;;
    views)
      O=$SC/xr2/views_$a; rm -rf $O; C=""; [ "$b" = clay ] && C="'viewmode lightingonly'"
      printf "import builtins, json\nbuiltins.XR2_VIEWS = json.load(open(r'%s/$D/data/'+('views_sub.json' if '$a'.startswith('dress') or '$a'.startswith('cine') else 'views.json')))\nbuiltins.XR2_OUT = r'%s/xr2/views_%s'\nbuiltins.XR2_CMDS = [%s]\nexec(compile(open(r'%s/$T/xr2_views.py', encoding='utf-8').read(), 'xr2_views.py', 'exec'), {'__name__': '__job__'})\n" "$WD" "$SCW" "$a" "$C" "$WD" > $SC/xr2/views_req.py
      echo "[views $a $b] $(SHME_KIND=pie SHME_OWNER=xr2 bash Tools/SHME_V2_20261014/run_v2.sh $SC/xr2/views_req.py xr2views 120 | tail -1)"; waitst $O/views_status.json;;
    walk)
      IFS=: read -r k a r v c <<< "$j"; O=$SC/xr2/walk_$a; rm -rf $O; C=""; [ "$v" = clay ] && C="'viewmode lightingonly'"; PB=False; [ "$c" = 1 ] && PB=True
      TR=$("/c/Program Files/Blender Foundation/Blender 5.2/5.2/python/bin/python.exe" -c "import sys;sys.path.insert(0,'$T');import xr2_layout as L;R=L.ROUTE_A if '$r'=='A' else L.ROUTE_B;print(R, L.poly_len(R))")
      PTS=${TR% *}; LEN=${TR##* }
      printf "import builtins
builtins.TRAILWALK_OUT = r'%s/xr2/walk_%s'
builtins.XR_TRAIL = %s
builtins.TRAILWALK_S0 = 0.001
builtins.TRAILWALK_SEG = %s
builtins.TRAILWALK_STATIONS = []
builtins.TRAILWALK_PANS = ()
builtins.XR_HOUSE_STATIONS = ()
builtins.XR_CMDS = [%s]
builtins.XR_PASSB = %s
exec(compile(open(r'%s/Tools/ExteriorRedesign_20261031/xr_walk.py', encoding='utf-8').read(), 'xr_walk.py', 'exec'), {'__name__': '__job__'})
" "$SCW" "$a" "$PTS" "$LEN" "$C" "$PB" "$WD" > $SC/xr2/walk_req.py
      echo "[walk $a $r $v csv$c] $(SHME_KIND=pie SHME_OWNER=xr2 bash Tools/SHME_V2_20261014/run_v2.sh $SC/xr2/walk_req.py xr2walk 120 | tail -1)"; waitst $O/trailwalk_status.json;;
  esac
done
echo XR2_CHAIN_DONE
