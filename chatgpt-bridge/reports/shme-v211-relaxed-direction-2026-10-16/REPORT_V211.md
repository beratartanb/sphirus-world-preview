# SHME V2.11 — Rahat kollar, kamera–girdi–karakter yönü, ivmelenme ve fren (2026-10-16)

**İstek:** V2.10'un teknik onarımlarını koruyarak:
- karakterin rahat hareket dilini (yürüme başlangıcında kollar, yerinde dönüşte kollar) düzelt;
- kamera, girdi ve karakter yönü arasındaki ilişkiyi düzelt;
- hızlanma ve frenin animasyonda görünmesini sağla;
- her şikâyeti, kanıtıyla birlikte tek tek raporla.

Kullanıcı kabulünü kendim verilmiş saymadım. Teknik sonuç, benim görsel incelemem ve kullanıcı kabulü her bölümde ayrı yazıldı.

## Sonuç (kısa)
- **Yürüme başlangıcında kolların içe kapanması** (ilk kabul koşulu) — *teknik: büyük ölçüde çözüldü, bir kalıntıyla PARTIAL*:
  - **Sahip 1:** CP başlangıç klipleri (`A_LS_M_Relaxed_Walk_Start_F_Rfoot/Lfoot`). Bu kliplerde kollar başlangıç boyunca rahat idle'dan 3–7° daha dar taşınıyordu; içlerinde V2.5/2.6'nın sabit +9° bake'i zaten vardı.
  - **Sahip 2:** yürüyüş döngüsünün (`A_LB_Walk_Fwd`) dar kollu döngü turları. Başlangıç tam bunların başına devrediyordu.
  - **Düzeltme:** yalnız kol zinciri yeniden yazıldı.
    - Taşıma (kolun gövdeye göre açısı) gövde çerçevesinde idle'dan yürüyüşe kesintisiz geçiyor.
    - Dirsek ve bilek idle'dan başlayıp klibin kendi hareketine dönüyor.
    - Salınım klibin kendisi.
  - **Ölçüm (uzun idle → W):**
    - Sol dirseğin hem idle hem yürüyüşün içinde kaldığı süre 0.70 → 0.17–0.23 s.
    - Sağ kol başlangıçta 0.15 s'de 24.0 → 20.4 cm'ye kapanıp 0.6 s kalıyordu; artık idle'dan yürüyüş taşımasına yumuşak geçiyor.
  - **Kalıntı:** yürüyüş döngüsünün 2.9–3.3 s'lik dar sağ kol fazı. Durup sol ayakla yeniden başlamada ve yerinde dönüşten sonra W'de, başlangıçtan ~0.5 s sonra kısa bir sağ kol içe gelişi görünebiliyor (§2.4).
- **Yerinde dönüşte "aksiyon karakteri" kolları** — *teknik: çözüldü*:
  - Sahip: AAMS Neutral dönüş kopyaları (`SHM_M_Neutral_Stand_Turn_*`).
  - Adımlar ve zamanlama korundu. Kollar kendi dinlenme pozları etrafında yumuşatıldı; dirsek ve bilek idle'dan alındı.
  - Ellerin idle'ın dışına çıkışı (medyan): hızlıda +10.7 → +4.5 cm, yavaşta +11.3 → +3.0 cm. Küçük doğal salınım kaldı.
- **Kamera–girdi yönü** — *teknik: çözüldü*:
  - İdle'da kamera, gövdeden en fazla 55° uzağa bakabiliyordu (2026-09-16 tasarımı). W ise farenin tam yönünü kullanıyordu.
  - Hızlı fare dönüşünden sonra 0.3–0.8 s boyunca ekran ile W yönü **125°'ye kadar** ayrışıyordu.
  - `CameraIdleOrbitMaxYaw` 55 → 180 yapıldı. Fark artık her karede 0.0°.
  - Hareket hâlinde fark zaten ≤ 1.2°. Çift düzeltme (otomatik takip döngüsü) yok.
- **Shift+W → Shift+S ve kamera 180** — *teknik: zaten doğruydu, ölçüldü*:
  - Shift+S: hız sınırı 490 → 300, ama hız anında kesilmiyor; 0.6 s'lik fren pivotu var. Ardından gerçek geri koşu döngüsü, en fazla tempolu hızında (çaprazlar dâhil). Geri depar yok.
  - Kamera 180: fren → depar 180 dönüşü → ileri yeniden hızlanma.
- **Yürüyüş → depar itişi** — *teknik: çözüldü; görsel kabul kullanıcıda*:
  - Önce 0.5 s düz tempolu döngü bekliyordu.
  - Artık rahat koşu başlangıcının itiş bölümü oynuyor (öne eğilme, sürücü adımlar), sonra depar.
  - Aynı itiş ters dönüşlerden sonraki yeniden hızlanmada da görünüyor.
  - Kesişlerde, W+A ↔ W+D'de ve kısa basışlarda tetiklenmiyor.
- **Dünya tepkisi / gerçek toparlama** — *OPEN (içerik yok)*:
  - Olaylar normal / planlı sert / taşma adayı olarak sınıflandı.
  - Taşma adayları: deparda fareyle tam 180 (55–67 m/s² sıçrama), tempolu S+D → S+A.
  - Koşarken yakalama adımı içeriği yok. Doğrulanmış içerik brifi §8'de; sahte kuvvet veya eski kayan toparlama dalı açılmadı.
