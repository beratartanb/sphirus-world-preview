# GD11 saç revizyonu G: ense bloğu, topuz oturuşu, ön yan tutamlar (yüz sabit)

Tarih: 2026-10-04. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi.

## Başlangıç (doğrulandı)

**Kaynak:** F raporu, commit `9134e507`.

| Parça | Asset / dosya |
|---|---|
| Saç (başlangıç) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementF_20261004/Hair/GR_LK_Hair_{Main,Loose}_h40d`, bağlamalar `GB_G11RF_*_f4abh40d` |
| Yüz (değişmedi) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab` + DNA `MHC_G11RD_F4AB_Head` |
| Ten / göz / kaş / kirpik | k10 / e2 / M_SlightArch / S_Thin; değişmedi |

- F'den daha yeni yerel çalışma yoktu. h40d aynen duruyor.
- **Yeniden üretilebilirlik kontrolü:** G oluşturucusu h40d ayarlarıyla çalıştırıldı (h41s). Sonuç h40d ile **bit bit aynı** (67.035 ana + 3.839 serbest tel). Böylece G'deki her fark yalnız yapılan değişiklikten geliyor.

## Yeni aday

`/Game/Sphirus/CharacterLab/GD11_HeadRefinementG_20261004/`

| Parça | Asset / dosya |
|---|---|
| Saç | `Hair/GR_LK_Hair_{Main,Loose}_h41f` + kask; LOD tablosu ayarlı |
| Bağlamalar | `Face/Bindings/GB_G11RG_*_f4abh41f`; hepsi F4ab yüzünü hedefliyor |

**Yazma yolları:** ilk çekimden önce bütün yollar G'ye yönlendirildi.
- G scriptleri (`gd11rg_face_run.sh`, `gd11rg_caps.sh`) stüdyo klasörü G değilse çekim yapmıyor.
- B, C, D, E ve F'ye bağlama yazmayı reddediyor.
- **Korunan dosyalar: 59/59 birebir aynı**, F dahil.

## Düzenlenebilir kılavuzlar (yeni)

- **`guides/h41f_guides.blend`:** her grup ayrı koleksiyon, her kılavuz ayrı eğri nesnesi; referans yapım kafası da içinde.
  - Gruplar: `nape_to_bun`, `back_to_bun`, `side_to_bun`, `top_to_bun`, `front_to_bun` (kuyrukları = topuz girişleri), `bun_loops` (topuz alt biçimi: `c_off` / `r` / `turn` özellikleri), `nape_free_g`, `behind_ear`, `front_side_frame`, `temple_veil`, `ear_lock`, `face_frame*`, `ff_wave`, `side_long`, `fringe`.
- **`h41f/guides.json`:** aynı veri, JSON olarak.
- **`h41f/strand_tags.json`:** her üretilmiş telin hangi kılavuzdan geldiği.
- **Düzenleme akışı:** `.blend` düzenlenir → `blender_g11rg_guides.py import` → `SPH_GUIDES_IN=<json>` ile yeniden üretim. Yalnız düzenlenen gruplar değişir, rastgele seçimler aynen kalır.
- **Gidiş-dönüş testi:** 125 eğri + 10 topuz grubu, **0,00000 cm** fark.
- **Korunan kopya (Saved dışında):** `SourceAssets/Characters/GD11_HairG_20261004/`; `README.txt`, `h41f/`, `guides/`, `tools/`, yapım kafası.
- **Dürüstlük notu:** kılavuzlar kodla üretildi ve düzenlendi. Ense girişi `nape_entry_v1.json` ile düzenlendi. Serbest elle groom yapılmadı.

## 1. Ense bloğunun kaynağı (board 01)

Etiketli tel katmanları kullanıldı: tam / serbest ense yok / ana ense yok / yalnız ana ense / yalnız serbest / topuz.

