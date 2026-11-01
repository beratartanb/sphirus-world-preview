# CHANGES V2.46 (2026-11-02)

## Üretim davranışı
Değişmedi: V2.45 üretimi aynen (SHM245_Walk_Fwd girişi, PSD_SHM244_LatStop, yerleşme/bakış dönüş kuralları, idle kancası kapalı).

## Kaydedilen asset değişiklikleri (davranışsal etkisi yeniden başlatılmış oturumda yok)
| Asset | Değişiklik | Durum |
|---|---|---|
| `Integrated/CharacterWorldFinal/WalkLoops/M_Ranger_Walk_Loop_F_PureForward_CWF` | iz `SHME_V246_Cost`: PoseSearchModifyCost +2,0 | yalnız bellek içi indekste etkili; kaldırılabilir (`build246_rangercost.py` remove) |
| `Integrated/.../M_Neutral_Walk_Loop_{F_L_20_Phase27Support, F_R_20_Phase275Support, FL, FR, F}` | iz `SHME_V246_Cost`: +6,0 | aynı (`build246_densecost.py` remove) |
| `Integrated/PSD_Dense_Stand_Walk_Loops` | yeniden kaydedildi (18→15 giriş) | yedek `v246_ddb`; ölçülen senaryolar aynı |
| `ABP_GR_MotionMatchingBase` (+child) | `SHM246_LookRoute` (bool, false), `SHM246_LookYaw` (float; Update_MotionMatching girişinde `PreviousDesiredControllerYaw`'dan yazılır); LS yanal kalkış InRange girişi `Select(LookRoute ∧ LS_LookDriven, |CalculateDirection(Acceleration, Rotator(LookYaw))|, |Direction|)` | anahtar kapalı → inert |
| `BP_GR_Player` | denenen pawn yaması bağlanamadı (yeniden yüklendi, kaydedilmedi) | değişmedi |

## Araçlar
`gen/`: `build246_rangercost.py`, `build246_densecost.py`, `install246_lookroute.py`, `install246_lookyaw.py` (başarısız), `install246_lookyaw2.py`, `pre246_inertia.py`/`post246_inertia.py`; `manifest233.py` ve runner `_check_manifest` uzun yol (`\?\`) desteği; `scratchpad/throttle.py` yeniden oluşturuldu; zincirler `run246_a..h.sh`.
Satıcı asset değiştirilmedi.
