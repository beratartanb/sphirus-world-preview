# SPHIRUS — İlk oynanış alanının Pine Forest Pack referansıyla yeniden tasarımı (PFR, 2026-11-04)

Harita `L_GR_SphirusHouse` (UE 5.8.1), gerçek oyuncu kamerası (GraceRanger, sabit adım 30 FPS). Üretim kaynakları: **Pine Forest Pack** (Kaizen Digital Interactive) + **Environment_Set** (NatureManufacture, yalnız gerekli yerde). Bu rapor çalışma boyunca doldurulur; durum etiketleri PASS / FAIL / PARTIAL / REVIEW_REQUIRED / NOT_TESTED.

## 1. Doğrulama: doğru proje, harita, paketler (2026-11-04 21:13–21:55)

| Konu | Bulgu | Kanıt |
|---|---|---|
| Üretim haritası | `/Game/GraceRanger/Maps/L_GR_SphirusHouse` (DefaultEngine.ini GameDefaultMap + EditorStartupMap), diskte 2026-11-01 06:18, sha1 `6d3efa3a…`; yüklü alt seviyeler `L_GR_CurrentHouseContent`, `L_SphirusHouse_ASSET_YARD` | `Config/DefaultEngine.ini`, `recon/probe.json` |
| Dünya katmanının güncelliği | Canlı editörden alınan yükseklik haritası sha1 `207f04e4…` = 2026-10-31 XR anlık görüntüsü; foliage 57 bileşen / 8.305 instance; aktör 774 (XR5 ışığı dahil). XR2/XR4 dünya katmanları hiç kaydedilmemişti; yalnız XR5 ışığı üretimde | `recon/probe.json` (`same_as_xr_recon: true`) |
| Pine Forest Pack | Fab listesi `e19f63fc…`, satıcı **Kaizen Digital Interactive**, yayın 2026-04-15, güncelleme 2026-07-16, UE 5.2–5.8, fotogrametri, Nanite/Lumen. Kurulu kopya `Content/PineForestPack` (143 mesh, 172 materyal, `L_Showcase` 35 MB, `M_Landscape_PineForest` + 9 çim tipi + 6 LayerInfo) | tarayıcı (Fab), `ref/fab_gallery_urls.txt`, `recon/probe.json` |
| Environment_Set | Fab satıcı sayfası NatureManufacture "Environment Set" (295 yorum). Kurulu kopya `Content/Environment_Set` (köknar/kavak ağaçları, Big/Middle/Small kaya, 47 zemin MI, `Environment_Set_Map`). "Forest - Environment Set" ayrı üründür, kurulu değil | tarayıcı, dizin listesi |
| Kullanılan assetler | Haritadaki 57 foliage bileşeninin 36'sı PineForestPack, 9'u Fishermans_Cabin (köknar ×1.518, çalı ×604), 5'i Calysto (genç ladin ×404, saz), 3'ü OakForestEnv (meşe ×6, kök), 2'si Megascans, 1'i PN_coniferBushes (`Pine_08` ×35), 1'i Real_Ivy. Landscape materyali `MI_EX_Integration_Valley` → `M_EX_Integration_Floor` (otomatik 4 doku, **boya katmanı yok**; dokular `T_VMA_BG_*` Chapter01 arka plan setinden) | `recon/foliage.json`, `recon/probe2.json` |
| Kullanılmayan "latest" tuzakları | `Saved/ChatGPTBridge/latest` 2026-09-25 tarihli (eski); XR pub klasörleri yerelde yok (GitHub raporları okundu) | GitHub `chatgpt-bridge/reports/exterior-*` |

## 2. Referanslar ve seçilen ana atmosfer

Erişilebilenler: Fab galerisinin 26 görselinden 17'si tam boyutta incelendi (lightbox); kurulu `L_Showcase` haritası ayrı bir editör oturumunda açılıp 26 karede çekildi (`ref/showcase/*.png`, `ref/showcase_sheet_A/B.jpg`) ve ışık reçetesi okundu (`ref/showcase_info.json`, `ref/showcase/fog_probe.json`). Erişilemeyen / bakılmayan: Trailer 2K ve Walkthrough 1–2 videoları (izlenmedi); galerinin kalan 9 görseli; `L_Lighting_Cloudy/Overcast` alt seviyeleri showcase haritasına bağlı değil (yalnız Morning yüklü).

**Seçilen senaryo: showcase'in "Morning" ışığı** — alçak, hafif sıcak güneş (pitch −34°, yaw −55°), çok güçlü hacimsel saçılma (hüzmeler), yoğun ama hacimsel sis (0.03, albedo sıcak beyaz), Mie 0.17 ile sütlü derinlik, histogram pozlama, filmic 0.75/0.55/0.26, doygunluk 0.9, LUT_Daytime 0.8. Galerinin "sisli açıklık" ve "kahraman gövde" kareleri de bu koşulda. Çelişen koşullar (öğle tepe ışığı, kapalı gri) birleştirilmedi.