- **Korunanlar:** diz üreticisi + `leg_guard`, onarılmış diz/idle klipleri, çift zemin uyarlaması düzeltmesi, yerinde dönüşte çift kök telafisinin kaldırılması, V2.10 depar kesiş paketi.
  - Kol bake'i bacak, pelvis, omurga ve köke dokunmadı. Yazma sonrası okumada sapma 0.0° / 0.0 cm.

## 1. Şikâyet tablosu
| # | Şikâyet | Yeniden üretildi mi | Neden (sahip) | Değişiklik | Kanıt | Teknik | Benim görsel incelemem | Kullanıcı |
|---|---|---|---|---|---|---|---|---|
| 1B | Yürüme başlangıcında kollar içe kapanıyor, kalıyor, sonra düzeliyor | Evet: 4 başlangıç türünde | CP başlangıç klipleri dar taşıma + yürüyüş döngüsünün dar kollu turları | Kol zinciri bake (v3) + döngü aykırı tur kaldırma | §2, `start_long_*`, `restart_*`, `tap_*`, `tipw_*` | PARTIAL (§2.4 kalıntı) | Kapanma ve "tutma" kayboldu; sağ kol başlangıçta gövdeye yapışmıyor | Bekliyor |
| 1A | Yerinde dönüşte kollar dışarıda, aksiyon pozu | Evet | `SHM_M_Neutral_Stand_Turn_*` içeriği | Kol yeniden eşleme (adımlar korunarak) | §3, `tip_fast_*`, `tip_slow_*` | PASS | Kol savrulması gitti, küçük salınım var | Bekliyor |
| 2 | Kamera dönerken W/A/S/D anlamı / yön ilişkisi | Evet: idle'da (hareket hâlinde değil) | İdle görsel kamera tutması (`CT_IdleYawOffset`, ±55°) | `CameraIdleOrbitMaxYaw` 180 | §4, `idle_camera_*` | PASS | Ekran ve W aynı yönde | Bekliyor |
| 3 | Shift+W → Shift+S fren + geri (≤ tempolu), kamera 180 ileri | Ölçüldü: zaten doğru | — | Yok (yalnız yeniden hızlanmaya itiş eklendi) | §5, `sprint_to_back_*`, `sprint_cam180_*` | PASS | Fren pivotu ve geri koşu okunuyor | Bekliyor |
| 4 | Yürüyüş → depar itişi görünmüyor | Evet | Hıza göre basamaklı yürüyüş + tempolu döngü rotası | İtiş rotası (rahat koşu başlangıcı) | §6, `walk_to_sprint_*` | PASS | Öne eğilen sürücü adımlar | Bekliyor |
| 5 | Ani ters dönüşlerde momentum | Ölçüldü | Fren/destek/dönüş zaten var; yeniden itiş döngüydü | İtiş rotası ters dönüşlerden sonra da | §7 | PARTIAL (fareyle tam 180 deparda sıçrama) | Yeniden itiş okunuyor | Bekliyor |
| 6 | Dünya tepkisi / gerçek toparlama | Sınıflandırıldı | İçerik yok; tasarım itme tabanlı | Yok (brif) | §8 | OPEN | — | — |
| 7 | 10 kabul zinciri | Kaydedildi | — | — | §9 | Teknik metrikler §9 | §9 | Bekliyor |

## 2. Yürüme başlangıcında kollar (ilk kabul koşulu)
### 2.1 Yeniden üretim ve kayıt (uzun idle → W, `v211a_a_long_base_r1`, görünür MetaHuman)
- **Ölçü:** göğüs çerçevesinde (spine_03 yan ekseni) dirseğin gövde orta hattına yanal uzaklığı ve üst kol abdüksiyonu.
  - Salınıma duyarsız; el yanal mesafesi salınımla değiştiği için ana ölçü değil.
  - Araç: `arms.py --carriage / --detail`.
- **İlk kapanma karesi:** hız 15 cm/s'yi geçtikten +0.02–0.08 s sonra. Sağ dirsek 24.0 → 21.3 → 20.5 cm, abdüksiyon 17.2 → 10.1 → 8.0°.
  - O anki kayıt: CP başlangıç saati 0.24–0.29, `SHM_IdleUpperW` 0.62 → 0.51, PBI alfa 1.0, montaj yok, tutulan poz (`SHM_IdleHold`) yok.
- **Tutma:** +0.14 → +0.71 s boyunca sağ dirsek 20.2–20.9 cm, abdüksiyon 7.5–9.3°. Bu aralıkta CP saati 0.33 → 0.86.
- **Toparlanma karesi:** CP devri 0.88–0.91 (+0.76 s). MM `A_LB_Walk_Fwd` 3.17 s'den devam ediyor; sağ abdüksiyon +0.93–1.10 s'de 12.7–14.2°.
- **Klip, aile, katmanlar:**
  - Gösterilen poz CP başlangıç değerlendiricisinin klibi: sağ ayak başlangıcı `A_LS_M_Relaxed_Walk_Start_F_Rfoot`, sol ayak `..._Lfoot` (`CT_GetCPStartSequence`).
  - MM telemetrisindeki `M_Ranger_Walk_Loop_F_PureForward_CWF` arka planda; gösterilen poz değil.
- **Retarget öncesi / sonrası ve son işlem:**
  - Sürücü iskelet (mx_) ile görünür MetaHuman (vx_) aynı değişimi gösteriyor.
  - Çalışma zamanı kol değerleri, aynı klip zamanındaki klip değerine 0.1–0.6° içinde eşit.
  - Retarget, gövde son işlemi ve `IdleUpperW` sahip değil. `IdleUpperW` kolu açar, kapatmaz.
