# Sphirus World: AI araç değerlendirmesi v2. Düzeltmeler, T1 ölçümü, kamera ve değerlendirme sistemi (2026-10-31)

v1 raporu (`REPORT_AI_TOOLING.md`) değiştirilmedi; bu dosya onu düzeltir ve gerçek test sonuçlarını ekler.

Etiketler:
- **DOĞRULANDI:** bu oturumda ölçüldü ya da kaynakta okundu.
- **DOĞRULANAMADI:** erişilemedi.
- **NOT_TESTED:** onay gerekiyor ya da kapsam dışı.

Tüm sayılar `t1/data/*.json` dosyalarından geliyor; tablolar `t1/TABLES_T1.md` içinde, kodla üretildi.

**Bu turda neye dokunuldu, neye dokunulmadı:**
- Editör **yeniden başlatılmadı**. Asset, harita, ayar veya yapılandırma değişmedi; kurulum yapılmadı.
- Editörde yalnız `measure` ve `control` türünde işler çalıştı, kilit sahibi `aitool` idi. Bu iş türlerinde runner kayıt işlemlerini engelliyor.
- Kamera görüş açısı geçici olarak değişti ve sonunda geri yüklendi: konum, FOV 90, game view kapalı.
- Aktör transform hash'i önce ve sonra aynı.
- Yeni dosyalar yalnız `Tools/AIToolingEval_20261031/` ve `Saved/Codex/AIToolingEval_20261031/` altında.

---

## 1. Unreal Sensei: "How to Make Games in Unreal Engine 5 with AI" (28.10.2026)

| Bilgi | Değer | Nasıl elde edildi |
|---|---|---|
| Video | https://www.youtube.com/watch?v=R_HFCPd5eAw | Sayfa üst verisi okundu |
| Yayın | 2026-10-28, 12:30 PDT. PLAYBOARD'da 2026-10-29 görünüyor (saat dilimi farkı) | Sayfa üst verisi okundu |
| Süre | 2:21:51 | Sayfa üst verisi okundu |
| Bölümler | 0:00 Intro, 6:07 MCP, 21:17 C++ Set Up, 33:10 AI Memory and Effort, 44:11 Control with Properties, 1:01:08 Blueprint Relationship, 1:14:06 kurs reklamı, 1:19:11 AI Generated Art, 1:30:30 Blob!, 1:38:18 Game Logic, 2:03:21 Level Design, 2:09:49 User Interface, 2:15:02 Final Game | Açıklama okundu |
| Açıklamadaki iddia | Başlangıç seviyesi; Unreal seçilen bir AI'ya bağlanıyor (Claude ve ChatGPT anılıyor); C++ üretiliyor; AI'nın güçlü ve zayıf yanları anlatılıyor | Açıklama okundu |
| Motor | UE 5.8: sitedeki "AI Game Starter Assets" sayfası bu videoya "Unreal Engine 5.8 AI game tutorial" diye bağlantı veriyor | Yalnız sitenin kendi sayfasından; **videoda doğrulanamadı** |

**DOĞRULANAMADI:**
- MCP bölümünde hangi sunucunun kullanıldığı: Epic'in Unreal MCP'si mi, bir topluluk sunucusu mu?
- Claude Code, Cursor ya da masaüstü uygulamasından hangisinin kullanıldığı.
- Editörde AI'nın tam olarak ne yaptığı: aktör, Blueprint, malzeme, ışık, ekran görüntüsü, görsel geri bildirim.
- Sonuçların nasıl doğrulandığı ve belirtilen somut sınırlamalar.

**Neden doğrulanamadı:**
- Transkript alınamadı: doğrudan altyazı isteği 404 ve "Precondition check failed" döndü; üçüncü taraf transkript siteleri 403 verdi.
- Yerleşik tarayıcıda transkript paneli yüklenmedi; oynatıcı "Altyazılar kullanılamıyor" gösterdi.
- Videoyu izlemedim.

