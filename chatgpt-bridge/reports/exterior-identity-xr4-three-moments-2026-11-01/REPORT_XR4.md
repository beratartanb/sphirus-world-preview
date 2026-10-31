# XR4: üç atmosferik an (sığınak, geçiş, sessiz tekinsizlik), tek bağlı bölge

İzole, bellek içi deneme; hiçbir paket kaydedilmedi. 2026-11-01. UE 5.8.1, `L_GR_SphirusHouse`, gerçek oyuncu kamerası, sabit adım 30 FPS.
Bölge: A rotası dilimi (ev sekisi → iskele → kaya sekisi → dere ağzı → karşı kıyı açıklığı). Temel: XR2 x8 dolaşımı.

## 0. Sonuç önce

| An | Kompozisyon niyeti | Sonuç | Tier |
|---|---|---|---|
| **Geçiş** (P2 kaya sekisi) | Tek sürekli ana kaya çıkıntısı; üstünde koyu ladin; dipte talus, yosun, eğrelti; zemin sessiz; ışık yalnız raf boyunca | **Değişti ve ilk bakışta okunuyor.** "Konmuş kaya" eleştirisi kalktı: 8 blok aynı doğrultuda, %45 gömülü, arkasında toprak seti. Karakterin 90° solu ve geri bakışı da tutuyor. | **3** |
| **Sessiz tekinsizlik** (P3 açıklık) | Kenarı yükseltilmiş sığ teras, meşe gelişte görüş hattında, 9 taşlık düzenli yay, dışa yatan halka ağaçlar, zemin boş | **Teras ve meşe çalışıyor; taş yayı okunuyor.** Ama i4'te eklediğim yosun yamaları (SM_GroundMossPatch) terasın eğiminde havada uçan plakalara dönüştü: FAIL. i5'te kaldırıldı; terasın zemini artık yalın toprak ve kök, taş yayı tek odak. | i4 **1 (kusur)**, i5 **2–3** |
| **Sığınak** (P0/P1 ev → iskele) | Çerçeveleyen dev gövdeler, sandal ilk hedef, su parçası, karşıda kapalı orman duvarı | Ev önünde iki büyük çam gövdesi çerçeve veriyor; verandadan sandal okunuyor. Ama alan hâlâ XR3 düzeyinde: zemin ön planı değişmedi. | **2** |
| Işık A (alçak güney güneşi, nemli yönlü sis) | Raf ve dere ağzı arkadan aydınlanır, ev karşı kıyıdan önden | Karşı kıyıdan eve bakış (P3 fwd) ve dere ağzı en iyi karelerini verdi; kaya sekisinde kayalar beyaza yaklaştı; verandadan bakışta su parladı | Tercih: **A**, güneş biraz daha düşük yoğunluk + kaya parlaklığı |
| Işık B (kapalı, düşük kontrast) | Değer hiyerarşisi yalnız kütlelerden | Kütleler okunuyor; ama sahne gri ve tatsız, dere ağzındaki hüzme kayboluyor | reddedildi |
| Kesintisiz yürüyüş | i5 + üretim ışığı ve i5 + ışık A, 101 m, gerçek hız | İki yürüyüş de takılmadan bitti; ilk i5 çekimi (bölüm 5) kirli kanıt olarak ayrıldı | |

Başarı sorusunun cevabı: **kaya sekisi karesi artık Sphirus'a ait okunuyor; açıklık yaklaşıyor; ev önü hâlâ paket sahnesi.** Bütün bölge için "güçlü ve tutarlı" diyemem; bir anı diyebilirim.

## 1. Teşhis: neden kaliteli asset'lerle hâlâ deneme sahnesi

XR3'ün kareleri, renk uyumu dışında altı nedenle demo gibi okunuyordu. Her neden için XR4'ün yaptığı:

