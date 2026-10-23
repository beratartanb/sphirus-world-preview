# SPHIRUS V2.24 — Doğru tempolu hareket, çalışan algısal kamera, gerçek arazi adımlaması

**Genel durum:** PARTIAL.
- Teknik doğrulama ve oyun hissi kabulü aşağıda ayrı ayrı yazıldı.
- Kullanıcı kabulü verilmiş sayılmadı.
- Görsel değerlendirmeyi kendim yaptım ve her hedefte ayrıca belirttim.

**Taban ve sahiplik**
- Taban: V2.23 üretimi (commit 9ac5c99).
- Motor: UE 5.8, yalnız Blueprint.
- Oyuncu zinciri: `BP_PBI_Player` → `BP_GR_Player`.
- Hareket: SHME bileşeni + `ABP_GR_MotionMatchingBase`.
- Kamera: GraceRanger rig.

**Ölçüm koşulları**
- Varsayılan sabit 30 FPS (`-UseFixedTimeStep`), aynı oturumda A/B.
- Ayrıca 20, 60 ve 120 FPS ile gerçek zamanlı koşular yapıldı.
- Gerçek klavye ve bakış girdisi (IA_Move / IA_Look / Shift).
- "o" = V2.23 üretimi; V2.24'ün değiştirdiği bütün anahtarlar V2.23 değerlerine sabitlendi.
- "p" = V2.24 üretimi.

**Üretime kaydedildi, temiz yeniden açılışta doğrulandı (`verify_prod224`: `bad: []`, ALL_OK)**
- ABP `SHM224_JRMode` = 3.
- SHME `RedirectSpeedDecay` = 600.
- Kamera D aşaması:
  - `GR223_PivotXY` = 1,
  - eski yatay katkılar 0,
  - `CamFollowEnabled` açık,
  - `CamFolYawFade` = 90.
- Koşu başlangıcı kliplerinde bel düzeltmesi (içerik).
- Ayak kaldırma (`SwingLiftEnabled`) açık: pay 10.5, ileri bakış 0.18 s, yalnız yükselen zeminde. İkinci promosyon, ikinci temiz yeniden açılışta doğrulandı.

---

## İlk sayfa: üç hedefin durumu

### TEMPO — PARTIAL (ters dönüş büyük ölçüde onarıldı; ağır çekim içeriği ve gövde eğimi açık)

| Soru | Cevap (ölçülen) |
|---|---|
| 20 FPS'te yanlış niyetli pivot | **Onarıldı.** Neden: ilk karede hız 178'e düşmüş, köprü eşiği 200 → sınıf 0 → genel pivot DB. Hız sınıflandırması kare hızından bağımsız yapıldı. 20/30/60/120 FPS'te doğru pivot. |
| 120 FPS'te 110 cm kayma | Aynı girdiyle bugün 34.6 cm (o). Neden: aynı pivotun **destek evresine göre** girilmesi. p'de bindirmeli girdide en kötü 22.5 cm. |
| S→W itişte ~51° öne eğilme | **Sahibi düzeltildi:** çalışma zamanı değil, **klibin bel bükümü**. V2.23'ün "çalışma zamanı ekliyor" tespiti, iki farklı kemik çiftinin karşılaştırılmasıydı. İçerik düzeltmesi geri pivotta göğüs korumasını geçemedi; reddedildi. **Açık.** |
| Tempolu kalkış eğimi | Klip kaynaklı. Kalkış kliplerinde bel düzeltmesi: görünür göğüs −1.1° (20.2 → 19.1). Küçük; üretimde. |
| W→S evreye bağlı kayma | Geri→ileri (S→W) için onarıldı: 10 evrede en kötü 64.7 → 25.5 cm, ortalama 36.8 → 13.9 cm, batma 13 → 4 cm. İleri→geri (W→S) karışık: bir evrede 35 → 50 cm. |
| A↔D yan ters dönüş | **Onarıldı.** Artık yan pivot seçiliyor, sprint dönüş kavisi kullanılmıyor. Ani ivme sıçramaları 7 (en kötü 291 m/s²) → 3 (28), en kötü ayak 33.9 → 16.5 cm. Ayrı yan pivot üretilmedi; mevcut CP2 sol/sağ pivotlar yeterli çıktı. |
| Planlı itiş / gerçek toparlanma ayrımı | Yapılmadı. Recovery'ye dokunulmadı. |
| Ağır çekim (yürüyüş arka ×0.72, tempolu sağ ×0.84, sprint yan ×0.69) | **Yapılmadı.** Ara hız içeriği üretilmedi; V2.23 ölçümleri geçerli. |
| Niyet tanımları | Ayrıldı: ileri koşu → geri, geri koşu → ileri, yan ters, kamera dönüşü + ileri (eski RevTurn yolu, değişmedi). |
| Sıfır hız geçişi kararsızlığı | Bir karelik yanlış (yan) pivot bulundu ve giderildi (erken rota). |

