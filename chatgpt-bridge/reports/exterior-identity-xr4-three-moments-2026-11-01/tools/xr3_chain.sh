#!/bin/bash
# xr3_chain.sh <job> ... : XR3 identity-pass jobs (owner xr3). Reuses the XR2 chain for apply/look/views/walk/probe and adds:
#   board:<tag>:<clay|lit>          pie job - xr3_board.py asset lineup (runtime spawns only) -> scratchpad xr3/board_<tag>
#   id:<dryrun|apply|restore>:<var> write job (map manifest) - xr3_apply.py identity pass on top of the applied XR2 variant
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad"
SCW=$(cygpath -m "$SC"); WD=$(cygpath -m "$PWD"); D=Saved/Codex/ExteriorIdentity_XR3_20261031; M="Saved/Codex/SHME_V233_20261027/checkpoint/manifests/vmp_map.json"
T=Tools/ExteriorIdentity_XR3_20261031; mkdir -p $SC/xr3
waitst() { for i in $(seq 1 720); do grep -q -E '"state": "(done|error)"' "$1" 2>/dev/null && break; sleep 5; done; cat "$1"; echo; sleep 8; }
for j in "$@"; do
  IFS=: read -r k a b <<< "$j"
  case $k in
    board)
      O=$SC/xr3/board_$a; rm -rf "${O:?}"; C=""; [ "$b" = clay ] && C="'viewmode lightingonly'"
      printf "import builtins
builtins.XR3_MODE = 'spawn'
exec(compile(open(r'%s/$T/xr3_board_spawn.py', encoding='utf-8').read(), 'xr3_board_spawn.py', 'exec'), {'__name__': '__job__'})
" "$WD" > $SC/xr3/board_req.py
      echo "[board spawn] $(SHME_KIND=write SHME_OWNER=xr3 SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh $SC/xr3/board_req.py xr3bspawn 900 | tail -1 | cut -c1-200)"
      printf "import builtins, json
builtins.XR2_VIEWS = json.load(open(r'%s/$D/data/board_views.json'))
builtins.XR2_OUT = r'%s/xr3/board_%s'
builtins.XR2_CMDS = [%s]
exec(compile(open(r'%s/Tools/ExteriorWorld_XR2_20261031/xr2_views.py', encoding='utf-8').read(), 'xr2_views.py', 'exec'), {'__name__': '__job__'})
" "$WD" "$SCW" "$a" "$C" "$WD" > $SC/xr3/bviews_req.py
      echo "[board views $a $b] $(SHME_KIND=pie SHME_OWNER=xr3 bash Tools/SHME_V2_20261014/run_v2.sh $SC/xr3/bviews_req.py xr3bviews 120 | tail -1)"; waitst $O/views_status.json
      printf "import builtins
builtins.XR3_MODE = 'destroy'
exec(compile(open(r'%s/$T/xr3_board_spawn.py', encoding='utf-8').read(), 'xr3_board_spawn.py', 'exec'), {'__name__': '__job__'})
" "$WD" > $SC/xr3/board_req.py
      echo "[board destroy] $(SHME_KIND=write SHME_OWNER=xr3 SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh $SC/xr3/board_req.py xr3bdestroy 300 | tail -1 | cut -c1-200)";;
    id)
      printf "import builtins\nbuiltins.XR3_MODE = '%s'\nbuiltins.XR3_VARIANT = '%s'\nexec(compile(open(r'%s/$T/xr3_apply.py', encoding='utf-8').read(), 'xr3_apply.py', 'exec'), {'__name__': '__job__'})\n" "$a" "$b" "$WD" > $SC/xr3/id_req.py
      F=$D/design/id_${a}_$b.json; rm -f $F
      echo "[id $a $b] $(SHME_KIND=write SHME_OWNER=xr3 SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh $SC/xr3/id_req.py xr3id 600 | tail -1 | cut -c1-300)"
      for i in $(seq 1 120); do [ -f "$F" ] && break; sleep 3; done; head -c 500 "$F"; echo; grep -q '"ok": true' "$F" || { echo "ID FAILED - chain stops"; exit 1; };;
    *)
      SHME_OWNER=xr3 bash Tools/ExteriorWorld_XR2_20261031/xr2_chain.sh "$j" | grep -v XR2_CHAIN_DONE;;
  esac
done
echo XR3_CHAIN_DONE
