# V2.24 değişiklik listesi (üretimde olanlar ve kapalı/reddedilenler)

## Üretimde (kaydedildi, temiz yeniden açılışta `verify_prod224` ALL_OK)

### SHME bileşeni (`BP_SHM_HumanMotionComponent`, DSL kaynağı `Tools/SHME_V1_20260925/shm_src.py`)
- **`SHM_UpdateRouting` — kare hızından bağımsız sınıflama.** `SpeedOnset` yeni bir değişken. Ters dönüş sınıfı ve yürüyüş türü bu değerle belirleniyor. Profil anahtarı `RedirectSpeedDecay` = 600.
- **`SHM_UpdateBodyTargets` — salınan ayak açıklığı.** Çıktılar: `SwingLiftL/R` ve `SwingGroundL/R`. Profil anahtarları:
  - `SwingLiftEnabled` true
  - `SwingLiftMargin` 10.5
  - `SwingLiftAhead` 0.18
  - `SwingLiftMinSpeed` 60
  - `SwingLiftTauUp` / `TauDown` / `TauContact`: 0.04 / 0.12 / 0.03
  - `SwingLiftRiseMin` / `RiseRamp`: 1 / 2 cm
- **`SHM_UpdateCameraV21` — takip, bakış dönerken merkeze dönüyor.** Yeni değişkenler `CamFolPrevYaw` ve `CamFolYawK`. Profil anahtarları: `CamFolYawFade` 90, `CamFolYawW` 9.

### `ABP_GR_MotionMatchingBase` (`SHM224_JRMode` = 3)
- **`SHM213_MontTick` (DSL'den yeniden kuruldu; V2.21 LastHitBy onarımı yeniden uygulandı)** şu değişkenleri yazıyor:
  - `SHM224_RevIntent`: isteğin kimliği.
  - `SHM224_EarlyRev`: ters dönüşün ilk fren karesi.
  - `SHM224_RevMir`: girişte yerdeki ayağa göre varyant.
- **EventGraph, MontTick'ten sonra:** isteğe ve ayağa göre `SHM_RedirectDB_JR` = `SHM224_DB_JRFwdO`, `JRBwdO`, `JRLat`, `JRFwdM` veya `JRBwdM`.
- **`Update_MotionMatching`:** köprünün "else" dalına `Branch(SHM224_EarlyRev)` → JR veritabanı eklendi.
- **`SHM_Snapshot`:** `SHM224_LiftL/R` ← bileşenden `SwingLiftL/R`.
- **`FeetIK_Layer`:** `ik_foot_l/r` için iki "Transform (Modify) Bone" düğümü (bileşen uzayında toplamsal Z). FootPlacement'tan sonra, PBI pelvis ve LegIK'tan önce.

### İçerik (`/Game/GraceRanger/SHME/Animations/V224/`)
- **Veritabanları:**
  - `PSD_SHM224_JogRevFwdO`, `JogRevBwdO`: orijinal pivot + geri koşu döngüleri.
  - `PSD_SHM224_JogRevLat`: CP2 sol/sağ pivot + yan döngüler.
  - `PSD_SHM224_JogRevFwdM`, `JogRevBwdM`: aynalanmış pivot + geri koşu döngüleri.
- **Aynalanmış pivotlar:** `SHM224_Jog_Bwd_Pivot_M` (kaynak `SHM_DPP_Jog_Bwd_Pivot`), `SHM224_Jog_Fwd_Pivot_M` (kaynak `A_CP2_Jog_Fwd_Pivot`). Kaynak klipler değişmedi.
- **Bel düzeltmesi:** `A_CP2_Jog_Fwd_Start` ve `SHM_JogQ_A_CP2_Jog_Fwd_Start`. Yalnız spine_01/02/04 ve baş değişti; ayaklar birebir aynı. Yedek: `checkpoint/pre_lumbar`.
- **Dokunulmayanlar:** kaynak animasyonlar ve üretim veritabanları. Sızıntı yok: `verify_prod224` → `db_leak224`.

### Kamera (D aşaması)
- `DA_GR_LocomotionBehavior`: `GR223_PivotXY` 1.
- `DA_SHM_Response_Default`:
  - `CamFollowEnabled` true;
  - eski yatay katkılar 0: `CamBrakeCarry`, `CamAccelCarry`, `CamTurnCarry`, `CamTurnCompGain`, `CamSideShiftMax`, `CamLookAheadWalk`, `CamLookAheadSprint`.

## Ölçüldü, üretime alınmadı
- **Kamera E2 (yan kaydırma) ve E3 (fren/hızlanma taşıması):** gerileme; geri alındı.
- **Geri pivotta bel düzeltmesi:** göğüs koruması 3.4° ile başarısız.
- **Aynalanmış pivotların aynı veritabanında bırakılması (r + ayna):** evreye göre ayırt edemedi; yerine açık ayak seçimi kuruldu.

## Araçlar (`Tools/SHME_V224_20261022/`)
- **Yamalar:** `v224_patch.py` … `v224_patch5.py`.
- **Kurulum:**
  - `install_v224_jrroute.py`, `install_v224_earlyrev.py`, `install_v224_revfoot.py`, `install_v224_swinglift.py`
  - `build_v224_jrdbs.py`, `build_v224_mirdbs.py`, `build_v224_odbs.py`
  - `mirror224.py`, `lumbar224.py`
- **Üretim ve doğrulama:** `promote224.py`, `verify_prod224.py`.
- **Ölçüm:** `lean224.py`, `phase224.py`, `cslip224.py`, `ter224.py`, `camoff224.py`, `entry224.py`, `final224.py`, `clipscan224.py`.
- **Senaryolar ve medya:** `scen224.txt` (`v212_run.sh` içinde), `media224.sh`.
