# Sphirus World — İnsan hareketi ve gerçekçilik, 1. geçiş (2026-11-24)

**Durum: KISMİ — genel iş tamamlanmadı.** Bu geçişte en yüksek öncelikli hareket sorunu (aşırı kalça sallanması) ve koşu/sprintteki aşırı üst gövde burkulması kaynağında ölçüldü, düzeltildi ve kaydedildi. Ağırlık/atalet, başlangıç–duruş, boşta duruş, saç fiziği, yüz, kıyafet ve tam regresyon **yapılmadı**; nedenleri aşağıda. AAA düzeyi iddia etmiyorum, kullanıcı kabulü yazılmadı.

Proje: `sphirus_UE59` (UE 5.9), oyuncu `BP_HybridA_Player`, sürücü animasyon grafiği `ABP_Sph_GASP`, görünür gövde `ABP_Sph_Body_GASP`.

## Sınıflandırma

| | |
|---|---|
| **Uygulandı ve ölçümle doğrulandı** | Kalça hattı dönme/eğilme azaltma (yürüyüş, sprint); koşu/sprintte omuz hattı burkulma azaltma; varsayılan betik sırası düzeltmesi; cilt/göz/kaş malzeme değerlerinin diskten kalıcılığı |
| **Uygulandı, görsel olarak doğrulanmadı** | Aynı değişikliklerin videoları çekildi (aynı kamera, aynı girdi) ama baştan sona izleyip yargılamadım; yargı sende |
| **Denendi, reddedildi** | (bu geçişte yok; saç fiziği önceki geçişte reddedildi) |
| **Uygulanmadı** | Faz 3 (ağırlık/atalet, başlangıç/duruş), Faz 5–7 (ayak teması yeniden değerlendirme, geçiş zinciri, boşta duruş), Faz 8–11 (yüz, saç, kıyafet, ışık), test haritasında 60/30/değişken Hz regresyonu, editörü yeniden açarak doğrulama |

## 0. Proje bütünlüğü

- **Varsayılan sırası sorunu (doğrulandı, düzeltildi):** `c_posture7_defaults.py` gerçekten `PS_AbdBase 12.5 / PS_AbdRun 9.5` yazıyor. `alldef.py` içinde `c_cr1_defaults.py` ondan **sonra** çalıştığı için son değer 8.5 / 13.5 oluyordu; yani sessiz geri alma olmamıştı ama güvence de yoktu. Şimdi kaydetme betiği (`w_save_mr1.py`) varsayılanları uyguladıktan sonra değerleri okuyup **yanlışsa kaydetmeden duruyor** (`PRESAVE` satırı: 8.5 / 13.5).
- **Diskten kalıcılık:** cilt, göz ve kaş malzeme örnekleri çalışan editörde **diskten yeniden yüklenip** okundu; değerler kayıtlı (mikro normal 1.2, düzleştirme 0.1, saçılım 0.6, iris doygunluğu 1.0, kaş Desat 0.25).
- **Doğrulanamayan:** `BP_HybridA_Player` ve `ABP_Sph_GASP` için "editörü kapat–aç–oku". Yalnız aynı oturumda kayıt sonrası okuma var.
- **Engel:** ev alt haritası `L_GR_CurrentHouseContent` editörde kaydedilmemiş değişiklik taşıyor ve bunu ben yapmadım (günlükte benim başlatmadığım oyun oturumları var: 04:54–05:00 ve 06:27). Harita değiştirmek veya editörü kapatmak o değişikliği silerdi; bu yüzden test haritası yüklenemedi ve editör yeniden açılamadı.
- Başlangıç yedeği: `Saved/UE59Work/mr1/ckpt0/`. Yazma manifesti: `ue59_m29_mr1save1_071053`. Kullanıcı kaydı değişmedi (`10201b8b41b7`).

## 1–2. Teşhis ve kalça sallanmasının tam kök nedeni

Ölçüm aracı `an_hip.py`: her kare, sürücü iskelet ve görünür gövde için ayrı ayrı; kalça hattı (iki kalça eklemi) ve omuz hattı üzerinden, yürüyüş döngüsü başına tepe-tepe değer.

Kayıtlı Tur 9 sürümü, düz test haritası (`f9_L`):

