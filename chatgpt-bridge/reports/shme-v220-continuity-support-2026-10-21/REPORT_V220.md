# SHME V2.20: geçiş sürekliliği, ayak desteği ve çalışma zamanı düzeltmeleri (2026-10-21)

**Taban:** V2.19 üretimi (commit `34305de`).

## Ölçüm düzeni

**Nedensel A/B (ana kanıt).**
- Editör `-UseFixedTimeStep -FPS=N` ile açıldı. Koşular deterministik: aynı ayar aynı santimi veriyor.
- **Son nedensel parti `g30`:** 30 FPS'de, her senaryo için "V2.20 üretimi" ile "V2.20 düğmeleri kapalı" (aynı içerik) yan yana. Kapalı hâl V2.19 davranışıdır; tek fark, yeniden temizlenen iki duruş klibi.
- **FPS çapraz denetimi:** son üretimle 20 / 60 / 120 FPS.

**Gerçek zaman.**
- Final partisi `v220f` (119 koşu), `v219f` ile aynı liste.
- Bu partiden **sonra** iki pawn ayrıntısı düzeltildi (yön tutmanın tetik koşulu, hız eğiminin kapsamı). Düzeltilmiş hâl `g30` ve 120 FPS ile ölçüldü.
- Gerçek zaman koşularında editör takılmaları (`v220f`'de 110 koşunun 55'inde > 0.1 s kare; editör 38 GB'da 7 kez yeniden başladı) tek tek tekrarları bozuyor. Bu yüzden nedensel kanıt sabit adımlı partiler.

**Metrikler.**
- Ayak başına net kayma / sürükleme yolu (`contact216`); iki ayak hiçbir zaman toplanmadı.
- Diz büküm düzlemi dönüş hızı (`knee_stage220`): sürücü iskelet `mx_` ve görünen beden `vx_` ayrı.
- Yerinde dönüş devri (`tip220`), duruşlar (`stops220`), klip zaman hızı (`cliprate220`).
- **Bu sürümde düzeltilen ölçüm hatası:** `contact216` zemin yüksekliğini koşunun **tümünden** kalibre ediyordu. Bu yüzden koşunun sonundaki bir değişiklik (ör. son duruş), hareketi bit bit aynı olan daha önceki pencerelerin sayılarını kaydırıyordu.
  - Bu yüzden bir "regresyon" ortaya çıktı (erken ters R 2.7 → 10.1). Ayak izleri 7.93 s'ye (son duruş) kadar birebir aynıydı (`diverge220.py`).
  - Pencereler artık, pencere sonundan 0.3 s sonra kesilen bir kopyada ölçülüyor (`ctrunc220.py`; `final220.py` içinde de aynı).
  - Önce / sonra tabloları aynı yöntemle yeniden hesaplandı.

Görsel değerlendirmeler teknik değerlendirmedir; **kullanıcı kabulü verilmiş sayılmaz.**

## Üç hedefin durumu

| Hedef | Uygulandı mı | Değişen düğüm / kod / klip | Önce → sonra | Kalan hata | Üretimde |
|---|---|---|---|---|---|
| **1. Toparlamada takılma sonrası geçmiş poza dönüş** | Aday uygulandı ve doğrulandı, **etkisiz.** Hedef **AÇIK** | `install_v220_recsearch.py`: toparlama penceresinde (0.08–0.62 s) MM aramasını kapatan kapı (`SHM220_RecHold`, `bShouldSearch ← SHM220_Search`) | Telemetri: takılma boyunca `Search = False`. Klip yine de 1.30 → 1.07 geri gitti (L 85 cm). Gerçek zaman 0.18 s takılma, 2 tekrar: sol hC 39 / 57 → 5 / 9, sağ 25 / 25 → 85 / 27 | Geri sarma MM aramasından gelmiyor. Takılma karesi klibi ~0.04 s ilerletiyor, sonraki kare takılma süresi kadar geri sarıyor: motorun varlık oynatıcı / blend stack güncellemesi. Blueprint erişemiyor | **HAYIR** (`SHM220_RecHold 0`) |
| **2. Geç ters dönüşte diz bükülmesi** | **EVET** | Kök aşama: `FootPlacement` `PlantSettings_Default = LockRotation`, basılı ayağın yönünü ters pivot boyunca kilitliyor. `Get_FootPlacementPlantSettings` → dış `Select`: ters kilit / toparlama / ters rota / 220 cm/s üstü yön değişiminde `PlantSettings_Walk` (`PivotAroundBall`). IK kapatılmadı, pelvis kilitlenmedi, klip pişirilmedi | Diz düzlemi (°/s, sürücü): 20 FPS 1033 → 567; 30 FPS 1241 → 537; 60 FPS 1211 (V2.18) → 893; 120 FPS 1356 → 911. Gerçek zaman 3 tekrar: 1082–1220 → 546–625. Görünen beden aynı | 60 / 120 FPS'de kazanç daha küçük (~%30) | **EVET** (`SHM220_PivotOn 1`) |
| **3. Yerinde ters dönüşte devir** | **EVET** | `BP_GR_Player.GR_UpdateIdleTurn`, üç kapı: (1) başlatma ilk montajın bitmesini beklemiyor; (2) zincirleme montajda referans açı `GR213_TurnDelta0` yenileniyor; (3) açı kamera 0.05 s durunca seçiliyor. Yeni montaj aynı yuvada oynayan montajın **gerçek pozundan** karışıyor; iki kök hareketi üst üste binmiyor; kalan açı tek karede atılmıyor | İstekten devire 0.27–0.33 s + boşta duruş → **0.10–0.20 s, boşta duruş yok** (90 / 180, iki yön, erken / orta / geç). Dönüş 0.10–0.24 s erken bitiyor. 180° erken: kalan açı 14° → 1°. Gerçek zaman 3 tekrar: 0.15–0.24 s, hepsinde boşta duruş yok | Dönüşte W'ye basmak: L 28 cm (V2.19'da da). Tam 180°'lik ters istek eski ters-açı aralığının dışında kalıyor; 0.4 s'lik bir takılma sonrası eski yola düştü (1 koşu) | **EVET** (`GR217_TipHand 1`) |