### KAMERA — PARTIAL (yatay ofset kameraya ulaşıyor ve takip üretimde; üç davranış kurulmadı)

| Soru | Cevap |
|---|---|
| Yatay ofset gerçekten kameraya ulaşıyor mu? | **Evet, ölçüldü.** Eski katkılar sıfırken bilinen 20.0 cm ofset, kamera−kapsül mesafesinde tam +20.0 cm göründü. |
| Algısal takip | Üretimde (D aşaması). Kamera sarsıntısı aynı (jerk95 1.53 → 1.58). Karakter fare dönüşünde ve yanlamada ekranda daha çok kayıyor (bilinçli yumuşak bölge, bölüm 2). |
| Katkılar tek tek | Fren/hızlanma taşıması (E3) fare dönüşünde sarsıntıyı 1.5 → 8.1 artırdı; **reddedildi**. Yan kaydırma (E2) koridorda fazladan kamera yolu üretti; **reddedildi**. Look-ahead (E1) ekranda fark yaratmadı. |
| Keşif / ilerleme / durup inceleme davranışları | **Kurulmadı.** |
| FOV | Tek sahip (SHME CamFOVDelta), değişmedi; pompalama yok (60–62.6°). |
| Tam ekran kanıt | Bütün kamera videoları tam ekran, gerçek en-boy oranında (kırpma kaldırıldı). |

### ARAZİ — PARTIAL (salınan ayak açıklığı çalışıyor; tümsekte sol ayak hâlâ takılıyor)

| Soru | Cevap |
|---|---|
| Tümsek → tepe → küçük iniş → düz | Ayak kaldırma açık (p): yürüyüşte tümsekte sağ ayak basış kayması 28.5 → 3.7 cm; inişte sol ayak 35 → 14–26 cm (iki koşu); koşuda inişte ayak açıklığı 0.9 → 6.8 cm, takılma 2 → 0; düz zemine etkisi yok. |
| Salınan ayak tümseği aşıyor mu? | Kısmen. Sol ayak tümsek tepesinde hâlâ 12 karede takılıyor. |
| IK / pelvis sahipliği | Açık yazıldı: FootPlacement duran ayağı, SHME yalnız salınan ayağın IK hedefini sürüyor, LegIK çözüyor; pelvis değişmedi. |
| Planlı iniş / gerçek düşüş ayrımı | Yapılmadı. |
| Ev–orman rotası | Ölçüldü (map_r2, pilot): o ile p arasında sıçrama sayısı aynı. |

### Diğer istekler (yapılmadı, açıkça)
- Kafa/üst gövde bakış eşliği pilotu.
- Kadraj odağı.
- Dinamik alan derinliği.
- Pozlama testi.
- Dar geçiş, el teması, nefes, ses.

V2.24'te bunların hiçbiri uygulanmadı.

## 1. TEMPO — ayrıntı

### 1.1 Yanlış niyetli pivot (20 FPS)
- **Neden:**
  - Ters dönüş isteğinin ilk karesinde kapsül zaten 245 → 178 cm/s'ye frenlenmiş oluyor (tek 50 ms'lik tik).
  - Bu, `RedirectBridgeMinSpeed` 200'ün altında. Sınıf 0 çıkıyor, köprü açılmıyor.
  - Genel `PSD_CP2_JogPivots`, geri→ileri istek için `A_CP2_Jog_Fwd_Pivot` veriyor.
  - 30 FPS'te aynı karede hız 200 olduğu için doğru seçim yapılıyordu.
- **Değişiklik (bileşen, çalışma zamanı):**
  - `SpeedOnset` = max(Speed, SpeedOnset − RedirectSpeedDecay·dt), sınıflandırma bununla yapılıyor.
  - `RedirectSpeedDecay` = 600 cm/s².
- **Kanıt:** 20 FPS S→W, üretimde (o) en kötü ayak 43.8 cm (yanlış pivot). Yeni seçim (r2) doğru pivotu seçiyor: 12.2 cm.