| Yürüyüş biçimi | Kalça yanal kayma | Kalça dikey | Kalça **eğilme** | Kalça **dönme** | Omuz dönme |
|---|---|---|---|---|---|
| Yürüyüş 180 cm/s | 4.4 cm | 4.6 cm | **13.0°** | **16.6°** | 16.3° |
| Koşu 415 cm/s | 1.9 cm | 5.3 cm | 10.3° | 8.3° | **44.4°** |
| Sprint 568 cm/s | 2.6 cm | 3.1 cm | 14.9° | **24.9°** | **39.7°** |

Bulgular:

1. **Sallanma bir ötelenme değil, dönme ve eğilme.** Yanal kayma ve dikey hareket olağan aralıkta; aşırı olan, kalça hattının her adımda dönmesi ve yana eğilmesi.
2. **Kaynak animasyon klibinin kendisi.** Sürücü iskelet ve görünür gövde değerleri aynı (13.0 / 13.0, 16.6 / 16.8). Yani yeniden hedefleme, duruş katmanı, ayak yerleşimi veya pelvis IK bunu eklemiyor; `M_Neutral_Walk_Loop_F` ve `M_Relaxed_Sprint_Loop_F` böyle.
3. **Koşu ve sprintte asıl kukla hissi üst gövdede:** omuz hattı döngü başına 40–47° burkuluyor, baş yanal olarak 7–10 cm salınıyor.
4. Ayak aralığı 14 cm (yürüyüş) — olağan; "podyum yürüyüşü" çapraz basıştan gelmiyor.
5. Kıyafetin (bol şortun) görünen kalça hareketine katkısı **ölçülmedi**.

Karşılaştırma için evrensel bir eşik uydurmadım; hedefi karakterin kendi verisinden koydum: hareketi kaldırmadan, aşırı kısmın yaklaşık üçte biri–yarısını almak.

## 3. Kukla/arcade görünümünün diğer nedenleri (bu geçişte yalnız ölçüldü veya dokunulmadı)

- Koşu/sprintte üst gövde burkulması — **düzeltildi** (aşağıda).
- Dönerek koşu başlangıcında gövdenin öne dalması (16.9 cm baş düşmesi, Tur 9) — dokunulmadı.
- Durağan duruşun simetrik ve dik olması — dokunulmadı.
- Saçın hareketsiz olması — dokunulmadı.

## 4. Uygulanan hareket sistemi değişiklikleri

Yeni bir denetleyici eklenmedi; mevcut pelvis katmanı (`GR_Bob` + ayak yerleşiminden önceki pelvis düğümü) genişletildi.

- **`ABP_Sph_GASP`:** mevcut pelvis düğümüne bileşen uzayında eklemeli dönme (`SphHipRot`); hemen ardına `spine_01` için karşı dönme düğümü (`SphSpineRot`). İkisi de ayak yerleşiminden **önce**, yani ayaklar düzeltilmiş pelvisten yeniden basıyor.
- **`BP_HybridA_Player.GR_Bob`:** her karede sürücünün kalça hattı okunuyor, bir önceki karede uygulanan düzeltme çıkarılarak klibin kendi değeri bulunuyor. Yavaş ortalaması (dönüş, eğilme) korunuyor; yalnız döngüsel kısmın bir payı geri alınıyor. Gövdeye aynı miktar ters dönme veriliyor ki omuzlar ve baş kendi hareketini korusun.
- Yalnız yerde, hareket hâlinde ve montaj oynamıyorken etkin; `HIP_On = 0` tüm katmanı kapatır.

| Parametre | Yürüyüş | Koşu | Sprint |
|---|---|---|---|
| Kalça dönmesinden alınan pay | 0.45 | 0 | 0.35 |
| Kalça eğilmesinden alınan pay | 0.38 | 0.2 | 0.33 |
| Omuz dönmesinden alınan pay | 0 | 0.35 | 0.30 |

## 5–6. Anatomi, cilt, yüz, saç, kıyafet

Bu geçişte **yeni değişiklik yok**. Önceki geçişin cilt/göz/kaş ve kol duruşu değişiklikleri duruyor ve malzeme tarafı diskten doğrulandı. Saç için istenen "proje kopyası üzerinde ön tutam düzenlemesi" yapılmadı; saç fiziği hâlâ kapalı ve bunu tamamlanmış iş olarak sunmuyorum.

## 7. Değişen varlıklar ve dosyalar

