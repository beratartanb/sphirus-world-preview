# GD32 — Saç ile karakterin birleştirilmesi (değerlendirme düzeni)

Tarih: 2026-10-11. İçerik: GD31'in final karakteri, yani GD31 yüzü G31 + h75c saç + özel kaş c4 + kirpik S_Thin + gövde + Henley + şort. Bu turda yüz, saç ve doku değişmedi; yalnızca birleştirildi.

Durum: **PASS (teknik)**. Görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** Yeni varlıkların tümü `/Game/Sphirus/CharacterLab/GD32_IdentityMaster_20261011` altında. Kullanılan GD31/GD15/GD11 varlıklarına yalnızca referans verildi, hiçbiri değiştirilmedi.

## 1. İsteğin

"Saç ile karakteri değerlendirme yapabilmemiz için birleştir." Seçimin: editörde açılabilen birleşik karakter ve saçlı değerlendirme panoları, ikisi birlikte.

## 2. Editörde nasıl açılır

1. Content Browser'da `/Game/Sphirus/CharacterLab/GD32_IdentityMaster_20261011/Maps/L_GD32_Eval_G31` haritasını aç.
2. Hazır kameralardan birini seç. Outliner'da kameraya sağ tıklayıp **Pilot** de (viewport'un görünüm menüsündeki kamera listesinden de seçilebilir):
   - `CAM_REF_front`, `CAM_REF_q3_faceR`, `CAM_REF_q3_faceL`, `CAM_REF_prof_faceL`: referans fotoğrafların çözülmüş kameraları (fov 15).
   - `CAM_HS_*`: baş-omuz dönüşü (ön, iki 3/4, iki profil, üstten ön, arka ve iki arka 3/4; fov 24).
   - `CAM_BODY_front`, `CAM_BODY_front3q`, `CAM_BODY_back`: tam boy.
3. **G** tuşu (Game View) simgeleri gizler. Sınırsız post-process hacminin pozlama ayarları çekimlerle aynı (manuel, EV 0).
4. Işık panolardaki yumuşak stüdyo ışığıyla aynı: `LKQA_key`, `LKQA_fill`, `LKQA_rim` ve gökyüzü ışığı. `LKQA_Grazing` (yan ışık) ve `LKQA_GameplaySun` haritada var ama kapalı (yoğunluk 0); istersen açabilirsin.
5. PIE ile de açılıyor; karakter aynı görünüyor (bkz. testler).

Blueprint: `Assembly/BP_GD32_Character_G31`. Yapısı:

```
Body (SKM_LK_BodyMesh, MI_GD15_Body_s1)
├─ Face (SKM_GD31_Face_g31, ABP_Face, GD31 n3 ten MI'ları, h6 göz)
│  └─ HairMain, HairLoose (h75c), Eyebrows (c4), Eyelashes (S_Thin)   (her biri GD31 bağlamasıyla)
├─ Henley (g17e)
└─ Shorts (g16c)
```

Bütün mesh'ler değerlendirme kalitesi için LOD0'a sabitlendi.

## 3. Panolar

- `B1`: REF ile birleşik karakter, saçlı, stüdyo ışığı, referansın dört kamerası.
- `B2`: yüz yakın plan, saçlı: REF | stüdyo | ön ışık.
- `C1`: baş-omuz dönüşü (9 açı), arkadan ve üstten saç dahil.
- `C2`: tam boy (ön, 3/4, arka).
- `V1`: doğrulama. Aynı kamera ve ışıkta GD31 çekim düzeni ile kayıtlı GD32 Blueprint+harita yan yana; ikisi aynı görünmeli. `data/diff5x_front.png`: aradaki farkın 5 kat büyütülmüş hali.

Bütün görüntüler, kayıtlı haritadaki kayıtlı Blueprint'in UE çekimleri. Boyama veya rötuş yok.

## 4. Teknik testler

| Test | Sonuç |
|---|---|
| Blueprint bileşenleri ve atamaları (mesh, MI, ABP, 4 groom + bağlama) | **PASS** (`data/assembly_check.json`) |
| Temiz editör oturumunda kayıtlı haritayı yükleme: 4 bağlamanın 4'ü yerinde | **PASS** (`data/evalqa_setup.json`) |
| PIE: oyun dünyasında 4 groom bağlı ve görünür, yüzde ABP_Face çalışıyor, LOD0 | **PASS** (`data/pie_check.json`) |
| Kayıtlı haritadan çekim (referans ×2 ışık, baş-omuz ×9, tam boy ×3) | **PASS** (20 çekim) |
| GD31 çekim düzeni ile birebirlik (aynı kamera ve ışık) | **PASS**: yüz bölgesinde ortalama fark 0,012–0,016 (0–1 ölçeğinde, yaklaşık 3–4/255), p99 ≤ 0,09. Fark yalnızca saç teli ve gözenek gürültüsü ile birkaç sanal doku karosu; geometri ya da konum farkı yok (`data/verify_gd31_vs_gd32_pixels.txt`, `V1`). |
| Saç "kask" geri düşmesi | **PASS** (taze editör: 18,5 GB kullanım, 11,2 GB boş sanal bellek; gevşek teller görünüyor) |
| Animasyon, hareket, saç simülasyonu | **NOT_TESTED** (karakter A-pozunda, statik) |
| Üretim değişmedi | **PASS** (Content / Config / Plugins temiz; `data/outside_change_scan.txt`; qa_config dokunulmadı; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

Yolda düzeltilen iki sorun:

- `new_level` haritayı boş kaydetti, ama editör geçici bir dünyada kaldı ve aktörler oraya yerleşti. Kendi oluşturduğum boş haritayı (8,8 KB, aktörsüz) sildim; aktörlerin bulunduğu dünyayı aynı adla kaydettim (601 KB).
- Blueprint şablonunda `set_editor_property` ile verilen bağlamalardan kaynak mesh'i olan üçü (HairMain, HairLoose, Eyelashes) tutmadı. `set_binding_asset` ile yeniden atandı. Temiz oturumda ve PIE'de doğrulandı.

## 5. Sınırlar

- **Statik A-pozu.** Blueprint'te animasyon yok. Kıyafetler gövdenin referans pozunda duruyor; bu poz için doğru. Animasyon eklenirse kıyafetlere leader pose gerekir (çalışma anında atanmalı).
- **Şort.** Çekimlerdeki Chaos kumaş şort (`CA_CR_Shorts_m1`) yerine deri bağlı `SKM_LK_Shorts_g16c` kullanıldı. Yüz ve saç değerlendirmesini etkilemiyor.
- **Oyun karakteri değil.** Hareket kontrolcüsü ve kamera yok; yalnızca bakıp değerlendirmek için.

## 6. Panolardaki gözlemler

Bunlar kabul kararı değil, senin değerlendirmen için not:

- **Saç rengi:** Referans açık bakır-kestane. h75c stüdyo ışığında daha koyu kahverengi okunuyor.
- **Topuz:** Referansta topuz alçak, ensede ve gevşek. h75c'de daha yukarıda ve yuvarlak (`C1`, profil ve arka).
- **Ön teller:** Referansta yüz kenarında kısa, dağınık teller var. h75c'de önden bakınca yanaklar boyunca daha uzun teller iniyor (`B1`, önden).
