# GD11 tur Z: seçilen tekli değişikliklerin birleşimi (Y1 + Y2 + Y3) ve kaş başına çok küçük dokunuş

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Önceki adaylar değiştirilmedi.

Kullanıcı tur Y'den 1, 2 ve 3'ü seçti. Ayrıca kaşın alın ortasına bakan iç ucunun referanstaki gibi biraz kalınlaştırılmasını istedi. İlk deneme (z2) için "kötü oldu, önceki kaşa çok çok küçük müdahale yapalım" dedi. Son aday bu çok küçük dokunuşla (z3) kuruldu.

## Aday

| Parça | Önce (taban, tur W) | Sonra (tur Z) |
|---|---|---|
| Yüz / DNA | `SKM_G11RR_Face_w5` | **`SKM_G11RR_Face_y1` / `MHC_G11RR_Y1_Head`** (Y1: üst kapak örtüsü yaklaşık %70 azaltıldı, yalnız kapak bölgesi) |
| Ten | gqk13 | **gqk15** (Y2: k13 tonu, daha temiz göz çevresi, daha az kırmızılık) |
| Kaş | M_SlightArch | **M_Natural** (Y3) + **kaş başı eki `GD11_FaceR_20261006/Grooms/GR_G11RZ_BrowHead_z3`** (`GB_G11RR_BrowHead_z3_y1`) |
| İris / kirpik / saç | e3g / S_Thin / h68e | aynı |

Önce (`prov/g11rzP0.json`) ve sonra (`prov/g11rzP2.json`) aynı editör oturumunda, aynı ışıkla ve time=0 ile çekildi.

## Kaş başı (board 03)

Kütüphane kaşına dokunulmadı. Yalnız iç uca ayrı, küçük bir prosedürel groom eklendi:
- **Oluşturucu:** `blender_g11rz_browhead.py`, tur O kaş oluşturucusunun kopyası. Kaş bandının yalnız iç %22'si üretiliyor ve dışa doğru yoğunluk sönüyor. Kökler önden düz ışınla yerleşiyor; en yakın nokta izdüşümü kökleri burun köküne kaydırıyordu.
- **Malzeme:** `MI_G11RZ_BrowHead_a`, kütüphane MI_Hair'in çocuğu; melanin 0,6, kırmızılık 0,25.
- **Tel kalınlığı:** M_Natural'ın 0,8 katı.

| Deneme | Tel | Sonuç |
|---|---|---|
| z1 | 448 | reddedildi: kütüphane malzemesinin varsayılan rengi çok koyu, ayrı siyah bir tutam gibi |
| z2 | 239 | kullanıcı: "kötü oldu" |
| **z3** | **81 (taraf başına ~40)** | seçildi: kaşın kendi başlangıç alanında, kaşla aynı renk, boy ve yönde; iç ucu yalnızca biraz daha dolu |

Kaş ve ek, kaş kaldırma, indirme, çatma, gülümseme ve uç ifadede yüzle birlikte hareket ediyor (board 04).

## Teknik

| Kontrol | Sonuç |
|---|---|
| y1 auto-rig (tur Y) | fit ort. 0,018 / maks 0,352 mm; 858 morph; DNA bağlı |
| 27 rig pozu (board 05) / 27 hareket karesi (board 06) | temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ (kaş başı ekinde LOD ayarı yapılmadı) |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| Y1 + Y2 + Y3 birleşimi | BAŞARILI (seçilen üç değişiklik bir arada, kimlik korundu) |
| KAŞ BAŞI DOKUNUŞU | KULLANICI KARARI BEKLİYOR (z3 çok hafif) |
| KİMLİK KORUNUMU | BAŞARILI |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (LOD TEST EDİLMEDİ) |

## Board'lar

- `01_BEFORE_AFTER_FACE.jpg`: önce/sonra ve referans.
- `02_FINAL_VIEWS.jpg`: beş açı.
- `03_BROW_HEAD.jpg`: kaş başı denemeleri M_Natural, z3, z2, z1.
- `04_BROW_IN_EXPRESSIONS.jpg`: kaş ifadelerde.
- `05_TECH_RIG.jpg`: 27 rig pozu.
- `06_TECH_MOTION.jpg`: 27 hareket karesi.

Kaynaklar: `SourceAssets/Characters/GD11_CombineZ_20261006`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
