# GD44 — Anatomi hatları: silüet çizgi-biçimi analizi + anatomik çizgi primitifleri

Tarih: 2026-10-12 · Aday: **G3** (`GD44_Body` morph'u, `SKM_GD44_BodyMesh` üzerinde; GD43 F5 + hat katmanı) · Durum: **PARTIAL** (teknik PASS, görsel kabul kullanıcıda)

Kullanıcı isteği: *"Daha fazla anatomi ve hatlar üzerinde çalış."*

## Yöntem: hatları ölçerek düzeltmek

`tools/gd44_sag.py` — vücudun dış hatları (ön görünüm: gövde yarı genişliği, bacak dış/iç kenarları; yan görünüm: ön/arka çizgiler, uyluk çapasına göre) bizim z'mizde örneklenir, referans satırları nirengi hizalı (göğüs/göbek/kasık/diz/baldır/bilek) getirilir ve **her nirengi segmentinde çizginin kirişten sarkması** karşılaştırılır. Genişlikten bağımsızdır: GD43'ün antropometrik genişlikleri (kiriş uçları) bizde kalır, yalnız çizginin **eğriliği** (kasın şişkinliği, çukuru) referansla karşılaştırılır. Artık + = referans daha dışa şişkin.

Güvenilir segmentler: bacak dış/iç hatları, böğür (bel→kalça), baldır, kaval, z 70 altı sırt çizgisi. **Kullanılmayanlar**: referansın koltukaltı seviyesindeki gövde genişliği, üst sırt ve bel→kalça sırt çizgisi ile göbek–orta uyluk ön çizgisi **sarkan kol/elle kirlenmiş** (5–8 cm'lik sahte artıklar üretir). İç uyluk artığı duruşa bağlı (referansın bacakları daha bitişik) → yalnız hafif bir iç hat tanımı yapıldı.

Düzeltmeler ("band bell": normali bakış yönüne bakan vertexlere z-çanı yer değiştirme):

| Hat | F5 artığı | İşlem (cm) | G3 artığı |
|---|---|---|---|
| Dış uyluk (kalça→diz) | diz üstü içbükey −1.2; orta uyluk VL eksik | +0.9 @z58, +0.6 @z67 | en çok 0.60 / ort. 0.30 |
| Böğür (bel→kalça) | içbükey −0.7 (ref +0.4 dışbükey) | +0.7 @z100 | en çok 0.68 / ort. 0.37 |
| Ön uyluk (kasık→diz) | kuadriseps tendonu üstünde +2.3 şişkin (ref düz) | −1.2 @z54, −0.6 @z62 | en çok 1.60 / ort. 1.01 (diz üstü hâlâ +1.0 şişkin) |
| Kaval | +0.05 (ref −0.9 hafif içbükey) | −0.3 @z34 | en çok 0.68 / ort. 0.31 |
| İç uyluk | duruşa bağlı | hafif −0.6 @z67 | (hedef değil) |
| Baldır dış/iç | ≤0.8 | — | değişmedi |

Yeni yüzey çizgileri (1.5–3 mm): biseps/triseps yan oluğu, dirsek kıvrımı, diz arkası çukuru + hamstring tendonları, iç uyluk (adduktör/hamstring) çizgisi, tibialis/peroneal çizgisi, deltopektoral oluk (dikiş üstü korumalı), yan göğüs/lat çizgisi.

## Doğrulama

- Antropometrik tablo (GD43 aracı) G3'te değişmedi: 28 ölçüden 18 bantta; göbek 78.3 ve orta uyluk 52.1 bandın üst sınırında, diz 34.9 alt sınırda (−0 %), göğüs +3 %, kalça +3 %, meme ucu arası −4 %, iskelet dirsek sapması aynı (`data/anthro_G3.txt`).
- Blender (mesh): ters üçgen 0, dikiş 0.0 mm (`data/gd44_G3_bodycheck.json`); hat sarkma tablosu `data/sag_G3.txt`, grafik `boards/B0_sag_G3.png`.
- UE 5.8 (G3): morph `GD44_Body` GeometryScript ile `SKM_GD44_BodyMesh` (LK vücudundan yeni kopya) LOD0-3'e yazıldı — LOD0 14 807 vertex / en çok 27.0 mm, LOD1 3 704 / 27.0 mm, LOD2 1 337 / 23.6 mm, LOD3 565 / 24.2 mm; taban mesh değişmedi (0.0 cm); ABP `GD44_Body=1` Modify Curve, iskelet eğrisi checkpoint sonrası eklendi; kaydedildi, dirty paket yok (`process/chain_G3.txt`). Harness yakalamaları: 20 tam boy + 48 yakın plan + 36 deformasyon (kil + ten, önce/sonra).
- Eval montajı `BP_GD44_Character_Body` + `L_GD44_Eval_Body` (giysisiz): montaj temiz koştu (6 varlık); BP yakalamaları (`g44bp_body_*`) ile harness piksel karşılaştırması: ön gövde bölgesi ortalama |d| 0.0043, p95 0.0157, >0.05 olan piksel %0.78 → kaydedilmiş BP aynı vücudu gösteriyor. PIE: 1 instance, hata yok; Body `SKM_GD44_BodyMesh` LOD0, Face `SKM_GD38_Face_t38` LOD0, 4 groom bağı görünür (`process/evalchain_G3.txt`).

## Panolar

- `boards/V1_TAM_BOY_CLAY_ONCE_SONRA.jpg`, `V2K_*`, `V3_*` — UE kil önce/sonra (önce = üretim vücudu).
- `boards/B*_blender_*.png` — F5 vs G3 bacak / gövde / tam boy; LK→F5→G3 ışıklı.
- Ten panoları yalnız yerel; üçüncü taraf referans yayınlanmaz.

## Dürüst değerlendirme

- **Teknik: PASS.** **Görsel: PARTIAL / kullanıcı kararı.** Hatlar ölçülebilir segmentlerde referansa yaklaştı; yüzey çizgileri 1.5–3 mm ile "okunur ama abartısız" tutuldu; tepe ışığında UE kil panolarında diz arkası, dirsek, yan kol oluğu ve böğür okunur, ten panolarında daha yumuşak.
- Sınırlar: referansın gövde/sırt hatları kirli olduğundan üst gövde hat karşılaştırması yapılamadı (görsel yargı); kalan dış uyluk / ön uyluk artıkları ≤ ~1.5 cm; prosedürel.
- Sonraki: giysi refit, SHC/RV yeniden tabanlama; temiz (kolsuz) referans silüeti bulunursa üst gövde hatları da ölçülebilir.

## Dosyalar

- UE: `/Game/Sphirus/CharacterLab/GD44_Lines_20261012/Body/{SKM_GD44_BodyMesh, ABP_GD44_Body_PostProcess}`, `.../Assembly/BP_GD44_Character_Body`, `.../Maps/L_GD44_Eval_Body`, `.../Studio`.
- Araçlar (`tools/`): `gd44_sag.py`, `gd44_anatomy.py` (A/S/atlas+çizgiler/B3/C/L), `gd44_anthro.py`, diğerleri GD43 ile aynı.
- Veri (`data/`): `sag_{F5,G1,G2,G3}.json`, `anthro_G3.json`, G1–G3 bodycheck, G3 rapor + env.
- Kaynak kopyası: `SourceAssets/Characters/GD44_Lines_20261012/`.
