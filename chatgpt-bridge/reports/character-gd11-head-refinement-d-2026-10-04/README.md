# GD11 baş revizyonu D: mevcut tipi koruyarak tamamlama (üst yanak desteği, çene geçişleri, kulak arkası saç, arka baş silüeti)

Tarih: 2026-10-04. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi; oynanabilir karakter değişmedi.

## Başlangıç adayı (doğrulandı)

**Başlangıç:** refinement C. Bu C, D85/h34 (B) ya da R3/h32 değildir.

| Parça | Asset |
|---|---|
| Yüz | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementC_20261004/Face/SKM_G11RC_Face_f3`, DNA `MHC_G11RC_F3_Head` (858 morph) |
| Saç | `.../GD11_HeadRefinementC_20261004/Hair/GR_LK_Hair_{Main,Loose}_h37`; kaynak `Saved/Codex/GD11_HeadRefinementC_20261004/hair/h37/strands.npz` |
| Ten | `.../GD11_HeadRefinementC_20261004/Skin/*_gck10` (k10) |
| Bağlamalar | `.../Face/Bindings/GB_G11RC_*_f3h37` |

Doğrulama: C'nin yeniden açılış kaydı (`reopen_check.json`) ve D'nin ilk kanıt çekimleri. Kullanıcı görsellerindeki "F3 / h37 / k10" etiketleriyle aynı paket.

## Yeni aday

`/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/`

| Parça | Asset |
|---|---|
| Yüz | `Face/SKM_G11RD_Face_f4ab`, DNA `MHC/DNA/MHC_G11RD_F4AB_Head`. Tek bir yeni auto-rig: fit ortalaması 0,016 mm, 858 morph, 8 LOD. |
| Saç | `Hair/GR_LK_Hair_{Main,Loose}_h38d` + kask; LOD tablosu ayarlı |
| Bağlamalar | `Face/Bindings/GB_G11RD_*_f4abh38d` |
| Ten | C'nin k10'u, salt-okunur kullanıldı; değişmedi |
| Göz / kaş / kirpik | GD11 e2 / M_SlightArch / S_Thin; değişmedi |

## 1. Arka uzamanın kaynağı: ANA SAÇ KÜTLESİ (board 04)

Kafatası **ana neden değil.**
- Saçsız baş: arka nokta y −6,2 cm.
- Glabella–arka kafa uzunluğu yaklaşık 19,7 cm; ortalamanın biraz üstünde ama normal aralıkta.
- Kafatasına **dokunulmadı.**

Tel geometrisi katmanlara ayrıldı (`blender_g11rd_backsil.py`, aynı ortografik profil çerçevesi; `data/back_silhouette_*.json`): kafatası / topuz dışı ana saç / topuz çekirdeği / serbest teller.

| Bant (z, cm) | h37 ana saç arka y | Kafatasından uzaklık h37 | h38d ana saç arka y | Uzaklık h38d |
|---|---|---|---|---|
| 162–164 | −14,79 | 9,26 | −13,67 | 8,13 |
| 164–166 | −14,18 | 8,36 | −12,77 | 6,95 |
| 166–168 | −13,59 | 7,97 | −11,15 | 5,53 |
| 168–170 | −10,79 | 6,06 | −8,33 | 3,59 |
| 170–172 | −10,07 | 6,45 | −7,86 | 4,24 |

**İki ayrı neden bulundu:**

1. **Lift alanı.**
   - Arka tepedeki uzaklık = taban + tepe kaldırma + arka kaldırma ≈ 0,45 + 3,0 + 1,15 ≈ 4,6 cm.
   - Önceki turda ön/tepe hacmi için artırılan tepe kaldırma (LF_TOP 3,0) arkada da aynı oranda etki ediyordu. Sonuç: topuzun önünde ve üstünde bir "yastık".
2. **Topuzun kaçan uçları.**
   - 1.901 telin (%2,8) son 2–3 noktası topuz merkezinden 3,9–5,7 cm uzağa, topuzun arkasına taşıyordu.

Topuz konumu ve topuz çekirdeği neden değil. Yakın planda ek kabuk ya da mesh görünmüyor (kask yalnız LOD3'te). Bağlama veya ölçek hatası yok.

## 2. Saç: h37 → h38d (board 05, 06, 09)

Oluşturucunun D kopyası `blender_g11rd_hair.py`. Yeni ve ayrı kontroller:

| Parametre | h37 | h38d | Etki |
|---|---|---|---|
| `LF_TOPBACK_CUT` (yeni) | 0 | 0,7 | Tepe kaldırma yalnız başın **arka** yarısında azalır; ön ve tepe aynı kalır |
| LF_BACK | 1,15 | 0,45 | Arka-üst yuvarlanma |
| `SPH_BUN_ESC_R` (yeni) | 1,0 | 0,45 | Topuzdan kaçan uç açılımı |
| `SPH_BUN_AXS` (yeni) | 1,0 | 0,4 | Topuz halkalarının eksen boyunca saçılması |
| SPH_BUN_CJ | 1,1 | 0,8 | Topuz grup merkezi dağılımı |
| `SPH_BEHIND_EAR` (yeni aile) | yok | 1,5 | Kulak arkası salık tutamlar |
| `SPH_BE_OUT` | — | 1,55 | Tutamların kafadan ayrışması (kulak ile saç arasında derinlik) |

**Kulak arkası tutamlar:**
- Sağda 3, solda 2; farklı uzunluk, genişlik ve tel sayısında.
- Kulağın gerisinden çıkıyor (y ≤ −2,7, kulağın önüne geçmez), hafif dışa açılıp sarkıyor, sonra ense/topuz akışına geri dönüyor.
- Kulak arkası serbest tel sayısı 190 → 420.

**Korunanlar:**
- Ön ve tepe hacmi: ön-üst en yüksek nokta 175,94 → 175,98 cm.
- Saç çizgisi ve alın kökleri (yoğunluk ve saç çizgisi parametreleri h37 ile aynı).
- Topuz konumu (161,6 / −8,6) ve saç rengi.

**Ara denemeler:**
- h38a ve h38b: arka kaldırma ve eksen saçılması tek başına yalnız 0,5–0,7 cm kazandırdı.
- h38c: kaçan uç ölçeği ve arka tepe kesimi eklendi.
- h38d: h38c'ye ek olarak kulak arkası tutamları daha ayrışık.
- Her biri aynı profil çerçevesinde sayısal ölçüldü.

## 3. Üst yanak / elmacık yanal desteği: YAPILDI, KABUL (board 07)

- **G1** (`data/G1.json`): dış göz altından kulak üst yarısı yönüne:
  - 0,6 mm yanal plato alanı (z 158,2–161,6, y 1–8,5);
  - 0,35 mm öne alan, burun dondurulmuş;
  - geniş rampalar.
- **Neden kabul:** clay'de üst yanak düzlemi göz altından kulağa doğru biraz daha devamlı okunuyor. Yüz genişlemedi, düzleşmedi, keskin kemik rafı yok.
- **Dokunulmadı:** göz aralığı, göz küreleri, burun, kulak, şakak ve kafatası genişliği, çene kemiği, ağız köşeleri.
- **Gerçek render'da fark çok küçük;** bu bilinçli bir tercih.

## 4. Çene geçişleri: YAPILDI, KABUL (board 08)

**Önce kaynak tespiti:**
- F3'te çene ön profili z 151,5–153,5 arasında neredeyse düz.
- Alt dudak altı geçiş, çene en önündeki noktanın yalnız 0,11 mm gerisinde.
- Yani geometri "tek parça". Sorun ışık ya da normal haritası değil.

**G2** (`data/G2.json`):

| İşlem | Değer |
|---|---|
| Çene yastığı (normal yönünde) | +0,5 mm |
| Yan geçiş düzlemleri | −0,25 mm |
| Alt dudak altı yumuşak geçiş | −0,25 mm |
| Gevşetme | 1 tur |

- Çene merkezi, genişliği ve uzunluğu değişmedi.
- Kazınmış çizgi, oluk, raf veya asimetri yok.

## 5. Korunması gereken bölgeler

| Bölge | Durum |
|---|---|
| Burun, gözler, kaşlar, göz kapakları, ağız genişliği, dudaklar | **Değiştirilmedi.** G1 ve G2'nin maskeleri bu bölgelerin dışında. |
| Alın–burun kökü | Yeni kusur görülmedi; değiştirilmedi. |
| Ten / yaş | k10 aynen kullanıldı. Kırışıklık eklenmedi, yaşlandırma yok. |

## 6. Teknik

| Kontrol | Sonuç |
|---|---|
| Bağlamalar | Final f4abh38d bağlamalarının dördü de `SKM_G11RD_Face_f4ab`'i hedefliyor (yeniden açılışta okundu) |
| Rig (54 çekim) | Göz kırpma, bakış, gülümseme, dudak kapama, çene ve ağız açma, vizemler, yanak sıkıştırma. Yeni çene ve yanak geçişlerinde bozulma yok. |
| Hareket (27 çekim) | Dönüşler, koşu-durma, etrafa bakma. Kulak, ense ve boyun çakışması görülmedi. Güçlü baş eğimi kapsanmadı. |
| Groom LOD | Temiz editörde ayarlandı. Mesafe testi 1,25 / 3 / 6 / 9 / 12 m'de örtü kesintisiz. 20 m test edilmedi. |
| Yeniden açılış | Temiz editörde yüz (DNA, 858 morph, 8 LOD), h38d groom'ları, materyaller, kask ve 4 bağlama yüklendi. LOD tablosu korunmuş. Önce ve sonra kaydedilmemiş paket yok. |
| Korunan asset'ler | **51/52.** Aşağıdaki istisnaya bakın. |

**Dürüst istisna:**
- Başlangıç adayı C'deki iki **stüdyo sunum materyali** yeniden kaydedildi: `Studio/MI_LK_Backdrop`, `Studio/MI_LK_Floor2`.
- Neden: kanıt çekimlerinden ilki C'nin face_run scriptiyle kuruldu. O script stüdyo klasörü olarak C'yi kullanıyordu.
- C'nin yüzü, DNA'sı, saçı, bağlamaları ve teni **değişmedi.**
- Sonraki bütün kurulumlar D scriptleriyle, stüdyo klasörü D olarak yapıldı. D scriptleri C'ye bağlama yazmayı reddediyor.

## Değerlendirmeler (ayrı ayrı)

| Başlık | Sonuç |
|---|---|
| MEVCUT TİPİN KORUNUMU | BAŞARILI. Yüz değişiklikleri 0,25–0,6 mm; izolasyon board'unda (09) aynı yüz. |
| ORİJİNAL REFERANSA BENZERLİK | KISMEN. Arka silüet ve topuz okuması daha yakın. Şakak örtüsü ve dağınık saç karakteri hâlâ uzak. |
| SAÇIN DOĞALLIĞI | KISMEN. Daha kontrollü arka kavis, ayrı okunan topuz, kulak arkasında salık tutamlar. Saç hâlâ scriptli, sanatçı kalitesinde değil. |
| BÜTÜN BAŞIN GERÇEKÇİLİĞİ | KISMEN |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (güçlü baş eğimi ve 20 m LOD test edilmedi) |

| Özel kontrol | Sonuç |
|---|---|
| BAŞLANGIÇ ADAYI DOĞRULANDI | BAŞARILI |
| ARKA UZAMANIN KAYNAĞI BELİRLENDİ | BAŞARILI (ana saç lift alanı + topuz kaçan uçları; kafatası değil) |
| KAFATASI KORUNDU | BAŞARILI |
| ARKA SAÇ SİLÜETİ | BAŞARILI (arka-üst taşma −2,5 cm; en arka nokta −1,1 cm) |
| ÖN/TEPE HACMİ KORUNDU | BAŞARILI |
| KULAK ARKASI AKIŞ | KISMEN (tutamlar var ve iki tarafta farklı; etki ölçülü, yakın planda zor seçiliyor) |
| TOPUZ KONUMU VE BÜTÜNLÜĞÜ | BAŞARILI |
| ÜST YANAK YANAL DESTEĞİ | KISMEN (clay'de okunuyor; gerçek render'da çok hafif) |
| ÇENE GEÇİŞLERİ | BAŞARILI (hafif) |
| ÇENE DENGESİ | BAŞARILI |
| GÖZ/BURUN/AĞIZ KORUNUMU | BAŞARILI |
| TEN/YAŞ KORUNUMU | BAŞARILI |
| SAÇ BAĞLANTILARI | BAŞARILI |
| RIG | BAŞARILI |
| DETAY SEVİYELERİ | BAŞARILI (20 m TEST EDİLMEDİ) |
| YENİDEN AÇILIŞ | BAŞARILI |
| KORUNAN VARLIKLAR | KISMEN (51/52; C'nin 2 stüdyo materyali yeniden kaydedildi, karakter asset'i yok) |

## Açık kalanlar

- **Profilde şakak / favori açık:** scriptli oluşturucu bunu üretemiyor; elle yazılmış rehber groom gerekiyor (C raporundaki sınır).
- **Kulak arkası tutamlar:** sınırlı ve ölçülü bırakıldı. Daha belirgin istenirse sayı ve ayrışma artırılabilir, ancak arka hacmi büyütme riski var.
- **Kafatası:** hafif uzun ama normal aralıkta. Değiştirilmedi; istenirse ayrı karar.
- **Güçlü baş eğimi ve 20 m LOD** test edilmedi.

## Board'lar

| Board | İçerik |
|---|---|
| 01 | Bütün baş önden: referans / başlangıç / yeni |
| 02 | İki 3/4 yön: referans / başlangıç / yeni |
| 03 | İki profil: başlangıç / yeni; üretilmiş profiller yalnız YARDIMCI |
| 04 | Arka uzamanın kaynağı: saçsız / ana saç / tam saç (UE) ve tel katmanları |
| 05 | Arka saç hacmi; ön/tepe hacminin korunduğu da görülüyor |
| 06 | Kulak arkası tutamlar: iki taraf, yakın ve bütün baş |
| 07 | Üst yanak desteği: değişmemiş / düzenlenmiş, clay ve gerçek render, iki ışık |
| 08 | Çene geçişleri: değişmemiş / düzenlenmiş, clay ve gerçek render, iki ışık |
| 09 | Değişikliklerin ayrılması: başlangıç / yalnız saç / yalnız yüz / final |
| 10 | Teknik: rig, hareket, LOD mesafe testi, yeniden başlatma sonrası |