- **Klip içeriği (çevrimdışı):**
  - Başlangıç klipleri kolları gövdeye göre ort. 8.5 / 10.4° taşıyor; rahat idle 12.5 / 15.0°.
  - Bu kliplerde V2.5/2.6'nın sabit +9° bake'i zaten vardı. Bu yüzden bir sabit açı daha **çözüm değildi**.
- **İkinci sahip:** `A_LB_Walk_Fwd` (6.83 s, 5 tur):
  - Sol kol döngü dikişinde (6.7–0.2 s) 4.6–6.6°, diğer turların aynı fazında 9–15°.
  - Sağ kol 3.1–3.2 s'de 5.5–6.1°, diğer turlarda ~9°.
  - MM başlangıçlardan tam bu bölgelere devrediyordu (3.13–3.17 / 6.567 s).

### 2.2 Değişiklik (`Tools/SHME_V211_20261016/v211_arm_bake.py`, v3)
- Yalnız kol zinciri: köprücük, üst kol, ön kol, el. Kök, pelvis, omurga, bacak, twist kemikleri, eğriler ve zamanlama dokunulmadı.
  - Yazma sonrası okuma: kol izleri hedefe 0.0° eşit; kök/pelvis/omurga/bacak sapması 0.0° / 0.0 cm. `leg_guard` devrede değil.
- **Başlangıç klipleri:**
  - Dirsek ve bilek idle değerlerinden başlıyor, devre kadar (0.88 / 0.77 s) klibin kendi hareketine sönümleniyor.
  - Üst kolun gövdeye göre taşıması (abdüksiyon, gövde ileri ekseni etrafında) idle taşımasından (12.5 / 15.0°) döngü ortalamasına (12.2 / 10.7°) yumuşak bir yol izliyor; en büyük sapma 0.24°.
  - Klibin salınımı (ileri-geri) aynı kaldı.
- **Yürüyüş döngüsü:** her kolda, diğer turların aynı yürüyüş fazından > 1° dar kalan kareler o faz ortalamasına çekildi (71 / 74 kare). Ortalamalar değişmedi: 11.9 → 12.2 / 10.4 → 10.7°.
- **Kaynak:** her bake orijinal anahtarlardan başlıyor, böylece tekrarlanabilir. Bu amaçla 11 orijinal kopya `/Game/ActionAdventureMovementS/Rollbacks/SHME_V211_Arms_Before_20261016/` altına alındı.
- **Kurallara uyum:**
  - Blend süresi uzatılmadı (`IdleUpperFallTau` 0.3 aynı).
  - Sabit açılı genel additive yok; değişiklik klip içeriğinde ve zamana bağlı.
  - Gövde inceltilmedi.
  - Başlangıç klibindeki diz onarımı bu düzeltme diye raporlanmadı.
  - Reddedilmiş başlangıç adayı (`SHM28_StartMode 1`) açılmadı; hâlâ 0.

### 2.3 Dört başlangıç: önce / sonra (son kayıtlı üretim, `v211a_*` → `v211z_*`)
Ölçü: başlangıçta (0–0.8 s) dirsek yanal mesafesi ve abdüksiyon medyanı. "İçeride" = 0–1.6 s içinde dirseğin hem idle'ın hem yürüyüşün 1 cm içinde kaldığı süre.