## Hedef ayrıntıları

### Hedef 2: diz — aşama yalıtımı

Koşul: `r_cutrev_r2` (geç ters), 30 FPS, sabit adım. Her satırda tek bir çalışma zamanı düğüm ailesi kapatıldı. Değerler sol dizin büküm düzlemi dönüş hızı (°/s):

| Değişken | Sürücü (mx) | Görünen (vx) |
|---|---|---|
| V2.19 üretimi | 1241 | 1208 |
| FootPlacement kapalı | 533 | — |
| LegIK kapalı | 521 | — |
| OrientationWarping kapalı | 1270 | — |
| StrideWarping kapalı | 1240 | — |
| Kilit `PivotAroundBall` / `PivotAroundAnkle` / `Unlocked` / `UnplantAngle 20` | 537 / 556 / 533 / 708 | — |
| **V2.20 (kapsamlı pivot kilidi)** | **537** | **522** |

- Görünen beden sürücüyle aynı; yeniden hedefleme suçsuz.
- IK bükülmeyi büyütmüyor. Kilitli ayak hedefini FootPlacement'ın yön kilidi veriyor; LegIK onu yalnızca çözüyor.
- **Kapsam denemesi:** Ters dönüşe sadece geç evresiyle sınırlama ve genel 220 cm/s terimini çıkarma (`SHM220_PivotT0` / `PivotNoRd`) denendi. Diz kazancı aynı kaldı, ama erken ters değerleri V2.19 seviyesine döndü (R 10 → 13). Düğmeler kuruldu, 0'da bırakıldı.
- **120 FPS'deki geç ters L 38 cm** pivot kilidinden değildi; pivot kapalıyken de 38.9 cm. Kaynak aşağıdaki hız eğimi düzeltmesinde.

### Hedef 3: yerinde ters dönüş (30 FPS, aynı girdi)

