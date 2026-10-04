# GD11 saç revizyonu H: ensedeki L biçimi, topuz birleşimi, sağ/sol 3/4 dengesi (yüz sabit)

Tarih: 2026-10-04. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi.

## Başlangıç (doğrulandı)

**Kaynak:** G raporu, commit `c860e345`.

| Parça | Asset |
|---|---|
| Saç (başlangıç) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementG_20261004/Hair/GR_LK_Hair_{Main,Loose}_h41f`, bağlamalar `GB_G11RG_*_f4abh41f` |
| Yüz / DNA / ten (değişmedi) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab`, `MHC_G11RD_F4AB_Head`, k10 / e2 / M_SlightArch / S_Thin |

- G'den daha yeni yerel çalışma yoktu.
- Kullanıcının işaretlediği yakın plan h41e idi. **Board 01** final h41f'i aynı arka-yan açılardan, arkadan aydınlatmayla gösteriyor.

## Yeni aday

`/Game/Sphirus/CharacterLab/GD11_HeadRefinementH_20261004/`

| Parça | Asset / dosya |
|---|---|
| Saç | `Hair/GR_LK_Hair_{Main,Loose}_h42d` + kask; LOD tablosu ayarlı |
| Bağlamalar | `Face/Bindings/GB_G11RH_*_f4abh42d`; hepsi F4ab yüzünü hedefliyor |
| Korunan kaynak (Saved dışında) | `SourceAssets/Characters/GD11_HairH_20261004/`: `h42d/` (`build_env`, `strands`, `abc`, `guides.json`, `strand_tags.json`, `guides_edited.json`), `guides/h42d_guides.blend`, `guides/h42c_guides.blend` (topuz düzenlemesi), `guides/h41f_base_guides.json`, `tools/`, `README.txt` |

**Yazma yolları:** ilk çekimden önce bütün yollar H'ye yönlendirildi; H scriptleri stüdyo klasörü H değilse çekim yapmıyor.

**Korunan dosyalar: 62/62 birebir aynı.** G (h41f) dahil.

## 0. Kılavuz gidiş-dönüşü (düzeltildi)

İlk deneme: `.blend` → JSON → yeniden üretim, değişiklik yapılmadan (h42rt).
- Sonuç h41f ile aynı değildi: 3.804 ana + 301 serbest tel, en fazla 0,72 cm fark.
- **Neden:** kılavuz koordinatları yuvarlanıyor (4 basamak, `.blend` içinde float32). Oluşturucunun yüzeye yansıtma adımları (en yakın yüz normali) bu küçük farkı bazı kilitlerde büyütüyor.

**Düzeltme:** bir kılavuz yalnız `.blend`'in **dışa aktarıldığı kaynak kılavuzdan** (`SPH_GUIDES_BASE`) 0,001 cm'den fazla farklıysa "düzenlenmiş" sayılıyor; aksi hâlde tam hassasiyetli hesaplanan değer kullanılıyor. Düzenlenen kılavuzların listesi `guides_edited.json`'a yazılıyor.

- Değişiklik yapılmayan gidiş-dönüş (h42rt2) artık **bit bit aynı**; düzenlenen kılavuz sayısı 0.
- Ara bir sürümde karşılaştırma tabanı yanlış seçilmişti. Ön yan ve topuz değişiklikleri birçok kilidin hesaplanan yolunu değiştirdiği için eski eğriler "düzenlenmiş" sayıldı. Bu fark edildi ve h42c/h42d yeniden üretildi. **Final h42d'de yalnız gerçekten düzenlenen 3 topuz grubu** "düzenlenmiş" olarak listeleniyor.

## 1. L biçiminin kaynağı (board 02)

Gruplara göre renklendirilmiş tel katmanları kullanıldı: tam / yalnız yan+arka / ense / serbest ve kulak arkası / topuz gizli / düz renk.

