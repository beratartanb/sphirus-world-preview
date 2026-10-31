# Sphirus World v5: gerçek patika eğrisi, kamera kaplanması, 16 m'lik kompozisyon pilotu P1 (PLAN, uygulanmadı) (2026-10-31)

v4'teki E1–E3 uygulanmadı.

**Bu turda değişmeyenler:**
- Sahne, asset ve kalıcı ayar değişmedi; kayıt yapılmadı; editör yeniden başlatılmadı.
- Editöre yalnız `measure` (salt-okunur) ve `pie` işleri gönderildi. PIE içinde piyonun yeri ve kontrol yönü geçiciydi.
- Konsol komutları: `Input.+key`, `csvprofile`, `HighResShot`.
- Dirty paket listesi her adımdan sonra aynı: yalnız iki ABP. Korunmaya devam ediyor; kaydedilmedi, sıfırlanmadı.

**Kanıtlar:**
- `v5/before/`: "önce" videosu, kareler, istasyon kareleri
- `v5/plan/`: hareket listesi, kuşbakışı harita, kaplanma tahmini
- `v5/camera/`: bitki materyalleri
- `v5/data/`: ölçümler ve performans CSV'si

---

## 1. Yürüyüş artık gerçek patika eğrisini izliyor (DOĞRULANDI)

- **Patika kaynağı:** projede yetkili bir çizgi var: `TRAIL` polyline'ı (`Tools/AAAPolishRear20260923/design_terrain.py`). 23 Eylül'deki arazi oyulması ve 24 Eylül'deki yapısal geçiş bu çizgiye göre yapılmış. v4'teki sabit yaw −92 yürüyüş, (3080, −2300)'den sonra bu çizgiden ayrılıyordu.
- **Segment:** çizgi üzerinde 16.5 m. Başlangıç (3074, −1692), bitiş (2498, −3154).
- **Yönlendirme:**
  - W basılı, yürüme hızı;
  - kontrol yönü her karede 2.5 m ilerideki çizgi noktasına doğru çevriliyor, en fazla 90°/s (oyuncunun fareyle yön vermesi gibi);
  - pitch −5°.
- **A geçişi (kayıtlı):**
  - 12.8 s oyun zamanı, 385 kare (30 FPS sabit adım = gerçek hız);
  - patikadan ortalama sapma 10.5 cm, en fazla 36 cm;
  - hız 127 cm/s.
  - Video: `v5/before/BEFORE_trail_curve_walk_12.8s_realtime_s60.avi`.
- **İstasyonlar** (s = 2 / 8 / 14 m; yaklaşma / sıkışma / açılma): ileri, sol 90°, sağ 90°, geriye bakış. 14 m'de ayrıca **evin yönüne** (yaw 117°) bir kare. Toplam 13 kare.
- **Düzeltilen bir ölçüm hatası:**
  - İlk denemede yer izi, patikanın 2 m yanındaki bir `SM_PineTree03` örneğinin karmaşık çarpışmasına 22–30 m yükseklikte çarptı; piyon havaya konuldu.
  - Bitki aktörü yok sayılarak düzeltildi ve tekrarlandı.
  - Hatalı denemenin verisi kullanılmadı.

**Videoyu gerçek zamanlı izlemedim.** Değerlendirme saniyede bir kare kâğıdına ve 13 istasyon karesine dayanıyor.

## 2. Eğim: patika doğal ve oynanabilir (DOĞRULANDI)

Araziden ölçüldü; bitki ve diğer mesh'ler yok sayıldı:

| | Değer |
|---|---|
| 2 m pencerede eğim | **1.8–8.8°**. İlk 2 m'de en dik: 8.3°. 5–15 m arası 1.8–5.4° |
| Yan eğim (±0.75 m) | −4.9 … +4.8° |
| Karakter sınırları | yürünebilir zemin 44.8°, basamak 45 cm, yürüme 132 cm/s |

- **v4 düzeltmesi:** v4'te raporlanan 21–23°, düz yürüyüşün patikadan çıkıp yokuş şevine tırmanmasından geliyordu. Patikanın kendisinde öyle bir bölüm yok.
- **Sonuç:** Orman patikası için doğal ve rahat bir eğim. Zikzak ya da basamak gerekmiyor. Yokuş tarafındaki dik şev (doğu) kapalılık hissini veriyor; korunmalı.

## 3. Geriye bakışta ev (DOĞRULANDI: arazi izin veriyor; bitki örtüsü kapatıyor)