| Senaryo | V2.19 devir | V2.20 devir | V2.19 bitiş | V2.20 bitiş | V2.19 L · R (net / sürükleme) | V2.20 L · R |
|---|---|---|---|---|---|---|
| 90 sağ, ilk dönüşün sonunda geri | 0.27 s + boşta | 0.14 s | 5.77 | 5.63 | 3.9/6.2 · 15.6/17.5 | 4.2/7.0 · 16.2/21.2 |
| 90 sol, aynı | 0.27 s + boşta | 0.14 s | 5.77 | 5.63 | 4.6/3.0 · 17.4/35.7 | 4.6/4.5 · 7.4/28.0 |
| 90 sağ, orta | 0.30 s + boşta | 0.20 s | 6.00 | 5.90 | 4.2/6.8 · 16.6/16.0 | 4.2/6.7 · 12.2/10.6 |
| 90 sol, orta | 0.30 s + boşta | 0.20 s | 6.00 | 5.90 | 4.6/10.2 · 2.2/16.1 | 4.6/4.0 · 4.5/17.8 |
| 90 sağ, geç | 0.27 s + boşta | 0.17 s | 6.23 | 6.13 | 4.2/6.7 · 12.3/8.7 | 3.9/6.6 · 12.3/8.7 |
| 180 → erken geri | 0.23 s + boşta | 0.17 s | 5.87 (14° kalır) | 5.80 (1°) | 3.4/5.6 · 16.5/19.7 | 3.4/8.1 · 14.6/21.9 |
| −180 → orta geri | 0.20 s + boşta | 0.20 s, boşta yok | 6.03 | 6.03 | 6.1/7.7 · 16.2/21.5 | 6.1/7.7 · 15.1/21.9 |
| 90 → 180 (`t_tiprev2`) | 0.20 s + boşta | 0.20 s, boşta yok | 6.03 | 6.03 | 4.8/12.9 · 11.4/20.9 | 5.2/7.3 · 11.1/13.6 |

- **Ara adaylar ve neden düzeltildikleri:**
  - Yalnızca başlatma kapısı açıkken devir 0.03 s'ye indi. Ama montaj her 0.13 s'de yeniden tetiklendi: dört montajlık zincir ve R 43.9 cm.
  - İkinci kapıdan sonra tetik tekti. Ama açı kamera dönerken seçiliyordu: 90° isteğe 45° klip, 31° kaldı.
  - Üçüncü kapı (0.05 s durulma) bunu düzeltti.
- 0.25 s içinde geri dönen bir bakış dönüşü hiç başlatmıyor. Bu doğru: hızlı bir bakış gövdeyi döndürmemeli.
- En yüksek gövde dönüş hızı üretimle aynı (336 / 361 / 500 °/s); açı tek karede atılmıyor.

### Hedef 1: toparlama takılması — denenmiş aday ve somut engel

- **Aday:** `install_v220_recsearch.py`. Toparlama veritabanında, toparlama başladıktan 0.08–0.62 s sonra MM araması kapanıyor.
- **Telemetri:** `SHM220_Search`, `SHM220_RecWin` ve `SHM217_RecT0` harness'e eklendi (yalnızca bu üç değişken). `rhC` koşusunda pencere açık, arama kapalı. 0.215 s'lik karede klip yalnızca 1.26 → 1.30 ilerledi; sonraki karede 1.07'ye döndü.
- **Sonuç:** V2.19'daki "MM yeniden aradı" teşhisi yanlıştı.
- **Elenen diğer kaynak:** `PlayRate` aralığı ve `PlayRateMultiplier` hep pozitif ve sınırlı (0.65–1.4).
- **Engel:** Motor içi zaman yeniden hizalaması. Aday üretime alınmadı. Takılma kayıtları hata kanıtı olarak saklandı.
- **İkinci yön düzeltmesi:** V2.19'un "r0_w ikinci yön çıkışında R ~46 cm" değeri bir pencere hatasıydı; o 46 cm senaryonun **son depar duruşuydu**. Çıkışın kendisi ≤ 4.1 / 8.9 cm. Duruş aşağıda düzeltildi (48.4 → 3.1).

## İlişkili geçişler

