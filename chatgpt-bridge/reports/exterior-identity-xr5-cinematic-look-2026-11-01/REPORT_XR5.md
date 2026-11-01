# XR5: sinematik görsel kimlik — ışık, renk, atmosfer (üç yön, seçilen taban + bölgesel atmosfer)

İzole, bellek içi deneme; hiçbir paket kaydedilmedi (harita, ışık sahipleri, materyaller diskte değişmedi). 2026-11-01. UE 5.8.1, `L_GR_SphirusHouse`, gerçek oyuncu kamerası (GraceRanger), sabit adım 30 FPS. Dünya: XR2 x9 + XR4 i5 dilimi (ev sekisi → iskele → kaya sekisi → dere ağzı → karşı kıyı açıklığı). Bütün ışık değişiklikleri mevcut sahiplerde (`EX_PostRain_Sun / Sky / Atmosphere / Humidity / NeutralExposure`), tek yedekten (`data/xr5/xr5_backup.json`) her uygulamada sıfırlanarak; bölgesel hacimler `XR5_*` etiketli geçici aktörler. Her çekimden sonra geri alındı.

## 0. Sonuç önce

| Yön | Fikir | Ne oldu | Karar |
|---|---|---|---|
| **L1 "gümüş nem"** | Yağmur sonrası ince, gümüşi nem; güneş orta-alçak (−24°, yaw −62°), 5600 K; serin-nötr gölge, sıcak-nötr vurgu; düşük doygunluk | Kaya ve zemin detayı korunuyor, derinlik katmanları sisle değil değerle ayrılıyor, siyah ezilmiyor (%0,7); su beyaz panelden gri yüzeye iniyor. Hüzmeler hâlâ baskın | **Taban seçildi** |
| **L2 "bakır ışık"** | Alçak, sıcak (4600 K) arka ışık; yönlü sıcak sis; en koyu pozlama | En "sinematik" tek kare (P3 fwd), ama gölet ve orman sisle düzleşiyor, güneş temas ışığı kayboluyor; "daha çok sis" tuzağının tam kendisi | reddedildi (güzel kare, zayıf yürüyüş) |
| **L3 "kapalı mavi saat"** | Kapalı gök, 7400 K, yumuşak 6° güneş, yüksek kontrast, soğuk gölge | Kütleler okunuyor ama siyahlar eziliyor (%4,4; P2 L90 %15), verandadan ve sandaldan bakışta su yine beyaz panel; "soğuk LUT" tuzağı | reddedildi |
| **FINAL v1** = L1 + bölgesel hacimler | gölet sisi 0,08/0,14 | **Başarısız:** sis gölet boyunca aydınlık bir duvar oldu; histogram pozlaması sise uyup geri kalanı ezdi (P0 fwd %19,9 siyah, P3 fwd %12; ev açıklıktan görünmüyor) | ayrıldı; kanıt `compare_xr5/x8v1_*`, `x8res_*` orta sütun |
| **FINAL v2** = L1 ayarlı + bölgesel hacimler | hüzme 1,6→0,8; gök 1,7→1,45; sis su yüzeyine yapışık (3–4× ince); ev +0,2 EV sıcak, raf −0,2 EV serin, açıklık −0,1 EV sakin | Ortalama 73 / beyaz %0,19 / siyah %0,99; su beyaz paneli bitti (P2 R90 beyaz %3,05 → %0,00), kaya turuncu-parlak değil, ev bölgesi sıcak ve okunur, gölet koyu ve sessiz | **uygulanan yön** |
| **RES** = FINAL v2 + rezonans deltası | −300 K, doygunluk 0,94, gren +0,08, vinyet +0,1, kenar saçılması 0,35, hafif macenta gölge | Aynı yer "biraz başka" okunuyor; parıltı yok, nesne yok. İlk evre için yeterince ince | dil önerisi, uygulanmadı |