**Bizim için çıkan sonuç (yalnız bölüm başlıklarından):**
- Yaklaşım C++ üretimi ve "property'lerle kontrol" üzerine kurulu.
- Bizim proje Blueprint-only; MCP'yi zaten içeriyor ve kapılı bir runner ile çalışıyor.
- Videodan alınabilecek somut bir araç ya da güvenlik pratiği bulunamadı. Bölüm içerikleri görülmeden daha fazlası söylenemez.

## 2. MCP: `RefreshTools` (DOĞRULANDI) ve v1 düzeltmesi

**Kaynakta okunan** (`ModelContextProtocolModule.cpp`, `ModelContextProtocolEditor.cpp`, UE 5.8.1):
- `ModelContextProtocol.RefreshTools` bir konsol komutu (`ECVF_Cheat`). Yaptıkları:
  - MCP modülündeki tool listesini boşaltır.
  - `OnRefreshTools` olayını yayar. Editör modülü bunu dinler ve ToolsetRegistry'deki mevcut araç setlerinden adaptörleri yeniden kaydeder.
  - Sunucu açıksa istemcilere `notifications/tools/list_changed` bildirimi planlar.
- Çalışma sırasında kaydedilen yeni araç setleri zaten otomatik yeniden kaydı tetikliyor (`OnToolsetRegistered`).
- RefreshTools **yeni eklenti yüklemez**: yeni açılan bir eklenti için editör yine yeniden başlatılmalı.

**Canlı test** (`refresh_probe.py`, control işi, sunucu kapalıyken):
- Komut çalıştı. Logda 00:05:34 UTC'de yeni bir satır çıktı: "Tool search enabled: registered 3 meta-tools (53 toolsets…)".
- Araç seti sayısı önce 53, sonra 53; liste aynı.
- Motor içi araç çağrısı (`ToolsetRegistry.ExecuteTool`) yenilemeden sonra da çalıştı.
- **NOT_TESTED:** istemcinin `list_changed` bildirimini alması. Bunun için sunucuyu başlatmak gerekiyor ve onay bekliyor.

**v1 düzeltmesi:** v1'de "yeni araç için editör yeniden başlatılmalı" demiştim. Doğrusu:
- Eklenti düzeyinde: evet, yeniden başlatma gerekir.
- Çalışma sırasında eklenen araç setleri ve eskimiş şema önbelleği: RefreshTools yeterli.

**Yeni ve önemli bulgu (DOĞRULANDI):** MCP sunucusu açılmadan, araç setlerinin fonksiyonları mevcut kapılı runner içinden çağrılabiliyor.
- `EditorAppToolset.CaptureViewport` 3 görünümde 0.36–0.39 s'de döndü.
- Dönen veri: PNG, kamera konumu, dönüşü ve FOV. İstenen pozla float hassasiyetinde eşleşiyor.
- Bu yol manifest, kilit ve PIE kapılarının içinde kalıyor. 8000 portunu açmak çekim döngüsü için **gerekli değil**.

## 3. SSIM ile FLIP: anlamları düzeltildi

v1'de "aynı görüntü = 1.0" ikisi için de yazılmıştı. Bu FLIP için yanlış.

