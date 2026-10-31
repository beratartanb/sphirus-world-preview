# v7 — Environment Visual Master Pass (izole deneme, kaydedilmedi)

Tarih: 2026-10-31 · Editör: UE 5.8.1 (V2.40 oturumu, sabit adım 30 FPS) · Harita: `L_GR_SphirusHouse` · Kamera: gerçek oyuncu kamerası (BP_PBI_Player + GraceRanger, FOV 60, kol 300 cm)

## Sonuç (önce bunu okuyun)

| Alan | Durum |
|---|---|
| Teknik akış (manifest, kilit, PIE kuralları, geri alma) | **PASS**. Deneme yalnızca bellekte yapıldı. Sonunda geri alındı ve doğrulandı. Disk üzerindeki harita sha1 `70dd481a…` değişmedi. |
| Arka patika (ağaç altı yürüyüş, 16–60 m): okunabilirlik + ışık hiyerarşisi | **Belirgin iyileşme**. Patika artık zeminden çıkan, kesintili bir toprak izi olarak okunuyor. Kenarlarda dal, taş, kök ve eğrelti grupları var. Güneş/gölge ayrımı net. |
| Bütünsel "AAA dönüşümü" | **PARTIAL**. Fark gerçek ama sınırlı. Kök nedenlerin yarısına (landscape malzemesi, büyük kütle ve siluet düzeni, IFA yoğunluk dağılımı) dokunulmadı. |
| Gölet (pond_shore) | **GERİLEME**. V0'daki ışık hüzmeleri kayboldu. Su düz beyaz bir yüzey gibi okunuyor. |
| Kamera | **PASS (yürüyüş)** / **PARTIAL (tek istasyon)**. Ayrıntılar aşağıda. |
| Performans | **PASS**. GPU medyanı +0,6 ms (%1,5), p95 aynı. VRAM +270 MB. |
| Görsel/oyun hissi kabulü | **Kullanıcı kararı**. Videolar gerçek zamanlı izlenmedi; değerlendirme 1 fps örnek karelerden ve istasyon görüntülerinden yapıldı. |