Başarı sorusu ("ışık/renk/atmosfer bu dünyaya ait mi?"): **FINAL v2 ile evet, tek bir dünya ve tek bir hava; ama kütle ve materyal sorunları ışıkla kapanmadı — bölüm 7'de ayrı listelendi.** Üretim ışığının verandadaki hüzmeli karesi tek kare olarak daha "çarpıcı"; FINAL v2 yürüyüş boyunca daha tutarlı.

## 1. Renk dili (tek dünya, tek hava)

Temel ilke: derinlik sisle değil **değer ve doygunluk kaybıyla**; gölge soğuk-nötr, orta tonlar nötr yeşil-kahve, güneş vurgusu sıcak-nötr ama doygunluğu düşük; beyaz nokta hafif soğuk (6200 K) ki ıslak taş ve su gümüş okusun, ev ahşabı ise bölgesel +sıcaklıkla ayrılsın.

| Katman | Değer (FINAL v2) | Niyet |
|---|---|---|
| Güneş | pitch −24°, yaw −62°, 1300 lux, 5600 K, disk 1,6°, hacimsel saçılma 0,8 | Orta-alçak; raf ve dere ağzı yan/arka ışık; hüzme vurgu, örtü değil |
| Gök | 1,45 (üretim 2,2) | Gölge dolgusu serin ama daha az; gölge okunurluğu yerel pozlamadan |
| Atmosfer | Mie 0,02, anizotropi 0,7 | Uzak katmanlar gümüşleşir |
| Yükseklik sisi | 0,015, düşüş 0,22, başlangıç 3 m, opaklık 0,55, iç saçılma [0,050 0,058 0,066], yönlü [0,012 0,0135 0,015] üs 8, hacimsel sönüm 1,5, albedo [200 210 220] | Nem her yerde ince; yön vurgusu yalnız güneşe bakınca |
| Beyaz dengesi | 6200 K, tint 0 | Gümüş |
| Gölge / orta / vurgu | gölge kazancı [0,96 1 1,06] + ofset [0,006 0,008 0,012]; vurgu doygunluğu 0,8, vurgu kazancı [0,98 0,975 0,96] | Soğuk gölge, sıcak-nötr düşük doygunluklu vurgu |
| Kontrast / doygunluk | 1,08 / 0,86 | Düşük doygunluk, orta kontrast |
| Tonmap (filmic) | slope 0,86, toe 0,6, shoulder 0,26, white clip 0,03 | Yumuşak omuz: su ve gök yanmaz |
| Pozlama | histogram, bias −0,75, min −1, max 10; yerel pozlama vurgu 0,78 / gölge 0,9 | Gölge detayını ezmeden parlak suyu bastır |
| Bloom / vinyet / gren | 0,25 (eşik 0,5) / 0,3 / 0,08 | Yalnız nem parıltısı; ölçülü |

**Bölgesel değişkenler (aynı güneş, aynı hava):**

| Hacim | Yer / boyut | Delta | Niyet |
|---|---|---|---|
| `XR5_PPV_House` | (900, 1300), 110×90 m, blend 9 m | +0,2 EV, −250 K, orta ton [1,03 1 0,96] | Sığınak: açık, sıcak, net |
| `XR5_PPV_Shelf` | (2900, 4900), 44×120 m, blend 7 m | −0,2 EV, kontrast 1,05, gölge [0,95 1 1,07] | Geçiş: daha koyu, daha serin, kapalı |
| `XR5_PPV_Glade` | (−900, 8750), 80×80 m, blend 9 m | −0,1 EV, doygunluk 0,9, yerel vurgu 0,75 | Sessiz tekinsizlik: sakin, az renk |
| `XR5_Fog_Pond` | (−600, 5200, −110), 42×38×4 m | radyal 0,004, yükseklik 0,05 düşüş 3,5 m, albedo [0,76 0,79 0,82] | Su yüzeyine yapışık nem; görünürlüğü düşük (bkz. 7) |
| `XR5_Fog_Inlet` | (2300, 7300, −40), 14×12×3 m | radyal 0,01, yükseklik 0,06 düşüş 3 m | Dere ağzında nem |