| | SSIM | NVIDIA FLIP (ꟻLIP) |
|---|---|---|
| Türü | **Benzerlik** indeksi | **Fark (hata)** ölçüsü |
| Aynı görüntü | 1.0. Azaldıkça benzerlik azalır; 0'ın altına inebilir | 0.0. 1'e yaklaştıkça fark büyür |
| Neye bakar | Pencerelerde parlaklık, kontrast ve yapı korelasyonu. Çoğunlukla gri tonlu; renk ve izleme mesafesi modeli yok | İki görüntü art arda değiştirildiğinde ("flip") bir izleyicinin göreceği farkı modeller: insan kontrast duyarlılığı, renk, kenar ve nokta farkları. Görme açısı başına piksel (PPD) ayarı var |
| Çıktı | Ortalama skor + SSIM haritası | Piksel başına hata haritası + ortalama / dağılım. LDR ve HDR sürümleri var |
| Sahnemizde kullanımı | Yapısal değişiklik: nesne kayboldu, yer değiştirdi, kamera kaydı | "İzleyici bu farkı görür mü?" ve nerede: gölge/ışık kayması, renk, gürültü |
| Ölçmediği şey | Sinematik kalite, referansa benzerlik | Sinematik kalite, referansa benzerlik |
| Durum | Bu turda Blender'ın Python'u (numpy 2.3.4) ile hesaplandı | **NOT_TESTED:** resmi NVlabs uygulamasının kurulumu onay bekliyor |

**Düzeltilmiş T4 ölçütü:**
- SSIM(aynı) = 1.0.
- FLIP(aynı) = 0.0.
- Bilinen bir değişiklik SSIM'i düşürmeli, FLIP'i yükseltmeli; ikisi de T1 gürültü tabanının dışına çıkmalı.

## 4. T1: aynı oturumda çekim tekrarlanabilirliği (DOĞRULANDI)

**Düzen** (`t1_cap.py`):
- Çalışan editör: V2.40 oturumu, `L_GR_SphirusHouse`, UE 5.8.1, viewport 1741×922.
- Çekim çağrısı: Bridge'in de kullandığı `take_high_res_screenshot(1920,1080, delay 0.2, force_game_view)`.
- Görünümler: ev önü, göl ve orman (Bridge `camera_plan.json`, 2026-09-25: `06_house_exterior`, `17_shoreline_gameplay`, `09_house_to_forest`).
- **Faz A:** kamera taşındıktan sonra 0.5 / 2.5 / 6 / 10 / 12 / 14 s'de çekim. 10–14 s çekimleri kamera hiç oynatılmadan alınan statik tekrarlar.
- **Faz B:** kamera götürülüp geri getirildi, 10 s beklendi, 2 tur daha çekildi.
- Toplam 24 çekim + 3 `CaptureViewport`.
- Ayarlar `t1/data/t1_log.json` içinde: tüm sg.* değerleri 3, AA 4 (TSR), Lumen GI/yansıma, VSM açık, HW RT 1. Sahnede histogram otomatik pozlama (bias −0.65, EV100 −2…16).
- PNG'den ham veriye dönüşüm bağımsız bir PNG çözücüsüyle kontrol edildi: fark 0, alfa her yerde 255.

### 4.1 Tam çözünürlük: Unreal'ın kendi karşılaştırma kuralıyla tekrarlar başarısız

Değerler: SSIM / UE-Low global fark / sonuç. Kopyalar `TABLES_T1.md`'de.

| Görünüm | Statik, poz oturduktan sonra | Geri dönüş (kamera götürülüp getirildi) |
|---|---|---|
| Ev önü | 0.864 / %9.8 / FAIL | 0.776–0.788 / %14.8–15.4 / FAIL |
| Göl | 0.920–0.926 / %3.6–4.0 / FAIL | 0.913–0.928 / %3.5–4.2 / FAIL |
| Orman | 0.861–0.897 / %8.6–11.4 / FAIL | 0.821–0.836 / %14.0–15.4 / FAIL |
| Kendisiyle (kontrol) | 1.000 / %0 / PASS | — |

- **Değişmemiş sahnenin 33 çiftinin 33'ü de** Unreal'ın Low toleransından geçemedi: global ≤ 0.02, yerel ≤ 0.10, kenar yumuşatma muafiyeti açık.
- Isı haritaları farkın nerede toplandığını gösteriyor:
  - rüzgârla sallanan bitki örtüsü ve ağaç tepeleri;
  - yerdeki güneş benekleri;
  - ince doku kenarları (TSR alt piksel titremesi).
  - Örnekler: `t1/heatmaps/`, `t1/sheets/forest_revisit_r2_vs_r3.png`.

