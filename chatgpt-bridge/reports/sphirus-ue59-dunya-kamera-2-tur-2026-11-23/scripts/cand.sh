#!/bin/bash
# cand.sh <tag> <views file> '<python dict for builtins.R2G_W>' [PRE console/py snippet]: apply an in-memory candidate, tour, nothing saved.
P="<PROJECT_ROOT>"; cd "$P"; T=Tools/R2G2_20261123
printf "import builtins\nbuiltins.R2G_W=%s\nexec(open(__import__('unreal').Paths.project_dir()+'Tools/R2G2_20261123/c_world.py',encoding='utf8').read())\n" "$3" > $T/_cand.py
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/$T/_cand.py" r2g2_cand 60 2>&1 | grep "^W" | cut -c1-200
PRE="$4" bash Tools/R2G_20261123/tour2_r2g.sh "$1" "$2" 2>&1 | tail -30
