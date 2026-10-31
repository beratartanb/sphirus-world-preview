#!/bin/bash
# V2.41 H: regional aim offset (aoh / tkha) vs o / tkk, fixed 30
source Saved/Codex/SHME_V241_20261031/lib241.sh; O=$D/chain.out
export SHME_MANIFEST=$D/checkpoint/manifests/aopre.json
echo "H start $(date +%T)" >> $O
WARM=1 ab h30 "j39_lr:o j39_lr:aoh j39_lr:tkk j39_lr:tkha j38_cc90:o j38_cc90:aoh j38_cc90:tkk j38_cc90:tkha j38_c90r:o j38_c90r:aoh j39_rw:tkk j39_rw:tkha"
echo "H_DONE $(date +%T)" >> $O