### 4.2 Poz oturması

Ortalama parlaklık (`luma_per_shot.json`):
- Göl ve orman 6 s'den sonra ±0.3 içinde sabit.
- Ev önünde ilk çekim çağrısı 3.6 s sürdü. Bu yüzden ev önünün 0.5 / 2.5 / 6 s etiketli çekimleri aslında 4.6 / 8.2 / 9.1 s'de alındı.
- Ev önünün ortalama parlaklığı 10.9 s ile 13.3 s arasında 85.3'ten 88.1'e çıktı, sonra sabitlendi.
- **Kural:** her görünümde en az 12 s bekle ve oturumun ilk çekimini at.

### 4.3 Ölçeği küçültülmüş metrikler: gürültü tabanı

| Görünüm | Statik: SSIM d16 / karo maks | Geri dönüş: SSIM d16 / karo maks | Global parlaklık farkı |
|---|---|---|---|
| Ev önü | 0.994 / 2.7 | 0.981–0.983 / 4.0–7.4 | ≤ 0.21 |
| Göl | 0.997 / 1.1–1.2 | 0.996–0.997 / 1.3–3.2 | ≤ 0.06 |
| Orman | 0.992–0.994 / 2.2–2.6 | 0.957–0.969 / 6.7–13.6 | ≤ 0.23 |

Karo maks: 16×9 ızgarada karo ortalama parlaklık farkının en büyüğü, 0–255 ölçeğinde.

### 4.4 Sentetik değişiklik duyarlılığı

Değişiklikler yalnız görüntü üzerinde yapıldı; sahne değişmedi. Eşik = geri dönüş gürültüsünün en kötüsü × 1.5:
- karo eşiği: ev 11.1, göl 4.8, orman 20.3;
- global eşik: 1.0;
- `ssim_d8` eşiği: gürültü minimumunun altı.

| Değişiklik | Ev önü | Göl | Orman |
|---|---|---|---|
| 160 px alan %20 karartıldı (karo maks) | 13.0, **yakalandı** (pay az) | 17.6, **yakalandı** | 14.3, **kaçtı** |
| 200 px alan yerine başka parça konuldu (karo maks) | 17.5, **yakalandı** | 36.7, **yakalandı** | 12.1, **kaçtı** |
| Kamera 3 px kaydı (`ssim_d8`; gürültü min ev 0.946, göl 0.990, orman 0.934) | 0.905, **yakalandı** | 0.944, **yakalandı** | 0.895, **yakalandı** |
| Pozlama +%5 (global) | +4.4, **yakalandı** | +4.4, **yakalandı** | +4.4, **yakalandı** |