- **Bloğun kaynağı:** `nape_to_bun` grubundaki 4 ana kilit (prim 17, 19, 20, 44; toplam 4.470 tel).
  - Bu teller topuz ile ense saç çizgisi arasında **kafatasından uzak, sıkı bir dikdörtgen kütle** oluşturuyordu.
  - Nedenleri:
    - genel yüksek yakınsama ve arka kümelenme ayarları (CONV 0,38, BACK_CLUMP 0,7) ense tutamlarını dar demetlere topluyordu;
    - topuz halkaları ense tellerinin girişini aşağıda tutuyordu.
- **Kök çizgisi sorun değildi:** F'de zaten yumuşatılmıştı.
- **Serbest ense tutamları (eski NAPE_ grubu):** 8 eşit aralıklı, eşit boylu tel tarak gibi diziliyordu ve alt sınırı daha da belirginleştiriyordu.

## 2. Ensede yapılanlar (board 02)

| Değişiklik | Etki |
|---|---|
| `SPH_NAPE_FIX`: yalnız ense kilitlerinde yakınsama ×0,35, arka kümelenme 0, topuz halkası yarıçapı ×0,5 (`SPH_NAPE_LOOP`) | Ense saçı geniş ve yumuşak bir yelpaze; topuzun çekirdeğine sarılıyor. |
| `SPH_NAPE_FLAT` 0,22 cm | Topuzun alt kenarının altındaki ense saçı saç derisine yatırıldı (ince, yukarı taranmış katman); topuz girişine doğru serbest bırakılıyor. |
| Eski tarak dizisi kapatıldı (NAPE_N 0) | Yerine `SPH_NAPE_G`: 6 düzensiz grup; aralık, boy (1,4–4,3 cm), kalınlık ve yan kavisleri farklı. |

**Kök, tutam ve uç ayrı ayrı ele alındı.** Ense görünürlüğü ölçülü; tıraşlı görünüm yok.

## 3. Topuz oturuşu (board 03)

**Kaynak biçim, dinamik değil.** Ana groom'da (topuz ve ana kütle) simülasyon **kapalı** (`EnableSimulation=False`); statik görüntü ile hareket sonrası görüntü aynı. Simülasyon yalnız serbest tellerde açık.

"Aşağı çekiliyor" hissinin üç nedeni:
1. Ense kütlesi topuzun devamı gibi okunuyordu (2. bölümde düzeltildi).
2. Ense kilitlerinin kuyrukları topuzun altına giriyordu. Düzeltme: `nape_entry_v1.json` kılavuz düzenlemesi; kuyrukların son %40'ı yukarı (+1,3–1,4) ve kafaya doğru (+0,8) kaydırıldı.
3. Topuz merkezi biraz aşağıda ve geride kalıyordu. **Ölçülü düzeltme:** z 161,6 → 162,0 (+0,4 cm), y −8,6 → −8,4 (kafaya 0,2 cm). Ayrı karşılaştırma h41h'de; topuz enseye inmedi ve büyümedi.

## 4. Ön yan tutamlar (board 04)

**Yeni `SPH_FSF` aileleri:** ön yan saç çizgisinin farklı köklerinden çıkan tutamlar.
- Karakter solunda 6, sağında 5 tutam.
- Uç yüksekliği z 151,5–162,4 arası: bazıları şakakta kalıyor, bazıları üst yanağa, bazıları çene hizasına iniyor.
- Kalınlık 0,20–0,38, dalga ve kavisler farklı.
- Yüzden uzaklık kökten uca 0,35 → 1,8 cm artıyor.

**Eski yüz çerçevesi kalın tutamları zayıflatıldı:** `SPH_FACE_MULT` 0,75 → 0,35. "Birer kalın tutam" yerine birbirine karışan bir aile oluştu.

**Değişmeyenler:** saç çizgisi, alın yüksekliği. Gözler, burun ve ağız kapanmıyor.

## Kontrol adayları

| Aday | İçerik |
|---|---|
| h41s | h40d'nin birebir kopyası |
| h41g | yalnız ense |
| h41h | ense + topuz oturuşu |
| h41c | yalnız ön yan |
| **h41f** | **birleşik final** |

Ara denemeler:
- **h41a / h41b:** ense, yatırma olmadan.
- **h41e:** ense + giriş + ön yan, topuz kaydırma olmadan.

