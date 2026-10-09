# GD13: orijinal referanslardan anatomik yüz kimliği yeniden kurulumu (Identity Master)

Tarih: 2026-10-09. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Unreal'daki hiçbir varlık değiştirilmedi.

| | |
|---|---|
| Yeni kaynak | `SourceAssets/Characters/GD13_IdentityMaster_20261009/GD13_IdentityMaster.blend` (düzenlenebilir `GD13_Head` + salt-okunur `GD12_Head_READONLY` / `F1H_Head_READONLY`, 4 çözülmüş referans kamerası (arka planda referans paneli), 5 inceleme kamerası, ışık A / B) |
| Dışa aktarım | `export/GD13_IdentityMaster.glb`, `export/GD13_IdentityMaster.obj` (deri + göz, 25 975 kullanılan vertex). Yerel; büyük binary olduğu için GitHub'a yüklenmedi |
| Tam DNA sırası | `data/head_GD13.npy` (33 845 vertex, MetaHuman DNA sırası korunuyor) |
| Taban | GD11 F1H (GD12'nin de tabanı). Yeni referanslar birincil kaynak |
| Tarif | `tools/build_gd13.sh` F1H'den GD13'ü birebir yeniden üretir (yeniden üretim farkı 0.0 mm) |
| Referanslar | `data/references.txt` |

---

## 1. Referanslar yeniden alındı ve doğrulandı

**Birincil kaynak:** kullanıcının bu mesajda verdiği 6 açılı sayfa (1448 × 1086).
- `references/` altına orijinali ve açık adlı panel kesitleri kaydedildi.
- Paneller arasında ayırıcı çizgi yok; bitişik sınırlar x 483 / 966, y 541.

| Panel | Ne gösteriyor | Çözülen kamera (baş pozu) |
|---|---|---|
| front | Ön; baş hafifçe sola dönük | yaw −5°, pitch +2° |
| q3_faceR | 3/4, sağ yüz yarısı | yaw −40° |
| q3_faceL | 3/4, sol yüz yarısı. Gerçek karşı görünüm, ayna değil (saç ayrımı ve kulak farklı) | yaw +40° |
| prof_faceL | Sol profil. Tam 90° değil, uzak kirpikler görünüyor | yaw +80° |
| rear34 / back | Yalnız saç ve topuz | yüz için kullanılmadı |

**Tutarlılık:**
- Ön, iki 3/4 ve profilde kimlik tutarlı: aynı çiller, burun, kaş ve saç ayrımı.
- **Tutarsızlık 1 — profil ölçeği:** profil paneli ~%9 küçük çizilmiş (14.0 / 15.4 px/cm). Profile serbest ölçekli ayrı kamera verildi.
- **Tutarsızlık 2 — profilde boyun duruşu:** profildeki çene altı–boğaz çizgisi farklı bir baş/boyun duruşu gösteriyor. Bu yüzden çene altı yalnız çene yakınında kullanıldı.
- Görüntüler yapay zekâyla üretilmiş konsept render gibi duruyor, kalibre fotoğraf değil. Buradan çıkan mm değerleri yaklaşıktır.

**Işık:** yumuşak stüdyo ışığı, kamera solu ve üstünden. Gölgeler geometriye çevrilmedi.
- Ölçümler yalnız silüetlerden, izleyici eğrilerinden ve kenarlardan alındı.
- Göz çukuru ve elmacık altı gölgeleri yalnız yan ışıklı clay karşılaştırmasıyla yorumlandı.

**Referanstan çıkarılan kanıt:**
- **MetaHuman yüz izleyicisi:** göz kapakları, dudaklar, philtrum ve nazolabial eğrileri, ön / 3/4 / profil panellerinde.
- **Deri anahtarlı silüetler:** profil ön kenarı, 3/4 uzak yanak/çene ve ön yanak (yanakta saç örttüğü için tek yönlü).
- **Elle seçilen noktalar:** etiketli piksel ızgaraları üzerinde kaş merkez çizgileri, burun kanadı kenarları, burun tabanı, çene/mandibula çizgileri.

**Kullanılmayanlar:** eski GD12 Tier A sayfası, ref6, yapay zekâ turnaround'ları ve eski 3D renderlar hedef olarak kullanılmadı.

## 2. GD11 ve GD12 incelendi: neden yeterince benzemiyordu?

Ölçümler aynı kameralarda, aynı yöntemle yapıldı.

| Sorun | Ölçülen neden |
|---|---|
| GD12 üzgün / kaygılı bakış | Kaş derisi ~1 cm indirilmiş, sabit kapak kıvrımının üstüne bastırılmış. Üst kapak kenarı da 1.5 mm indirilmiş. **Göz açıklığı:** GD12 9.4 px, referans 15.6 px, F1H 11.3 px (aynı göz, aynı kamera). Referansın gözü *daha açık*, GD12 ters yöne gitmiş |
| Bu karar neden verildi? | GD12'nin tanı malzemesindeki iris ~8.6 mm çiziliyordu. Bu yüzden irisin çevresinde fazla sklera görünüyor ve göz "çok açık" okunuyordu. GD13'te iris anatomik boyuta (~11.7 mm) ve piksel başı gölgelendirmeye geçirildi |
| GD12 üst kapakta katlanma | İndirilen kaş sabit kıvrıma basınç yapıyor. Yakın planda çift kıvrım görünüyor (C1, GD12) |
| Geniş ve köşeli alt yüz | Ön görünüm çene konturu sapması: F1H 3.0 mm, **GD12 10.1 mm** (GD12 çeneyi ve çene açısını genişletmişti). Ağız seviyesinde alt yanak her yanda +5.2 mm geniş |
| Profil / kök | Kök ve üst burun sırtı +4.0 mm önde. Çene yastığı −3.6 mm geride. Labiomental oluk yok (F1H'de labiomental ile pogonion aynı derinlikte) |
| 3/4 çene hattı | Referansta arka mandibula sınırı kulağa doğru dik yükseliyor. Modelde GD11'in S8–S10 geçişlerinden kalan çene altı / gonial dolgunluk sınırı aşağı çekiyor |

## 3. Modelleme yöntemi değiştirildi (gerçekte ne yapıldı)

### 3.1 Önce ölçüm altyapısı kuruldu

Her panel için perspektif baş kamerası çözüldü:
- Başlangıç: göz kapakları ve dudaklar.
- İyileştirme: tüm kanıtla, şekille dönüşümlü (bundle adjustment).

Model ve referans karşılaştırmaları aynı yöntemle yapılıyor:
- izleyici eğrileri ve bağlı mesh noktaları;
- silüetlerde "malzeme bölgesinin en dış vertexi";
- jaw line için malzeme çizgisi (yüzeyin aşağı döndüğü mandibula sınırı).

### 3.2 İstatistiksel anatomik model uydurması denendi ve sanatsal olarak REDDEDİLDİ

MetaHuman yüz modeli denendi: 22 bölge, 1198 kimlik PCA modu ve bölge öteleme/ölçek parametreleri.
- Dört açıyla birlikte uyduruldu (fitA–fitD).
- Kontur artıkları 1–2 mm'ye indi.

Ancak sonuç sanatsal olarak kabul edilemezdi:
- kaş çatma çizgileri;
- çökük yanaklar;
- burun modları açıldığında deforme olmuş, iri bir burun (fitD).

Mod sayısı kısıtlanıp alçak geçiren uygulandığında değişim ≤6 mm kaldı ve kimlik değişmedi. Bu yüzden istatistiksel fit geometri olarak kullanılmadı. **Yalnız büyük-form hatalarının nerede olduğunu ölçmek için kullanıldı.** Kayıtlar: `data/fit*`, `r/OV_fit*`.

### 3.3 Nihai geometri: ölçülen hedeflere göre bölgesel yeniden şekillendirme

Seçenek A uygulandı: MetaHuman topolojisi üzerinde yeniden şekillendirme.

**Kullanılan araçlar** (scriptli, anatomik adlı, ölçülen landmark'lara oturtulmuş):
- Handle tabanlı yumuşak deformasyon (`tools/gd13_sculpt.py`). ZBrush Transpose / Move / soft-mod hareketinin scriptli karşılığı.
  - düz plato alanlı büyük bölge ölçekleme;
  - Wendland çekirdekli taşıma;
  - şişirme;
  - temel F1H'ye göre deplasman gevşetme.
- Göz kapağını göz küresi üzerinde döndüren bir kapak operatörü (yarım göz kırpma hareketi; kapak göze giremez).
- Her geçişten sonra katlanma taraması ve F1H'ye karşı unfold.

**Bu çalışma şunlar değildir:**
- Elle serbest fırça sculpt'ü değil. Kullanıcının istediği tarzda ZBrush veya Blender'da elle sculpt yapılmadı.
- Remesh veya retopoloji yapılmadı.

**Neden Seçenek B (bağımsız yeni baş) yapılmadı?**
- Ölçülen farkların hepsi bu topolojide üretilebildi: alt yüz genişliği, kök, çene, göz açıklığı, dudak ve burun oranları.
- Yeni baş, DNA ve rig yolunu kaybettirirdi.
- Seçenek B denenmedi, yalnız değerlendirildi.

**Tarif:** S2 → S3c → S4 → S5 → S6 + unfold → SF1 → S9 → SF3 + unfold (`ops/*.json`). Her geçiş aynı kameralarda referansla karşılaştırıldı.

**Reddedilen veya değiştirilen ara adaylar** (`ops/rejected_or_superseded`):

| Aday | Neden reddedildi |
|---|---|
| S1 | Wendland çekirdekleri geniş işlemde etkisizdi |
| S3 | Kapak indirme, yanlış tanı |
| S3b | Kapak açmada kıvrım |
| S7 / S8 / S10 | Dudak kenarı sırtı ve üst dudakta tümsek |
| GD13a | Dudak sırtı |

## 4. Bölge bölge yapılan anatomik değişiklikler (F1H → GD13)

| Bölge | Ne yapıldı | Anatomik amaç | Ölçülen sonuç (+ = model önde / geniş) |
|---|---|---|---|
| Alt yüz genişliği | Ağız–çene seviyesinde düz alanlı yumuşak daraltma (×0.93) | Elmacıktan çeneye daralan yüz, U/V geçişi; yanaklar oyulmadı | Ön alt yanak +5.0 → **+2.6 mm**. Ön çene gövdesi +3.0 → **−1.0 mm** |
| Mandibula / çene açısı | Gonial bölgeyi yukarı ve içe toplama, arka (~4 mm) ve orta (~3 mm) mandibula sınırını kaldırma, köşe gevşetme | GD11'den kalan çene altı ve gonial dolgunluğu azaltmak; referanstaki gibi kulağa doğru yükselen net çene hattı | Görsel: C5, A2 3/4. Kas eklenmedi, köşe keskinleştirilmedi |
| Kök / burun sırtı başlangıcı | Nasion ~3.7 mm geri, gevşetme | Daha derin kök; referanstaki düz burun çizgisi ve derinde oturan göz | Profil kökü +4.2 → **+2.9 mm** |
| Burun | Kanat daraltma (iki kez, toplam ~%17), uç aşağı döndürme (~2 mm), uç lobülleri ve kanat kenarı | Daha dar kanat, aşağı ve yuvarlak uç, önden daha az görünen burun deliği | Ön kanat artığı 2.5 mm, değişmedi |
| Göz kapakları | Üst kapak göz küresi üzerinde ~2.4 mm açıldı, kıvrım yumuşatıldı. Alt kapak 0.4 mm indi. Dış köşe 0.7 mm dışa alınıp gevşetildi | Referanstaki açık, sakin göz; GD12'deki ağır kapak, kıvrım ve üzgün bakış giderildi | Açıklık (aynı göz): F1H 11.3, GD12 9.4, **GD13 15.4 px** (referans 15.6) |
| Kaş | Kaş derisine dokunulmadı (GD12'nin indirmesi uygulanmadı). Dış kaşa ~1 mm öne çıkıntı | Çatma veya üzgün ifade yok. Kaş kılı konumu groom işidir | Tanı kaşı referans çizgisine göre yerleştirildi (yalnız materyal) |
| Elmacık / orta yüz | Malar çıkıntı (+1.3 mm, öne ve yana), elmacık altında çok hafif yumuşak düzlem (−0.6 mm) | Yüksek elmacık okuması; oyuk açılmadı | — |
| Dudaklar | Dudaklar ~1.3 mm geri; yuvarlak hacim (üst +0.7, alt +1.0 mm); köşeler hafif kaldırılıp gevşetildi | Profilde fazla öne çıkan ağzı geri almak, önden daha dolgun ve yuvarlak dudak | Profil dudak bandı +3.3 → **+3.1 mm**. GD12'ye göre +4.9 → **+3.1 mm** |
| Labiomental / çene | Alt dudak tabanı geri, çene yastığı ~4 mm öne. **Çene uzatılmadı** | Belirgin labiomental oluk ve öne çıkan çene yastığı | Profil çene yastığı −3.2 → **−2.6 mm** |
| Alın, şakak, kafatası, kulak, boyun | Değiştirilmedi (0.00 mm) | Saç örtüyor; profilde alın sapması −1.3 mm, değişmeyi gerektirmiyor | — |

## 5. GD12 → GD13 gerçek 3B mesh farkı

- **Genel:** en çok 7.74 mm; hareket eden vertexlerde ortalama 1.29 mm. 10 915 vertex 0.1 mm'den, 5 860 vertex 1 mm'den fazla hareket etti.
- **F1H → GD13:** en çok 5.92 mm, ortalama 1.12 mm, 4 575 vertex 1 mm'den fazla.
- **Haritalar:** D1 ve D2 panoları. Üstte yüzey normali yönü (kırmızı dışarı, mavi içeri, ±4 mm), altta 3B vektör büyüklüğü.
- **Bölge tablosu:** `data/checks_head_GD13.json`. Bölge başına normal ortalaması, en büyük değer ve ortalama x / y / z vektörü.

**GD12'ye göre öne çıkan bölgeler:**

| Bölge | Normal ortalama | En çok | Ortalama vektör (x / y / z) |
|---|---|---|---|
| Üst kapak | −1.3 mm | 7.7 mm | y −0.58, z +1.78 |
| Kaş / supraorbital | — | — | z +1.5 (GD12'nin indirdiği kaş geri geldi) |
| Alt yanak / jowl | −2.5 mm | 5.9 mm | — |
| Çene gövdesi / açısı | −2.1 mm | 5.9 mm | — |
| Dudaklar | — | — | y −0.6 / −0.65 (geri) |
| Çene | — | 5.0 mm | — |
| Alın, şakak, kafatası, boyun, kulak | 0 | 0 | — |

Simetrik daraltmada x ortalaması sıfıra yakın çıkar; içe hareket "normal" sütununda görülür.

## 6. Referansa benzerlik: ölçülenler

Kameralar her baş için ayrı ayrı yeniden çözüldü. + değer, modelin referanstan önde veya dışarıda olduğu anlamına gelir.

| Ölçüt (mm, ortalama) | F1H | GD12 | **GD13** |
|---|---|---|---|
| Profil: kök / üst burun sırtı | +4.2 | +4.0 | **+2.9** |
| Profil: burun ucu | +1.0 | +1.0 | +0.9 |
| Profil: subnazal / üst dudak | +6.8 | +6.9 | **+5.8** |
| Profil: dudaklar | +3.3 | +4.9 | **+3.1** |
| Profil: çene yastığı | −3.2 | −3.6 | **−2.6** |
| Ön: alt yanak (ağız seviyesi) | +5.0 | +5.2 | **+2.6** |
| Ön: çene gövdesi | +3.0 | +3.0 | **−1.0** |
| Ön: çene konturu (RMS) | 3.0 | 10.1 | **2.8** |
| Ön: nazolabial eğri (RMS) | 3.2 | 3.3 | **2.5** |
| 3/4: uzak çene | −1.4 / −3.7 | −0.9 / −3.4 | **−2.1 / −4.8 (kötüleşti)** |
| Göz açıklığı (px, aynı göz, referans 15.6) | 11.3 | 9.4 | **15.4** |

Kalan belirsizlik:
- Ön ve 3/4'te "subnasale" noktası tüm başlarda ~6.7 mm sapıyor. Referanstaki görünen burun tabanı ile modeldeki en derin profil noktası farklı tanımlar olabilir; çözülmedi.
- Konturlar ve izleyici eğrileri ten dokusunu, çilleri, kaşı ve saçı ölçmez. Benzerliğin büyük kısmı bunlardan gelir.

## 7. Sanat değerlendirmesi

**Daha iyi olanlar** (B1, A2, C1–C6):
- **İfade:** GD12'deki üzgün/kaygılı kaş, kaş çatma ve çift kapak kıvrımı yok. Göz referanstaki gibi açık ve sakin.
- **Alt yüz:** elmacıktan çeneye daralan alt yüz. 3/4'te net ama yumuşak çene hattı.
- **Profil:** daha derin kök ve öne gelen çene yastığı.
- **Burun:** kanatlar daha dar.

**Hâlâ benzemeyenler:**
- **Dudaklar:** referanstan ince. Ağız önden hafif büzük ve aşağı köşeli okunuyor; köşelerdeki küçük çukur F1H'den kalma. 3/4'te alt dudak sınırında hafif çizgi var.
- **Burun:** referanstaki yuvarlak, hafif sarkık uç ve kolumella–dudak ilişkisi tam kurulamadı (subnasale belirsizliği).
- **Göz şekli:** açıklık doğru. Referanstaki badem şekli, iç-orta tepe noktası ve görünen kapak kıvrımı tam değil; göz 3/4'te biraz yuvarlak okunuyor.
- **3/4 elmacık altı:** çapraz bir geçiş gölgesi var; F1H'den beri mevcut.
- **Yaş ve yüzey ipuçları:** referanstaki nazolabial, göz altı ve alın çizgileri, çiller ve ten bilinçli olarak eklenmedi. Yaşlandırma riski vardı ve görevin dışında.
- **Kaş:** tanıdaki kaş bandı groom değil. Gerçek kaş groom'unun referans çizgisine göre yeniden yerleştirilmesi gerekiyor.

**Sonuç:**
- GD13, GD12'den açıkça daha çok referansa benziyor. Yön doğru ve fark büyük-formda görünür.
- Ancak "referanstaki kadının kendisi" düzeyinde değil: dudak, burun ucu, göz şekli ve yüzey/yaş ipuçları eksik.
- Genel kimlik **PARTIAL**.

## 8. Teknik geometri kontrolleri

| Kontrol | Sonuç |
|---|---|
| Vertex sayısı / sonluluk | 33 845, tamamı sonlu; DNA sırası korundu |
| Keskin kıvrım (dihedral 120°'den büyük) | GD13 46. F1H 43, GD12 42 (+3, ağız iç köşeleri ve burun deliği) |
| Ters dönmüş üçgen | 0 |
| Üçgen alan oranı | En küçük 0.24 (GD12 0.11), en büyük 3.0 (alt dudak orta hattı) |
| Kapak – göz küresi | F1H'ye göre içeri giren kapak vertexi 0; açıklık değişimi en çok −0.10 mm |
| Simetri | Deplasman asimetrisi p99 0.98 mm (F1H'ye göre). Tek taraflı kemik hareketi yok |
| .blend yeniden açma | Açıldı. GD13_Head nihai başla 0.0001 mm farklı; 9 kamera, 4'ünde referans arka planı; salt-okunur GD12 ve F1H mevcut |
| GLB / OBJ geri yükleme | İkisi de açıldı (25 975 vertex / 51 652 üçgen) |
| Tarifin yeniden üretimi | `build_gd13.sh` F1H'den GD13'ü 0.0 mm farkla üretiyor |

## 9. Mevcut üretim dosyaları korundu mu? — PASS

| Kontrol | Sonuç |
|---|---|
| Unreal varlıkları | Bu oturumda Content, Config ve Plugins altında değişen dosya yok. Editör yalnız MetaHuman izleyicisi için açıldı; kirli paket yok, hiçbir şey kaydedilmedi, temiz kapatıldı |
| GD11 / GD12 kaynakları | Değişmedi (yalnız okundu) |
| Diğer çalışmalar | Eski yüzler, MetaHuman DNA ve rigler, B2 vücut, Henley, Chaos şort, h74b / h75a / h75c saçları, locomotion, kamera, animasyon Blueprint'leri ve haritalar dokunulmadı |
| Yeni dosyaların yeri | `SourceAssets/Characters/GD13_IdentityMaster_20261009/` ve `Saved/Codex/GD13_Identity_20261009/` |

## 10. Kalan işler

**Sanat:**
1. **Dudaklar:** vermilyon yüksekliği ve alt dudağın yuvarlak dolgunluğu (referans daha dolgun), ağız köşesi çukuru (F1H'den kalma), ön görünümde büzük okuma. Elle sculpt önerilir.
2. **Burun ucu ve kolumella:** referanstaki yuvarlak, hafif sarkık uç; burun tabanı–philtrum ilişkisi (subnasale belirsizliği).
3. **Göz şekli:** badem göz; kapak kıvrımı ve pretarsal şerit; dış köşe yüksekliği.
4. **3/4 elmacık altındaki çapraz geçiş** ve hafif nazolabial yumuşak doku. Yaşlandırmadan, oyuk açmadan.
5. **Kaş groom'u:** referans kaş çizgisine göre yerleştirme. Kaş derisi değiştirilmedi.
6. **Ten:** gerçek x19a ve çil ile kimlik değerlendirmesi. Burada yalnız tanı materyali kullanıldı.

**Teknik (yalnız onaydan sonra):**
7. Aynı DNA vertex sırası korundu. Yeni bir SKM kopyasına doğrudan fark olarak bake edilebilir (`blender_g11ww_deltamap` + `ue_g11uu_apply2`); 858 morph ve DNA korunur.
8. Kapak açıklığı arttı (üst kapak ~2.4 mm). UE'de göz kırpma ve kapak morph'ları, kirpik ve göz kenarı mesh'leri kontrol edilmeli; gerekirse düzeltici morph.
9. Saç, kaş ve kirpik groom'ları yeni SKM'ye yeniden bağlanmalı.
   - Kafatası ve şakak değişmedi; saç yeniden hizalama gerekmiyor.
   - Yanak ve çene içe aldığı için gevşek tellerde batma riski yok.
   - Yine de yüz çevresindeki teller kontrol edilmeli.
10. Rig pozları, hareket kareleri, LOD, checkpoint ve korunan varlık doğrulaması.

## 11. Kabul değerlendirmesi

| # | Ölçüt | Sonuç |
|---|---|---|
| 1 | Orijinal referansa benzerlik | **PARTIAL**. GD12'den belirgin biçimde yakın; dudak, burun ucu, göz şekli ve yüzey ipuçları eksik |
| 2 | Genel yüz kimliği | **PARTIAL** |
| 3 | Kafatası ve yüzün ana formları | **PARTIAL**. Alt yüz, kök, çene yastığı ve mandibula düzeldi. Kafatası, alın ve şakak saç altında, değiştirilmedi. 3/4'te uzak çene biraz kötüleşti |
| 4 | Orbita / göz kapağı anatomisi | **PARTIAL**. Açıklık referansla aynı, GD12 kıvrımı giderildi. Badem şekli ve kapak kıvrımı eksik |
| 5 | Elmacık ve yanak yumuşak doku hacmi | **PARTIAL**. Elmacık çıkıntısı ve alt yanak daralması yapıldı; elmacık altındaki çapraz geçiş kaldı |
| 6 | Burun anatomisi | **PARTIAL**. Kök, kanat ve uç dönüşü düzeldi; uç biçimi ve kolumella–subnasale ilişkisi çözülmedi |
| 7 | Ağız çevresi ve dudak anatomisi | **PARTIAL**. Dudaklar geri alındı ve yuvarlaklaştı; referanstan ince, köşeler zayıf |
| 8 | Mandibula ve çene anatomisi | **PARTIAL**. Ön çene konturu 2.8 mm, çene yastığı öne, çene hattı yükseldi; çene uzatılmadı |
| 9 | Doğal dinlenme ifadesi | **PARTIAL**. Göz ve kaştaki üzgün/kaygılı ifade giderildi (PASS düzeyinde); ağız önden hafif büzük |
| 10 | Mesh kalitesi ve kaynak bütünlüğü | **PASS**. Ters üçgen 0, kapak kesişimi yok, katlanma F1H'ye yakın (+3), .blend / GLB / OBJ yeniden açıldı, tarif birebir |
| 11 | Rig'e hazırlık | **NOT TESTED**. DNA sırası korundu ama rig, mimik, göz kırpma, kirpik ve LOD testi yapılmadı |

## Panolar (`boards/`)

| Dosya | İçerik |
|---|---|
| `A1_CLAY_REF_KAMERALARI_ISIK_A.jpg` | Orijinal referans / GD12 / GD13 clay; 4 çözülmüş referans kamerası, ön yumuşak ışık |
| `A2_CLAY_REF_KAMERALARI_ISIK_B.jpg` | Aynı kameralar, yan sert ışık (yüzey geçişleri) |
| `A3_CLAY_5_ACI_INCELEME.jpg` | 5 inceleme açısı. Sağ profil referansta yok, yardımcı kamera |
| `B1_KIMLIK_TEN_REF_KAMERALARI.jpg` | Kimlik: basit ten, iris, geçici kaş, kirpik çizgisi, dudak tonu (saçsız tanı materyali); referans / GD12 / GD13 |
| `B2_KIMLIK_5_ACI.jpg` | 5 inceleme açısında ten |
| `C1` – `C6` | Yakın planlar: göz/kaş/orbita, elmacık/orta yüz, burun, dudak/ağız köşeleri, çene/mandibula, profil derinliği (siluet çizgisi) |
| `D1_DEFORMASYON_GD12_GD13.jpg`, `D2_DEFORMASYON_F1H_GD13.jpg` | Gerçek mesh farkı: normal yönü ve 3B büyüklük |
| `E1_SILUET_UST_USTE.jpg` | Modelin çözülmüş kameradaki dış hattı, referans üzerinde (GD12 / GD13) |

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
