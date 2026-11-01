# CHANGES V2.42 (2026-11-01)

Üretim davranışı DEĞİŞMEDİ: her yeni parça bir anahtarın arkasında ve varsayılanı V2.41 davranışını veriyor (`VERIFY241 ALL_OK` son kurulumdan sonra). Hiçbir satıcı asset'i düzenlenmedi.

## Yeni içerik (yalnız yeni paketler, manifest `v242_lat`, `v242_idle`, `v242_idb2`)
| Asset | Ne | Kaynak / yöntem |
|---|---|---|
| `/Game/GraceRanger/SHME/Animations/V242/SHM242_LatStop_L_B<l|r>_P<00..23>` (15 klip) | sola yanal fren/duruş ailesi, bırakma fazı bin'leri | `gen242_latstop.py` = gen237 temas-planlı duruş, `A_CT_Jog_Left` (266 cm/s) üzerinde, kök profili v0 200 / 410 cm/s² (0,49 s, 48,8 cm), son duruş `SHM_A_CP2_Jog_Fwd_Stop` son karesi |
| `.../SHM242_LatStop_R_B<l|r>_P<..>` (20 klip) | sağa yanal | `A_CT_Jog_Right` (249 cm/s) |
| `.../PSD_SHM242_LatStop` | DB, 32 klip (klip içi kayma ≤ 8 cm olanlar), şema/bias `PSD_LS_CoreLateralStop`'tan, tam pencere BranchIn `SHME_V242_LatStop`, continuing bias −3 | `build242_latdb.py` |
| `.../SHM242_Idle_Weighted` | 12 s ağırlıklı + nefes alan duruş idle'ı (feet sabit, bacaklar menteşe-güvenli çözücü) | `gen242_idle.py` (kaynak `af_Stand_Idle_NaturalBaseline_Phase275` kare 0) |
| `.../PSD_SHM242_Idle` | DB (1 klip), şema canlı `PSD_Dense_Stand_Idles`'tan | `build242_idledb.py` |

## ABP (`ABP_GR_MotionMatchingBase` + child), manifest `v242_abp*`
| Değişken | Varsayılan | Etki | Kurulum |
|---|---|---|---|
| `SHM242_DB_LatStop` (PoseSearchDatabase) | `/Game/GraceRanger/Animations/LookStrafe/PSD_LS_CoreLateralStop` (satıcı) | `Update_MotionMatching` `K2Node_Select_3` Option 1 (yanal fren DB'si) artık bu değişkeni okur | `install242_latvar.py` (+ `fix_latvar.py`: ilk kurulum yanlış yol nedeniyle None yazmıştı, düzeltildi) |
| `SHM242_IdleOn` (float) / `SHM242_IdleDB` | 0 / None | `Update_MotionMatching` girişinde: IdleOn>0,5 ve seçili DB adı 'Stand_Idles' içeriyorsa `CurrentSelectedDatabase := IdleDB` + `SetDatabaseToSearch(IdleDB, InterruptOnDatabaseChange…)` — **ilk sürümde etkisiz** (sonraki chooser çağrısı eziyor; ekleme noktası inceleniyor) | `install242_idledb.py` |

## Pawn (`BP_GR_Player` + `BP_PBI_Player`), manifest `v242_pawn`
| Değişken | Varsayılan | Etki | Kurulum |
|---|---|---|---|
| `GR242_TurnSettleGate` (bool) | False | `GR_UpdateIdleTurn`: dönüş montajını başlatan AND'in serbest `A=true` pini → NOT(kapı AND `GetCurveValue('SHM_StopSettle')` ∈ [0,5, 2]) — duruş klibi yerleşene kadar idle dönüşü başlamaz | `install242_turngate.py` |

## Harness
- `Tools/SHME_V212_20261017/v212_run.sh`: senaryolar `w42_id` (yürüyüş identity döngüsü), `j42_lr_p10` (j41_rl_p10'un D-yeniden-kalkışlı aynası).
- `Saved/Codex/SHME_V242_20261101/lib242.sh`, `vars242.sh`, `vars242_cap.sh` (adaylar `lat`, `tg`, `latg`, `idl`; kamera türevleri S/D/G), `Tools/SHME_V242_20261101/v242_ab.sh`, `ab_safe242.sh`.
- Araçlar: `gait242.py` (LTP'den yürüyüş/duruş/kalkış identity metrikleri), `cropstrip242.ps1` (karakter merkezli kare şeridi), `media242.sh` (yan yana gerçek hız AVI), `run242_fps.sh`.

## Geri alma
- Anahtarları varsayılana çekmek yeterli (üretim = varsayılan). Tam geri alma: `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/v242_abp*/`, `v242_pawn/` yedekleri (sha1 doğrulanmış); yeni paketler silinebilir (V242 klasörü).
