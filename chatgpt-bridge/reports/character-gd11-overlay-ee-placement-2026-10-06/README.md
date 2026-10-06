# GD11 tur EE: referans ve model üst üste; yüz yerleşimleri yeniden kuruldu (E1)

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

Kullanıcı isteği: "Hâlâ arası çok boş. Referans ve modeli ön ve yan açıdan üst üste koy ve tekrar suratındaki yerleşimlerini yap."

## Yöntem

**Önden:** model saçsız olarak referans fotoğrafın çözülmüş kamerasından çekildi.
- Burun altı, üst dudak sınırı, ağız çizgisi ve alt dudak sınırı hem referansta hem modelde **aynı görüntü yöntemiyle** bulundu: orta hat sütununda kırmızılık ve gölge (`blender_g11ree_imglm.py`).
- Değerler gözler arası mesafeye bölündü ve göz hizasına göre karşılaştırıldı (`data/imglm_final.txt`).
- Board 01'de camgöbeği çizgiler referans, macenta çizgiler model.

**Yandan:** referans profil fotoğrafının çözülmüş kamerası yok. Modelin profil çekimi alına (kaş arası) ve ağız çizgisine hizalanıp bindirildi (`blender_g11ree_profov.py`, board 02). Kulak hizalaması referansta saç altında kaldığı için kullanılmadı.

## Bulgu

| (göz hizasından, IPD oranı) | Referans | y1 | D1 | **E1** |
|---|---|---|---|---|
| burun altı | 0,758 | 0,754 | 0,687 | **0,749** |
| üst dudak sınırı | 0,907 | 0,951 | 0,957 | **0,901** |
| ağız çizgisi | 1,114 | 1,148 | 1,148 | **1,108** |
| alt dudak sınırı | 1,263 | 1,356 | 1,350 | **1,260** |
| burun–dudak arası (filtrum) | **0,89 cm** | 1,17 cm | 1,60 cm | **0,90 cm** |
| üst dudak kırmızısı | 1,23 cm | 1,17 | 1,14 | **1,24** |
| alt dudak kırmızısı | 0,89 cm | 1,24 | 1,20 | **0,90** |

**Sonuç:** burun tabanının yeri y1'de zaten referansla aynıydı. Boşluğun asıl sebebi ağzın 2–5 mm fazla aşağıda ve alt dudağın uzun olmasıydı. B4/C2b/D1'de burun tabanını kaldırmak boşluğu daha da büyüttü. Önceki turlardaki bu hata, burun altı için kullanılan elle seçilmiş referans noktasının burun deliği gölgesine işaretlenmiş olmasından kaynaklanıyordu.

## E1 = y1 + `data/E1b.json`

| İşlem | Değer |
|---|---|
| Burun tabanı | **y1'deki yerinde** (kaldırma geri alındı) |
| Burun ucu | yalnız uç 3 mm yukarı (burun altı sabit); alt sırt 0,5 mm öne |
| Ağız | dudaklar bütün hacmiyle **2,5 mm yukarı**; filtrum kısaldı |
| Alt dudak | alt sınır ek 1,5 mm yukarı (alt dudak kırmızısı referans boyunda) |
| Burun kökü, yanak, çene | D1 ile aynı: burun kökü daraltma ve yumuşatma; yanak ön kütlesi 1,5 mm geri; çene 3 mm öne, alt kenar 2 mm aşağı |

Ağız genişliği değişmedi: önden referansla aynı. Ağız köşeleri aşağı çekilmedi; tüm ağız yukarı taşındı.

Bölge ölçümü (y1'e göre, `data/heat_E1b_vs_y1.txt`):
- dudak bölgesi en çok 4 mm (ağız taşıma);
- göz kapakları en çok 0,4 mm;
- yanak en çok 3 mm.

## Teknik

| Kontrol | Sonuç |
|---|---|
| e1 auto-rig | taze editör, rig kapısıyla; fit ort. 0,019 / maks 0,352 mm; göz 0,000; 858 morph; DNA bağlı |
| e1 27 rig pozu (board 07) | temiz: ağız açma, konuşma biçimleri, gülümseme, dudak kaldırma, göz kırpma; dişler dudakla birlikte doğru |
| e1 27 hareket karesi (board 08) | temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

- `01_FRONT_LANDMARKS.jpg`: önden hiza çizgileri y1 / D1 / E1.
- `02_PROFILE_OVERLAY.jpg`: profil bindirmesi.
- `03_MOUTH_ZOOM.jpg`: burun–ağız yakın plan.
- `04_34_OVERLAY.jpg`: 3/4 referans kamerası.
- `05_WITH_HAIR.jpg`: saçlı görünüm.
- `06_NOHAIR.jpg`: saçsız görünüm.
- `07_TECH_RIG_e1.jpg`, `08_TECH_MOTION_e1.jpg`: rig pozları ve hareket.

Kaynaklar: `SourceAssets/Characters/GD11_OverlayEE_20261006`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
