# Sphirus: GASP + SHME fizik katmanı + Core Motion — hareket ve kamera uygulaması (2026-11-09/10)

Motor UE 5.8.4 · harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse` · aktif oyuncu `BP_HybridA_Player` (artık GASP tabanlı) · rapor tarihi 2026-11-10.

## 0. Sonuç özeti

| Konu | Durum | Kanıt |
|---|---|---|
| GASP (5.8, temiz kopya) projeye entegre, satıcı dosyalarının üzerine yazılmadı | **PASS (teknik)** | §1, `data/gasp_import_manifest.json` |
| Aynı MetaHuman üzerinde temiz GASP adayı (B) | **PASS (teknik)**, görsel REVIEW_REQUIRED | §2, `videos/*_gaspB.mp4` |
| Bağımsız hareket-fizik + efor bileşeni (`AC_Sph_Motion`) | **PASS (teknik)**, his REVIEW_REQUIRED | §4 |
| Klavyeyle ani ters niyette fren → bas → it (araba gibi yay yerine) | **PASS (ölçüm)** | §4.2 |
| Kamera süpürmesinde sprint yayı | Bilinçli olarak yay (brif izin veriyor); kök ofseti 20–27 cm'e dayanıyor → **PARTIAL** | §4.2 |
| Efor açık/kapalı A/B | **PASS (ölçüm)**: ardışık sert manevrada ~%15 daha yavaş toparlanma, 5 s dinlenmede geri geliyor; his REVIEW_REQUIRED | §4.3 |
| Görünür nefes / efor tepkisi | **PASS (ölçüm)**: dinlenmede omuz nefesi 2,05 cm (nefes katmanı olmadan 0,85 cm) | §4.4 |
| Omuz/köprücük "kilitli" | Ölçümle kilitli değil (omuz kuşağı salınımı yürüyüşte 4–5 cm, koşuda 8–12 cm; retarget kaynağın ~%80'ini taşıyor); düşük omuz algısı sayıyla doğrulanamadı → **REVIEW_REQUIRED** | §3 |
| Yürüyüş/koşu klip tutarlılığı (start'a geri dönme yok) | **PASS (ölçüm)**: 30 s yürüyüşte 1 start + 26,8 s tek döngü | §2.3 |
| Bekleme (50 s) | **PASS (ölçüm)**: tek uzun döngü + nefes + seyrek GASP idle break (14–26 s arayla), girdiyle anında kesiliyor; görsel REVIEW_REQUIRED | §5, §11 |
| Etkileşim montajları (18 adet, MCPaul iskeleti) GASP sürücüsünde | **PASS (teknik)**: tam beden ve UpperBody oynuyor | §6 |
| Aktif oyuncuya geçiş (tek piyon, tek AnimBP zinciri) | **PASS (teknik)**: `BP_HybridA_Player` GASP karakterine yeniden ebeveynlendi; ikinci piyon runtime'da yok | §7 |
| Story Framework / istasyon / kayıt regresyonu | **PASS (teknik)**: istasyon/ev kuralı/kamera/kayıt yazma/yükleme çalışıyor; ev içi yürüme yeniden 150 cm/s; `LoadGame(IgnorePlayerLocation=False)` konumu ve yönü birebir geri yüklüyor (önceki "yüklemiyor" bulgusu test hatasıydı, §11) | §7, §11 |
| Relaxed GASP seti | Araç engeli kalktı (§11), **uygulanmadı** | §2.4 |
| Core Motion klipleri | Bu turda locomotion için **reddedildi** (gerekçe §2.5) | §2.5 |
| Cook/paket, 60 FPS, eğim/merdiven, traversal | **NOT_TESTED** | §8 |

Kullanıcının oynanış kabulü ayrı: aşağıdaki PASS'lar teknik/ölçüm PASS'larıdır.

## 1. GASP kurulumu ve sahiplik

- Kaynak: launcher önbelleğindeki temiz `GameAnimationSample_5.8` (kullanıcının kendi `GameAnimationSample` projesi 31 dosyada değiştirilmiş olduğu için kaynak olarak kullanılmadı). Bağımlılık kapanışı başsız editörle çıkarıldı (`changes/deps.py`).
- 1688 dosya (1,96 GB) Sphirus'a **yalnız eksik olanlar** eklenerek kopyalandı; 347 dosya zaten birebir aynıydı; hiçbir Sphirus dosyasının üzerine yazılmadı. Yumuşak referanslar (MetaHumans/Common — Sphirus'takilerle farklı) kopyalanmadı. Liste: `data/gasp_import_manifest.json`.
- 14 motor eklentisi (Mover, AnimationLocomotionLibrary, SmartObjects, RigLogic …; hepsi Epic motor eklentisi, imzasız DLL yok), 27 `DDCvar` konsol değişkeni ve 43 gameplay etiketi eklendi. Sphirus çarpışma kanalları **değiştirilmedi** (GASP 1–3: Traversable/Mouse/Obstacle; Sphirus 1–3: VineWall/Movement/Ledge → GASP traversal izleri Sphirus kanallarına düşer; traversal bu turda kapsam dışı, §8).
- Sphirus'a ait türevler (`/Game/Sphirus/Player/GASP/`): `BP_Sph_GASPCharacter` (GASP CMC karakter kopyası; GASP kamera/input kurulumu kapatıldı, alt sınıflar için `Sph_GASPBeginPlay` / `Sph_GASPLanded` giriş olayları), `ABP_Sph_GASP` (sürücü AnimBP kopyası, UpperBody katmanı eklendi), `ABP_Sph_Body_GASP` + `Rig/RTG_Sph_UEFN_to_MH` (MetaHuman gövde retarget'ı, nefes katmanı), `BP_Sph_GASP_B` (aday piyon). Hareket katmanı `/Game/Sphirus/Player/Motion/AC_Sph_Motion`.
- Tek bilinçli satıcı varlığı istisnası: `SK_UEFN_Mannequin` iskeletinin "uyumlu iskeletler" listesine `SK_MCPaul_Skeleton` eklendi (yalnız meta veri; §6). Yedek: manifest + `C:\Users\berat\SphirusCheckpoints\GASP_PrePromote_20261110_0614`.

**Tekil sahiplik şeması (son durum):**

| Katman | Sahip |
|---|---|
| Input / niyet | `BP_HybridA_Player` Sphirus input'u (`IA_Sph_*`); GASP IMC eklenmiyor. Gait isteği `GR_GaitSel` → GASP `CharacterInputState` (W yürüme, Shift koşu, Shift basılı sprint; ev içinde yalnız yürüme) |
| Hareket durumu | Tek CMC; hız/ivme/fren/sürtünme/dönüş hedeflerini GASP `UpdateMovement_PreCMC`/`UpdateRotation_PreCMC` yazar; `AC_Sph_Motion` yalnız iki çarpan verir (`SpeedScale`, `AccScale`). Eski Sphirus hız yazıcıları devre dışı |
| Poz seçimi | `ABP_Sph_GASP`: GASP chooser + Motion Matching + blend stack + Offset Root Bone + Foot Placement + Leg IK |
| Retarget | `RTG_Sph_UEFN_to_MH` (GASP'ın Epic MetaHuman retarget'ının kopyası) tek kez, görünür gövdede |
| Fiziksel ek tepki | `ABP_Sph_Body_GASP` nefes katmanı (göğüs + köprücük, `EUse` ile) ve GASP'ın kendi eğilme additive'i |
| Üst beden / etkileşim | Montajlar sürücüde: `DefaultSlot` (tam beden) + yeni `UpperBody` (spine_01 üstü, önbellekli tek değerlendirme) |
| Kamera | Sphirus `GR_SpringArm` + `Cine` (önceki kazanımlar: derinlik gecikmesi, baş takipli yanal ofset, ivme tepkisi); GASP GameplayCamera ve kamerası otomatik etkin değil |

## 2. Temiz GASP adayı (B) ve karşılaştırma

### 2.1 Kurulum
B = Sphirus oyuncusunun kopyası, GASP karakter kopyasına yeniden ebeveynlenmiş; gizli sürücü UEFN mankeni + GASP AnimBP; görünür MetaHuman `RTG_Sph_UEFN_to_MH` ile. Kamera, yüz, saç, giysi, Story Framework bileşenleri aynı. Test: PIE'de GameMode üzerinden B doğurulup kontrol ettirildi (`changes/swap.py`).

### 2.2 A (mevcut Core Motion) – B (temiz GASP) – C (GASP + Sphirus fizik/efor) aynı protokol
Tablolar `data/ac_*.md`, `data/bc_*.md`, gövde metrikleri `data/body_*.txt`. Öne çıkanlar:

| Ölçüm (aynı girdi) | A | B | C |
|---|---|---|---|
| Klip seçimi (saniyede değişim, yürüyüş/koşu) | 12–21 blend kimliği/s | 0,4–1,8 | 0,4–1,8 |
| Yürüyüşte W→S terslemesi | kapsül 0,3 s'de durur, 0,8 s'de 180'e; gövde blend zinciri | 0,1 s'de 200→40, 0,4 s'de 200; `Walk_Turn_L_180` pivot klibi | B ile aynı (yürüme hızında fren ölçeği küçük) |
| Klavyeyle sprint terslemesi (S+Shift) | (sprint yok, koşu 500) | — | 700→51 cm/s 0,5 s, hız yönü terslemeye kadar sabit (yay yok); `Sprint_Turn_L_180 → Run_Hourglass → Reface_Start` |
| Kamera süpürmesiyle sprint 180° | koşuda yay (287→161) | yay, en düşük 330 cm/s, kök ofseti 20–27 cm | yay, en düşük 302 cm/s (bilinçli) |
| Yürüme duruşu (kapsül) | 0,6 s / 63 cm | 0,13 s / 20 cm (GASP duruş klibi 200→0'ı 0,2 s'de yapar) | B ile aynı |
| Koşu/sprint duruşu | 1,2 s / 303 cm (500'den) | 0,40 s / 158 cm (700'den) | 0,40 s / 160 cm |

### 2.3 Uzun kayıtlar (C, düz test sahnesi)
- 30 s kesintisiz yürüyüş: `Stand_Idle_Loop 0,1 s → Walk_Start_F_Lfoot 3,2 s → Walk_Loop_F 26,8 s`; başlangıç klibine geri dönüş 0; hız 199–200; oyun adımı ort. 0,0334 s (gerçek zaman).
- Bekleme 50 s: §5.

### 2.4 Relaxed set — BLOCKED
GASP'ta tam bir Relaxed set var (122 yürüme, 118 koşu, 17 bekleme). Seçim tablosu yalnız Mover AnimBP bağlamı için yazılmış; bağlam sınıfı ilk denemede Python'dan değiştirilemedi. Güncelleme: doğru metin biçimiyle `InstancedStruct.import_text` çalışıyor (§11.2); Relaxed set yine de bu turda bağlanmadı. Kopya AnimBP `ABP_Sph_GASP_Rx` derleniyor ama bağlamsız tablo kullanılamaz; üretimde kullanılmıyor.

### 2.5 Core Motion — bu turda locomotion'da reddedildi
Gerekçe: aynı protokolde Core Motion veritabanları saniyede 12–21 blend kimliği değişimi ve terslemede blend zinciri üretti; GASP aynı girdide tek, amaçlı klipler (start/stop/turn/pivot/reface) seçti. Core Motion pivot kliplerinde kök yaw 0 (önceki rapor). Core Motion içeriği projede duruyor; etkileşim montajları (MCPaul) GASP sürücüsünde oynamaya devam ediyor (§6). Kadın yürüyüşünün GASP'a karşı görsel A/B'si: `videos/TS_side_A_*` ve `TS_side_C_*` (yan), kullanıcı kararı.

## 3. Omuz / köprücük / omurga — ölçüm

Metrikler görünür MetaHuman ve gizli sürücü iskeletinde eş zamanlı (`changes/an_body.py`):

| | A yürüme | B/C yürüme | B/C koşu–sprint | Sürücü (GASP) |
|---|---|---|---|---|
| Omuz kuşağı sol–sağ salınımı (cm) | 3,0–5,3 | 4,1–5,1 | 8,2–12,2 | yürüme 5–6, sprint 10–15 |
| Kalça–omuz çizgisi burulması (°) | 19–30 | 27–39 | 40–68 | MetaHuman ile ±1° |
| Boyun altında omuz düşüklüğü (cm) | 6,2–6,6 | 6,5–7,4 | 3,6–5,0 | 7,7–8,9 |

- İlk ölçümde köprücük eklem konumunu kullandığım için omuz "kilitli" görünmüştü; bu yanlıştı (köprücük dönünce eklem değil omuz hareket eder) ve düzeltildi.
- Retarget, sürücüdeki omuz kuşağı hareketinin ~%80'ini taşıyor; burulma birebir aktarılıyor. Omuz düşüklüğü 6,2–7,4 cm, anatomik olağan aralıkta.
- Sonuç: "kilitli omurga / düşük omuz" sayısal bir kayıp olarak bulunmadı. Görsel yargı için yan ve 3/4 videolar: `videos/TS_side_*`, `TQ_q34_*`. **REVIEW_REQUIRED.**

## 4. SHME fizik ve efor katmanı (`AC_Sph_Motion`)

### 4.1 Model (her tick)
`Acc` (yumuşatılmış yatay ivme), `TurnSev` (niyet–hız karşıtlığı × hız payı), `Demand = Acc/1500 + 0,45·TurnSev + hız payı`, `E` (dE/dt = 0,9·Demand·(1−E) − (E/5)·clamp(1−2·Demand)), `EUse` (alçak geçirgen, 0,8/s — manevra kendini yavaşlatmaz, SHME V2.29 dersi), `ReqLoad` (istek yönü 60°'den fazla değiştiği karede kilitlenen yük). Tüketiciler:
- `SpeedScale` → GASP `CalculateMaxSpeed` × ölçek: niyet hızla ters ve hız yüksekse 0,05'e kadar düşer (düşüş 15/s, toparlanma 3/s) → CMC önce frenler, sonra yeni yöne iter.
- `AccScale` → GASP `CalculateMaxAcceleration` × (1 → 0,75, `EUse` ile): yorgunken daha yavaş yeniden hızlanma.
- `EUse` → görünür gövde nefes katmanı (§4.4).
Anahtarlar: `Enabled`, `EffortEnabled`.

### 4.2 Fren → bas → it (P0 "araba gibi dönüş")
Klavyeyle sprintte S: kapsül 0,1 s'de 700→523, 0,5 s'de 51; hız yönü tersleme anına kadar 180°'de; ardından yeni yöne 1,3 s'de 500. GASP kliplerinin kendi kök profilleri (`data/` ve §2): sprint 180 klibi 700→24 cm/s 0,3 s, 180° 0,6 s'de, 1,6 s'de 700'e döner — kapsül artık aynı fiziksel olayı anlatıyor. Kamera süpürmesinde (fare 360°/s) niyet kademeli döndüğü için yay korunuyor (brif izin veriyor); burada Offset Root Bone 20–27 cm'e dayanıyor (sınır 30 cm) → ayak kayması riski, PARTIAL.

### 4.3 Efor A/B (aynı girdi)
Gerçek üretim oyuncusu, düz test sahnesi, aynı girdi (`EP_off_p1` / `EP_on_p1`); anahtar kaydedici tarafından düzenleme bildirimi tetiklemeden uygulanır. Sütunlar: en yüksek hız / tersleme süresi (S basışı → hız yönünün dönmesi) / %50 ve %90 hıza ulaşma / duruş (s, cm) / gövde–kapsül ayrışması (cm) / pelvis çökmesi (cm) / omuz salınımı (cm) / E, EUse / en düşük SpeedScale / AccScale.

| seg | input | efor kapali: vmax / rev / t50 / t90 / stop (s, cm) / sep / drop / rock / E,EUse / Smin / Acc | efor acik: same |
|---|---|---|---|
| 0 | release | 0 / - / - / - / -,- / 4 / 0.0 / 0.1 / 0.00,0.00 / 1.00 / 1.00 | 0 / - / - / - / -,- / 5 / 0.2 / 0.2 / 0.00,0.00 / 1.00 / 1.00 |
| 1 | W LeftShift | 700 / - / 0.50 / 1.31 / -,- / 30 / 21.2 / 10.1 / 0.00,0.00 / 1.00 / 1.00 | 700 / - / 0.50 / 1.30 / -,- / 30 / 21.2 / 10.3 / 0.51,0.23 / 1.00 / 0.94 |
| 2 | S LeftShift | 700 / 0.54 / 0.00 / 0.00 / -,- / 24 / 6.1 / 13.2 / 0.00,0.00 / 0.12 / 1.00 | 700 / 0.57 / 0.00 / 0.00 / -,- / 24 / 5.9 / 12.9 / 0.82,0.58 / 0.11 / 0.86 |
| 3 | W LeftShift | 633 / 0.50 / 0.00 / 0.00 / -,- / 21 / 20.2 / 10.7 / 0.00,0.00 / 0.19 / 1.00 | 571 / 0.46 / 0.00 / 0.00 / -,- / 23 / 22.1 / 13.7 / 0.91,0.75 / 0.28 / 0.81 |
| 4 | S LeftShift | 547 / 0.26 / 0.00 / 0.86 / -,- / 28 / 13.8 / 14.6 / 0.00,0.00 / 0.57 / 1.00 | 462 / 0.27 / 0.00 / 0.90 / -,- / 26 / 16.9 / 18.0 / 0.95,0.85 / 0.64 / 0.79 |
| 5 | W LeftShift | 579 / 0.44 / 0.00 / 0.00 / -,- / 27 / 12.4 / 13.8 / 0.00,0.00 / 0.27 / 1.00 | 494 / 0.29 / 0.00 / 0.00 / -,- / 30 / 14.6 / 12.4 / 0.97,0.92 / 0.51 / 0.77 |
| 6 | release | 486 / - / 0.00 / 0.00 / 0.30,83 / 18 / 9.3 / 9.9 / 0.00,0.00 / 0.92 / 1.00 | 464 / - / 0.00 / 0.00 / 0.26,75 / 24 / 5.8 / 7.0 / 0.73,0.86 / 0.96 / 0.79 |
| 7 | S LeftShift | 667 / - / 0.47 / 1.23 / -,- / 23 / 15.3 / 17.0 / 0.00,0.00 / 1.00 / 1.00 | 646 / - / 0.57 / 1.21 / -,- / 25 / 13.2 / 21.4 / 0.82,0.80 / 1.00 / 0.80 |
| 8 | release | 689 / - / 0.00 / 0.00 / 0.39,154 / 38 / 20.3 / 8.1 / 0.00,0.00 / 1.00 / 1.00 | 666 / - / 0.00 / 0.00 / 0.37,144 / 26 / 23.2 / 3.7 / 0.38,0.49 / 1.00 / 0.88 |
| 9 | W LeftShift | 678 / - / 0.47 / 1.20 / -,- / 24 / 19.0 / 16.3 / 0.00,0.00 / 1.00 / 1.00 | 658 / - / 0.50 / 1.20 / -,- / 25 / 13.9 / 16.6 / 0.64,0.51 / 1.00 / 0.87 |
| 10 | S LeftShift | 698 / 0.53 / 0.00 / 0.00 / -,- / 33 / 13.1 / 16.0 / 0.00,0.00 / 0.11 / 1.00 | 678 / 0.57 / 0.00 / 0.00 / -,- / 24 / 24.0 / 14.5 / 0.86,0.71 / 0.12 / 0.82 |
| 11 | release | 625 / - / 0.00 / 0.00 / 0.36,129 / 27 / 16.6 / 4.0 / 0.00,0.00 / 0.97 / 1.00 | 548 / - / 0.00 / 0.00 / 0.33,101 / 21 / 14.6 / 5.8 / 0.69,0.78 / 0.97 / 0.81 |

Okuma: ilk sert manevrada iki koşum neredeyse aynı (efor henüz düşük; manevra kendini yavaşlatmıyor — SHME V2.29 kuralı). Üçüncü ardışık terslemeden sonra efor açıkken ulaşılan hız 462–494 cm/s, kapalıyken 547–579 cm/s (~%15 daha yavaş toparlanma); son frende 101 cm'e karşı 129 cm. 5 s dinlenmeden sonraki koşuda fark %3'e iniyor (E 0,97 → 0,38). Görünür tarafı nefes (§4.4). Etki ölçülü; abartılı sallanma yok. Önceki iki A/B denemesi geçersizdi (anahtar uygulanmamıştı; PIE'de bildirimli yazma piyonun durumunu her kare sıfırladı) ve rapordan çıkarıldı.

### 4.4 Görünür efor: nefes
`ABP_Sph_Body_GASP`: retarget'tan sonra göğüs (`spine_05`, Z ekseni, 3°) ve iki köprücük (Y ekseni, 4°) additive; genlik `0,3 + 0,7·EUse`, hız `13 → 43 nefes/dk`. Eksenler PIE'de ölçülerek kalibre edildi (`data/cal_breath_result.json`: köprücük Y ekseni iki omzu birlikte +4,8/+5,8 cm/birim kaldırıyor). Sonuç: üç ardışık sert manevradan sonra durunca omuz nefesi 2,05 cm (nefes katmanı olmayan B beklemesinde 0,85 cm); dinlenik beklemede 1,5 cm.

## 5. Bekleme
50 s: tek `M_Neutral_Stand_Idle_Loop`, klip değişimi 0, pelvis kayması ≤1,5 cm, baş hızı medyan 2,9 / p95 4,3 cm/s, nefes 1,5 cm. Eski sistemdeki 2× hızlı tekrar yok. GASP'ın seyrek idle break klipleri (6 adet) yalnız deneysel durum makinesi yolunda; o yol kapalı. Güncelleme: idle break'ler artık `AC_Sph_Motion` üzerinden oynuyor (§11.3).

## 6. Etkileşim montajları
Oyunun 18 montajı (zıplama, yatak, kesme, taşıma, giyinme, içme, diz çökme, alma, dökme, uzanma, uyanma, 6 maske işi) `SK_MCPaul_Skeleton` üzerinde; 16'sı `DefaultSlot`, 2'si `UpperBody`. Çözüm: (a) UEFN iskeletine MCPaul uyumluluğu (meta veri; aynı UE5 kemik adları), (b) `ABP_Sph_GASP`'a önbellekli tek değerlendirmeli `UpperBody` katmanı (spine_01, mesh-uzayı dönüş). PIE testi: `AM_GR_Day_Chop` aktif ve eller kesme pozunda; `AM_GR_Day_CarryArms` yürürken aktif, eller öne/yukarı, bacaklar yürüyor.

## 7. Üretime geçiş ve regresyon
- Checkpoint `C:\Users\berat\SphirusCheckpoints\GASP_PrePromote_20261110_0614`, ardından B'de doğrulanan adımlar oyuncunun kendisine uygulandı (`changes/p1_reparent.py`, `p2_wire.py`, `p3_indoor.py`). `BP_HybridA_Player`, oyuncuya başvuran 7 Blueprint (GameMode'lar, ev/çatı bağlamı, DayHub, DayStation, SplitPiece, MaskBench) ve yeni AnimBP/bileşenler hatasız derleniyor.
- Tek piyon, tek değerlendirme zinciri: eski `ABP_Sph_Driver` / `RTG_Sph_Core_to_MH2` / `PSD_Sph_*` artık oyuncu tarafından kullanılmıyor (projede duruyor, geri alma için). AAMS bağımlılığı geri gelmedi.

| Regresyon (gerçek oyuncu, ev haritası) | Sonuç | Kanıt |
|---|---|---|
| Sola/sağa yürüme kadrajı (kamera sabit) | A: baş X 0,27–0,33 (ort. 0,30), D: 0,29–0,37 | `videos/CL_strafe_prod.mp4` |
| Ev içi kuralı (koridorda Shift) | Koşu yok; ev içi yürüme 150 cm/s (eski tempo; §11), basan ayak kayması medyan 11 → 9 cm/s | `videos/H_hall_i1.mp4` (önce: `H_hall_prod.mp4`) |
| Kesme istasyonu (yaklaş, E, sol tık) | A ile aynı: istasyon etkileşimi ve aksiyon kamerası (kol 106 cm); bu protokolde iki sistemde de kesme montajı tetiklenmiyor; montajın GASP sürücüsünde oynadığı ayrı PIE testinde doğrulandı (§6) | `videos/D_chop_prod.mp4`, `evidence/D_chop_prod_raw_f210.png` |
| Kıyafet / yüz / saç | Doğru (gri atlet, yeşil şort) | üretim kareleri |
| Bekleme 20 s | tek `Stand_Idle_Loop`, baş X 0,30 sabit | `videos/I_idle_prod.mp4` |
| Kayıt/yükleme | Oyun içi kayıt yazıyor (5804 B); aynı oturumda `LoadGame` piyonu taşımıyor (önceden de); önyüklemeyle yükleme oyuncuyu (832, −220)'ye koyuyor, yürüyüş 200 cm/s. Kullanıcı kaydı her testten sonra bayt bayt geri yazıldı (cmp eşit) | `data/reg_save_prod.txt` |
| Seçim tablosu bağlam hatası | **Düzeltildi (§11)**: Sphirus kopyası tablolar, bağlam `ABP_Sph_GASP_C`; aynı girdide günlükte 2359 → 0 hata, klip/veritabanı seçimi birebir aynı | `data/chooser_fix.txt` |

## 8. Açık kalanlar
1. Kamera süpürmesiyle yüksek hız dönüşlerinde kök ofseti 20–27 cm (sınır 30) — ayak kayması riski.
2. Relaxed set: bağlam aracı artık çalışıyor (§11) ama set bağlanmadı; seçim tablosu Mover AnimBP özelliklerine bağlı, ayrı iş.
3. GASP traversal / çarpışma kanalı uyumsuzluğu; vault/mantle bu turda bağlanmadı.
4. Kamera çalı/ağaç yapraklarından geçebiliyor (bahçe kayıtlarında görüldü).
5. Ev içi kuralının ve istasyonların gerçek oyuncuyla doğrulanması §7'de; menüden kayıt/yükleme, cook/paket, 60 FPS, eğim/merdiven, taşıma sırasında beden: NOT_TESTED (aksi §7'de belirtilmedikçe).
6. Test sahnesinde "B" varyantı (katman çalışma anında kapatılarak) geçersiz çıktı; B kanıtı ev haritasındaki `*_gaspB` kayıtlarıdır.

## 9. Videolar
Tümü PIE, 30 kare/s, gerçek zamanlı (her karede oyun adımı kaydı `data/*.json` `gdt`, ortalama 0,033 s), düzeltilmiş kırpma kodlayıcısı.
| Video | İçerik |
|---|---|
| `PH_phys_gaspA / gaspB / prod` | A / B / üretim (C): koşu-sprint, bırak, S tersleme, W, S |
| `B_turns_gaspA / gaspB / prod` | fareyle 360°, 150° zikzak, yerinde 180°, sprintte 360°/s dönüş |
| `CL_strafe_gaspA / prod` | kamera sabit A, D, W+A, W+D, W, S (sola giderken kadraj) |
| `A_loco_gaspA / prod` | yürüme → koşu → sprint (fare 150°) → yürüme → duruş |
| `H_hall_prod`, `D_chop_prod`, `I_idle_prod` | ev içi kural, istasyon, bekleme |
| `TS_side_A_t2 / TS_side_C_t2` | düz sahne, yan profil (yürüme 4 s, duruş, koşu-sprint 3 s, duruş, W, S) |
| `TQ_q34_A_t2 / TQ_q34_C_t2` | aynı girdi, arka 3/4 |
| `TW_walk30_C_t2` | 30 s kesintisiz yürüyüş |
| `TI_idle50_C_t2` | 50 s bekleme |
| `EP_on_p1 / EP_off_p1` | efor açık/kapalı, aynı girdi, gerçek oyuncu |
| `EF_on_c2` | bahçede efor açık (nefes ve fren) |
| `H_hall_i1` | ev içi kural, 150 cm/s (§11) |
| `A_loco_n1` | seçim tablosu kopyalarıyla aynı yürüme→sprint→duruş protokolü (§11) |
| `I_idle50_n1` | 50 s bekleme, iki idle break (§11); GitHub boyut sınırı için %75 çözünürlükte yeniden kodlandı |
| `IO_idlecut_n1` | idle break başladıktan 3,3 s sonra W: kırılma anında kesiliyor (§11) |

Yan/3-4 kamera gövdeye yakın; baş üstten kısmen kesik (omuz–omurga–pelvis net). Tüm videolarda oyun adımı ortalaması 0,033 s (`data/*.json` `gdt`).

## 10. Geri alma
- Oyuncu öncesi: `C:\Users\berat\SphirusCheckpoints\GASP_PrePromote_20261110_0614\Content\Sphirus\CharacterLab\Hazel_20261106\Playable\BP_HybridA_Player.uasset` (Core Motion oyuncusu A). Editör kapalıyken geri kopyalanır.
- GASP içe aktarma öncesi: `C:\Users\berat\SphirusCheckpoints\GASP_P0A_20261109_2325` (uproject, Config, kayıtlar). Eklenen GASP dosyaları `data/gasp_import_manifest.json` listesinden silinebilir.
- Her yazma işinin manifest yedeği: `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_*`.

## 11. Devam (2026-11-10 öğleden sonra): açık maddeler
Her adım manifest yedekli tek yazma işi + editör yeniden açılışı; sonra gerçek oyuncuyla PIE testi.

**11.1 Ev içi tempo 150 cm/s.** `BP_Sph_GASPCharacter`'a `SphContextSpeedScale` (varsayılan 1) eklendi; `CalculateMaxSpeed` sonucu `SphMotion.SpeedScale` ile birlikte bununla da çarpılıyor (`changes/i1_ctxspeed.py`). Oyuncu, `CharacterInputState`'i yazdığı yerde `GR_HomeContext > 0,5 ? 0,75 : 1` yazıyor (`changes/i2_indoor_speed.py`). Koridor testi: en yüksek 150 cm/s, Shift koşturmuyor; dışarıda yürüme 200 / koşu 500 / sprint 700 değişmedi (`A_loco_i1`). Basan ayağın yatay hızı (sabit yürüyüş, iki ayaktan küçüğü) medyan 11,3 → 9,2 cm/s: yavaşlatma kayma eklemedi.

**11.2 Seçim tablosu bağlam hatası.** Kök neden: kopyalanan AnimBP'nin sınıfı (`ABP_Sph_GASP_C`) satıcı tablolarının bağlam sınıfıyla eşleşmiyor (doğrulama yalnız editörde çalışıyor; paketlenmiş oyunda bu günlük yok). Önceki "Python'dan yapılamaz" sonucu yanlıştı: `InstancedStruct.import_text`, `ContextObjectTypeClass(...)` biçimindeki metni kabul ediyor. Çözüm (`changes/n1_choosers.py`): `CHT_PoseSearchDatabases_Dense` ve `CHT_CMCCharacterAnimations`, `/Game/Sphirus/Player/GASP/Choosers/` altına kopyalandı; kopyaların bağlamı `ABP_Sph_GASP_C` yapıldı (CMC tablosunun ikinci, struct bağlamı korunarak); `ABP_Sph_GASP`'taki iki `Evaluate Chooser` düğümü kopyalara bağlandı ve bağlam pini `self`'e yeniden bağlandı. Satıcının kök tablosu `CHT_PoseSearchDatabases` yalnız `MMDatabaseLOD` değerine göre Dense/Sparse/ExtremeSparse seçiyor; Sphirus'ta bu değer 0, yani her zaman Dense. Bu yüzden ABP artık Dense kopyasını doğrudan değerlendiriyor (LOD geçişi bilerek bırakıldı). Satıcı dosyalarına dokunulmadı. Sonuç: aynı girdide `LogChooser: Error` 2359 → 0; klip ve veritabanı dizisi (`A_loco_i1` ile `A_loco_n1`) birebir aynı, hız profili ±5 cm/s.

**11.3 Seyrek bekleme hareketleri (idle break).** GASP bunları yalnız deneysel durum makinesinde oynatıyor; o yol tüm hareketi değiştirdiği için açılmadı. Sahip `AC_Sph_Motion` (`changes/k1_idle.py`). Hız < 3 cm/s, girdi yok, yerde, başka montaj yok ve `IdleEnabled` koşullarında süre birikiyor. Süre `IdleNext`'i (rastgele 14–26 s) geçince 5 GASP `M_Neutral_Stand_Idle_Break` klibinden biri `DefaultSlot`'ta dinamik montaj olarak oynuyor (giriş 0,5 s, çıkış 0,6 s). Girdi gelirse yalnız kendi klibi hâlâ oynuyorsa 0,3 s'de kesiliyor; etkileşim montajı başlarsa onun yerine geçiyor. Ölçüm: 50 s beklemede iki kırılma (5,3 s ve 6,3 s), arada 24,8 s; kapsül kayması 0 cm. Kırılmanın 3,3. saniyesinde W'ye basınca 0,07 s içinde yürüme başladı ve montaj kesildi. Risk: montajsız etkileşim beklemelerinde (ör. istasyonda 15 s+ beklerken) de bir kırılma oynayabilir → REVIEW_REQUIRED.

**11.4 Kayıt yükleme.** Önceki regresyon testi `LoadGame`'i `IgnorePlayerLocation=True` ile çağırmıştı; Story Framework (`SFSaveManager_AC.LoadPlayerData`) bu durumda konumu bilerek uygulamıyor. Bu yüzden "konum geri yüklenmiyor" bir test hatasıydı. `False` ile: kayıt (1225, −696, yön 180°) → 7 m uzağa ışınla → yükle → (1225, −696, 180°) birebir; ardından yürüyüş 200 cm/s (`data/reg_save_pos.txt`). Kullanıcı kaydı test sonunda bayt bayt aynı (cmp).

**11.5 Derleme.** `BP_HybridA_Player`, ona başvuran 9 Blueprint, `ABP_Sph_GASP`, `ABP_Sph_Body_GASP`, `AC_Sph_Motion`: hatasız, güncel. Editör temiz yeniden açıldı.

Hâlâ açık: kamera süpürmesinde kök ofseti 20–27 cm; Relaxed set bağlanmadı; traversal/çarpışma kanalları; kamera yapraklardan geçiyor; cook/paket, 60 FPS, eğim/merdiven NOT_TESTED; görsel/his kabulü kullanıcıda.
