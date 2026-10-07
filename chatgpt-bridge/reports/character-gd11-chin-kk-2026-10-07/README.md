# GD11 tur KK: çene boyu referansa göre kısaltıldı, çene ucu köşeleri yumuşatıldı (J5 → K5)

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

## Kullanıcı istekleri

- "J5 iyi gibi ancak çenesi çok fazla uzun, referans üzerinden tekrar çalış."
- "Çenenin belirgin köşe çıkıntılarını biraz yumuşat." Kullanıcının açıklamasına göre bu, uç çenenin köşeleri.

**Taban:** J5 (tur JJ) + k15 + M_SlightArch + e3g + S_Thin + h68e.

## Ölçüm (çözülmüş ön kamera, gözler arası mesafeye oran; `data/imglm.txt`, `data/menton.txt`)

| Göz hizasından | Referans | J5 | **K5** |
|---|---|---|---|
| ağız çizgisi | 1,114 | 1,108 | 1,108 |
| alt dudak sınırı | 1,263 | 1,260 | 1,260 |
| çene ucu (alt nokta) | 1,883 | 1,911 | **1,869** |
| ağızdan çene ucuna | **0,769** | 0,803 | **0,761** |

## K5 = J5 + `data/K5.json`

| İşlem | Değer |
|---|---|
| Çene ucu alt yüzeyi yukarı (çene kısaltma) | 2,5 mm |
| Uç çene köşeleri elipsoid yuvarlama (iki köşe, ön ve alt) | 1,2 / 0,8 mm içe |
| Çene ucu yumuşatma | 3 tur |

Bölge ölçümü J5'e göre (`data/heat_K5_vs_j5.txt`):
- çene en çok 3,5 mm;
- dudak en çok 0,13 mm;
- yanak en çok 1,6 mm (çene kenarına yakın sönüm);
- göz, burun ve kulak 0,00 mm.

Çene hattının genişliği (J5) korundu.

**Elenen denemeler (board 05):**
- K3: kutu alanla köşe yuvarlama; çene kenarında çentik bıraktı.
- K6: daha güçlü; köşede düzlük oluştu.

## Gözlemlerim (karar kullanıcının)

Çene yakın planında (board 01) J5'teki düz tabanlı, iki köşeli çene ucu K5'te yuvarlak. Çene kısaldı. Önden alt yüz J5'in geniş U biçimini koruyor; profil neredeyse aynı.

## Teknik

| Kontrol | Sonuç |
|---|---|
| k5 auto-rig | taze editör, rig kapısıyla; fit ort. 0,021 / maks 0,345 mm; göz 0,000; 858 morph; DNA bağlı |
| k5 27 rig pozu / 27 hareket karesi | temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

- `01_CHIN_COMPARE.jpg`: referans / J5 / K5; ön, çene yakın planı, 3/4 ve profil.
- `02_REF_CAMERA.jpg`: çözülmüş referans kameraları.
- `03_FRONT_BLEND.jpg`: %50 bindirme.
- `04_WITH_HAIR.jpg`: saçlı görünüm.
- `05_CLAY.jpg`: çene ucu kil denemeleri.
- `06_TECH_RIG_k5.jpg`, `07_TECH_MOTION_k5.jpg`: rig pozları ve hareket.

Kaynaklar: `SourceAssets/Characters/GD11_ChinKK_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
