# SPHIRUS V2.23 — Doğal hareket, çevre farkındalığı, oynanış kamerası

**Durum:** PARTIAL. Teknik doğrulama, kalan maddeler ve oyun hissi kabulü aşağıda ayrı ayrı yazıldı. Kullanıcı kabulü verilmiş sayılmadı.

- **Taban:** V2.22 üretimi (commit 6bbab23). Yerelde daha yeni bir değişiklik yoktu: V2.22'den sonra hiçbir `.uasset`/`.umap` değişmemişti.
- **Motor ve sahiplik:**
  - UE 5.8, yalnız Blueprint.
  - Oyuncu zinciri: `BP_PBI_Player` → `BP_GR_Player`.
  - Hareket katmanı: SHME bileşeni + `ABP_GR_MotionMatchingBase`.
  - Kamera: GraceRanger rig. Black Eye Camera etkin değil.
- **Ölçüm koşulları:**
  - Varsayılan sabit 30 FPS (`-UseFixedTimeStep`).
  - Aynı senaryo farklı oturumlarda bit düzeyinde aynı çıktı verdi.
  - 20/60/120 FPS ve gerçek zamanlı koşu ayrıca yapıldı (bölüm 5).
  - Gerçek klavye ve bakış girdisi kullanıldı (IA_Move / IA_Look / Shift).

## Kısa özet

| Hedef | Sonuç | Üretimde |
|---|---|---|
| Tempoluda ani ters yön (S→W) "kameraya ışınlanma + ağır çekim" | Nedeni bulundu ve giderildi. Sprint dönüş kavisi tempolu geri koşuya uygulanıyordu. Yerine geri→ileri pivot geldi. **Yeni kusur:** itişte gövde öne eğilmesi. | AÇIK (PARTIAL) |
| Tempoluda W→S | Değişmedi. Kayma destek evresine göre 4–52 cm. | — (açık) |
| Hız–ritim–adım uyumu | Bütün gait'ler ölçüldü. Kalıcı koşuda ayak–yol uyumu iyi (0.95–1.02). Ağır çekim kaynakları: oynatma hızları. | Ölçüm (düzeltme açık) |
| Tempolu kalkışın depar benzeri olması | Sahibi ayrıştırıldı (çalışma zamanı eğimi; klip değil). | Açık |
| Kamera: yatay pivot ofsetleri | **Kritik hata bulundu.** SHME'nin bütün yatay kamera ofsetleri kameraya hiç ulaşmıyordu. Düzeltme kuruldu (anahtar). | Kapalı (aday) |
| Algısal takip ve görüş look-ahead | Kuruldu ve ölçüldü. Her senaryoda V2.22'den iyi değil. | Kapalı (aday) |
| FOV / netlik / pozlama | Ölçüldü (sahiplik ve değerler). Değişiklik yok. | — |
| Arazide adımlama, bakış eşliği, dar geçiş, el teması, ayak sesi | Ölçüldü veya incelendi, uygulanmadı. | Açık |

---

## 1. Kritik hareket onarımları ve hız–adım uyumu

### 1.1 "Kameraya doğru ışınlanma" — nedeni
- **Kanıt:** yeni konum yetkisi izi (`trace223.py`). Aynı karelerde şu katmanlar ayrı ayrı kaydedildi:
  - kapsül dünya konumu ve hızı,
  - mesh'in kapsüle göre ofseti,
  - MM root,
  - MM pelvis,
  - görünür gövde pelvisi,
  - kamera pivotu.
- **Sınıflandırma:** hiçbir katmanda konum sıçraması yok. Kapsülün hızla açıklanamayan hareketi ≤0.9 cm/kare. Görünür pelvisin kapsülden bağımsız hareketi ≤4.5 cm/kare. Kök hareketi uygulanmıyor (`rmp` 0), mesh ofseti sabit, kamera pivotu sürekli.
- **Doğrulanan neden: yanlış içerik seçimi.**
  - Tempoluda geri koşu (S) sırasında W'ye basılınca `SHM213_MontTick`'teki "ileri koşu ters dönüş" rotası tetikleniyor.
  - Koşulları: kamera yönüne istek ve hız > 150 cm/s.
  - Bu rota V2.16'da depar için yazılmış `SHM216_RevTurn_*` klibini seçiyor: 121° kök dönüşlü bir koşu kavisi, hızı hiç 140 cm/s'nin altına inmiyor, 416 cm/s'ye itiyor.
  - Kapsül ise sıfıra kadar durup 270 cm/s² ile yeniden hızlanıyor. Bacaklar 150–300 cm/s koşarken gövde 0–130 cm/s ilerliyor; bu ağır çekim etkisi yaratıyor.
  - Görünür pelvis kapsülün 15–19 cm gerisinde (kameraya doğru) 1.3 s kalıyor; pelvis 12 cm düşüyor.
  - Yan kayıtta derin, yana bükülen bir çömelme ve sıçrama görülüyor.