### Referansta gözlem → bizim alanda karar → doğrulama görüntüsü

| # | Referansta gözlem (showcase / galeri) | Bizim alanda uygulanan karar | Doğrulama görüntüsü |
|---|---|---|---|
| 1 | Kanopi tek aile: düz, yüksek çam gövdeleri (Pine01/02/03), seyrek alçak dal; 5/6/7 ve LowPoly varyantları orta kat | 1.518 Fishermans köknarı (10–12 m, sarı-yeşil) aynı yükseklik bandındaki PFP çamlarına çevrildi (Pine06, LowMed01/02, Pine05×0.7, Pine07×0.6, SonoTall); kanopi yalnız PFP | `cap/views_before` ↔ `cap/views_after` P0/P1/P2 ±90°, yürüyüş A |
| 2 | Alt kat: broadleaf fideler (SonoSapling 1–4 ≈1.800), SonoTree 3.5 m, genç çam | Calysto genç ladinin %65'i PFP juvenile/sapling/SonoTree'ye çevrildi; %35 koyu vurgu olarak kaldı | P2_rockshelf_L90, D10_climb_fwd |
| 3 | Zemin: iğne/kahverengi humus tabanı + yosun-yaprak halısı (~105 bin küçük yosun instance'ı) + yerel kök/kozalak/dal/mantar | **Planlanan** PFP landscape materyali + boyalı katman yolu UE 5.8 Python'da kapalı (TargetLayers salt okunur, §4). **Uygulanan:** sahipli otomatik landscape örneği PFP zemin taramalarıyla yeniden giydirildi (Forest = PineGround01 iğne tabanı, Grass = GroundForest01 humus; projeye ait 2K kopyalar), üstüne yosun cepleri, iğne kümeleri, kozalak, dal, döküntü kartları, mantar foliage olarak | P3_glade_arrive, P2_rockshelf_fwd, yürüyüş B zemin kareleri |
| 4 | Patika: sıkışmış toprak + yaprak döküntüsü, kenarı eğrelti/yosunla kesik, genişlik nefes alıyor | Decal şeritleri kaldırıldı; ana rotalar boyunca her 2,6–3,4 m'de PFP trail/ground patch mesh'leri (sıkışmış orta, düzensiz kenar), kenarlarda döküntü kümeleri | D08_narrows_fwd, P1_landing_fwd, top görünüm |
| 5 | Kaya: yosun başlıklı yuvarlak bloklar, dipte eğrelti; büyük kütleler (CliffRock/PineCliff) duvar gibi üst üste | Raf, halka ve çıkıntı kayaları PFP cliff ailesi, tek sahipli MI (`MI_EX_PF_Cliff`: serin tint, yosun ↑); 12 noktada 2–4'lü PineGroundRock grupları %30–45 gömülü; Environment_Set Big_Rock kaldırıldı | P2_rockshelf_fwd/L90, P1_landing_R90 |
| 6 | Devrik gövdelerde raf mantarı, kütük yığını, kökler | DeadTrunk04 küçük kütükler + yanlarında Mushroom01; x9 rüzgâr devrikleri korundu | D09_hollow_fwd, P3_glade_seat |
| 7 | Eğrelti yalnız nemli/gölgeli ceplerde, kaya diplerinde | Asit yeşili FernWild %50 azaltıldı; FernLong02 yalnız kaya diplerinde | P2_rockshelf_entry |
| 8 | Işık: hüzmeler kanopiden, sis derinliği katmanlıyor, gölgeler ezik değil | PF sabah yönü/rengi mevcut sahiplerde (güneş −30/−60, 1500 lux 5300 K), üç tur ölçüldü: p2/p3'ün yoğun sisi (0.018–0.022, opaklık 0.85) her şeyi boğdu; XR5 FINAL v2 berraklığı (sis 0.013, başlangıç 2 m, opaklık 0.6) + ılımlı hüzme (hacimsel 1.5) + tam doygunluk + +0.15 EV ile **p4 final** seçildi | `cap/cmp_look_p3`, `cap/cmp_look_p4`, `perf/exposure_p3_look.json`, `perf/exposure_p4_look.json`, §5 pozlama tablosu |
| 9 | Kahraman gövde: ön planda 1 m çapında gövde, sarmaşık/yosun | 6 kahraman Pine04 (×1.2–1.3) ev önü, iskele, raf girişi, açıklık arkası, sırt, kapı yanında (foliage instance) | P0_refuge_fwd, P1_landing_from_veranda |
| 10 | Su: karanlık, yüzeyde kırık parıltı, kıyıda ıslak çamur/yaprak | `MI_EX_Pond` (pürüzlülük 0.45, murk 5.5, dalga genliği 0.045, emilim 0.20/0.165/0.12); kıyı bandında sandal iskelesi, kıyı kayaları ve döküntü (WetPuddle katmanı boya yolu kapalı olduğu için yok) | P1_landing_boat, P2_rockshelf_R90 |

Referanstan alınmayan / kendi yorumum: dünya halkası, iki rota, ev–göl–orman hiyerarşisi (XR2 x9 iskeleti), açıklıktaki "fazla düzenli taş yayı" (Sphirus fısıltısı), ev önü ayak taşları. Bunlar paketin değil projenin kararı.

## 3. Mevcut alanın teşhisi (BEFORE, üretim haritası, gerçek oyuncu kamerası)

Kanıt: `cap/views_before/*.png` (39 istasyon), `cap/before_sheet_P0P1.jpg`, `cap/before_sheet_P2P3.jpg`, `cap/walk_beforeA_sheet.jpg`, `cap/walk_beforeB_sheet.jpg`, `cap/top_before/`.

Etkiye göre sıralı tespitler (her biri bir görüntüye bağlı):

| # | Tespit (görünen) | Görüntü | Neden hipotezi | Sınıf |
|---|---|---|---|---|
| 1 | Orman her yöne aynı: eşit aralıklı gövde galerisi, koru/açıklık/kenar hiyerarşisi yok; "demo" okunuyor | P2_rockshelf_L90, P3_glade_arrive, yürüyüş A f00902/f01353 | 7 m serpme, dünya halkası ve rotalar üretimde hiç yok (XR2 kaydedilmemiş) | YAPISAL |
| 2 | Zemin tek doku: tırmanışta biçilmiş çim gibi parlak yeşil "çayır", düzlükte olive-kahve tekrarlı doku; patika yalnız iz | yürüyüş B f01596–f02849, P2_rockshelf_L90, P1_landing_L90 | otomatik landscape materyali (`M_EX_Integration_Floor`, VMA arka plan dokuları), boya katmanı yok | MATERYAL/YAPISAL |
| 3 | Kanopi iki aile: sarı-yeşil köknar (Fishermans, 1.518) çam yeşiliyle çatışıyor; kamera sık sık köknar dallarının içinde | P1_landing_fwd, P2_rockshelf_entry, yürüyüş A f00451, B f00001 | tür listesi kararı verilmemiş; köknar 10–12 m ve kamera yüksekliğinde dallı | KOMPOZİSYON |
| 4 | Asit yeşili eğrelti kütleleri ve broadleaf çalı kameraya kapanıyor | P1_landing_back, P2_rockshelf_fwd, P2_rockshelf_exit_back | FernWild01 doygunluğu, yol kenarı çalı (Bush_02/03/06) | MATERYAL/MESAFE |
| 5 | Açıklık yok: P3 istasyonu alçak dallı çam kümesinin içinde (L90/R90/back dalların içinde) | P3_glade_L90/R90/back/seat | karşı kıyı terası ve meşe/taş yayı yalnız XR4 denemesinde vardı | YAPISAL |
| 6 | Kıyı: düz raf, sazlık yok, iskele/sandal yok; su yüzeyi gök parlaması | P1_landing_boat, P2_rockshelf_R90 | WetPuddle/kıyı bandı yok, x9 yer işaretleri kaydedilmemiş | YAPISAL |
| 7 | Ev önü: zemin düz çayır + eşit serpilmiş küçük bitki; sığınak anı kurulmamış | P0_refuge_house_back, P0_refuge_front_path | hiyerarşi yok (XR5 §7 #6) | KOMPOZİSYON |
| 8 | Işık: hüzmeler tek kare güzel ama rota boyunca zemin düz aydınlık; derinlik katmanı yalnız sisten | P1_landing_R90, yürüyüş A f01804 | XR5 FINAL v2 "gümüş" tabanı; PFP referansı daha koyu, daha hacimsel | IŞIK |
| 9 | Kamera engeli: açıklık girişinde kamera saça/gövdeye gömülü (yol kenarında büyük gövde) | yürüyüş A f02255/f02706 | rota A sonunda gövde/genç ağaç 1 m içinde | OYNANIŞ |
| 10 | P0_refuge istasyonu (700,1250) üretimde evin çatısına oturuyor (XR3 istasyon tanımı evin içinde) | P0_refuge_L90/R90/back | istasyon hatası; ev önü için D01_veranda ve house_back/front_path kullanılmalı | KANIT |

Omurga kararı: önce 1–2–5–6 (biçim ve zemin), sonra 3–4–7 (aile ve hiyerarşi), en son 8 (ışık) ve 9 (temizlik).

## 4. Uygulananlar (p1 → p2 → p3 → p4, hepsi tek kayıtta; 2026-11-04 22:21–23:40)

Yöntem: her tur `Tools/PineForestRedesign_20261104/pfr_design.py <tur>` ile çevrimdışı tasarlandı (`design/<tur>/*.json`), kapılı editör koşucusunda (`pfr_apply.py`, manifest `pfr_world`) belleğe uygulandı, aynı 39 istasyon + iki rota yürüyüşüyle ölçüldü; p4 sonunda tek seferde kaydedildi (`promote_pfr.py`), editör kapatılıp **diskten yeniden açılarak** son doğrulama seti alındı (§5–6). Ev iç/dış içeriği, girişler, hikâye nesneleri ve alt seviyeler değişmedi; ev yeri değişmedi (gerek görülmedi); göl yüzeyi büyütülmedi.

| Alan | Yapılan | Dosya / kanıt |
|---|---|---|
| Arazi (makro) | 2026-10-31 XR2 x9 yükseklik haritası (dünya halkası, ev tümseği, havza, sırt, geçit) üretim landscape'ine içe aktarıldı; geri okuma örneklerle doğrulandı | `design/p1/apply_apply.json` ("terrain written and verified"), `cap/top_before` ↔ `cap/top_final` |
| Kanopi | 1.518 Fishermans köknarı yükseklik bandına göre PFP çamlarına çevrildi (Pine06 / LowMed01-02 / Pine05 ×0.6–0.8 / Pine07 / SonoTall; ev önü hattında Pine03 "TallFront" veya kaldırıldı); genç ladinin %65'i PFP juvenile / sapling / SonoTree; 6 kahraman Pine04 | `pfr_palette.py` FIR_SWAP / YOUNG_SWAP, `design/p4/foliage_p4.json` |
| Ev önü görüş hattı (p2) | Ev→su ve kıyı→ev hatlarının 5,2 m içindeki genç çam/çalı (7 + 16) ve yeni çalı/fidelerin 3,8 m içindekiler kaldırıldı; sığınak "sessiz bölge" | `cap/cmp_p2/cmp_P0_refuge_house_back.jpg` (P1 kapalı → P2 açık) |
| Zemin | Landscape MI yeniden giydirildi: Forest = `T_EX_PF_PineGround01_*`, Grass = `T_EX_PF_GroundForest01_*` (projeye ait 2K kopyalar, `max_texture_size`), Sand/Cliff mevcut 2K VMA; tiling 420/440/400/600; renk ofsetleri PFP tabanına. Üstüne foliage: 16 yosun cebi (MossLeaf01-04, MossClump, p2 ×0.72), iğne kümeleri, kozalak (p2 0.85–1.25), dal, mantar, 950 döküntü kartı (p3: sahipli koyu `MI_EX_PF_DeadLeaves01/02`, FT override) | `design/p4/mats_p4.json`, `design/p4/newfol_p4.json`, `cap/cmp_p3/` |
| Patikalar | x9 decal şeritleri kaldırıldı; ana rotalar boyunca PFP TrailPatch01/02 + GroundPatch01/04 (2,6–3,4 m aralık, rota yönünde ±20–25°); ıslak çukurda PineStone04 ×0.55 basamak taşları; görünmez, yalnız pawn'ı tutan su-geçiş duvarları korundu | `design/p4/newfol_p4.json`, yürüyüş A f02997 |
| Kaya | Raf/çıkıntı/halka kütleleri PFP cliff ailesi, tek sahipli `MI_EX_PF_Cliff` (p2: parlaklık 0.8, serin tint, yosun 0.9); 12 noktada ana blok + parçalar (p2, sıra yok), kaya dibinde FernLong02; taş yayı r 4,2 m ×0.85 yarı gömülü; Environment_Set Big_Rock gizlendi | `design/p4/spawn_p4.json` (258 `PFR_*` aktör, 4 gizli) |
| Kıyı | Sandal iskelesi, kıyı kayaları, su kenarı döküntüsü; `MI_EX_Pond` koyu/mat değerler | P1_landing_boat, P1_landing_R90 |
| Işık (p4 final) | Güneş −30/−60, 1500 lux, 5300 K, kaynak açısı 1.4, hacimsel 1.5; gök 1.3; sis 0.013 / düşüş 0.2 / başlangıç 200 / opaklık 0.6 / hacimsel sönüm 1.2 / albedo 235-226-212; Mie 0.035, anizotropi 0.4; PP: beyaz 6000 K, doygunluk 1.0, kontrast 1.06, filmic 0.8/0.55/0.26, bloom 0.35, vinyet 0.4, pozlama −0.45 EV | `design/p4/look_p4.json`, önceki değerler `design/look_backup_original.json` |

**Kapalı yol (dürüst):** PFP landscape materyaline geçip Forest/GroundPath/ForestField/WetPuddle katmanlarını boyamak UE 5.8 Python'da yapılamadı — `Landscape.target_layers` salt okunur, LayerInfo ataması yalnız Landscape modu arayüzünden; `land_trial.py` denemesi geri alındı, yeniden giydirme yolu seçildi. Kullanıcı bir kez Landscape modunda 6 PFP LayerInfo'sunu atarsa boya yolu (`paint_masks.py`) açılır.

**Performans düzeltmesi (p2):** p1'de 12 satıcı 4K taraması doku havuzunu 77–323 MB aşırdı (her PIE karesinde kırmızı "texture pool exhausted" uyarısı); p2'de yalnız iki baskın set, 2K sahipli kopya olarak kaldı (§6).

## 5. Önce/sonra ve referans karşılaştırması

Tüm FINAL kareleri kaydedilmiş haritanın **diskten yeniden açılmış** editör oturumundan (pfr_04, 2026-11-04 23:44–23:58), BEFORE ile aynı istasyon/poz/FOV/çözünürlük/kalite ayarlarında (PIE, HighResShot 1920×1080, gerçek GraceRanger kamerası, sabit adım 30). Işık ve pozlama bilinçli olarak değişti (§4 p4); karşılaştırmalar bunu içerir.

Kanıt: `cap/cmp_final_required/cmp_sheet.jpg` (zorunlu 7 bakış + 3 ek), `cap/cmp_final/sheet_P0P1.jpg`, `sheet_P2P3.jpg`, `sheet_D.jpg` (39 istasyon, ±90° ve geri bakışlar dahil), `cap/cmp_top/cmp_sheet.jpg` (üstten / eğik yerleşim), `cap/ref_vs_final/cmp_sheet.jpg` (referans ↔ final, 6 çift), ara turlar `cap/cmp_p2/`, `cap/cmp_p3/`, `cap/cmp_look_p3/`, `cap/cmp_look_p4/`; yürüyüş videoları `video/routeA_before_after_part*.avi`, `video/routeB_before_after_part*.avi` (BEFORE | FINAL yan yana, gerçek hız, aynı kare = aynı oyun zamanı).

| Zorunlu bakış | İstasyon | BEFORE → FINAL (görünen) | Durum |
|---|---|---|---|
| 1 Evden çıkış | P0_refuge_front_path | Kameranın önündeki köknar/fide duvarı gitti; su, sandal iskelesi ve iğne/döküntü zemin eğimle aşağıda okunuyor | PASS |
| 2 Eve yaklaşma | P0_refuge_house_back | Veranda tam okunur; ön bahçe koyu toprak + koyu döküntü + basamak taşları (p1'deki genç çam perdesi p2'de temizlendi) | PASS |
| 3 Evden suya iniş | P1_landing_from_veranda | Ortadaki genç çam kaldırıldı; su yüzeyi, sandal, kıyı kayaları ve kütük görünür | PASS |
| 4 Kıyıdan eve / ormana | P1_landing_back, P1_landing_fwd | Asit yeşili eğrelti duvarı yerine gövdeler, kaya dibi eğreltisi, döküntü; ileri bakışta köknar dalı yerine yosunlu kaya kütlesi | PASS |
| 5 Ana orman patikası | P2_rockshelf_fwd, D08_narrows_fwd | Kameraya kapanan çalı yerine yosunlu uçurum kütlesi + iğne zemin; D08'de alt kat yeşillendi, sol önde fide kameraya yakın | PASS / PARTIAL (D08) |
| 6 Ağaçlar arasından geri bakış | P3_glade_fwd, D11_saddle_fwd | Ortadaki genç çam gitti, ev gölün karşısında okunuyor; sırtta PFP çamları + yeşil alt kat | PASS |
| 7 Arka orman bağlantısı | D07_gate_fwd | PFP çalıları + döküntü; değişim ılımlı (kapı fenerinin görünürlüğü korundu) | PASS (ılımlı) |

Pozlama (ortalama parlaklık 0–255 / beyaz% / siyah% / doygunluk; `perf/exposure_before_final.json`, `perf/exposure_showcase.json`):

| Set | Ortalama | P0 | P1 | P2 | P3 |
|---|---|---|---|---|---|
| BEFORE (39) | 76 / 0.22 / 0.83 / 0.259 | 75 / 0.253 | 71 / 0.259 | 72 / 0.249 | 74 / 0.266 |
| FINAL (39) | 80 / 0.30 / 0.11 / 0.263 | 75 / 0.244 | 76 / 0.285 | 75 / 0.233 | 79 / 0.175 |
| Referans L_Showcase (26 kare) | 79 / 0.05 / 0.72 / 0.363 | — | — | — | — |

Okuma: parlaklık referansla aynı banda geldi, ezik siyah oranı düştü; **doygunluk referansın altında kaldı** (0.26 ↔ 0.36). Fark içerik kaynaklı: referansın zemini yeşil sarmaşık/yosun halısı (~105 bin instance), bizimki kahverengi iğne/döküntü tabanı + 16 yosun cebi (bellek bütçesi, §6). Referans çiftlerinde (`cap/ref_vs_final`) kaya kütlesi, ışık yönü, döküntü zemini ve kaya grupları yakın; yeşil zemin halısı, berrak mavi-yeşil su ve referansın daha soğuk-nötr ışığı bizde yok (sıcak sabah hüzmesi tercih edildi, §2).

Üstten (`cap/cmp_top`): ev yeri ve göl yüzeyi aynı; kanopi tek aile; ev çevresinde SonoTree/fide kümeleri kuş bakışı açık yeşil lekeler olarak okunuyor (oyuncu kamerasından değil).

## 6. Oynanış kontrolleri ve performans

**Yürüyüş (gerçek karakter, kaydedilmiş harita, diskten açılmış oturum):** rota A ev önü → iskele → kaya rafı → açıklık (101 m, 10/10 adım, hata yok, 3.221 kare) ve rota B arka kapı → sırt (89 m, 10/10, 2.849 kare) BEFORE ile aynı tohum/çizgi/hızda tamamlandı (`cap/walk_finalA|B/trailwalk_log.json`). 39 istasyonda ileri/±90°/geri bakışlar alındı; BEFORE'da kameranın köknar dalı veya çalı içinde kaldığı istasyonlar (P1_landing_fwd, P2_rockshelf_entry, P2_rockshelf_fwd, D02_houseSE_fwd) FINAL'de açık. Çarpışma: kaya/uçurum kütleleri BlockAll, yumuşak örtü çarpışmasız, su-geçiş duvarları görünmez ve yalnız pawn'ı tutar; sandal ve kıyı kayaları yürünebilir kıyı şeridini daraltmıyor (rota A f00215). **NOT_TESTED:** ev içi etkileşimler/kapı tetikleyicileri bu geçişte çalıştırılmadı — ev alt seviyeleri (`L_GR_CurrentHouseContent`, `L_SphirusHouse_ASSET_YARD`) hiç kirlenmedi ve kaydedilmedi, yani yapısal olarak değişmedi; PlayerStart'tan PIE başlangıcı iki yürüyüşte de çalıştı.

**Performans** (csvprofile, 1907×928 editör PIE, sabit adım 30, aynı rotalar; BEFORE 22:01 pfr_02 oturumu, FINAL 23:50 pfr_04 temiz oturumu; `perf/before_A|B.json`, `perf/final_A|B.json`):

| Rota | Set | Kare p50 / p95 ms | Game thread p50 | GPU p50 / p95 ms | VRAM kullanılan / bütçe MB |
|---|---|---|---|---|---|
| A (iskele→açıklık) | BEFORE | 35.7 / 47.5 | 13.5 | 33.8 / 45.1 | 6590 / 7045 |
| A | FINAL | 36.3 / 50.2 | 21.5 | 35.0 / 48.4 | 6946 / 7040 |
| B (kapı→sırt) | BEFORE | 39.9 / 44.9 | 13.2 | 38.0 / 43.0 | 6610 / 7045 |
| B | FINAL | 39.6 / 45.3 | 21.0 | 38.3 / 43.2 | 6933 / 7040 |

Okuma: kare süresi GPU'ya bağlı ve pratikte değişmedi (A +0.6 ms p50 / +2.7 ms p95, B −0.3 / +0.4). Game thread istatistiğindeki artış bekleme kaynaklı: thread'in kendi işi (Exclusive/GameThread toplamı) 35.9 → 34.6 ms, en büyük tekil artış UI +1.7, TickActors +1.7, Animation +1.2 ms (`perf/final_A.json` kaynağı CSV). **VRAM +350 MB** (6946 / 7040 bütçe, 94 MB pay): yeni PFP foliage dokuları (pakette 325 doku, 567 MB yerleşik, 49'u 4K) — p1'deki 12 adet 4K landscape taraması p2'de 2K sahipli kopyaya indirildiği hâlde pay dar.

Doku akış havuzu (`r.Streaming.PoolSize` 1000 MB, `ListTextures` yerleşik 1401 MB / diskte 4092 MB, 1267 doku; `perf/vram_probe_final.json`, `Saved/Profiling/MemReports/…23.57.17`): "texture pool exhausted" kırmızı uyarısı örneklenen yürüyüş karelerinde BEFORE A 3/16, B 12/16; FINAL A 0/16, B 14/16 — rota B'deki havuz taşması **bu geçişten önce de vardı**, rota A'da kayboldu. En büyük yerleşik dokular bu alanın dışında: `AAMS/Demo/UI/AAMS2_0_Logo` 6829×3076 sıkıştırmasız **3 × 83 MB**, Calysto `T_Black_Spruce_Leaves_01_B/ORD` 4K, `OakForestEnv/Landscape/T_Snow_N` 4K, Fishermans `T_Boat_DO` 4K. Ölçülen darboğazda yapılan düzeltme: landscape dokuları 2K sahipli kopya (p2). Önerilen, bu geçişin kapsamı dışında kalan düzeltme: AAMS demo logosunun referansını kaldırmak (~250 MB) ve OakForestEnv landscape dokularının yüklenme nedenini kapatmak; ardından havuz 1500 MB'a çıkarılabilir.

Donanım: RTX 4060 Laptop 8 GB, i7-13650HX, 32 GB (`hardware-quality-baseline-20261013`); GPU sınırlı; projede tanımlı sayısal bütçe yok → göreli karşılaştırma raporlanır.

## 7. Kalan sorunlar ve dürüst kabul

Görsel onay kullanıcıya aittir; aşağıdakiler benim gördüğüm açıklar.

1. **Zemin kimliği referansın gerisinde (en büyük açık):** referansın yeşil sarmaşık/yosun halısı ve boyalı patika katmanları bizde yok — PFP landscape materyali + boya yolu 5.8 Python'da kapalı (§4), yosun halısı bellek payı yüzünden 16 cep ile sınırlı. Doygunluk 0.26 ↔ 0.36. Kullanıcı Landscape modunda 6 PFP LayerInfo'sunu bir kez atarsa `paint_masks.py` boya yolu açılır; VRAM payı (94 MB) ek 4K içerik kaldırmaz, önce §6'daki dış tüketiciler alınmalı. REVIEW_REQUIRED.
2. **Rota B doku havuzu taşması** geçiş öncesinden kalma; kırmızı uyarı editör PIE'de görünür, bazı dokular düşük mip'te kalabilir. Kapsam dışı düzeltme önerisi §6. PARTIAL.
3. Yosun cepleri yakın mesafede yer yer "yapıştırılmış" okunuyor (P3_glade_back); ıslak çukurdaki basamak taşları fazla düzenli (rota A f02997). PARTIAL.
4. Ev önünden suya bakışta su yüzeyinde parlak güneş yansıma lekesi (P0_refuge_front_path, P1_landing_from_veranda): güneş yaw'ı veya su pürüzlülüğü ile yumuşatılabilir; XR5 ışığında koyuydu (`cap/cmp_look_p4`). REVIEW_REQUIRED.
5. D08_narrows_fwd'de sol önde fide kameraya yakın; D13_backyard'da yeni çalılar evin cephesine yakın. PARTIAL.
6. Kuş bakışı SonoTree/fide kümeleri açık yeşil lekeler (`cap/cmp_top`); oyuncu kamerasında sorun değil. NOT: tasarım kararı, isteğe bağlı seyreltme.
7. Göl çizgisi yeniden şekillendirilmedi (göl büyütme yasağı; yalnız kıyı giydirildi); ev yeri değişmedi. Bilinçli.
8. Ev içi etkileşimler NOT_TESTED (§6).
9. Kayıt adımında `MI_EX_PF_Landscape` (kullanılmayan deneme varlığı) bellekten silindi, kaydedilmedi; editör kapanışı bu kirli kayıt yüzünden 240 s sonra zorla kapatıldı (harita zaten kaydedilmişti). Diskten yeniden açılış iki kez doğrulandı: pfr_04 (39 istasyon + 2 yürüyüş) ve pfr_05 (yükleme sonrası kirli paket yok → Bridge dışa aktarımı); pfr_04'teki kirli harita bayrağı üst görünüm kamerasının spawn/destroy'undan geliyordu, yükleme kaynaklı değil.
10. Fab galerisinin 9 görseli ve 3 videosu incelenmedi (§2).

Kabul (kullanıcının 7 sorusuna benim cevabım, kanıtla): evden çıkış/yaklaşma/iniş/kıyı/patika/geri bakış/arka bağlantı — 7 bakışın 6'sı PASS, D08 PARTIAL (§5 tablo); oynanış rotaları gerçek karakterle PASS; performans değişmedi, bellek payı dar (PARTIAL); referansa görsel yakınlık kaya/ışık/döküntüde yakın, zemin halısında uzak (REVIEW_REQUIRED).

## 9. Teslimat dosyaları (hepsi `Saved/Codex/PineForestRedesign_20261104/`)

| Teslimat | Yol |
|---|---|
| Kaydedilmiş üretim haritası | `Content/GraceRanger/Maps/L_GR_SphirusHouse.umap` (2026-11-04 23:35, sha1 `0e550a00…`) + 52 sahipli paket (`Content/GraceRanger/Environment/Exterior20260921/{Materials,Foliage,Textures}/*_PF_*`, düzenlenen `MI_EX_Pond`, `MI_EX_Integration_Valley`, `MI_PR_*`) |
| Geri alma noktası | `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/pfr_world.json` + yedek kopyalar (§8) |
| Referanslar, seçilen atmosfer | `ref/showcase/*.png`, `ref/showcase_sheet_A/B.jpg`, `ref/showcase_info.json`, `ref/fab_gallery_urls.txt`, `ref/board_sheet.jpg`; §2 tablosu |
| Üstten yerleşim önce/sonra | `cap/cmp_top/cmp_sheet.jpg` (`cap/top_before`, `cap/top_final`) |
| Önce/sonra, temsilî noktalar | `cap/cmp_final_required/cmp_sheet.jpg` (zorunlu bakışlar), `cap/cmp_final/sheet_*.jpg` (39 istasyon), tek satırlar `cap/cmp_final/cmp_<istasyon>.jpg` |
| Referans ↔ final yan yana | `cap/ref_vs_final/cmp_sheet.jpg` |
| Sürekli oynanış kaydı (ev–kıyı–orman, gerçek karakter) | `video/routeA_before_after_part1..4.avi` (107 s, BEFORE \| FINAL yan yana, 1664×472, gerçek hız 15 fps = her 2. kare), `video/routeB_before_after_part1..4.avi` (95 s); parçalar ≤ 92 MB (GitHub sınırı); kaynak kareler `cap/walk_before*/frames/`, `cap/walk_final*/frames/` (MJPEG, sabit adım 30 fps) |
| Performans | `perf/before_A|B.json`, `perf/final_A|B.json`, ara turlar `perf/after_p1_*`, `perf/after_p2_*`, pozlama `perf/exposure_*.json`, bellek `perf/vram_probe_final.json` |
| Tasarım/uygulama kaydı | `design/p1..p4/*.json` (plan, foliage, yeni tipler, aktörler, materyaller, ışık, apply/promote çıktıları), `recon/*.json` |
| Araçlar | `Tools/PineForestRedesign_20261104/` (`pfr_design.py`, `pfr_apply.py`, `promote_pfr.py`, `run_round.sh`, `run_p3.sh`, `run_final.sh`, `restart_editor.sh`, `export_bridge_pfr.py`, `make_videos.sh`, `ref_pairs.sh`, `compare_pairs.ps1`, `sheet.ps1`, probe'lar) |
| ChatGPTBridge / GitHub | Bridge dışa aktarımı run `2026-11-05_001038_629813_e45c5f` (18 standart bakış, bu geçişin gerçek oyuncu-kamera pozlarından; temiz oturum pfr_05, kirli paket yok; `Saved/ChatGPTBridge/latest`, kontakt `cap/bridge_sheet.jpg`); GitHub `beratartanb/sphirus-world-preview` (**herkese açık** repo, AGENTS.md gereği): release `chatgpt-world-latest` (15 dosya) + connector aynası `chatgpt-bridge/latest/` (28 dosya) 2026-11-05 00:14; `LATEST.json` run_id doğrulaması aşağıda |

## 8. Geri alma

Harita ve dokunulan 16 proje sahipli materyal örneği `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/pfr_world/` altında sha1 doğrulamalı yedekli (`pfr_world.json`); yeni oluşturulan paketler (`MI_EX_PF_*`, `FT_EX_PF_*`, `T_EX_PF_*`; manifestte "new") kayıt öncesi yoktu. Editör kapalıyken yedekleri aynı yollara kopyalamak ve "new" paketleri silmek üretim haritasını 2026-11-01 06:18 hâline (sha1 `6d3efa3a…`) döndürür. Satıcı paketlerine (PineForestPack, Environment_Set, Fishermans_Cabin, Calysto…) hiçbir yazma yapılmadı; bellekte kirlenen `MI_FallenNeedle` kayıt adımında diskten yeniden yüklendi (`design/p4/promote.json`).
