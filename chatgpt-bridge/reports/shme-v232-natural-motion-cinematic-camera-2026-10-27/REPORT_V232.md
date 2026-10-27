# SPHIRUS — SHME V2.32: doğal insan hareketi + fiziksel tepkili sinematik takip kamerası (2026-10-27)

Taban V2.31 üretimi (Bridge efcf466). Blueprint-only UE 5.8, git yok; checkpoint + editör yoluyla değişiklik. Tüm sayılar sabit adımlı
editörde aynı girdiyle ölçüldü (aksi yazılmadıkça 30 FPS, `contact231` en kötü basılı-ayak kayması / sürüklenmesi, cm). "Teknik PASS"
görsel/oyun hissi kabulü değildir: aşağıdaki görsel kayıtlar sizin değerlendirmeniz içindir, kabul olarak yazılmadı.

**Üretime alınanlar (4 grup):** `camera` (sinematik yörünge), `bfexit` (B_F ters dönüş DB'lerine ileri çıkış döngüsü), `loadedbf`
(yük altında B_F yakalama adımı ailesi + çıkış döngüsü), `floorguard` (T7 salınım ayağı zemin koruması).
**Reddedilen / üretime alınmayan:** tick sırası (tk / IntentTickPrePhysics), başlangıç hız bağlama (sb), idle-duruş başlangıç kopyaları
(nötrleştirildi), duruş klibi yeniden pişirme (geri alındı), basılı-ayak bırakma açısı (etkisiz), T6 pelvis gecikmesi telafisi.

**Doğrulama:** promote232 kaydı temiz (dirty []); temiz yeniden açılışta `verify232` **ALL_OK = true** (V2.29–V2.31 sözleşmeleri +
V2.32: knob'lar, ABP DB yolları, yörünge kablolaması, fonksiyon düğümleri, X DB çıkış döngüleri, LoadRevFwd 30 + P21/P30, IntentTickPrePhysics
false, bağlı LastHitBy yok). ALL_OK yapılandırma kontrolüdür; doğal hareketin görsel kabulü değildir.
**Ölçüm hacmi:** bu turda ~700 A/B koşusu (2'si geçersiz: P1 zaman aşımı = benim kuyruk hatam; bir ISO koşusu INVALID_STATE, tablolardan
düşüldü) + 120 soak döngüsü + ~23 kayıt.

## 0. Baştaki 14 soru — doğrudan cevaplar

1. **Düşük hızlı dönüşün 60 FPS kötü evresi düzeldi mi?** — *Kısmen, ölçülebilir iyileşme.* s29_swl12: 60 FPS 20.7 → 20.7 (değişmedi),
   30 FPS 11.6/11.0 → 11.1/11.1, 20 FPS 18.8 → 9.0, gerçek zaman 56.4 → 11.1. 60 FPS'teki ~21 cm evre hâlâ var; sahibi vendor pivot →
   yavaş B_F klibi giriş evresi (S1 teşhisi). **Açık.**
2. **Yüklü yakalama adımlı hareket bütün girişlerde güvenilir mi?** — *Yükleme kutularının hepsi kapıdan geçiyor, iki giriş korumalı geri
   düşüşte.* B_F yüklü aile 32/32 kutu kapıdan geçti (gerçek destek ayağı / evre / giriş hızı / blend sırası). F_B'de P29 yeniden üretildi
   (b_short 16); P21/P30 hiçbir varyantta geçmedi (plan diğer ayağı iki kez yere koyuyor) → bu iki girişte üretimdeki V2.26 klipleri
   güvenli geri düşüş olarak kalıyor (PSD_SHM231L_LoadRevFwd = 30 yüklü + P21/P30). FPS'ler arası: e29_load 30 FPS 15.0 → 6.5/12.4, 60
   14.7 → 12.6, 120 29.8 → 15.3, 20 13.9 → 9.0, gerçek 43.5 → 12.5.
3. **Eforlu dönüşlerdeki 60/120 FPS kaymaları giderildi mi?** — *Büyük ölçüde.* e29_chain 60 FPS 26.1 → 19.8 (V2.31 başlangıcı 14.3 →
   26.1 gerilemesinin yarısı geri alındı; tamamı değil), 30 FPS 25.4 → 6.5, 120 FPS 33.5 → 17.3. e31_s2_4750 20 FPS 21.9 → 7.0, 30 FPS
   15.5 → 6.5/11.1. Sahip: B_F DB'lerinde ileri çıkış döngüsü yoktu → klip sonunda bir kare başka B_F kutusuna arama (tek kare seçim
   sıçraması); X DB'leri ile blip 82 → 57 (P2, 54 koşu).