| Olay | Kök neden (ölçüldü) | Değişiklik | Önce → sonra (30 FPS, aynı girdi) | Durum |
|---|---|---|---|---|
| **B) Depar duruşu** | 50–105 cm sürükleme vardı (V2.18 ve V2.19'da da). Eski pencereler son duruşu hiç ölçmüyordu. İki neden: (a) **içerik:** `SHM_A_RR_M_Relaxed_Run_Stop_F_L/Rfoot` klibinde arkadaki ayak 165–450 cm/s hızla, zeminden yalnızca 0.9–5.6 cm yüksekte öne süzülüyor; (b) **yön:** depar hareket yönüne bakıyor, bırakınca gövde 0.6 s içinde 90° kameraya dönüyor, kapsül hâlâ yana kayıyor | (a) `swingclear220.py`: yalnızca bu iki proje klibinde arkadaki ayak salınımda en az 8 cm'ye kaldırıldı, bacak menteşe olarak yeniden çözüldü. (b) `GR220_StopFaceHold`: gövde yön hızı ~0; koşullar: hareket girdisi 0.08 s'den uzun yok, hız > 5, kameraya göre yön farkı > 45° | İleri depar duruşu R **48.4 → 3.1**; S-kavis duruşu **21.0 → 2.4**; yan depar duruşu sağ L **103.9 → 74.7** (klip) **→ 6.4** (klip + yön tutma), sol L **105.2 → 76.4 → 6.5**. Gerçek zaman final (3 tekrar): L 96–100 → 1.9–3.7 | **Üretimde** |
| **B) Kesişin ortasında bırakma** | Duruş klibi frenin ortasından (0.93–1.00) 250–260 cm/s'de giriyor. Yön farkı < 45°, yön tutma devreye girmiyor | — | R ~26 cm, değişmedi | **AÇIK** |
| **C) Shift bırak / yeniden bas** | Hız sınırı anında tempoya düşüyor (490 → 300 cm/s, 0.25 s'de). Tempolu döngü 1.3–1.5× hızda oynuyor, ardından depar döngüsüne yeniden giriliyor | `GR220_GaitDownDecel 250`: hız sınırı, **hedef yürüyüş biçimi depardan düşükken** insan yavaşlamasıyla iniyor; gerçek hızın üstünde tutulmuyor; artışlar anında | `p_tapretrig` L **18.5 / 25.3 → 4.0 / 6.1**; `p_j2s_tap` L 9.4 / 14.4 → 3.9 / 3.1. 120 FPS: L 33.8 → 4.6. İkisi de depar döngüsünde kalıyor | **Üretimde** |
| **A) Kesiş → S** | AAMS pivot klibi 0.13'te giriyor. Yön tutma sınırından ~0.3 s sonraki ilk aramada 1.40'a atlıyor: frenin ve basışın 1 saniyesi atlanıyor. Bu her FPS'de oluyor (20 / 30 / 60 / 120). Kapsül hızını 0.6 s'de 50°'den 160°'ye ≥ 100 cm/s döndürüyor; klip 303 → 0 cm/s'yi 0.65 s'de frenleyip basıyor. V2.19'un "1.7–2.7 kat hızlı" ölçümü bu atlama | Kapsülün klibin fren yolunu izlemesi denendi (üç aday: `GR215_RevBrakeAccel 470`; `Accel 250 / Fric 0.3 / Decel 250`; `Accel 300 / Fric 0.3`) | Atlama aynı arama karesinde kaldı. Sürükleme R 20 → 38–46 | **RED, AÇIK.** Geri koşu hızı 300 cm/s (tempo sınırı) |

**Bu düzeltmelerin ara hatası ve nasıl yakalandığı:**
- **Yön tutma:**
  - (1) `RInterpTo_Constant` hız 0'da hedefe **anında atlıyor** (UE kuralı); tutma 0.01 ile yapılıyor.
  - (2) 0.1 s'lik W→S tuş boşluğu tutmayı tetikledi (`k_ws_cam` L 14 → 40); 45° kapısı eklendi.
  - (3) "Girdi yok" önce CMC ivmesinden okunuyordu. Kök hareketli bir ters adımda tuş basılıyken de sıfır okunuyordu; şimdi oyuncunun hareket girdisinden okunuyor.