### 1.2 Uygulama (üretimde)
- **ABP `SHM223_RevRearGate` = 1:** karakter kendi yüzüne göre geriye giderken (hız·aktör ileri < −0.5) bu rota kullanılmıyor.
- **Tempolu ters dönüş veritabanı** = `PSD_SHM_Redirect_JogReversalQ`. İçinde geri→ileri tempolu pivot (`SHM_DPP_Jog_Bwd_Pivot`) var, ileri koşu döngüsü yok.
- **Pivotun itiş duruşu** sahip olunan kopyada yeniden işlendi: klipteki eğim tepesi 30.6° → 11.2°, kol sürüşü ×0.6, ayak hatası 0.0 cm.
- Sahiplik tek ve açık: konum = kapsül (GR), poz = tek bir pivot klibi.

### 1.3 Ölçüm (sabit 30, aynı oturum; S→W penceresi; 3 tekrar aynı)

| | V2.22 | V2.23 |
|---|---|---|
| Seçilen klip zinciri | Rear → Right_Pivot → **RevTurn (depar kavisi)** → Jog_Fwd | Rear → Right_Pivot → **Jog_Bwd_Pivot** → Jog_Fwd |
| En kötü tek temas kayması (sağ / sol) | **51.7** / 12.4 cm | **13.3** / 16.8 cm |
| Toplam sürüklenme (iki ayak) | 89 cm | 106 cm |
| Alçak salınım (sağ) | 120 cm | 61 cm |
| Görünür pelvis − kapsül (ileri) | −19.4 … +3.8 cm | −1.3 … +11.0 cm |
| En büyük ani ivme (üst gövde) | 296 m/s² | 41 m/s² |
| Karakterin ekranda yatay titremesi (kamera aynı) | 11.6 | 6.8 |
| **Gövde öne eğimi, tepe** | 31° | **51°** (itiş evresi, ~0.4 s) |

- **Normal hızlı kanıt:** `img/jogrev_SW_final_side.jpg`, `img/jogrev_SW_final_diag.jpg`, `vid/jogrev_SW_*` (sabit 30 FPS oyun zamanı = gerçek hız, kesilmemiş kareler; `slow3x` dosyaları yalnız inceleme içindir).
- **Görsel değerlendirme:**
  - V2.22: dizleri yukarıda bir çömelme, gövdenin yana bükülüp sıçradığı bir dönüş.
  - V2.23: dik bir fren, ardından öne itiş ve doğrudan tempolu koşu.
  - Ancak V2.23'te itiş evresinde gövde belirgin öne atılıyor. Bu, istenen "derin eğilme yok" ölçütünü karşılamıyor.
- **Yeni kusurun sahibi:** klip değil. Klipteki eğim 11°'ye sınırlansa da oyundaki tepe ancak 57°'den 51°'ye iniyor. MM mesh 36° gösteriyor, görünür gövdeye aktarımda +15° ekleniyor, SHME `LeanFwd` ~1 etkin. Aynı çalışma zamanı katmanı tempolu kalkışları da 34°'ye çıkarıyor (bkz. 2.1). Sonraki adım: ABP'deki ivme eğimi zincirini bulmak.

### 1.4 Değişmeyen ve açık kalanlar
- **W→S (ileri→geri pivot, `A_CP2_Jog_Fwd_Pivot`):**
  - Sol ayak kayması destek evresine bağlı. V2.22 tekrarları: 11.7 / 20.7 / 29.1 / 4.2 cm. V2.23 tekrarları: 11.7 / 52.5 / 29.1 / 6.8 cm.
  - 52.5 cm'lik durumun nedeni: önceki dönüş değişince bu dönüşün başladığı evre kayıyor. İçerik aynı ve evreye duyarlı.
  - Geri yöndeki yeniden hızlanma yavaş: kapsül ~200 cm/s², klip 0→238 cm/s'ye 1.13 s'de çıkıyor.
