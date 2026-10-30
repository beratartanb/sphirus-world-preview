# SPHIRUS V2.38: Fizik bilgili yön değişimi ve denge toparlanması (V2.37 fcc85e2 üzerine)

Tarih: 2026-10-30. Tabanlar:
- Kod/varlık: V2.37 üretim durumu.
- Kanıt: `tables_fin4.md`. Hepsi aynı derlemeden: temiz açılış + `VERIFY238 ALL_OK`.

Etiketler:
- **Teknik:** PASS / FAIL / PARTIAL / NOT_TESTED.
- **Görsel ve oyun hissi:** ayrı yazıldı. Bunlar senin kabulündür; burada yalnız gözlemim var.

## Özet (tek paragraf)

Tempolu koşuda sert 90° dönüş artık fizik planlı yeni bir aileyle yapılıyor (48 klip; sağ ve sol için döngü evresi başına birer klip). Akış şöyle: isteğin geldiği anda hangi ayağın yere ineceğine ve ne kadar süre kaldığına bakılır. Ardından ya **normal destek** (plant → transfer → itiş) ya da **ek fren adımlı** plan seçilir. Kapsül klibin yolunu ve yönünü kare kare izler. Gövde dönüşe önden girer, hız kaybı görünür.

Ölçülen sonuçlar:
- Ayak kayması 0–10 cm (V2.37'de 11–13 cm).
- Tepe ivme 0.53–0.67 g (V2.37'de 0.65 g ve fren teması yoktu).
- Yönün %80'i 0.77–0.83 s'de dönüyor (V2.37'de 0.5 s).

Açık kalanlar: depar 90°, art arda kesmeden sonra gelen ters dönüş patlaması, 45 / 135 / 180 için yeni içerik, Seviye 3 ve baş yönünün sahibi olan vendor aim offset. NVIDIA modelleri araştırıldı ama indirilmedi. Gerekçe ve tablo §9'da.

---

## İlk sayfa: soruların cevapları (1–14)

**1. Hangi verilerle değerlendirildi?**
Her koşu aynı kareleri kaydediyor:
- kapsül konumu ve hızı;
- giriş vektörü ve istenen hız;
- klip, klip zamanı ve veritabanı;
- ABP ve bileşen değişkenleri;
- görünen MetaHuman kemikleri ve eksenleri;
- kamera.

`balance238.py` bunlardan şunları üretir:
- kütle merkezi (Dempster/Winter segment oranları, görünen mesh üzerinden);
- XCoM / yakalama noktası;
- destek ayağı (top kemiği yere 3 cm'den yakın ve 40 cm/s'den yavaş);
- temas başına hız değişimi;
- pelvis / göğüs / baş yönü;
- yönün %80'ine ulaşma süresi;
- tepe ivme (μ_eff).

Planın kendisi `gen238_cut_write.json` dosyasında: temas, rol, zaman, yer, hız ve yön. Bu bir **açıklanabilir yaklaşımdır**, kuvvet ölçümü değildir. Model ve sınırları `skills/sphirus-balance-recovery`'de.

**2. Seçimi gerçekten değiştiriyor mu?**
Evet.
- Tempolu yan bölüm artık atlanmıyor (`SHM210_JogCutMode` 1) ve `PSD_SHM238_JogCut`'a yönleniyor.
- MM, istek karesinde isteğin evresine uyan bölmeye giriyor (klip zamanı 0.03–0.13 s) ve klibi sonuna kadar oynatıyor.
- Evre, gelecek ayağı ve kalan süreyi belirliyor. Bu da planı belirliyor:
  - c90r: P21, zayıf plant;
  - c90rb: P05, normal;
  - c90l: P20, iç ayak, önce fren;
  - c90lb: P13, normal.
- Temiz açılışta soğuk ilk kullanımda veritabanı her karede hazırdı (0 boş kare). Doğru klip seçildi: R_P21 0.0 cm, L_P20 6.8 cm.
- **Teknik: PASS.**

**3. 90° yük nasıl taşınıyor?**
Plan ve oyun aynı sırayı izliyor:
1. Ayak ivmenin tersine, öne ve dışa konur (fren + dönüş itişi).
2. Pelvis yükü alır. Pelvis inişi ≤ 1.8 cm sönümlemeyle sınırlı; 48 klipte en fazla 6.4 cm.
3. Göğüs pelvisten önde döner.
4. Yeni destek ayağı yeni hatta iner.
5. Yeniden itiş 300 cm/s² ile yapılır.
6. Yerleşme (settle) gelir.

Hız 300'den 115–176 cm/s'ye iner, sonra geri çıkar. Tepe ivme 0.53–0.67 g. Kapsül her karede klibin komut yönünde.

Kayma, aynı oturumda o / V2.37:

| Senaryo | V2.38 (o) | V2.37 (pre238) |
|---|---|---|
| c90r | 9.6 | 12.5 |
| c90rb | 0 | 11.2 |
| c90l | 0 | 12.8 |
| c90lb | 6.0 | 6.6 |

Üst gövde patlaması ≤ 26–31 m/s². Bu, ısınmış döngü tabanıyla aynı seviye.

- **Teknik: PASS.**
- **Görsel (gözlemim): PARTIAL.** Fren okunuyor: dizler bükülüyor, duruş genişliyor, göğüs önden dönüyor, kollar sönüyor. Zayıf-plant girişinde (P21) 2–3 karelik dizler-bükük fren pozu hafif çömelmiş görünebilir. Baş dönüşte önde, ama dönüşten sonra kamera dönene kadar yaklaşık 40°'de kalıyor (bkz. 6).

**4. Hangi içerik üretildi?**
- `SHM238_Cut_{R|L}_P00..P23` (48 klip) + `PSD_SHM238_JogCut`, kaynağı `gen238_cut.py`.
- Başlangıç noktası: V2.37 döngüsünün istek anındaki pozu ve döngünün kendi salınım/iniş biçimleri.
- Bunların üstüne planlı temaslar, iki kemikli bacak çözümü, erişime göre pelvis ve bütün beden katmanları eklendi. Katmanlar: baş önden, göğüs önden, pelvis takip, a/g'den eğilme, fren payına göre kol sönümü.
- Eğriler:
  - `SHM226_V/W` (hız sözleşmesi);
  - `SHM238_Turn/W` (yeni yön sözleşmesi);
  - `SHM237_FPPelvisOff`.
- Ham lisanslı animasyon ve yedek yayımlanmadı. Çubuk JSON'u da yayımlanmadı; yalnız render edilmiş sayfalar var.

**5. Normal destek ile ek adım arasındaki fark?**
48 bölmenin dağılımı:
- 10'unda yeni hatta 4 temasla varılıyor;
- 38'inde 5 temasla.

Sayı tabloda yazılı değil, plan simülasyonundan çıkıyor.

Oyunda iki durum, aynı hız ve aynı 90°:

| | Normal destek (dış ayak sırada, zaman var) | Ek adım (iç ayak sırada / dış ayak çok erken) |
|---|---|---|
| Örnek | c90rb → P05: plant 0.32 s → transfer 0.63 → itiş 0.94 → itiş 1.32 | c90l → P20: **fren** 0.12 → plant 0.45 → transfer 0.76 → itiş 1.07 → itiş 1.44 |
| En düşük hız | 162–169 cm/s | 115–116 cm/s (sol), 176 (sağ, zayıf plant) |
| Görünüş | kısa plant, hemen yeni hat | ek fren adımı, daha derin diz bükümü, daha uzun yeniden itiş |

Sayfalar: `sheets/fin_c90rb_v238_side.png` ile `sheets/fin_c90r_v238_side.png`. Videolar: `vid/jog90_right_v238_favourable_side` ile `vid/jog90_right_v238_side`.

Not: oyun içi temas sayacı aynı ayağı 0.1–0.2 s içinde iki kez sayıyor (topuk/top yeniden algılama). Bu yüzden destek farkını planın rolleri ve ölçülen hız/yön ile veriyorum.

- **Teknik: PASS.**
- **Görsel:** fark normal hızda görünüyor. Kabul senin.

**6. Beden parçaları ne yapıyor?**
Yön, eski yöne göre, +1.0 s'de (pelvis / göğüs / baş):

| Senaryo | V2.38 | V2.37 |
|---|---|---|
| c90r | 80 / 75 / 38° | 81 / 64 / 12° |
| c90lb | 83 / 85 / 25° | 85 / 54 / 2° |

- Göğüs pelvisi önden götürüyor.
- Baş dönüş sırasında öne geçiyor (0.2–0.6 s'de 41–47°).
- Baş dünyaya kilitli değil.
- Dönüşten sonra baş yaklaşık 40°'de kalıyor. Sebep: vendor `ABP_AAMS_ActionLayer_MM` LookAtAimOffset başı kontrol (kamera) yönüne tutuyor. Hareket bakışı (gaze) bunu yalnız kısmen düzeltiyor (10–20° → yaklaşık 40°, yumuşatılmış).

- Kollar: fren payına göre salınım sönüyor.
- **Teknik: PARTIAL** (baş sahibi vendor katmanı, değiştirilmedi).

**7. Donma / bekleme var mı?**
Yok.
- Klip saati gerçek zamanda akıyor (oynatma hızı değişmedi).
- Giriş geciktirilmiyor.
- Pozu dondurmak yok.
- Hız eğrisi temaslar boyunca sürekli.

Ek zorluk görünür biçimde geliyor: ek temas, plant'ta daha düşük hız, daha uzun yeniden itiş.

- **Teknik: PASS.**

**8. Kontrol gecikmesi?**
- Gövde istek karesinde tepki veriyor: aktör yönü 0.07 s'de 3°, 0.2 s'de 12°. Baş ve göğüs ilk karelerde başlıyor.
- Kapsülün yeni yöne dönmesi bir temas gerektiriyor. Yönün %80'i 0.77–0.83 s (V2.37'de 0.5 s).
- Bu bilinçli bir sonuç: V2.37 ilk 0.4 s'de 72° dönüyordu, fren teması yoktu ve 0.9 g'de kayan bir döngü eğrisi kullanıyordu.

- **Oyun hissi:** "daha ağır ama daha yerli" olması bekleniyor. Kabul senin; NOT_TESTED (oyuncu girişiyle elle oynanmadı, yalnız enjekte girişle).

**9. NVIDIA araştırması ne buldu?**
Ayrıntı ve kaynaklar `research/research_v238.md`'de (2026-10-30'da okundu).

| Teknoloji | Karar | Neden |
|---|---|---|
| CMC fren/dönüş ayarları, PoseSearch bias + interrupt, inertialization profili, küçük açılı orientation/stride warping | **Şimdi kullanılabilir** | Mevcut sahipler; bu sürümde bias ve rota kullanıldı |
| MotionBricks (SOMA ağırlıkları) | **Uyarlama gerekir** | Ticari ağırlık ve Windows var. Ama SOMA iskeleti + SOMA→MetaHuman retarget + dışa aktarıcı bizim işimiz. Kinematik: denge garantisi yok |
| Kimodo (SOMA-SEED) | **Uyarlama gerekir** | Aynı retarget ihtiyacı. SMPL-X ağırlıkları ticari değil, asla kullanılmaz |
| Control Rig FBIK, Motion Warping | **Uyarlama gerekir** | FootPlacement / MM sahipliğiyle çakışır |
| ARDY | **Deneysel** | Linux'ta test edilmiş; kapılı Llama-3-8B kodlayıcı (~14 GB VRAM); kinematik |
| Physics Control, Slope Warping, Dead Blending | **Deneysel** | Belgeleri "geliştiriliyor / üretim için değil" |
| ProtoMotions, Physical Animation | **Gereksiz maliyet** | IsaacLab / Linux, çoklu A100 eğitimi, politika UE'de çalışmaz; yalnız fikirleri işe yarar |

Kinematik modeller fizik garantisi değildir.

**10. Neden hiçbir model indirilmedi / denenmedi?**
- **Gerçek ihtiyaç:** 90° için gereken tek şey doğru temas sırası ve kapsülle uyumlu kök. Bunu kendi MetaHuman iskeletimizde, lisans ve retarget riski olmadan üreten bir üreteç yazıldı ve oyunda çalışıyor.
- **Donanım:** RTX 4060 Laptop, 8 GB. ARDY kodlayıcısı ~14 GB istiyor; Kimodo için ~17 GB söyleniyor (doğrulanmadı). MotionBricks yalnız 4090'da ölçülmüş ve TensorRT 10.8 istiyor.
- **MetaHuman uyumu:** üçü de SOMA kullanıyor. Resmî bir SOMA→MetaHuman yolu yok.
- **Kural:** bir yapay zekâ klibi ancak bizim iskeletimizde temas/kök/kapsül kontrollerinden geçerse karşılaştırmaya girer. Prosedürel klibi aynı ölçütlerde geçerse üretime alınır (`skills/sphirus-motion-synthesis`).
- Bu sürümde model indirme veya eğitim yok.

**11. V2.37'den kalan açıklar?**
Aynı oturumda o / pre238, ilk ayrılan karenin klip / kapsül farkıyla kontrol edildi:

| Senaryo | V2.38 | V2.37 | Durum |
|---|---|---|---|
| j36_sside | 15.0 | 15.8 | Değişmedi. V2.38 bu rotaya dokunmuyor: klip ve kapsül aynı, fark yalnız ayak IK'sında. Vendor `A_LS_Jog_Right_Start` sahibi açık kalıyor |
| jstart | 68.4 | 83.0 | Sahip yine vendor `af_Loco_Jog_Start_TurnR045`. Fark V2.38 rotasından değil, döngüye giriş evresinden; **açık** |
| j36_rsx | – | – | Koşulmadı (bu sürümün kapsamı 90°). **NOT_TESTED** |
| j30_rel_3450 | 10.3 | 7.1 | Ayrılma 3.37 s'de, döngüye giriş evresinde (her iki yöne de dönen yazı-tura). V2.38 sinyali yok. **Değişmedi / gürültü** |
| e29_chain | 6.3 | 11.1 | Klip ve kapsül aynı. **Değişmedi** |
| c29_combo | 15.4 | 22.9 | Boşta evre farkı. **Değişmedi** |

Üst gövde tepkisi: kesmede göğüs önden ve kol sönümü var (6). Genel üst gövde katmanı yeni değil.

**12. Kamera ve önceki kazanımlar?**
- Kamera kontrolü değişmedi.
- Bakış, yalnız kamera arkaya dönmeyi beklerken (`CamRecState` 1–3) ve 150 cm/s üstünde, mevcut LookAt zinciriyle harekete bakıyor. Ağırlık yumuşatılıyor; alfa basamağı 125 m/s² patlama yapıyordu, yumuşatmayla gitti.
- İnceleme ve el ile bakış önceliği korunuyor: `InspectLookAlpha` > 0 iken kapalı.
- Önce sabit yan/çapraz gözlemci kamerasıyla doğrulandı, sonra oyun kamerasıyla (`vid/*_game`).

Korunan kazanımlar (aynı oturum):

| Senaryo | V2.38 | V2.37 | Kaynak |
|---|---|---|---|
| j36_stop | 0 | 9.0 | V2.37 durma ailesi |
| j36_stopr | 0 | 5.5 | V2.37 durma ailesi |
| j35_rev | 11.7 | 9.7 | V2.35/36 ters dönüş (evre farkı) |
| j34_chain1 | 7.5 | 7.9 | V2.35/36 ters dönüş |
| w38_c90r (yürüme 90) | 0 | 0 | |
| wdiag | 0 | 12.3 | |
| s38 depar 90'lar | 11.1 / 6.4 | 11.1 / 6.4 | aynı klipler |

- S = kontrollü geri yürüme, değişmedi: j38_c135r aynı V2.36 ters dönüş klibi, kayma aynı.
- Çift pelvis düzeltmesi geri gelmedi: tek FootPlacement pelvis kaynağı; klipte `SHM237_FPPelvisOff`.

**13. Açık / deneysel / reddedilen**
- **60 FPS sol kesme erken bırakılıyor:** sınıf 0 yeniden kilitlenmesi hold'u deliyor. **Açık.**
- **Depar 90° (reddedildi, üretilmedi):** aynı plan 494 cm/s'de 8 temas ve ~2 s istiyor, pelvis 10–15 cm iniyor. Önce-fren tasarımı gerekiyor.
- **Art arda kesme (j38_cc90):** ikinci basış ters dönüş sayılıp V2.16 RevTurn klibine gidiyor. Kayma 6.1 cm (V2.37'de 15.9) ama patlama 71 m/s². **Açık.**
- **mtf_jog (hızlı titrek kesmeler):** 48.9 cm (V2.37'de 24.1). Kesme klipleri devreye giriyor, sonra RevTurn kayıyor. **Açık, gerileme.** Kaynak art arda kesmeyle aynı.
- **Baş sahibi** vendor aim offset; bakış yalnız kısmi düzeltme.
- **İtilme dedektörü:** klibe bağlı hız geri kazanımını dış itilme sanıyor. ABP'de korundu (`GuardS` 1.6 s). Bileşen düzeyi düzeltme açık.
- **45°:** döngü eğrisinde kaldı. Ölçüm: 0.49 g, hız kaybı yok; ek içerik gerekmedi.
- **135° / 180°:** mevcut V2.36 ters dönüş ailesi. Ayrı fizik planlı 135° içeriği yok. **Açık.**
- **Seviye 3 (ölçülü denge kaybı):** karar kuralı beceride tanımlı, içerik yok. **NOT_TESTED.**
- **ABP durumu:** `BS_UP_TO_DATE_WITH_WARNINGS`. Uyarılar V2.38 yön yamasından beri var; hata yok, sebebi incelenmedi.

**14. Sayılar ve süre**
`data/chain.out`'tan:
- **428 ölçüm koşusu** + 19 ısınma koşusu.
- **15 editör yeniden başlatma** + 1 otomatik yeniden deneme. Dahil olanlar: 4 temiz açılış (fin, fin3, w4, fin4) ve FPS kipleri (60 / 120 / 20 / gerçek zaman, iki kez).
- Süre: 01:29–07:40 (~6.2 saat).
- Final kanıt seti (fin4, tek derleme): 2 soğuk + 64 koşu (30 FPS) + 10 çekim + 3 FPS kipi × 14 koşu.
- V2.37'de 432 koşu / 17 yeniden başlatma vardı.
- Bu sürümde tekrar sayısı amaç değildi. Ama yürüme korumasının iki kez daraltılması iki ek final turu gerektirdi; bu yaklaşık 130 koşu ve 6 yeniden başlatma demek. Ders `skills/sphirus-safe-unreal-iteration`'a yazıldı: son geniş regresyondan sonra gelen her yama geniş seti yeniden ister.

---

## Karar katmanı (uygulanan)

Ayrı bir fizik motoru yok. Karar, mevcut veriyle **istek anında bir kez** veriliyor. Akış:

| Durum | Ne zaman | Ne yapar |
|---|---|---|
| **Stable** (döngü) | — | — |
| **Kontrollü fren / Destek transferi** | İstek geldiğinde | Evre bölmesi, gelecek ayağı ve kalan süreyi belirler. MM o bölmeye girer |
| **Ek adım (Seviye 2)** | İç ayak sıradaysa, ya da dış ayak çok erken iniyorsa | Fren veya zayıf plant ile başlar |
| **Normal destek (Seviye 1)** | Dış ayak sırada ve zaman varsa | Plant ile başlar |
| **Redirect / RePush** | Planın son temasları | Yeniden hızlanma |
| **Settle** | `SHM238_W` 0'a indiğinde | Döngüye dönüş |

Histerezis ve titreme önleme:
- Bölüm ve veritabanı, `SHM238_W` açık olduğu sürece tutulur (`install238_hold`).
- Toparlanma ailesi plan boyunca + 1.6 s susturulur.
- Karar her karede değil, istek anında bir kez verilir. Bölme geçişi bias −25 ile tutulur.

Seviye 3 tanımlı, içerik yok (13).

## Hatalar ve düzeltmeler (bu sürüm)

**Yürüme koruması (3 tur)**
- **İlk koruma:** başlangıç hızı < 220 olan *her* bölümü atlıyordu.
- **İlk final turu:** bunun geri dönüşü de (206 cm/s), deparın içindeki yeniden kilitlenmeyi de bozduğunu gösterdi:
  - j35_rev 6 → 34 cm;
  - e29 6 → 44 cm.
- **walk2:** sınıf ≤ 1.5 ve "henüz aktif değil" koşulları eklendi.
- **fin3:** bölümler arasında da `RdLatSkip`'in True kaldığını gösterdi (eski `RedirectSpeed0`). Bu döngü girişlerini ve kapsül yolunu değiştiriyordu (mt_jog kapsülü 9.5 cm sapıyordu).
- **walk3:** yalnız bileşen bölümü aktifken çalışıyor. Bölüm dışında davranış tam olarak V2.37.
- **fin4:** bütün o / pre238 ayrılmaları ya V2.38 kesme bölümünde başlıyor ya da hiçbir V2.38 sinyali olmadan oluşuyor:
  - döngüye giriş evresi (iki yöne de);
  - boşta evre seçimi;
  - aynı klipte ayak IK farkı.

**Diğer düzeltmeler**
- **Yön sıçraması:** `W` tek başına düşerken interpolasyon bölüyordu ve yön 90 → 145'e sıçradı. `Turn` ve `W` artık birlikte sıfıra iniyor.
- **Baş patlaması:** katman basamaklarından 58 m/s² patlama vardı. ±4 kare yumuşatmayla 26'ya indi.
- **Bakış alfası patlaması:** 125–141 m/s². FInterpTo ile çözüldü.

## FPS kipleri

Değerler aşağıdaki tabloda (o / pre238; kayma cm, patlama m/s²).

| scenario | 30 | 60 | 120 | 20 | real |
|---|---|---|---|---|---|
| j38_c90r | 9.6 / 12.5 (26 / 0) | 12.1 / 11.6 (52 / 33) | 8.3 / 12.8 (85 / 69) | - | 8.8 / 11.5 (31 / 0) |
| j38_c90l | 0.0 / 12.8 (0 / 0) | 37.6 / 27.2 (45 / 45) | 9.0 / 24.1 (83 / 74) | - | 8.2 / 8.8 (0 / 37) |
| j35_rev | 11.7 / 9.7 (32 / 37) | 12.3 / 15.7 (75 / 62) | 19.9 / 21.3 (146 / 146) | - | 8.0 / 8.5 (30 / 35) |
| j30_rel_3450 | 10.3 / 7.1 (33 / 33) | 13.8 / 13.4 (67 / 78) | 8.7 / 8.7 (133 / 132) | - | 13.3 / 6.3 (30 / 53) |
| e29_chain | 6.3 / 11.1 (76 / 76) | 19.8 / 20.6 (155 / 155) | 17.3 / 17.6 (146 / 146) | - | 6.3 / 25.9 (86 / 69) |
| w38_c90r | 0.0 / 0.0 (0 / 0) | 6.2 / 0.0 (30 / 30) | 11.4 / 10.3 (81 / 82) | - | 8.2 / 0.0 (0 / 0) |
| jlean | 12.0 / 25.9 (36 / 36) | 14.7 / 27.3 (73 / 70) | 40.1 / 27.7 (298 / 197) | - | 9.7 / 46.7 (35 / 61) |

20 FPS bu turda koşulmadı. Bir önceki derlemede (fin, yürüme koruması walk1) koşulmuştu; `tables_fin.md` §3.

| Durum | Bulgu | Etiket |
|---|---|---|
| **60 FPS sol kesme** | Klip 0.7 s'de erken bırakılıyor: hold açıkken bölüm sınıf 0 ile yeniden kilitleniyor ve veritabanı JogSteady'ye dönüyor. Sonraki döngü klipleri 27–37 cm kayıyor. V2.37 de aynı döngüde 27 cm kayıyor | **açık** |
| 60 FPS sağ kesme | 12.1 (V2.37'de 11.6). Kayma kesme klibinin içinde | — |
| **120 FPS** | Sağ/sol 8.3 / 9.0 (V2.37'de 12.8 / 24.1). Patlama 83–85 m/s² (V2.37'de 69–74). 120 FPS'te bütün senaryolarda patlamalar yüksek | — |
| **Gerçek zaman** | 8.8 / 8.2 (V2.37'de 11.5 / 8.8) | — |
| w38 (yürüme) 60 / 120 | Aynı klip ve kapsül, fark yalnız ayak IK'sında | — |
| w38 gerçek zaman | Koşular baştan farklı (gerçek zaman deterministik değil) | — |
| jlean 120 FPS | 40.1 (V2.37'de 27.7), patlama 298 | **açık** |

**Teknik:**
- 30 / 120 / gerçek zaman: PASS.
- 60 FPS: PARTIAL (sol kesme erken bırakılıyor).

## Dosyalar
- `CHANGES_V238.md`: üretim tablosu, yamalar, geri dönüş.
- `data/tables_fin4.md`: final tabloları (tek derleme).
- `research/`: NVIDIA ve UE araştırması.
- `skills/sphirus-balance-recovery`, `skills/sphirus-motion-synthesis` (yeni). Güncellenenler: `sphirus-safe-unreal-iteration`, `sphirus-game-dev-director`.
- `code/`: üreteç, kurulumlar, araçlar.
- `manifests/`: yalnız JSON.
- `sheets/`, `vid/`: normal hızda, kesilmemiş 30 FPS çekimler. Yavaş çekim yok.
  - `vid/jog90_right_v237_*` ile `vid/jog90_right_v238_*`: önce / sonra.
  - `*_favourable_*`: normal destek.

## Kabul
- **Teknik:**
  - 90° sağ/sol: **PASS** 30 / 120 FPS ve gerçek zamanda (kayma, sürekli hız, kapsül = plan, soğuk ilk kullanım, verify). 60 FPS'te **PARTIAL**: sol kesme erken bırakılıyor.
  - Art arda kesme ve titrek kesme: **FAIL** (açık, gerileme var).
  - Depar / 135 / 180 / Seviye 3: **NOT_TESTED** veya reddedildi.
- **Görsel ve oyun hissi:** senin kabulün. Benim gözlemim PARTIAL:
  - fren okunuyor;
  - zayıf-plant girişi hafif çömelik;
  - dönüş sonrası baş kameraya yakın kalıyor.