| Varlık / dosya | Değişiklik |
|---|---|
| `/Game/Sphirus/Player/GASP/ABP_Sph_GASP` | `SphHipRot`, `SphSpineRot`; pelvis düğümüne dönme, yeni `spine_01` düğümü |
| `/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player` | `GR_Bob` içine kalça/omuz mantığı; değişkenler `HIP_*` (14), `SH_*` (4) |
| `Tools/UE59_20261124/` | `an_hip.py`, `c_hip1.py`, `m_hip1_mcp.py`, `m_hip2_mcp.py`, `c_mr1_defaults.py`, `w_save_mr1.py`, `hk_rear9.py` |
| `Saved/UE59Work/r9/alldef.py` | `c_mr1_defaults` en sona eklendi |

## 8–9. Ölçülen sonuçlar (ev haritası, aynı rota, aynı girdi; katman kapalı → açık)

| | Kalça eğilme | Kalça dönme | Omuz dönme | Baş yanal | Ayak kayması (en kötü) |
|---|---|---|---|---|---|
| Yürüyüş | 13.1° → **9.1°** | 17.6° → **10.2°** | 16.2° → 16.1° | 4.9 → 5.2 cm | 2.2 → 2.2 cm |
| Koşu (kısa, geçiş klibi dahil) | 12.8° → 11.0° | 15.3° → 15.5° | 37.2° → **25.3°** | 7.9 → 4.7 cm | 1.5 → 1.6 cm |
| Sprint (kısa) | 11.6° → **7.4°** | 23.6° → **15.4°** | 35.7° → **24.2°** | 9.2 → 5.8 cm | 1.2 → 1.3 cm |