4. **Duruştan geri kalkış ve durma kapanışları doğal mı?** — *Durma kapanışı: belirgin iyileşme. Geri kalkış: açık.* c30_calm 33.3 →
   17.9, wdiag 21.6 → 12.5 (T7 zemin koruması: kapanış adımındaki ayak artık zeminin altından geçmiyor). Gerçek idle duruşundan geri kalkış
   (j30_slow / jback) 38 cm'de kaldı: AAMS türevli JogQ başlangıçları üretim idle duruşundan ayak başına 16 cm farklı başlıyor; idle-duruş
   kopyaları 38 → 22'ye indirdi ama bırak→yeniden bas girişinde MM kopyayı da seçti (j30_rel_3200 35 → 54) → üretime alınmadı.
   **Açık** (çözüm: duruş süresine bağlı rota).
5. **Yan/arka çapraz geçişlerde basılı ayak sürüklenmesi çözüldü mü?** — *Hayır.* c29_combo 48.8 (V2.31; son üretimde sayısal 57.6 = sınıflayıcı bölümlemesi, kusur penceresi kare-aynı, bkz. 2D), a29_angb 33.5 → 21.0/23.4
   (iyileşme, zemin koruması). Sahip teşhisi: yön anahtarındaki blend basılı ayağı 108–178° döndürüyor; FootPlacement o ayağı hiç
   basmıyor (blend hızı SpeedThreshold 60 üstünde) → bırakma açısı (pb90/pb120) etkisiz. **Açık.**
6. **Üst gövde ve kollar daha doğal mı?** — *Denetlendi; değişiklik yapılmadı.* Yürüyüş makul (kol 27 cm, baş yanal 4.5 cm, gövde 4°).
   Depar duruşu (gövde 29° öne, baş yanal 14 cm, omuz/kalça 53°) KLİPTEN geliyor: PBI / eğim eğrisi / settle / omurga karşı-dönüş / ham IK
   hepsi kapatılınca değişmiyor. Hafif atletik okunuyor; düzeltme klip yeniden yazımı gerektirir. **Aday yok, açık bulgu.**
7. **Efor ve toparlanma beden hareketiyle görünüyor mu?** — *Yük altındaki iki yönde evet (ölçüm + kayıt), toparlanmada kısmen.* Yüklü
   B_F + F_B yakalama adımı ailesi üretimde; e29_recov 31.6/32.7 → 26.9/26.4 (iyileşme ama hâlâ > 20). Rastgele sendeleme eklenmedi.
8. **Kamera hangi fiziksel durumlarda üç çeyrek açıdan gösteriyor?** — Depar sırasında sert dönüşte gövde görüş yönüne göre döndüğünde
   (sprint 90° yörünge 13.7°), fren ortasında ikinci yön isteğinde (12.9°), duvar yanında dönüşte yan boşluğa göre kısılmış (8.2°),
   tempolu 90°'de hafif (2.3°). Yürüyüşte neredeyse yok (0.5°), duruşta, bakışta, dar alanda, incelemede ve depar 180° (strafe ailesi:
   gövde görüşe bakmaya devam ediyor) 0.
9. **Oyuncu fareyle bakarken otomatik kamera nasıl davranıyor?** — Kontrol yaw'ı değiştiği anda hedef 0'a iner (bakış kapısı) ve bakıştan
   sonra 1.2 s daha hızlı (0.4 s) yerleşmeyle 0'da kalır. Kamera kontrol yaw'ını hiç yazmaz; hareket girdisinin yön referansı kontrol
   yaw'ında kalır (d_ctl 0.00°, d_vin 0.0° bütün senaryolarda). Yürürken bakışta 0.1°, duruşta bakışta 0.
10. **Odak ve orbit yürüyüşte sakin, deparda anlamlı mı?** — Evet, ölçüldüğü kadarıyla: yürüyüş ≤ 0.5°, tempolu 2.2–2.3°, depar 12.9–13.7°;
    jerk95 değişmedi (0.57 → 0.60), FOV / zoom / shake / roll artışı yok. Görsel kabul sizde.