| # | Neden (görünen) | Kanıt karesi | XR4 kararı |
|---|---|---|---|
| 1 | **Değer hiyerarşisi yok.** Kameraya yakın baskın koyu kütle yok, tek bir ışık odağı yok; her şey orta değerde | XR3 P2 fwd: kaya, orman ve zemin aynı parlaklıkta | Raf üstüne koyu ladin korusu (11 ağaç); raf dibi yalın iğne tabanı; her anda tek ışık salımı (iskelede su, rafta raf boyu, açıklıkta taş yayı) |
| 2 | **Ölçek hiyerarşisi yok.** Bütün gövdeler 30–50 cm, bütün bitkiler aynı boy | XR3 P0/P1 | 4 kahraman çam (PineTree03/04 ×1.3–1.4, ~1 m gövde, 36 m boy) çerçeve kenarlarına; talus üç boyda |
| 3 | **Kayalar prop.** Tek tek kayalar, aralarında boşluk, düz yamaçta | XR3 i3 P2 | Tek sürekli ana kaya: 8 örtüşen blok, ortak doğrultu, %45 gömülü; arkasında +1,1 m toprak seti (arazi); dipte talus + yosun + eğrelti yalnız dibe |
| 4 | **Eşit dağılım, her yerde eşit detay = gürültü.** | XR3 P2 entry, P3 arrive | Raf şeridinde küçük bitkilerin %88'i, açıklık terasında tamamı kaldırıldı; eğrelti yalnız kaya dibinde |
| 5 | **Açıklığın kompozisyonu yok.** | XR3 P3 back | Sığ teras (+0,55 m kenar), meşe gelişte görüş hattına taşındı, 9 taşlık yay (r 4,8 m, eş boy, radyal), halka ağaçlar 7° dışa yatık, arkada dikili ölü ağaç |
| 6 | **Işık düz bir öğle anahtarı.** | hepsi | İki geri alınabilir alternatif: A alçak güney güneşi + yönlü nemli sis; B kapalı düşük kontrast |

Teşhisin özü: paket karışımı değil, **hiyerarşi yokluğu.** Aynı asset'ler hiyerarşiye girince (büyük/küçük, koyu/açık, boş/dolu) sahne "yazılmış" okunuyor. P2 bunu kanıtlıyor; P0 kanıtlamıyor çünkü orada hiyerarşi kurulmadı.

## 2. Uygulanan (x9 + i5)