- **Hız eğimi:**
  - (1) Depar kesişi hız sınırını 490 → 416'ya indiriyor. Eğim bunu yumuşattı, kesiş yolu değişti ve 120 FPS'de geç ters ayağı zemine sürtündü (L 6 → 38).
  - (2) Shift tuşuna bağlamak yetmedi: yeniden basışta hedef yürüyüş biçimi tuşun ~0.25 s gerisinde.
  - Şimdi eğim hedef yürüyüş biçimine bağlı. 120 FPS: geç ters L 5.9 (V2.19 6.0), Shift kazancı korundu.

## Girdi gecikmesi (2+1 kare)

`input_latency220.py` (PIE). Harness'in girdi verdiği kare sonundan itibaren, hareket bileşeninin girdiyi gördüğü kare:

| Yol | Kare |
|---|---|
| Enhanced Input enjeksiyonu (gerçek cihazın kullandığı yol) | bir sonraki kare (1) |
| Harness konsol tuşu (`Input.+key`) | 2 kare |

- Harness'teki "2 kare"nin bir karesi **konsol zorlamalı tuş yolundan** geliyor; üretim sırasından değil.
- Girdi vektöründen klip seçimine geçen "+1" kare üretim sırasıdır: ABP, bir önceki karedeki hareket durumunu okuyor.

## Son nedensel parti (`g30`, 30 FPS): V2.20 üretimi vs düğmeler kapalı

- Her senaryo bir kez koşturuldu; sabit adımlı koşular deterministik.
- "Kapalı" = pivot kilidi, yerinde dönüş devri, yön tutma ve hız eğimi kapalı; aynı içerik.
- Pencereler kesilmiş kopyada kalibre edildi. Tam tablo `g30_table.md` içinde.

| Olay | Kapalı (≈ V2.19) | V2.20 |
|---|---|---|
| Yan depar → bırak, son duruş, sağ | L 74.7 / 80.4 | **L 6.4 / 8.8** |
| aynı, sol | L 76.4 / 84.2 | **L 6.5 / 8.0** |
| Shift bırak / bas `p_tapretrig` | L 18.5 / 25.3 | **L 4.0 / 6.1** |
| Shift bırak / bas `p_j2s_tap` | L 15.5 / 25.3 | **L 3.9 / 3.1** |
| Çok erken ters, sağ / sol | R 12.1 / 13.0 | R 9.6 / 11.0 |
| Erken ters (+0.25 s) | L 7.2 / 19.3 | L 6.1 / 5.7 |
| Kesiş → S, kesiş penceresi | R 13.1 / 20.1 | R 10.1 / 16.7 |
| Çok erken ters + bırakma | L 6.1 / 4.1 | L 2.6 / 0.0 |
| Geç ters diz düzlemi (sürücü / görünen, °/s) | 1238 / 1205 | **537 / 522** |
| Yerinde ters devir: 90 orta sağ / sol, `t_tiprev`, 180 erken | 0.30 / 0.30 / 0.27 / 0.23 s + boşta | **0.20 / 0.20 / 0.14 / 0.17 s, boşta yok** |
| `t_tiprev2` sürükleme L / R | 12.9 / 20.9 | 7.3 / 13.6 |
| `t_tiprev` R sürükleme | 17.5 | **21.2 (daha kötü)** |
| Shift bırakma `p_j2s_rel` L · R | 3.3 / 7.6 · 11.8 / 13.5 | 6.9 / 12.6 · 4.8 / 12.0 (karışık) |
| S-kesiş R sürükleme | 12.8 | 15.4 (daha kötü, küçük) |
| Yürüyüş, eğim, basamak, yürü-dur-yürü, yürüyüş → depar (5 senaryo), tempolu → depar, geniş kavis, S-kavis, yana kaçış, ters itiş, duruştan depar, ikinci ters, normal ters giriş / çıkış | — | **değişmedi** |

