#!/bin/bash
# VF2B helpers (owner aip). J "<python>" [kind] [tail]: run a snippet with the PIE helper preloaded. JF file name timeout kind.
P="<PROJECT>"; cd "$P"; T=Tools/VF2B_20261125; O=aip
RUN(){ SHME_OWNER=$O SHME_KIND=$3 bash Tools/SHME_V2_20261014/run_v2.sh "$P/$1" $2 ${4:-120} 2>&1; }
J(){ printf "exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/h.py',encoding='utf8').read())\n%s\n" "$1" > $T/_step.py; RUN $T/_step.py vf2b_s ${2:-measure} 90 | grep -v "^OK " | tail -${3:-1} | cut -c1-${4:-400}; }
W(){ timeout $1 cat /dev/zero >/dev/null 2>&1; }
PIE_ON(){ USHA=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); RUN Tools/SF52_20261105/pie_start.py vf2b_pie pie 60 | tail -1 | cut -c1-60; W 10; RUN Tools/SF52_20261105/p0.py vf2b_p0 measure 30 | tail -1 | cut -c1-40; W 12; }
PIE_OFF(){ RUN Tools/SF52_20261105/pie_stop.py vf2b_stop control 90 | tail -1 | cut -c1-40; W 5; h=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); [ "$h" = "$USHA" ] && echo "SLOT_OK" || echo "SLOT_CHANGED $h"; }
