# GD11 O1: overlay / silüet eşleştirme — yüz (O1G), saç silüeti (H1) ve ince teller (H2)

Tarih: 2026-10-09. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Eski varlıkların hiçbiri silinmedi ya da değiştirilmedi.

| Aşama | Aday | Taban |
|---|---|---|
| Yüz overlay pass'i | **SKM_G11RR_Face_ww5bo1g (O1G)** | S10F (ww5bs10f) |
| Saç silüeti pass'i (H1) | **h74a** | h73b telleri; yeniden kurulum yok, son işlem |
| İnce tel pass'i (H2) | **h74b** = h74a + 3521 ince ayrık tel | h74a |
| Korunanlar | cilt x19a, iris e3n, kaş M_SlightArch (m3), ww5bf ağız onarımı | aynı |

## 1. Önce iki önemli bulgu

### 1a. S10F saç board'ları bozuk render'dı

- **Belirti:** S10F raporundaki saç kasklı ve blok gibiydi; kulak altındaki ve ensedeki ince teller yoktu, saç çizgisi sert görünüyordu.
- **Neden:** saç verisi değil, editör belleği. Editör 2 gündür açıktı ve 62,7 GB bellek ayırmıştı; sanal bellekte 2 GB boş kalmıştı. UE saç tellerini oluşturamayınca saçı yedek kask LOD'u ile çizdi. Günlükte hata yok.
- **Kanıt:** aynı h73b, S8, R1 ve S1 çekimlerinde tellerle doğru görünüyor.
- **Düzeltme:** editör yeniden başlatıldı. Bu rapordaki bütün saçlı çekimler taze editörde alındı.
- **Board:** `03_HAIR_ALL_VIEWS.jpg`, 1. sütun bozuk render, 2. sütun aynı h73b'nin doğru render'ı.

"Saç kötüleşti / kask / küçük teller kayboldu" algısının büyük kısmı bu render hatasından geliyordu.

### 1b. 6'lı referans setinin panelleri birbiriyle tutarlı değil

| Tutarsızlık | Ne yapıldı |
|---|---|
| İki 3/4 panel (r34, l34) aynı yönden çekilmiş | Sol 3/4 karşılaştırması için l34 aynalandı (yüz simetrik varsayımıyla) |
| Profil panellerinde baş ön ve 3/4 panellerine göre ~%13 küçük (göz–ağız 92–94 px, önde 108 px) | Profiller kendi ölçeğiyle hizalandı |
| Çene tabanı: önde adayın çenesi referanstan **3,6 mm aşağıda**; profilde referansın çenesi adaydan **~15 mm aşağıda** | Çene boyu **değiştirilmedi**. Önceki kurallarınız da bu yönde (çene uzatma 3 kez reddedildi). |
| Saç genişliği: aynı yükseklikte ön panel saçı bizden 9 mm dar, arka panel 13 mm geniş gösteriyor (ortografik bakışta eşit olmalı) | Saç düzeltmesi yalnız tutarlı yönlere yapıldı |

## 2. Yöntem: overlay aracı (`tools/blender_g11o1_ov5.py`)

**Hizalama**
- Referans panelinde ve aday çekiminde aynı MetaHuman yüz izleyicisi kullanıldı.
- Ön ve 3/4: iki göz açıklığının merkezi + iki ağız köşesi, en küçük kareler benzerlik dönüşümü. Kalıntı önde ~1 px, 3/4'te 1–4 px.
- Profil: nasion + göz → stomion yüksekliği ölçeği, dönüş 0. Burun ucu kalıntısı 1–4 px.

**Çizgiler**
- Aday konturu render edilen mesh'ten (geometri) alındı; çekimdeki ışık ve saçtan etkilenmiyor.
- Referans konturu görüntüden (ten / fon anahtarı) alındı.
- Çene alt çizgisi ve kaş çizgisi her iki görüntüde aynı görüntü yöntemiyle çıkarıldı.

**Bantlar** göz çizgisinden ağız çizgisine oranla tanımlandı: kaş, elmacık, yanak kütlesi, alt yanak, ağız, çene gövdesi; çene altı sütunları: çene tabanı, çene yanı, çene gövdesi.

**Sayılar:** mm. Kontur için **+ = aday referansın dışında**; satırlar için **+ = aday daha aşağıda**. Referans panelleri 480 px olduğundan çözünürlük ~0,65 mm/px; 1 mm altı farklar ölçülemez.

