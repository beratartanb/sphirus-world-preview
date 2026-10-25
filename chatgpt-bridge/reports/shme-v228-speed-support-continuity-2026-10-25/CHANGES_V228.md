# SPHIRUS V2.28 — değişiklik listesi (durum: üretim / aday / araç)

Taban: V2.26 üretimi + V2.27 kurulu-kapalı adayları (bridge `a6682a0`). Kontrol noktası `Saved/Codex/SHME_V228_20261025/checkpoint/pre_v228/` (ABP_GR_MotionMatching(.Base), BP_SHM_HumanMotionComponent, DA_SHM_Response_Default, DA_GR_LocomotionBehavior, 66 V226 varlık, L_GR_CurrentHouseContent) + `checkpoint/tools/` (DSL kaynakları V2.27 hali, harness). Üretime alınan gruplar (03:30, temiz yeniden açılış ALL_OK 05:40): hareket (klip-bağlı kapsül + tutma, FP açık), iptal yolları, arazi (tavan 36), gerçek-kenar kaydırma (uzat 18 / kısalt 12), inceleme (kimlik + odak). Ayrıntı `REPORT_V228.md §4`; geri alma `promote228.py {rollback: True}`.

## HAREKET — klip-bağlı kapsül hızı ve iptal yolları
| Değişiklik | Dosya | Kapsam | Düğme / durum |
|---|---|---|---|
| 64 SHM226 klibine `SHM226_V` (tasarım hızı, karakter ileri ekseni) + `SHM226_W` (=1, karışım tanığı) eğrileri | `add_speedcurve228.py` | aday varlıklar | — |
| ABP `SHM_Snapshot`: `SHM228_DesV` = V/W (W>0,1), `SHM228_Cmd` = DesV + LeadFrames·ΔDesV, `SHM228_On`; bileşen sözleşmesine `ClipSpeed`/`ClipSpeedOn` yazımı | `install_v228_clipspeed.py`, `fix_v228_abp_w.py` | ABP (grafik yaması) | `SHM228_ClipSpeed` (0), `SHM228_LeadFrames` 1 |
| Bileşen değişkenleri `ClipSpeed`, `ClipSpeedOn`, `InspectPrevHitName`, `InspectSwitch` | `add_comp_vars228.py`, `shm_component_vars.py` | BP_SHM_HumanMotionComponent | — |
| `BP_GR_Player.GR_Impl_CP_PhysicalRedirect` sonuna klip-hız dalı: `Velocity = Fwd × (ClipSpeed − MaxAccel·dt·dot(fwd, DesiredDir))`, `GroundFriction` 0; CalculateMaxAcceleration dokunulmadı (ilk sürümün ivme sıfırlaması niyeti öldürdü) | `install_v228_gr.py`, `fix_v228_gr2.py` | GR hareket katmanı | profil `GR228_ClipSpeed` (0) |
| İptal yolları: `SHM228_EntrySign/Brake/Cancel/Reroute`, bırakmada fren fazı tutuşu, ikinci istekte karşı aile DB'sine yeniden rota (SHM_HoldDB + interrupt arama), yeniden giriş mandalı devre dışı (PrevRev 10), arama kısıtı rota karesinde kalkar (`SHM228_ThrOK`), niyete-karşı güvenlik (push fazında, `SHM228_AgainstT` > 0,08 s → Dead), aile kapısı tutuşla OR | `install_v228_cancel.py`, `fix_v228_cancel2.py`, `fix_v228_cancel3.py` | ABP | `SHM228_RelHold` (0), `SHM228_CancelOn` (0), `SHM228_AgainstMax` 0,08 |
| İçerik: 10 kutu yeniden üretildi (fren ayağı tau0'da zeminde ise yönlendirilmez, diğer ayak fren ayağı) + iki DB tam BranchIn penceresiyle yeniden kuruldu + üç eğri yeniden eklendi | `gen228_rev.py` (gen226 kuralı), `build_v226_revdbs.py` (ENTRY 10, NPH 32), `add_revcurve227.py`, `add_speedcurve228.py` | aday varlıklar: B_F P6 P14, F_B P2 P6 P10 P13 P18 P26 P29 P30 | — |

## İNCELEME
| Değişiklik | Dosya | Düğme / durum |
|---|---|---|
| Hedef kimliği = son karedeki aktör nesne adıyla eşitlik (`InspectPrevHitName`), yeni adayda mandal korunur ve `InspectSwitchOn` (0,25 s) sonra yumuşak geçiş, mandal yokken odak noktasına anında geçiş; odak = aktör konumu | `shm_src.py` SHM_UpdateCameraV21 (DSL, funcs yeniden derleme ×2) | `InspectIdOn` (DSL varsayılanı 0), `InspectFocusMode` (0), `InspectSwitchOn` 0,25 |
| LookAt düğümleri DEĞİŞTİRİLMEDİ (eksen zaten +Y; `install_v228_lookaxis.py` iptal) | — | — |

## ARAZİ
| Değişiklik | Dosya | Düğme / durum |
|---|---|---|
| Gerçek-kenar kapısı: sonda yükselmesi − sürekli eğimin (tan(TerrainSlope)·2·StepEdgeProbe) ürettiği yükselme > StepEdgeMin; kısa/uzun iniş durumu (uzat `StepEdgeShift` / kısalt `StepEdgeShort`) | `shm_src.py` SHM_UpdateBodyTargets (DSL) | `StepEdgeOn`, `StepEdgeShort` 12 (yeni), `StepEdgeShift` 12→18 (aday te4b) |
| Kaldırma tavanı | DA | `SwingLiftMax` 25 → 36 (aday tl36) |

## Test aracı
| Değişiklik | Dosya |
|---|---|
| Anlar ve giriş durumu `moments228.py`; klip saati–kapsül saati `speedclock228.py`; klip-bağlı hız izleme `clipspeed228.py`; basış ölçeri `step228.py` (düz zemin tabanı), kare izi `ter228.py`; baş/boyun bakış `gaze228.py` (kemik eksenlerinden ileri); kol/baş/gövde devir `arms228.py` | `Tools/SHME_V228_20261025/` |
| Sondalar (salt okunur): `probe_entry228/gr228/gr228b/masks228/look228/lookat228/route228/jr228/order228` | |
| Telemetri: cvars `ClipSpeed`,`ClipSpeedOn`; avars `SHM228_*` | `v212_run.sh` |
| Varyantlar `rhC`,`rhCF`,`rhC0`,`rhCR`,`rhCRr`,`tl36`,`te4`,`te4s`,`te4b`,`ins5` | `vars228.sh` |
| Zincirler `run228_t1..t6.sh`, `run228_build.sh`/`build2.sh`, `run228_gen*.sh`, `run228_c3.sh`, `run228_fin.sh "<gruplar>"`; terfi `promote228.py`, doğrulama `req/verify_fin228.py`, tablolar `req/tables228.sh` | `Saved/Codex/SHME_V228_20261025/` |