**Ön–tepe akışı, saç çizgisi ve renk** h40d ile aynı.

## 5. Teknik (board 07)

| Kontrol | Sonuç |
|---|---|
| Bağlama | 4 bağlamanın hepsi `SKM_G11RD_Face_f4ab`'i hedefliyor. Yüz auto-rig yok. |
| Baş eğimi | Yaklaşık 26° öne ve 30° yukarı (dinamik). Topuz biçimini koruyor; ense telleri boyna girmiyor; ön tutamlar yüze saplanmıyor; nötre temiz dönüş. |
| Hareket | Dönüşler ve koşu-durma (27 çekim) temiz. |
| LOD | Temiz editörde ayarlandı (%65 ×1,25 / %40 ×1,7 / kask), yeniden açılışta korunmuş. Mesafe testi 1,25–25 m, önden / 45° / arkadan. Ense sınırı, topuzun alt biçimi ve ön tutamlar sıçramıyor. Bu bir **mesafe görünüm testi; aktif LOD indeksi bu build'de okunamıyor.** |
| Yeniden açılış | Temiz editörde yüz, DNA, 858 morph, h41f groom'ları, materyaller, kask ve 4 bağlama yüklendi; kaydedilmemiş paket yok. |
| Korunan dosyalar | **59/59** |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| ENSE BLOĞUNUN KAYNAĞI | BAŞARILI (belirlendi: ana `nape_to_bun` kilitleri + tarak dizisi) |
| ENSE KÖK–TUTAM–UÇ BÜTÜNLÜĞÜ | KISMEN (yatık ve yelpaze; arkadan aydınlatmada alt kenarda hâlâ ince bir kısa tel sınırı) |
| KÜT ALT SINIRIN GİDERİLMESİ | KISMEN (panel gitti, sınır inceldi ve düzensizleşti; tamamen kaybolmadı) |
| TOPUZUN BAŞA OTURMASI | KISMEN (biraz daha yukarıda ve içeride; hâlâ derli toplu) |
| AŞAĞI ÇEKİLME HİSSİNİN GİDERİLMESİ | KISMEN (ense paneli ve alt giriş düzeltildi; profilde hafif ağırlık kalıyor) |
| TOPUZ–ENSE BAĞLANTISI | BAŞARILI |
| ÖN YAN TUTAM ÇEŞİTLİLİĞİ | KISMEN (çok köklü aile var; tutamlar ince olduğu için etki ölçülü) |
| DOĞAL ASİMETRİ | BAŞARILI (6 / 5, farklı boylar) |
| YÜZÜ ÇERÇEVELEME | KISMEN |
| ÖN–TEPE KAZANIMLARININ KORUNUMU | BAŞARILI |
| YÜZ/DNA/TEN KORUNUMU | BAŞARILI |
| BINDING | BAŞARILI |
| HAREKET | BAŞARILI |
| LOD | BAŞARILI (mesafe testi; aktif indeks doğrulanamadı) |
| YENİDEN AÇILIŞ | BAŞARILI |

## Açık kalanlar

- **Ense alt kenarı:** ince bir kısa tel çizgisi kalıyor.
- **Ön yan tutamlar:** referanstaki kadar hacimli ve dağınık değil.
- **Saç karakteri:** genel olarak hâlâ referanstan daha düzenli.

Bunların bir sonraki adımı, `h41f_guides.blend` üzerindeki ilgili grupları tek tek düzenlemek.

## Board'lar

| Board | İçerik |
|---|---|
| 01 | Ense bloğunun kaynağı (katmanlar) |
| 02 | Ense önce/sonra: h40d / yalnız ense / final |
| 03 | Topuz oturuşu: h40d / ense+topuz / final |
| 04 | Ön yan tutamlar: orijinal / h40d / yalnız ön yan / final |
| 05 | Düzenlenebilir kılavuzlar ve final katmanları |
| 06 | Bütün baş: ön, iki profil, arka |
| 07 | Hareket, LOD, yeniden açılış |
