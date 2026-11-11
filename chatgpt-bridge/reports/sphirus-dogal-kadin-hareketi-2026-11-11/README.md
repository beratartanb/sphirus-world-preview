# Sphirus: doğal kadın hareketi — karşılaştır, seç, düzelt, aktif oyuncuya uygula (2026-11-10/11)

Uygulama tarihi: 2026-11-10 22:40 – 2026-11-11 09:05 (UE 5.8.4, `sphirus.uproject`, harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse`).
Başlangıç: [GASP Relaxed + SHME raporu](../sphirus-gasp-relaxed-shme-fullbody-2026-11-10/README.md) (A = o raporun üretim durumu).

Durum etiketleri: **IMPLEMENTED** (projede, kayıtlı) · **TECH_TESTED** (oyunda ölçüldü) · **VISUALLY_INSPECTED** (benim kare/video incelemem) · **USER_ACCEPTED** (yok — kullanıcı henüz oynamadı) · **PARTIAL** · **NOT_TESTED**.

## 0. Özet

**Aktif oyuncuda artık Core Motion kadın hareket ailesi çalışıyor (C).** Bekleme, yürüme, jog, koşu, kalkış, duruş, pivot ve yerinde dönüş bu aileden; GASP'ın Relaxed seçim mantığı (hız/yön/durum) korunarak her Relaxed veritabanı yöne göre karşılık gelen kadın veritabanına eşleniyor. Zıplama, iniş, çömelme ve traversal Relaxed'da kaldı. `SphCM=False` ile A'ya tek ayarla dönülüyor.

| | Durum |
|---|---|
| Adil A/B karşılaştırması (aynı MetaHuman, kıyafet, sahne, kamera, girdi; aday anahtarı her karede okunarak kanıtlandı) | IMPLEMENTED, TECH_TESTED |
| Seçim: koşu/fren/duruşta Core Motion kadın performansı A'dan belirgin biçimde daha uygun (dik koşu, kompakt kollar, öne katlanmayan fren) | VISUALLY_INSPECTED (benim), **USER_ACCEPTED değil** |
| Core Motion'ı GASP'a taşırken bulunan 8 kök neden ve düzeltmeleri (§4) | IMPLEMENTED, TECH_TESTED |
| Tempo 150 (ev) / 160 / 290 / 500 cm/s, sakin ivme, kliplere göre fren | IMPLEMENTED, TECH_TESTED |
| Ayak teması: yürüme kayması 1,8 cm/temas (A 3,0), koşu 1,0 (A 3,3) | TECH_TESTED |
| Omuz/kol duruşu (§6) | VISUALLY_INSPECTED, ek ofset yok; karar kullanıcıda |
| Efor açık/kapalı | TECH_TESTED (hız/ivme/toparlanma); görünür beden farkı küçük → PARTIAL |
| Gerçek akışlar: üst kat kapısı E, mutfaktan çıkış–basamak–koşu–dönüş–eve dönüş, odun toplama + kesme (E + sol tık), ev içi Shift | TECH_TESTED |
| Oyun içi kayıt/yükleme, tek piyon, temiz yeniden açılış, derleme | TECH_TESTED |
| Sprint 135°/180° dönüşlerinde klip değişimi | PARTIAL |
| Gerçek GPU/CPU maliyeti, paket, menüden kayıt, eğim/merdiven, yatak/çay/maske akışları | NOT_TESTED |

Kullanıcı kaydı (`SFSaveSlot.sav`, SHA1 `8622025b…`) başta ve sonda aynı. Geri alma noktası: `C:\Users\berat\SphirusCheckpoints\WomanMotion_Pre_20261110_2255`.

## 1. Korunan zincir ve başlangıç doğrulaması

| Öğe | Canlı değer |
|---|---|
| Oyuncu | `BP_HybridA_Player` → üst sınıf `/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter` |
| Sürücü AnimBP | `ABP_Sph_GASP` (UEFN iskeleti; Relaxed seçim tablosu yolu `SphRelaxed=True` korunuyor) |
| Görünür beden | `ABP_Sph_Body_GASP`, retarget `RTG_Sph_UEFN_to_MH` (önceki köprücük −5° düzeltmesi korunuyor) |
| Hareket / efor | `AC_Sph_Motion` (efor, fren, SHME yerleşme/göğüs öncülüğü, bekleme kırılmaları) |
| Kullanıcı kaydı | `SFSaveSlot.sav` SHA1 `8622025b…` — başta ve sonda aynı (bkz. §11) |
| Geri alma noktası | `C:\Users\berat\SphirusCheckpoints\WomanMotion_Pre_20261110_2255` (+ `_sha1.txt`, 151 dosya) |

Hazel başı, bedeni, saçı, kıyafeti, Story Framework, kapılar, envanter, kamera bileşenleri **değiştirilmedi**. AAMS bağımlılığı veya ikinci hareket denetleyicisi eklenmedi; eski `ABP_Sph_Driver` / Core Motion oyuncusu etkinleştirilmedi.

## 2. Adaylar (aynı MetaHuman, aynı kıyafet, aynı ışık/zemin/kamera)

| Aday | Ne | Nasıl seçildi (çalışma anında doğrulandı) |
|---|---|---|
| **A** | GASP Relaxed (önceki üretim), 165/375/585 cm/s | `SphCM=False`; kayıt satırlarında `abp=None`, veritabanları `PSD_Relaxed_*` |
| **B** | Core Motion kadın ailesi GASP sürücüsünün içinde (doğal hızlar 186/278/502 = B1; hedef tempo = B2..B7) | `SphCM=True` her karede okunup kayda yazıldı (`abp={'SphCM': 'True'}`), veritabanları `PSD_CM_*`, klipler `CM_af_*` |
| **C** | B'nin düzeltilmiş hâli, aktif oyuncuya terfi | Üretim varsayılanı; aday ayarı verilmeden kaydedildi (`_C1` kayıtları) |

Basic Movement Female veya başka bir kadın hareket seti **kurulu değil** (MC_VillageLife / MC_Sample yalnız `am_` erkek klipleri). Kurulu kadın kaynak: `/Game/MC_Core_Motion/Animations` `af_*` (LocomotionV2 walk/jog/run, Idle, Turn).

Kaynak envanteri (klip kök hızları içerikten ölçüldü, `data/cm_inventory.json`):

| Aile | Klipler | Kaynak kök hızı | UEFN'e aktarılmış (boy oranı ×0,944) | Relaxed karşılığı |
|---|---|---|---|---|
| af_Walk | 8 yön döngü, 4 başlangıç, 4 duruş, 4 pivot, 8 dönüşlü başlangıç | 197 cm/s (1,9 s döngü) | 186 | 165 |
| af_Jog | aynı yapı | 294 | 278 | 375 (Run) |
| af_Run | ileri döngü, başlangıç, duruş, 8 dönüşlü başlangıç | 532 | 502 | 585 (Sprint) |
| Idle / Turn | 12 bekleme, 8 yerinde dönüş | 0 | 0 | — |

Seçilen 82 klip `/Game/Sphirus/Player/GASP/CM/Anim/CM_af_*` olarak kopyalandı (vendor `MC_Core_Motion` değişmedi). Eski V1 `Locomotion` (yürüme 110 cm/s) ve `_NoRM` kopyaları kullanılmadı.

## 3. Aşama 1 — doğal hızlarda kaynak performans

Aynı oyuncu, aynı düz test sahnesi, aynı girdi (`PS` planı: bekle → yürü → dur → Shift sprint → dur → yürü → S), kliplerin kendi hızında: A 165/375/585, B1 186/278/502.
Karşılaştırma tabloları `evidence/sheet_stage1_q34_A_vs_B1.png`, `sheet_q34_A_vs_C.png`, `sheet_side_A_vs_C.png`, `sheet_rearview_A_vs_C.png` (arkadan), `sheet_faceview_A_vs_C.png` (önden) — üst sıra A, alt sıra B/C; yan ve 3/4'te 2, 3, 4, 8, 9, 11. saniye, arkadan/önden 0, 2, 3, 8, 9, 11. saniye.

Görsel inceleme (benim; kullanıcı kabulü değil) — **VISUALLY_INSPECTED**:
- **Sprint / koşu:** A gövdeyi öne kapatıyor, başı eğik, kollar geniş açık (sporcu sprinti). Core Motion kadın koşusu dik, kollar gövdeye yakın, el bilekleri rahat.
- **Fren:** A sprint duruşunda belirgin öne katlanma ve çömelme; Core Motion dik, dizlerle yük alarak duruyor.
- **Yürüme:** Core Motion adımı tek çizgiye yakın, kalça abartısız; kol salınımı A'dan geniş (salınımın arka ucunda eller hafif dışa açılıyor — görsel risk olarak not).
- **Bekleme:** iki aile de sakin; Core Motion ağırlık aktarımı daha belirgin.

Klip düzeyinde (sürücü iskeleti, `data/posture_clips.json`): üst kol açılması yürümede 8,6° (Relaxed 16,5°), koşuda 17° (Relaxed sprint 39°); gövde eğimi koşuda 21° (Relaxed sprint 24°). Aktarım kaynağa sadık: omuz yüksekliği, kol açısı, gövde eğimi ve ayak açısı kaynakla aynı ±1–4° içinde.

**Seçim:** taban aile = Core Motion kadın (bekleme, yürüme, jog, koşu, başlangıç, duruş, pivot, yerinde dönüş). Zıplama, iniş, çömelme, kayma ve traversal Relaxed'da kaldı (Core Motion'da kadın karşılığı yok).

## 4. Core Motion'ı GASP'a doğru taşımak (kök nedenler ve düzeltmeler)

Her biri önce oyunda yeniden üretildi, ilk bozuk olay bulundu, tek hedefli düzeltildi ve aynı testle doğrulandı.

| # | Belirti (oyunda) | Kök neden | Düzeltme | Durum |
|---|---|---|---|---|
| 1 | Görünür beden kapsülden 3 m önde koşuyor | Kopyalarda `EnableRootMotion`/`ForceRootLock` kapalı (kaynaktan miras); kök hareketi pozda kalıyor | 82 klipte açıldı (`w4_rm.py`) | IMPLEMENTED, TECH_TESTED |
| 2 | Ayaklar hiç kalkmıyor, kapsül altında sabit | Core Motion iskeletinde `ik_foot_*`/`ik_hand_*` yok; GASP FootPlacement + LegIK ayakları referans pozdaki IK kemiklerine çekiyor | IK kemikleri her karede FK ayak/ele yazıldı, doğrulama hatası 0,0 cm (`w5_ikbones.py`) | IMPLEMENTED, TECH_TESTED |
| 3 | Sprint 135/180'de yengeç gibi yan adım klipleri | Relaxed seçim tablosunun yön ayrımı (F/B/LL/LR/RL/RR) tek 8 yönlü veritabanında kayboluyordu | Yöne göre 32 veritabanı (F/B/L/R × döngü/başlangıç/pivot + duruşlar), 49 eşleme (`w9_dbdir.py`, `w10_abpmap.py`) | IMPLEMENTED, TECH_TESTED (PARTIAL: sprint 180) |
| 4 | Klip döngü sınırında sürekli yeniden seçim | Veritabanı maliyet ayarları varsayılan (−0,01); Relaxed döngülerinde −0,05..−0,5 | Her CM veritabanı yerini aldığı Relaxed veritabanının devam/temel/döngü maliyetlerini aldı (`w8_dbbias.py`) | IMPLEMENTED |
| 5 | Koşuda sol ayak her basışta 13 cm havada | Döngü kliplerinde `loop=False`; Pose Search döngü sonunda yörüngeyi kesip başa dönüyor, iki faz karışıyor, IK hedefi doğrusal karıştığı için basan ayak havada | 20 döngü klibinde `loop=True` (Relaxed ile aynı kural) (`w12_loop.py`); ayırma testi: `a.AnimNode.LegIK.Enable 0` ayağı indiriyor, FootPlacement kapatmak indirmiyordu | IMPLEMENTED, TECH_TESTED (sol ayak 13 → 2,3 cm) |
| 6 | (sözleşme) FootPlacement temas eğrisi bulamıyor | GASP FootPlacement `PlantSpeedMode=Manual`, `contact_l/r` eğrilerini okuyor | `contact_l/r`, `movedata_speed` eğrileri ayak hareketinden üretildi (`w11_curves.py`) | IMPLEMENTED |
| 7 | Kalkışta atılma, ayak kayması | GASP ivmesi 800 cm/s² (0,2 s'de tam hız); CM kalkışları 0,9–1,4 s | Yürüme 350, jog 420, sprint 450→350 cm/s² (`w7_accel.py`) — gecikme eklenmedi, hız değişimi yumuşadı | IMPLEMENTED, TECH_TESTED |
| 8 | Durmada ayak kayması | Fren 380–780 cm/s² Relaxed duruşlarına göreydi; CM duruşları daha uzun | `BrakeDecelLow/High` 260/520 | IMPLEMENTED, TECH_TESTED |

Retarget: `Rig/RTG_Sph_CM_to_UEFN` (IK_CoreMotion_MCPaul → IK_UEFN_Mannequin, bacak/ayak zincirleri 1:1, Root zinciri eşlenmedi, Root Motion op hedef kökü `root`, hedef poz otomatik hizalı). Önceki 7 Kasım Core Motion denemesinin iki tuzağından (pelvisi yere çeken kök op, 3'e 4 bacak eşlemesi) kaçınıldı.

Sürücü bağlantısı: `ABP_Sph_GASP.Update_MotionMatching` içinde Relaxed seçim tablosunun çıktısı (hız/yön/duruma göre `ValidDatabases`) korunuyor; `SphCM=True` iken her Relaxed veritabanı `CM_Keys/CM_Vals` eşlemesiyle karşılık gelen kadın veritabanına çevriliyor, eşlemesi olmayanlar (zıplama, iniş, çömelme, kayma, traversal) aynen kalıyor. `SphCM=False` A'ya birebir döner.

## 5. Aşama 2 — hedef tempo: hız, kadans, ivme, fren

| | Bant (brif) | Önce (A) | Şimdi (C) | Nasıl |
|---|---|---|---|---|
| Ev içi yürüme | 140–150 | 150 | **150** | yürüme 160 × ev içi ölçek 0,9375 (oynatma ≈ 0,81) |
| Dış yürüme | 150–165 | 165 | **160** | CM yürüme döngüsü 186 → Motion Matching oynatma hızı ≈ 0,86 |
| Jog / koşu | 280–320 | 375 | **290** | CM jog 278 → oynatma ≈ 1,04 |
| Hızlı koşu (Shift) | 480–520 | 585 | **500** | CM koşu 502 → ≈ 1,0 |
| İvme | — | 800 / 800 / 800→300 | **350 / 420 / 450→350** | kalkış klipleriyle uyumlu, gecikme yok |
| Fren (bırakma hızına göre) | — | 380–780 | **260–520** | CM duruş klipleri |

Oynatma hızı: GASP Motion Matching düğümünün kendi `PlayRate` aralığı **0,80–1,05** (önce 0,85–1,15) — klip yalnız bu aralıkta kapsül hızına uydurulur; bütün animasyonlar global yavaşlatılmadı, yürüme klibi koşu için hızlandırılmadı (gait'ler ayrı aileler). Stride Warping düğümü bu sürücüde yok ve eklenmedi; yürümede adım uzunluğu kaynakta kaldı, yalnız kadans ~%14 düştü → **VISUAL_REVIEW_REQUIRED** (ağır çekim izlenimi verip vermediği kullanıcı kararı).

Ölçülen (üretim C, sabit 30 kare/s adım):

| Test | C | A |
|---|---|---|
| 30 s yürüme: klip | tek `CM_af_Loco_Walk_Fwd` döngüsü, 4 değişim | tek Relaxed döngü, 3 |
| 30 s yürüme: temas başına ayak kayması p50 / p90 | **1,8 / 4,2 cm** (54 temas) | 3,0 / 4,7 cm |
| 20 s koşu: temas başına kayma p50 / p90 | **1,0 / 4,2 cm** (29 temas) | 3,3 / 6,1 cm |
| Yürüme duruşu (bırak → 0) | 0,63–0,67 s | 0,47 s |
| Sprint duruşu | 1,10–1,17 s, ~280 cm | 0,83 s / 260 cm |
| 0 → 500 cm/s | yarıya 0,63 s, %90'a 1,36 s | daha hızlı (800 cm/s²) |

Gait geçişi: Shift basılınca kalkış → jog kalkışı → koşu dönüşlü kalkışı → koşu döngüsü; bırakınca koşu duruşu → jog duruşu → bekleme (kayıt `CM_run20_C1`, `CM_game_C1`). Evde Shift: ev içi bağlam koşmayı engelliyor (önceki tur korundu, bu turda değiştirilmedi; ev içi hız 150 ölçüldü — bkz. §9).

## 6. Omuz, kol, omurga

Görünür MetaHuman bedeninden ölçüldü (oyun kaydı, `data/summary_A_B_C.md`):

| Ölçüt (yürüme / koşu) | A (Relaxed) | C (Core Motion) |
|---|---|---|
| Omuz hattı boyun tabanına göre (cm) | −5,8 / −3,4 | −5,4 / −4,8 |
| Köprücük yükselme açısı | −3,8° / +0,9° | −2,0° / −0,4° |
| Köprücük öne açısı (+ = omuz önde) | +2,3° / +8° | −2,1° / −4° |
| El açıklığı (yanal) | 45–47 cm | 23–37 cm |
| Gövde öne eğimi (koşu) | 26–34° | 23° |

- "Omuz düşük": iki ailede de omuz hattı boyun tabanının ~5 cm altında; önceki turun köprücük −5° retarget düzeltmesi (UEFN→MH) korundu, yeni ofset **eklenmedi**.
- "Omuz geriye gerilmiş": açı ölçüsü C'de omzu A'dan 4–5° daha geride gösteriyor (kaynak kadın performansının dik duruşu: kaynak klipte de omuz hattı göğüs kemiğinin 2,1 cm gerisinde, Relaxed'da 0,6 cm önünde — `data/posture_clips.json`). Ön/arka karelerde göğüs öne itilmiş veya kürek kemikleri sıkışmış görünmüyor; kollar gövdeye yakın ve gevşek → **VISUALLY_INSPECTED, karar kullanıcıda**. Sabit ek ofset yığılmadı (brif §6).
- Koşu duruşu: A'nın öne kapanan, kolları açık sprinti yerine dik, kompakt kadın koşusu (bkz. `sheet_side_A_vs_C.png`, `sheet_faceview_A_vs_C.png`).
- Omurga: kaynak mocap pelvis–göğüs karşı dönüşünü taşıyor; SHME göğüs öncülüğü/yerleşme katmanı (önceki tur) bunun üstüne küçük genlikle ekleniyor (§8).

## 7. Dönüşler

Klavye (kamera sabit, düz sahne; `CM_kturn_C1`, yan `CM_kturnS_C1`):

| Dönüş | Giriş → en düşük → çıkış (cm/s) | Yeni yöne ulaşma | Klipler | Durum |
|---|---|---|---|---|
| Yürüme 45° | 160 → 160 → 160 | 0,17 s | `Walk_Fwd` → `Walk_FwdRight` → `Walk_Fwd` (akış) | TECH_TESTED |
| Yürüme 135° | 160 → 63 → 160 | 0,30 s | döngü + çapraz döngü | TECH_TESTED |
| Sprint 45° | 500 → 495 → 500 | 0,27 s | `Run_Fwd` (yönlendirme) | TECH_TESTED |
| Sprint 135° | 500 → 107 → 397 | 0,70 s | `Run_Start_TurnR135` → `Jog_FwdRight` → `Run_Start_TurnR090` | PARTIAL (3 klip) |
| Sprint 180° | 497 → 4 → 320 | 0,63 s | `Run_Start_TurnL180` → `Jog_FwdRight` → `Jog_FwdLeft` → `Jog_Start_TurnL135` → `Run_Fwd_Start` | **PARTIAL** (1,5 s'de 5 klip; Core Motion'da hareket hâlinde sprint dönüşü yok, durup dönerek kalkış klipleri kullanılıyor) |
| Yürürken 180° (S) | 160 → 5 → 160 | 0,33 s | `Walk_Start_TurnR180_Rfoot` | TECH_TESTED |

Fare: kamera yaw'ı tek başına fren üretmiyor (önceki tur kuralı, değişmedi); bu turda ayrı fare dönüşü kaydı alınmadı → **NOT_TESTED** (bu tur).
Zıplama/iniş: Relaxed içerik ve önceki turun yerdeyken zıplama-başlangıç filtresi korundu; küçük basamaktan inişte tam iniş toparlanması bu turda yeniden ölçülmedi → **NOT_TESTED** (bu tur). Ev rotasında basamak inip çıkma iniş klibi seçmedi (§9).

## 8. SHME ve efor

Korunan (önceki turda kurulmuş, bu turda değiştirilmedi, Core Motion üstünde çalışıyor): `AC_Sph_Motion` efor birikimi/sönümü, fiziksel fren (bırakma hızına göre), ivme ölçeği, yerleşme yayı (frende göğüs ileri ~1,7° → geri), dönüşte göğüs öncülüğü, efor eğimi, nefes. Değişen: fren aralığı 260–520 (Core Motion duruşlarına göre).

Kaynak klibin zaten karşıladığı (ikinci kez eklenmedi): ilk adım öncesi ağırlık aktarımı ve 45–180° dönüşlü kalkışlarda basan ayak (`af_Loco_*_Start_Turn*_Lfoot/Rfoot`), fren basışında diz yük emilimi (duruş klipleri), pivotlarda eski yönü söndürüp yeni yöne itiş (`*_Pivot`).

Efor açık/kapalı (aynı girdi, üretim C, `data/effort_ab_C1.md`, videolar `C_effort_on.mp4` / `C_effort_off.mp4`): 

| Ölçüt | Efor kapalı | Efor açık |
|---|---|---|
| İlk sprint, yarı hıza / %90'a | 0,63 / 1,36 s | 0,64 / 1,37 s (ilk manevra ağırlaşmıyor) |
| 2. tersleme sonrası ulaşılan hız | 420 cm/s | 378 cm/s |
| 3. tersleme sonrası | 340 cm/s | 289 cm/s |
| Efor E / ivme çarpanı (en düşük) | 0 / 1,00 (anahtar gerçekten kapalı) | 0,78 / 0,82 |
| 5 s dinlenmeden sonra sprint | 459 cm/s | 424 cm/s (E 0,78 → 0,32) |
| Sprint duruşu | 1,07 s / 278 cm | 1,16 s / 278 cm |

Efor hız, ivme ve toparlanmada ölçülüyor; komut gecikmesi yok, sakin yürüyüşte efor neredeyse birikmiyor (30 s yürümede E en çok 0,08; ardışık sprint terslemelerinde 0,78). Görünür beden farkı (nefes + ~2° efor eğimi) küçük → **PARTIAL / VISUAL_REVIEW_REQUIRED**. Dönüş/fren basışında yük emilimi ve yeniden itiş Core Motion kliplerinden geliyor; SHME'nin ayrı itiş/fren klip üretimi bu turda yeniden kurulmadı.

## 9. Oyun akışları (ev, kapı, istasyonlar, kayıt)

Gerçek ev haritası, gerçek tuşlar; ışınlama yalnız başlangıç konumu. Etkileşim hedefi (Story Framework `TargetInteractionActor`) her karede kayda yazıldı (`data/gameplay_flows_C.txt`).

| Akış | Ne oldu | Durum | Video |
|---|---|---|---|
| Üst kat kapısı (`GR_Day_WardDoor`) | Yürü → imleç kapı küresine (r=24 cm) → hedef oluştu → E → karakter kendi yürüyüp kapıya hizalandı, `AM_GR_Day_Reach` → kapı açıldı → W ile odaya girildi | TECH_TESTED | `C_house_door_E.mp4` |
| Mutfaktan çıkış + basamak + koşu + dönüş + eve dönüş | İçeriden 150 cm/s → arka mutfak kapısından (`SPH_Door_RearKitchenDoor` açık) basamaklardan indi (z 238→170) → dışarıda 500 cm/s → 1,8 s'de durdu → 180° → geri yürüdü → basamaklardan çıktı → içeride | TECH_TESTED (iniş toparlanması seçilmedi) | `C_house_exit_steps_return.mp4` |
| Odun toplama + kesme | Odun yığını → E → `AM_GR_Day_Pick` → kucakta taşıma (`AM_GR_Day_CarryArms`) ile kütüğe yürüme → E → `AM_GR_Day_Chop` hazır duruş → sol tık → tek vuruş → yarılmış odun (`GR_Day_Piece1`) | TECH_TESTED | `C_wood_pick_chop.mp4`, `evidence/sheet_chop_flow_C.png` |
| Ev içi Shift | Koridorda Shift basılıyken gait yürüme kaldı, en çok 150 cm/s | TECH_TESTED | `C_house_hall_shift150.mp4` |
| Oyun içi kayıt/yükleme | Kayıt (1386,−696) yön 180 → 7 m uzağa → `LoadGame(IgnorePlayerLocation=False)` → konum/yön birebir → yükleme sonrası yürüme 160 | TECH_TESTED | `data/save_load_C.txt` |
| Tek piyon / eski sürücü yok | Oyunda 1 `BP_HybridA_Player`; AnimBP'ler `ABP_Sph_GASP` + `ABP_Sph_Body_GASP` + yüz; `ABP_Sph_Driver` yok | TECH_TESTED | `data/save_load_C.txt` |
| 60 s bekleme | 2 seyrek bekleme kırılması (17,1 s, 53,1 s), kapsül kayması 0 | TECH_TESTED | `C_final_idle60.mp4` |
| Yeniden açılış | Editör kapatılıp açıldı; oyuncu zincirindeki 5 BP `UP_TO_DATE`; CDO: `SphCM=True`, 160/290/500, fren 260/520 | TECH_TESTED | — |

**Önceki turlarda "E istasyonu açmıyor" sonucunun gerçek nedeni** (bu turda bulundu): (1) Story Framework hedefi yalnız kamera ışını istasyonun küçük etkileşim küresine (kapı 24 cm, kütük 46 cm) değince oluşuyor — eski test kamerayı sabit −22°'de tutuyordu, ışın küreyi kaçırıyordu; (2) kesme istasyonu tasarım gereği `GR_Wood > 0` istiyor — yeni oyunda önce odun toplanmalı. Hareket sistemiyle ilgili bir engel değildi; kod değiştirilmedi.

NOT_TESTED: yatağa giriş/kalkış, çay/kapak tutuşu, maske taşıma (bu turda tam akış çalıştırılmadı), menü üzerinden kayıt/yükleme, gerçek eğim/merdiven (yalnız mutfak basamakları), kapıdan Shift tutarak çıkış.

## 10. 30/60 FPS ve performans

| Test | Sonuç | Durum |
|---|---|---|
| Sabit 30 / 60 kare/s adım, aynı girdi (`C_final_gamecam` / `C_final_fps60`) | yürüme duruşu 0,63 / 0,60 s, sprint duruşu 1,17 / 1,15 s, yürürken 180° yeni yöne 0,33 / 0,32 s; klip dizisi aynı (60'ta 2 kısa ek geçiş, ayak fazına bağlı) | TECH_TESTED |
| Zaman ölçeği değiştirilmemiş oynanış, ekran görüntüsü yok, 35 s (`data/gameplay_flows_C.txt` sonu) | C: kare süresi p50 41,7 / p95 42,2 / p99 42,6 ms, en çok 90 ms, >50 ms 3 kare; A aynı protokol: 41,7 / 42,2 / 42,6, en çok 85 ms, >50 ms 1 | PARTIAL — editör oturumu ~24 kare/s'ye kilitli görünüyor (p50 = p95); Core Motion ailesi fark yaratmadı ama gerçek GPU/CPU maliyeti **NOT_TESTED** |
| Cook / paket | çalıştırılmadı | NOT_TESTED |

## 11. Olaylar, geri alınanlar, geri alma

- **Kullanıcı kaydı iki kez test sırasında yerinden alındı ve geri kondu.** (1) Arka plana `&` ile başlatılan ilk kayıt dizisi ölü görünüp yaşadı; ikinci dizi paralel çalıştı (iki editör). (2) Bitti sandığım bir dizinin üstüne yenisini başlattım; ikinci dizinin editör yeniden başlatması birincinin oyun oturumunu kesti ve kayıt kenarda kaldı. Her iki seferde dosya, testin kenara aldığı kopyadan (`videos/<etiket>/slot_before.sav`) SHA1 `8622025b…` doğrulanarak geri kondu; eski günlerden yedek kullanılmadı. Önlem: kayıtlar artık meşgul korumalı `cmrun.sh` ile başlıyor; dizi başına süre sınırı kaldırıldı.
- **Geri alınan / kullanılmayan denemeler:** ilk 14 yönsüz CM veritabanından 8'i (yerine yöne göre bölünmüş 32 veritabanı); B1 (doğal hızlar 186/278/502, tempo dışı); MM oynatma hızını tek başına kullanan B2 (kalkış/duruş kayması); ayak sorununu temas eğrisinde arayan deneme (eğriler sözleşme gereği kaldı, ama düzeltme `loop` bayrağı oldu). Ayak yerleşimi/IK kapatma testleri yalnız konsol değişkeniyle, kalıcı değişiklik yok.
- **Yazma kapısı çalıştı:** oyun oturumu açıkken gönderilen yazma işi reddedildi (`REFUSED_PIE`), eski kuyruk işi taşındı (`STALE_JOB`).
- **Geri alma:** `C:\Users\berat\SphirusCheckpoints\WomanMotion_Pre_20261110_2255` içeriğini `Content/Sphirus/Player` ve `Content/Sphirus/CharacterLab/Hazel_20261106/Playable` üzerine kopyalamak (editör kapalıyken) üretimi A'ya döndürür; yeni `CM/` klasörü referanssız kalır. Daha hafif yol: `ABP_Sph_GASP.SphCM=False` + hızlar 165/375/585 + fren 380/780 (`cm_cfg.py` 'A').

## 12. Açık kalanlar

1. **Kullanıcı oynayarak kabul etmedi.** Koşu/fren/duruş görsel kararı, yürümede ~%14 düşük kadansın ağır çekim izlenimi verip vermediği, kol salınımının genişliği ve omuz konumu senin kararın.
2. **Sprint 135°/180°:** 1,5 s'de 3–5 klip değişimi (PARTIAL). Core Motion'da hareket hâlinde kadın sprint dönüşü yok; duruş + dönüşlü kalkış klipleri kullanılıyor. İki iyileştirme yolu: proje-sahipli bir "fren–bas–dön–it" klibi (SHME V2.25/V2.54 üretecinin bu ailede yeniden kurulması) ve aşağıdaki seçim tablosu hatası.
3. **Önceden var olan seçim tablosu hatası:** `CHT_Sph_PoseSearchDatabases_Relaxed` bir iç sütunda `MovementDirection_Recent` değişkenini arıyor; `ABP_Sph_GASP`'ta bu değişken yok (10 Kasım'dan beri, A ve C'yi aynı şekilde etkiliyor). Yön geçmişine bağlı veritabanı seçimi bu yüzden eksik çalışıyor olabilir.
4. **Stride Warping yok:** yürümede adım uzunluğu kaynakta kaldı, yalnız kadans düştü.
5. Fare ile hızlı dönüş, küçük basamaktan düşüş/iniş, gerçek merdiven ve eğim bu turda yeniden ölçülmedi.
6. Yatak, çay/kapak, maske taşıma tam akışları; menüden kayıt/yükleme; cook/paket; gerçek GPU/CPU maliyeti: NOT_TESTED.
7. Ev işi montajları Relaxed/UEFN bedeniyle yazılmış; Core Motion bekleme duruşuyla montaj giriş/çıkışında tavır farkı görsel olarak denetlenmedi.

## 13. Videolar ve veri

Hepsi PIE, sabit oyun adımı (30 kare/s; `C_final_fps60` 60), gerçek hızda kodlandı (oyun saati = video süresi), aynı kırpma. Ham animasyon/varlık yok.

| Video | İçerik |
|---|---|
| `A_relaxed_q34/side/rearview/faceview`, `A_relaxed_walk30`, `A_relaxed_run18` | A (önceki üretim) |
| `B1_coremotion_natural_q34/rearview/faceview` | B, Aşama 1: Core Motion doğal hızlarda (186/278/502) |
| `C_final_q34/side/rearview/faceview`, `C_final_gamecam` | C, aynı girdi (bekle → yürü → dur → sprint → dur → yürü → S) |
| `C_final_walk30`, `C_final_run20`, `C_final_idle60` | uzun yürüme, koşu, bekleme |
| `C_final_keyturns`, `C_final_keyturns_side`, `C_final_brake` | klavye 45/135/180 (arka/yan), fren ve tersleme |
| `C_effort_on`, `C_effort_off` | efor A/B, aynı girdi |
| `C_final_fps60` | 60 kare/s |
| `C_house_door_E`, `C_house_exit_steps_return`, `C_wood_pick_chop`, `C_house_hall_shift150` | gerçek ev akışları |

Veri: `data/summary_A_B_C.md` (+ `.json`: aday, klip değişimi, temas başına kayma, görünür beden duruşu), `data/turns_stops_C1.txt`, `data/effort_ab_C1.md`, `data/gameplay_flows_C.txt`, `data/save_load_C.txt`, `data/cm_inventory.json`, `data/posture_clips.json`, `data/cm_map2.json` (Relaxed → CM eşlemesi), `data/w9_windows.json` (arama pencereleri), `data/w11_curves.json` (temas oranları). Değişiklik listesi: `changes/changes.md`. Karşılaştırma tabloları: `evidence/` (ayrıca `sheet_door_exit_C.png`: üst sıra kapı, alt sıra mutfak çıkışı).
