# SPHIRUS — SHME V2.37: doğal duruşun girişi, kesilmesi ve çıkışı (2026-10-29)

V2.36 üretimi (Bridge eaaedca) üzerine yapıldı. Proje Blueprint-only UE 5.8; git yok. Geri dönüş, sha1 doğrulamalı manifest yedekleriyle yapılır.

**Ölçüm koşulları:**
- Sayıların hepsi sabit adımlı editörde, aynı girdiyle ölçüldü. Aksi yazılmadıkça 30 FPS.
- Kayma ölçütü: `contact231`, en kötü basılı top kayması (cm).
- `o` = V2.37 üretimi. `pre237` = V2.37 gruplarının hepsi V2.36 değerinde.
- Kanıt temiz açılıştan sonraki derlemenin koşularıdır (`fin2`, `g60/g120/g20/greal`, `cold2`, `cap2`).
- `+` işaretli hücreler ilk derlemedendir. O koşular duruş DB'sine hiç girmez, bias değişikliğinden etkilenmez; tablo `TABLES_V237.md`.

Teknik PASS, görsel kabul değildir. Görsel yargılarım normal hızlı (30 FPS oyun zamanı = gerçek hız, ağır çekim yok) kayıtlardan çıkarılmış, zaman damgalı kare şeritlerine dayanıyor (`sheets/cap2_*`). Videoları gerçek zamanlı oynatıp izleyemedim. Ritim ve oyun hissinin son kabulü sizde; aşağıda gördüğüm kusurları açıkça yazdım.

## Üretimde (temiz açılışta VERIFY237 ALL_OK)

| Grup | İçerik |
|---|---|
| `start` | Adım planlı düz tempolu sol/sağ kalkış (`SHM237_JogStart_F_L/Rfoot`). Kök ölçülen kapsülde. |
| `resume` | Duruşun içinden yeniden itiş: 24 bölme × 4 an + düz kalkışlar (`PSD_SHM237_JogResume`). |
| `stop` | V2.36 duruş planı; fren pelvisi klipte, FootPlacement pelvisi frende kapalı (`SHM237_FPPelvisOff`). |
| `stop` giriş | Duruş DB'si continuing bias −3 → **−25** (girişte bölme sıçraması). |

Ayrıntılar ve geri dönüş: `CHANGES_V237.md`.

## 0. İlk sayfa: doğrudan cevaplar

