# GD38 — Kaş arası ve kaş simetrisi, göz altı simetrisi, profilde dudak yanları

Tarih: 2026-10-11. Başlangıç: GD37 yüzü N37 (GD35 görünümü: ten n3, göz h6, sakin göz pozu, saç h75c).

Durum: **PARTIAL.** Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED). Üretim karakterine uygulanmadı. Yeni varlıklar yalnız `/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011` altında.

## 1. İsteğin

"Kaş arası açıklığını da referans üzerinden düzelt. Sol kaş sağdakine göre biraz garip ve fazla asimetrik duruyor. Aynı şekilde sol ve sağ göz altı torbaları. Dudak yanları işaretlediğim gibi hâlâ yan görünümde garip ve şişik duruyor." İşaretli görsel: `process/00_KULLANICI_ISARETI.jpg`.

"Sol kaş" görüntüdeki sol kaş olarak okundu, yani öznenin **sağ** kaşı (−x). Bu, GD36'da da düzeltilen taraf. İyi taraf olarak öznenin sol yarısı (+x) alındı.

## 2. Teşhis

| Konu | Ölçüm | Neden |
|---|---|---|
| **Kaş arası** | Görünen kaş başları arası (ön, 2x çerçeve): referans 65–72 px, GD37 74–81 px. Yani modelde ~3 mm fazla. 3/4 sağ görünümde de ~3 mm geniş. | Kaş istasyonları referanstaki kaş başlarının üstünde duruyor. Ancak grumun baş kısmındaki seyrek ve kısa kıllar yüzünden görünen koyu kaş başı istasyondan 2–3 mm dışarıda başlıyor (`process/03`). |
| **Kaş asimetrisi** | Öznenin sağ kaşının başı 2,3 mm daha içeride ve 2,1 mm daha yukarıda. Baş daha ince (4,8 / 6,4 mm), kuyruk daha uzun. | İki kaş, hafif yan dönmüş referans fotoğraftan **ayrı ayrı** izlenmişti. Ayrıca kaş kemiği sağda 1,6 mm öndeydi (GD36'da göz kapağına yakın olduğu için korunmuştu). |
| **Göz altı torbaları** | Sağ göz altı, sol tarafın aynasına göre 1,4 mm farklı (0,7 mm önde, 0,6 mm yukarıda). Üst kapak 2,5 mm farklı. | Öznenin **sağ göz küresi**, sol göz küresinin hizalı aynasına göre **1,5 mm önde, 0,7 mm dışarıda**. Kapaklar ve torba bu göze oturduğu için öne çıkıyor. |
| **Dudak yanları (profil)** | Referansta ağız köşesi dudağın en önündeki noktadan belirgin biçimde daha geride (yaklaşık 4 mm). | Modelde dudakların yan kısmı ve ağız köşesi çevresi öne şişkin; ağız çevresi bir "çıkıntı" gibi okunuyor. Köşenin iç cebi köpek dişinin hemen yanında olduğu için köşe dişe girmeden geri alınamıyor. |

## 3. Yöntem

### Hedef `T38` (`tools/gd38_edit.py`, tarif: `data/T38_recipe.txt`)
1. **Dudak yanları:** dış deri 2,5 mm geri alındı.
   - Hareket dişlere olan uzaklıkla yumuşak bir kalınlık rampası izliyor: dişe yakın iç astar sabit, dış deri tam hareket ediyor. Dudak yanda inceliyor.
   - Ağız köşesi iç cepleri sabit kaldı (1 mm çekirdek, 8 mm yumuşak geçiş).
   - Alan, orta hatta 0 ve yanda 2,0–2,6 cm arasında tam. Yanağa doğru 3,7 cm'de bitiyor.
2. **Öznenin sağ göz bölgesi:**
   - Göz küresi, sol göz küresinin hizalı aynasına taşındı (−0,74 / −1,49 / −0,10 mm).
   - Gözün 1,5–2,8 cm çevresi göz küresiyle birlikte rijit taşındı. Kapaklar biçimini koruyup göze oturmaya devam ediyor; göz kabuğu ve kenar meshleri de taşındı.
   - Alt kapağın altındaki torba bölgesi sol tarafın hizalı aynasının biçimini aldı (kapak kenarı sabit).
   - Üst kapak kıvrımının üstündeki kaş kemiği de aynalandı.
3. **Kaşlar** (`tools/gd38_browsym.py`, `data/brow3d_s8.json`):
   - Öznenin sağ kaşı, sol kaşın hizalı aynası yapıldı.
   - İki kaş başı da 2,5 mm orta hatta doğru uzatıldı (istasyon başları arası 20,0 → 17,7 mm).
   - ds7 grum parametreleri ve n4 rengi aynı.

### Denenip reddedilenler
`process/01`, `process/02`, `data/T38_recipe.txt`:

| Deneme | Sorun |
|---|---|
| Dış yüzey bayraklı dudak alanı | 158–259 ters üçgen |
| Diş boşluğuna göre sınırlama | Sağ köşe cebinde 6–50 ters üçgen |
| Q2: 3 mm, dar geçişle sabit cep | Profilde köşede koyu çukur |
| Göz bölgesinin tam aynası (E1) | Üst kapak kıvrımında ve dış köşede 70 ters üçgen |
| İlk T38: kaş kemiğinde dar orta hat geçişi | Kaş arasında dikey çizgi |

### Motor zinciri (`tools/gd38_finalT.sh`)
1. GD37 MHC kopyası.
2. 4 aşamalı geri beslemeli fit.
3. Otomatik rig (858 morph, DNA).
4. Kaşın yeni deride simetrik istasyonlarla üretilmesi.
5. Saç ve kirpik bağlama.
6. Çekimler.
7. Değerlendirme Blueprint'i ve haritası, PIE.

## 4. Sonuç

### Sağ–sol fark (rig sonrası)
Öznenin sağ yarısı ile sol yarının hizalı aynası arasındaki ortalama fark (p95 parantez içinde):

| Bölge | GD37 | **GD38** |
|---|---|---|
| Kaş kemiği | 2,0 (4,7) mm | **0,9 (2,7)** |
| Üst kapak | 2,5 (4,4) | **1,6 (3,1)** |
| Göz altı / alt kapak | 1,4 (2,4) | **0,9 (1,6)** |
| Glabella | 1,2 | **1,0** |
| Elmacık | 0,5 | **0,3** |
| Çene gövdesi | 1,4 | **1,2** |

### Kaşlar
- İki kaş aynı biçimde (`K1`).
- Görünen kaş başları modelin orta hattına göre simetrik: her iki taraf ~37,5 px (GD37: 32 / 47 px).
- Görünen aralık:
  - eşik ölçümünde 75–79 px (GD37 79–81);
  - ızgaralı yakın planda ~67 px;
  - referans 65–72 px.

### Dudak yanları
- Dış deri ağız köşesi çevresinde 2,5 mm geride.
- Profilde ağız çizgisi daha uzun ve dudak çevresi daha az şişkin (`D1`, `D2`; en net kil satırları).

## 5. Panolar

- `K1`: kaşlar. Satırlar: önden saç gizli, önden saçlı sakin göz, sağa bakış, sola bakış.
- `G1`: göz bölgesi ve göz altı. Satırlar: stüdyo, ön ışık, kil.
- `D1`: profil dudak yanları. Satırlar: saçlı, saç gizli, kil.
- `D2`: sağa bakış dudak yanları. Satırlar: saçlı, ön ışık, kil.
- `F1`: REF | GD37 | GD38, saçlı, dört açı. `F2`: aynısı saç gizli.
- `process/01`: dudak yanı kil adayları. `process/02`: göz bölgesi adayları. `process/03`: eski (sarı) ve yeni (camgöbeği) kaş istasyonları.

## 6. Editörde değerlendirme

1. Şu haritayı aç: `/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Maps/L_GD38_Eval_T38`. Blueprint: `BP_GD38_Character_T38`.
2. Sakin göz pozu yalnız **Simulate (Alt+S) veya PIE** sırasında görünür.

## 7. Teknik testler

| Test | Sonuç |
|---|---|
| Hedef T38: ters üçgen 0, kat 43 (GD37: 41), en küçük alan oranı 0,52. Sağ göz kapağı–göz küresi teması GD37 ile aynı (300 köşe). | **PASS** |
| Fit (4 aşama) → hedef: ortalama 0,057 / p99 0,74 mm, en fazla 3,8 mm (ense, önceki geçişlerle aynı). Göz küreleri hedefe birebir oturdu. | **PASS** |
| Otomatik rig, DNA, 858 morph (`MHC_GD38_T38`, `SKM_GD38_Face_t38`) | **PASS** |
| Rig sonrası: ters üçgen 0, kat 43. İstenen değişikliğin %100'ü korundu (yön kosinüsü 0,999). Sağ göz küresi hedefteki gibi taşındı, sol göz değişmedi. | **PASS** |
| Düzenleme bölgeleri dışındaki yüz GD37 ile aynı (en fazla 0,075 mm), dişler değişmedi | **PASS** |
| Kaş (ds8s, simetrik), saç h75c ve kirpik yeni yüze bağlı; PIE'de 4 groom görünür, `eyeUpperLidUp` 0,6 | **PASS** |
| Kayıtlı Blueprint ile çekim düzeninin birebirliği: yüzde ortalama fark 0,011–0,015, yalnız gürültü (GD37: 0,011–0,016) | **PASS** |
| İfadeler (RigLogic), LOD1–7. Göz küresi taşındığı için göz kırpma / bakış testi önerilir. | **NOT_TESTED** |
| Üretim değişmedi (`data/outside_change_scan.txt`). qa_config geri yüklendi, editör kaydetmeden kapatıldı. | **PASS** |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 8. Açık kalanlar

- **Kaş arası.** Eşik ölçümüne göre görünen aralık hâlâ referanstan ~3–7 px geniş olabilir; yakın planda ise eşit görünüyor. İstenirse kaş başı yoğunluğu (`BR_HEAD_DENS` 0,45) artırılabilir, böylece görünen baş istasyona yaklaşır.
- **Göz küresinin taşınması** RigLogic göz hareketlerini etkileyebilir. Rig yeni göz konumuyla yeniden üretildi ama ifade ve bakış testi yapılmadı.
- **Üst kapak farkı (1,6 mm).** Kapak biçimleri korunarak taşındı, aynalanmadı; tam aynalama kıvrımda ters üçgen üretiyor.
- **Dudak yanları** ağız köşesinin dişe yakın cebi yüzünden 2,5 mm ile sınırlı. Köşenin daha da geride okunması için dudakların orta kısmı öne alınabilir. Ancak profil silueti referansla uyumlu olduğu için bu yapılmadı.