**T1 sonucu:**
- Tam çözünürlüklü piksel karşılaştırması (ve Unreal'ın kuralı) bu sahnede regresyon testi olarak **kullanılamaz**.
- Ölçeği küçültülmüş ve karo tabanlı ölçüm:
  - göl ve ev önünde bugünden kullanılabilir;
  - ormanda yerel değişiklikleri yakalayamıyor, çünkü rüzgâr ve güneş benekleri gürültüsü çok büyük.
- Ormanın yakalanabilmesi için görüntünün deterministik olması gerekir (bkz. 6. bölüm).
- **NOT_TESTED:** editör yeniden açıldıktan sonra aynı test (T1 ikinci bölüm; yeniden başlatma onay gerektiriyor).

**Ek gözlem:** Çalışan editörde V2.40 oturumundan kalma iki ABP paketi dirty durumda:
- `/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching`
- `ABP_GR_MotionMatchingBase`

Bu turdan önce de sonra da aynıydılar; dokunulmadı, kaydedilmedi. Biri editörde "Save All" yaparsa bunlar da kaydedilir. Bu bir risk.

## 5. Unreal'ın Screenshot Comparison sistemi işimizi görür mü?

UE 5.8.1 kaynağından okunan:
- **Karar mekanizması** (`ImageComparer.cpp`): piksel toleransı. Low ön ayarı: kanal başına 16, parlaklık 16. Karar, toleransı aşan piksel oranına göre: global ≤ %2, en kötü blok (10×10 ızgara) ≤ %10.
- **Kenar yumuşatma muafiyeti:** 3×3 komşulukta en az iki birebir aynı renkli komşusu olmayan piksel "kenar yumuşatılmış" sayılıyor. Bitki dolu sahnemizde bu, piksellerin %92–100'ü. Sonuçta test, neredeyse yalnız parlaklık farkı ≤ 16 kontrolüne dönüşüyor.
- **SSIM:** motorda bir SSIM fonksiyonu var (8×8 pencere), ama `ScreenShotManager.cpp`'de yorum satırı; geçti/kaldı kararında kullanılmıyor.
- **Varsayılan çekim seçenekleri** (`FAutomationScreenshotOptions`): gürültülü özellikler kapatılıyor (AA, otomatik pozlama, motion blur, SSR) ve **tonemapping kapatılıyor**. Bu yüzden karşılaştırılan görüntü oyuncunun gördüğü görüntü değil.
- **Altyapı:**
  - Doğru görüntü (ground truth) proje içinde tutuluyor; Screenshot Browser'da onaylanıyor; platform/RHI başına ayrı.
  - Çekim için bir FunctionalScreenshotTest aktörü (haritaya eklenir) ya da otomasyon testi gerekiyor.
  - `CompareImageAgainstReference` yalnız `GIsAutomationTesting` iken çalışıyor.

**Değerlendirme:**
- Kendi kuralının birebir taklidi, tonemapped oyun görüntüsünde T1'in 33 çiftinin 33'ünde FAIL verdi.
- **Sinematik değerlendirme için uygun değil:** tonemapping ve pozlama kapalı.
- **Teknik regresyon için:** ancak ayrı bir test haritası veya alt seviyede, rüzgâr ve zaman sabitlenip gürültülü özellikler kapatılmışken CI kapısı olarak denenebilir. Bu asset/harita gerektirir; onay bekliyor; **NOT_TESTED**.
- **Bugünkü işimiz için:** kendi ölçümlerimiz (4.3 ve 4.4) daha uygun.

## 6. Ev önü, göl ve orman için kamera ve değerlendirme sistemi (tasarım)

Ayrıntılar `CAMERA_EVAL_SYSTEM.md` ve `cameras_env_v1.json` içinde. Özet:

**İki kamera sınıfı, iki ayrı ölçüm:**

**R: teknik regresyon kameraları.**
- Editör viewport pozları; PIE yok.
- JSON'da sabit poz, FOV, 1920×1080, game view; çekim runner ile.
- Ölçülen: karo, d16 SSIM, global parlaklık ve (onaydan sonra) FLIP haritası. Eşikler görünüm başına T1 gürültü tabanından.
- Sonuç: PASS / FLAG. Bu bir görsel kabul değil.

**P: oyuncu kamerası istasyonları.**
- Gerçek karakter ve GraceRanger kamerası, PIE'de.
- İstasyonlar level-art skill'indeki P00–P11 kimlikleriyle: P00 ev önü, P11 orman hacmi, göl manzarası.
- Her istasyonda ileri, ±90° ve geriye bakış + 5–15 s yürüyüş.
- **Sinematik kaliteye yaklaşım** burada ölçülür:
  - referanslarla ilke karşılaştırması: `reference-comparison.md`'deki 10 soru (derinlik katmanları, orta plan doluluğu, ön plan, ışığın formu desteklemesi…);
  - `visual-acceptance.md`'deki Tier 0–4 ölçeği;
  - açıklayıcı sayısal göstergeler: değer grupları, parlaklık yüzdelikleri, kontrast, doygunluk. Bunlar kalite puanı değildir.
- Puanlamayı iki kez, sırası karıştırılmış olarak ben yaparım. Son kabul kullanıcıda.

**Referans görüntüler yerelde kalır** (telif); Bridge'e yalnız bizim çekimlerimiz ve türetilmiş sayılar gider.

**Not:** T1'de kullanılan Bridge pozları otomatik üretilmiş geometrik adaylar. Örneğin göl görünümünde ön planda bir genç ağaç ve dallar kadrajı kapatıyor. Skill kurallarına göre bunlar kabul kamerası değildir.

## 7. Doğrulanmış sonuçlar, eksikler, riskler

**DOĞRULANDI**
- Aynı oturumdaki gürültü tabanı ölçüldü (bölüm 4).
- Unreal'ın kuralı bu sahnede FAIL veriyor.
- Ölçeği küçültülmüş metrikler göl ve ev önünde çalışıyor.
- RefreshTools çalışıyor.
- `CaptureViewport` MCP sunucusu olmadan runner içinden çalışıyor.
- Görüntüleri dönüştürme yolu kayıpsız.
- Kurulum gerektirmeyen ölçüm ortamı var: Blender Python + numpy.
- Viewport geri yüklendi; aktörler değişmedi.

**Eksik / NOT_TESTED**
- FLIP (kurulum onayı).
- Editör yeniden açıldıktan sonra T1 (yeniden başlatma onayı).
- Rüzgâr ve zaman sabitlemesi; Movie Render Queue ile birikimli çekim. MRQ eklentisi projede açık değil: eklenti açmak ve Level Sequence oluşturmak onay gerektirir.
- Oyuncu kamerası istasyon pozları henüz kaydedilmedi.
- Unreal Screenshot Comparison'ın deterministik test haritasında denenmesi.
- MCP sunucusu ve istemci tarafında `list_changed`.
- Video içeriği (transkript yok).

**Riskler**
- Orman görünümünde yerel değişiklikler ölçümle yakalanamıyor; yanlış "değişiklik yok" sonucu çıkabilir.
- Oturumun ilk çekimi gecikiyor; pozlama oturmamış olabilir.
- Uzun ve PIE ağırlıklı oturumdan sonra viewport'ta duvar eksik çizimi gibi tuzaklar biliniyor. Bu turda gözlenmedi, ama yeni bir editörde tekrar edilmeli.
- Dirty iki ABP paketi kazara kaydedilebilir.
- Bridge kamera pozları eski (2026-09-25); dünya değiştiyse kadraj kayar.
- Görsel puanlamam deterministik değil.
- 8000 portu açılırsa kimlik doğrulaması yok ve runner kapıları atlanır. Bu yüzden önerim: döngüyü runner içinde tutmak.

## 8. Onay bekleyen işlemler

Hiçbiri yapılmadı.

1. **FLIP kurulumu.** Resmi NVlabs FLIP Python paketi, proje dışındaki ayrı bir venv'e; Blender Python'u ya da sistem Python'u kullanılmaz.
2. **Editörü yeniden başlatmak** ve T1'in ikinci bölümünü (oturumlar arası) çalıştırmak. Önce dirty ABP'lerin ne olacağına karar verilmeli; önerim kaydetmeden kapatmak.
3. **Determinizm denemesi.** İki seçenek:
   - (a) Değişiklik gerektirmeyen yol: 5 kare çekip piksel başına medyan almak (T1b). Bu yalnız ölçüm, onay gerektirmez ama ayrı bir tur.
   - (b) MRQ eklentisini açmak + bir review Level Sequence asset'i oluşturmak (yapılandırma ve asset değişikliği).
4. **P istasyonlarını kaydetmek:** PIE'de gerçek oyuncu kamerasıyla, salt-okunur. Hangi istasyonların seçileceği kullanıcı kararı.
5. **MCP sunucusu ve Claude Code bağlantısı.** Artık düşük öncelik: in-process çağrı yolu yeterli.