- **A↔D yan ters dönüş:** hâlâ RevTurn'e gidiyor. Anahtarı yanları da kapsayacak şekilde genişlettim (2); bu, yan dönüşe geri pivot verdi ve sürüklenme 199 cm'ye çıktı. Reddedildi. Yan dönüş için kendi veritabanında yan pivotlar gerekiyor.

### 1.5 Denenen, ölçülen, üretime alınmayan aday (kurulu, kapalı)
"Ağır çekim yeniden itiş"i doğrudan çözmek için hız yetkisini kapsül ile içerik arasında eşleştirmeyi denedim:

- **İçerik:** iki pivot (`SHM223_JogPiv_F_B` / `_B_F`), V2.16 yöntemiyle kapsül yoluna yazıldı. Hedef itiş 420 cm/s²; önce zaman bükme, sonra destek ayaklarının dünyaya sabitlenmesi.
- **Hareket modeli:** `GR223_RevPushAccel` (sıfır geçişinden sonra ek ivme) ve `SHM223_JrHold` (bölümü itiş boyunca açık tutma).
- **Ölçüm:** kapsül yazılan eğriyi neredeyse birebir izledi. Ama hızlı itiş SHME'nin yakalama noktası hatasına dayalı **denge toparlama** veritabanını (`PSD_SHM_Recovery_L`) tetikledi; toparlama adımları itişin ortasına girdi. Bölümü açık tutmak da bunu engellemedi; sürüklenme arttı.
- **Sonuç:** üretime alınmadı. Daha hızlı itişten önce toparlama talebinin bu durumda kapatılması gerekiyor.
- **Tuzak:** kopyalanan klipler kaynaklarının veritabanı giriş notify'larını miras alıyor (`PSD_CP2_JogPivots`, `PSD_SHM_Redirect_JogReversal`). Bunlar temizlendi; doğrulamada sızıntı yok.

### 1.6 Hız–ritim–adım uyumu (sabit hızlı 2.5 s pencereler, `cad223.py`)

| Gait / yön | Hız (cm/s) | Adım sıklığı (spm) | Zeminde adım (cm) | Adım / beklenen | Oynatma hızı |
|---|---|---|---|---|---|
| Yürüyüş ileri | 132 | 108 | 73 | 1.00 | ×1.24 |
| Yürüyüş geri | 125 | 100 | 77 | 1.02 | **×0.72** |
| Yürüyüş sağ / sol | 112 | 109 / 104 | 62 / 62 | 1.00 / 0.95 | ×1.24 / ×1.15 |
| Tempolu ileri | 300 | 164 | 111 | 1.00 | ×1.01 |
| Tempolu sağ | 255 | **136** | 113 | 1.01 | **×0.84** |
| Tempolu sol | 255 | 177 | 86 | 1.00 | ×0.96 |
| Tempolu geri | 245 | 169 | 88 | 1.01 | ×0.92 |
| Depar ileri | 490 | 173 | 171 | 1.00 | ×0.81 |
| Depar, yan sınır (416) | 416 | **148** | **169** | 1.00 | **×0.69** |

Okuma:

- **Ayak–yol uyumu:** zemindeki adım her yerde beklenen adıma eşit (0.95–1.02). Yani kalıcı koşuda ayaklar kaymıyor; stride warping tutuyor.
- **Ağır çekim etkisi oynatma hızından geliyor.** MM oynatma hızı = kapsül hızı / klibin indeksli kök hızı. Üç yerde ara hız için içerik yok:
  - yana deparın hız sınırında depar döngüsü ×0.69 oynuyor: 148 spm'de 169 cm'lik uzun ve yavaş adımlar,
  - geri yürüyüş ×0.72,
  - sağa tempolu ×0.84 ve sola göre asimetrik.
- **Tempolu ileri koşu insan değerinde:** 3 m/s'de 164 spm. "Tempoluda depar klibinin yavaşlatılması" kalıcı koşuda görülmüyor.
- **Düzeltme:** bu hızlar için içerik gerekiyor. Bu turda yapılmadı, açık.