## 2. Üç yön, aynı 24 oyuncu kamerası

`compare_xr5/x7_<yer>_<bakış>.jpg`: ÜRETİM | L1 | L2 | L3. Ham kareler `stills_xr5/views_id_x7_L1|L2|L3`.

| | Üretim | L1 gümüş nem | L2 bakır ışık | L3 kapalı mavi |
|---|---|---|---|---|
| Güneş | −27°, −38°, 1150 lux, 6500 K | −24°, −62°, 1400 lux, 5600 K | −10°, −95°, 1600 lux, 4600 K | −34°, −75°, 650 lux, 7400 K, 6° |
| Gök / sis | 2,2 / 0,012 | 1,7 / 0,016 | 0,9 / 0,022 sıcak yönlü | 2,5 / 0,026 soğuk |
| WB / kontrast / doygunluk | 6500 / 1 / 1 | 6200 / 1,08 / 0,86 | 5300 / 1,12 / 0,92 | 6900 / 1,18 / 0,8 |
| Ortalama parlaklık / beyaz % / siyah % / doygunluk (24 kare) | 90 / 0,15 / 0,59 / 0,217 | 79 / 0,51 / 0,72 / 0,213 | 72 / 0,00 / 1,73 / 0,179 | 82 / 0,30 / 4,37 / 0,227 |
| P1 sandal (su) | parlak düz yüzey | koyu, hüzmeli | koyu kahve, sis | **beyaz panel** |
| P2 raf (kaya) | sıcak tan, parlak | gümüş, detay | gri-sıcak, düz | soğuk, siyah ezik |
| P3 fwd (ev suyun üstünden) | iyi | iyi, su gri | **en iyi tek kare**, ev sisli | soğuk, düz |
| P0 fwd (ev önünden gölet) | hüzme | hüzme, gri su | koyu, ağır | düz, soğuk |

Okuma: L1 tek başına en dengeli (en düşük siyah ezilmesi, nötr RGB, kaya detayı). L2'nin gücü tek karede, zayıflığı yürüyüşte (her yer aynı sıcak sis). L3 kütleyi okutuyor ama siyah ezerek ve suyu beyazlatarak; "soğuk ve karanlık = atmosfer" tuzağı.

## 3. FINAL: v1 başarısızlığı ve v2

`compare_xr5/x8_<yer>_<bakış>.jpg`: ÜRETİM | L1 | FINAL v2. `x8side_<yer>.jpg`: ±90° ÜRETİM/FINAL. `x8v1_*.jpg` ve `x8res_*.jpg`: v1 (aşırı sis) kanıtı.

- **v1 (başarısız, ayrıldı):** gölet LocalFogVolume 0,08 radyal / 0,14 yükseklik. Gölet üstünden bakan her istasyonda sis aydınlık bir duvar oluşturdu, histogram pozlaması ona uyup ön planı ezdi: P0 fwd siyah %19,9, P1 sandal %13,4, P3 fwd %12,1; ortalama siyah %6,9, doygunluk sisin mavi albedosuyla 0,28'e çıktı. Bu, "sisle örtme"nin sayısal hâli.
- **v2:** sis su yüzeyine yapışık (z −110, 4 m yükseklik, düşüş 3,5 m, 0,004/0,05), dere ağzı aynı mantıkla; raf −0,35→−0,2 EV, açıklık −0,15→−0,1; güneş hacimsel saçılması 1,0→0,8. Sonuç ortalama 73 / beyaz %0,19 / siyah %0,99 / doygunluk 0,238: üretimden ~1/3 EV koyu, siyah ezilmesi L1 düzeyinde, beyaz kırpma üretim düzeyinde.