11. **Kamera dar alanda güvenli mi?** — Yörünge yalnız boom yaw'ına eklenir; GR_UpdateRig'in bütün çarpışma izleri aynı döndürücüden
    kurulur (yörünge çarpışma kontrollü). Yan boşluk + iç mekân ölçeği: koridor / incelemede 0; duvar yanında 8.2°'ye kısılır; min kamera-
    kapsül mesafesi değişmedi (78 cm duvar, 195 cm açık). Teknik PASS; görsel kabul sizde.
12. **Arazi yükseliş/inişinde iki ayak uyumlu mu?** — *Hayır, açık.* 28–30 cm basamakta arka ayak 11 cm fazla yüksekten geçiyor ve
    0.13 s asılı kalıyor, pelvis 0.9 s geç yerleşiyor. T6 (pelvis gecikmesi telafisi) arka ayak tepesini 11 → 13, tempolu inişi 10.8 →
    16.3 kötüleştirdi → reddedildi. T7 zemin koruması basamaklarda nötr.
13. **PIE assertion, bellek, test süreleri?** — IsUnique: 2038 tarihî koşuda 4 çökme (V2.31'de 3); bu oturumda ~700 A/B koşu + 120 soak
    döngüsü (20 çıplak PIE + 100 harness sonu) → 0 çökme; motor PDB yok, ortak tutucu yalnız MediaCapture (çökmeler yakalama dışı
    koşularda) → istatistiksel olarak sonuçsuz, **açık**. Bellek: kendi hatam olan yörünge LastHitBy hata seli (kare başına 3 satır) bulundu
    ve onarıldı; kalan log yükü test telemetrisi (`SHM|` satırı, kare başına ~1.6 KB, yalnız TelemetryEnabled) → 38 GB koruması ~60–80 dk'da
    bir yeniden başlatıyor (her biri loglandı). Süre: sabit-30 koşu ~35–45 s.
14. **Son üretimde ne açık, ne aday, ne eksik?** — Bölüm 14 tablosu.

## 1. Başlangıç ve koruma
- Taban: V2.31 üretimi (Bridge efcf466). Taze sabit-30 editörde `verify231` ALL_OK.
- Checkpoint `checkpoint/pre_v232`: 181 dosya / 141 MB. Kapsam: piyon, ABP, SHME, DA, profiller, kamera BP'leri, harita, V226 + V231 animasyon klasörleri ve araçlar.
- Sonradan alınan ek checkpoint'ler:
  - Stops ve Starts/Jog klasörleri;
  - A_CT_Jog/Walk_Fwd;
  - `pre_lhb232` (bileşen, LastHitBy onarımından önce).
- **Kendi hatam — checkpoint boşluğu:** `stopfix232` /Game/GraceRanger/Animations klasörünü de taradı. Bu yüzden 6 klip checkpoint'siz yazıldı:
  - 4 `A_CT_Sample_*` klibinin referansı yok;
  - `A_CT_Ref_Walk_Stop_F_L/R` iki ABP'de referanslı.
  - Değişiklik, kapanış adımının bir kısmında ≤1.2 cm salınım ayağı kaldırması; bacak koruması geçti.
  - Bu değişiklik birebir geri alınamaz; tek kaynak OneDrive sürüm geçmişi. Klipler korundu ve burada bildiriliyor.
  - Yeni kural: bir üretecin *taradığı* her klasör checkpoint'lenir.
- Oturum düzeni:
  - her aday ayrı bayrak;
  - üretim → aday aynı oturumda iç içe (interleaved) ve 2 tekrar;
  - FPS sabit-adım editör argümanı (her mod için yeniden açılış, nedeni loglandı).

## 2. Hareket kusurları

### 2A Eforlu dönüş gerilemeleri — ÜRETİMDE (bfexit + loadedbf)
- **Tek kare seçim sıçraması** (blip232):
  - V2.31'in 82 koşusunda 139 adet görüldü.
  - Sınıf (a): B_F klibi biter, MM sonunda bir kare başka bir B_F kutusuna geçer, sonra çıkış ailesine döner. O karede görünen toplar 440–640 cm/s sıçrıyor.
  - Sahip: B_F DB'lerinde ileri çıkış döngüsü yok (F_B DB'lerinde var ve orada sıçrama yok).
- **Onarım** — yeni varlıklar:
  - PSD_SHM232_JogRevBwdX ve PSD_SHM232_LoadRevBwdX: B_F klipleri + A_CT_Jog_Fwd;
  - PSD_SHM232_SlowRevBwdX: yürüyüş + tempolu döngü.
  - ABP DB yolları bunlara çevrildi.
