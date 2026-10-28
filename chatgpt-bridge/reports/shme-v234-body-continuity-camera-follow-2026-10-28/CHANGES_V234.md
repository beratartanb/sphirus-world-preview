# CHANGES V2.34 (2026-10-28, taban V2.33 / Bridge a4417bc)

## Üretimde (VERIFY234 ALL_OK, temiz açılış)

### loco — kamera gövdeyi değiştirmez
**Bileşen `BP_SHM_HumanMotionComponent`**
- `SHM_UpdateCameraV21` içinde:
  - `InFrameOff`: henüz devredilmemiş otomatik dönüş.
  - `LocoIFY`: bir sonraki karenin girdi çerçevesi.
  - `LocoYaw`: gövde/hareket çerçevesi.
  - `LocoState`: 0 çerçeve, 1 keşif, 2 tutma.
- Girdi çerçevesinin devri:
  - çubuğun net sapmasıyla (10–70°);
  - oyuncu bakışıyla;
  - bırakınca hemen.
- Keşif, yürüyüş/tempoluda (hız < 380) şu durumlarda başlamaz:
  - ters dönüşte;
  - depardan başlayan yön değişiminde;
  - başlangıç ailesinin içinde ve bitişinden sonraki 0.5 s içinde.

**`/Game/GraceRanger/BP_GR_Player`**
- Yeni değişkenler: `GR234_LocoOn`, `GR234_LocoYaw`. Yazıcı: `GR_UpdateSHMSignals`.
- `GetControlRotation` okumaları `Select(GR234_LocoOn, GR234_LocoYaw, kontrol yaw)` ile değiştirildi. Etkilenen fonksiyonlar:
  - `CalculateMaxSpeed`
  - `CalculateMaxAcceleration`
  - `CalculateGroundFriction`
  - `GetDesiredGait`
  - `GR_Impl_CR_UpdateBackwardIntent`
  - `GR_Impl_CP_PhysicalRedirect`
  - `GR_UpdateIdleTurn`

**DA:** `LocoFrameEnabled`, `LocoExploreEnabled`, `LocoExploreMaxSpeed 380`.

### camfollow
**DA:**
- `CamRecMinSpeed 60` (yürüyüş açık)
- `CamRecWalkRate 45`
- `CamRecFaceMax 40`
- `CamRecTurnSide`
- `CamEnvEnabled`

**Bileşen:**
- Tepki zarfı `CamEnv`: bölüm başlayınca 0.12 s'de yükselir, bölüm boyunca tutar, bittikten 0.3 s sonra 0.6 s'de söner.
- Gövde yönü kapısı.
- 180° taraf seçimi (`CamRecTurnSign`).

### revkeep
**ABP `ABP_GR_MotionMatchingBase`**
- `SHM_Snapshot` son ters dönüş veritabanını hatırlar: `SHM234_RevDB`, `SHM234_RevDBT`.
- `Update_MotionMatching` girişinde, stand-back dalından sonra, şu koşulların hepsi tutarsa yalnız o veritabanında arama yapılır:
  - aile 3,
  - `RevDBT` < 0.6 s,
  - ivme yok veya hız < 60.
- Anahtar: `SHM234_RevKeepOn` = 1.

**Bileşen `SHM_UpdateRouting`:**
- Aynı yöne yeniden basış ters dönüş ailesinde kalır.
- Bırakma boşluğu da en çok `RevGraceTime` (0.4) kadar bu ailede kalır.
- Yeni değişkenler: `SHM234_RevAgo`, `SHM234_RevDir`, `SHM234_GapT`.

### sprintcalm
- ABP `SHM211_DB_Sprint` → `V233/SprintCalm/PSD_SHM233_SprintCalm` (V2.33 içeriği).

### İçerik: duruş kapanış adımları
- Klasör: `/Game/GraceRanger/SHME/Animations/Stops`.
- Her klipte yalnız son kapanış adımı (≤ 80 cm) değiştirildi; parmak ucu adımın ortasında en az ~4 cm kalkıyor.
- Ayağın yatay yolu değişmedi; bacak IK ile yeniden çözüldü.
- Üreteç: `gen234_stopclear.py`.
- Manifestler: `stopclear`, `stopclear3`, `stopclear4`.

## Araçlar
- **Ölçüm:** `camab234.py`, `envtime234.py`, `stage234.py`, `clipstage234.py`, `clipstop234.py`, `check234.py`, `worst234.py`, `tables234.py`.
- **Yapı kontrolü:** `probe234_camfn.py`, `probe234_route.py` (yeni durum yazıcıları + düğüm tabanı).
- **Kurulum:** `install_v234_loco.py`, `install_v234_revkeep.py`.
- **Üretime alma / doğrulama:** `promote234.py` (geri dönüş değerleriyle), `verify234.py`.
- **Medya / paket:** `media234.sh`, `pub234.sh`.
- **Senaryolar (`v212_run.sh`):** `cam34_*`, `s34_*`, `j34_*`.
- **Telemetri:** `cvars` listesine `Loco*`, `CamEnv`, `CamRec*` ve `MoveLatchYaw` eklendi.

## Skill'ler
- `sphirus-camera-direction`, `sphirus-natural-motion`, `sphirus-safe-unreal-iteration`: kurallar ve gerçek başarısız örnekler eklendi.
- `sync_claude_skills.py` çalıştırıldı.

## Geri dönüş
- `promote234.py` + `{'rollback': True}`: knob'lar V2.33 değerlerine döner.
- Grafik ve içerik değişiklikleri: `checkpoint/manifests/<ad>/` yedekleri.
- Duruş klipleri (21): orijinaller, her klibin ilk değiştirildiği manifestin yedeğindedir:
  - 16 klip `stopclear` içinde;
  - 5 klip `stopclear4` içinde: BL_L, BL_R, BR_R, FL_R, FR_R.
