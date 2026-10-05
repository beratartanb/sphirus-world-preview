# GD11 baş revizyonu O: N (n1/h49a) üzerinden — burun ucu–kanat bütünlüğü, özel kaş groom'u, saçın başı kaplaması

Tarih: 2026-10-05/06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi; N kaydı değişmedi.

## Başlangıç (doğrulandı) ve adaylar

| Durum | Yüz / DNA | Kaş | Saç | Bağlamalar |
|---|---|---|---|---|
| **S başlangıç = N kaydı** | `GD11_HeadRefinementN_20261005/Face/SKM_G11RN_Face_n1` / `MHC_G11RN_N1_Head` | `GR_GD_Eyebrows_M_Fine` (reddedilen) | `GD11_HeadRefinementN_20261005/Hair/GR_LK_Hair_{Main,Loose}_h49a` | `GB_G11RN_*_n1h49a` (N, yalnız okundu) |
| **NO yalnız burun** | `GD11_HeadRefinementO_20261005/Face/SKM_G11RO_Face_o6` / `MHC_G11RO_O6_Head` (yeni auto-rig) | M_Fine | h49a | `GB_G11RO_*_o6h49a` |
| **BO yalnız kaş** | n1 | **özel prosedürel kaş `GR_O_Brow_b4`** (`MI_O_Eyebrows_Mid2`) | h49a | hair/kirpik N bağlamaları + `GB_G11RO_EyebrowsCustom_b4_n1h49a` |
| **HO yalnız saç** | n1 | M_Fine | `GD11_HeadRefinementO_20261005/Hair/GR_LK_Hair_{Main,Loose}_h51a` | `GB_G11RO_*_n1h51a` |
| **C birleşik** | o6 | özel kaş b4 | h51a | `GB_G11RO_*_o6h51a` + `GB_G11RO_EyebrowsCustom_b4_o6h51a` |