**Board'larda:** camgöbeği = referans, pembe = aday. Ön görünümde alın ve şakak satırlarında referans kenarı saçla örtülü; pembe kontur kafatasını gösterir, karşılaştırma dışıdır.

## 3. Yüz overlay pass'i (O1G)

### Hangi çizgiler eşleşiyor? (S10F → O1G, mm)

| Görünüm / çizgi | Kaş | Elmacık | Yanak kütlesi | Alt yanak | Ağız | Çene gövdesi |
|---|---|---|---|---|---|---|
| Ön, sol kontur | (saç) | (saç örtüyor) | (saç örtüyor) | −1,2 → −1,2 | −1,8 → **−1,2** | −1,2 → −1,2 |
| Ön, sağ kontur | (saç) | (saç örtüyor) | (saç örtüyor) | +4,9 → +4,9 | +2,7 → +2,7 | +3,0 → +3,0 |
| Sağ 3/4, uzak kontur | +0,6 | −2,6 → **−1,9** | −2,6 → **−1,3** | +1,3 → +2,6 | +2,6 → +3,5 | +1,3 → +1,9 |
| Sol 3/4 (ref aynalı) | 0 | −8,2 (saç teli) | (saç teli) | −1,9 → **−1,3** | −0,6 | −1,9 |

| Çizgi | S10F → O1G | Not |
|---|---|---|
| Ön çene alt çizgisi: çene yanı | +0,6 / −1,2 → aynı | eşleşiyor (±1 mm) |
| Ön çene alt çizgisi: çene gövdesi | −0,3 / +1,8 → +0,6 / +2,1 | eşleşiyor (≤2 mm) |
| Ön çene tabanı | +2,4 / +3,3 | aday 2–3 mm aşağıda; çene boyu değiştirilmedi |
| Burun tabanı satırı (ön) | +0,2 → +0,4 | eşleşiyor |
| Profil: glabella / burun ucu | −0,8 / −3,1 ; burun ucu hizalı | eşleşiyor |
| Profil: dudaklar | −6,3 / −3,9 (aday geride) | değişmedi |
| Profil: çene önü | −4,7 / −5,5 (aday geride) | çene öne çıkışı korundu, değiştirilmedi |
| Profil: çene altı | −14 / −15 (referans aşağıda) | paneller çelişkili (1b), değiştirilmedi |
| **Kaş çizgisi** (koyu bant) | aday 5 açıda da **2–7 mm aşağıda** | kaş değişiklikleri daha önce reddedildi; dokunulmadı, öneri olarak bırakıldı |
| Burun–dudak çizgisi (izleyici) | konum 1,1–1,3 mm, şekil 0,2–0,4 mm | eşleşiyor; "sert" okuma çizginin yerinden gelmiyor |
| Alt dudak (izleyici) | referans önde ~3 mm, 3/4'te 3–4,5 mm daha dolgun | istenen alanın dışında; öneri |

### O1G'de ne yapıldı? (yalnız yumuşak doku)

- 3/4'te uzak yanak konturu referansın ~2,6 mm içindeydi. Silüet vertex'leri: |dx| 4,8–5,7, y ≈ 10,3, z 157,5–161.
- Ön-yan yanağa geniş bir plato dolgusu eklendi: yana 1,5 mm, öne 0,8 mm.
  - Uzun geçişler: üstte 158,9 → 160,6 (sırt oluşmasın diye), altta 156,2 → 157,8.
  - İç kenar burun-dudak oluğunun dışında kalıyor; dolgu kulağa varmadan sönüyor.
- Elmacık altına küçük, geniş dolgu (0,7 mm), çukur derinleşmesin diye.
- Alt yanak ve çene yanında yalnız dolduran yumuşatma (kesme yok).
- Tarif: `data/O1_recipe.txt`.

**Elenen ara sürümler:**

| Ara sürüm | Neden elendi |
|---|---|
| O1a–d | plato kenarında sırt |
| O1e | elmacık altı p10 daha derin |
| O1f | elmacık altı p10 −0,71 |
| O1h | dolgu ×1,5: 5 yeni çıkıntı vertex'i |
| O1i, O1j | düzleştirme dolguyu sildi ya da ek kazanç yok |

### Bölge ölçümleri (S10F → O1G)

Kabartı: p10 = en derin çukur, ort = ortalama (mm).

