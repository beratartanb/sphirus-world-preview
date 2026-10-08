# GD11: yanak ve alt çene yumuşak doku dağılımı (ww5bs9)

Tarih: 2026-10-08. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

| | Yüz | Saç / cilt / iris / kaş |
|---|---|---|
| Önce | ww5bs8 (S8) | h73b / x19a / e3n / M_SlightArch (m3) |
| Sonra | **ww5bs9 (S9)** | aynı |

Eski varlıkların hiçbiri silinmedi ya da değiştirilmedi.

## İstek

Önden:
- dış yanak ve elmacıktan orta yanağa destek;
- göz altının dışı ve üst yanak düzlemi daha yana otursun;
- ağız yanından alt yanağa geçiş oyuk ve dar kalmasın.

3/4 ve profilden:
- yanaktan çeneye geçiş yumuşasın ve hafif dolsun;
- kulak altı, masseter önü ve arka çene bölgesine hafif yumuşak doku dolgunluğu.

Kemik keskinleştirme yok; çökük yanak, keskin masseter, köşeli çene açısı yok; şişkinlik yok.

## Yapılanlar

| Bölge | İşlem |
|---|---|
| Dış yanak / üst yanak düzlemi | Düz, yayvan bir yan genişlik alanı (z 156,4–158 cm, en çok 1,6 mm); kulak birleşiminden önce sönüyor |
| Elmacık → orta yanak | Geniş, yumuşak destek dolgusu |
| Ağız yanı → alt yanak | Yumuşak dolgu ve yalnız dolduran yumuşatma |
| Kulak altı / arka çene | Kulak altından boyun üstüne kadar devam eden yayvan yan dolgunluk. Çene açısının arkasını ve altını doldurur; köşe yuvarlanır. |
| Yanak → çene geçişi | Yalnız dolduran (kesmeyen) yumuşatma, iki bölgede. Hiçbir yer içeri gitmedi. |

**Yarım yüz genişliği** (mm, S8'e göre):

| z (cm) | 150 | 151 | 152 | 153 | 155 | 156 | 157 |
|---|---|---|---|---|---|---|---|
| S9 − S8 | +1,7 | +1,7 | +2,0 | +2,2 | +0,1 | +1,3 | +1,4 |

Göz hizası ve üstü değişmedi.

**Kontroller:**
- Burun ve dudak değişmedi; çene ucu öne ya da aşağı gitmedi.
- Yeni katlanma yok (keskin kıvrım 41, kulak önü 2: önceki gibi).
- Bölge ölçümleri `data/eval_S9_vs_S8.txt` dosyasında. Kulak altı ve arka çene +1,3 mm; bu bölgede kabartı değişmedi, yani yeni kabarık oluşmadı.

## Dürüst değerlendirme

| Hedef | Durum | Not |
|---|---|---|
| Dış yanak ve üst yanak daha yana | **KISMEN-BAŞARILI** | Önden elmacık altı ve dış yanak daha dolu; yüz çizgisi daha yayvan. |
| Ağız yanı → alt yanak oyuk olmasın | **KISMEN** | Daha dolu ve yumuşak; ağız köşesinin dışındaki gölge hâlâ var (kısmen dudak ve ifade şeklinden). |
| Yanak → çene geçişi yumuşak | **BAŞARILI** | 3/4'te çene hattı daha az tanımlı ve keskin; geçiş daha organik. |
| Kulak altı / arka çene dolgunluğu | **BAŞARILI (hafif)** | Profilde çene → boyun geçişi daha dolu ve yumuşak; köşe öne çıkmadı. |
| Genel | **KISMEN-BAŞARILI** | Alt yüz daha geniş, etli ve kadınsı; şişkin değil. Önden alt çene artık daha geniş bir U. Bunu "köşeli" bulursan arka çene genişliği yarıya indirilebilir. |

## Teknik

| Kontrol | Sonuç |
|---|---|
| ww5bs9 | ww5bs8 kopyası + doğrudan fark (2493 köşe, en çok 3,6 mm); normaller ve teğetler yeniden; 858 morph ve DNA korundu |
| Rig pozları ve hareket kareleri | 27 + 27, temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7); korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |
| Disk | C: 15 GB boş (%99) |

## Board'lar

| Dosya | İçerik |
|---|---|
| `00_NOHAIR_ALL_VIEWS.jpg` | saçsız: önce (S8) / sonra (S9) / referans; ön, iki 3/4, iki profil |
| `01_HAIR_ALL_VIEWS.jpg` | aynı açılar, saçlı |
| `02_FOCUS_FRONT.jpg` | önden: dış yanak ve üst yanak düzlemi; ağız yanı → alt yanak (üst = önce, alt = sonra) |
| `03_FOCUS_34_PROFILE.jpg` | 3/4 ve profil: yanak → çene, kulak altı ve arka çene |
| `05_TECH_Rig.jpg`, `05_TECH_Mot.jpg` | rig pozları ve hareket kareleri |

Tarif: `data/S9_soft.json` (+ `blender_g11xx_soften6` yalnız dolgu, iki bölge, kesme 0). Kaynaklar: `SourceAssets/Characters/GD11_SoftFixS9_20261008`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