- **Yüklü aile:** B_F 32/32 kutu kapıdan geçti. F_B'de P29 yeniden üretildi. P21/P30 üretim klibiyle geri düşüşte.
  - PSD_SHM231L_LoadRevFwd **yerinde** yeniden kuruldu: checkpoint pre_v232'de; geri alma checkpoint kopyasıyla.
- **Sonuçlar** (P2, 2 tekrar):

  | Senaryo | Önce (cm) | Sonra (cm) |
  |---|---|---|
  | e29_chain | 25.4 | 6.5 |
  | e29_load | 15.0 | 6.5 / 12.4 |
  | e31_s2_4750 | 15.5 | 6.5 / 11.1 |
  | e31_s2_4900 | 15.0 | 11.1 / 13.6 |

  - Blip 38 → 17 (bu 15 senaryoda).
- **FPS** (o → P, tek tekrar):

  | Senaryo | FPS | Önce (cm) | Sonra (cm) |
  |---|---|---|---|
  | e29_chain | 60 | 26.1 | 19.8 |
  | e29_chain | 120 | 33.5 | 17.3 |
  | e29_load | 120 | 29.8 | 15.3 |
  | e31_s2_4750 | 20 | 21.9 | 7.0 |
  | e31_s2_4750 | gerçek zaman | 41.2 | 22.0 |

### 2B Düşük hızlı dönüş 60 FPS — AÇIK
- s29_swl12: 60 FPS 20.7 → 20.7; diğer modlarda iyileşme (20 FPS 18.8 → 9.0, gerçek zaman 56.4 → 11.1).
- Sahip: vendor pivot'tan yavaş B_F klibine giriş evresi.
- Bu tur bu evreye özel aday üretilmedi. "Belirli FPS adına gizli çözüm" kuralı gereği 60 FPS'e özel ayar yapılmadı.

### 2C Duruştan geri kalkış — AÇIK (iki aday reddedildi)
- **sb (başlangıç hız bağlama, V2.28 klip-bağlı kapsül):**
  - jback 21.8 → 43.1, d_back 21.8 → 26.6, j30_rel_3200 54 → 62, jstart 48.6 → 59.5. Reddedildi.
  - ABP terimi knob 0 ile kurulu kaldı (SHM232_StartBind = 0, davranış yok).
- **Başlangıç sabitleme (pinstart) ve idle-duruş kopyaları (SHM232_IS_*):**
  - Gerçek idle'dan geri kalkış 38 → 22.
  - Ama j30_rel_3200 35 → 54 ve jstart 48.6 → 68.9.
  - Kopyalar nötrleştirildi: orijinal kemik izleri geri yazıldı, ek eğriler silindi (max fark 0.0 cm).
  - Python'da DB girdi silme API'si yok ve BranchIn kaldırmak girdiyi silmiyor. Bu yüzden kopyalar başlangıç DB'lerinde birebir eş olarak duruyor; davranış değişikliği yok.
  - Kalıcı silme editör arayüzünden yapılabilir.

### 2D Yürüyüş / tempolu duruş kapanış adımı — ÜRETİMDE (floorguard)
- **İzolasyon:** c30_calm 33.3 tüm çalışma zamanı katmanlarında aynı kaldı:
  - settle kapalı 33.3, FootPlacement kapalı 32.4;
  - bütün IK/warping kapalı 32.3;
  - PBI ve fren duruşu kapalı da aynı.
- Klip yeniden pişirme (minclear) etkisizdi (33.3 → 33.4); 23 duruş klibi checkpoint'ten geri yüklendi.
- **Sahip:** MM çıkış pozundaki salınım ayağı zemin bandının 0.7–5.6 cm altından geçiyor.
- **T7 SwingFloorGuard 1.5 cm:** temas dışındaki ayağın poz merkezi, kendi basılı yüksekliği + 1.5 cm'nin altındaysa en çok 6 cm kaldırılır.
- **Sonuçlar:**

  | Senaryo | Önce (cm) | Sonra (cm) |
  |---|---|---|
  | c30_calm | 33.3 | 17.9 |
  | wdiag | 21.6 | 12.5 |
  | a29_angb | 33.5 | 21.0 / 23.4 |
  | jstart | 48.6 | 45.8 |

  - Basamaklarda nötr.