### 1.2 İsteğin kimliği ve bir karelik yanlış pivot
- **Dört niyet ayrıldı.** MontTick, ters dönüşün ilk karelerinde, hızın aktörün baktığı yöne göre durumundan niyeti kilitliyor:
  1. ileri koşu → geri,
  2. geri koşu → ileri,
  3. yan ters,
  4. kamera dönüşü + ileri (eski RevTurn yolu, değişmedi).
- **Rota:** EventGraph, MontTick'ten hemen sonra `SHM_RedirectDB_JR`'yi isteğe göre yazıyor: `JogRevFwdO`, `JogRevBwdO` ya da `JogRevLat`. Her birinde tek pivot ve döngüler var.
- **Bir kare erken:** İstek, bileşenin bölümü başlamadan bir tik önce görünüyor; o karede genel seçici yan pivot (`A_CP2_Jog_Right_Pivot`) veriyordu.
  - `SHM224_EarlyRev`: bölüm yok, girdi hızdan 150°'den fazla sapmış, 150 < hız < 340.
  - Köprünün "else" dalı → doğrudan JR veritabanı.
  - 20 FPS'te S→W ani ivme sıçramaları her evrede 0.

### 1.3 Evreye bağlı kayma = ayak varyantı
- **Kanıt (`phase224.py`, 40'tan fazla koşu):**
  - `SHM_DPP_Jog_Bwd_Pivot` her evrede 0.87 s'den giriliyor ve girişte sol ayağın yerde olmasını bekliyor.
  - Sağ ayak yerdeyken sağ ayak 13 cm batıyor ve 37–65 cm kayıyor.
  - Poz eşleştirme evreyi ayırt edemiyor: ayna ve orijinal aynı veritabanındayken her evrede aynayı seçti.
- **Değişiklik:**
  - **İçerik:** sol/sağ aynalanmış kopyalar (`mirror224.py`). Bileşen uzayında aynalama, referans poz düzeltmesi. Aynanın aynası birebir; izli kemiklerde fark < 0.4 cm.
  - **ABP:** ayağa göre açık seçim. Sağ top 2 cm daha alçaksa (geri→ileri) ya da sol top 2 cm daha alçaksa (ileri→geri), aynalı veritabanı kullanılıyor.
- **Sonuç:**

| Geri→ileri, 10 evre | Önce | Sonra |
|---|---|---|
| 30 FPS, en kötü ayak | 64.7 cm | 25.5 cm |
| 30 FPS, ortalama | 36.8 cm | 13.9 cm |
| Batma | −13 cm | −4 cm |
| 20 FPS, en kötü ayak | 62.4 cm | 32.7 cm |

- **Tablolar:** `phase224_30fps_before_after.txt`, `phase224_20fps_before_after.txt`.
- **Kalan:**
  - İleri→geri karışık: bir evrede 35 → 50 cm.
  - Bırak/yeniden bas 49 → 51 cm.
  - Fare 180° + W (RevTurn yolu) değişmedi: 55 cm.

### 1.4 Gövde eğimi — sahibi
- **Aynı karede ve aynı eksende ölçüm** (`lean224.py`; klip → MM mesh → görünür, ayakta duruş referansı çıkarıldı):
  - S→W itişte göğüste klip +20.2°, MM +20.2°, görünür +24.2°.
  - Retarget göğüse +4°, alt gövdeye +11° ekliyor.
  - Çalışma zamanı katmanları tek tek kapatıldı (PBI, APA, fren duruşu, eğri eğimi, oryantasyon/adım bükme): en fazla 3° etki.
- **Sonuç:** V2.23'ün "eğimi çalışma zamanı ekliyor" tespiti yanlıştı. Klipte pelvis→boyun 11° ile çalışma zamanında pelvis→spine_03 36° karşılaştırılmıştı. Kambur görüntü klibin bel bükümü: pelvis→spine_03 duruşa göre +26.6°.
- **İçerik denemesi (`lumbar224.py`):** spine_01/02 geriye, spine_04 karşı dönüş.
  - Koşu başlangıcı kliplerinde göğüs koruması geçti, görünür −1.1°; üretimde.
  - Geri pivotta göğüs 3.4° değişti, **reddedildi**. Gereken şey yazılmış bir duruş; karşı dönüş yetmiyor.

### 1.5 Yapılmayanlar
- Ağır çekim içeriği (ara hızlar).
- Planlı itiş / gerçek toparlanma ayrımı.

## 2. KAMERA — ayrıntı

| Aşama | Ne | Ölçüm |
|---|---|---|
| A | V2.23 kaydı | — |
| B | `PivotXY` 1, eski yatay katkılar 0 | Kamera yolu V2.23 ile birebir aynı. |
| C | Bilinen 20 cm ofset | Kamera−kapsül mesafesinde tam +20.0 cm. |
| D | Algısal takip (üretim) | Kamera sarsıntısı (jerk95) 1.53 → 1.58. Ekranda yanal kayma: fare dönüşü 5.3 → 10.5, yanlama 13 → 24. Evdeki rotada kameranın en yakın mesafesi 167 → 190 cm. |
| E1 | Look-ahead | Ekranda fark yok. |
| E2 | Yan kaydırma | Koridorda fazladan kamera yolu; reddedildi. |
| E3 | Fren/hızlanma taşıması | Fare dönüşünde jerk95 1.5 → 8.1; reddedildi. |

- **Bakış dönüşünde takip sönümlemesi** (`CamFolYawFade` 90): ağırlık devrede (ortalama 0.25), ama ekrandaki kaymayı değiştirmedi. Kayma bilinçli kadraj, yani yumuşak bölge yasası.
- **Gerçek zamanlı koşu:** jerk95 hem V2.23'te hem V2.24'te 9–12. Değişken kare süresi ölçüyü şişiriyor; gerçek zamanlı koşu yalnız gerçek zamanlı koşuyla karşılaştırılmalı.
- **Kare hizalama etkisi:** Aynı yapıyla iki oturumda aynı senaryonun jerk95 değeri 1.5 ve 8.0 çıktı, çünkü gidişat bir kare kaydı.
- **Geri dönüş:** `GR223_PivotXY` 0 + `CamFollowEnabled` kapalı. V2.23 değerleri: taşımalar 6/8/6, dönüş telafisi 16, yan kaydırma 40, look-ahead 4/18.
- **Kurulmayanlar:** keşif / ilerleme / inceleme davranışları, kadraj odağı, alan derinliği, pozlama testi.

## 3. ARAZİ — ayrıntı
- **Sahiplik:**
  - FootPlacement duran ayağı yerleştiriyor.
  - SHME yalnız salınan ayağın IK hedefini kaldırıyor. FeetIK katmanında, FootPlacement'tan sonra ve LegIK'tan önce `ik_foot_l/r` +Z ekleniyor.
  - LegIK bacağı çözüyor. İkinci bir yerleştirme yok, pelvis değişmedi.
- **Yasa:**
  - Öndeki zemin, ayak merkezi ve pay karşılaştırılıyor.
  - Yalnız öndeki zemin destek düzleminden (`FootZ`) 1 cm'den fazla yüksekse etkin; +3 cm'de tam etki.
  - Temasta hızlı bırakma (0.03 s).
- **Dersler:**
  - Ayak merkezi tabanın ~6.5 cm üstünde; 4 cm pay hiç kaldırmadı.
  - Yükselme koşulu olmadan düz zeminde karelerin yarısında kaldırdı (her yerde sabit katman, reddedildi).
  - `baseZ`'ye göre ölçülen koşul tümsekte geç açıldı.
- **Sonuç (30 FPS):**

| | Önce | Sonra |
|---|---|---|
| Yürüyüş, tümsekte sağ ayak basış kayması | 28.5 cm | 3.7 cm |
| İniş, sol ayak basış kayması | 35.3 cm | 13.7–26.1 cm |
| Koşu, inişte ayak açıklığı | 0.9 cm | 6.8 cm |
| Koşu, inişte takılma | 2 | 0 |

- Düz zeminde (wfwd, c23_walk) kaldırma hiç kare açmadı; kaymalar aynı.
- **Kalan:**
  - Sol ayak tümsek tepesinde 12 karede takılıyor.
  - Planlı iniş ile düşüş ayrımı yapılmadı.

## 4. Kare hızları, gerçek zaman, ilk kullanım
- **20, 30, 60 ve 120 FPS:** bütün ters dönüş senaryoları koşuldu. Ham çıktı: `final224_t9.txt` ve `phase224_*`.
- **60 FPS:** sıçrama sayacı her koşuda gürültülü (14–21, üretimde de aynı).
- **120 FPS:** V2.23'teki 110 cm'lik koşu bugün üretimde 34.6 cm. Ayağa göre seçimin 120 FPS'te temiz veritabanlarıyla tekrarı yapılmadı (yalnız bayat aynalı girdili aday koşuldu).
- **Gerçek zamanlı (~20 FPS):**
  - W>S>W ph2'de en kötü ayak o 21.6 / p 12.7 cm.
  - Bir koşuda Shift dokunuşu kaçtı (koşu yerine yürüyüş). Ölçüm koşuyu yansıtmıyor; geçersiz sayıldı.
- **Isınma:** her grupta bir ısınma koşusu var; ilk kullanım ayrıca ölçülmedi.

## 5. Kaydet, yeniden aç, gerilemeler
- Bütün kurulumlar: önce kontrol noktası (`checkpoint/pre_v224`, `pre_promo224`, `pre_lumbar`), sonra temiz editör, sonra yükleme, sonra kayıt.
- `verify_prod224` iki ayrı temiz yeniden açılışta ALL_OK verdi. Kontrol edilenler:
  - LastHitBy onarımı,
  - kamera ve profil başvuruları,
  - yeni düğümler (EarlyRev, RevMir, köprü dalı, FeetIK kaldırma, Snapshot),
  - veritabanı içerikleri,
  - üretim veritabanlarına V2.24 klibi sızıntısı.
- **Gerileme kontrolü (aynı oturum):** sprint ters dönüş, fare 180°, duruşlar, kalkışlar ve kısa dokunuşlar o ile aynı ya da daha iyi.
- **Bulunan tuzaklar:**
  - BranchIn izi silinince klip veritabanı listesinde kalıyor. Çözüm: temiz veritabanı.
  - Uzun süre açık kalan editör 75 GB bellek taahhüdünde çöktü. Çözüm: her derlemeden önce yeni editör.

## 6. Geri dönüş
- **Tempo:** `SHM224_JRMode` 0 ve `RedirectSpeedDecay` 0 → V2.23. Veritabanları ve aynalı klipler `V224/` altında; üretim veritabanlarına dokunulmadı.
- **Kamera:** bölüm 2.
- **Arazi:** `SwingLiftEnabled` kapalı.
- **Koşu başlangıcı bel düzeltmesi:** `checkpoint/pre_lumbar` içindeki iki `.uasset` geri kopyalanır.
- **SHME kaynakları:** `checkpoint/pre_promo224` ve `checkpoint/tools/*.v224a`.

## 7. Görsel değerlendirme (kendi incelemem; kullanıcı kabulü değildir)
- **Video ayarları:** sabit 30 FPS oyun zamanı, gerçek hız; düzenlenmemiş kareler.
- **Kare:** oyun görüntüsünün tamamı, kenardan yalnız 15 px. Hizalı 1728×924 kopya, 1758×940'ın %98'i, en-boy oranı aynı (1.87). MediaIOCore, 64'ün katı olmayan genişliği çökme riskine karşı reddediyor; tam kare çekim bu yüzden ilk denemede alınamadı.
- **Görünüm:** gövdede yalnız PIE içi kil görünümü.
- **Ağır çekim:** `*_slow3x.avi` dosyaları yalnız inceleme içindir.

**Videolar**

| Video | Kamera | Gözlem |
|---|---|---|
| `jogrev_SW_ph4_before/after_*` | yan + çapraz | Önce: fren sırasında derin çömelme, sağ ayak batıyor. Sonra: dik fren, ayak yerde. İtiş anında gövdenin öne eğilmesi **hâlâ görünüyor** (açık kusur). |
| `jog_AD_before/after_diag` | çapraz | Önce: koşu dönüş kavisi, bacak yükseğe kalkıyor. Sonra: yan pivot, temiz yan adımlar. |
| `jogrev_WSW_*_game` | oyun kamerası | Ters dönüş kamera açısından sakin. |
| `cam_mouse_turns_*_game` | oyun kamerası | Sonra: karakter ekranda biraz daha yana kayık; kopukluk yok. |
| `terrain_bump_walk_*` | yan | Bu kamera açısında ve ölçekte önce/sonra farkı gözle seçilemiyor; iyileşme ölçümde (bölüm 3). |
| `map_house_forest_*_game` | oyun kamerası | Neredeyse aynı. |

- **Kareler:** `img/*_ab.jpg` (üst satır önce, alt satır sonra).

## 8. Maliyet
- **Yeni iz atımı:** kare başına iki yer izi (salınan ayak), yalnız ayak kaldırma açıkken ve hareket ederken.
- **ABP:** birkaç dal ve iki kemik düğümü.
- **Veritabanları:** beş yeni, küçük.
- **Ölçülmedi:** profil (stat/Insights) çalıştırılmadı; maliyet etkisi NOT_TESTED.