- Depar duruşu klip düzeltmesi içerik olduğu için iki tarafta da var. Etkisi ayrıca ölçüldü (eski → yeni klip, 30 FPS):
  - İleri depar duruşu R 48.4 → 3.1;
  - S-kavis duruşu L 21.0 → 2.4;
  - yan duruş L 103.9 → 74.7. Kalanı yön tutma ile 6.4'e indi.

## FPS çapraz denetimi (son üretim)

- Ayak başına net / sürükleme (cm), pencere kalibrasyonlu.
- Karşılaştırma tabanı: 20 ve 120 FPS'de V2.19 (`v219x20`, `v219x120`). 60 FPS'de V2.19 ölçümü yok; taban V2.18 (`v219q60`).
- Tam liste `fps220_cmp.txt` içinde (bu dosya kalibrasyon düzeltmesinden önce üretildi).

| Olay | 20 FPS V2.19 → V2.20 | 60 FPS V2.18 → V2.20 | 120 FPS V2.19 → V2.20 |
|---|---|---|---|
| Çok erken ters, sağ | L 7.4 → **2.6**, R 5.3 → 2.4 | R 10.3 → **5.7** | R 13.3 → **9.6** |
| Çok erken ters, sol | R 2.5 / 2.3 → 1.9 / **10.7** | R 9.7 → 6.1 | — |
| Normal ters, sağ | eşit | R 23.6 → **9.6** | eşit (R 13.7) |
| Normal ters, sol | L 5.8 → 3.9 | eşit | eşit (R 22.6) |
| Geç ters | eşit | L 4.4 → **12.1** (2 karelik süzülme, aşağıya bakın) | L 6.0 → 5.9 |
| Kesiş → S | R sürükleme 21.5 → **26.5** | R 42.4 → **5.8** | eşit |
| Depar ters + ikinci ters | eşit | R 19.7 → **7.6** | — |
| Shift kısa bırak / bas (`p_j2s_tap`) | L 8.6 → **3.7** | → 3.4 | L 33.8 → **4.6** |
| Geç ters diz düzlemi (°/s) | 1033 → **565** | 1211 → **893** | 1356 → **911** |

- **60 FPS'deki geç ters L 12.1:**
  - Salınan sol ayak, ters dönüş girişinde zemine ~1 cm daha yakın geçiyor. Ölçücü bu 2 havada kareyi (`HH`) 12 cm'lik bir "temas" sayıyor. Basılı ayak kayması değil.
  - Pivot kilidi kapalıyken 5.2.
  - Dar kapsam (yalnızca geç evre, genel terim yok) bunu değiştirmedi.
  - 20 / 30 / 120 FPS'de yok.
  - Açık yan etki olarak bırakıldı.
- **120 FPS'de daha önce görülen L 38:**
  - Kaynağı hız eğimiydi: kesişin hız sınırını yumuşatıyordu.
  - Eğim hedef yürüyüş biçimine bağlandıktan sonra L 5.9.
- **Yerinde ters dönüş:**
  - 20 / 60 / 120 FPS'de aynı davranış: tek devir, arada boşta duruş yok.
  - Kayma (`t_trv2_m`): L 4.8–8.0, R 11.5–12.2.

## Gerçek zaman final (`v219f` → `v220f`)

- Takılma uyarısıyla birlikte okunmalı (yukarıya bakın). Pencere kalibrasyonu düzeltilmiş hâli `final220_table.md` içinde.
- `v220f`, yön tutma ve hız eğiminin son düzeltmelerinden önceki hâl. Son hâl `g30` ve 120 FPS ile ölçüldü.
- **Öne çıkanlar:**
  - Yan depar duruşu L 96–100 → 1.9–3.7 (3 tekrarın hepsi).
  - S-kavis duruşu R 54.7 → 0.
  - Shift kısa bırakma L 29.6 → 3.4.
  - Diz 1082–1220 → 546–625 °/s.
  - Yerinde ters devir 0.21–0.38 s + boşta → 0.15–0.24 s.
