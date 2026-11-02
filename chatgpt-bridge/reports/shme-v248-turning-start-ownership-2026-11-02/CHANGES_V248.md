# CHANGES V2.48 (2026-11-02)

## Üretime alınan (bkz. REPORT §5; `SHM248_On` := 1.0, `SHM248_BackCos` := −0,64 = 130°)
| Asset | Ne | Manifest |
|---|---|---|
| `ABP_GR_MotionMatchingBase` (+ child `ABP_GR_MotionMatching`) | `SHM_Snapshot` (oyun iş parçacığı): pawn `GetControlRotation` → `SHM248_LookYaw`; `SHM248_TurnStart` = jog gait ∧ ivme ∧ (istek bedenin 115°'den fazla arkasında ∧ bakışın 135°'den fazla arkasında DEĞİL) ∨ tutma (T2 DB içinde ∧ dönüş ilerlemesi < 89); `SHM233_StandBack` yalnız bakışa-göre geriye istekte; V2.28 sözleşme kapısı `SHM228_On` ∨= TurnStart∧W; V2.38 `SHM238_Delta` := \|Delta\| (klip-işaretli dönüş); `ClipSpeedLat` yazımı; dönüş bitiş kenarında bileşen `LocoExplore/LocoState/LocoOn/LocoYaw` := beden yönü; `SHM248_PostTurn` kilidi. `Update_MotionMatching`: jog kalkış DB aramalarının önünde `SHM248_TurnStart` → `SHM248_DB_TurnStart_L/R` (T2); PostTurn → `PSD_CT_JogSteady`; LS yanal rotası tutma sırasında kapalı | v248_abp…v248_abp14, v248_prom |
| `BP_SHM_HumanMotionComponent` | yeni değişken `ClipSpeedLat` (float) | v248_latvel3 |
| `BP_GR_Player` (+ `BP_PBI_Player`) | `GR_Impl_CP_PhysicalRedirect` V2.28 hız yazımı: `Velocity = Forward*ClipSpeed + Right*ClipSpeedLat` | v248_latvel3 |
| `V248/SHM248_Jog_Start_Turn{L,R}{090,135,180}_crop` (6 yeni) | `SHM_JogQ_af_Loco_Jog_Start_Turn*` proje kopyalarının dönüş bitimi + 0,25 s'de kırpılmış hâli (0,93–1,0 s); eğriler `SHM226_V/VL/W`, `SHM238_Turn` (işaretli, sonda ±90) `/W`, `SHM241_SYaw/SW` | v248_crop2 |
| `V248/PSD_SHM248_JogStartT2_L/_R` (2 yeni) | PSD_SHM237_JogStartS_L/R girişleri − geriye kalkışlar + 6 kırpılmış dönüş klibi (her iki yön her iki DB'de); BranchIn `SHME_V248_T<L/R>` izleriyle | v248_tdb5 |
| 26 proje kalkış klibi (SHM_JogQ_*, SHM232_IS_*, SHM237_JogStart_F_*) | yeni BranchIn notify izi (T2 DB'ye) | v248_tdb5 |
| `SHM_JogQ_af_Loco_Jog_Start_Turn*` (6 tam kopya) | eğriler `SHM226_V/VL/W`, `SHM238_Turn/W` eklendi (T DB'leri artık rota dışında; eğriler üretimde okunmuyor), `SHM241_SYaw/SW` yeniden yazıldı (büyük/küçük harf) | v248_curves2 |
| `V248/PSD_SHM248_JogStartT_L/_R` (2) | ilk sürüm (kırpılmamış), rota dışı, inert | v248_tdb |
| `Tools/SHME_V212_20261017/v212_run.sh` | telemetri `avars` += SHM248_TurnStart/TT/LookYaw; yeni senaryo `j45_sl2` (yedek `data/v212_run_before_v248.sh`) | — |

Satıcı (AAMS) assetleri değiştirilmedi. Doğrulayıcı `verify241 ALL_OK` her kurulum sonrası.

## Araçlar (Tools/SHME_V248_20261102)
build248_turnstartdb.py, install248_turnstart.py, add248_turncurves.py, install248_turnbind{,2,3,4,5}.py, add248_latcurve.py, install248_latvel.py, add248_turncrop.py, install248_t2.py, install248_loco.py, promote248.py, sel248.py, ltpcols248.py, cropstrip248.ps1, ab_safe248.sh, v248_ab.sh; zincirler `run248_a…m,j`.

## Temizlik (CLEANUP)
`cleanup/delete_plan.tsv` (silme öncesi kayıt, 37 288 satır) → `delete_log.txt`: 63,2 GB v245 öncesi ham telemetri (Evidence/LTP), 9,0 GB yayımlanmış pub/ kopyaları (V2.28–V2.45, XR2/XR3/AIToolingEval), 4,8 GB V2.11 video, 156 MB çökme dökümü, pycache, 11-01 öncesi autosave. Boş alan 18 GB → 93 GB. Korunan: V2.46/47/48 çıktıları, tüm Tools, checkpoint/manifest yedekleri (manifest referanslı 146 yedek), karakter/dünya turu klasörleri (.dna/GD11 soy), Intermediate/DDC. Hiçbir Content/Config/Plugin dosyasına dokunulmadı.
