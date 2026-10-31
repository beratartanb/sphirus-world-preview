#!/bin/bash
# run_after.sh <variant> : AFTER evidence for an XR2 variant (apply in memory -> clay views + walks under the NEUTRAL review light ->
# production look -> free-movement probes -> lit views + walks with csvprofile). Restore is a separate, explicit step.
V=$1; T=Tools/ExteriorWorld_XR2_20261031
bash $T/xr2_chain.sh apply:dryrun:$V apply:apply:$V look:NEUTRAL views:after_clay:clay walk:after_A_clay:A:clay:0 walk:after_B_clay:B:clay:0 \
     look:restore probe:after views:after_lit:lit walk:after_A_lit:A:lit:1 walk:after_B_lit:B:lit:1