Kalıcı hiçbir şey kaydedilmedi. Ana sahne, hareket sistemi (ABP'ler temiz, dirty içerik paketi 0) ve production assetleri dokunulmamış durumda.

---

## 1. V0 değerlendirmesi: kök nedenler (oyuncu kamerasından, 7 istasyon × 3 yön)

1. **Zayıf güneş, güçlü gök dolgusu** (güneş 1150 lux / gök 2,2). Gölgeler kalkık, form okunmuyor. Her şey aynı değerde ve düz.
2. **Sis 7 m'de başlıyor, opaklığı %50.** Orta mesafe sütlü, gölet yıkanmış görünüyor.
3. **Tek tip orta boy dağılım.** Büyük/orta/küçük kütle hiyerarşisi yok.
4. **Zemin tek malzemeli ve tekdüze.** Patika "yeşil eğimde biraz kahverengi" olarak okunuyor; kenar geçişi, kök, taş ve döküntü yok.
5. **Geniş yapraklar kameraya giriyor.** Bu sorun v5/v6'da ayrı ele alındı.

## 2. Üç ışık/atmosfer yaklaşımı (aynı kamera, aynı istasyonlar)

Tüm varyantlar mevcut look sahiplerine yazıldı (EX_PostRain_Sun / _Sky / _Humidity). LUT, renk düzenleme, bloom ve vinyet değiştirilmedi (AGENTS: turuncu/teal grade yok). Her uygulamadan önce orijinal değerlere dönüldü, sonra `recapture_sky()` çalıştırıldı.

| Varyant | Güneş (pitch, yaw / lux / K / açı) | Gök | Sis (yoğunluk / başlangıç / opaklık) | Gözlem |
|---|---|---|---|---|
| V0 (mevcut) | -27, -38 / 1150 / 6500 / 1,3 | 2,2 | 0,012 / 700 / 0,50 | Düz, sütlü |
| V1 "filtrelenmiş gün ışığı" (Requiem benzeri) | -38, -38 / 3200 / 5600 / 1,0 | 1,1 | 0,008 / 1200 / 0,40 | En güçlü hiyerarşi ve form; fazla sıcak |
| V2 "alçak nemli sabah" | -14, 59 / 2400 / 4900 / 1,5 | 1,3 | 0,020 / 300 / 0,60 + yönlü saçılım | Atmosferik ama sütlü ve düz; hüzme artefaktı |
| V3 "bulutlu ıslak serin" (TLOU2/PNW benzeri) | -45, -38 / 450 / 6800 / 10 | 2,4 | 0,016 / 500 / 0,55 | Yumuşak ve serin ama düz, okuma zayıf |
| **Seçilen TRIAL2/3** | -36, -38 / **2600 / 6500** / 1,0 | **1,4** | 0,010 / 900 / 0,45 | V1'in yapısı, Sphirus paletine soğutulmuş, biraz V3 nem derinliği |

Görsel: `v7/compare/iteration/variants_compare.jpg`, ham kareler `v7/stills/V0..V3`.
İlk TRIAL'de (3000 lux / 6100 K / gök 1,3) güneşteki eğreltiler asit yeşili görünüyordu, bu yüzden güneş zayıflatıldı ve soğutuldu (TRIAL2).

## 3. Çevre tasarımı: ~45 m'lik bağlantılı örnek alan (yay 16–60 m)

Patika dört bölgeye ayrıldı. Sağ taraf her yerde yokuş yukarı.

| Bölge | Rol | Uygulama (yalnızca mevcut assetler) |
|---|---|---|
| Z1 eşik (yay ~30–35 m) | Avludan ormana geçiş | Yokuş tarafında kapı kayası + taş (çit ve odun yığını insan tarafını tutuyor); kök yaması; eğrelti grubu; dal |
| Z2 tırmanış (~35–42 m) | Yönlendirme, ritim | İzi dikleştiği yerde enine kesen yosunlu kök kütlesi (doğal basamak); şev dibinde kökler; sol kenarda toprak geçişi; taşlar |
| Z3 sıkışma (~45–50 m) | Kapanma | Kayalık şev (2 büyük kaya + dip taşları); şev dibinde 2 eğrelti grubu (büyük/orta/küçük); sol aşağıda devrik gövde |
| Z4 açılma (~53–60 m) | Rahatlama | Açıklık korundu; yokuş kenarında kütük; toprak geçişi; küçük eğrelti grupları, kenar döküntüsü |
| İz | Patika okuması | Her 2,4 m'de bir `Forest_Ground` decal (iğne yaprağı + toprak), her 4. aralık boş (kesintili, "temiz kahverengi şerit" değil) |

Son yapı (TRIAL3) 57 öğeden oluşuyor:
- 18 decal;
- 39 mesh:
  - 5 kaya ve taş, 1 gövde, 1 kütük;
  - 20 eğrelti;
  - 6 Megascans kök: 3 `tkwqbbofa` yama kökü + 3 `wgxjfhr` yosunlu kök;
  - 3 dal, 2 küçük taş grubu.

Hepsi `VMP_` etiketli ve `VMP_Trial` klasöründe. Spec: `v7/data/trial_spec2.json`; uygulanan konumlar ve rotasyonlar: `v7/data/build_build.json`.

### Yineleme geçmişi (neyin işe yaramadığı da kanıt)

| Sürüm | Sorun (görüntüden) | Kök neden | Düzeltme |
|---|---|---|---|
| TRIAL (60 öğe) | Dirt_Track decal'ları araç tekerlek izi gibi okunuyor | Yanlış asset semantiği | Kaldırıldı |
| TRIAL | Scattered_Leaves sarı geniş yaprak | Kozalaklı ormana ve palete uymuyor | Kaldırıldı |
| TRIAL | SM_Root_4 ağarmış beyaz çubuk; şev mesh'inde neon yeşil yosun | Asset malzemesi | Kaldırıldı |
| TRIAL | compression_left90'da kamera kafaya girdi (84 cm, V0 171) | Eklenen prop'lar kamerayı itiyor | TRIAL2: Camera kanalı yok sayıldı → 104 cm (kısmi) |
| TRIAL2 | Arka girişte soluk "tabak": Megascans yama kökü eğimde yatay duruyor, alt kenarı havada, gölge düşürüyor, üstüne decal boyanmış | Düz mesh + eğim; decal projeksiyonu | TRIAL3: düz prop'lar eğim normaline hizalandı; mesh'ler decal almıyor |
| TRIAL2 | Eğreltiler hâlâ kamerayı çekiyor | GR kamera sondaları Visibility kanalını da okuyor (Camera ignore yetmedi) | TRIAL3: yumuşak prop'lar (eğrelti, dal, küçük taş, kök) NoCollision, yerli yumuşak foliage gibi. Sert prop'lar (kaya, gövde, kütük) çarpışmayı korudu, yalnızca Camera kanalını yok sayıyor |
| TRIAL2 | SM_FernWild01 güneşte asit yeşili | Asset malzemesi; ışık düzeltmesi yetmedi | TRIAL3: SM_FernLong01 kullanıldı |
| TRIAL2 | Decal kutusu ±90 cm, kaya yüzeylerini boyayabiliyor | Projeksiyon derinliği | TRIAL3: decal'lar eğim normali boyunca, ±30 cm |

Not: release istasyonunda V0'da "koyu kaya" gibi görünen kütle aslında bir **toprak şevi**. Trial ışığında toprak olarak okunuyor; bir şey silinmedi (`compare/iteration/release_crop.jpg`, V1/V3 karşılaştırması).

## 4. Sonuçlar: BEFORE (V0) ve TRIAL3

Görüntüler `v7/compare/V0_vs_TRIAL3/` altında: istasyon başına yan yana kareler ve `overview_forward_V0_vs_TRIAL3.jpg`.

| İstasyon | Değerlendirme |
|---|---|
| house_front | Daha net form ve değer ayrımı; ev daha az yıkanmış. Beyaz gömlek güneşte kırpılmaya yakın. Pozlama dokunulmadı, bu açık bir sorun. |
| pond_shore | **Geriledi**. V0'daki hacimsel hüzmeler (alçak güneş + yoğun sis) kayboldu. Su gökyüzünü düz beyaz yansıtıyor. |
| trail_house_side | İz ve kenar döküntüsü okunuyor. Sağ ön plan kenarı daha zengin. |
| trail_rear_entry | Daha sıcak, güneşli ve okunur. Kök yaması artık eğimde ama hâlâ hafif açık tonlu bir kabarıklık gibi. |
| trail_compression | En büyük kazanç: toprak izi, eğrelti grupları ve güneşli/gölgeli bantlar sıkışmayı okutuyor. |
| trail_release | Açılma daha aydınlık ve okunur. Ön plandaki eğrelti hâlâ fazla parlak ve doymuş. Bir kaya güneşte çok açık tonlu okunuyor. |
| uphill_lookback | Esasen yalnızca ışık değişti. Hafif iyileşme; ev ve orman arası katmanlar korunuyor. |

### Gerçek yürüyüş (pure pursuit, yay 16→60 m, 33,4 s, 3 pan, sabit adım = aynı kare aynı oyun zamanı)

- `v7/video/vmp_walk_before_vs_trial3_part1.avi` ve `part2.avi`: GitHub 100 MB sınırı nedeniyle ikiye bölündü.
- `vmp_pan_{threshold,compression,release}_before_vs_trial3.avi`: ±100° bakış panları, sol/sağ dönüş.
- 4 saniyede bir örnek kare: `compare/iteration/walk_sheet_4s.jpg`.

Videolar **gerçek zamanlı izlenmedi**; değerlendirme 1 fps örneklerinden yapıldı.

### Kamera (oyuncu kamerası ile pawn arası mesafe, cm)

| Koşu | Medyan | p5 | Min | V0'a göre >25 cm kısalma |
|---|---|---|---|---|
| BEFORE | 193 | 177 | 171 | — |
| TRIAL2 | 190 | 170 | 168 | 16 tick, yay 42,2–42,9 m, en kötü 27 cm |
| TRIAL3 | 189 | 171 | 169 | 12 tick (0,4 s), yay 42,6–43,1 m, en kötü 26 cm |

Normal yürüyüşte kamera çekilmesi pratikte yok.

Duran istasyon compression_left90'da (kamera yokuşa bakıyor) mesafe 171'den 120 cm'ye iniyor. TRIAL'de 84, TRIAL2'de 104 idi. Kalan neden büyük olasılıkla Z3 dip taşı (`VMP_032`, kollara 1,76 m mesafede, sert, Visibility kanalını engelliyor). Çözüm: taşı ~0,6 m yukarı kaydırmak. Bu son düzeltme **uygulanmadı/test edilmedi**.

### Performans (CSV profiler, aynı makine, aynı yürüyüş; p50/p95 ms)

| Koşu | Kare | Oyun iş parçacığı | GPU | GPU belleği MB |
|---|---|---|---|---|
| walk BEFORE | 41,4 / 46,2 | 15,0 / 18,6 | 39,9 / 44,4 | 6348 |
| walk TRIAL3 | 42,1 / 45,9 | 12,8 / 13,8 | 40,5 / 44,1 | 6622 (+274) |
| istasyonlar V0 | 42,5 / 46,3 | 14,9 / 18,9 | 40,7 / 42,8 | 6363 |
| istasyonlar TRIAL3 | 42,3 / 46,7 | 13,3 / 14,2 | 40,7 / 42,9 | 6638 |

- V2 istasyonları 31,5 ms GPU ile açıkça daha ucuz. Nedeni muhtemelen ters yöndeki alçak güneşle değişen gölge maliyeti; seçilen yön bu değil.
- Oyun iş parçacığındaki düşüş bu değişiklikle açıklanmıyor; gürültü olarak kabul edin.
- Tablo: `v7/data/perf_table.txt`.

## 5. Ulaşılamayan / açık kalanlar (dürüst liste)

1. **Landscape malzemesi** hâlâ tek frekanslı. Decal'lar yalnızca patika şeridini çözüyor; yamaçların "yeşil halı" okuması sürüyor. Asıl kaldıraç malzeme katmanları (ıslak toprak / yosun / iğne yaprağı, eğime ve nem maskesine bağlı). Bu landscape malzemesi ve katman yazımı demek, kalıcı ve riskli bir değişiklik. Ayrı onay gerekiyor.
2. **Büyük kütle ve siluet düzeni** (kanopi boşlukları, büyük ağaç grupları, IFA yoğunluk yeniden dağıtımı) bu geçişte yapılmadı. Yalnızca yer seviyesi orta ve küçük kütleler eklendi.
3. **Gölet ışığı geriledi.** Tek bir global güneş/sis ayarı hem patika hem gölet için optimal değil. Seçenekler:
   - göleti V0 ayarında bırakmak (ışığı değiştirmeyip yalnızca çevre tasarımını almak);
   - gölet için yerel hacimsel sis ya da hüzme çözümü;
   - güneşi biraz alçaltmak (-30°).
4. **Karakter pozlaması**: beyaz gömlek 2600 lux altında kırpılmaya yakın. Pozlama telafisi ya da gömlek albedosu ayrıca ele alınmalı.
5. **Asset sınırları**: PineGroundRock güneşte çok açık tonlu; FernWild01 doymuş. Vendor orijinalleri değiştirilmedi (AGENTS). Gerekirse sahibi olduğumuz MI kopyalarıyla tonlanabilir.
6. compression_left90 dip taşı düzeltmesi test edilmedi.

## 6. Güvenlik ve geri alma

- **Manifest**: `vmp_map`, sha1 `70dd481aaab3…`, yedeği doğrulandı (`v7/data/manifest_vmp_map.json`).
- **Kilit**: aitool tek sahip; iş sonunda bırakıldı.
- **PIE kuralları**: yazma ve PIE işleri PIE sırasında başlatılmadı. Bir kez, salt-okunur bir ölçüm (`vmpcol`) yanlışlıkla yürüyüş PIE'si sırasında çalıştı ve boş döndü. Etkisi yok, ama kural ihlali olarak not ediyorum.
- **Son durum (editörden ölçüldü)**:
  - `VMP_` aktör sayısı 0;
  - ışık, gök ve sis değerleri orijinalle birebir;
  - dirty içerik paketi yok (ABP'ler temiz);
  - harita yalnızca bellekte dirty, içerik orijinal;
  - PIE kapalı.

  Haritayı **kaydetmeyin** ya da editör kapanırken "Don't Save" seçin; disk sürümü zaten orijinal.
- **Denemeyi yeniden kurmak**: `vmp_trial_chain3.sh` + `look_TRIAL2_req.py` ile yaklaşık 2 dakikada, kaydetmeden yeniden kurulabilir.

## 7. Kalıcı hale getirme: onay gerektirir (uygulanmadı)

Önerilen sıra:
1. Dip taşı düzeltmesi + gölet ışık kararı (yukarıdaki 3. madde).
2. Çevre öğelerini ayrı bir sublevel veya data layer'a kaydetmek (`L_GR_SphirusHouse_VMP`), ana haritaya gömmeden.
3. Işık değişikliği ayrı ve geri alınabilir bir adım olarak.
4. Bridge export + LATEST.json doğrulaması (AGENTS gereği).

Her adım manifest ve yedekle, ayrı onayla yapılır.

## Dosyalar

- `v7/stills/{V0,V1,V2,V3,TRIAL,TRIAL2,TRIAL3,walk_vmp_before,walk_vmp_trial3}`: ham oyuncu kamerası kareleri (JPEG q90, yalnızca yeniden kodlandı)
- `v7/compare/V0_vs_TRIAL3`: istasyon karşılaştırmaları
- `v7/compare/iteration`: varyant sayfası, TRIAL2 genel bakış, sorun kırpımları, lookat sayfaları, yürüyüş örnekleri
- `v7/video`: 5 AVI (MJPEG, yan yana, kare = oyun zamanı)
- `v7/data`:
  - perf JSON ve tablo, `walk_camdist.txt`;
  - istasyon ve yürüyüş logları;
  - spec'ler, build/remove kayıtları, look orijinal ve uygulanan değerleri;
  - area_probe, zincir çıktıları, manifest
- `v7/code`: istek sarmalayıcıları ve zincir betikleri. `tools/`: vmp_build, vmp_spec2, look_variant, pie_stations, walk_camdist, vmp_compare, pack_v7 vb.