| Bölge | Hareket ort / en çok (mm) | Kabartı p10 | Kabartı ort |
|---|---|---|---|
| Dış yanak (kulak birleşimi hariç) | +1,17 / 2,16 | −1,03 → −0,97 | −0,37 → −0,21 |
| Elmacık altı | +0,99 / 2,03 | −0,60 → **−0,59** | −0,41 → **−0,31** (daha az çukur) |
| Yanak (bukkal) | +0,32 / 0,95 | −1,43 → −1,35 | −0,45 → −0,43 |
| Ağız yanı | +0,12 / 0,48 | −1,45 → −1,36 | aynı |
| Alt yanak / çene yanı | +0,15 / 0,48 | −1,45 → −1,34 | −0,24 → −0,21 |
| Çene açısı / arka çene | **0,00** | aynı | aynı |
| Çene ucu (pogonion) | **0,00** | aynı | aynı |

**Kontroller**
- Yeni çukur 0, yeni çıkıntı 0.
- Keskin kıvrım 43 (S10F ile aynı).
- Alt kapak, üst kapak/kaş, burun, çene ucu ve çene açısı 0 mm; dudak kırmızısı ≤0,01 mm. Ağız köşesinde ve kulakta en çok 0,2–0,3 mm hareket var.

**Not:** S10 klasöründen kopyalanan eski kabartı dosyası farklı parametrelerle üretilmişti ve sahte "yeni çukur" uyarıları verdi. Bütün karşılaştırmalar aynı araçla yeniden üretilen S10F kabartısıyla yapıldı.

## 4. Saç silüeti pass'i (H1, h74a)

**Ölçüm (doğru render, h73b):**
- Ön silüet referansa yakın.
- Arka görünümde kulak üstü / kulak / ense hizasında saçımız toplamda +12 / +9 / **+27 mm** geniş.
- Profilde saçımız referansın içinde kalıyor; "arkaya genişleme" doğru render'da yok.
- h73b'nin 3D tel kapsamı iki tarafta simetrik (p99 farkı ≤ 0,4 cm). Overlay'deki sol/sağ farkı referans panelinden geliyor.

**H1 işlemi:** kökler sabit, saç katmanı kafa derisinin dışında yanlara doğru inceltildi.
- Oranlar: üst yanlarda %10, kulak hizasında %20, ense hizasında %30.
- Yüzü çerçeveleyen ön teller (y > 7) dokunulmadı.
- Telin ilk %25'i (kök tarafı) korundu.
- Kafa derisinin içine giren tel yok.
- Yeniden kurulum yapılmadı; kurulum kilitleri yeniden kümelerdi.

| Toplam genişlik farkı (sol + sağ, mm; + = bizimki geniş) | h73b | **h74a** | h74b |
|---|---|---|---|
| Arka: kulak üstü | +12,4 | **+4,9** | +4,9 |
| Arka: kulak | +9,1 | **+0,6** | +2,4 |
| Arka: ense | +26,7 | **−1,2** | −3,0 |
| Ön: üst yan | +9,1 | **+4,9** | +4,3 |
| Ön: şakak / kulak üstü | +5,2 | **−1,8** | −1,8 |
| Ön: kulak | −6,7 | −14,6 | −13,3 |
| Ön: kulak altı | −5,8 | **−28,2** | −23,9 |
| Profil arka (sağ / sol) | −34 / +7 | değişmedi (≤1 mm) | değişmedi |

**Bedel:** ön ve 3/4'te kulak altında sarkan teller boyuna yaklaştı. Ön panel o bantta daha geniş saç gösteriyor (önde −6 → −28 mm). Teller hâlâ görünüyor (`03` ve `04` board'ları).

## 5. İnce tel pass'i (H2, h74b)

- h74a'ya 3521 ince ayrık tel eklendi: mevcut `fly` / `mess_face` / `mess_ear` / `mess_bun` tellerinin %35'i kopyalandı.
- Her kopya kökü çevresinde ≤8° döndürüldü, %75–105 boyda, hafif dalgalı.
- Kütle silüeti değişmedi (yukarıdaki tablo).
- Etki küçük ve çoğunlukla topuz–ense çevresinde; saç çizgisinde fark yok denecek kadar az (`04_HAIR_DETAIL.jpg`).

## 6. Dürüst değerlendirme