- Tek tek kötü tekrarlar takılmalı koşulardı. Örnek: çok erken ters, sağ, r1 = 77.9 cm, toparlama sırasında 0.118 s'lik kare.

## Korunan kazanımlar

Kanıt: `g30` (kapalı vs V2.20, deterministik) ve FPS partileri.

| Kazanım | Durum |
|---|---|
| Bileşen END / START düzeltmesi | Bileşene dokunulmadı. Normal ters giriş / çıkış birebir aynı. |
| AAMS yaw-snap düzeltmesi | Dokunulmadı. Ters dönüşlerde değer aynı ya da daha iyi. |
| Kamera–girdi yönü eşleşmesi | Değişmedi. Yön tutma gövde yönünü değil yalnızca dönüş hızını sınırlıyor; girdi çerçevesi aynı. |
| Rahat kollar ve yürüyüş başlangıcı | Yürüyüş senaryolarının hepsi birebir aynı (yürüyüş → depar ×5, yürü-dur-yürü). |
| Çift zemin uyumunun kaldırılması | FootPlacement değişikliği yalnızca ters / toparlama / 220 cm/s üstü yön değişiminde. Eğim ve basamak birebir aynı. |
| Recovery v8 basışı | Çok erken ters sağ / sol R 12–13 → 9.6–11 (30 FPS); 20 / 60 / 120 FPS'de eşit ya da daha iyi. |
| Düşük FPS LowStand düzeltmesi | 20 FPS'de çok erken ters L 7.4 → 2.6. Toparlama girişi aynı karede (5.25). |
| Ayrı tempolu → depar itişi ve JogLink 490 | `p_j2s` / `p_j2s_mid` / `p_j2s_dir` birebir aynı. JogLink 490 doğrulandı. |
| Yedek / test içeriğinin üretim DB'lerinden ayrı tutulması | `verify_prod220`: sızıntı yok, `None` girdi yok. Satıcı `PSD_SM_LocoTransitions` dosyası değişmedi. Yerinde dönüş klipleri V2.15 ile byte-eşit. |

**Bilinen küçük bedeller (deterministik):**
- `t_tiprev` R sürükleme 17.5 → 21.2.
- S-kesiş R sürükleme 12.8 → 15.4.
- `p_j2s_rel` L 3.3 → 6.9 (R 11.8 → 4.8).
- 20 FPS: çok erken ters sol R sürükleme 2.3 → 10.7 (net aynı), kesiş → S R sürükleme 21.5 → 26.5.
- 60 FPS: geç ters 2 karelik süzülme.

## Doğrulama

- Son üretim kaydedildi. Editör kapatılıp temiz açıldı; ardından:
  - `verify_prod220_final.txt`: **PASS**. Sızıntı yok, kirli paket yok. Bütün V2.20 düğmeleri beklenen değerde: `SHM220_PivotOn 1`, `RecHold 0`, `PivotT0 0`, `PivotNoRd 0`, `GR217_TipHand 1`, `TipHandSettle 0.05`, `StopFaceHold 1`, `StopFaceHoldMinErr 45`, `StopFaceDelay 0.08`, `GaitDownDecel 250`, `GR215_RevBrake*` 0. İki duruş klibi V2.20 sürümünde.
  - `flag_diff_v220_final.txt`: test tabanı = kaydedilmiş üretim. Tek fark `TelemetryEnabled` (yalnızca test kaydı).
- Son derleme: ABP'de `UP_TO_DATE_WITH_WARNINGS`. Uyarı, MM düğümünün pin zincirindeki eski bir `IsValid` iş parçacığı uyarısı; V2.20 düğümleri `IsValid` kullanmıyor. Pawn `UP_TO_DATE`.
- Kullanıcı değişikliklerine dokunulmadı. Her kurulum yalnızca kendi açtığı kirli paketleri yeniden yükledi.

## Kayıtlar