- **Arazi (x9):** raf arkasına toprak seti (+1,1 m, 0,6–2,5 m doğudan, 6 m'de sönüyor), raf içinde 25 cm etek; açıklık terası (merkez düzlüğü %75, kenar +0,55 m r 5,2–7,6 m). 481 örnek değişti; 281 foliage instance yeniden zemine oturtuldu.
- **Ana kaya:** 8 × Environment_Set Big_Rock_01/02, ölçek 1,75–2,05, %45 gömülü, doğrultu boyunca 3–3,4 m aralıkla örtüşen; 4 talus (Middle_Rock), 2 eğrelti, dilimdeki 4 XR2 tek kaya gizlendi (çarpışma korundu).
- **Kanopi:** 11 kara ladin (raf üstü + dere ağzı), 4 kahraman çam (i5'te foliage instance olarak: aynı çarpışma sınıfı, aynı kamera davranışı), dilimdeki 3 köknar çamla değişti.
- **Açıklık:** 9 taşlık yay, 2 dikili ölü ağaç, meşe taşındı, halka ağaçlar yatık, terasta küçük bitki yok.
- **Zemin sessizliği:** raf şeridinde ve terasta toplam ~350 küçük instance kaldırıldı (çim, örtü, eğrelti, çalı, genç ağaç); 8305 → sayı listede.
- **Materyal:** XR3 i3'ün 9 proje sahipli MI ayarı ve 127 dinamik MI retint aynen.
- **Işık A/B:** mevcut sahiplerde (`EX_PostRain_Sun/Sky/Humidity`), yedekli, her çekim sonrası geri alındı.

## 3. Kanıt: önce/sonra aynı oyuncu kamerası

`compare/x4_P*_prod.jpg` (ÖNCE = üretim haritası, SONRA = x9+i4, üretim ışığı), `compare/x4_P*_clay.jpg` (kil, nötr ışık), `compare/x5_P*.jpg` (x9+i5), `compare/x4L_P*.jpg` (ışık A), `compare/x4LB_P*.jpg` (ışık B).

**P2 geçiş.** Kilde: ÖNCE düz zemin ve tek tek kayalar; SONRA tek bir kütle, karakterin solunda duvar, sağda açık raf. Işıklıda: koyu ladin üstte, iğne taban altta, raf boyunca ışık. Eleştiri: Big_Rock dokusu kristal ve açık; ışık A'da beyaza yaklaşıyor (ton düşürülmeli). Geri bakışta (exit_back) ev, su ve kaya aynı karede ve hiyerarşi tutuyor.

**P3 sessiz tekinsizlik.** Kilde teras kenarı ve taş yayı okunuyor; meşe gövdesi gelişte sağda. i4 ışıklıda yosun plakaları havada (FAIL, açık kusur); i5'te kaldırıldı. "fwd" karesi (suyun üstünden ev) bu turun en güçlü karesi: koyu orman duvarı, su, ev, teras ön planı.

**P0/P1 sığınak.** Kahraman gövdeler çerçeve veriyor (P0 fwd), verandadan sandal ve su okunuyor. Ön plan ve zemin değişmedi; bu an bu turda yeniden kurulmadı.

**Başarısız denemeler (ayrı):** i4 yosun plakaları (eğimde uçan 5 m yamalar); i4 kahraman çamlar aktör olarak (istasyon yerleştirici tepelerine çıktı, i5'te foliage'a taşındı); ışık B.

## 4. Işık/lookdev alternatifleri

| | Üretim | A | B |
|---|---|---|---|
| Güneş | −27°, yaw −38°, 1150 lux | −11°, yaw −95° (güney), 2200 lux, 5000 K | −32°, 380 lux, 7000 K, 8° yumuşak |
| Gök | 2,2 | 0,9 | 2,1 |
| Sis | 0,012, 7 m | 0,028, yönlü sıcak, 0 m | 0,02, soğuk |
| P2 | orta | raf arkadan rim, kaya fazla parlak | gri, kütle okunur |
| P3 fwd | iyi | en iyi: ev önden, su koyu | düz |
| P1 veranda | hüzmeler güzel | su parlak panel | sakin |

Karar: A yönü doğru (güney güneşi, raf ve dere ağzı için arka ışık); sonraki tur: yoğunluk 1600, kaya parlaklığı 0,45, su için yansıma kontrolü.

## 5. Kesintisiz yürüyüş ve performans

**Kirli deneme (ayrıldı):** i5'in ilk çekiminde XR3'ün geri alma işi yalnız `XR3_` etiketli aktörleri sildiği için i4'ün 114 aktörü (kahraman çam aktörleri, yosun plakaları, kopya ladin ve bloklar) sahnede kalmıştı. O çekimde yürüyüş 47. saniyede rota üstündeki bir i4 kahraman çamına takıldı (62 m'de durdu) ve istasyonlarda yosun plakaları görünüyordu. Geri alma `XR3_`+`XR4_` olarak düzeltildi, 114 aktör silindi, i5 temiz uygulandı; aşağıdaki kanıt temiz çekimdir (`compare_xr4/x6_*.jpg`, `stills_xr4/views_id_x6_*`). İlk çekimin kareleri `x5_*.jpg` olarak saklandı, kanıt sayılmıyor.

- `video/XR4_routeA_i5_prod_vs_lightA_part1..3.avi`: 107 s gerçek hız (sabit adım 30 FPS, ikide bir kare, 15 FPS oynatma), sol üretim ışığı, sağ ışık A; aynı kare aynı oyun zamanı. Rota çizgisini izleyen sürücü. **Videoyu gerçek zamanlı izlemedim**; t=20/40/60/80/100 s karelerine baktım.
- Kare gözlemleri: t≈40 s kaya sekisinde raf ve ladin duvarı okunuyor; t≈80 s karşı kıyı tırmanışında taş yayının bir kısmı teras kenarını aşıp yamaca çıkıyor ve orada "dizilmiş taş" gibi okunuyor (kusur; yay yarıçapı terasın içinde kalmalı).

| Koşu (A rotası, ışıklı, pass B) | Kare p50/p95 ms | Oyun iş parçacığı | GPU | VRAM MB |
|---|---|---|---|---|
| x8 (XR2) | 39,4 / 52,7 | 17,1 / 20,2 | 37,7 / 50,5 | 7046 |
| x9+i5 (XR4) | 36,7 / 50,2 | 13,8 / 15,8 | 35,0 / 48,2 | 6903 |

Fark ölçüm gürültüsü içinde; ~350 instance kaldırıldı, 42 aktör eklendi (11 ladin 26–62 bin üçgen, 12 Nanite dışı Big/Middle_Rock).

## 6. Geri alma

`data/restore_verify_xr4.txt`: yükseklik haritası sha1 aynı; foliage 57 bileşen / 8305 instance, 0 fark; aktörler 768/768 (etiket, sınıf, konum, gizlilik); XR2/XR3/XR4 aktörü 0; 4 kaya yeniden görünür; 127 materyal slotu ve 9 proje sahipli MI yedekten geri yazıldı; ışık sahipleri geri alındı. Harita diskte `70dd481a…` (2026-09-25). Bellekte harita ve 9 MI "dirty" ama içerik orijinal: **editörü kapatırken "Don't Save" seç.**

## 7. Dürüst kabul

- **Geçiş (P2):** Tier 3. "Bu Sphirus mu" sorusuna bu karede evet diyebiliyorum: tek kütle, koyu üst, sessiz alt, raf boyunca ışık. Eksik: kaya dokusu açık ve kristal (ışık A'da beyaza yaklaşıyor); kaya dibinde toprak birikimi arazide değil, blok gömülmesiyle taklit edilmiş.
- **Sessiz tekinsizlik (P3):** Tier 2–3. Suyun üstünden ev karesi güçlü; geliş karesinde taş yayı ve teras okunuyor; ama yayın yarısı yamaca taşıyor ve zemin çok çıplak kaldı (ot/yosun mozaiği yok, çünkü mevcut yosun mesh'leri eğimde plakaya dönüşüyor).
- **Sığınak (P0/P1):** Tier 2. Kahraman gövdeler çerçeve veriyor, sandal ve su okunuyor; "house_back" karesinde yeni çam dalları kamerayı kapatıyor (kahraman çam eve 5 m yakın). Ev önü yeniden kurulmadı.
- **Işık:** A doğru yön; yoğunluk ve kaya parlaklığı ayarı gerekli. B reddedildi.
- Videolar izlenmedi; görsel kabul kare örnekleriyle verildi.

## 8. Sonraki adım ve onay

Kayda hazır bir şey yok. Sorduğum onay, yön onayı: (1) kaya sekisi yaklaşımını (ana kaya + ladin üst + sessiz alt) ev önü ve iskele için de uygulamak; (2) ışık A'yı sahiplerde kalıcı değerlere taşımak (güney güneşi, 1600 lux, kaya parlaklığı 0,45); (3) taş yayını terasın içine almak ve kahraman çamı evden uzaklaştırmak. Onaylanırsa i6 aynı dilimde koşar; kabul: üç anın ±90° kareleri Tier ≥ 3 ve izlenmiş bir yürüyüş.

## Dosyalar

| | |
|---|---|
| `maps/XR4_plan.png` | üç anın planı |
| `compare_xr4/x4_P*_prod.jpg`, `x4_P*_clay.jpg` | ÖNCE/SONRA (i4), üretim ışığı ve kil |
| `compare_xr4/x6_P*.jpg` | ÖNCE / SONRA i5 üretim ışığı / SONRA i5 + ışık A (temiz kanıt) |
| `compare_xr4/x4L_*.jpg`, `x4LB_*.jpg` | ışık A ve B karşılaştırmaları (i4) |
| `compare_xr4/x5_*.jpg` | kirli ilk i5 çekimi (kanıt değil) |
| `compare_xr4/x6_walk_*.jpg` | yürüyüş kareleri |
| `stills_xr4/` | ham kareler |
| `video/XR4_*` | yürüyüş, iki ışık yan yana |
| `data/` | id_i4/i5, apply/restore kayıtları, plan_x9, ışık A/B tanımları, performans, geri alma doğrulaması |
| `tools/` | `xr4_design.py`, güncel `xr3_apply.py` (XR3+XR4 geri alma), `xr2_views.py` (ağaç aktörlerini yok sayan yerleştirici) |
