# SPHIRUS V2.25 — Tempolu hareket, anlamlı kamera, arazi geçişi

**Genel durum: PARTIAL.** Üç hedefin yalnızca biri (inceleme kamerası) kısmen tamamlanmış davranış olarak üretime girdi; arazide küçük ama gerçek bir düzeltme ve bir gerileme onarımı üretimde; tempolu geri dönüş içeriği yazıldı, ölçüldü ve **üretime alınmadı**.
- Teknik doğrulama (ayar/graf: `verify_prod225` ALL_OK, temiz yeniden açılış) ile hareket kalitesi ve görsel kabul ayrı yazıldı.
- Kullanıcı kabulü verilmiş sayılmadı. Görsel değerlendirmeyi kendim yaptım ve her yerde ayrıca belirttim.

**Taban ve sahiplik**
- Taban: V2.24 üretimi. UE 5.8, yalnız Blueprint. Oyuncu zinciri `BP_PBI_Player` → `BP_GR_Player`; hareket SHME bileşeni + `ABP_GR_MotionMatchingBase`; kamera GraceRanger rig + SHME kamera fonksiyonu.
- Kontrol noktası: `Saved/Codex/SHME_V225_20261023/checkpoint/` (ikili varlıklar + DSL kaynakları + harness).

**Ölçüm koşulları**
- Varsayılan sabit 30 FPS (`-UseFixedTimeStep`), aynı oturumda A/B, gerçek klavye/bakış girdisi. Ayrıca 20 / 60 / 120 FPS ve gerçek zamanlı koşular.
- "o" = üretim. "rv" = o + yazılı geri dönüş veritabanları. "ins" = o + inceleme kamerası (artık üretim).
- **Harness tuzağı (yeni bulundu):** her koşudan önce SHME DA alanları şema varsayılanına sıfırlanıyor, sonra koşunun bayrakları uygulanıyor. Kaydedilmiş DA değeri ancak bayrak açıkça verilirse sınanıyor. Bu yüzden üretim inceleme kanıtı "ins" koşularıdır.

---

## İlk sayfa: üç sonucun gerçek durumu

### 1. TEMPOLU GERİ DÖNÜŞ — PARTIAL, üretimde DEĞİL

| Soru | Cevap (ölçülen) |
|---|---|
| Karaktere özel fren–destek–yeniden itiş içeriği var mı? | **Evet, yazıldı.** 16 klip (geri→ileri B_F, ileri→geri F_B; her biri 8 destek evresi), iki yeni veritabanı. Klipler kapsülün **ölçülmüş** fren/itiş hız eğrisinden üretildi (5 evrenin ortalaması), fren ayağı durma noktasının ötesine tasarlandı, ilk itiş adımı zamanla tasarlandı. Klip içi ayak hatası en kötü 1.26 cm. |
| Doğru destek evresinden giriliyor mu? | Evet. MM, klibi evre kutusuna göre 0.00–0.13 s'den giriyor; toparlanma talebi her koşuda 0. |
| Basılı ayak kayması (en kötü, 13 senaryo, 30 FPS) | Ortalama **26.1 → 17.5 cm**, en kötü **49.7 → 31.8 cm**. 7 senaryoda daha iyi, 6'sında daha kötü (ör. ph3 16.6 → 31.8). |
| Kare hızına dayanıklı mı? | **Hayır.** 20 FPS: ph0 49.6 → 12.2 cm. 60 FPS (üretim → aday): ph0 32.4 → 29.2, sw_ph2 21.6 → 26.3, ph3 15.4 → 40.5. 120 FPS: ovl 35.2 → 39.1. Düşük kare hızında açık iyileşme, 60/120'de eşit ya da kötü. |
| 120 FPS / 110 cm hatası | Temiz veritabanlarıyla yeniden üretilemedi: aynı girdiyle 120 FPS'te üretim 35.2 cm, aday 39.1 cm. "Çözüldü" denmiyor. |
| Planlı itiş toparlanmayı tetikliyor mu? | Hayır; adayda `RecoveryDemand` her koşuda 0. Toparlanma kapatılmadı. |
| Koruma testleri (fare 180, cut-reverse, jog start, taps, walk start) | Aday ile üretim aynı sayılar (ör. fare 180: 6 sıçrama, en kötü 292 m/s², ikisinde de). Gerileme yok, iyileşme de yok. |
| Ağır çekim aileleri (yürüyüş arka, jog sağ, sprint yan) | **Yapılmadı.** |
| Görsel (kendi değerlendirmem, `img/jogrev_SW_*_f58.jpg`) | Aynı anda aday dizleri derin bükülü, leğeni alçak, kolları toplanmış bir çömelme duruşunda; üretimin öne eğik itiş adımından daha iyi görünmüyor. |
| Karar | Kare hızına bağlı sonuç ve görsel değerlendirme nedeniyle **üretime alınmadı**. Geri alma gerekmiyor (üretim V2.24 veritabanlarında). |

