# GD18 — Overlay ile kanıtlanmış burun anatomisi, çene formu ve ağız derinliği

Tarih: 2026-10-10. Başlangıç ve geri dönüş noktası GD17 G17; GD17'ye dokunulmadı.

Final aday **G18**. Durum: **PARTIAL**. Teknik testler geçti; görsel benzerlik kabulü senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** Tüm UE varlıkları `/Game/Sphirus/CharacterLab/GD18_IdentityMaster_20261010` altında, yalnızca test amaçlı. Kaynaklar `SourceAssets/Characters/GD18_IdentityMaster_20261010` altında: `GD18_IdentityMaster.blend`, GLB/OBJ, sculpt verisi, op dosyaları ve araçlar. GD14 W9, GD15, GD16, GD17 kaynakları ve GD17'nin görünüm (skin/iris/kaş) varlıkları yalnız okunarak kullanıldı.

## 1. Teşhis: overlay'ler ne gösterdi?

Yöntem: Referans fotoğraflarının her biri için GD13'te çözülmüş kamera (konum, odak, dönüş) kullanıldı. GD17 bu kameralarla hem UE'de gerçek materyalle, hem Blender'da kil olarak render edildi; referans panelin üstüne **%50 saydamlıkla** bindirildi. Hiçbir görüntü deforme edilmedi, ölçeklenmedi veya kaydırılmadı. Ek olarak kırmızı/cyan fark görüntüsü (kırmızı = referans, cyan = model) ve aynı cilt-anahtarı yöntemiyle çıkarılan silüet kontur kalıntıları (px; ön/3-4 ≈ 0,65 mm/px, profil ≈ 0,71 mm/px) kullanıldı. Panolar: `boards/O1–O3`.

Dört görünümde tutarlı farklar (yalnız bir görünümde görülenler atlandı):

| Bölge | Kanıt | Fark (GD17 → referans) |
|---|---|---|
| Burun ucu lobülü | Profil satır kalıntıları 232–252: model +0,7…+3,8 px önde, en öndeki nokta referansın pronasalesinden ~5 mm aşağıda | Lobül dikeyde fazla uzun ve alçak; referansın ucu kompakt ve daha yukarıda |
| Kolumella / infratip | Profil 262–264: +7,2 / +5,0 px (model 3,5–5 mm önde) | Kolumella sarkıyor |
| Kanat kenarları | Ön ve 3-4 overlay: modelde burun delikleri büyük oval, referansta küçük; kanat kenarı 3B'de sill'in 1,2 cm üstünde | Lateral kanat kenarı çok yüksek (retraksiyon görünümü) |
| Burun sırtı genişliği | Ön kırmızı/cyan: yan duvarlar boyunca kırmızı (referansın yan duvarı ışık alıyor) | Referansın sırtı daha geniş ve yumuşak; modelde keskin, dar sırt |
| Radix | Profil 194–202: +1…+3 px | Model radix'i fazla dolu (GD16'dan beri biliniyor) |
| Üst dudak tabanı | Profil 283–293: +3…+11 px | Model ağzı belirgin biçimde önde; referansın üst dudağı burnun altında dik ve geride |
| Labiomental oluk | Profil 316–322: +2,7…+6 px | Modelde oluk sığ, bölge şişkin |
| Çene yastığı alt yarısı | Profil 334–355: −1…−5 px | Referansın yastığı altta daha önde ve yuvarlak |
| Çene uzunluğu | Ön overlay'de çene alt kenarı referansın altında; profil alt-çene çizgisi +3,4 px | Model çenesi ~2–3 mm uzun |
| Çene alt köşeleri | 3-4 uzak kontur 365–381: +3…+7 px (sağ), sol 3-4 eşleşiyor | Alt köşeler kare; referans yuvarlak U |

Doğrulanan ve dokunulmayanlar: alın, kaş kemiği, kapaklar, elmacık, orta/alt yanak, çene açısı, kafatası, boyun, kulaklar (hepsi 0,000 mm değişim). Ön alt yüz silüeti GD17'de zaten ±1 px içindeydi; genişlik silüetten değil, yastık/köşe formundan düzeltildi.

## 2. Müdahaleler (yalnız kanıtlı bölgelere)

Hepsi `ops/` altında anatomik adlarla, simetrik, plato maskeli yumuşak alanlar (GD13 sculpt operatörleri). Rastgele Smooth, preset veya PCA kullanılmadı.