Ten/göz k10/e2, kirpik S_Thin (hepsinde aynı). Her çekim setinin kompozisyonu editörden okundu (`prov/*.json`: mesh, DNA, groom, bağlama hedefi, materyal, animasyon sınıfı, kamera/ışık çekim json'larında). Korunan dosyalar: `data/preservation_check.txt`.

## Sorulara doğrudan cevaplar

| Soru | Cevap |
|---|---|
| Burun ucu–kanat bütünlüğü düzeldi mi? | **Kısmen.** n1'de uç ayrı bir top, kubbe–kanat arasında dik basamak (0,8 cm / 0,2 cm) ve lobülün altında sert bir raf okunuyordu. o6 (`data/O6.json`): uç yanlara genişletildi (plato alanı +1,5 mm), kubbe yanakları doldurulup kubbe–kanat basamağı yalnız dış yüzey normallerinde maskeli Laplace yumuşatmasıyla kapatıldı, uç tepesi −0,5 mm, infratip +1,6 mm yuvarlandı, kolumella +1 mm öne; nazal maksimum 2,67 mm, burun dışı sıfır (`heat_O6_vs_n1.txt`; burun deliği içi / kanat kenarı / üst dudak dokunulmadı). Önden ve alttan uç kanatlara daha yumuşak bağlanıyor, fakat lobül hâlâ belirgin ve infratip alt kenarı hâlâ sert (board 02). Uç projeksiyonu artmadı. |
| Neden daha güçlü/ farklı yöntemler denenmedi? | Denendi ve reddedildi: O1 (küçük blob opları, 0,7 mm, görünmez), O2 (blob dolgu + yükseklik haritası dolgusu: burun deliği kenarını buruşturdu), O3 (Taubin relax: 0,8 cm basamakta etkisiz), O4 (yükseklik haritası alçak geçiren: lobül çıkıntısını "gören" harita burun deliğini ezdi, 4,9 mm). O5 (maskeli yöntem, hafif) ve O6 (aynı yöntem, daha güçlü) güvenli kaldı; O6 rig'lendi. Hepsi `face/` kaynaklarında, clay karşılaştırmaları `pv/clay_n1_o*`. |
| Referans burun karakteri? | **Kısmen.** Referansta uç geniş, yumuşak ve kanatlarla tek yüzeyde; bizde kubbe daha belirgin, kanat kenarı kalın. Yeni rig: fit ort. 0,017 mm, 858 morph, DNA kalıcı; rig/hareket çekimlerinde burun deliği/uç deformasyonları temiz (board 07). |
| Kaş tasarımı M_Fine'ın yerine geçti mi? | **Evet, özel prosedürel groom.** `blender_g11ro_brow.py`: iç baş (x 1,25) → gövde → kemer tepesi (x 3,4, u=0,62) → kuyruk (x 5,3) orta eğrisi, bölgeye göre kalınlık (iç 0,78 / gövde 0,62 / kuyruk 0,22 cm), kıl açısı (50° → 10° → −16°), uzunluk 0,5 cm, yoğunluk profili, 0,08 asimetri; kökler n1 derisinde (BVH), kıllar deriden 0,15 mm üstte; `.abc` → `GR_O_Brow_b4` + Alembic'ten GroomBinding. Yinelemeler board 03 satır 3: b1 (1,2 cm fazla yukarıda, ince, turuncu) → b2 (yükseklik doğru; MI_Facial_Hair haki, koyu materyal siyah levha) → b3 (iç baş dolu, hâlâ siyah) → **b4** (`MI_O_Eyebrows_Mid2` melanin 0,62 / kızıllık 0,6, tel 0,005 cm, ~1,6 k kıl/kaş). |
| Özel kaş referansa uyuyor mu? | **Kısmen.** Yükseklik (kaş altı–göz merkezi ≈1,7 cm), iç başlangıç, gövde dolgunluğu, yumuşak kemer ve kuyruk incelmesi referans yönünde; nötr ifade, göz/kapak/kaş kemiği mesh'i değişmedi. Eksikler: kuyruk ucunda kopuk birkaç kıl, alt kenar sağ kaşta hafif testere dişi, kıl rengi referanstan biraz daha kızıl, gövde yönleri henüz tek katman (üst-dış kaplama katmanı yok). Hepsi `brow_b4_env.txt` ve materyal ile ayrı ayrı düzenlenebilir (konum/kalınlık/açı/yoğunluk/renk bağımsız). |
| Saç başı doğal kaplıyor mu? | **Kısmen.** h51a = h49a ile aynı örnekleme (kilit kümeleme) + 31 ana kilidin aile bazlı yeniden rotası (`o2_guides.json`: alın köşesi F1 ×9, şakak F2 ×8, kulak üstü F3 ×9, kulak arkası F4 ×5) + yay/yan kaldırma parametreleri (LF_SIDE 1,6 → 0,55). Yoğun telde ölçülen etki: şakak ailesi ort. 1,16 cm / maks 3,2 cm, kulak arkası 0,69 cm, kulak üstü 0,51 cm (`data/h51a_vs_h49a_family_displacement.txt`). Görünür sonuç: şakak üstünde çapraz-aşağı süpürme ve yan kütlede daha yakın yatış (board 04 main-only profil / 3/4); alın köşesi ve şakak açıklığı küçük ölçüde kapandı, saç çizgisi değişmedi. Topuz büyümedi. |
| Ana çapraz örtüşme (kaçak teller gizliyken) okunuyor mu? | **Kısmen.** Serbest groom gizliyken (board 04 satır 1–2) şakak ailesinin ön kilidi yan kilit üstünden aşağı-geri geçiyor; ama referanstaki gibi iki ayrı aile farklı seviyede ve ayrı yön olarak net okunmuyor. |
| h50a neden kullanılmadı? | İlk kaplama denemesi (`h50a_env_defective.txt`) yan kök yoğunluğunu da değiştirdi; bu kilit kümelemesini değiştirdiğinden `prim:N` kılavuz düzenlemeleri yanlış kilitlere uygulandı: 7.739 tel 3–6 cm sıçramalı, 288 tel yüzden geçiyor (`strand_geometry_check_h50a_h51a.txt`, `tagE_h50a.png`). h51a sıfır sıçrama / sıfır yüz kesişmesi. |
| Ense / kulak arkası / topuz birleşimi? | **Değişmedi (N ile aynı).** nape_field parametreleri korundu; ense omurgası kılavuz düzenlemeleri bu yapılandırmada etkisiz (SPH_NAPE_N=0 → ense kilidi yok). Board 05: A/B/C/D etiket grupları h51a için; main-only ve tam çekimler h49a ile aynı. |
| Yüz kimliği korundu mu? | **Evet.** o6 − n1 farkı yalnız burun bandında (2,67 mm maks; dudak/çene/yanak/göz/kulak/kafatası 0,00 mm). Kaş ve saç mesh'i değiştirmedi; board 01/06 birleşik C aynı kişi. |
| Oyun ışığı? | Test edildi (`gameplay` = yön ışığı + gök; siyah kare değil) fakat tek sert güneş: yüzün yarısı gölgede; sadece "kararmıyor / saç-kaş aşırı parlamıyor" kontrolü. Üretim haritası/ışığı değiştirilmedi. |
| Taze editörde saç neden farklı görünüyor? | Chain, auto-rig OOM'u sonrası taze editörde koşuldu; serbest groom (yüz çerçevesi telleri) taze editörde yazarlık rest şeklinde (aşağı sarkan uzun teller), uzun ömürlü editörde ise oturmuş görünüyordu. S ve C aynı taze editörde çekildi (adil karşılaştırma); fark saç yazarlığından değil, editör sim durumundan. |

## Teknik (board 07)

| Kontrol | Sonuç | Kayıt |
|---|---|---|
| o6 auto-rig (taze editörde, tek başına) | fit ort. 0,017 / p95 0,068 / maks 0,350 mm; 858 morph; DNA `MHC_G11RO_O6_Head` | `prov/g11roNO.json` |
| Uzun ömürlü editörde ilk rig denemesi | **OOM (paging file too small)** 58 GB boş diske rağmen; editör yeniden başlatıldı, rig tekrarlandı | `Saved/Logs/g11rn_reopen.log` |
| Rig 54 + hareket 27 + eğim 7 + dönüş 10 (C) | Temiz: kırpma, kaş yukarı/aşağı (özel kaş bağlı), bakış, çene/ağız, gülümseme, burun deliği; kulak/boyun kesişmesi ve kök kopması yok | `g11rorig_*`, `g11romot_*`, `g11roP_*`, `g11roRL_*` |
| Groom LOD | h51a Main/Loose kalınlık tablosu 1,0/1,25/1,7/1,0 kaydedildi; 24 mesafe çekimi (1,25–25 m); aktif LOD indeksi Python'dan okunamıyor | `G11RO_LOD`, `data/lodprobe_1.json` |
| Yeniden açılış | o6 (858 morph, DNA), h51a groom/MI/kask, `GB_G11RO_*_o6h51a` + özel kaş bağlaması yüklendi; kirli paket yok | `G11RO_REOPEN2` |
| Korunan dosyalar | **89/89 grup aynı** (N/M/L/K/J adayları ve kaynakları) | `data/preservation_check.txt` |
| Disk | DDC 3 günden eski girdiler silindi (53,6 GB); zincir öncesi 58 GB boş | — |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| BURUN UCU–KANAT BÜTÜNLÜĞÜ | KISMEN |
| REFERANS BURUN KARAKTERİ | KISMEN |
| ÖZEL KAŞIN REFERANSA UYGUNLUĞU | KISMEN (konum/dolgunluk/kemer evet; renk ve kuyruk ucu eksik) |
| SAÇIN BAŞI DOĞAL KAPLAMASI | KISMEN (küçük kazanım) |
| ANA ÇAPRAZ ÖRTÜŞME | KISMEN |
| YOĞUN ENSEDEN TOPUZA TOPLANMA | DEĞİŞMEDİ (N ile aynı; bu turda düzenlenmedi) |
| KULAK ARKASI HACİM | DEĞİŞMEDİ (N ile aynı) |
| TOPUZ BİRLEŞİMİ | DEĞİŞMEDİ (N ile aynı) |
| YÜZ KİMLİĞİNİN KORUNUMU | BAŞARILI |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (aktif LOD indeksi TEST EDİLMEDİ; oyun ışığı yalnız kararma kontrolü) |

Önerilen adaylar: NO (o6) ve BO (b4) ayrı ayrı; C (o6 + h51a + b4) birleşik. Saç için h51a küçük bir adım; h49a ile fark board 04'te. **ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**

## Board'lar

`boards/01_WHOLE_HEAD.jpg` referans | başlangıç | yeni bütün baş · `02_NOSE_TIP.jpg` burun ucu (ön / eşleşen 3/4 / profil / alttan, clay + heat) · `03_BROW.jpg` referans / reddedilen M_Fine / özel kaş (b1→b4 yinelemeleri) · `04_MAIN_HAIR_FLOW.jpg` ana akış ve kaplama (serbest groom gizli / açık) · `05_NAPE_EAR_BUN.jpg` ense / kulak arkası / topuz + A–F etiket grupları · `06_SEPARATION.jpg` ayrı adaylar + birleşik + oyun ışığı · `07_TECH_REOPEN.jpg` rig / hareket / LOD / yeniden açılış. Ham kareler `Saved/Codex/CharacterLookdev_20260930/captures/g11ro*` (yayımlanmadı; board'lar kırpılmamış karelerden).