**Kalan neden (ölçüldü, çözülmedi):** görünen ayak klibin ayak yolunu izlemiyor. F_B fren ayağı klipte sabitken ekranda 32 cm ilerliyor; kapsül ile klip kökü ise 4 cm içinde örtüşüyor. Stride / Orientation Warping elendi (alfa 0'da sonuçlar birebir aynı). Sıradaki şüpheliler: MM oynatma hızı (kapsül hızı / dizinli kök hızı, 0.7–1.2) ve FootPlacement kilit tespiti.

### 2. ANLAMLI KAMERA (durup inceleme) — PARTIAL, üretimde

| Soru | Cevap |
|---|---|
| Davranış kuruldu mu? | **Evet.** Kamera merkezinden tek küre izi → hedef adı ("INS_/Mask/Door/Lamp") → bekleme (0.35 s) → kilit → kadraj yumuşar → sınırlı baş/boyun/gövde bakışı → bakış kayınca veya yürüyünce dönüş. |
| QA hedefinde (fener, 4.4 m) | Durduktan **0.57 s** sonra yakalandı. Kamera **~44 cm yaklaştı** (kapsüle göre 185 → 141 cm), yan ofset 30 → 27 cm, bakış alfası 1.0. İnceleme içinde kamera sarsıntısı dışarıdakinin yarısı (jerk95 0.36 / 0.71). |
| Gerçek zamanlı (son birleşim, `v225fin_ins_*`) | Yakalama 0.55 s, bırakma 8.2 s'de (sabit adımla aynı), yaklaşma 178 → 141 cm, bakış alfası 1.0; geri yürüyüşte 0.5 s / alfa 0.84; yürürken tetiklenmiyor. |
| Bakış değişince / yürüyünce | İlk sürüm ~2 s geç bırakıyordu; bekleme sınırı + hız sınırı 60 cm/s ile düzeltildi. Bakış kaydıktan sonra **~0.8 s** içinde normal kadraja dönüyor. Yürürken serbest bakış inceleme tetiklemiyor (doğru). |
| Fare önceliği / girdi geri beslemesi | Kontrol yaw'ı yalnız oyuncu girdisiyle değişiyor; inceleme kamera ofsetine yazıyor, girdiye değil. |
| FOV / netlik | FOV sahibi değişmedi (pompalama yok). DOF eklenmedi. Fark yaklaşma + kadraj ile, ölçek hilesi yok. |
| Gerçek ev rotası | **Tamamlanmadı.** Atölye duvarındaki R05 maskeleri çarpışmalı (BlockAll) ama 2.5 s bakışta ışın maskeye isabet etmedi. İsabet edilen aktörün adı telemetride olmadığı için neden ayrılamadı. Eski `Furniture_*Mask*` parçalarının çarpışması yok, iz onları hiç göremez. |
| Baş açısı | Bakış alfası ölçüldü; kemik dönüş açısı telemetride yok → **NOT_TESTED**. |

### 3. ARAZİ GEÇİŞİ — PARTIAL (iyileşme + gerileme onarımı üretimde; yüksek basamak açık)

| Soru | Cevap |
|---|---|
| Tümsekte sol ayak takılması | Eski ölçü aracı, düz zeminde iz çizgisinin 1–2 cm altındaki basılı kareleri de "takılma" sayıyordu. Ayağın kendi zemin kalibrasyonuna göre düzeltildi: tümsekte takılma V2.24'te de V2.25'te de 0. |
| Yükselen zeminde adım (yürüyüş, V2.24 → V2.25) | B1 sağ ayak sürtme **51 → 18 cm**; B2 sol ayak zeminden en düşük **0.9 → 2.5 cm**, sürtme **84 → 35 cm**, basılı kayma **26 → 7 cm**. İki giriş ayağıyla da benzer. |
| Basılı ayak titremesi (V2.25 içinde bulundu, onarıldı) | T1 kapısı basılı sol ayağa kare kare 2–10 cm kaldırma uyguluyordu (geri besleme). T1b: kaldırma yalnız ≥ 0.10 s temassız ayağa. Dikey ikinci fark 12.6 → 6.2 cm (V2.24: 8.8). Düz zeminde kaldırma 0. |
| İnişte destek kayması | 15 / 28 cm inişlerde basılı kayma 0.6–4.6 cm; leğen sürekli. |
| Planlı adım hazırlığı (T2/T2c) | **Reddedildi:** leğen V2.24'te zaten sürekliydi; T2c FootPlacement ile çift düzeltme yapıp 28 cm basamak çıkışında leğeni 8 cm çökertti. Kapalı. |
| Yüksek basamağa çıkış | **Açık:** 28 cm basamakta sağ ayak 6 kare zemin içinde, basılı kayma 12–16 cm; step2 parkurunun ilk basamağında (10/22 cm) sol ayak 18 kare. |
| Gerçek ev–orman rotası | **Koşulmadı.** |

---

## Doğrulama ve kanıt

- **Temiz yeniden açılış:** `verify_prod225` ALL_OK (`pub/verify_prod225_final.txt`). Yalnız ayar/graf doğrulaması.
- **Gerçek zamanlı son birleşim** (`v225fin_*`, ~28 FPS): üretim geri dönüşü ph0 47.2 / sw_ph2 24.8 cm (V2.24 ile aynı aralık); tümsek yürüyüşü 30 FPS sonuçlarıyla tutarlı. Tek uzun kare 125 ms.
- **İlk kullanım:** harness her koşudan önce ısıtma koşusu yapıyor; "ilk kullanım" kanıtı **yok**.
- **Editör çökmesi (bir kez):** PIE bitişinde `GameViewport.IsUnique()` assert; harness yeniden başlatıp koşuyu tekrarladı. Kök neden araştırılmadı.
- **Performans:** sabit adımda `dt` maliyet değil; oyun/animasyon süresi ölçülmedi → **NOT_TESTED**. Eklenen iş: kare başına 1 küre izi (inceleme açıkken) + 2 ayak altı çizgi izi.
- **Videolar:** tam kare 1728×972 (16:9). Kırpma kaldırıldı: oyun, bu boyutta yüzen PIE penceresinde oynuyor; genişlik 64'ün katı olduğu için MediaIOCore kabul ediyor.

## Medya (`vid/`, `img/`)
Hepsi son kayıtlı birleşimden, sabit 30 FPS oyun zamanı = gerçek hız, kesilmemiş tam kare 1728×940:
- `jogrev_SW_prod_side` / `jogrev_SW_candidate_side`: S→W geri dönüş, üretim ve aday, yan kamera (ayrıca 1/3 hızlı inceleme kopyası).
- `jogrev_WS_prod_diag` / `jogrev_WS_candidate_diag`: W→S→W, çapraz kamera. `jogrev_WSW_prod_game`: oyun kamerası.
- `inspect_qa_game` / `inspect_qa_diag`: dur → bak → incele → geri bak → yürü (üretim inceleme kamerası).
- `terrain_bump_walk_side` / `terrain_bump_walk_game`: tümsek yürüyüşü (T1 + T1b).
- Normal hızdaki videolar ana kanıttır; GIF'ler önizleme içindir.

## Açık liste (bu sürümün dışında kaldı)
- Geri dönüş: görünen ayak ≠ klip ayağı (oynatma hızı / FootPlacement); F_B_P4 klip içi 8.9 cm kayma; ağır çekim aileleri.
- Kamera: ev maskelerine isabet; isabet edilen aktörün adı telemetriye; paketli oyunda `GetDisplayName` nesne adı döndürür → hedefler için `GR_Inspect` etiketi daha sağlam.
- Arazi: yüksek basamakta iniş noktası (ayak basamak içine iniyor); gerçek ev–orman rotası.
- Dar geçit, el teması, ses ve yeni efekt aileleri: dokunulmadı.