## 2. Yeni ve yeniden tasarlanan karakter hareketleri

| Hareket | Durum | Ölçüm / not |
|---|---|---|
| Tempolu kalkış ("depar gibi atılım") | **açık** | Gövde tepesi 34.5° (kalıcı tempolu 18–27°), 0.5–0.9 s'de; eller 35–46 cm öne. Klibin kendisi en fazla 10.5° (döngüden düşük). PBI ~5° ekliyor (kapatınca 29.1°), SHME APA 0. Kalanı çalışma zamanı ve görünür gövdeye aktarım. Seçim doğru (`SHM_JogQ_*` sessiz kalkış). |
| Farklı idle sürelerinden ileri/yan/geri/çapraz başlangıç (`s23_idle`, `s23_jstart`) | **korundu** (V2.22) | Başlangıçlar 1.1–4.4 s farklı idle sürelerinden başarıyla seçildi. V2.22 kollu başlangıç içeriği ileri yönde kullanılıyor; yan ve geri V2.8 yolunda. |
| Geri→ileri tempolu ters dönüş | **kaynak yeniden düzenlendi** | Pivot duruşu işlendi (bölüm 1). |
| Kısa basış / bırakma | **açık** (V2.22'den devralındı) | Değişmedi. |
| Arazide adımlama | **açık**, ölçüldü | Tempolu tümsek: sağ salınım ayağı 580 cm boyunca zemine <4 cm ve hızlı süzülüyor (alçak salınım). Yürüyüşte tümsek: sağda tek temasta 28.5 cm kayma. Alçalma: solda 32.5 cm. Yan eğim: sol alçak salınım 225 cm. FootPlacement basılan ayağı yerleştiriyor; salınan ayağın açıklığına sahip yok. Pilot adımlama kurulmadı. |
| Bakış eşliği (göz / baş) | **açık**, incelendi | MM ABP'de bakış değişkenleri: `LS_LookDriven`, `SHM_LookRate`. Yüz son işlem ABP'sinde: `EnableHeadMovementIK`. Gövde ABP'sinde göz kontrolü yok; yüz RigLogic ile kopya-poz. Uygulanmadı. Desteklenmeyen göz kontrolü varmış gibi raporlanmıyor. |
| Nefes / efor | **korundu** (V1.3.7) | ABP'de `SHM_BreathAlpha` / `SHM_BreathRate` / `SHM_BreathTime`. SHME `Exertion` ile derinleşen ve hızlanan nefes katmanı mevcut. Bu turda yeniden ölçülmedi: NOT_TESTED. |
| Zıplama / iniş | NOT_TESTED | İncelenmedi. |

## 3. Kamera, bakış, kadraj, netlik ve ışık algısı

### 3.1 Kritik bulgu: yatay pivot ofsetleri kameraya ulaşmıyordu
- **Kanıt:** graf dökümü ve kamera dünya yolu karşılaştırması.
  - `BP_GR_Player.GR_CameraSafeOrigin`, istenen pivota (yükseklik + `GR_SHM_PivotOffset` = SHME `CamOffset`) güvenlik izi çekiyor. Ama sonuç olarak `MakeVector(0, 0, GR_SafePivotZ)` döndürüyor; X/Y atılıyor.
  - SHME'de takip açıkken ileri ofset −5.6 cm oldu, ama kameranın dünya yolu ofsetsiz koşuyla 0.1 cm'ye kadar aynıydı.
- **Etkisi:** V1.3.x'ten bu yana şu yatay ofsetlerin hiçbiri kamerada görünmedi:
  - fren ve ivme taşıması,
  - dönüş taşıması,
  - dönüş kompozisyonu,
  - yan kaçış,
  - V2.21 look-ahead (raporda 4→18 cm).

  Bunlar kör ayarlanmış. Yalnız dikey parçalar (adım çökmesi, iniş, gövde yüksekliği) kameraya ulaşıyordu.
- **Düzeltme:**
  - Profil anahtarı `GR223_PivotXY` eklendi.
  - Açıkken XY ofseti, izin engelsiz kalan oranıyla ölçekleniyor (güvenlik önce) ve aktör eksenine çevrilerek geçiriliyor.
  - Çarpışma güvenliği korunuyor: koridorda 0 kare ihlal.
  - **Üretimde 0**, gerekçesi 3.3'te.

### 3.2 Uygulanan algısal davranışlar (aday)
- **Kamera eksenine göre yumuşak bölge takibi** (`CamFollowEnabled`):
  - Bölge: yanal 12 cm, derinlik 10 cm.
  - Bölge içinde takip noktası dünyada yerinde kalıyor; küçük adım, kısa basış ve yerleşmelerde kamera kıpırdamıyor.
  - Bölge kenarında, kapsülün kendi eksen hızı referans alınarak kritik sönümlü çekiliyor; sabit hızda gecikme yok.
  - Dururken yavaşça ortalanıp duruyor; duruşta sürekli salınım yok.
  - Durum dünya X/Y'de saklanıyor (kamera ekseninde saklamak fare dönüşlerinde ±13 cm savrulma üretiyordu).
- **Görüş yönlü look-ahead:**
  - İleriye çekiş yalnız kamera yönünde ilerlerken; yanlara ×0.5.
  - Geri koşuda kameraya doğru çekiş yok.
  - Kontrol yönüne geri besleme yok: bakış gecikmesi 0.
- **Kör ayarlanmış fren ve ivme taşıması:** ofset görünür hâle gelince tempolu W→S'de kamera sarsıntısı 2.1'den 7.8 cm/kare²'ye çıktı. Kapatınca 2.6'ya döndü.

### 3.3 Neden üretime alınmadı
Ölçümler kameranın dünya yolu üzerinden, aynı senaryolarla yapıldı:

| Senaryo | V2.22 | Aday (takip + taşıma 0) | Aday + dönüş ofsetleri 0 |
|---|---|---|---|
| Yürüyüş başlangıçları, en büyük sarsıntı | 0.56 | 3.7 | 0.70 |
| Kesiş→ters, en büyük sarsıntı | 2.8 | 5.8 | 5.2 |
| Deparda fare dönüşleri: ekran yatay aralığı | 0.11 | 0.40 | 0.25 |
| Deparda fare dönüşleri: sarsıntı 95. yüzdelik | 2.0 | 2.3 | **9.2** |
| Kısa basışlarda kamera yolu (kapsül 43 cm) | 64.5 cm | 62.2 cm | 57.0 cm |
| Bakış gecikmesi / çarpışma ihlali | 0 / 0 | 0 / 0 | 0 / 0 |

- Takip ve eski dönüş ofsetleri birbirine bağlı davranıyor. Hiçbir ayar her senaryoda V2.22'den iyi değil.
- Kural gereği başarısız aday üretime alınmadı.
- Kod ve anahtarlar kurulu (`GR223_PivotXY` 0, `CamFollowEnabled` false).
- Sonraki tur: takip ile dönüş ofsetlerini gait başına birlikte ayarlamak ve her senaryoyu kamera dünya yolunda ölçmek.

### 3.4 FOV, netlik, pozlama: ölçüldü, değiştirilmedi
- **FOV:** tek sahip, mevcut hız FOV'u (`CamFOVSpeedMax` 0). İkinci bir etki eklenmedi.
- **Netlik:** kamerada odak 260 cm sabit, f/8, ~20 mm odak uzaklığı. Bu pratikte hiperfokal; görüntüde alan derinliği yok. İnceleme odağı için etkileşim sisteminde odak hedefi tutan bir değişken yok. Dinamik netlik kurulmadı.
- **Pozlama:**
  - Tek sahip `EX_PostRain_NeutralExposure`: sınırsız hacim, histogram tabanlı, bias −0.65, EV −2…16.
  - Uyum hızı yükselme 5 / alçalma 5. Bu, UE varsayılanından (3/1) belirgin hızlı; pencere ve iç–dış geçişlerinde pompalama riski taşıyor.
  - Görüntü ölçümüyle doğrulanmadığı için üretim haritasında değiştirilmedi. Açık.
- **Lens etkileri:** hareket bulanıklığı 0.25, vinyet 0.2, kromatik sapma 0.1. Artırılmadı.

## 4. Çevre teması, efor ve ses

| Hedef | Durum |
|---|---|
| Dar geçişte omuz / kol toplama | Uygulanmadı (açık). |
| Masa / korkuluk / kapı kenarına el teması | Uygulanmadı (açık). Etkileşim sistemi `AC_Interact_AAMS`; odak hedefi değişkeni yok. |
| Nefes / efor | Mevcut V1.3.7 katmanı (bölüm 2), yeniden ölçülmedi. |
| Ayak sesi / yüzey / iç–dış ses | Değiştirilmedi. Mevcut sahiplik: `AC_Footsteps_AAMS` ve foley notify'ları. İç–dış karışım durumu yok. Açık. |

Bu hedeflerin çalışan pilot örnekleri bu turda üretilmedi. Turun süresi, kritik hareket hatasının ve kamera hatasının kök nedenlerine harcandı. Bunu açıkça belirtiyorum.

## 5. Test kapıları

- **Kalıcılık:**
  - Kayıttan sonra temiz açılışta doğrulama: `ALL_OK`.
  - Editör kapatılıp açıldıktan sonra doğrulama: `ALL_OK` (`verify_prod223_final.txt`, `verify_prod223_reopen.txt`).
  - Kirli paket yok.
  - `Accessed None` günlük hatası: 0.
- **İlk kullanım:** veritabanı önbelleği yenilendikten ve editör açıldıktan sonra ısınmasız ilk koşu, ısınmalı koşuyla aynı klip zincirini ve sayıları verdi.
- **Regresyon (sabit 30):** aşağıdaki testlerde ani ivme sayıları ve kamera değerleri V2.22 ile aynı (bkz. `final223.txt`):
  - pilot rota, gerçek harita rotası r1/r2,
  - kesiş→ters (sağ/sol), depar ve tempolu fare dönüşleri, ani duruşlar,
  - yürüyüş başlangıçları, yeniden başlama, kısa basış ve basılı tutma,
  - arazi ve koridor çarpışması.

  Değişiklik yalnız tempolu geri→ileri ters dönüş yolunda.
- **Kare hızı** (`fps223.txt`): sabit 20/60/120 FPS. S→W'de iki senaryo × dört kare hızı:

  | | 20 FPS | 30 FPS | 60 FPS | 120 FPS |
  |---|---|---|---|---|
  | V2.22, en kötü kayma (ws / ovl) | 49 / 55 | 52 / 54 | 16 / 27 | 17 / 43 cm |
  | V2.23, en kötü kayma (ws / ovl) | 44 / 36 | 17 / 15 | 15 / 21 | 18 / **110** cm |
  | V2.22, üst gövde en büyük ani ivme | 135 | 296 | **1062–1108** | **1975–2053** m/s² |
  | V2.23, üst gövde en büyük ani ivme | 29–30 | 28–41 | 39–43 | 75–91 m/s² |
  | V2.22, gövde öne eğimi tepesi | 27–33° | 31° | 33° | 34° |
  | V2.23, gövde öne eğimi tepesi | 30° | 51° | 49° | 48° |

  Okuma:

  - V2.22'nin depar dönüş kavisi yüksek kare hızında çok büyük poz sıçramaları üretiyordu; V2.23'te bunlar yok.
  - En kötü kaymanın ortalaması 39 cm'den 34 cm'ye iniyor.
  - **Yeni kusur 1:** 20 FPS'te MM, geri→ileri dönüşte ters yönlü pivotu (`A_CP2_Jog_Fwd_Pivot`) seçiyor.
  - **Yeni kusur 2:** 120 FPS'teki bir tekrarda sağ ayak 110 cm kayıyor.
  - Bu iki kusur ve itişteki öne eğilme nedeniyle durum PARTIAL. Sonuçlar seçilmedi; bütün tekrarlar yazıldı.
- **Gerçek zaman** (değişken kare süresi, ~30 FPS): doğru pivot seçildi. S→W en kötü kayma: sol 21.1 / sağ 11.5 cm. Mouse dönüşleri ve kısa basışlar çalıştı. Sabit adımlı test gerçek oynanışın yerine sayılmadı; ikisi ayrı etiketlendi.
- **Maliyet:** üretimde yeni her-kare iz yok. Kurulu adaylar kapalıyken çalışmıyor; MontTick'e yalnız iki nokta çarpımı eklendi.

## 6. Repertuvar sınıflandırması

| Hareket | Sınıf |
|---|---|
| Tempolu geri→ileri ters dönüş | kaynak yeniden düzenlendi + runtime düzeltildi (PARTIAL; itiş eğimi açık) |
| Tempolu ileri→geri ters dönüş | korundu (açık: evreye bağlı 4–52 cm) |
| Tempolu A↔D ters dönüş | korundu (açık) |
| Tempolu kalkış | açık (sahibi ölçüldü) |
| Yürüyüş başlangıcı (V2.22) | korundu |
| Depar dönüş sonrası yeniden itiş (V2.22) | korundu |
| Kısa basış | açık |
| Arazide adımlama | açık (ölçüldü) |
| Kamera (V2.22 yakınlık, adım ritmi) | korundu; yatay ofset hatası bulundu (aday kapalı) |
| Bakış eşliği, netlik odağı, pozlama, dar geçiş, el teması, ses | açık |
| Zıplama / iniş | NOT_TESTED |

## 7. Geri alma
- **A1:** `ABP_GR_MotionMatchingBase` CDO'da `SHM223_RevRearGate` 0 ve `SHM_RedirectDB_JR` = `PSD_SHM_Redirect_JogReversal`. Pivot duruşu için: `checkpoint/SHM_DPP_Jog_Bwd_Pivot.pre223.uasset`.
- **Bütün graf değişiklikleri:** `Saved/Codex/SHME_V223_20261022/checkpoint/` altındaki kopyalar (editör kapalıyken). Ayrıntı: `CHANGES_V223.md`.

## 8. Medya (normal hız; değiştirilmemiş kareler)

Bütün kayıtlar sabit 30 FPS oyun zamanıyla alındı, yani oynatma gerçek hızda. Görünür gövdede yalnız PIE'ye özel kil test görünümü kullanıldı.

- **`vid/jogrev_SW_before_side`** / **`_after_side`**, **`_before_diag`** / **`_after_diag`**: tempolu S→W, V2.22 ile V2.23 karşılaştırması.
- **`vid/jogrev_WS_before_game`** / **`_after_game`**: tempolu W→S, oyun kamerası. Bu durum değişmedi ve açık.
- **`vid/jog_mouse_turns_game`**: tempolu koşuda fare dönüşleri; V2.23 üretimi, kamera V2.22.
- **`vid/jogstarts_side`**: farklı idle sürelerinden tempolu kalkışlar. Açık kusur: atletik kalkış.
- **`vid/taps_diag`**: kısa basışlar (açık).
- **`vid/map_r2_game`**: gerçek harita rotası.
- **`img/cam_before_after.jpg`**: kamera adayı C ile V2.22, oyun kamerası. Fark ince, aday üretimde değil.

Not: oyun kamerası kareleri görüntünün ortasından kırpılmıştır; kadraj tam ekrandan daha yakın görünür.

## 9. Süreçte bulunan ve giderilen tuzaklar
- **LastHitBy hatası geri geldi:** MontTick lisp kaynağından yeniden kurulunca V2.21'deki çeviri hatası döndü. Kamera yönü testi dünya X'ini okuyordu; testlerde kamera yönü 0 olduğu için görünmedi.
  - Doğrulama `lasthitby_linked` ile yakaladı.
  - Onarım yeniden uygulandı; kurulum betiği artık bunu her seferinde kendisi yapıyor.
- **Ölçüm altyapısı:** bellek koruması editörü yeniden başlatınca bir ölçüm grubu eski editör günlüğünü okudu ve 0 satır döndü. Ayrıca yeniden başlatma gerçek zamana geçebiliyordu. `lib223.sh` iki sorunu da düzeltti.
- **Veritabanı sızıntısı:** kopyalanan kliplerin miras aldığı veritabanı girişleri üretim veritabanlarına girmek üzereydi. Temizlendi; doğrulama artık bunu kontrol ediyor.

## 10. Kullanıcı kabulü için oyunda deneme
1. Shift'e kısa basıp tempoluya geçin. W ile ileri koşun, S'ye basıp geri koşun, sonra tekrar W'ye basın.
   - Beklenen: yerinde fren, sıçramasız öne itiş; bacaklar gövdeyle aynı hızda.
   - Bilinen: itişte gövde belirgin öne eğiliyor.
2. Tempoluda W→S: değişmedi. Bazı adım evrelerinde ayak kayabilir.
3. Kamera V2.22 ile aynı. Yatay ofset ve takip adayı bir sonraki tur için kurulu ama kapalı.