### 1. Sol kalkıştaki kaymanın gerçek nedeni ve çözüm
Aynı referans uzayında (oyunun görünen mesh'i `vb_` ve MM çıktısı `mx_`, aynı karelerde) iki neden vardı:

1. **Yük taşıyan ayak havadaki döngü pozuna döndürülüyordu.** V2.36 klibi, karşı ayağın topuk basışında destek ayağını döngünün havadaki pozuna slerp ediyordu. Bu sırada top kilitliydi. Sonuç: ayak eğimi 39° → 122°, ayak bileği topun önüne geçti, top 16–17 cm geri kaydı.
2. **Kök kapsülden hızlıydı.** Klip kökü 470 cm/s² ivmeleniyordu; oyundaki kapsül 165 → 245 cm/s². MM klibi 0.70–0.84 hızla oynattı (yavaş çekim kalkış). 0.65 s'de başlangıç yolu bitince klip adım ortasında kesildi.

Çözüm (`gen237_start.py`, ayağı kaldırarak gizleme değil):
- Kök ölçülen kapsülü izliyor.
- İnişler planlı: 30 → 65 → 105 cm → döngünün kendi inişi.
- Yük taşıyan ayakta en çok 50° topuk kalkışı. Döngünün kendi toe-off'u yalnız itişin son 0.16 s'sinde.
- Kalkış yolu DB'si de klibi içeriyor; ayrıca bitişten sonra kesilmiyor.

### 2. Bu temas oyunda korunuyor mu?
Evet.
- **Oynatma:** `j36_wjs` içinde sol kalkış tek parça oynuyor: 0.00–0.93 s, hız 1.03. V2.36'da 6 parça, 0.00–0.48 s, hız 0.79 idi.
- **Kayma:** sol kalkış artık en kötü olayın sahibi değil.
  - `j36_wjs` 8.9 cm, sahibi duruş bölmesi P09. V2.36 değerleriyle 14.3, sahibi sol kalkış.
  - `j34_chain1` 7.9 cm. V2.36 değerleriyle 17.1.
- **FPS:** `j34_chain1` 60/120/20 FPS'te 6.8 / 6.7 / 10.8 cm (V2.36 değerleriyle 27.9 / 33.3 / 17.3).
- **İlk kullanım:** temiz açılışta, ısıtma koşusu olmadan 7.5 cm; DB'siz kare 0.

### 3. Duruş ortasındaki istek hangi hareketten devam ediyor?
Duruş dört durumla ayrılıyor. Her birinin çıkış sahibi açık:

| Durum | Ne zaman | Çıkış sahibi | Ölçüm (30 FPS) |
|---|---|---|---|
| A: bırakma başı | duruş taahhüt edilmeden | Döngü sürer; duruş episodu yok (`j36_rse`) | 0.0 cm (V2.36 değeriyle 5.6) |
| B: fren ortası | gövde yavaşlarken | Yeniden itiş DB'si (`PSD_SHM237_JogResume`) mevcut pozla eşleşen kareden devam eder. | `j36_rsm` 0.0 (9.5); `j34_chain1` 7.9 (17.1) |
| C: duruş sonu | ayaklar oturmak üzere | Düz kalkış, 0. kareden | `j36_rsl` 6.8 (8.7) |
| D: ters istek | duruş içinde S | V2.36 ters dönüş ailesi (`JogRev_F_B`) | `j36_rsx` 17.1 (17.9). **Açık:** içerik değişmedi. |

B durumundaki eşleşmeler:
- `j36_rsm`: sol kalkışın hareketli kısmı, klip zamanı 0.47.
- `j34_chain1`: `RePush_Br_P01_T057`, klip zamanı 0.20.

Bu eşleşme, duruşun o anki pozundan üretilmiş ya da o poza en yakın kalkış karesidir. Durağan kalkış klibi hareket hâlindeyken 0. kareden başlamıyor.

Görsel (`sheets/cap2_rsm.png`): 5.1 s'de yavaşlama, 5.2 s'den itibaren kesintisiz yeniden hızlanma. Ölçülen kayma yok.

**Gördüğüm kusur:** kollar 5.1 → 5.3 s arasında, yani ~0.2 s'de sarkık hâlden koşu taşımasına kalkıyor ve gövde öne giriyor. Hızlı ama sıçramasız bir kalkış. Rahat bir kadın için biraz sportif görünebilir; normal hızda izleyip karar vermeniz gerekiyor.

### 4. Pelvis çökmesi nereden geliyordu, ne değişti?
Zincir aynı karelerde ölçüldü (`pelvis237.py`): kaynak klip → MM çıktısı → FootPlacement öncesi/sonrası (`SHM_HCi/HCo`) → görünen mesh.

- **Kaynak ve retarget:** temizdi. Klip freni neredeyse düz bacakla 91–94 cm'de taşıyordu.
- **Sahip FootPlacement'tı:** AllLegs pelvis modu, yaylı. Pelvisi frende 6–9 cm indiriyordu. V2.36 fren minimumu 84.5 cm, destek dizi 117°.
- **Değişiklik:**
  - Klip, `SHM237_FPPelvisOff` eğrisini taşıyor: frende 1, son basıştan 0.25 s sonra 0.
  - FootPlacement'ın `DisablePelvisCurveName` özelliği bu eğriye bağlandı.
  - Oturmuş duruşta eğimli zeminde FootPlacement yine çalışıyor.
  - Eğriyi taşımayan klipler için hiçbir şey değişmedi.

Sonuç (30 FPS, frende pelvis minimumu ve oradaki destek dizi):

| Senaryo | V2.36 değerleriyle | V2.37 |
|---|---|---|
| `j36_stop` | 84.5 cm, diz 117°, FP −6.2 | 90.2 cm, diz 142°, FP −0.5 |
| `j36_stopb` | 83.4 / 115° / −8.7 | 87.4 / 131° / −0.6 |
| `j36_wjs` (2. duruş) | 82.3 / 112° / −8.4 | 87.3 / 120° / −0.5 |

Görsel (`cap2_stopr_stop.png` ve `cap2_stopr_pre_stop.png`, aynı girdi):
- V2.36: 5.1–5.3 s'de dizler bükük, çömelme okunuyor.
- V2.37: fren dik, bacaklar uzun. Kollar 0.3 s içinde sönüp iniyor, gövde dikleşiyor, baş düz.

**Kalan:** V2.37 duruşu, ayaklar hafif önlü-arkalı (adım duruşu) oturuyor. Son basış 1.3–1.5 s'de (V2.36 0.8–1.2 s); duruştan sonra ayak 8.7–19.7 cm toplanıyor. Bu küçük bir kapanış adımı. Şeritte sakin görünüyor, ama V2.36'dan daha uzun bir oturma.

### 5. Ters dönüşte kol ve gövde tepkisi normal hızda okunuyor mu?
Kısmen.
- **Bu sürümde yapılanlar:** ters dönüş içeriği (V2.36 tam beden fren) değişmedi. V2.37'nin ters dönüşe etkisi yalnız yol ve giriş tarafında.
- **Kare şeridi** (`cap2_rev.png`): fren adımında kollar iniyor, gövde dik, dönüş ~5.6–5.9 s. `o` ile `pre237` aynı görünüyor.
- **Değerlendirme:** tepki 0.3–0.5 s'lik kısa bir eylem. Normal hızda kolların fren olaylarına bağlı inişi zor seçiliyor.
- **Sonuç:** fren olaylarıyla zamanlanmış yeni üst beden içeriği bu sürümde **üretilmedi**. Bu madde **NOT_DONE**.

### 6. Hangi V2.36 gerilemeleri kapandı?

| Gerileme | 30 | 60 | 120 | 20 | gerçek | Durum |
|---|---|---|---|---|---|---|
| `j34_chain1` | 7.9 / 17.1 | 6.8 / 27.9 | 6.7 / 33.3 | 10.8 / 17.3 | 9.9 / 17.9 | **Kapandı** |
| `j36_wjs` | 8.9 / 14.3 | 6.4 / 8.6 | 11.3 / 20.1 | 6.0 / 16.5 | 14.0 / 13.5 | Sabit adımda kapandı; gerçek zamanda eşit |
| `j30_rel_3450` | 10.3 / 16.3 | 13.4 / 9.3 | 9.1 / 9.0 | 6.4 / 10.5 | 6.4 / 9.7 | Kısmen; 60 FPS kötü |
| `e29_chain` 20 / gerçek | | | | 6.0 / 9.0 | 21.1 / 13.9 | 20 kapandı, gerçek **açık** |
| `jstart` (45° / lateral) | 57.4 / 50.2 | 46.3 / 46.2 | 45.3 / 44.5 | 54.1 / 54.1 | 70.9 / 66.2 | **Açık** |
| `j36_sside` | 22.2 / 21.7 | 24.0 / 35.9 | 20.4 / 36.2 | 17.3 / 17.7 | 27.7 / 32.9 | **Açık** (görsel FAIL) |
| `c29_combo` | 15.4 / 7.9 | 11.8 / 11.8 | 12.9 / 12.9 | 8.9 / 8.9 | 13.0 / 12.9 | **Açık** |

Hücreler `o` / `pre237`, en kötü kayma (cm).

Ayrıca duruş ailesinin kendisi bütün modlarda V2.36 değerlerinden iyi:
- `j36_stop` 0.0 / 6.7 / 5.0 / 0.0 / 6.6 cm (30/60/120/20/gerçek). V2.36 değerleriyle 5.6–8.7.
- `j36_rsm` 0–6.4 cm. V2.36 değerleriyle 9.5–44.1.

### 7. Hâlâ kötü olan durumlar ve nedenleri
- **Yan / çapraz kalkış** (`j36_sside`, vendor `A_LS_Jog_Right_Start`): 7.3–7.4 s'de görünür çömelme, 7.3–7.5 s'de dışa savrulan kol (`cap2_sside.png`).
  - Kayma 17–28 cm. Görsel **FAIL**; V2.37 değiştirmedi.
  - Gereken şey yeni lateral/dönüşlü kalkış içeriği; bu sürümün kapsamına sığmadı.
- **`jstart`** (45° dönüş kalkışı, vendor `TurnR045` / `Left_Start_AAMS`): 45–71 cm. Aynı içerik boşluğu.
- **Ters istek duruş içinde** (`j36_rsx`): 17.1 / 17.9 cm, iki varyantta eşit. Sahibi değişmeyen ters dönüş klipleri.
  - İlk derlemede 7.3 / 9.8 idi; oturumlar arası dalgalanıyor.
- **`e29_chain` gerçek zaman** 21.1 cm, `c29_combo` 30 FPS 15.4 cm: V2.37 içeriğine dokunmayan yollar.
  - `c29_combo`: yürüme-sol tek kare olayı, iki modlu.
  - `e29_chain`: W2S yürüme-sprint. Gerçek zamanda koşudan koşuya değişiyor.
- **Ters dönüş üst beden zamanlaması:** madde 5.
- **Kapanış adımı:** duruş oturması V2.36'dan ~0.4 s uzun (madde 4).

### 8. Kaynak / entegrasyon / nihai kabul

| Parça | Kaynak | Oyuna entegrasyon | Nihai kabul |
|---|---|---|---|
| Düz sol/sağ kalkış | PASS (planlı inişler, 50° sınır) | PASS (tek parça, hız 1.0, cold 0 DB'siz kare) | Sizde. Kare şeridinde kusur görmedim. |
| Duruş ortası yeniden itiş | PASS | PASS (0–6.4 cm, bütün FPS) | Sizde. Kol kalkışı hızlı (madde 3). |
| Fren pelvisi | PASS | PASS (FP pelvisi −0.5 cm) | Çömelme gitti; kapanış adımı uzun. |
| Duruş girişi (bias −25) | — | PASS (60/120 FPS 15–20 → 5–7 cm) | Teknik |
| Ters dönüş üst beden | NOT_DONE | — | NOT_DONE |
| Yan / dönüşlü kalkış | FAIL (vendor) | FAIL | FAIL |

### 9. Kamera ve ilk kullanım kazanımları korundu mu?
Evet.
- **Kamera:** kamera değişkenlerine dokunulmadı.
- **Kamera A/B:** `j36_stopr:camoff` ve `cam34_wflow:camoff` A/B'leri ilk derlemede koşuldu (kamera kapalı karşılaştırma, ayrıntı tablolarda yok).
- **İlk kullanım:** temiz açılışta ısıtma koşusu olmadan 5 senaryonun hepsinde DB'siz kare 0. Kaymalar 0.0–9.3 cm (bölüm 5 tablosu).
- **Efor:** efor zinciri (`e29_load`) değişmedi; bekleme 0.13 s.
- **180°:** gerçek 180° kamera tepkisi bu sürümde ayrıca ölçülmedi. Kamera koduna dokunulmadığı için V2.36'daki NOT_TRIGGERED durumu geçerli sayılıyor; yeniden doğrulanmadı.

### 10. Test sayısı, yeniden başlatma ve zaman dağılımı
- **Koşular:** 432 ayrı etiketli PIE koşusu (A/B, FPS modları, cold, kayıt) + 19 ısıtma koşusu.
- **Editör açılışları:** 17 (1 ilk açılış + 16 yeniden açılış): FPS modu değişimleri, temiz açılış doğrulamaları, kayıtlar.
- **Zaman** (05:27 → ~13:45, yaklaşık 8 saat 20 dk):

| Dilim | Süre |
|---|---|
| Kurulum, ilk açılış | 05:27–05:37 |
| Kalkış/duruş üreteçleri, kuru koşu, yazma | 05:37–06:35 (~1 sa) |
| Aşamalı testler A→B→C→D (S1–S4) | 06:35–07:44 (~70 dk) |
| Üretime alma, temiz açılış, doğrulama + bir düzeltme | 07:47–08:05 |
| İlk nihai kanıt (30/60/120/20/gerçek, cold, kayıt) | 08:05–10:27 (~2 sa 20 dk) |
| 60/120 FPS duruş sıçramasının sahibi, bias adayları | 10:27–11:16 |
| Bias üretime, temiz açılış, VERIFY ALL_OK, nihai kanıt yeniden | 11:17–13:15 (~2 sa) |
| Tablolar, kayıtlar, şeritler, rapor, yayın | 13:15–13:45 |

İlk nihai kanıtın bir bölümü boşa gitti: 60/120 FPS duruş gerilemesini o koşular gösterdi, düzeltmeden sonra bütün kanıt yeniden alındı.

## 1. Duruş girişinin yapışması (bu sürümün geç bulgusu)
- **Sorun:** bırakmadan sonraki ~0.08 s'de duruş DB'si her aramada **klip zamanı 0'da yeni bir faz bölmesi** seçiyordu.
  - Örnek dizi: 120 FPS'te P04 → P16 → P05 → P17 → P06.
  - Sonuç: 60/120 FPS'te basılı ayak 15–20 cm kayıyordu.
  - Kesme modu `InterruptOnDatabaseChangeAndInvalidateContinuingPose` (salt okunur `probe237_stopsearch.py`).
- **Adaylar:** DB kopyaları, ABP değişkeniyle aynı editörde denendi (cb10, cb25).
  - −10 sıçramayı yalnız kısalttı.
  - −25 ilk bölmede kaldı: 120 FPS `j36_stop` 19.8 → 5.0, `rsm` 19.8 → 5.0, `stopb` 11.4 → 0. 30 FPS `rse` 14.0 → 0.
- **Üretim:** üretimdeki DB'nin özelliği değiştirildi (manifest `bias1`, ikili yedek). Ardından temiz açılış, ALL_OK ve bütün kanıt yeniden alındı.

## 2. Kayıtlar (normal hız, düzenlenmemiş)
Her kayıt `vid/<ad>.gif` ve `<ad>_realtime.avi` olarak var. Önce/sonra çiftleri aynı girdi ve aynı kayıt penceresiyle alındı.

| Konu | Önce (V2.36) | Sonra (V2.37) |
|---|---|---|
| Duruş ve yeniden kalkış | `stop_restart_v236_side` | `stop_restart_v237_side`, `_game`, `_diag` |
| Duruş ortası yeniden basış | `midstop_repress_v236_side` | `midstop_repress_v237_side` |
| Yürüme > tempolu > duruş | `walk_jog_stop_v236_side` | `walk_jog_stop_v237_side` |
| Ters dönüş | `reversal_v236_side` | `reversal_v237_side` |

Yalnız V2.37 kayıtları:
- `early_repress_v237_side`, `late_repress_v237_side`, `midstop_opposite_v237_side`
- `stop_other_foot_v237_side`, `chain1_restart_v237_side`
- `stop_side_start_v237_game` / `_side` (kalan FAIL)
- `effort_reversal_v237_side` (ilk derlemeden; bu yol duruş DB'sine girmez)

Kare şeritleri:
- Son derleme: `sheets/cap2_*`.
- İlk derleme: `sheets/*_oS*`, `*_pre*`.

## 3. Sınırlamalar
- **Hareket referansı:** bu sürümde yeni gerçek hareket referansı incelenmedi; V2.36'nın notları kullanıldı.
- **İzleme:** videoları gerçek zamanlı izleyemedim; yargılar 0.1 s adımlı normal hızlı kare şeritlerinden.
- **Donanım:** PS donanımında test yok.
- **Koşu tekrarı:** hücrelerin çoğu tek koşu. Gerçek zaman modu deterministik değil; koşudan koşuya ±5 cm dalgalanma görüldü.
- **Yayımlanmayanlar:** ikili varlıklar, yedekler, ücretli ham animasyon ve çubuk JSON verisi.