| Kriter | Durum | Not |
|---|---|---|
| Ön silüet referansa yaklaşsın | **KISMEN** | Önde alt yanak–çene konturu zaten referans çizgisindeydi (±1–5 mm); O1G ön konturu değiştirmedi (≤0,6 mm). Kalan fark çene tabanı (aday 2–3 mm aşağıda); paneller çelişkili olduğu için dokunulmadı. |
| Yanak / çene / çene ucu geçişi yumuşasın | **KISMEN (az)** | Elmacık altı ve yanak çukurları biraz azaldı; 3/4 yanak kütlesi konturu 1,3 mm yaklaştı. Görsel fark ince. |
| Yüz daha az kemikli okusun | **KISMEN (zayıf)** | Kontur ve burun-dudak çizgileri referansla zaten eşleşiyor. Kalan "kemikli / sert" okuma iç biçim ve gölgelemeden geliyor; ayrı bir pass gerekiyor (aşağıda). |
| Saçın yan / arka silüeti daha dar ve doğal olsun | **BAŞARILI (arka, ön üst) / KISMEN (ön kulak altı)** | Arka kulak ve ense referansa oturdu (+9 → +1, +27 → −1 mm); ön üst yan ve şakak yaklaştı. Ön kulak altı referanstan daha dar kaldı. |
| Küçük ayrık teller geri gelsin | **BAŞARILI** | Asıl neden bellek kaynaklı render hatasıydı. Doğru render'da teller geri. H2 topuz çevresine az miktar ekledi. |
| Kask / blok görünümü olmasın | **BAŞARILI (render) / KISMEN (biçim)** | Kask görüntüsü render hatasıydı. h74a'da ense enseye doğru daralıyor. Referanstaki belirgin, alçak ve dağınık topuz biçimine henüz ulaşılmadı. |
| Çene uzatılmasın, yüz sertleşmesin / oyulmasın | **BAŞARILI** | Çene, çene açısı ve dudak 0 mm; yeni çukur 0. |

Teknik başarı referansa benzerlikle aynı şey değil. Yüzdeki görsel değişim küçük; saçtaki en büyük görsel kazanç render hatasının giderilmesi.

**Öneriler (her biri ayrı küçük pass olarak):**
1. Kaş çizgisi 2–7 mm yukarı. Kaş daha önce reddedildi; sizin kararınız.
2. Alt dudak hacmi ~2–3 mm.
3. Alt yüzde gölgelemeye dayalı iç biçim pass'i (kemikli okumanın kaynağı).
4. Topuzu alçaltıp daha belirgin ve dağınık yapmak.
5. Saç rengi referanstan koyu.

## 7. Teknik

| Kontrol | Sonuç |
|---|---|
| ww5bo1g | ww5bs10f kopyası + doğrudan fark (1178 köşe, en çok 2,3 mm); normaller ve teğetler yeniden; 858 morph ve DNA korundu |
| h74a / h74b | içe aktarma, simülasyon, kask ve LOD'lar tamam; ww5bo1g bağlamaları kaydedildi (4/4 + 4/4) |
| Rig pozları | 27, temiz (`08_TECH_Rig.jpg`) |
| Hareket kareleri | O1G + h73b 27; O1G + h74b 27; temiz, saç hareket halinde tellerle render ediliyor |
| Korunan adaylar | 89/89 (iki zincirde) |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7/7) |
| LOD | TEST EDİLMEDİ |
| Editör | bellek nedeniyle yeniden başlatıldı (`lk_editor_restart.sh`); sonrasında bütün çekimler taze editörde |
| Disk | C: 50 GB boş |

## Board'lar

| Dosya | İçerik |
|---|---|
| `00_NOHAIR_ALL_VIEWS.jpg` | saçsız: S10F / O1G / referans; 5 açı |
| `01_FACE_OVERLAY_A.jpg`, `01_FACE_OVERLAY_B.jpg` | yüz overlay'i: ön, iki 3/4, iki profil; S10F ve O1G çizgileri referans çizgileriyle |
| `02_HAIR_OVERLAY.jpg` | saç silüeti overlay'i: ön, arka, 3/4, iki profil; h73b / h74a / h74b. Profil kenarındaki yatay çizgiler kare dışına taşan topuzun örnekleme artefaktı. |
| `03_HAIR_ALL_VIEWS.jpg` | S10F bozuk render / taze h73b / h74b / referans; 6 açı |
| `04_HAIR_DETAIL.jpg` | ince teller: saç çizgisi ve topuz–ense yakın planı |
| `08_TECH_*.jpg` | rig ve hareket kareleri |

- Sayılar: `data/face_lines_S10F_O1G.txt`, `data/hair_lines_h73b_h74a_h74b.txt` ve `data/ov5_*.json`.
- Kaynaklar: `SourceAssets/Characters/GD11_OverlayO1_20261009`.
- Saç tel verisi: `Saved/Codex/GD11_HairQ_20261006/hair/h74a`, `h74b`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