- **İzolasyondaki iki "gerileme" (kendi analizim; ham veriler data/'da):**
  - **c29_combo 48.8 → 57.6** (yalnız fg):
    - koşu boyunca o ile fg arasındaki en büyük top farkı 3.9 cm;
    - kusur penceresi (vendor yürüyüş pivot'u → A_LB_Walk_Left) kare kare aynı.
    - Fark, temas sınıflayıcısının bölümü farklı karede başlatmasından geliyor (i0 260 / 272). Fiziksel kötüleşme değil.
  - **j30_rel_3450 24.5 → 27.3** (yalnız P):
    - fg tek başına 19.4 (r2 INVALID_STATE, düşüldü);
    - P ile Pnf ilk adımdan sonra MM dalında ayrılıyor (6.4 s'de 80 cm yol farkı);
    - en kötü değer sonraki bir duruş klibine kayıyor. Dal ayrışması; sahip değil.
  - j30_rel_3200 120 FPS'te 14.1 → 34.8 ve 20 FPS'te 30.9 → 38.0 gibi tek tekrarlık FPS sonuçları da aynı ayrışma sınıfında. **Açık izleme maddesi.**

### 2E Yan / arka çapraz geçişler — AÇIK
- pa90 / pa120: canlı PlantSettings düzenlenemedi, NOT_TRIGGERED.
- pb90 / pb120: ABP CDO yolu ile uygulandı ama her metrik üretimle aynı.
- FootPlacement, yön anahtarındaki ayağı blend hızı yüzünden hiç basmıyor; bırakma açısı kapı değil.
- Sahip: anahtar anındaki blend. Üretim değişikliği yok.

### 2F Bırak – yeniden bas — AÇIK
- j30_rel_3200 35.0 = 35.0, j30_rel_3450 24.5 → 27.3 (2D'de açıklanan dal ayrışması).
- Gerçek zamanda 30.7 → 23.8 ve 56.1 → 26.9.
- Sahibi geri kalkışla aynı: AAMS başlangıç duruşu farkı.

### Reddedilen: tick sırası
- tk (canlı ön-fizik) ve mevcut sahip bayrağı IntentTickPrePhysics: blip 15 → 6.
- Ama swl12 11.6 → 52.6, s180 35.9 → 71, wstart 14.2 → 33.7, d_sprint 16 → 27.
- Sistem tek karelik gecikmeye göre ayarlı (V2.28 öncü kareler, CP kapıları). Bayrak üretimde false; verify232 kontrol ediyor.

## 3. Efor
- Yük altında iki yönde yakalama adımı üretimde (2A). Toparlanma e29_recov 31.6/32.7 → 26.9/26.4.
- Destek aktarımı, ölçülü itiş ve kısa toparlanma klip ailesiyle geliyor. Yeni rastgele sendeleme yok.
- Görsel değerlendirme: `loaded_reversals_before_side` / `loaded_reversals_v232_side` kayıtları.

## 4. Üst gövde (upper232)
- Çerçeve: hareket hâlinde seyir yönü, durunca kalça hattı. Gövde, duruşa göre ölçüldü.

  | Yürüyüş tipi | Kol (cm) | Baş yanal (cm) | Gövde (°) |
  |---|---|---|---|
  | Yürüyüş | 27 | 4.5 | +4 |
  | Tempolu | 40 | 9 | 11 |
  | Depar | 60 | 14 | 29 öne (+ −5 → 32 depara girişte) |

- Depar duruşunun sahibi klip (sahip izolasyonu B7). Hafif atletik okuma için klip düzeyinde yeniden yazım gerekir; bu tur yapılmadı.

## 5–9. Sinematik kamera — ÜRETİMDE (camera)

**Tasarım:** yeni framework yok; mevcut SHME kamera katmanı + BP_GR_Player boom'u.
- `SHM_UpdateCameraV21` içinde bir **görsel azimut** (CamOrbitYaw) üretilir.
- Bu değer `GR_SHM_CamOrbit` üzerinden yalnız **boom yaw'ına** eklenir (MakeRotator_43.Yaw).
- Kontrol döndürmesi ve hareket girdisinin yön referansı hiç değişmez (girdi kontrol yaw'ında). Geri besleme döngüsü yok.

**Hedef:**
```
A(hız) × [sin(gövde yaw − görüş yaw) + 0.5·sin(seyir yönü − görüş yaw)] / 1.5 × yan boşluk × iç mekân ölçeği × konfor
```
- A: yürüyüş 2°, tempolu 8°, depar 16°.
- Gecikme 0.3 s, ardından kritik sönümlü yay (5 rad/s). Fren ve dönüş sırasında kamera eski yönü kısa süre taşır, sonra yeni takip yerine yerleşir.

**Oyuncu önceliği:** kontrol yaw hızı > eşik ise hedef 0 olur, 1.2 s tutulur ve 0.4 s'de yerleşir. İnceleme ve teleport'ta 0.

**Sıfır:** shake, FOV, zoom, roll artışı.

**Kritik hata ve onarım (kendi hatam):**
- Yörünge bloğu ilk kurulduğunda kontrol döndürmesini DSL çevirmeni yüzünden `Pawn.LastHitBy` (hep None) üzerinden okuyordu. Bu V2.21'deki MontTick hatasının aynısı.
- Sonuçları:
  - kontrol yaw 0 okunuyordu;
  - yörünge görüşe göre değil dünya X'ine göre hesaplanıyordu;
  - bakış kapısı hiç çalışmıyordu;
  - her karede 3 hata log'a yazılıyordu.
- Harness yaw0 = 0 ile koştuğu için ilk ölçümler makul göründü.
- Onarım: bileşen grafında `GetLastHitBy` → `Pawn::GetController`. `build_funcs.py` artık her yeniden kurulumda bunu uyguluyor; `verify232` bağlı LastHitBy arıyor.
- **Bütün kamera ölçümleri onarımdan sonra yeniden yapıldı (P2C).** Ek test olarak görüş, harekete başlamadan önce gerçek bakış girdisiyle 30° çevrildi: yörünge 13.7 = 13.7 (görüş yönünden bağımsız).

**Ölçümler (P2C, o / c2 = yeni kamera, sabit 30):**

| senaryo | yörünge max | beden yolu farkı | kontrol yaw farkı | jerk95 | min mesafe |
|---|---|---|---|---|---|
| depar sert sağ (s90) | 13.7° | 0.0 cm | 0.00° | 0.57 → 0.60 | 195 |
| aynı, görüş 30° (s90y) | 13.7° | 0.0 | 0.00 | 0.68 → 0.70 | 196 |
| fren + ikinci istek (brk2) | 12.9° | 0.0 | 0.00 | 0.68 → 0.69 | 195 |
| duvar yanında dönüş | 8.2° | 0.0 | 0.00 | 1.18 → 1.31 | 78 |
| tempolu 90° | 2.3° | 0.0 | 0.00 | 0.53 → 0.50 | 195 |
| analog çapraz tempolu | 2.2° | 0.0 | 0.00 | 0.65 → 0.65 | 193 |
| yürüyüş 45° | 0.5° | 0.0 | 0.00 | 0.32 → 0.32 | 191 |
| yürürken fare bakışı | 0.1° | 0.0 | 0.00 | 3.29 → 3.29 | 190 |
| duruşta bakış | 0.0° | 0.0 | 0.00 | aynı | 195 |
| depar 180° (strafe) | 0.0° | 0.0 | 0.00 | aynı | 184 |

**Ek ölçümler:**
- FPS: yörünge 20, 30, 60 ve 120'de aynı 13.7°; jerk95 değişmedi.
- Gerçek zamanda jerk maksimumu (61.6 / 36.8) kare takılmalarıyla çakışıyor (önceki kare 0.09–0.15 s). O karede yörünge 0°.
- Üç çeyrek süresi metriği (25–65°, hareket hâlinde) bu senaryolarda değişmedi (0.40 s). Sağa sert dönüşte gövde depar yönüne dönerken alfa zaten 25–65° bandını hızla geçiyor; yörünge bandın dışındaki açıyı artırıyor.
- B5'te sola dönüşte 0.40 → 0.93 s ölçülmüştü. Bu ölçüm onarım öncesine ait; yaw0 = 0'da değer geçerli, ama onarımdan sonra yeniden ölçülmedi.

## 10. Beden × kamera matrisi (A/B/C/D)
Aynı girdi, sabit 30. A = pre232 (her V2.32 knob'u V2.31 değerinde), B = ncam (V2.32 beden + V2.31 kamera), C = ocam (V2.31 beden + yeni
kamera), D = o (V2.32 üretim). Sütunlar: en kötü kayma (cm) / yörünge max (°). Beden yolu farkı (d_pos) ve kontrol yaw farkı her hücrede
0.0 cm / 0.00° — kamera bedene ve girdiye dokunmuyor, beden değişiklikleri kamerayı değiştirmiyor.

| senaryo | A | B | C | D |
|---|---|---|---|---|
| zincir: yürü → depar → sert sağ → fren → yeni yönde itiş | 11.5 / 0.7 | 11.5 / 0.7 | 11.5 / 13.7 | 11.5 / 13.7 |
| depar sert sağ | 11.5 / 0.7 | 11.5 / 0.7 | 11.5 / 13.7 | 11.5 / 13.7 |
| fren ortasında ikinci istek | 16.5 / 0.7 | 11.5 / 0.7 | 16.5 / 12.9 | **6.5** / 12.9 |
| duvar yanında dönüş | 13.1 / 0.7 | 13.1 / 0.7 | 13.1 / 8.2 | 13.1 / 8.2 |
| yürürken fare bakışı | 6.9 / 0.1 | 6.8 / 0.1 | 6.9 / 0.1 | 6.8 / 0.1 |
| analog çapraz tempolu | 22.1 / 0.5 | 22.1 / 0.5 | 22.1 / 2.2 | 22.1 / 2.2 |

Jerk95: A 0.56–3.29 = D 0.57–3.29 (en çok +0.12, duvar yanında 1.18 → 1.30); min mesafe aynı (78–195 cm).

## 11. Arazi — AÇIK
- **terrain232, ter_drop_walk +18 cm basamak:**
  - arka ayak tepe yüksekliği varış zemininin 11 cm üstünde;
  - 0.13 s asılı kalıyor;
  - erken kalkış 2.6 cm.
- **−30 cm iniş:** öncü ayak 34 cm tepe yüksekliği, pelvis gecikmesi 28.7 cm.
- **T6** (salınım hedefi pelvis gecikmesi kadar indirilir): erken kalkış 2.6 → 0 oldu ama tepe 11 → 13, tempolu iniş 10.8 → 16.3 → reddedildi.
  - Kod kurulu, SwingPelvisComp = 0.
- T7 basamaklarda nötr (ter_drop_walk / ter_step2: 6.5 = 6.5).

## 12. Otomasyon

**IsUnique:**
- `SLevelViewport::EndPlayInEditorSession` içinde `check(GameViewport.IsUnique())`: PIE sonunda FSceneViewport paylaşımlı referansının başka bir tutucusu var.
- 2038 tarihî koşuda 4 çökme. Bu oturumda 0.
- Soak: 20 çıplak PIE döngüsü + 100 harness-sonu döngüsü, 0 çökme.
- Motor PDB'leri yok; çağrı yığını sembolsüz.
- Etkin eklentilerin kaynağında tek ortak tutucu MediaCapture; çökmeler yakalama dışı koşularda oldu.
- Sonuç: motor tarafı mı otomasyon tarafı mı ayırt edilemedi. Açık.

**Bellek / log:**
- (1) Yörünge LastHitBy seli: oturum başına ~100 bin hata satırı. Onarıldı.
- (2) Test telemetrisi `SHM|` (bileşen PrintString, yalnız TelemetryEnabled, normal oyunda maliyet yok): kare başına ~1.6 KB, P2 oturumunda 77 MB log metni.
  - V2.31 ile aynı oran; shm_evidence log'dan okuyor.
  - Yan dosyaya taşıma bu tur yapılmadı. Açık otomasyon maddesi; briefin "yan dosya" kuralına göre bir sonraki tura önerildi.
- 38 GB koruması 02:39, 03:29, 04:19, 06:32 ve 08:24'te yeniden başlattı (nedenleri chain.out'ta).

**Kesinti (kendi hatam):**
- `run232_p1.sh` iki kez başlatılmıştı. İkinci örnek, çalışan PIE oturumunun içine DB yeniden kurma işi kuyrukladı.
- Oyun iş parçacığı kare 72'de dondu, runner 06:50'den itibaren askıda kaldı.
- Editör kapatıldı (neden loglandı), P1 iptal edildi, P2 temiz yeniden açılışla koşuldu. X DB'leri birinci örnek tarafından doğru yazılmıştı.

**Süre:** sabit-30 koşu 35–45 s. P2'de 108 koşu ~69 dk; FPS zinciri 4 mod × 20 koşu ~74 dk.

## 13. Kabul ve üretime alma
- Sıra: teknik onarım → aynı oturumda iç içe A/B (P2, 2 tekrar) → FPS 60/120/20/gerçek → sahip izolasyonu (ISO) → üretime alma → temiz
  yeniden açılış doğrulaması → son kanıt + matris → normal hızlı kayıtlar.
- Kabul kuralları kontrolü: girdi kontrolü (d_ctl / d_vin 0 her yerde), yanlış aile (blip 82 → 57, B_F→B_F sıçramaları kalktı), büyük
  basılı-ayak kayması (median 20.3 → 16.1; iki görünür artış sınıflayıcı bölümlemesi / dal ayrışması olarak açıklandı — bkz. 2D), poz
  sıçraması (pop sayıları aynı sınıf), kamera görünürlüğü (min mesafe ve kadraj aralığı aynı), normal yürüyüş (yörünge ≤ 0.5°) ve inceleme
  (ins_ws 10.4 = 10.4, yörünge 0) — kötüleşme ölçülmedi.
- Yüklü aile FPS'ler arasında ve iki giriş evresinde (P21/P30 geri düşüş) doğrulandı; koşulsuz değil: kapıdan geçmeyen giriş üretim klibine gider.
- Kamera: oyuncu bakışı önceliği var; kontrolü bozan davranış ölçülmedi → otomatik katkı açık. Geri alma: promote232 {'rollback': True}
  veya yalnız DA CamOrbitEnabled = false (önceki kararlı kamera birebir döner: ncam = pre232 kamera değerleri).
- Üretimde açık olan değişiklikler — hareket: bfexit, loadedbf, floorguard; kamera: camera; arazi: yok (T6 kapalı, T7 basamaklarda nötr).

**Son üretim kanıtı (fin2, temiz yeniden açılış sonrası, sabit 30, 33 senaryo, hepsi FINISHED):** P2'deki aday sayılarıyla
örtüşüyor (c30_calm 17.9, e29_chain 6.5, e29_load 6.5, 4750 11.1, swl12 11.1, wdiag 12.5, brk2 6.5, ins_ws 10.6, ter 6.5). Tek ayrışan:
jstart 55.5 (P2'de aday 43.7/43.3, üretim 48.6) — oturumlar arası dal ayrışması sınıfında (V2.32 oturum kuralı: karar aynı oturum iç içe
koşulara dayanır); açık izleme maddesi. data/tables_fin2.txt.

## 14. Teslim tablosu
| başlık | durum | not |
|---|---|---|
| 2A eforlu dönüş 60/120 / 4750 / yüklü aile | **ÜRETİMDE** | e29_chain 30: 25.4 → 6.5; 60: 26.1 → 19.8; 120: 33.5 → 17.3; 4750 20 FPS 21.9 → 7.0 |
| 2B düşük hızlı dönüş 60 FPS | AÇIK | swl12 60 FPS 20.7 değişmedi (diğer modlar iyileşti) |
| 2C duruştan geri kalkış | AÇIK (sb, pinstart, IS kopyaları reddedildi) | 38 cm; AAMS başlangıç duruşu farkı; duruş süresine bağlı rota önerisi |
| 2D duruş kapanış adımı | **ÜRETİMDE** (T7) | c30_calm 33.3 → 17.9, wdiag 21.6 → 12.5 |
| 2E yan / arka çapraz | AÇIK | c29_combo 48.8 → 57.6 sayısal (sınıflayıcı; fiziksel kusur aynı); a29_angb 33.5 → 23.8 |
| 2F bırak – yeniden bas | AÇIK | dal ayrışmalı; FPS'e göre ± |
| 3 efor | **ÜRETİMDE** (yüklü iki yön) | toparlanma 31.6 → 26.4, hâlâ > 20 |
| 4 üst gövde | BULGU, aday yok | depar duruşu klipten (29° öne) |
| 5–9 sinematik kamera | **ÜRETİMDE** | 13.7° depar dönüşü, 0 bakış/dar alan, beden bağımsız, FPS bağımsız |
| 11 arazi | AÇIK (T6 reddedildi, kod kapalı) | arka ayak 11 cm / 0.13 s asılı |
| 12 IsUnique | AÇIK, bu turda 0 / ~820 PIE | sembolsüz; MediaCapture şüphesi kanıtsız |
| 12 log telemetrisi | AÇIK | SHM| satırı yan dosyaya taşınmalı (V2.33) |
| Tick sırası | REDDEDİLDİ | IntentTickPrePhysics false |
| Checkpoint boşluğu (A_CT_Ref_Walk_Stop_F_L/R) | BİLDİRİLDİ | ≤ 1.2 cm, geri alınamaz |
| Görsel kabul | BEKLİYOR (kullanıcı) | vid/ kayıtları |
