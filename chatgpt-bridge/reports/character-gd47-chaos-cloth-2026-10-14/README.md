# GD47 — Oyun karakterine çalışma zamanı Chaos Cloth (Henley + şort)

Tarih: 2026-10-14 · Genel durum: **PARTIAL** — kumaşlar oyunda simüle ediliyor ve PIE'de doğrulandı. Hareket halindeki sallanma için kanıt yalnızca durağan karelerden ibaret, görsel kabul kullanıcıda · Üretim değişikliği: `BP_Player_MM` (+ alt sınıflar `BP_GR_Player`, `BP_PBI_Player` yeniden derlenip kaydedildi)

Kullanıcı isteği (GD46'dan devam): *"üstünde yerçekimine karşı sallanan bir şey gibi değil"*. GD46 Henley'i idle pozunda statik olarak oturttu. Bu iş, giysilerin hareketle yerçekimi altında sarkıp sallanması için gerçek zamanlı Chaos Cloth getiriyor.

## Sonuç tablosu

| # | Madde | Durum |
|---|---|---|
| 1 | Henley: **bütün giysi** Chaos Cloth (`CA_GD47_Henley_w2`, kesik parça yok) | **PASS (teknik)** · görsel: PARTIAL (kullanıcı kararı) |
| 2 | Şort: lookdev'de kabul edilen `CA_CR_Shorts_m1` oyuna taşındı | **PASS (teknik)** |
| 3 | Pawn: `HenleyCloth` + `ShortsCloth` (Manny altında), skinned Henley/Shorts gizli (geri dönüş için duruyor), lider poz Construction Script'te (MCP) | **PASS** |
| 4 | PIE doğrulama (simülasyon açık, idle/yürüme/koşu, önce/sonra) | **PARTIAL**: durağan karelerde içe geçme görülmedi; hareket sırasındaki sallanma video/seri kareyle kanıtlanamadı |
| — | Performans (kumaş simülasyon maliyeti) | **NOT_TESTED** |

## 1. Henley Chaos Cloth (`/Game/Sphirus/CharacterLab/GD47_ChaosCloth_20261014/Cloth/`)

- **Kaynak:** oyundaki GD46 Henley `SKM_GD46_Henley_f5` (LOD0, 8075 köşe). Kalıp ağında ana kumaş **4 ayrı parça** (ön, arka, iki kol). Dikiş köşeleri üst üste ama kaynaklı değil, kaynaksız simülasyonda paneller birbirinden ayrılırdı. **Kaynak (weld)** 0.01 cm toleransla yapıldı: 8075 → 7831 köşe.
- **MaxDistance ağırlık haritası** (çevrimdışı alan, `tools/gd47_weights.py`; `process/weights_w2_summary.json`):
  - Yaka bandı, plaket (ve iki yan şeridi) ile manşetlerin 1 cm yakını **0 cm** (sabit), oradan 7–8 / 7 / 5 cm'de serbestleşir.
  - Omuz/yoke (z>133) **≤1.5 cm**, ön göğüs (V/plaket) **≤2 cm**, gövde z 120'de **3.5 cm** → etekte **4.5 cm**, kollar **3 cm** (koltuk dikişinde gövde değerine yumuşak geçiş).
  - Trim/düğmeler yalnızca render: Proxy Deformer ile simüle kumaşı izler.
- **Dataflow** (`ue_cr_cloth_build.py` deseni, `tools/build_henley_cloth.py`): StaticMeshImport (sim = ana kumaş bölümü) → TransferSkinWeights(`SKM_GD46_Henley_f5`) → ProxyDeformer → MaxDistance (yüksek 8 cm) → Backstop (0 / 40 cm) → LongRangeAttachment → Damping 0.1 → Collision → SetPhysicsAsset `PHYS_GD47_HenleyCollider_w2` (GD47 klasöründe `PHYS_CR_HenleyCollider` kopyası: pelvis/spine_02 kapsülleri şort bel bandı dış yüzeyine şişirilmiş).
- **Etek rest şekli** z 108→100 arasında normal boyunca 0.7 cm dışarı itildi (1239 köşe), böylece kinematik/backstop hedefi şort bel bandının üstünde kalır.
- **Malzemeler:** g17e MI'larının clothing açık kopyaları (`/GD47_ChaosCloth_20261014/Materials/MI_LK_*_g17e_cloth`, ebeveyn `M_CR_Textile(_B)`). Bölüm malzemeleri build sonrası ayarlandı. Okuma (asset): `Henley / Henley_Trim / Buttons`. PIE'de `ChaosClothComponent.get_material(i)` aynı üçlüyü verdi.
- **w1 → w2:** w1'de (etek 7 cm, göğüs sınırsız) yürürken arka etekten şort bel bandı görünüyordu ve plaket bölgesi gevşekti. w2'de etek 4.5 cm, göğüs ≤2 cm, etek rest'i +0.7 cm.

## 2. Şort

`CA_CR_Shorts_m1` (CORRECTIVE geçişi, lookdev'de kabul) **olduğu gibi** kullanıldı: aynı `SKM_LK_Shorts_g16c` kaynağı, oyundakiyle aynı m1 malzemelerinin `_cloth` kopyaları (shorts / trim / drawstring), PIE'de bölüm malzemeleri doğru.

## 3. Pawn değişikliği (`BP_Player_MM`)

- Önce kontrol noktası: üç Blueprint'in kopyası + sha256 (`process/hashes.txt`; `checkpoint/` altında).
- Manny'nin altına `HenleyCloth` (`CA_GD47_Henley_w2`) ve `ShortsCloth` (`CA_CR_Shorts_m1`) ChaosClothComponent'leri eklendi. `use_attach_parent_bound`, her zaman pose tick açık.
- Skinned `Henley` / `Shorts` **gizlendi** (silinmedi, geri dönüş için).
- **Lider poz:** SCS şablonunda verilen lider poz örneğe taşınmadığı için (GD45 tuzağı) Construction Script'e editör MCP Blueprint araç setiyle eklendi: `… → Shorts.SetLeaderPoseComponent(Manny) → HenleyCloth.SetLeaderPoseComponent(Manny) → ShortsCloth.SetLeaderPoseComponent(Manny)` (`process/mcp_leaderpose_apply.json`). Derleme + kayıt yapıldı. Kaydedilen `.uasset` içinde `CA_GD47_Henley_w2` / `CA_CR_Shorts_m1` geçiyor, kirli paket yok.

## 4. PIE doğrulaması

PIE başlangıcında (`process/pie_v1.json`) `HenleyCloth` ve `ShortsCloth` Manny'ye bağlı, lider = canlı Manny, `is_simulation_enabled = True`, bölüm malzemeleri doğru. `Henley`/`Shorts` gizli. Hata: kumaşla ilgili log satırı yok. PIE'deki Blueprint hataları (EnviroSense el algılama, ayak izi decal'leri) test aracının bileşen yeniden kurulumundan geliyor ve önce (skinned) koşularında da aynen var.

**Panolar** (üst sıra = önce: GD46 skinned Henley; alt sıra = sonra: Chaos Cloth; aynı kamera takvimi):
- `boards/gd47_pie_before_after_idle.png`: idle, 4 kamera açısı
- `boards/gd47_pie_before_after_motion.png`: yürüme (yan / ön-3/4 / arka) ve koşu (yan / ön-3/4)
- `boards/gd47_pie_torso_zoom.png`: gövde yakın plan

**Görülen:**
- Arka etekte, skinned Henley'de yürürken görünen **şort bel bandı taşması (GD46'nın açık kusuru) Chaos Cloth ile kayboldu**.
- Etek ve arka yerçekimiyle düz iniyor, önde etekte yumuşak kıvrımlar var.
- Omuzlarda vatka, göğüste/omuzda içe geçme veya titreme durağan karelerde görülmedi.

**Sınırlar (dürüst):**
- UE Python PIE dünyasına kamera ekleyemiyor. Açılar oyuncu kamerasının control-rotation yörüngesiyle alındı, kamera yumuşatması yüzünden bazı kareler hedef açının bir öncekini gösteriyor (önce/sonra yine aynı takvimle, karşılaştırılabilir).
- Hareket sırasında yüksek çözünürlüklü ekran görüntüsü birkaç kare gecikiyor. Dönüş/duruş anındaki **sallanmayı gösteren seri kareler güvenilir alınamadı**, sallanmanın kendisi bu raporda görüntüyle kanıtlanmış değil. Doğrulanan: kumaş simülasyonu açık ve hareket karelerinde etek şekli değişiyor. Lütfen kendi PIE oturumunuzda koşup durarak bakın.
- V yaka/plaket açıklığı bazı açılardan göğüs derisini gösteriyor. Bu Henley tasarımının kendisi, önce (skinned) karelerde de aynı.
- Kumaş asset'i tek LOD. Performans ölçülmedi (NOT_TESTED).

## Geri alma

`BP_Player_MM`: `HenleyCloth` + `ShortsCloth` bileşenlerini silip `Henley`/`Shorts`'u görünür yapmak (Construction Script'teki iki yeni SetLeaderPose düğümü de silinmeli), **ya da** editör kapalıyken `checkpoint/` içindeki üç `.uasset`'i geri kopyalamak (hash'ler `process/hashes.txt`).

## Değişen / yeni paketler

- Değişen: `BP_Player_MM`, `BP_GR_Player`, `BP_PBI_Player`.
- Yeni (izole GD47 klasörü): `CA_GD47_Henley_w1/w2`, `DF_GD47_Henley_w1/w2`, `SM_GD47_Henley_w1/w2_Sim`, `PHYS_GD47_HenleyCollider_w1/w2`, `MI_LK_{Henley,Henley_Trim,Buttons}_g17e_cloth`.
- Harita kaydedilmedi. Lookdev/CORRECTIVE orijinalleri değiştirilmedi.
