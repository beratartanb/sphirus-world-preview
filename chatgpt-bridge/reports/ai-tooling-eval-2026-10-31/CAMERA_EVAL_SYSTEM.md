# Sabit kamera ve görsel değerlendirme sistemi (tasarım v1, 2026-10-31)

Durum: **tasarım**. Hiçbir aktör, asset, sequence veya yapılandırma oluşturulmadı.

Mevcut sahipler kullanılıyor; yeni bir sistem kurulmuyor:
- çekim: kapılı runner + Bridge çekim çağrısı;
- kabul ölçütleri: `sphirus-aaa-environment-polish` (Tier 0–4, durma koşulları);
- referans: `reference-comparison.md` ve `reference-authority.md`;
- istasyon kimlikleri: `sphirus-level-art-direction` (P00–P11).

## 1. Kamera seti

Veri dosyası `cameras_env_v1.json`. Kameralar sahnede aktör değil; yalnız veri olarak tutulur, harita değişmez.

| Sahne | R: regresyon (editör pozu) | P: oyuncu kamerası istasyonu (kabul) |
|---|---|---|
| Ev önü | R-HF-1 = Bridge `06_house_exterior` (T1'de ölçüldü). Eklenecek: R-HF-2 yakın malzeme (P08 tipi), R-HF-3 zemin teması (P09 tipi) | P00 House front: ileri, ±90°, geriye bakış + 5–15 s yaklaşma, iki yönde |
| Göl | R-PD-1 = Bridge `17_shoreline_gameplay` (T1'de ölçüldü). Ön plandaki genç ağaç kadrajı kapatıyor, **yeniden kadrajlanmalı**. Eklenecek: R-PD-2 = `08_water_to_house` | "Pond reveal" (skill'de kahraman alan) ve kıyı yolu: ileri, ±90°, geriye bakış + yürüyüş |
| Orman | R-FO-1 = Bridge `09_house_to_forest` (T1'de ölçüldü). Eklenecek: R-FO-2 = `11_forest_edge` | P11 Forest volume at player height, P04 First compression: ileri, ±90°, geriye bakış + yürüyüş |

- **R kameraları** teknik regresyon içindir. Bridge pozları otomatik geometrik adaylardır; ilk kurulumda görüş açısı ve kapanma kontrol edilip gerekirse yeniden kadrajlanır.
- **P istasyon pozları henüz yok.** Gerçek karakter ve GraceRanger kamerasıyla PIE'de kaydedilmeli. Oyun FOV'u PIE'den okunacak; burada uydurulmadı.

## 2. Çekim protokolü (R)

1. Kilit (`lock233.sh acquire`). PIE yok. Dirty paket listesi kaydedilir.
2. Çekim `take_high_res_screenshot` ile yapılır; T1'deki `t1_cap.py` deseni:
   - 1920×1080, `force_game_view`, `delay` 0.2;
   - viewport `CaptureViewport` ile yeniden çizilir.
   - Kaydedilenler: poz, FOV, sg.* ve r.* değerleri, ışık ve post-process durumu.
3. **Isınma:**
   - oturumun ilk çekimi atılır;
   - her kamera taşımasından sonra en az 12 s beklenir;
   - görünüm başına 3 çekim alınır, 2 s aralıkla.
4. **Deterministik mod:** hedef, rüzgârı ve zamanı sabitlemek. Yollar, birbirinden ayrı onaylar gerektirir:
   - (a) 5 çekimin piksel başına medyanı (değişiklik gerektirmez; denenecek);
   - (b) Movie Render Queue + review Level Sequence (eklenti + asset onayı);
   - (c) ayrı bir test alt seviyesi.
5. Viewport geri yüklenir; dirty paket listesi ve aktör transform hash'i önce/sonra karşılaştırılır.

## 3. Teknik regresyon ölçümü (R)

| Ölçü | Anlamı | İlk eşik (T1 gürültüsü × 1.5) |
|---|---|---|
| Global ortalama parlaklık farkı | Pozlama ve ışık kayması | \|Δ\| > 1.0 → FLAG |
| Karo maks (16×9, ortalama parlaklık) | Yerel nesne, ışık veya gölge değişikliği | ev 11.1, göl 4.8, orman 20.3 (orman yerel değişiklikleri **yakalayamıyor**, bkz. v2 §4.4) |
| SSIM d16 / d8 | Yapı ve kadraj (kamera kayması, nesne yer değiştirmesi) | d8: ev < 0.94, göl < 0.985, orman < 0.93 |
| FLIP haritası (onaydan sonra) | İzleyicinin göreceği farkın yeri ve büyüklüğü | gürültü tabanı ölçüldükten sonra belirlenecek |
| Tam çözünürlük SSIM / UE-Low | Yalnız bilgi | Kapı değil (gürültüden FAIL veriyor) |

**Çıktı:** PASS / FLAG ve ısı haritası. FLAG, "değişiklik var, insan baksın" demektir; görsel kabul değildir.

**Eşiklerin güncellenmesi:**
- T1 ikinci bölümünden (oturumlar arası) sonra;
- deterministik mod denendikten sonra.

## 4. Sinematik kaliteye yaklaşım (P)

Bu bölüm regresyondan tamamen ayrıdır; tek bir sayıya indirgenmez.

1. **İlke karşılaştırması.** Her referans karesi ve Sphirus karesi için `reference-comparison.md`'deki 10 soru kaydedilir: derinlik katmanı sayısı, orta plan doluluğu, yolun okunması, zeminin kırıklığı, büyük kütle grupları, negatif alanın amacı, yapı-zemin teması, ön plan, tekrarın gizlenmesi, ışığın formu desteklemesi. Çıktı: ilke farkı → kök neden düzeyi → yapısal eylem.
2. **Tier puanı** (`visual-acceptance.md`): önce/sonra farkı için Tier 0–4.
   - Kahraman alanlar (ev önü, göl manzarası) Tier 4 hedefler.
   - Durma koşulları A–H uygulanır; ±90° görünüm çökerse puan en fazla Tier 2 olur.
3. **Açıklayıcı sayısal göstergeler** (kalite puanı değildir; referans kümesinin aralığıyla yan yana gösterilir):
   - parlaklık yüzdelikleri p5/p50/p95;
   - değer grubu oranları (koyu / orta / açık);
   - yerel kontrast;
   - doygunluk dağılımı;
   - kenar yoğunluğu haritası.
4. **Puanlayıcı tutarlılığı:** aynı kareleri iki kez, sırası karıştırılmış olarak puanlarım; uyuşmazlık raporlanır.
5. **Son kabul kullanıcıdadır.** Yürüyüş ve dizi gerektiren kategoriler, görüntü gerçekten izlenmeden NOT_TESTED kalır.

**Referans görüntüler** yerel bir klasörde kalır; Bridge'e yalnız türetilmiş sayılar ve bizim çekimlerimiz gider.

## 5. Döngü

Değişiklik öncesi R + P çekimi:
1. değişiklik (ilgili sahip skill ve onay ile);
2. R çekimi → regresyon (PASS / FLAG + harita);
3. P çekimi → ilke karşılaştırması + Tier + göstergeler;
4. kullanıcı kabulü;
5. Bridge'e çekimler, ayarlar, ölçümler ve rapor yüklenir.
