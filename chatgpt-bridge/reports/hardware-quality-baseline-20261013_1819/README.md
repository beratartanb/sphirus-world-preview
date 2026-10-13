# Donanım – Görsel Kalite – Karakter Kontrolü: Başlangıç Kaydı (2026-10-13 18:19–20:35)

Bu, **ölçüm ve kayıt** görevidir. Hiçbir sahne, karakter, animasyon, Blueprint, materyal veya kalıcı proje ayarı değiştirilmedi (bkz. §10 koruma kontrolü). Yeni bilgisayarda bu klasöre dokunmayın; `REPRODUCE.md` ile yeni bir rapor oluşturup karşılaştırın.

Etiketler: **PASS / FAIL / PARTIAL / BLOCKED / NOT_TESTED / NOT_IMPLEMENTED** (`TEST_STATUS.md`). Teknik sonuçlar sanatsal/hissel onay **değildir**. Görsel değerlendirmeler gözlemdir; nihai sanat onayı kullanıcıya aittir.


> **Yayın notu:** GitHub kopyası yalnız belgeleri, özet ölçüm tablolarını (`raw/measurements.csv` vb.), küçültülmüş JPG görüntüleri ve küçük GIF klipleri içerir. Ham CSV profilleri, tam telemetri JSON'ları, tam çözünürlüklü PNG'ler, klip kareleri, config kopyaları ve koruma manifestleri yerel klasörde `Saved/ChatGPTBridge/reports/hardware-quality-baseline-20261013_1819/` altında kalır.

---

## 0. Yönetici özeti (kanıta dayalı)

1. **Başlıca sınır: GPU işlem gücü.** Ölçülen her ağır sahnede GPU süresi kare süresine eşit (fark ≤ 1 ms). GPU kullanımı %97–98. Game thread ise editörde 9.6–10 ms, PIE'de 14–17 ms, standalone oyunda 6.5 ms ölçüldü. Standalone 1920×1080 (A, arka yokuş) sonuçları: **30.6 FPS, GPU 31.8 ms, game thread 6.5 ms**.
2. **GPU yükünün büyük kısmı bitki gölgeleri; bu kısım proje tarafında da azaltılabilir.**
   - En pahalı geçiş `ShadowDepths` (Virtual Shadow Map): A'da GPU süresinin %47–56'sı.
   - Bitkiler gizlendiğinde (yalnız tanı) GPU süresi 18.5 → 7.4 ms (ev→göl) ve 23.2 → 6.5 ms (arka yokuş) oluyor.
   - VSM kapatıldığında hızlanma yok (18.5 → 20.7 ms). Sorun VSM'nin kendisi değil, bitkinin gölgeye yazılma biçimi.
   - Bu, donanımdan bağımsız bir **optimizasyon fırsatı**dır (WPO, gölge önbelleği geçersizleşmesi, yoğun maskeli bitki). Bu görevde düzeltilmedi.
3. **Çözünürlük etkisi güçlü.** Standalone 1080p'de iç çözünürlük %50 olunca GPU süresi 31.8 → 15.5 ms, FPS 30.6 → 61.2.
4. **VRAM (8 GB, masaüstüyle paylaşılan) hedef kalitede editör/PIE iş akışını sınırlıyor.**
   - C profilinde PIE'de yerel VRAM kullanımı bütçeyi aştı: uygulamalar açıkken 7.5 / 6.57 GB, kapalıyken 7.6 / 7.08 GB.
   - Rotalarda 30–40 saniyede 42–341 adet >50 ms takılma ve p99 59–88 ms ölçüldü.
   - Aynı C profili standalone oyunda 6.0 / 7.04 GB'a sığdı; takılma görülmedi, ama hızı 22.5 FPS.
   - Masaüstü uygulamaları (Photoshop, Edge, 6× Fotoğraflar, vb.) GPU'da ~2.5 GB tutuyordu. Kapandıklarında UE'nin VRAM bütçesi 6.57 → 7.09 GB'a çıktı ve A rotaları %11–12 hızlandı (34.5 → 38.4 FPS, 38.3 → 43.0 FPS).