- Segment boyunca 9 noktadan, göz hizasından evin çatısına ve üst köşelerine bakıldı. **Arazi hiçbir noktada engellemiyor.**
- Çarpışmalı geometriye atılan izler çoğunlukla doğrudan evin çatısına ulaşıyor. Birkaç noktada araya çarpışmalı büyük ağaçlar giriyor.
- **Sıkışma istasyonu sol 90°:** ev sisin içinden **zaten görünüyor**; sığınak anı bu segmentte var.
- **Açılma istasyonu, evin yönü:** ev **görünmüyor**. Sight line'ı 3.5–5.7 m'deki çarpışmasız genç çam ve ladinler kapatıyor (`before/stills/release_house.png`).
- Bu yüzden açılmada bir geriye bakış penceresi **seçenek** olarak önerildi (G4). Zorunlu değil, çünkü sığınak görünümü sıkışmada zaten var.

## 4. Kamera ve bitki örtüsü: neden oluyor, çözüm ne?

**Ölçülenler:**
- Canlı kamera düzeni:
  - yay kolu 300 cm, çarpışma testi açık, prob 12 cm, Camera kanalı;
  - kamera gecikmesi açık (hız 10);
  - çalışırken FOV 60 (kamera yöneticisi bileşen değeri olan 100'ü eziyor).
- Pilot alanındaki **tüm** genç çam, ladin, çalı ve eğrelti örnekleri `NO_COLLISION`, yani Camera kanalını yok sayıyor. Büyük ağaçlar, kayalar ve ölü gövdeler ise Camera kanalını engelliyor.
- **Patikayı izleyen yürüyüşte:**
  - kamera hiçbir taç içine **girmedi** (v4'te patika dışına çıkıldığı için ~2 s içerideydi);
  - ~8–10 m'de bir `SM_Pine_Juvenile_01` (s 10 m, sağda 1.72 m, boy 3.7 m, taç yarıçapı ~1.1 m) yaklaşık 24 kare (~0.8 s) boyunca yakın planı dolduruyor;
  - bu genç çamın tacının kenarı patika merkezine yalnız 58 cm.
- **Materyaller:**
  - genç çam ve eğrelti: `M_Object_Wind_Foliage` (masked);
  - çalılar: `M_Foliage` (masked) + `M_EX_RefugeShrubBark`;
  - genç ladinler: `MM_Tree_Foliage_01` (**opak**);
  - `Pine_08`: `MA_Pine` (masked).
  - Hiçbirinde kameraya yakın soldurma ya da dither parametresi **yok** (`camera/foliage_materials.json`).

**Çözüm, iki katman** (kamera sistemine bu turda dokunulmadı):

1. **Yerleşim kuralı** (bu pilotta, G1): göz hizasındaki (1.2–2.3 m) yumuşak uzun bitkilerin tac kenarı patika merkezinden **≥ 1.0–1.2 m**. Opak ladinler kamera yakın alanına hiç girmez. Bu bir koridor temizliği değil; yalnız tacı patika üstüne taşan örneği yarım metre dışarı iter.
2. **Kamera tarafı** (ayrı onay; sahibi materyal + kamera):
   - **Önerilen:** masked bitkiler için **proje sahipli** bir yakın-kamera dither'ı. Örneğin piksel derinliği 30–110 cm arasında `DitherTemporalAA` ile opacity mask yumuşatılır. AGENTS gereği satıcı ana materyalleri değişmez; proje sahipli kopya veya örnek gerekir.
   - **Önerilmeyen:** bitkiye kamera çarpışması vermek. Sık bitkide kamera sürekli ileri-geri pompalar.
   - **Daha geniş seçenek:** yoğun bitki bölgelerinde kolu kısaltan veya omuz tarafını değiştiren bir kamera davranışı. `sphirus-camera-direction` kapsamında ayrı iş.

## 5. 16 m'lik bölgenin kompozisyonu: sorun ve yeni plan

### Önce (gözlem + envanter)

Envanter: segmentin 14 m çevresinde 1013 örnek. "Sağ", yürüme yönünün sağı = yokuş tarafı.

| Bölge | Büyük kütle | Orta / küçük | Okunma |
|---|---|---|---|
| **Yaklaşma 0–5 m** | Kök plakası, sarmaşıklı büyük gövde, şev (sağda 7 yapısal öğe) | Sağ orta bantta 16 uzun yumuşak bitki | **En güçlü kısım.** Patika şev ve kök plakasıyla okunuyor; geriye bakış iyi |
| **Sıkışma 5–11 m** | Sağ şevde yapısal öğe yok; sağ 90° düz bir yosun şevi | Sağ kenarda 4 uzun (biri kamerayı sıyırıyor), solda seyrek | Patika iz olarak var; yokuş tarafı yapısız; evin görünümü sol tarafta |
| **Açılma 11–16.5 m** | Sağ ileride bir kaya levhası | Sol orta bantta 14 uzun + 14 orta + 35 alçak; patikada yalnız alçak örtü | **Patika açık yosun yamacında eriyor;** zemin her yerde aynı. Evin yönünü genç ağaç kümesi kapatıyor |

### Plan P1: yalnız mevcut örneklerin yerini değiştirmek

- 13 örnek taşınıyor; sayı aynı kalıyor.
- Yeni asset yok; ışık ve arazi değişmiyor; koridor açılmıyor.
- **Yaklaşma bölümüne dokunulmuyor.**

| Grup | Ne | Neden (ritim) |
|---|---|---|
| G1 yakın alan (1) | Patikanın 58 cm'ine kadar taşan genç çam 51 cm şeve doğru, dışarı | Sıkışma korunur; kamera artık tacı sıyırmaz |
| G2 sıkışma (3) | Yokuş şevine 2 genç ladin (3.2 m ve 4.3 m'ye; uzaktaki seyrek bölgeden) + pilot alanındaki bir ölü çam gövdesi şev boyunca, patikaya paralel +12° | Yokuş tarafına **büyük yatay kütle** + orta dikeyler. Asimetrik baskı: sol (ev) tarafı geçirgen kalır. Gövde, açılmaya doğru bir yönlendirme çizgisi olur |
| G3 iz kenarı (6) | Açılmadaki yamaçtan 6 eğrelti, patikanın 0.9–1.4 m'sine; iki yana dönüşümlü, 1.5–3 m aralıklı, düzensiz | **Taban, kenar bitkileri arasındaki bant olarak okunur.** Temiz kahverengi şerit değil; AGENTS'teki "kesintili bitki" şartı |
| G4 geriye bakış penceresi (3, **seçenek**) | Açılma istasyonundan evin yönündeki çizgide duran 3 genç ağaç, çizgiye dik 1.8 m kaydırılır | Ağaçlar arasında dar bir pencere; açıklık değil |

**Kanıtlar ve tahmin:**
- Kuşbakışı harita: `plan/plan_p1_map.png`.
- Örnek başına tam transformlar (eski ve yeni; uygulama ve geri alma listesi): `plan/plan_p1_resolved.json`. Yer yükseklikleri araziden alındı, zemin üstü yükseklik korundu.
- Prova işi (salt-okunur) 13 örneği canlı olarak doğruladı; uyumsuzluk yok.
- **Tahmin:** aynı kamera izinde, kameranın bitkiye sürtündüğü kare sayısı **24 → 0** (`plan/predicted_cam_occlusion_p1.json`; sınır kutusu tabanlı bir yaklaşık hesap).

### Değişecek örnekler (özet)

Tamamı `plan_p1_resolved.json`'da.

| Grup | Mesh | Bileşen # / indeks | Konum önce → sonra (x, y, z cm) | Yaw | Mesafe |
|---|---|---|---|---|---|
| G1 | SM_Pine_Juvenile_01 | 1 / 8 | (3028.6, −2720.8, 442.9) → (3072.7, −2747.3, 481.2) | 155.3 | 51 cm |
| G2 | SM_Young_Black_Spruce_01 | 76 / 128 | (3853.0, −3581.0, 985.6) → (3320.8, −2520.6, 542.5) | 69.9 | 11.9 m |
| G2 | SM_Young_Black_Spruce_02 | 77 / 127 | (3711.0, −2979.0, 680.1) → (3322.5, −2731.6, 560.5) | 78.7 | 4.6 m |
| G2 | SM_PineDeadTrunk03 | 23 / 5 | (3424.0, −3073.0, 621.1) → (3233.3, −2549.8, 506.9) | 33.9 → −109.0 | 5.6 m |
| G3 | SM_Fern02 | 67 / 75 | (3274.0, −3564.0, 756.6) → (2894.6, −2813.0, 401.7) | 34.9 | 8.4 m |
| G3 | SM_FernWild01 | 19 / 113 | (3315.0, −3367.0, 700.8) → (2628.7, −2797.4, 389.2) | 44.2 | 8.9 m |
| G3 | SM_FernLong01 | 17 / 27 | (2008.1, −2633.1, 388.9) → (2740.8, −3001.7, 394.1) | 40.0 | 8.2 m |
| G3 | SM_FernWild01 | 19 / 28 | (2175.0, −2500.7, 374.3) → (2513.5, −2974.1, 406.1) | −97.5 | 5.8 m |
| G3 | SM_Fern02 | 67 / 58 | (2165.0, −2538.0, 384.0) → (2660.0, −3167.4, 428.3) | 72.7 | 8.0 m |
| G3 | SM_FernLong01 | 17 / 171 | (3126.5, −3361.3, 642.5) → (2409.1, −3057.1, 397.5) | 24.3 | 7.8 m |
| G4 | Pine_08 | 81 / 28 | (2475.0, −2657.0, 341.8) → (2315.2, −2739.8, 352.6) | −154.4 | 1.8 m |
| G4 | SM_Young_Black_Spruce_02 | 77 / 200 | (2417.0, −2518.0, 393.5) → (2257.2, −2600.8, 423.0) | 124.0 | 1.8 m |
| G4 | SM_Pine_Juvenile_01 | 1 / 176 | (2419.0, −2440.0, 376.8) → (2578.8, −2357.2, 314.8) | −53.7 | 1.8 m |

**Bilinen riskler**
- **Taç örtüşmesi:** bazı hedefler komşu taçlarla örtüşüyor (G4'te 4–7 komşu). Sık ormanda normal, ama iç içe geçen ağaçlar yapay görünebilir. Uygulamada görsel olarak kontrol edilip gerekirse 0.5–1 m ayarlanır.
- **Boşalan yerler:** G2 ladinleri ve G3 eğreltileri 5–12 m öteden alınıyor. Eski yerlerde küçük boşluklar oluşur. Bunlar yokuşun uzak bandında ve açık yamaçta, çok örnekli bölgelerde; yine de "sonra" setinde bakılacak.

## 6. Performans "önce" (DOĞRULANDI)

Stok `csvprofile`, B geçişi, kayıt kapalı, editör PIE, viewport 1741×922.

| | Kare süresi ort. / p95 / maks | GPU ort. / p95 | Oyun thread'i | Render thread'i | VRAM |
|---|---|---|---|---|---|
| ÖNCE | 42.1 / 45.2 / 48.2 ms | 40.6 / 42.9 ms | 15.7 ms | 42.1 ms | 6327 / 7122 MB |

Pilot örnek sayısını değiştirmediği için beklenen fark gürültü düzeyinde. "Sonra" ölçümü aynı yöntemle alınacak.

## 7. Onay istenen adımlar (hiçbiri yapılmadı)

**Aşama A: belleğe uygulama + "sonra" seti, KAYIT YOK**
1. Manifest + doğrulanmış yedek: `L_GR_SphirusHouse.umap` (`manifest233.py`). Bitki örtüsü bu paketin içinde; dış aktör paketi değil.
2. Tek bir kapılı `write` işi 13 transformu uygular (`update_instance_transform`), kaydetmez. G4 ayrıca açılıp kapatılabilir.
3. Aynı ölçümler tekrarlanır: aynı yürüyüş (eğri, 12.8 s), aynı 13 istasyon karesi, CSV performans, kamera kaplanma ölçüsü, `trail_audit`.
4. Önce/sonra video ve kareler yan yana raporlanır.
5. **Geri alma:** `plan_p1_resolved.json`'daki özgün transformlar aynı işle geri yazılır, ya da harita kaydedilmeden yeniden yüklenir. Bu sırada iki ABP'ye dokunulmaz; runner'ın kayıt koruması yalnız manifestteki haritaya izin verir.

**Aşama B: kalıcı hale getirme (A'nın görsel kabulünden sonra, ayrı onay)**
- Yalnız `L_GR_SphirusHouse` kaydı.
- AGENTS gereği Bridge dışa aktarımı ve `LATEST.json` doğrulaması.
- Bundan önce editörün yeniden açılması önerilir: hem ABP'ler kaydedilmeden atılmış olur, hem uzun PIE sonrası viewport tuzağı temizlenir.

**Ayrı iş:** masked bitkiler için proje sahipli yakın-kamera dither'ı (materyal ve kamera sahipleri).

## 8. Eksikler / doğrulanmamışlar

- "Sonra" görselleri, yürüyüşü ve performansı: Aşama A onayına bağlı.
- Kaplanma tahmini yaklaşık; gerçek sonuç Aşama A yürüyüşünde ölçülecek.
- Videolar gerçek zamanlı izlenmedi.
- Disk ile bellek arasında tam ABP karşılaştırması: geri dönüşten sonra yapılacak (v4 planı).