- Gerçek zaman, 30 fps yakalama. Kırpılmamış, düzenlenmemiş kareler; yalnızca PIE'de kil test görünümü.
- `vid/`: GIF gerçek hız, `_realtime.avi` gerçek zaman, `_slow3x.avi` 1/3 hız. `img/`: kontak sayfaları.
- **ON / OFF:** ON = V2.20 üretimi, OFF = V2.20 düğmeleri kapalı, aynı içerik.
- **Revizyon notu:** Kayıtlar yön tutmanın ve hız eğiminin son düzeltmelerinden önce alındı. Görülen davranış aynı:
  - depar durunca gövde yönünü koruyor (son hâlde 0.08 s'lik bırakma beklemesi var);
  - Shift kısa bırakılınca depar sürüyor.

| Konu | Dosyalar |
|---|---|
| Geç ters diz | `laterev_knee_off_diag`, `laterev_knee_on_diag`, `laterev_knee_on_side`, `img/late_reverse_knee_off_on.jpg` |
| Yerinde ters devir | `tiprev_off_diag`, `tiprev_on_diag`, `tiprev_on_game`, `tip180rev_off_diag`, `tip180rev_on_diag`, `img/tip_reverse_off_on.jpg`, `img/tip180_reverse_off_on.jpg` |
| Depar duruşu | `sprintstop_facing_off_side`, `sprintstop_facing_on_side`, `sprintstop_facing_on_diag`, `sprintstop_left_on_game`, `sprintstop_fwd_on_side`, `img/sprint_stop_facing_off_on.jpg` |
| Shift bırak / bas | `shift_repress_off_side`, `shift_repress_on_side`, `jogtap_on_diag`, `img/shift_repress_off_on.jpg` |
| Toparlama ve açık takılma hatası | `earlyrev_right_diag`, `earlyrev_left_diag`, `earlyrev_stall_open_side`, `earlyrev_stall_open_diag`, `img/recovery_stall_open.jpg` |
| Açık olanlar | `cutback_open_diag` (kesiş → S), `cutrelease_open_diag` (kesişte bırakma), `tiprev_w_open_diag` (yerinde ters + W), `img/cut_to_s_open.jpg` |
| Korunanlar | `slope_jog_side`, `restart_side`, `slope_chain_diag` |

**Teknik görsel değerlendirme (kullanıcı kabulü değil):**
- **Depar duruşu:** OFF'ta gövde kayarken 90° kameraya dönüyor, geniş bir hamle duruşu oluşuyor. ON'da gövde koştuğu yöne bakarak, ayaklar altında duruyor. Daha doğal.
- **Yerinde ters dönüş:** ON'da yeni dönüş, adım atan pozdan doğrudan başlıyor; arada boşta duruş yok.
- **Diz:** Kontak sayfası çözünürlüğünde fark ince. Sayısal düzlem hızı yarıya iniyor.
- **İleri depar duruşu:** Fren adımı hâlâ uzun ve biraz atletik.

## Açık kalanlar

1. Toparlama takılmasında geri sarma (Hedef 1). Motor seviyesi; aday kapalı.
2. Kesiş → S pivotunda 1 saniyelik atlama (A). Kapsül fren adayları reddedildi.
3. Kesiş ortasında bırakmada duruşa giriş: R ~26 cm.
4. Yerinde ters dönüşte W: L 28 cm (V2.19'da da). Tam 180°'lik ters istek eski ters-açı aralığının dışında.
5. Diz kazancı 60 / 120 FPS'de daha küçük (~%30; 30 FPS'de %57).
6. Daha önce bulunan, düzeltilmeyenler:
   - `SHM213_MontTick` her karede boş bir pawn okuyor; oturum başına on binlerce PIE hata satırı.
   - Hızlı S-kesişte (`chain_sscut`) depar kavis döngüsü 310 cm/s'de 0.53× hızda (yavaş çekim) oynuyor; L ~55–60 cm.

## Dosyalar ve geri alma

- Kod ve graf özetleri `CHANGES_V220.md` içinde (betiklerin kendi açıklamaları).
- Geri alma noktaları:
  - V2.19 tabanı: `Saved/Codex/SHME_V220_20261021/checkpoint/baseline_v219`.
  - Duruş klipleri: `checkpoint/pre_stopclear`.
  - Yükseltme öncesi: `checkpoint/pre_promote`.
