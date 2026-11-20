#!/bin/bash
# swap_state.sh before|after : editor must be closed. "before" stores the current (final) files under checkpoints/20261120_after
# (with sha1 list) and copies in the pre-round backups from the first manifest of each file; "after" restores the final files and
# verifies their sha1. Used only to record before-videos of the 2026-11-20 round.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; A=Saved/UE59Work/checkpoints/20261120_after
tasklist 2>/dev/null | grep -qi UnrealEditor.exe && { echo EDITOR_RUNNING; exit 1; }
F="ue59_m22_gait_042229:Content/GraceRanger/Input/IMC_GR_SFGameplay.uasset ue59_m22_gait_042229:Content/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player.uasset ue59_m22_gait_042229:Content/Sphirus/Player/GASP/ABP_Sph_GASP.uasset ue59_m22_carry_042256:Content/Sphirus/Player/GASP/ABP_Sph_Body_GASP.uasset ue59_m22_clipk_044339:Content/Sphirus/Player/Motion/AC_Sph_Motion.uasset ue59_m22_clipk_044339:Content/Sphirus/Player/GASP/BP_Sph_GASPCharacter.uasset"
if [ "$1" = before ]; then
  [ -f $A/sha1.txt ] && { echo ALREADY_SWAPPED; exit 1; }
  mkdir -p $A; for x in $F; do f=${x#*:}; mkdir -p "$A/$(dirname $f)"; cp -p "$f" "$A/$f"; sha1sum "$f" >> $A/sha1.txt; done
  for x in $F; do m=${x%%:*}; f=${x#*:}; cp -p "$M/$m/$f" "$f"; done; echo SWAPPED_TO_BEFORE; sha1sum ${F//ue59_m22_[a-z]*_[0-9]*:/} 2>/dev/null | cut -c1-12 | tr '\n' ' '
else
  [ -f $A/sha1.txt ] || { echo NO_AFTER_COPY; exit 1; }
  for x in $F; do f=${x#*:}; cp -p "$A/$f" "$f"; done; sha1sum -c $A/sha1.txt | grep -c OK; mv $A/sha1.txt $A/sha1_restored_$(date +%H%M%S).txt; echo RESTORED_AFTER
fi