- Kalça yanal kayma, dikey hareket, kol salınımı ve ayak aralığı değişmedi (hareket yok edilmedi, yalnız aşırı dönme/eğilme alındı).
- Yürüyüşte omuz hareketi korunuyor; gövde sertleşmedi (ölçüyle).
- Koşu ve sprint kayıtları ev haritasında alan kısıtı yüzünden kısa (2'şer döngü) ve hızlanma klibini içeriyor; düz test haritasındaki uzun ölçümle tekrarlanmalı.
- **Regresyon (ev haritası, sınırlı):** yürüyüş → koşu → dur → A/D planı 60 Hz ve 30 Hz'de en kötü 1.9 / 1.7 cm (kapalıyken 1.6). İkinci plan (sprint → geri) verandadan düşüş içerdiği için kapalı/açık her iki durumda da gürültülü (kapalı 30 Hz 23.5 cm, açık 10.0 cm); bundan sonuç çıkarmıyorum.
- **Yapılamayan:** Tur 9 kabul planları ve eski 24'lük set (düz test haritası, 60/30/değişken Hz). Bu yüzden "Tur 9 kazanımları korundu" diyemiyorum; yalnız ev haritasındaki sınırlı kontrolde bozulma görmedim.

Videolar (`videos/`, gerçek hız, aynı başlangıç, aynı girdi, aynı ışık): `mr1V_walk_rear_off/on` (sabit arka tam beden), `mr1V_run_rear_off/on`, `mr1V_walk_game_off/on` (gerçek omuz kamerası). Yan ve ön kamera çekilmedi.

## 10. Karakter görsel karşılaştırmaları

Bu geçişte yeni görsel değişiklik yok; önceki geçişin önce/sonra görselleri `sphirus-ue59-karakter-gercekcilik-1-2026-11-24/evidence/` altında.

## 11. Performans

Bu geçişte ölçülmedi. Eklenen maliyet: karede dört soket okuma ve birkaç matematik düğümü, iki animasyon düğümü. Ölçmeden "maliyetsiz" demiyorum.

## 12–14. Çözülmeyenler ve sıradaki iş

1. **Senin kararın gereken engel:** `L_GR_CurrentHouseContent` içindeki kaydedilmemiş değişiklik. Kaydedilmeli mi, atılmalı mı? Bu çözülmeden test haritası regresyonu ve yeniden açarak doğrulama yapılamıyor.
2. Düz haritada uzun koşu/sprint ölçümü ve Tur 9 regresyon seti (60/30/değişken Hz).
3. Ağırlık ve atalet: başlangıçta destek bacağına yüklenme, duruşta yerleşme, 90° başlangıçtaki dalış.
4. Boşta duruş: asimetrik yük, hafif nefes dışı canlılık.
5. Saç: proje kopyasında ön tutamların sabitlenmesi, ardından fiziğin açılması.
6. Yüz (göz kırpma, bakış, ifade), kıyafet davranışı, kıyafetin kalça görünümüne etkisi.
7. Tur 9'dan açık kalanlar: kısa A/D dokunuşu (23 cm), 180° yürüyüş başlangıcı (48 cm), sendeleme, yan/arka düşme, koşu→yürüyüş iniş süresi kararı.

## EK — Kayıtlı ve yeniden açılmış sürümde doğrulama (aynı gün, sonradan)

Onayınla ev alt haritasındaki kaydedilmemiş değişiklik atıldı ve editör yeniden açıldı. Aşağıdakiler yukarıdaki "yapılamadı" maddelerinin yerine geçer.

**Kalıcılık (yeniden açıldıktan sonra diskten okundu):** `PS_AbdBase 8.5`, `PS_AbdRun 13.5`; `HIP_On 1`, kalça payları 0.45 / 0 / 0.35 ve 0.38 / 0.2 / 0.33, omuz payları 0.35 / 0.30; animasyon grafiğinde `SphHipRot`, `SphSpineRot`; cilt değerleri 1.2 / 0.1 / 0.6; saç fiziği kapalı; kirli paket yok (`data/final/log.txt`).

**Düz test haritası, uzun ölçüm (6–13 döngü), katman kapalı → açık (`data/final/hip.txt`):**

| | Kalça eğilme | Kalça dönme | Omuz dönme | Baş yanal (sürücü) |
|---|---|---|---|---|
| Yürüyüş 180 | 13.1° → **9.0°** | 16.6° → **9.6°** | 16.3° → 16.4° | 5.1 → 5.4 cm |
| Koşu 415 | 10.4° → 8.6° | 9.2° → 8.8° | 44.0° → **29.0°** | 6.9 → 8.3 cm |
| Sprint 569 | 15.0° → **11.0°** | 24.9° → **17.4°** | 39.7° → **28.0°** | 9.7 → 8.5 cm |

30 Hz'de aynı sonuç (yürüyüş 8.7° / 9.8°, koşu omuz 28.4°, sprint 10.5° / 17.1°). Kalça yanal kayma, dikey hareket, ayak aralığı değişmedi. Not: koşuda sürücü iskeletin baş yanal salınımı azalmadı (6.9 → 8.3 cm); görünür gövdede 5.0 → 5.9 cm. Yani koşuda baş sabitleme iyileşmedi, yalnız gövde burkulması azaldı.

**Ayak teması regresyonu (yerde en kötü kayma, cm):**

- Eski 24'lük set (12×60 Hz, 7×30 Hz, 5×değişken): en kötü **4.1 cm**, 10 cm üstü yok. Sprint→geri 30 Hz 1.8 cm, ikinci test 1.7 cm. Tur 8/9 kazanımları korunuyor.
- Tur 9 kabul planları: 60 Hz'de 16 plan, 30 Hz'de 7, değişken Hz'de 5 koştu (`data/final/r9plans.txt`; her kaydın kimliği `r9_<plan>_<hz>_M1`). Eski A/D senaryosu 1.8 / 1.8 / 1.7 cm; koşu A↔D 1.8 / 1.6 / 1.7; yürüyüş zinciri 2.0 / 1.8 / 1.8; geri zincir 4.2.
- Düşme 60 ve 30 Hz: eller yerde (3.6–6.5 cm), önceki geçişle aynı.

**Açık duran veya yeni görülen kötü örnekler (gizlemiyorum):**

1. **Sprint A↔D, 60 Hz: 83 cm** (bir dönüşün çıkışında yeniden ters komut; sol ayak yere yakınken kapsül ~500 cm/s). Katman açıkken 3/3, kapalıyken 2/2 tekrarlandı, yani **kalça katmanından gelmiyor**. Tur 9 finalindeki tek koşuda 1.8 cm çıkmıştı; orada komut ~0.05 sn farklı fazda gelmiş ve başka klip seçilmişti. Tur 9'da bu senaryoyu tek koşuyla "geçti" saymam hataydı. Çözülmedi.
2. Kısa A/D dokunuşu: 60 Hz'de 1.8 cm, 30 Hz'de 3.1 cm, değişken Hz'de **22.4 cm** — bilinen tek örnek hâlâ var, hangi koşulda çıkacağı koşudan koşuya değişiyor.
3. 180° yürüyüş başlangıcı: 47.9 cm (değişmedi).

**Hâlâ yapılmayanlar:** yan/ön kamera videoları, performans ölçümü, Faz 3 ve Faz 5–11'in tamamı.