| Parça | Kaynak |
|---|---|
| **Yatay** | `side_to_bun` ana kütlesinin kulak arkasındaki alt kenarı (yeşil). Üzerinden geçen `temple_veil` tutamları (mor) bu çizgiyi güçlendiriyor. |
| **Dikey** | `nape_to_bun` şeridi (turuncu, G'deki 4 kilit). |
| **Köşe** | İkisinin arasındaki bölgede kök yok. |

**Neden kök yok:** saç çizgisi tablosu kulak arkasında (azimut 115°) z≈161,5'te, 135°'de 158'de, 150°'de 153,5'te. Kulak arkası yatay ilerleyip enseye dik iniyor. Köşe bölgesinde yalnız 88 (karakter solu) / 226 (karakter sağı) kök var.

**Işık kenarı değil:** geometrik sınır olduğu tel katmanlarında doğrulandı.

## 2. Yüzeye yatırma (SPH_NAPE_FLAT) kontrolü (board 03, satır 2)

- **Kapalı (h42nf):** 4.214 ense teli değişti (en fazla 3,4 cm). Ense bloğu kalınlaşıp uzadı.
- **Sonuç:** yatırma bloğu inceltiyor ama L'nin nedeni değil. Kılavuz şeklini bozmuyor; yalnız topuzun alt kenarının altındaki ense bölümünü saç derisine yaklaştırıyor. Finalde açık kalıyor.

## 3. Ense–yan geçişi (board 03)

**Köşe dolgusu (`corner_to_bun`, yeni aile)**
- Kendi RNG'si var, mevcut tellerin hiçbiri değişmiyor.
- Kökler: yumuşatılmış arka saç çizgisi ile eski saç çizgisi arasındaki band (112–152°, 161,0 → 153,4).
- Teller saç derisini izleyerek çapraz yukarı-geri gidip topuzun alt-yan tarafına giriyor; topuz çekirdeğine sarılıyor.
- Her taraf için 4 düzenlenebilir kılavuz; 2.600 tel.
- Kökler üst banda daha yoğun (`SPH_CORNER_BIAS` 0,7).

**Ense seyreltmesi (`SPH_NAPE_THIN`)**
- Alt saç çizgisine yakın ense ve köşe telleri olasılıkla azaltılıyor: saç çizgisinde %25, 2,4 cm içinde %100.
- 1.020 tel çıkarıldı; ensede kademeli görünürlük.
- Diğer teller değişmedi.

**Sonuç:** keskin dikey şerit kenarı ve boş köşe gitti; kulak arkasından enseye köşegen bir geçiş var. Alt kenar inceldi ve kademelendi. Ancak ense hâlâ **ters yamuk bir alan** olarak okunuyor: L kırıldı, ama ense tamamen doğal bir saç çizgisine dönüşmedi.

## 4. Topuz (board 04)

- **Konum değişmedi** (z 162,0 / y −8,4, G ile aynı).
- **Biçim, `.blend` üzerinde düzenlendi** (`blender_g11rh_bunedit.py`): 3 alt halka grubunda (bun:6/7/9) yarıçap ×0,85, merkez +0,35 cm yukarı ve +0,3 cm kafaya doğru.
- **Simülasyon:** ana groom'da kapalı (statik görüntü = render). Serbest tellerde açık.
- **Sonuç:** alt ağırlık hafifçe azaldı. Köşe dolgusu topuzun alt-yan girişini besliyor. Topuz hâlâ derli toplu ve oval okunuyor.

## 5. R/L tanısı (board 05)

**Kamera:** R/L kameraları x=0'a göre tam simetrik (yaw −58 / −122, pitch 1, uzaklık ve FOV aynı). Kafa merkezi kayması 27 px.

**Çekim koşulları:** aynı yüz, materyal, poz ve LOD.

**Saçsız ve simetrik ışık:**
- Yeni `front` ışığı (yüz orta hattının önünde tek spot) eklendi. Ortalama parlaklık R 0,463 / L 0,467.
- Silüet genişliği 831 / 837 px (%0,7). Ten ve clay görünümde R ile aynalanmış L neredeyse aynı.
- **Yüz geometrisi farkı açıklamıyor.**

**Stüdyo ışığı:** ana ışık bir taraftan geliyor. R görünümü (karakter sağı) yüzü önden ve düz alıyor; L yarı gölgede ve modelli. **"R daha ince ve uzun" algısının büyük kısmı ışıktan geliyor.**

**Saç:** karakter sağında şakak ve kulak çevresi biraz daha açıktı; uzun dikey tutamlar yüzü uzun gösteriyordu.

**Not:** `sky` adlı ilk simetrik ışık denemesi karakteri aydınlatmadı; yalnız silüet olarak kullanıldı.

## 6. Sağ saç çerçevesi (board 06)

Yalnız karakter sağında:
- Ön yan tutam tablosu değişti (`SPH_FSF_TABLE`): uç z 151,5 olan en uzun tutam kaldırıldı; daha kısa ve orta boy, yüzden biraz daha uzak tutamlar eklendi (6 adet, uç z 155,6–162,2).
- Sağdaki uzun yan kilit kaldırıldı (`SPH_SIDE_SKIP_R` 0,1,2).
- **L tarafı değişmedi.**

**Sonuç:** fark hafif. R/L dengesizliğinin ana kaynağı ışık olduğu için saçla tam kapanmadı.

## 7. Teknik (board 08)

| Kontrol | Sonuç |
|---|---|
| Bağlama | 4 bağlamanın hepsi `SKM_G11RD_Face_f4ab`'i hedefliyor. Yüz auto-rig yok. |
| Baş eğimi / dönüş / koşu-durma / nötre dönüş | Temiz. Ense telleri boyna girmiyor; kulak arkası gruplar kulakla kesişmiyor. |
| LOD | Temiz editörde ayarlandı, yeniden açılışta korunmuş. Mesafe testi 1,25–25 m önden / 45° / arkadan; L ve ense paneli geri gelmiyor, topuz sıçramıyor. **Mesafe testi; aktif LOD indeksi okunamıyor.** |
| Yeniden açılış | Temiz editörde yüz, DNA, 858 morph, h42d, materyaller, kask ve 4 bağlama yüklendi; kaydedilmemiş paket yok. |
| Korunan dosyalar | **62/62** |

## Sorulara cevaplar

- **L'nin yatay ve dikey parçalarını hangi gruplar oluşturuyordu?** Yatay: `side_to_bun` alt kenarı (+ `temple_veil`). Dikey: `nape_to_bun` şeridi. Köşe: saç çizgisi tablosunun kulak arkasındaki dik inişi yüzünden köksüz.
- **`SPH_NAPE_FLAT` bu görünümü etkiliyor muydu?** Bloğun kalınlığını azaltıyordu; L'nin nedeni değildi.
- **Kılavuz şekli son işlemlerde bozuluyor muydu?** Hayır. Ama yeniden üretimde yuvarlama hassasiyeti vardı; düzeltildi.
- **Ense gerçekten düzeldi mi?** Köşe dolduruldu ve dikey kenar kırıldı. Ense alanı hâlâ yamuk biçimli: KISMEN.
- **Topuzun biçimi mi konumu mu değişti?** Yalnız biçim (3 alt grup).
- **R/L farkının kaynağı?** Çoğu ışık; bir kısmı saç çerçevesi; kamera ihmal edilebilir; yüz değil.
- **L korundu mu?** Evet, L tarafındaki saçlar değişmedi.
- **Yüz, DNA ve ten sabit mi?** Evet (62/62).

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| ENSE L BİÇİMİNİN KAYNAĞI | BAŞARILI |
| ENSE–YAN SAÇ DOĞAL GEÇİŞİ | KISMEN |
| KÖŞELİ PANEL OKUMASININ GİDERİLMESİ | KISMEN (L köşesi yok; yamuk ense alanı kalıyor) |
| TOPUZUN ANA SAÇLA BÜTÜNLÜĞÜ | KISMEN |
| TOPUZUN İKİ 3/4 AÇIDA DOĞALLIĞI | KISMEN |
| R/L KARŞILAŞTIRMA KOŞULLARI | BAŞARILI |
| R TARAFINDAKİ İNCE/UZUN OKUMANIN KAYNAĞI | BAŞARILI (belirlendi: esas olarak ışık) |
| R SAÇ ÇERÇEVESİ | KISMEN |
| L GÖRÜNÜMÜNÜN KORUNUMU | BAŞARILI |
| ÖN–TEPE KAZANIMLARININ KORUNUMU | BAŞARILI |
| YÜZ/DNA/TEN KORUNUMU | BAŞARILI |
| BINDING | BAŞARILI |
| HAREKET | BAŞARILI |
| LOD | BAŞARILI (mesafe testi) |
| YENİDEN AÇILIŞ | BAŞARILI |

**Öneri:** inceleme ışığında, stüdyo ana ışığı R/L karşılaştırmalarında simetrik bir ışıkla birlikte kullanılmalı. Yüze bu turda dokunulmadı; yüzü değiştirme önerisi yok.

## Board'lar

| Board | İçerik |
|---|---|
| 01 | Başlangıç doğrulaması: final h41f, işaretli açılar |
| 02 | L biçiminin kaynağı: grup renkli katmanlar |
| 03 | Ense–yan önce/sonra: h41f / yatırma kapalı / yalnız köşe / final |
| 04 | Topuz oturuşu: h41f / yalnız topuz düzenlemesi / final |
| 05 | R/L tanısı: saçsız ten, clay, tam saç; simetrik ve stüdyo ışığı |
| 06 | R/L saç dengesi |
| 07 | Düzenlenen kılavuzlar |
| 08 | Bütün baş ve teknik |