**Burun (`N18C.json`)**
- Kıkırdak sırt +0,6 mm (GD17'de kaybolan düz sırt çizgisi).
- Uç lobülünün ön yüzü yukarı doğru sıkıştırıldı (z-ölçek 0,78, pivot z 159,55; alan y ≥ 14,4 ile sınırlı, böylece burun deliği çatısı ve kolumella yerinde kaldı): pronasale 3,4 mm yukarı çıktı, projeksiyon korundu (y 15,48 → 15,46).
- Lobül yuvarlatma (+0,55 mm normal), lobülün alt ön yüzü −1,2 mm.
- Kolumella −1,2 mm geri / +0,5 mm yukarı.
- Lateral kanat kenarları −1,0 mm (medial "soft triangle" dışarıda bırakıldı; daha fazlası ince kenarı katlıyor).
- Kanat lobülü, kanat-yanak oluğu ve nazofasiyal oluk için 0,3–0,45 mm'lik yumuşak dolgular; yan duvarlar +0,6 mm (sırt plateau genişliği z 161,5'te 1,07 → 1,17 cm).

**Çene (`C18c.json`)**
- Labiomental oluk −1,4 mm (ölçülen derinlik 2 mm arttı).
- Alt yastık +1,5 mm öne (pogonion y 12,86 → 13,01).
- Çene altı +2,0 mm yukarı (menton z 151,47 → 151,67).
- Alt çene %8 daraltıldı (pürüzsüz x-ölçek: z 152'de genişlik 4,55 → 4,22 cm; mentolabial seviye 5,63 → 5,68 cm korundu).
- Prejowl 0,45 mm dolgu. Gonial, masseter, çene sınırı, yanaklar: 0,000 mm.

**Ağız derinliği ve radix (`P18d.json`)**
- Radix −0,9 mm.
- Üst dudak −3,2 mm, alt dudak −2,2 mm, tüm dudak kalınlığı birlikte (düzgün derinlik). Vermilyon şekli ve GD17'nin uç inceltmesi korundu; ağız köşeleri sabit.

## 3. Adaylar

| Aday | İçerik | Karar |
|---|---|---|
| A | Burun (ilk sürüm) + çene | Reddedildi: uç lobülü hâlâ uzun/alçak, supratip +1 mm önde; çene altı geniş ve düz |
| B | A + radix + dudak derinliği (−2,2/−1,5) | Reddedildi: A'nın burun sorunu sürüyor; dudak etkisi yetersiz |
| C | Lobül sıkıştırma + köşe hareketi + dudak (−2,8/−1,8) | Reddedildi: çene alt köşelerinde kilde tümsekler |
| D | C'nin burnu + pürüzsüz çene daraltma + dudak (−3,2/−2,2) | Rig'e kadar götürüldü, UE yakın planında reddedildi: lobül sıkıştırma alanı burun deliği çatısını ve kolumellayı da 1,4–2,1 mm yukarı taşımış, delikler büyümüş (`process/21–22`) |
| **E = G18** | D'nin tamamı, lobül sıkıştırma alanı y ≥ 14,4 ile sınırlı (delik çatısı ve kolumella yerinde) | Seçildi |
| F2 | E + kanat kenarını vestibül duvarıyla 1,6 mm indiren uzun alan | Reddedildi: kanat tabanında 13 ters üçgen |

Ara adımlarda kanat kenarı hareketinin kapı (gate) parametreli ve medial erişimli sürümleri 8–31 ters üçgen üretti; hepsi elendi. Pano: `boards/G1` (A/B), `process/13–22` (C/D/E).

Dürüst not: E'de burun delikleri GD17'dekiyle aynı boyda kaldı; referansın daha küçük delikleri için kanat kenarının 2–3 mm daha aşağı sarkması gerekiyor. Bu, mevcut topolojide ince kanat kenarını katlıyor (F2); ancak kanat çevresinde yerel topoloji/yeniden örnekleme ile mümkün. Açık kalan madde.

## 4. Sonuç ölçümleri

Profil bantları (sabit çözülmüş profil kamerası, px; + = model önde):

| Bant | GD16 | GD17 | **GD18** |
|---|---|---|---|
| Radix | 3,06 | 3,12 | 3,66 |
| Üst sırt | 0,36 | −0,12 | 0,38 |
| Alt sırt / supratip | −0,52 | −1,56 | 0,54 |
| Uç | −0,55 | −0,97 | 1,22 |
| Kolumella / subnazale | 2,09 | 2,58 | 1,18 |
| Subnazale / üst dudak | — | +8,2 | +6,8 |
| Çene yastığı | — | −1,5 | −0,3 |

Sculpt aşamasında (G18S = E): supratip +0,59, uç +1,24, kolumella +1,06, çene yastığı −0,2, üst dudak bandı +6,8 (GD17 +8,2). Üst dudak bandının hâlâ pozitif olmasının nedeni: ölçüm satırları vermilyonun üstünde ve referansın dudağı modelden daha geride; 3,2 mm'lik geri alma farkın yaklaşık üçte birini kapattı. Daha fazlası ağız şeklini değiştirmeye başlar, bu yüzden burada durdum.

Bölge değişimleri G17S → G18S (`data/G18S_region_changes.json`): burun ≤ 3,7 mm, dudaklar ≤ 3,8 mm, çene ≤ 3,6 mm, submental ≤ 2,4 mm, glabella/radix ≤ 1,0 mm; alın, şakak, elmacık, yanaklar, çene açısı, kafatası, boyun, kulaklar 0,000 mm; üst kapak ≤ 0,57 mm (radix alanının medial kantusa uzanan kenarı; kapak-göz küresi ilişkisi değişmedi).

## 5. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,034 mm, p95 0,18, p99 0,38, en fazla 1,16 mm; GD16/17 ile aynı glabella noktaları) |
| Otomatik rig, DNA, 858 morph, ABP_Face_PostProcess | **PASS** (otomatik rig ok, DNA, 858 morph) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,034 mm, en fazla 1,16 mm; GD17 → GD18 rig sonrası ortalama 0,40 mm, en fazla 3,84 mm) |
| Ters üçgen | **PASS** (0) |
| Keskin kıvrım | **PARTIAL** (7 sınırda; GD17'dekilerle aynı: 6 doğal kenar + 1 üst dudak sınırı; yeni yok) |
| Üçgen alan oranı min | 0,25 sculpt / 0,28 rig sonrası (GD17 0,29; lobül alt yüzünde) |
| Göz kapağı ve göz küresi | **PASS** (değişmedi: 361/300) |
| Kaş ve kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, gövde animasyonu, saç simülasyonu | **NOT_TESTED** (C: sürücüsünde 2,9 GB boş) |
| Yeniden üretim | **PASS** (`tools/build_gd18.sh` G17S'ten G18S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD18 klasörleri dışında dosya değişmedi; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel benzerlik kabulü | **NOT_TESTED** (senin incelemen) |

## 6. Panolar

| Pano | İçerik |
|---|---|
| `O1–O3` | Teşhis: GD17 overlay'leri (tam yüz, burun ve çene yakın plan; gerçek + kil) |
| `O4_*` | Sonuç overlay'leri: dört görünüm, satırlar GD17 gerçek / GD18 gerçek / GD17 kil / GD18 kil |
| `O5`, `O6` | Burun ve çene yakın plan overlay'leri (REF / GD17 / GD18) |
| `A2` | Profil çizgileri (REF / GD17 / GD18) |
| `C2–C6` | Kil: Blender (iki ışık) ve UE yakın plan (gerçek + kil) |
| `D1`, `D2`, `D4` | Tam yüz gerçek materyal: REF / GD17 / GD18 |
| `E` | Deformasyon haritası GD17 → GD18 |
| `F1–F3` | Rig, ifade ve LOD |
| `G1` | Adaylar A / B (kil overlay) |

Tüm görseller gerçek render; üzerine boyama yapılmadı. GD17 ve GD18 aynı görünüm (s1t6n cilt, h6 iris, c4 kaş, h75c saç), aynı ışık ve aynı kameralarla alındı.

## 7. Disk ve kaynaklar

C: sürücüsünde 2,2–3,0 GB boş alanla çalışıldı. GD17'nin yakalamaları pano için GD18 klasörüne geçici kopyalandı ve pano üretildikten sonra silindi (`data/report_tmp_copies.txt`); GD17 orijinalleri yerinde. Önceki sürümlerin hiçbir dosyası değiştirilmedi.

Rölyef (yüksek frekans pürüz, mm): burun sırtı 0,026 → 0,026, uç lobülü 0,073 → 0,084, kanatlar 0,045 → 0,062 (kanat kenarı/lobül op'ları küçük bir pürüz ekledi; GD16'nın 0,087 uç değerinin altında), çene yastığı 0,037 → 0,039.

## 8. Açık kalanlar

- Üst dudak profilde hâlâ referanstan ~2–3 mm önde; onaylarsan bir sonraki adımda ağız şeklini bozmadan 1–1,5 mm daha alınabilir.
- 3-4 sağ görünümde çenenin uzak alt köşesi referansın 2 mm dışında; sol 3-4 ve ön görünüm eşleşiyor (referans panellerinin kendi asimetrisi).
- Radix hâlâ ~1,5 mm dolu (GD16'dan beri kabul edilen profil).
