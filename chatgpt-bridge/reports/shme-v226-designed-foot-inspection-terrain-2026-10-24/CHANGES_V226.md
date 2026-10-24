# SPHIRUS V2.26 — değişiklik listesi (durum: üretim / aday / araç)

Taban: V2.25 üretimi (bridge commit 99198f3). Kontrol noktası `Saved/Codex/SHME_V226_20261024/checkpoint/` (pre_v226 ikili varlıklar + DSL kaynakları + harness; ev alt seviyesi için etiket-sonrası / küre-öncesi / küre-sonrası kopyalar). Tüm Blueprint/DA değişiklikleri DSL (`shm_src.py`, `shm_profiles.py`, `shm_component_vars.py`) üzerinden derlendi; diff'ler `code/*.diff`.

## Üretime alınanlar (DA_SHM_Response_Default + bileşen + ABP, temiz yeniden açılışta `verify_prod226` ile doğrulandı)
| Değişiklik | Dosya | Not |
|---|---|---|
| Arazi T3a: kaldırma kapısı yalnız destek zemini üstündeki platformda | `v226_patch_terrain5.py` → `SHM_UpdateBodyTargets` | |
| Arazi T3d/T3e: platform içindeki ayak temas sayılmaz, dışarı kaldırılır; `StepPenLiftMax` 36 | `v226_patch_terrain7/8.py` | |
| Arazi T3g: kaldırma açığı kaldırmasız poz ayağından (yarıya yakınsama kök nedeni) | `v226_patch_terrain10.py` | 28 cm basamak basışı platform üstünde |
| `SwingLiftMargin` 10,5 → 6 | DA | T3g ile tümsek kaldırması 14–15 cm |
| İnceleme I3 telemetri: çarpılan aktör adı/mesafe/yükseklik/eşleşme | `v226_patch_inspect3.py` | yalnız telemetri |
| İnceleme I4 sözleşmesi: `GR_Inspect` aktör/bileşen etiketi (`InspectTag`), odak = aktör sınır merkezi, `InspectJump` (DSL varsayılanı 2; kaydedilmiş DA 45 — değiştirilmedi), `InspectZoomOn` ayrımı (false = yalnız kadraj + bakış) | `v226_patch_inspect4.py` → `SHM_UpdateCameraV21` | zoom C üretime alınmadı |
| `InspectRadius` 22 → 12 | DA | iki yakın maske ayrışır |
| Maskelere `GR_Inspect` etiketi (4 R05 maskesi) | `tag_masks226.py`, `L_GR_CurrentHouseContent` | geri alma `untag_masks226.py` |
| Maskelere yalnız Visibility sorgusuna cevap veren küre bileşeni (r 12, 25 cm önde, QueryOnly) | `inspect_probes226.py` (`req/probes_r12.py`) | geri alma `req/probes_remove.py`; sahne çarpışması değişmedi |
| ABP: `SHM226_ShiftL/R` + FeetIK dünya-uzayı ModifyBone ×2 (LegIK öncesi) | `install_v226_shift.py` | kurulu, `StepEdgeOn` false → sıfır vektör (etkisiz) |
| Bileşen değişkenleri: `InspectHitName/Dist/Z/Match/ActorName`, `SwingShiftL/R`, `SwingShiftTL/TR` | `shm_component_vars.py` | |
| Profil anahtarları: `InspectZoomOn`(f), `InspectTag`, `InspectJump` (DA 45), `StepEdgeOn`(f), `StepEdgeShift` 12, `StepEdgeShiftFar` 18, `StepEdgeMin` 10, `StepEdgeStepTime` 0,45, `StepEdgeStepMax` 120, `StepEdgeProbe` 15, `StepPenLiftMax` 36 | `shm_profiles.py` | |

## Üretime alınmayanlar (aday / reddedilen)
| Değişiklik | Dosya | Durum |
|---|---|---|
| 32 faz kutulu yazılı geri dönüş klipleri + DB'ler (`SHM226_JogRev_*`, `PSD_SHM226_JogRevBwd/Fwd`), footspeed v1/v2 + `Disable_FootLock` eğrileri | `gen226_rev.py`, `build_v226_revdbs.py`, `add_footspeed226.py` | aday; FootPlacement gezintisi + çıkış sıçraması çözülmedi (REPORT §3) |
| DB `continuing_pose_cost_bias` −0,4 | `req/dbbias226.py` | denendi (t12), geri alındı (−0,05) |
| İniş kaydırması `StepEdgeOn` (te6/te6x) | T3b/T3c/T3f | aday; gerçek rotada yanlış tetikleme (map_r1 278 kare) |
| İnceleme yakınlaşması `InspectZoomOn` true (C) | — | tutarsız, kapalı |

## Test aracı (§2)
| Değişiklik | Dosya | Not |
|---|---|---|
| `state_mode` production / candidate; etkin durum kaydı (`_state.json`), `INVALID_STATE`; `pie_window` 64'ün katı genişlik | `Tools/SHME_V1_20260925/qa_pie.py` | şema varsayılanı sıfırlaması kaldırıldı |
| Özet satırında durum + mod | `Tools/SHME_V21_20261014/pop_report.py` | |
| cvars/avars/senaryolar (`ins_ws`, `ins_ws2` 172°) | `Tools/SHME_V212_20261017/v212_run.sh` | |
| A/B sürücüsü (taban `o` = üretim modu), adaylar | `v226_ab.sh`, `ab_safe226.sh`, `vars226.sh` | |
| Zincir tanısı: `clipfoot226.py`, `req/capterm.py` (dünya çerçevesi ayrışımı), `chain226.py`, `plant225.py`, `posture226.py`, `datacontract226.py` | | araç |
| Arazi/inceleme ölçümü: `step226.py`, `probe_route226.py`, `inspect226.py` | | araç |
| Üretime alma / doğrulama: `promote226.py`, `verify_prod226.py` (`make_verify_promote226.py`) | | |
| Son zincir `run_fin.sh` (TER otomatik kararı, FPS taraması, soğuk başlatma, üretime alma, temiz doğrulama, kanıt, yakalama), medya `media226.sh`, yayın `pub226.sh`/`publish226.sh` | | |
