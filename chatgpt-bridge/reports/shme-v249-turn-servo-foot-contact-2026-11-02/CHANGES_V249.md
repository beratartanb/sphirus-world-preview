# CHANGES V2.49 (2026-11-02)

Every write went through the gated runner with a write manifest and a verified backup (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/v249_*.json`). Rollback: `Tools/SHME_V249_20261102/restore249.py <manifest> --apply [--only a,b]` (sha1 verified). Vendor assets and the CoreMotionAAMS/Candidate originals were not modified.

## In production
| asset | change | manifest | script |
|---|---|---|---|
| ABP_GR_MotionMatchingBase (+ child compiled) | root-motion owner vars, snapshot owned latch, entry DB override (`IfThenElse_84`), hold term | v249_rm | install249_rm.py |
| BP_GR_Player / BP_PBI_Player chain | `GR_Impl_CP_PhysicalRedirect` skipped while the component's RootMotionOwned is set | v249_rm | install249_rm.py |
| BP_SHM_HumanMotionComponent | var RootMotionOwned | v249_rm | install249_rm.py |
| 6 crops SHM248_Jog_Start_Turn{L,R}{090,135,180}_crop | root curves SHM249_RX / SHM249_RY | v249_rc | add249_rootcurves.py |
| ABP | capsule position servo (anchor ∘ clip root, Lead 1) | v249_servo | install249_servo.py |
| ABP | servo feed-forward from clip speed + Kp 0.35 | v249_servo2b | install249_servo2.py |
| 14 turn clips (6 crops + 8 SHM_JogQ Turn 090/135/180 copies) | foot ground-contact repair (foot bone only, ball ≥ floor) | v249_foot / foot3 (10 straight/045 clips restored to originals) | fix249_footpitch.py, restore249.py |
| ABP | SHM249_TurnDone latch, hold InRange on Abs(T) | v249_turndone | install249_turndone.py |
| ABP | rest gate SHM249_FromRest (speed < 40) on owner and entry branch | v249_restgate | install249_restgate.py |
| ABP CDO | **SHM249_RM 1.0, SHM248_HoldT 0.0** (promotion) | v249_prom | promote249.py (turn) |

## Installed, inactive (knob 0)
| ABP | SHM249_FPOff (FootPlacement yields while the servo owns a turn on flat ground) | v249_fpoff | install249_fpoff.py |

## Changed and restored
| PSD_SHM248_JogStartT2_L / _R | continuing_pose_cost_bias −2.0 → −0.5 (no effect on the 60 FPS hand-over) → back to −2.0 | v249_t2bias, v249_t2bias2 | set249_t2bias.py |

## Abandoned (restored from manifests)
- ball-pivot foot repair v3/v3c/v3e (moved the stance 14 cm; leg guard failures) — v249_pivot..pivot4.
- engine root motion (`RootMotionFromEverything`): zero root motion through the blend stack's ResetRoot; the RM ≥ 1.5 path stays inert.

## Tools
`Tools/SHME_V249_20261102/`: turn249.py, pivot249.py, stance249.py, score249.sh, probe249_compressed.py, probe249_mirror.py, plus the installers above. `Tools/Retention/retention.py` + `protect.txt` (dry run by default; media temp dirs only after 6 h).
