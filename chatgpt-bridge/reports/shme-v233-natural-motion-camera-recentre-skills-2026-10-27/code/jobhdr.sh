#!/bin/bash
# jobhdr.sh <src.py> <dst.py.tmp> : V2.33 job header for the gated runner (runner.py G2-G4). Kind = $SHME_KIND or inferred from the
# script name (qa_pie -> pie; revert / gc / throttle / memprobe / post_check / mp_job / only_ / end_pie -> control; verify / probe / *_dry /
# scan / read -> measure; anything else -> write, which the runner refuses without $SHME_MANIFEST). Owner = $SHME_OWNER (default anon:
# refused while EDITOR_LOCK names an owner).
src="$1"; dst="$2"; b=$(basename "$src" .py)
k="${SHME_KIND:-}"
if [ -z "$k" ]; then case "$b" in
  qa_pie*) k=pie;;
  revert_*|gc_job*|throttle*|memprobe*|post_check*|mp_job*|only_*|end_pie*|quit*) k=control;;
  verify*|probe*|*_dry|*dry*|scan*|read*|*_probe|*_measure) k=measure;;
  *) k=write;; esac; fi
{ echo "# SHME_KIND: $k"; echo "# SHME_OWNER: ${SHME_OWNER:-anon}"; [ -n "${SHME_MANIFEST:-}" ] && echo "# SHME_MANIFEST: $SHME_MANIFEST"; cat "$src"; } > "$dst"