| Başlangıç | Kol | Önce: başlangıç dirsek / abd. | Önce: içeride | Sonra: başlangıç dirsek / abd. | Sonra: içeride |
|---|---|---|---|---|---|
| Uzun idle → W | Sol | 20.5 cm / 11.5° | 0.70 s | 21.1 cm / 12.8° | 0.17–0.23 s |
| Uzun idle → W | Sağ | 20.6 cm / 8.3° (idle 23.8 / 17.0'dan 0.15 s'de) | 0.00 s | 23.4 cm / 15.1° (yürüyüşe 20.6'ya yumuşak) | 0.00 s |
| Dur → hemen W (2 kez) | Sol | 21.1 / 12.6° | 0.27 / 0.13 s | 21.1–21.2 / 13.1–13.2° | 0.30 / 0.40 s |
| Dur → hemen W (2 kez) | Sağ | 22.0–22.1 / 13.8–14.0° | 0.12 / 0.16 s | 22.1 / 13.9–14.0° | 0.59 / 0.28 s (§2.4) |
| Kısa bas → bırak → tekrar | Sol (tekrar basış) | 20.9 / 12.6° | 0.97 s | 20.9 / 12.2° | 0.37 s |
| Yerinde 90° → W | Sol | 20.6 / 11.8° | 0.56 s | 21.2 / 13.4° | 0.20 s |
| Yerinde 90° → W | Sağ | 20.6 / 8.4° | 0.00 s | 21.9 / 14.0° | 0.59 s (§2.4) |

- **Görsel (ön-çapraz, aynı zamanlar):** `img/start_long_before_v2_v3.jpg`.
  - ÖNCE: sağ kol ilk adımda kalçaya yapışıyor.
  - SONRA: kol yanda doğal asılı, sonra salınıyor.
- **Reddedilen ara denemeler (kanıt saklı):**
  - v1: idle yerel dönüşleri tüm zincire + tek taşıma ofseti. Sol kol yürüyüşten 5–6° fazla açıldı, sağ kol değişmedi.
  - v2: tüm zincire idle yerel + gövde çerçevesinde taşıma. Sayılar iyiydi ama çekimde **kol geriye tutuluyordu**: elin 18–30 cm gövde arkasında.
  - v2'nin nedeni: idle'ın köprücük/üst kol yerel dönüşleri, göğsü farklı eğik başka bir gövdede kolu geriye itiyor. Yerel dönüş yalnız dirsek ve bilek için taşınabilir.

### 2.4 Kalıntı (PARTIAL)
- **Konum:** yürüyüş döngüsünün 2.9–3.3 s'lik sağ kol geri salınımı.
  - Çevrimdışı aykırı tur kaldırmayla 3.7–5.4° → 6.8–9.4°'ye çıktı.
  - Oyunda hâlâ ~4–6° (dirsek 17.4–18.4 cm) görünüyor.
- **Ne zaman görünüyor:** sol ayak başlangıcı bake sonrası döngüye 2.4–2.5 s'den devrettiğinde (dur → W, yerinde dönüş → W). Bu durumda başlangıçtan ~0.5 s sonra ~0.3 s'lik kısa bir sağ kol içe gelişi.
- **Önerilen sonraki adım:**
  - döngünün o turunu, aynı fazda en geniş turdan yeniden yazmak; ya da
  - MM'nin sol ayak devrini bake öncesi faza (6.57 s) yönlendirmek.

## 3. Yerinde dönüşte kollar
- **Gerçek klip ve çalışma zamanı kaydı:**
  - `BP_GR_Player.GR_UpdateIdleTurn`, DefaultSlot dinamik montajı olarak oynatıyor.
  - Klipler: `/Game/GraceRanger/SHME/Animations/Turns/SHM_M_Neutral_Stand_Turn_{045,090,135,180}_{L,R}`; AAMS `/Game/AAMS/AAMS/Animations/Locomotion/Idle/M_Neutral_Stand_Turn_*` kopyaları.
  - Telemetri: `mont` / `mona`.
  - İçerik: dinlenme abdüksiyonu 17–18° (idle 13–14°); dönüşte 28°'ye, eller 41–51 cm'ye açılıyor.
- **Adaylar incelendi (`turnclip_table.py`):**
  - Core Motion `af_Stand_Idle_Turn*`: stil uyumlu ama %10–90 dönüş 1.6 s ve adımsız sürünme.
  - `A_LS_M_Relaxed_Stand_Turn`: kollar fazla kapalı (0–5°).
  - Karar: AAMS'nin adım ve zamanlaması korundu, yalnız kollar kontrollü olarak yeniden yazıldı.
- **Değişiklik:**
  - Omuz zinciri klibin kendi dinlenme pozu etrafında yumuşatıldı (köprücük 0.3, üst kol 0.4 kazanç).
  - Dirsek/bilek idle'dan, hareketleri 0.5 / 0.6 kazançla.
  - Dinlenme taşıması idle'ın gövde çerçevesindeki taşımasına oturtuldu (sol −5.4°, sağ −2.3°).
  - Kollar dondurulmadı.
- **Ölçüm (7 dönüş, son üretim):**

| Senaryo | Önce: el idle'ın dışına (medyan / max) | Sonra | Önce: dirsek (medyan) | Sonra | Önce: maks. abd. medyanı | Sonra |
|---|---|---|---|---|---|---|
| Hızlı (720°/s) | +10.7 / +17.9 cm | +4.5 / +8.4 cm | +5.5 cm | +2.1 cm | 28.5° | 19.3° |
| Yavaş (60°/s) | +11.3 / +14.2 cm | +3.0 / +7.4 cm | +5.9 cm | +1.5 cm | 24.1° | 17.8° |

- **Görsel:** `img/tip_fast_before_after.jpg`. ÖNCE: kol yana savruluyor; SONRA: aynı anda vücuda yakın küçük salınım. `tip_fast_*`, `tip_slow_*`.
- Montaj sıçramaları önceki ile aynı sınıfta (önce 2–6, sonra 0–3; en kötü 28–44 → 26–28 m/s²).

## 4. Kamera – girdi – karakter yönü
- **Zincir (canlı grafik dökümü, `Saved/Codex/SHME_V211_20261016/Graphs/`):**
  - W/A/S/D: `BP_ExampleCharacter_MotionMatching` EventGraph `IA_Move` → `GetRight/ForwardVector(GetControlRotation.yaw)` → `AC_State_AAMS.DetermineMovement` → `AddMovementInput`.
  - Kontrol yaw'ı her karede `TW_CameraWorldYaw`'a eşitleniyor (`BP_GR_Player` EventGraph, LookDrivenLocomotion).
  - Ekran: `GR_UpdateRig` boom yaw'ı = `CT_VisualCameraYaw` = kontrol yaw'ı + `CT_IdleYawOffset` + `CT_CounterYaw` (`CT_UpdateCameraResponse`).
  - `CT_IdleYawOffset`, idle'da kamerayı gövdenin ±`CameraIdleOrbitMaxYaw` (55°) içinde tutuyordu (2026-09-16 "arka orbit sınırı").
- **Tek zaman çizelgesi (`dirtl.py`):** ekran kamerası yaw'ı, kontrol yaw'ı, istenen dünya yönü (kontrol + çubuk açısı), CMC ivme yönü, hız yönü, kapsül, görünür göğüs yaw'ı.

| Durum (önce) | ekran − girdi maks. | ivme − istek maks. | sonda hız − ivme | sonda kapsül − hız | sonda göğüs − kapsül | hız yerleşmesi |
|---|---|---|---|---|---|---|
| İdle, fare 90/−90/180 sonra W | **125°** (yalnız hareket ederken 35°) | 0° | 0° | 0 / −14° | 5–6° | 0.31–0.63 s |
| Yürüyüş, W + fare 120°/s | 0.1° | 6° | 0° | 0° | −2.5° | 0.31 s |
| Tempolu, W + fare | 0.7° | 18° | 0° | 0° | −10° | 0.19 s |
| Depar, W + fare | 1.2° | 26° | 0° | 0° | +10° | 0.16 s |
| Geri yürüyüş (S) + fare | 0.1° | 25° | 0.1° | −180° (geri adım) | −2° | 0.31 s |
| Geri tempolu (S) + fare | 0.4° | 6° | 0.2° | −180° | +5° | 0.29 s |
| Tempolu D / A / S+D / S+A | 0.3–0.5° | 4° | ≤ 0.8° | −89 / +89 / −134 / +134° | — | 0.23–0.55 s |
| Depar W+D 6 s fare yok | 1.0° | 0° | 0° | 0° | −7° | 0.41 s |
| Tempolu W+D 6 s fare yok | 0.6° | 0° | 0° | −45° (yan koşu) | +18° | 0.37 s |

- **Okuma:**
  - Hareket hâlinde ekran ve girdi aynı yönde (≤ 1.2° karşı-yaw).
  - "ivme − istek" farkı dönüş hızı modeli (momentum), girdi eşleme hatası değil.
  - Fare olmadan tutulan çaprazlarda kontrol yaw'ı sabit kaldı: kamera otomatik takip döngüsü veya çift düzeltme yok.
  - **Tek kusur idle tutmasıydı:** hızlı fare dönüşünden sonra 0.3–0.8 s (testte 1.9–2.4 s toplam) ekran ile W yönü ayrışıyor; o anda W, ekranın 35° yanına yürüyordu.
- **Değişiklik:** `DA_GR_LocomotionBehavior.CameraIdleOrbitMaxYaw` 55 → 180 (tutma hiç devreye girmiyor).
  - FOV, mesafe, omuz ve sinematik değerler değişmedi (`CameraVisualResponse` 8, `CameraVisualCounterYaw` 1.2, `SprintCutFaceLead` 15 aynı).
  - Sonra: idle'da ekran − girdi maks. **0.0°**; yerinde dönüşler aynı; W, 180 sonrası doğrudan ekran ileri.
- **Bilinen yan etki:** idle'da kamera artık karakterin etrafında serbestçe dönüyor. Yerinde 180 dönüş sırasında yüzü kısa süre görebilir. Görsel kabul kullanıcıda.
- **Kanıt:** `idle_camera_before_game` / `idle_camera_after_game` (oyun kamerası), `walk/jog/sprint_camera_game`, `direction_table.txt`.

## 5. Geri ve 180 (madde 3)
- **Shift+W → W bırak → Shift+S** (`b_s2back`):
  - Hız sınırı S anında 490 → 300; hız ise 0.62 s'de 490 → 8 cm/s'ye düşüyor (hız anında kesilmiyor).
  - Bu sırada ileri→geri koşu pivotu oynuyor: `A_LR_Run_Pivot_F_B_*`, depar ters dönüş köprüsü.
  - Ardından gerçek geri koşu döngüsü `A_RB_Run_Rear`, 300 cm/s'de. Gövde ileri bakmaya devam ediyor (geri adım).
  - Ters ya da yavaşlatılmış depar klibi yok.
- **Çaprazlar** (S+A / S+D): kısa depar eğrisi → pivot → `A_RB_Run_RearLeft/Right`, 300 cm/s. Geri depar yok.
- **Kamera 180 + W** (`b_cam180`): fren 490 → 79 cm/s (0.6 s) → `Sprint_Turn_R_180` → yeniden hızlanma, deparla 490'a +1.9 s'de.
  - V2.11 itiş rotasıyla yeniden hızlanma artık koşu başlangıcı itişiyle (§6).
- **Sonuç:** istenen davranış zaten mevcuttu. Bu görevde değişiklik gerekmedi; kanıt: `sprint_to_back_*`, `sprint_cam180_*`.

## 6. Yürüyüş → depar itişi (madde 4)
- **Önce** (`g_w2s` taban):
  - Shift basılınca hız 132 → 490 (360 cm/s², ~1 s).
  - Gösterilen yürüyüş hıza göre basamaklı (Run 210–400).
  - `Update_MotionMatching` tempolu rotası (`PSD_CT_JogSteady`) 237–388 cm/s'yi 0.5 s düz tempolu döngüyle oynatıyor; depar rotası 230 cm/s'den itibaren depar döngüsünü hızlanırken açıyor.
  - Araya giren klip `A_CT_Jog_Fwd`; deparı açan koşul gösterilen yürüyüş = Sprint (≥ 400) ve hız ≥ `SHM_SprintDBMinSpeed`.
- **İdle → depar ayrı:** zaten rahat koşu başlangıcı (`A_RR_M_Relaxed_Run_Start_F_*`) oynuyordu; değişmedi.
- **Proje içeriği taraması:**
  - `A_C01R_Sprint_WalkToSprint/RunToSprint` 206 → 721 cm/s ve 28–44° gövde eğimi: başka hız bandı, atletik. Kullanılmadı.
  - Uygun içerik projenin kendi rahat koşu başlangıcı (`PSD_RR_Start`).
- **Değişiklik** (`ABP_GR_MotionMatchingBase`, `install_v211_push.py` + `promote_push.py`):
  - `SHM211_PushGate` itiş bayrağını hesaplıyor:
    - son 1.0 s içinde hız 200 cm/s'nin altına inmiş;
    - ivme > 120 cm/s²; |yön| < 35°;
    - CP başlangıcı yok; yön değiştirme bölümü yok;
    - bölüm bittikten ≥ 0.35 s sonra;
    - sınır 420 cm/s.
  - Tempolu ve depar rotaları bu bayrakla `PSD_RR_Start`'a yönleniyor. `SHM211_PushMode 1`.
- **Sonuç** (`g_w2s` itiş): 226 → 385 cm/s arası rahat koşu başlangıcının itiş bölümü oynuyor (klip 0.43 → 0.89 s), sonra depar döngüsü.
  - Yan görüntü (`img/walk_to_sprint_side.jpg`): ÖNCE dik tempolu koşu; SONRA öne eğilen, sürücü adımlı hızlanma.
  - Hız eğrisi değişmedi (CMC aynı).
- **Yeniden tetiklenme yok:**
  - depar W+A ↔ W+D ve ardışık kesişler: itiş yok;
  - geniş viraj: yok;
  - kısa basışlar kilitlenmiyor (bir basışta 1 kare).
- **Kalıntı:**
  - Yürüyüş gösterimi 132 → 207 cm/s arasında (~0.2 s) hızlandırılmış yürüyüş döngüsü.
  - Tempoludan depara (300 → 490) itiş yok; tasarım gereği dar tutuldu.

## 7. Ani ters dönüşlerde momentum (madde 5)

| Olay | Fren | Destek / dönüş | Yeniden itiş (önce → sonra) | Not |
|---|---|---|---|---|
| Geniş depar virajı (fare 90°/s) | yok | döngü + eğri | — | normal, sıçrama ≤ 32 m/s² |
| Keskin depar kesişi 90° (tuş) | 468 → 338 | depar eğrisi → 90 kesiş klibi | döngü | V2.10 paketi |
| Tam ters (tuş, W → S → W 0.7 s) | 490 → 2 (0.6 s) | koşu pivotu | depar başlangıcı → tempolu döngü → depar → **koşu başlangıcı itişi** | ikinci ters itiş bitmeden: yeni başlangıç |
| Deparda geri isteği (Shift+S) | 490 → 8 (0.62 s) | pivot | geri koşu ≤ 300 | §5 |
| Fare 180 ve 0.7 s sonra geri | 490 → 75 | eğri → pivot → 180 dönüş → yan tempolu ile yeniden yüzlenme | tempolu → depar döngüsü 237'den → **koşu başlangıcı itişi (dönüş bitince)** | ilk denemede 192 m/s² baş sıçraması; 0.35 s bekleme ile giderildi (en kötü 46) |
| Kamera 180 (fare) | 490 → 75 | pivot → 180 dönüş | tempolu → depar → **itiş** | |

- **Tuş ile fare karşılaştırması:**
  - Aynı "geri dön" niyeti tuşla (S) geri adım + geri koşu, fareyle (kamera 180 + W) gövde dönüşü + ileri koşu.
  - Bu, madde 3'teki tasarımla tutarlı. İkisinde de fren ve destek görünüyor.
- **Kilitleme yok:** girdi kilitlenmiyor, bütün dönüşler yavaşlatılmadı, yanlış klip tutulmuyor.
- **PARTIAL:** deparda fareyle tam 180'de dönüş içinde 55–67 m/s² sıçrama (klip içeriği, `Sprint_Turn_*_180`) — §8 taşma adayı.

## 8. Dünya tepkisi ve gerçek toparlama (madde 6)
- **Sınıflandırma** (`recov_table.py`, son üretim koşuları):
  - **Normal** (döngü/eğri, yön bölümü yok): depar 45° (W+A, %10 hız kaybı), tempolu 90°, geniş depar virajı.
  - **Planlı sert** (yön değiştirme klipleri emiyor, basılı ayak sürünmesi ≤ 1.9 cm/kare, sıçrama ≤ 39): depar W+A ↔ W+D 90°, tuşla ters, deparda Shift+S (çaprazlar dâhil), tempolu 180 yan ters.
  - **Taşma adayları:** fareyle deparda tam 180 (sıçrama 55–67 m/s²), tempolu S+D → S+A 135° (45). Gerçek bir yakalama adımının yeri bunlar.
- **RecoveryDemand = 0 kanıt sayılmadı:**
  - SHME toparlaması tasarım gereği yalnız dış itmeye bakıyor.
  - Eski niyet/çekiş dalı V1.3.x'te depar duruşunda 35 cm, duvarda 84 cm sahte adım üretmişti. Açılmadı; sahte kuvvet eklenmedi.
- **Kontrollü aday:** projede koşarken dışa yakalama adımı içeriği yok.
  - `SHM_Rec*` duran karakter için; `Run_Shuffle` 512 cm/s yana koşu değişimi.
  - Düz zemin adayı kurulamadı → **OPEN**.
- **Eğim, basamak, iniş, depar etkisi:**
  - 8° eğim ve 10 cm şeritte dur → dön → başla zincirleri §9'da.
  - Normal virajda sendeleme yok; `RecoveryDemand` her yerde 0.
- **Doğrulanmış içerik brifi** (satın alma yapılmadı; V2.10 brifinin ölçülerle güncellenmiş hâli):
  - Hız bantları: depar 4.9 m/s, tempolu 3.0 m/s; Manny iskeleti, kök hareketi, 30 fps+.
  - **A. Deparda 135–180° fare dönüşü taşması:** fren adımı + 1 dışa yakalama (yan / çapraz) + yeni yöne itiş. L/R, iki faz (iç/dış ayak havadayken). Fren çökmesi ≤ 10–12 cm; gövde eğimi ≤ 15° (karakter atletik değil).
  - **B. İtiş bitmeden ikinci ters dönüş** (hız 120–300 cm/s): tek destek adımı + yeniden yüzlenme. Bugün yan tempolu klipleriyle yapılıyor.
  - **C. Tempolu 135° çapraz geri değişimi:** 1 destek adımı.
  - Her klip oyuncu yön değiştirince veya durunca kesilebilir olmalı. Tetik: taşma adayı sınıfı (planlı sert + sıçrama > 40 veya sürünme > 5 cm) ve deparda Δyön > 120°.

## 9. Kabul zincirleri (son kayıtlı üretim, `v211z_*`)
- **Kayıt:** gerçek zamanlı yakalama, 30 fps sınırı, elde 22–29 fps; AVI'ler ölçülen yakalama hızında oynuyor.
- **Kameralar:** kollar için ön-çapraz (D) ve yan (S), yön için oyun kamerası (G), momentum için sabit tam gövde (D/S).
- **Test görünümü:** kıyafetin göğüste delinmesi (kapsam dışı) ten göstermesin diye yalnız test dünyasında görünür gövdeye opak gri QA kili verildi. Kıyafet, yüz ve saç üretim görünümünde. Hiçbir kare çıkarılmadı veya düzenlenmedi.
- **Üretim doğrulaması:** `verify_prod211.txt`.
  - V2.9/2.10 değerleri yerinde: CutMode 2, TipOld false, HC_Off false, StopMode 1, StartMode 0, CutTail 0.8, SL = `PSD_SHM210_SprintCut`, `SprintCutFaceLead` 15.
  - V2.11 değerleri: `SHM211_PushMode` 1, `CameraIdleOrbitMaxYaw` 180, 13 kol varlığı değişmiş.

| # | Zincir | Koşu | Teknik ölçü | Sıçrama >25 m/s² (en kötü) | Benim görsel incelemem |
|---|---|---|---|---|---|
| 1 | Rahat idle → yavaş / hızlı sola-sağa yerinde dönüş | `tip_slow_nD`, `tip_fast_nD/nS` | El idle'ın dışına medyan +3.0 / +4.5 cm (önce +11.3 / +10.7) | 0 / 3 montaj (28) | Kollar yakın, küçük salınım; adımlar aynı |
| 2 | idle → W | `a_long_nD/nS` | Sol "içeride" 0.17–0.23 s (önce 0.70); sağ yumuşak geçiş | 0 | Kol yanda asılı, sonra salınım |
| 3 | dur → W; dönüş → W; bas → bırak → tekrar | `a_restart_nD`, `a_tipw_nD`, `a_tap_nD` | §2.3; sağ kol kalıntısı 0.28–0.59 s | 0 / 1 (30) / 0 | Başlangıç rahat; ~0.5 s sonra kısa sağ kol içe gelişi (§2.4) |
| 4 | yürü → Shift | `g_w2s_nS/nG` | Koşu başlangıcı itişi 226 → 385 cm/s, sonra depar | 1 (27) | Öne eğilen itiş |
| 5 | Shift+W → bırak → Shift+S | `b_s2back_nS/nG`, `b_s2backl_nD` | −180 @ 466 → yön %90 0.64 s; geri koşu 300; çapraz −135 @ 400, 1.22 g | 4 (43) / 2 (36) / 2 (35) | Fren pivotu → geri koşu |
| 6 | Shift+W + kamera 180 | `b_cam180_nG/nD` | −180 @ 491, %90 0.76 s, 1.01 g; yeniden itiş | 7 (60) / 4 (35) | Fren-dönüş-itiş okunuyor; dönüşte sarsıntı (§7 PARTIAL) |
| 7 | Depar kesişi ve ardışık ters kesişler | `chain_sscut_nD`, `chain_sprint_nG` | 90 @ 484 → 1.14 g, %37; ters −180 @ 396 | 8 (41) / 7 (35) | V2.10 paketi korunmuş |
| 8 | Kamera dönüşü idle / yürüyüş / tempolu / depar | `d_idle_nG`, `d_walk/jog/sprint_nG` | ekran − girdi idle 0.0° (önce 113–125°), hareket ≤ 1.2° | 5 (46) / 0 / 0 / 3 (27) | W her zaman ekran ileri |
| 9 | Eğim / tek ayak yükseltide dur → dön → başla | `chain_slope_r_nS`, `legs_lfoot_walk_nD` | dönüş %90 1.12 / 1.3 s; duruş 0.52 s / 33–34 cm | 1 (30) / 1 (43) | Ayaklar yüzeyde, V2.10 ile aynı |
| 10 | Sert dönüşte toparlama / normal virajda sendeleme yok | `r_ms2_nD`, `r_curve_nG` | Viraj 45° @ 491, 0.58 g, sıçrama 0; fare 180 @ 490 | 5 (45) / 0 | Virajda sendeleme yok; sert dönüşte gerçek yakalama adımı yok (OPEN) |

- **Sıçrama sınıfları önce ile aynı:**
  - kısa basış bırakmasında baş/omuz 30–35 (önceki kayıtta 32);
  - depar omuz sıçramaları (V2.10 tabanı 39–63);
  - montaj sıçramaları (önce 2–6).
  - Kol bake'i ve itiş rotası yeni bir sıçrama sınıfı eklemedi. İtişin ilk sürümündeki 192 m/s² giderildi.
- **Ayak kayması ve diz:** bacak, pelvis ve kök izleri değişmedi (okuma 0.0). V2.10 diz/leg_guard ölçüleri geçerli.

## 10. Değişen dosyalar, ayarlar, geri alma
- **Animasyon içeriği** (yalnız kol izleri):
  - `/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Walk_Fwd`
  - `/Game/GraceRanger/Animations/LookStrafe/Sample/A_LS_M_Relaxed_Walk_Start_F_Lfoot`, `..._Rfoot`
  - `/Game/GraceRanger/SHME/Animations/Turns/SHM_M_Neutral_Stand_Turn_{045,090,135,180}_{L,R}` (8)
  - Veritabanı yeniden anahtarlandı (tag `V211A`): `PSD_LB_WalkLoops`, `PSD_SHM_TurnInPlace`.
- **Yeni (geri alma kaynağı):** `/Game/ActionAdventureMovementS/Rollbacks/SHME_V211_Arms_Before_20261016/` (11 orijinal kopya; referanssız).
- **Profil:** `DA_GR_LocomotionBehavior.CameraIdleOrbitMaxYaw` 55 → 180.
- **ABP:** `/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase` (+ child derlemesi):
  - üyeler `SHM211_*`, fonksiyon `SHM211_PushGate`;
  - EventGraph çağrısı + rota dalı;
  - `Update_MotionMatching`: `K2Node_CallFunction_91.Database` ve `K2Node_Select_24/25 Option 1` rota üyelerine bağlandı;
  - `SHM211_PushMode` 1.
- **Geri alma:**
  - **Hızlı:** `SHM211_PushMode` 0 (rotalar orijinal veritabanlarına döner); `CameraIdleOrbitMaxYaw` 55.
  - **Kollar:** `Saved/Codex/SHME_V211_20261016/checkpoint/arms_before/` (13 dosya, SHA256SUMS) editör kapalıyken geri kopyalanır. Ya da `v211_arm_bake.py` kaynağıyla yeniden üretilir.
  - **Tam:** `checkpoint/baseline_v210/` (34 dosya: Sandbox ABP'ler, BP_GR_Player, BP_PBI_Player, DA'lar, profiller, retarget, başlangıç klipleri).
- **Araçlar:** `Tools/SHME_V211_20261016/`:
  - `v211_arm_bake.py`, `install_v211_push.py`, `promote_push.py`, `promote_orbit.py`, `verify_prod211.py`;
  - ölçüm: `arms.py`, `dirtl.py`, `gaitl.py`, `recov_table.py`, `probe_armclip.py`, `turnclip_table.py`;
  - grafik: `dump_dir.py`, `dump_abp.py`, `gtrace.py`;
  - koşum: `v211_run.sh`, `v211_ab.sh`, `ab_safe.sh`, `dir_batch.sh`, `cap_final.sh`;
  - medya: `make_media211.sh`, `media211.sh`, `sheet211.ps1`, `sheet_frames.py`.
- **Değişmeyenler:** karakter anatomisi, iskelet oranları, kıyafet, üretim haritası, FOV, kamera mesafesi, omuz ofseti, sinematik kamera değerleri, CMC hız/ivme.

## 11. Medya (`pub/`)
- **`img/` (aynı oyun zamanında kareler):**
  - `start_long_before_v2_after.jpg`: ÖNCE / reddedilen v2 / SONRA.
  - `tip_fast_before_after.jpg`
  - `walk_to_sprint_side.jpg`: itiş kapalı / açık.
  - `idle_camera_before_after.jpg`: 55° tutma / 180.
- **`vid/`:** GIF (gerçek hız, her 2. kare) ve gerçek zamanlı AVI; adlar `media211.sh` listesinde (ÖNCE/SONRA çiftleri ve 10 zincir). `walk_to_sprint_*` ayrıca 1/3 hız AVI.

## 12. Beceri eklemeleri (yalnız doğrulananlar)
- `sphirus-human-motion-engine`:
  - `authoring.md`: kol taşıması bake'i, idle yerel dönüş tuzağı, temiz kaynaktan bake, DSL `Name_0` tuzağı.
  - `motion-diagnosis.md`: yürüme başlangıcı kol sahipleri, dönüş kolu sahibi, itiş beklemesi.
  - `architecture.md`: V2.11 üretim düğümleri.
  - `validation.md`: yeni araçlar ve koşum gerçekleri.
  - `mm-coverage.md`: itiş rotası ve yön bölümü sonrası bekleme tuzağı.
- `sphirus-character-camera`:
  - `camera-feel.md`: kamera–girdi yönü ve idle tutma.
  - `support-momentum-intents.md`: V2.11 sınıflandırma.
- Senkronizasyon: `sync_claude_skills.py`, 0 hata.

## 13. Kullanıcı testi
`USER_PLAYTEST_V211.md`. His, görünüm ve kontrol kabulü kullanıcıda; ben kabul vermedim.