5. **Hedef kalite (C) görüntüyü az değiştiriyor ama pahalı.**
   - C, mevcut özelliklerle sinematik ölçeklenebilirlik demektir (doku hariç).
   - Maliyet: editörde GPU +%35–61 (+10.5–12.5 ms), standalone'da GPU 31.8 → 43.6 ms (+%37), VRAM +~0.8–0.9 GB.
   - Görüntü farkı küçük: ışık/GI tonu, yansıma ve sis huzmelerinde. Yeni bitki veya içerik görünür hâle gelmedi.
   - Su yüzeyindeki şerit/dikdörtgen yansıma deseni A'da da var, C'de belirginleşiyor. Bu bir sahne/yansıma sorunu, donanım değil.
6. **Hareket/kamera sorunlarının çoğu yükten bağımsız.**
   - Aynı girdiler hafif ortamda (60 FPS), 30 FPS sınırlı hafif ortamda ve evde (A ~47–54 FPS, C ~27–33 FPS) aynı sonucu verdi. Bu iki konuyu kapsıyor: yerinde dönüşte üst gövde öne bükülmesi ve dönüş eşiği, hız/durma değerleri.
   - Sprint + hızlı sağ–sol girişinde "donma" yalnız evde görüldü. Sebep bir bahçe kapısı direğine (`AD_Life_GatePostN`) çarpma ve geri itilme montajıdır. Hafif ortamda donma yok.
   - Kamera bitkinin içinden geçip karakteri yapraklarla örtebiliyor (klip kanıtı).
7. **Yeni donanım bu eksikleri kendiliğinden çözmez:** su yansıma deseni, kamera–bitki örtmesi, yerinde dönüş postürü, sahne/rota kompozisyonu, performans için yapılmış geçmiş doku/WPO kısıtlamaları (§5).

---