Kare gözlemleri (FINAL v2):
- **P1 sandal / R90:** su artık koyu, kıyıda ince parıltı; üretimde beyaz %3,05 olan P2 R90 su karesi %0,00. Hüzmeler kalıyor ama örtmüyor.
- **P2 raf fwd / L90:** kaya gümüş-gri, tanecik ve yosun okunuyor; üretimde sıcak-tan ve parlak. Arka orman derinlik katmanıyla ayrılıyor; dere ağzı sisi ince bir aydınlanma olarak var.
- **P2 exit_back:** kaya turuncu lekeli ve beyaz değil; arkada ev sıcak (ev hacmi), su koyu lacivert, kaya serin: üç materyal aynı karede ayrışıyor.
- **P0 house_back / P1 L90:** ev bölgesi daha açık ve sıcak; veranda ahşabı okunur; çam yeşilleri doygun kalıyor.
- **P3 fwd:** ev görünür, su yansımalı, karakter ezik değil; v1'in sis duvarı yok.
- **P3 arrive:** üretimin hüzmeli, "güzel" karesi yok; zemin ve taş yayı düz ışıkta — burada FINAL daha az çarpıcı. Kırmızı-mor yaprak döküntüsü (bkz. 7) FINAL'de de rahatsız ediyor.

## 4. Pozlama ve renk değerlendirmesi

`data/xr5/exposure_table_xr5.md` (24 istasyon × 7 set; hücre = ortalama parlaklık 0–255 / ≥245 beyaz % / ≤10 siyah % / doygunluk; 4 piksel adımla örnekleme). Yer ortalamaları:

| Yer | Üretim | L1 | L2 | L3 | FINAL v1 | FINAL v2 | RES |
|---|---|---|---|---|---|---|---|
| P0 ev | 88 / 0,05 / 0,73 / 0,233 | 79 / 1,14 / 0,65 / 0,214 | 73 / 0 / 1,09 / 0,174 | 84 / 1,00 / 3,40 / 0,212 | 68 / 0,38 / 7,18 / 0,271 | **73 / 0,56 / 0,78 / 0,236** | 69 / 0,51 / 1,00 / 0,285 |
| P1 iskele | 87 / 0,03 / 0,21 / 0,215 | 78 / 0,77 / 0,43 / 0,201 | 69 / 0 / 1,93 / 0,172 | 82 / 0,08 / 5,42 / 0,203 | 69 / 0,01 / 10,35 / 0,272 | **72 / 0,20 / 0,88 / 0,223** | 68 / 0,26 / 1,02 / 0,273 |
| P2 raf | 93 / 0,51 / 1,23 / 0,254 | 78 / 0,03 / 1,64 / 0,215 | 71 / 0 / 3,57 / 0,166 | 80 / 0,04 / 7,17 / 0,247 | 59 / 0 / 7,45 / 0,273 | **70 / 0,01 / 1,96 / 0,243** | 66 / 0,01 / 2,26 / 0,321 |
| P3 açıklık | 91 / 0,03 / 0,20 / 0,165 | 82 / 0,11 / 0,18 / 0,222 | 74 / 0,01 / 0,33 / 0,206 | 84 / 0,07 / 1,48 / 0,247 | 69 / 0 / 2,52 / 0,290 | **75 / 0,01 / 0,34 / 0,250** | 71 / 0,01 / 0,40 / 0,306 |

Okuma: üretim her yerde aynı parlaklıkta (87–93) = yer kimliği yok; FINAL v2'de ev 73 ≈ iskele 72 > raf 70, açıklık 75 ama en az doygun ve en az kontrastlı (raf en koyu ve serin; ev en sıcak). Beyaz kırpma yalnız ev bölgesinde (güneşli duvar, bilinçli). Siyah ezilmesi her yerde <%2. "Parlak beyaz su" ölçülebilir olarak çözüldü (P2 R90 beyaz %3,05 → %0,00; P1 R90 ortalaması 84 → 65). Kaya parlaklığı: P2 L90 kaya duvarı ortalaması 91 → 69, doygunluk 0,40 → 0,21 (sıcak tan → gümüş).

