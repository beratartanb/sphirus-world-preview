# GD11 tur VV: referans kontur ölçümü, yan genişletme geri, alt yüz kontur fiti (uu31c → vv2)

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

## Kullanıcı sorusu ve istek

**Soru:** "Karakteri tekrar referansla üst üste eşleştirip kasları, etleri ve yüz şekli formunu ayarladın, onayladın mı?"

**Cevap: hayır.** uu31c'yi teslim etmeden önce referans konturlarıyla ölçüp onaylamamıştım. Ölçüm bu turda yapıldı.

**Ölçüm sonucu (+ = bizimki dışarıda):**

| Bölge | ss4 | uu31c |
|---|---|---|
| Ön, orta yanak | +1,1 / +2,7 mm | +1,7 / +3,1 mm |
| 3/4, burun yanı yanak | +5,1 mm | +5,4 mm |
| 3/4, ağız-çene uzak kontur | +7–8 mm | +7–8 mm |

Bu ölçüme göre:
- Silüet referanstan ince değil, biraz geniş.
- uu31c'deki yan genişletme farkı büyütmüştü.
- "Kemikli ve kaslı" görüntü dış hattan değil, yüzeydeki gölgelerden geliyor.

Kullanıcı: "Devam et." Plan: genişletmeyi geri al, taşan alt yüzü içeri çek.

## Yapılan

1. **VV0:** UU31 eksi yan genişletme.
2. **vv2:** çok açılı kontur fiti (90 adım, yalnız alt yüz, en çok 1,4 mm, simetrik, yumuşatılmış).
3. Rig sonrası geri yazma uu11 kopyasına yapıldı: kalan fark alçak geçirilmiş, normaller ve teğetler yeniden hesaplandı. 858 morph ve DNA korundu.

Ek bir deneme (VV3: ağız yanı ve alt yanak 3 mm içeri) aynı sonucu verdi; kullanılmadı.

## Ölçüm: önce / sonra (referans konturlarına, cm)

| Kontur | uu31c | vv2 |
|---|---|---|
| Ön, orta yanak (sol / sağ) | +0,17 / +0,31 | +0,10 / +0,25 |
| Ön, alt yanak | +0,10 / +0,20 | +0,01 / +0,13 |
| 3/4, burun yanı yanak | +0,54 | +0,50 |
| 3/4, ağız-çene uzak kontur | +0,82 / +0,72 | +0,72 / +0,63 |
| 3/4 toplam (RMS) | 0,486 | 0,427 |

## Dürüst değerlendirme

- **Ön kontur:** yanak referansa yaklaştı; alt yanakta fark 0–1,3 mm.
- **3/4 uzak kontur:** yaklaşık 1 mm azaldı ama hâlâ 6–7 mm dışarıda. Fit en fazla 1,4 mm hareket ettiriyor; daha fazlası yüzün altını bozuyordu.
- **Kalan farkın nedeni:**
  - Bu kontur ağız köşesinin hemen yanında. Fark, büyük olasılıkla referanstaki gerginlik ifadesinden (dudaklar bastırılmış, ağız köşesi içeri) ve ağız ile yanak arasındaki yumuşak dokudan geliyor.
  - Dinlenik ifadeyle 3/4 çekim karşılaştırması bu turda yapılmadı; bu yorum o yüzden doğrulanmadı.
  - Bunu kemik düzeyinde 6 mm daraltmak, önceki turlarda reddedilen "sivri ve uzun yüze" geri götürür.
- **Görsel fark:** vv2 ile uu31c arasındaki fark küçük. Yan genişlik geri alındı, alt yüz çok az daraldı.

## Teknik

| Kontrol | Sonuç |
|---|---|
| vv2 | uu11 kopyası; alçak geçirilmiş kalan fark (en çok 1,63 mm); normaller ve teğetler yeniden; 858 morph; DNA |
| Rig pozları ve hareket kareleri | 27 + 27, temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7); korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |
| Not | Editör yeniden başlatıldıktan sonra ilk saçlı çekimler, malzeme derlemesi bitmeden alındı (mor/siyah). Derleme bitince yeniden çekildi; board'lar doğru çekimlerden. |

**VideoCaptures:** `Saved/VideoCaptures` (460 oyun içi QA videosu, 14–22 Eylül, ~46 GB) kullanıcının onayıyla Geri Dönüşüm Kutusu'na taşındı. Bu videoları yalnız QA ve kanıt betikleri (`export_evidence.py`, `qa_*`) kullanıyordu. Disk 2,2 GB'dan 48 GB'a çıktı.

## Board'lar

| Dosya | İçerik |
|---|---|
| `01_UU31C_VS_VV2.jpg` | saçsız ön ve 3/4, saçlı, dinlenik ifade |
| `02_REF_CAMERA.jpg` | referans kameraları, %50 bindirme |
| `03_TECH_Rig_vv2.jpg`, `03_TECH_Mot_vv2.jpg` | rig pozları ve hareket kareleri |

Kaynaklar: `SourceAssets/Characters/GD11_ContourVV_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