## 1. Kapsam ve koşullar
- **Proje:** `sphirus.uproject`, UE 5.8.1 (CL 56057345), Development Editor, DX12 SM6, harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse` (+ `L_SphirusHouse_ASSET_YARD`, `L_GR_CurrentHouseContent`), 768 aktör, 8.305 foliage örneği.
- **Karakter zinciri** (canlı PIE'de okundu):
  - GameMode `BP_GM_GR_GraceRanger`.
  - Pawn mesh `CharacterMesh0` = gizli AAMS "TravistyGames_Mascot" sürücü iskeleti.
  - Görünen gövde `Manny` bileşeninde `SKM_MH_MainCharacter_BodyMesh`, yüz `SKM_MH_MainCharacter_FaceMesh` (MetaHuman).
  - Kamera spring arm hedef boyu 300 cm (iç/dış aynı).
- **Editör görüntü alanı:** 1523×587 px (≈0.89 MP). Yaygın 1920×1080 oyun penceresinin %43'ü. Editör/PIE sayıları bu boyuttadır.
- **Standalone:** `-game -windowed` (cook edilmemiş, Development), editör kapalı.
- **Faz koşulu:**
  - **Faz 1** (18:20–19:17): masaüstü uygulamaları açık.
  - **Faz 2** (19:17 sonrası): Photoshop/Edge/Fotoğraflar kapalı. Bu değişikliği ben yapmadım; bellek kaydından tespit edildi.
  - Faz 2'de editör çizim çağrılarının (DrawCalls) ~2.700 → ~540'a ve SlateUI GPU maliyetinin 1.08 → 0.32 ms'ye düştüğü de görüldü. Editör pencere düzeni de değişmiş olabilir; kontrolsüz koşul olarak işaretlendi.
- **Isınma:** her editör/PIE ölçümünden önce 8–20 s, standalone'da ilk 1800 kare hariç. Açılış: 18:20:14 → motor 18:22:38 → harita + runner 18:24:21 (≈4 dk 7 s). Shader derlemesi: editör log sayacına göre açılış ve ilk deneme sırasında (18:31'e kadar) 2.023 shader derlendi; ölçümlerin geri kalan 1.5 saatinde yalnız +51 shader (C, VSM-kapalı tanısı ve lab için yeni permütasyonlar). ShaderCompileWorker süreçleri havuzda açık kalabildiği için süreç sayısı tek başına derleme kanıtı değildir. Tekrarlı ölçümlerin ±%1 tutarlılığı kararlı durumu destekler.
- **Kayıt yükü:** performans ölçümü ile video/görüntü kaydı ayrı geçişlerde yapıldı. Klipler t.MaxFPS 30 ile ayrı bir PIE oturumunda alındı.

## 2. Donanım envanteri (özet; ayrıntı `INVENTORY.md`)
| Bileşen | Değer |
|---|---|
| Sistem | ASUS ROG Strix G614JV (dizüstü), Windows 11 Pro 10.0.26300, güç planı "Turbo" |
| CPU | Intel Core i7-13650HX, 14 çekirdek / 20 iş parçacığı |
| GPU (Unreal'ın kullandığı) | NVIDIA GeForce RTX 4060 Laptop GPU, sürücü 616.56 (2026-08-20). Ekranı bu GPU sürüyor (D3D12 adapter 0, 1 çıkış). Güç sınırı 140 W (varsayılan 100 W). PCIe 4.0 x8 |
| Fiziksel VRAM | 8188 MiB (nvidia-smi); D3D12 "dedicated" 7956 MB; paylaşılan sistem belleği 16192 MB |
| UE VRAM bütçesi (OS) | Faz 1 ≈ 6.51–6.58 GB, Faz 2 ≈ 7.04–7.19 GB (`GPUMem/LocalBudgetMB`) |
| Masaüstü VRAM kullanımı (UE kapalıyken) | 2.5 GB (Photoshop, Fotoğraflar, Edge, vb. açıkken) |
| RAM | 32 GB (2×16 GB DDR5-4800). Faz 1'de UE yokken boş fiziksel ~12.5 GB, commit boşluğu ~13.4 GB. Pagefile otomatik (20 → 62 GB'a büyüdü) |
| UE süreci | Editör boşta: WS 9.5 GB / private 16.2 GB. Oturum sonunda private 23.8 GB. C sırasında sistemde boş RAM 0.8–1.9 GB'a indi |
| Disk | Crucial P3 1 TB NVMe (proje + DDC aynı diskte). C: 930 GB, test başında 176.7 GB boş |
| Ekran | 1920×1200 @165 Hz, DPI %125 |
| Isı/güç (ölçüm sırasında) | GPU 72–87 °C, 80–100 W, 2520 MHz (yük altında sabit). Yazılımsal termal yavaşlatma bayrağı 85–87 °C'de örneklerin ~%4'ünde aktif (saat 2400–2500 MHz). Donanımsal termal/güç kısıtı bayrağı görülmedi |

## 3. Proje/ölçüm ayarları (A = mevcut)
- Scalability: sg.* = 3 (Epic), ResolutionQuality 0 (= varsayılan).
- Çözünürlük: r.ScreenPercentage 0 (varsayılan); editör görüntü alanı %100 (`r.Editor.Viewport.ScreenPercentage 100`); PIE A'da %100 olduğu kontrol oturumuyla doğrulandı.
- Yükseltme/AA: TSR (AA yöntemi 4; geçmiş %200).
- Dinamik çözünürlük kapalı, VSync kapalı, t.MaxFPS 0, GameUserSettings FrameRateLimit 0.
- Işık/gölge: Lumen GI + yansıma, Lumen HW ray tracing açık, VSM açık (proje Epic gölge SMRT 12/8), Nanite açık.
- Doku/bitki: streaming pool 1000 MB (LimitPoolSizeToVRAM 0), foliage.DensityScale 1, r.ViewDistanceScale 1.
- **PIE dünyası "max tick rate 60" ile başlıyor.** Bu ~60 FPS'te bir sınır oluşturuyor. Standalone'da 0 (sınırsız). t.MaxFPS 200 ile PIE B 64 FPS'e çıktı ve orada game thread sınırına (~15.6 ms) takıldı.
- 215 cvar'lık tam döküm `inventory/cvars_A_initial.json` dosyasında. A'dan farklı her ayar `raw/static_C_r1.json → cvars_applied` alanında (C için 74 cvar).

## 4. Profil farkları (A/B/C/D)
| Profil | Ne değişti | Not |
|---|---|---|
| **A** | Hiçbir şey | Gerçek çalışma koşulu |
| **B** | Yalnız iç çözünürlük %50 (`r.ScreenPercentage 50`; PIE'de `r.Editor.Viewport.OverridePIEScreenPercentage 0`) | **Editör görüntü alanında uygulanamadı:** GPU geçiş maliyetleri A ile birebir aynı kaldı. Bu yüzden B yalnız PIE ve standalone'da geçerli |
| **C** | sg.GI/Reflection/Shadow/ViewDistance/AA/PostProcess/Effects/Shading/Foliage/Landscape = 4 (Cinematic) | Texture 3'te kaldı: Cinematic, streaming havuzunu 3000 MB yapıyor, 8 GB'lık paylaşılan kartta güvenli değil. İçerik/yerleşim/ışık/zaman/pozlama değişmedi. Öne çıkan değişiklikler: Lumen screen probe 16→8 downsample, octahedron 8→16, VSM SMRT 16/8 ve 8192 sayfa, volumetric fog grid 8→4, r.ViewDistanceScale 1→10, SSR 3→4, GTAO 2→4 açı |
| **D** | Hafif test haritası `/Game/GraceRanger/Tests/L_GR_MovementLab` (proje içi, 2026-09-14; düz zemin, koridor/oda duvarları, rampa, 16 cm basamaklı merdiven, alçak tavan) | Aynı GameMode/karakter/kamera. Üretim haritası değiştirilmedi; geçiş öncesi "kirli paket yok" doğrulandı |

## 5. Geçmişte performans için kaliteden vazgeçilmiş mi?
Ayrıntı: `HISTORY_QUALITY_REDUCTIONS.md`. Kısaca:
- **Evet, ve bugünkü haritayı etkileyenler var** (09-22/23):
  - 48 çevre dokusu 4K/8K → 2048, çim/sazlık 1024.
  - Ana çamlar ve diğer ağaçlarda WPO bitişi 11000 → 6500.
  - Zemin örtüsünde WPO 3200 → 1800, cull 2600 → 2200.
  - Genç çam doku sınırları; çalı kabuk POM'u kapalı.
  - Dış çamlarda WPO yok, 430 m cull.
  - VT havuz boyutları config'te sabitlendi.
- **Gerekçe:**
  - Bir kısmı açıkça "optimization/streaming/VRAM" diye belgelenmiş.
  - WoodlandRefuge WPO/cull değişikliğinin yazılı gerekçesi yok; donanım kaynaklı diye sunulmamalı.
  - Foliage 9.316 → 2.560 azaltması sanat/okunabilirlik gerekçeli (yan etkisi draw call düşüşü).
- **Kalıcılaşmış geçici ayar bulunmadı:** canlı cvar'lar Epic, t.MaxFPS 0, ScreenPercentage 0.
- Geçmiş eksik (git yok, sohbetler yok). **Bu, başka kısıtlama yapılmadığını kanıtlamaz.**

## 6. Kontrollü performans sonuçları
Tam tablo: `raw/measurements.csv` (107 satır; test kimliği, saat, faz, tekrar, görüntü alanı). Ham CSV'ler yerelde `raw/csv/`.

### 6.1 Editör görüntü alanı, statik noktalar (1523×587, Faz 1, 3 tekrar, ortalama)
| Nokta | A FPS | A GPU ms | A p99 ms | C FPS | C GPU ms | C p99 ms | VRAM A→C (GB) |
|---|---|---|---|---|---|---|---|
| P1 ev içi | 55.6 | 17.2 | 19.4 | 35.0 | 27.8 | 30.7 | 5.26 → 6.13 |
| P2 evden göle | 36.9 | 26.3 | 28.4 | 26.6 | 37.0 | 40.3 | 5.24 → 6.07 |
| P3 göl kıyısı | 35.0 | 27.8 | 30.1 | 25.6 | 38.3 | 40.6 | 5.23 → 6.06 |
| P4 arka yokuş/orman yolu | 29.4 | 33.3 | 35.5 | 21.4 | 46.0 | 49.2 | 5.24 → 6.05 |
| P5 yokuştan eve bakış | 29.0 | 33.8 | 36.3 | 21.2 | 46.3 | 49.6 | 5.37 → 6.30 |
- Tekrar farkı ±%1. Game thread 9.6–10.1 ms (editör UI'si dahil).
- Editörde bütçe ≈6.54–6.57 GB. C, bu bütçenin %92–96'sında.

### 6.2 PIE (gerçek oyun modu, karakter + kamera, 1523×587)
| | Faz | A | B (%50) | C |
|---|---|---|---|---|
| R1 ev içi → veranda → göl kıyısı (31.7 s, 3×) | 1 | **34.5 FPS**, p99 38.6 ms, takılma 1–4 | 56.7 FPS (60 sınırı), p99 21.5 | **19.4 FPS**, p99 84.7 ms, **208–238 takılma** |
| R2 ev yanı → arka bahçe → yokuş yolu (39.6 s, 3×) | 1 | **38.3 FPS**, p99 35.9 | 56.8 FPS (60 sınırı), p99 21.6 | **20.7 FPS**, p99 77.3, **237–341 takılma** |
| R1 | 2 | 38.4 FPS, p99 31.6 | 59.8 (t.MaxFPS 200, GT sınırı) | 23.5 FPS, p99 66.0, 109–177 takılma |
| R2 | 2 | 43.0 FPS, p99 30.5 | — | 25.1 FPS, p99 59.3, 42–154 takılma |
| VRAM yerel kullanılan / bütçe (rota) | 1 | 6.39–6.41 / 6.57 GB | 6.40 / 6.57 | **7.48–7.51 / 6.57–6.63 (aşım)** |
| | 2 | 6.60 / 7.09 | — | **7.58–7.59 / 7.08 (aşım)** |

PIE statik noktalarında GPU (Faz 1, A → C): P2 20.0 → 29.3 ms, P4 25.0 → 35.8 ms.

### 6.3 Kontroller ve tanılar (PIE, Faz 2)
| Ölçüm | P2 evden göle GPU ms | P4 arka yokuş GPU ms | Anlamı |
|---|---|---|---|
| A (referans) | 18.5 | 23.2 | — |
| Override kapalı + %100 | 18.5 | 23.2 | PIE A gerçekten %100 iç çözünürlük |
| t.MaxFPS 200 | 18.5 | 23.2 | A bu noktalarda sınıra takılmıyor |
| **Bitki gizli** (`ShowFlag.InstancedFoliage 0`) | **7.4** | **6.5** | GPU'nun %60–72'si bitki kaynaklı |
| VSM kapalı (CSM'e düşer) | 20.7 | 24.9 | VSM'yi kapatmak hızlandırmıyor |
| B + t.MaxFPS 200 | 9.8 (64 FPS) | 11.9 (64 FPS) | Kare = game thread 15.6 ms. Bunun ~9 ms'si editör UI'si; oyun mantığı (anim 1.6, aktör tick 1.6, CMC 0.1–0.3) ~4 ms |

### 6.4 Editörden bağımsız standalone (`-game`, cook edilmemiş Development, P4 civarı oyuncu kamerası, Faz 2)
| Profil | Çözünürlük | FPS | Kare ms (p95/p99/maks) | GPU ms | GT ms | ShadowDepths ms | VRAM / bütçe |
|---|---|---|---|---|---|---|---|
| A | 1920×1080 | **30.6** | 32.7 (33.3 / 33.7 / 49.5) | 31.8 | 6.5 | 17.8 | 5.22 / 7.19 GB |
| B (%50) | 1920×1080 | **61.2** | 16.3 (17.0 / 17.4 / 79.9) | 15.5 | 6.5 | 7.3 | 5.13 / 7.19 |
| C | 1920×1080 | **22.5** | 44.5 (45.2 / 45.5 / 48.3) | 43.6 | 6.6 | 23.6 | 6.00 / 7.04 |
| A | 1523×587 | 33.6 | 29.8 (30.5 / 30.9 / 68.5) | 29.0 | 6.6 | 16.0 | 5.02 / 7.19 |
- Haritanın açılması 70–86 s sürdü; ilk 1800 karede (ısınma) 4–13 kare >50 ms, en uzunu 2.1–3.1 s.
- Standalone tek pozdur; rota değildir. Oyuncu `BugItGo` ile P4 yakınına ışınlandı ve kamera oyun kamerasıdır. PIE/editör statik poz kamerasıyla birebir aynı değil.
- **Paketli Development build ölçülmedi (BLOCKED):** projede paket/cook çıktısı ve paketleme yapılandırması (MapsToCook vb.) yok. Cook bu görevin kapsamı dışında.

## 7. Görüntü karşılaştırması (A ↔ C)
- Eşleştirilmiş görüntüler: `images/P{1..5}_*_{A,C}_r1.jpg` (yerelde PNG).
- Fark haritaları: `images/diff/*_A_vs_C_x4.jpg` (fark ×4).
- Gürültü tabanı: aynı ayarla ikinci çekim (`*_noise_*`). Editörde B uygulanmadığı için B çekimi fiilen A'nın ikinci çekimidir.
- Piksel istatistiği (ortalama |Δluma|, 0–255):

| Nokta | A–A gürültü | A–C | Yorum |
|---|---|---|---|
| P1 ev içi | 1.48 | 2.80 | İç mekânda çok küçük fark; C biraz daha aydınlık (88.2 → 89.9) |
| P2 evden göle | 3.32 | 7.73 | Farkın çoğu orta bant (su/kıyı): yansıma ve sis huzmeleri |
| P3 göl kıyısı | 2.95 | 8.77 | Su yüzeyi yansıması belirgin değişiyor |
| P4 arka yokuş | 9.29 | 12.19 | Gürültü yüksek (rüzgâr/WPO), C farkı gürültünün az üstünde |
| P5 eve bakış | 6.62 | 11.35 | Üst bant (taçlar/sis) |

Gözlemler:
- C'de **yeni bitki ya da içerik görünür hâle gelmedi.** r.ViewDistanceScale 10 bu kapalı orman görüşlerinde fark yaratmıyor; görüşler yakın kütlelerle kapanıyor.
- C, gölge yumuşaklığını, bitki içi GI tonunu ve sis huzmesi keskinliğini değiştiriyor. Su yüzeyinde **şerit/dikdörtgen yansıma deseni** A'da da (P2) var, C'de daha keskin.
- Estetik farkı yüzdeyle ifade etmiyorum. Yukarıdaki sayılar piksel istatistiğidir, kalite puanı değildir.

## 8. Hareket ve kamera (hafif ortam ↔ ev; ayrıntı `MOTION_CAMERA.md`)
Aynı sabit girdi dizileri (`motion_suite.py` M1–M9) dört koşulda koşturuldu. Gerçekleşen kare hızları ölçüldü; ağır çekim yok:
- Hafif ortam ~59–60 FPS.
- Hafif ortam t.MaxFPS 30 (gerçekleşen 29.9–30.0).
- Ev A 47–54 FPS.
- Ev C 27–33 FPS.

Telemetri hem gizli sürücü iskeletten hem görünen MetaHuman'dan alındı. Ayak kayması değerleri iki iskelette birbirine yakın çıktı.

Klipler (gerçek zamanlı, 30 FPS sınırlı kayıt geçişi): `clips/*.gif`.

## 9. Karakter, çevre ve oynanış (nitel; nihai onay kullanıcıda)
Ayrıntı: `CHARACTER_ENVIRONMENT_GAMEPLAY.md`.
- Karakter görüntüleri: `images/charshots_lab_char_*.jpg`.
- Onaylanmış bir referans bu görevde bulunamadı. Bu yüzden benzerlik puanı verilmedi.

## 10. Koruma kontrolü ve geri alınanlar
- **Content/Config/Plugins:** test öncesi/sonrası manifest 27.157 dosya, değişen/eklenen/silinen = **0** (`raw/preserve_manifest_diff.json`).
- **Config/*.ini:** başlangıç kopyasıyla birebir aynı.
- **Kirli paket:** tüm oturum boyunca hiç oluşmadı; harita geçişlerinden önce doğrulandı.
- **Cvar'lar:** her oturumdan sonra başlangıç dökümüne geri yazıldı; kapanışta fark 0 (`raw/final_editor_state.json`). PIE override cvar'ı 1'e döndü. bThrottleCPUWhenNotForeground eski değerine döndü.
- **EditorPerProjectUserSettings.ini** yalnız editör UI durumu nedeniyle değişti (son açılan haritalar, viewport kameraları). Editör kapandıktan sonra başlangıç kopyası geri yüklendi; birebir aynı olduğu doğrulandı.
- **Olay — yanlışlıkla üzerine yazılan dosya:** İlk karakter görüntüsü denemesinde HighResShot, proje yolundaki boşluk nedeniyle dosya adını kesti. Sonuç olarak `<kullanıcı>\OneDrive\Documents\Unreal.png` (oluşturulma 2026-09-25 21:47) **üzerine yazıldı**. Önceki içeriği bilinmiyor. OneDrive sürüm geçmişinden geri alınabilir; dosya silinmedi, bırakıldı. Araç düzeltildi (boşluksuz geçici yol).
- Yeni oluşturulanlar yalnızca bunlar: bu rapor klasörü, `Tools/HardwareQualityBaseline_20261013/` (salt ölçüm araçları), `Saved/Logs/HQB_*.log`, `Saved/Profiling/CSV` ve `Saved/Screenshots` altındaki yeni dosyalar, normal kapanışın yazdığı `Saved/Autosaves/PackageRestoreData.json` (`RestoreEnabled:false`, boş).

## 11. Net karar
**S1 – Başlıca sınır ne?**
**GPU işlem gücü**, ardından **VRAM kapasitesi (8 GB, masaüstüyle paylaşımlı)**, birlikte de **proje verimsizliği (bitki gölgesi)**. CPU, RAM ve disk birincil sınır değil:
- GPU: her ağır noktada GPU ms ≈ kare ms; %97–98 kullanım. 1080p A'da 30.6 FPS, %50'de 61.2 FPS.
- VRAM: C'de PIE aşımı ve yüzlerce takılma. Masaüstü uygulamaları kapanınca A rotaları +%11–12.
- Proje verimsizliği: bitki gizlenince GPU 23.2 → 6.5 ms.
- CPU: standalone game thread 6.5 ms (≈150 FPS tavanı). PIE'deki 15–17 ms'nin ~9 ms'si editör UI'si.
- RAM: 32 GB, editör oturumu 16 → 24 GB commit büyüdü. C sırasında boş RAM 0.8 GB'a düştü; yeni bilgisayarda izlenmeli ama birincil sınır değil.
- Disk: NVMe; ölçüm pencerelerinde streaming bekleme yok. 4 dk açılış ve ilk kare takılmaları ayrı kaydedildi.

**S2 – Hedef kalite açıldığında ne oluyor?**
- Görüntüde küçük fark: ışık/GI tonu, gölge yumuşaklığı, sis huzmesi, su yansıması. Yeni içerik görünmüyor.
- Performans:
  - Editörde GPU +10.5–12.5 ms (FPS 29–56 → 21–35).
  - Standalone 1080p'de 30.6 → 22.5 FPS.
  - PIE'de VRAM bütçe aşımıyla rota başına 42–341 takılma.

**S3 – Donanımdan bağımsız iş gerektirenler:**
- Bitki gölge maliyeti (WPO/VSM geçersizleşmesi, maskeli overdraw).
- Su yüzeyi şerit yansıması.
- Kamera–bitki çakışması (kamera yaprak içinden geçiyor; görüş trace'i çarpışmasız bitkiyi görmüyor).
- Yerinde dönüşte üst gövde öne bükülmesi ve dönüş eşiği (~130–170°, kamera dönüşünün ardından toplu dönüş montajı).
- Rota üzerindeki çarpışma engelleri (kapı direği sprintte geri itiyor).
- PostRain/Woodland dönemindeki doku/WPO kısıtlamalarının sanatsal etkisi.
- Hafif ortam zemininde doku geçiş sınırı (yalnız test haritası).
- Paketleme yapılandırmasının hiç olmaması.

**S4 – Şimdi bu bilgisayarda ilerletilecekler:**
- Bitki gölgesi/WPO optimizasyonu: ölçülebilir, A'da GPU'nun yarısından fazlası.
- Su yansıma deseni.
- Kamera çarpışma/görünürlük politikası.
- Yerinde dönüş postürü ve eşik ayarı, hareket hissi.
- Rota/kompozisyon işleri.
- Paketleme yapılandırması.

Bunların hepsi düşük-orta kalite profilinde, iç çözünürlük düşürülerek test edilebilir. Hareket sonuçları 30–60 FPS arasında aynı çıktığı için hissel testler bu makinede geçerli.

**Yükseltme sonrasına bırakılacaklar:**
- Cinematic GI/gölge/yansıma ile final görsel değerlendirme.
- Doku sınırlarının (2K/1K) geri yükseltilmesi.
- Yüksek çözünürlüklü uzun yakalamalar, C profilinde editör/PIE iş akışı.

**S5 – Yükseltmede öncelik:**
1. **Daha güçlü GPU.** Ölçüm: GPU-bound, %50 çözünürlükte 2× FPS, C'de +%37 GPU süresi.
2. **Daha fazla VRAM (12 GB ve üstü).** Ölçüm: C/PIE bütçe aşımı ve takılmalar; masaüstü uygulamalarının 2.5 GB tutması.
3. **RAM 32 GB → daha fazla olması faydalı ama ikincil.** Ölçüm: C sırasında 0.8 GB boş, editör commit 24 GB.

CPU yükseltmesi bu ölçümlerle desteklenmiyor. **Yeni bilgisayar için FPS tahmini veya hızlanma oranı verilmiyor;** aynı testleri `REPRODUCE.md` ile ölçün. Arada proje değişirse önce manifest farkına bakın.

## 12. Yapılamayan / eksik testler (özet; tam liste `TEST_STATUS.md`)
- **Paketli Development build:** BLOCKED (paket yapılandırması/cook yok).
- **Editör görüntü alanında B:** BLOCKED (cvar uygulanmıyor; PIE ve standalone'da yapıldı).
- **VRAM'in fiziksel ayrımı:** UE'nin yerel kullanımı/bütçesi ve nvidia-smi toplamı kaydedildi; süreç başına GPU belleği "N/A". WDDM, süreç bazında göstermiyor.
- **Ev içi merdiven, alçak tavan, kapı geçişinde ayrıntılı kamera ölçümü:** PARTIAL. Kapı geçişi yalnız R1 rotasında; merdiven yalnız hafif ortamda.
- **Oynanış:** Etkileşimler (kapı açma, merdiven/tavan arası, vent, çekmece), yeniden başlatma ve kayıt NOT_TESTED. Kayıt sistemi NOT_IMPLEMENTED (yalnız AAMS demo SaveGame var). Maske/algı/görev fikirleri NOT_IMPLEMENTED.
- **Sıcaklık/güç:** nvidia-smi sensörleri var. CPU sıcaklığı/güç kısıtı için sensör verisi alınmadı; CPU termali hakkında hüküm yok.