## 5. Yürüyüş: ev → gölet → orman sürekliliği

`video/XR5_routeA_prod_vs_FINAL_part*.avi`: A rotası 101 m, gerçek hız (sabit adım 30 FPS, ikide bir kare, 15 FPS oynatma), sol üretim ışığı, sağ FINAL v2; aynı kare aynı oyun zamanı. Ham yürüyüş kareleri yayınlanmadı (1,1 GB/çekim); t=20/40/60/80/100 s kareleri `compare_xr5/x8_walk_*.jpg`.

**Videoyu gerçek zamanlı izlemedim**; t=20/40/60/80/100 s karelerine baktım. Gözlem:
- t≈20 s (raf boyu): üretimde kaya sıcak-tan ve zemin yeşil-kahve; FINAL'de kaya gümüş-gri, zemin koyu ve serin, su koyu. Ama güneş alan blok üstleri FINAL'de de beyaza yakın: kaya parlaklığı ışıkla yalnız yarı çözüldü (bölüm 7, #2).
- t≈60 s (dere ağzı ormanı): üretimde tek bir hüzme sahneye "güzel" bir odak veriyor; FINAL'de ışık düz ve eşit, kare daha sakin ama daha az çarpıcı. Burada FINAL'in zayıf noktası: orman içinde değer hiyerarşisini yalnız bölge biası ve derinlik katmanı taşıyor, ışık odağı yok. Mor-kırmızı döküntü iki tarafta da rahatsız.
- t≈80 s (karşı kıyı tırmanışı, taş yayı): fark küçük; FINAL biraz serin ve az doygun. Yayın yamaca taşması her ikisinde.
- Üç bölge arasında güneş yönü, gök ve sis aynı; geçişler hacim blend yarıçapıyla (7–9 m) yumuşak, kare örneklerinde pozlama sıçraması yok.
Sürekliliğin "duygusal" değerlendirmesi izlenmiş bir yürüyüşü gerektirir: NOT_TESTED (kare örnekleriyle PARTIAL). Dürüst okuma: FINAL yürüyüş boyunca tutarlı; üretimin rastgele hüzmeleri tek karede daha güçlü, yürüyüşte tutarsız.

## 6. Rezonans dili (aynı yer, biraz başka)

Önerilen kural: **güneş, gök ve sis asla değişmez** (dünya aynı); değişen yalnızca algı katmanı: beyaz dengesi −300 K (hafif sıcak-macenta), doygunluk ×0,94, gren +0,08, vinyet +0,1, kenar saçılması 0,35, gölge kazancı [0,98 0,96 1,04]. İlk evrede bu kadar; sonraki evrelerde aynı eksenler kademeli (−600 K, saçılma 0,7, bölgesel hacimlerin blend yarıçapı daralır, gölet sisi albedosu hafif sıcak). Parıltı, nesne, renk sıçraması yok. RES kareleri `compare_xr5/x8res_*.jpg` sağ sütun; sayısal fark FINAL v2'ye göre −4 parlaklık, +0,06 doygunluk (macenta gölgeden), siyah +%0,2.

## 7. Işıkla kapanmayan kütle / kompozisyon / materyal sorunları (ayrı liste)

Bunlar FINAL v2'de de görünür; ışık/renk bunları gizlemek için kullanılmadı.

| # | Sorun | Kanıt | Sahip / çözüm |
|---|---|---|---|
| 1 | **Su materyali**: beyaz panel ışıkla düştü ama suyun düz, pürüzsüz, yansıma-ağırlıklı okunması materyal kaynaklı (pürüzlülük/normal/derinlik rengi). Hüzmeli karede su hâlâ "cam" | P1 sandal, P2 R90 | su MI (proje sahipli kopya): pürüzlülük artışı, koyu derinlik rengi, rüzgâr normal'i |
| 2 | **Big_Rock dokusu** kristal ve açık; FINAL gümüşe çekti ama tanecik ölçeği hâlâ "granit prop" | P2 fwd, L90 | MI albedo 0,45 + makro kir/yosun maskesi; alternatif kaya seti |
| 3 | **Kırmızı-mor geniş yaprak döküntüsü** çam ormanında; FINAL'in düşük doygunluğunda bile rahatsız | P3 arrive, P2 fwd zemin | döküntü katmanı iğne/kahve ile değişmeli (foliage/decal) |
| 4 | **Taş yayı** terasın kenarını aşıp yamaca çıkıyor | P3 arrive, yürüyüş 80 s | yay yarıçapı terasın içinde kalmalı (XR4 notu, açık) |
| 5 | **Açıklık zemini çıplak**; yosun mozaiği yok (mevcut yosun mesh'leri eğimde plaka) | P3 arrive/seat | yosun için eğime uyan decal/landscape layer |
| 6 | **Ev önü yeniden kurulmadı**; sığınak anı ışıkla sıcak okunuyor ama ön plan hâlâ paket dağılımı | P0 fwd, front_path | XR4 raf yaklaşımı ev önüne |
| 7 | **Kahraman çam dalları** house_back kamerasını kapatıyor | P0 house_back | çamı 5 m uzaklaştır |
| 8 | **Köknar kanopi çatışması** (808 köknar harita geneli), raf dilimi dışında duruyor | P1 L90 arka | tür listesi kararı |
| 9 | **Hüzmeler kameraya**: P0/P1'de güneş yönü kameraya denk gelince hüzmeler ne yaparsan yap baskın; FINAL vurguya indirdi ama kaldıramaz | P0 fwd, P1 veranda | kabul edilebilir vurgu; istenmezse güneş yaw'ı −62 → −80 (raf arka ışığını korur) |
| 10 | **Gölet sisi görünmüyor**: v2'de güvenli ince değer su yüzeyinde neredeyse okunmuyor; "sessiz zamansız" his suyun koyuluğundan geliyor, nemden değil | P3 fwd | 0,01–0,02 arası tek bir ek deneme; ya da Niagara buhar (vfx sahibi) |

## 8. Geri alma

Her çekim sonrası `look5:restore`: sahipler `xr5_backup.json`'dan geri yazıldı, 5 `XR5_*` aktörü silindi (`data/xr5/xr5_restore.json`, problem 0). Dünya katmanı (x9 + i5) ve 9 proje sahipli MI XR4'teki yöntemle geri alındı; doğrulama `data/restore_verify_xr5.txt`: yükseklik haritası sha1 aynı; foliage 57 bileşen / 8305 instance, bütün konumlar aynı (6 bileşende yalnız −0,0/0,0 işaret farkı, XR4 anlık görüntüsünde de aynı); aktörler 768/768; XR2/XR3/XR4/XR5 aktörü 0; 4 kaya yeniden görünür, 42 aktör silindi, 127 materyal slotu ve 9 MI yedekten. Diskte hiçbir `.umap/.uasset` değişmedi; bellekte harita ve MI'lar dirty ama içerik orijinal: **editörü kapatırken "Don't Save" seç.**

## 9. Dürüst kabul

- Üç yön gerçekten farklı (gümüş / bakır / kapalı mavi) ve aynı 24 kamerada karşılaştırıldı: PASS.
- Tutarlı taban + bölgesel değişkenler: FINAL v2 teknik PASS (sayılar bölüm 4); görsel kabul: ev ve raf Tier 3 (ışık olarak), iskele Tier 3, açıklık Tier 2 (düz ışık, döküntü ve çıplak zemin ışıkla kapanmıyor).
- "Parlak beyaz su, aşırı parlak kaya, solgun orman, kayıp gölge detayı": su ve kaya ölçülebilir düzeldi; orman solgunluğu değer katmanlarıyla düzeldi; gölge detayı siyah <%2 ile korunuyor. Suyun materyal karakteri ve kaya dokusu açık kalıyor (7).
- FINAL v1 başarısız ve ayrıldı; v2 tek düzeltme turuydu, küçük dokunuş döngüsü yapılmadı.
- Yürüyüş videosu izlenmedi; süreklilik kare örnekleriyle PARTIAL.
- Hiçbir şey kaydedilmedi.

## 10. Onay sorusu

Kayda hazır bir şey yok. Sorduğum, yön onayı: (1) FINAL v2 değerlerini (bölüm 1) `EX_PostRain_*` sahiplerine ve `XR5_PPV_*`/`XR5_Fog_*` hacimlerini haritaya kalıcı yazmak; (2) bölüm 7'deki 1–3'ü (su MI, kaya MI, döküntü) ayrı bir materyal turu olarak açmak; (3) rezonans deltasını bir PPV blend ağırlığı olarak hazırlamak (oyun mantığı sahibi sonra bağlar). Onaylanırsa, kayıt öncesi manifest + yedek ve kayıt sonrası aynı 24 kamera ile doğrulama.

## Dosyalar

| | |
|---|---|
| `compare_xr5/x7_*.jpg` | ÜRETİM / L1 / L2 / L3, 8 istasyon |
| `compare_xr5/x8_*.jpg` | ÜRETİM / L1 / FINAL v2, 12 istasyon; `x8side_*` ±90° |
| `compare_xr5/x8v1_*.jpg`, `x8res_*.jpg` | FINAL v1 (başarısız) ve RES |
| `compare_xr5/x8_walk_*.jpg` | yürüyüş kare örnekleri |
| `stills_xr5/` | 24 istasyon ham kareler: L1, L2, L3, FINAL (v2), RES |
| `video/XR5_routeA_prod_vs_FINAL_part*.avi` | yürüyüş, üretim ve FINAL v2 yan yana |
| `data/xr5/` | `xr5_backup.json`, `xr5_L1/L2/L3/FINAL/RES/restore.json`, `xr5_FINAL_v1_overmist.json`, pozlama JSON'ları + tablo, yürüyüş günlükleri, `restore_verify_xr5.txt` |
| `tools/` | `xr5_look.py` (üç yön + FINAL/RES + yedek/geri alma), `xr5_final.py` (v2 ayarı), `exposure_stats.ps1`, `exposure_table.py` |

---

## 11. Onay sonrası: FINAL v2 haritaya kaydedildi (2026-11-01 06:18)

Kullanıcı onayı ("Evet") ile `tools/xr5_promote.py` gated runner üzerinden (manifest `xr5_map`, doğrulanmış yedek `…/manifests/xr5_map/…/L_GR_SphirusHouse.umap` sha1 `70dd481a…`) çalıştı:

- Işık sahipleri `EX_PostRain_Sun / Sky / Atmosphere / Humidity / NeutralExposure` = bölüm 1 değerleri (deneme ile aynı kod yolu, `xr5_backup.json`'dan).
- Beş bölgesel hacim kalıcı: `EX_Look_PPV_House / PPV_Shelf / PPV_Glade / Fog_Pond / Fog_Inlet` (klasör `EX_PostRain_Look`; `XR5_` ön eki kaldırıldı ki deneme geri almaları bunları silmesin).
- `EX_Look_Resonance`: sınırsız PPV, öncelik 3, **blend weight 0** (etkisiz); bölüm 6'nın deltası mutlak değer olarak hazır (WB 5900 K, doygunluk 0,81, gren 0,16, vinyet 0,40, kenar saçılması 0,35, gölge kazancı [0,98 0,96 1,04]). Oyun mantığı sahibi blend weight'i rezonans ilerlemesine bağlar. Not: deneme RES karelerinde doygunluk yanlışlıkla mutlak 0,94 uygulanmıştı (FINAL 0,86'dan yüksek); kalıcı PPV'de doğru çarpan (×0,94 → 0,81) kullanıldı, bu yüzden RES kareleri kalıcı deltadan biraz daha doygundur.
- **Yalnız harita paketi kaydedildi** (`save_packages([map])`, `save_ok True`); harita sha1 `70dd481a…` → `6d3efa3a…`. XR3 denemesinden dirty kalan 9 proje MI'sı (içerik orijinal) kaydedilmedi; editörü kapatırken o 9 MI için **"Don't Save"**.
- Doğrulama (`data/save_verify_xr5.txt`): yükseklik haritası aynı, foliage 57/8305 konum farkı 0, aktör 768 → 774 (yalnız 6 look aktörü eklendi, silinen 0). Kayıt sonrası aynı 24 istasyon (`stills_xr5/views_id_x8_saved`, `data/xr5/exposure_saved.json`): ortalama 72,5 / beyaz %0,22 / siyah %0,99 — deneme FINAL ile aynı (72,5 / 0,19 / 0,99). İstasyon başına farklar (en çok P3_glade_back, 8,4) dünya katmanından: deneme kareleri x9+i5 (XR4 raf, teras, retint) üzerindeydi, kaydedilen harita **üretim dünyasını** koruyor (XR2/XR4 dünya katmanları kaydedilmedi, ayrı onay bekliyor).
- `xr5_backup.json` → `xr5_backup_preXR5_production.json` (eski üretim ışığı); sonraki `look5` koşusu yeni üretimden taze yedek alır.

## 12. Materyal turu (bölüm 7, #1–3): izole deneme, kaydedilmedi

Sahip probu (`data/xr5/xr5_mat_probe.json`, `tools/xr5_mat_probe.py`): su = proje sahipli `MI_EX_Pond` (ebeveyn `M_PR_CalystoPhysicalInland`, aktör `EX_Pond_CalmSurface`; Roughness 0,34, Specular 0,2, Murkiness 3,8, Absorption [0,14 0,125 0,11], Calm Normal Amplitude 0,025). Döküntü = foliage `SM_DeadLeaves02` (194 instance) satıcı `MI_DeadLeaves01` (Color_Tint [0,68 0,49 0,21], Albedo 0,6). **Big_Rock üretim haritasında yok** (XR4 raf katmanı kaydedilmedi) → kaya MI turu XR4 dünya terfisiyle birlikte.

Deneme (`tools/xr5_mat_trial.py`, manifest `xr5_mat`, bellek içi, geri alındı; `compare_xr5/x10_*.jpg` ÖNCE = kaydedilmiş harita, SONRA = deneme):
- **Su:** Roughness 0,45, Specular 0,16, Murkiness 5,5, Absorption [0,20 0,165 0,12], Calm Normal Amplitude 0,06. Sandal ve P2 R90 karelerinde yüzey artık cam değil: koyu, mikro dalgalı, kıyıda kırık parıltı; derinlik çay rengi. Eleştiri: parıltı noktaları biraz fazla (0,06 → 0,045 önerilir). Sonuç **PARTIAL (yön doğru, bir ayar daha)**.
- **Döküntü:** 194 instance'a iğne-kahve dinamik MI (tint [0,38 0,30 0,19], albedo 0,45) uygulandı; ama 8 istasyonun hiçbirinde `SM_DeadLeaves02` kadrajda değil (mor döküntü kareleri XR4 dilimindeydi) → görsel kanıt yok, **NOT_TESTED**; sayısal olarak uygulandı ve geri alındı.
- P3_glade_fwd SONRA karesinde karakter kameraya dönük: istasyon yerleştiricinin yaw'ı kontrol rotasyonundan önce oturmuş; ışık/materyal kanıtı değil, yerleştirici gürültüsü.

Kayıt için onay sorusu: `MI_EX_Pond` için su değerleri (amplitude 0,045 ile) kaydedilsin mi? Döküntü için önce `SM_DeadLeaves02`'nin göründüğü bir istasyon tanımlanmalı.
