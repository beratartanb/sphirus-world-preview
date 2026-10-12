# GD43 — Antropometrik doğrulama: vücut gerçek bir insana ne kadar yakın? (ölçüm → düzeltme → yeniden ölçüm)

Tarih: 2026-10-12 · Aday: **F5** (`GD43_Body` morph'u, `SKM_GD43_BodyMesh` üzerinde; GD42 E6 + GD41 atlası üzerine düzeltme katmanı) · Durum: **PARTIAL** (teknik PASS, görsel kabul kullanıcıda)

Kullanıcı sorusu: *"Şu anda yapmış olduğun vücut bir insan vücuduna ne kadar yakın ve anatomisi ne kadar doğru? Tekrar anatomi üzerinde çalış ve doğrulama yaparak ilerle."*

## Kısa cevap

- **Oranlar (iskelet)**: boy 173.3 cm; kasık 0.463 H, diz 0.278 H, akromion 0.805 H, uyluk/bacak alt eklem uzunlukları norm bandında. **Tek belirgin iskelet sapması**: üst kol eklem-eklem 25.0 cm (norm 27.7–30.8) ve ön kol 27.8 (norm 23.9–27.0) → MetaHuman dirseği ~3 cm yukarıda duruyor; iskelet değiştirilmediği için **raporlandı, düzeltilmedi**.
- **Yumuşak doku (GD42 E6'da ölçülen → GD43 F5)**: bel kesiti genişliği kadar derindi (oran 1.00; gerçek bel 1.2–1.4) → 1.27; üst kol çevresi +%10 → norm; el bileği −%11 → norm; meme ucu arası 14.9 cm (norm 18–21.5) → 17.3; kalça çevresi +%6 → +%3; diz −%2 → norm; omuz genişliği tavanda → tavanın altında.
- **Kalan sapmalar (bilinçli / küçük)**: göğüs çevresi +%3 (referans dolgun; isteğe bağlı küçültme), kalça +%3 ve uyluk +%0–1 (kaslı kalça/bacak; referans yönü), meme ucu arası −%4.
- Sonuç: 28 ölçüden 18'i norm bandında, 7'si bandın ≤%4 dışında, 3'ü iskelet kaynaklı. Siluet ve çevreler artık zayıf-atletik 173 cm bir kadına **makul ölçüde** yakın; kas/yağ biçimleri prosedürel (artist sculpt değil), ince geçişler hâlâ "CG" okunabilir.

## Yöntem

`tools/gd43_anthro.py`: bind iskeletinden eklem yükseklikleri ve segment uzunlukları; gövde/bacak için yatay, kollar için kemik eksenine dik gerçek düzlem kesitleri (kenar/düzlem kesişimi) → **dışbükey zarf çevresi** (mezura gibi; sternal vadi ve gluteal yarığı köprüler); en dar bel / en geniş kalça / en geniş baldır / en dar bilek aramaları; meme ucu arası; akromion seviyesi omuz genişliği. Norm bantları: ANSUR-II kadın ortalamaları boya ölçeklenmiş + zayıf/atletik düzeltme — **yaklaşık plausibilite bantları**, milimetrik hedef değil.

Ölçüm tuzakları (araç bunlara göre düzeltildi): A-pozu kolları z 128–143'te her yatay "en geniş" ölçümü kirletir (yalnız akromion bandı kullanıldı); kasık altındaki yatay kesitler iki bacağı tek sahte halka yapar (kalça araması kasık + 5 cm üstünden başlar); referans yan silüetinde sarkan el belin önündedir (GD40'ın bel derinliği hedefi buradan kirlenmişti); el bileği çevresi stiloid seviyesinde ölçülür.

## Ölçüm tablosu (cm; LK = üretim vücudu, GD42_E6 = önceki aday, GD43_F5 = bu pas)

| ölçü | LK | GD42_E6 | GD43_F5 | norm (cm) | durum (GD43_F5) |
|---|---|---|---|---|---|
| göğüs çevresi (meme ucu seviyesi) | 88.3 | 94.5 | 94.9 | 86.0–92.0 | 3% yüksek |
| göğüs altı çevresi | 74.0 | 76.0 | 76.1 | 73.0–78.0 | OK |
| bel çevresi (en dar) | 70.9 | 72.9 | 73.0 | 66.0–73.0 | 0% yüksek |
| göbek çevresi | 77.8 | 76.2 | 77.6 | 70.0–78.0 | OK |
| kalça çevresi (en geniş) | 95.9 | 104.9 | 101.9 | 93.0–99.0 | 3% yüksek |
| üst uyluk çevresi | 53.1 | 59.3 | 59.1 | 54.0–59.0 | 0% yüksek |
| orta uyluk çevresi | 46.2 | 52.4 | 52.4 | 47.0–52.0 | 1% yüksek |
| diz çevresi | 34.4 | 34.3 | 35.4 | 35.0–38.5 | OK |
| baldır çevresi | 34.1 | 36.4 | 36.4 | 34.0–37.5 | OK |
| bilek çevresi (ayak) | 20.6 | 20.7 | 20.7 | 20.5–23.0 | OK |
| üst kol çevresi | 29.2 | 31.4 | 28.4 | 25.5–28.5 | OK |
| ön kol çevresi | 22.2 | 23.5 | 23.5 | 22.5–25.0 | OK |
| el bileği çevresi | 13.4 | 13.4 | 14.8 | 14.8–16.2 | OK |
| omuz genişliği (akromion seviyesi) | 43.8 | 45.5 | 45.1 | 40.0–45.0 | 0% yüksek |
| meme ucu arası | 7.1 | 14.9 | 17.3 | 18.0–21.5 | 4% düşük |
| bel genişliği | 25.0 | 22.3 | 24.9 | 23.5–26.5 | OK |
| bel derinliği | 19.2 | 22.3 | 19.7 | 18.0–21.0 | OK |
| bel genişlik/derinlik | 1.30 | 1.00 | 1.27 | 1.2–1.4 | OK |
| kalça genişliği | 35.0 | 37.7 | 35.8 | 33.0–36.5 | OK |
| kalça derinliği | 23.8 | 25.9 | 25.3 | 22.0–26.0 | OK |
| kalça genişlik/derinlik | 1.47 | 1.45 | 1.41 | 1.3–1.6 | OK |
| kasık yüksekliği | 80.3 | 80.3 | 80.3 | 79.7–84.0 | OK |
| diz eklemi yüksekliği | 48.1 | 48.1 | 48.1 | 46.8–51.1 | OK |
| akromion yüksekliği (tahmin) | 139.5 | 139.5 | 139.5 | 138.6–143.8 | OK |
| üst kol (eklem-eklem) | 25.0 | 25.0 | 25.0 | 27.7–30.8 | 10% düşük |
| ön kol (eklem-eklem) | 27.8 | 27.8 | 27.8 | 23.9–27.0 | 3% yüksek |
| uyluk (eklem-eklem) | 42.3 | 42.3 | 42.3 | 40.7–45.1 | OK |
| bacak alt (eklem-eklem) | 39.8 | 39.8 | 39.8 | 39.9–44.2 | 0% düşük |

GD43_F5: 18 / 28 ölçü norm bandında (bantlar yaklaşık; ANSUR-II kadın ortalamaları boya ölçeklenmiş + atletik/zayıf düzeltme).

## Düzeltme katmanı (F5, `gd43_anatomy.py` C bölümü)

| Bölge | Ölçüm (E6) | İşlem | Sonuç (F5) |
|---|---|---|---|
| Bel | 22.3 × 22.3 cm, oran 1.00 | genişlik ×1.12, derinlik ×0.88 (kesit merkezi etrafında, z 103–119) | 24.9 × 19.7, oran 1.27; lumbar sırt çizgisi LK'ye ±0.5 cm |
| Kalça | çevre 104.9, genişlik 37.7 | trokanter/TFL üstü yan doku 1.8 cm içe + gluteal apeks 0.8 öne | 101.9 / 35.8 |
| Üst kol | çevre 31.4 | humerus ekseni etrafında radyal ×0.91 (yalnız kolun kendi yarıçapı içinde) | 28.4 |
| El bileği | 13.4 | stiloid bandında radyal ×1.14 (el koruması bilek ekleminin 2.5 cm ötesinden başlar) | 14.8 (bandın alt sınırı) |
| Diz | 34.3 | diz eklemi etrafında ×1.035 | 35.4 |
| Göğüs | meme ucu arası 14.9 | apeks alanı merkezi x 10.5, eksen 22° yana | 17.3 |
| Omuz | 45.5 (tavan 45) | deltoid yan başlığı 10 → 7 mm | 45.1 |

Reddedilen ara adımlar: F6 (göğüs çanı yan yarıçapı 6.0: yan gerilme artmadı/azalmadı), F7 (normal-yönlü itme kapısı: 15 ters üçgen) → F5 kaldı. Yan göğüs–koltukaltı bölgesinde 3.5× alan gerilmeli birkaç üçgen kalıyor (ters üçgen yok).

## Doğrulama

Blender (mesh): ters üçgen 0, alan oranı 0.63–3.53, kenar oranı 0.64–2.77, dikiş 0.0 mm (`data/gd43_F5_bodycheck.json`); sırt/ön çizgi tablosu (`data/backline_F3.txt`, F5 ile aynı blok-out).

UE 5.8 (F5): morph `GD43_Body` GeometryScript ile `SKM_GD43_BodyMesh` (LK vücudundan yeni kopya) LOD0-3'e yazıldı — LOD0 14 757 vertex / en çok 27.0 mm, LOD1 3 698 / 27.0 mm, LOD2 1 336 / 23.6 mm, LOD3 565 / 24.2 mm; taban mesh değişmedi (0.0 cm); ABP `GD43_Body=1` Modify Curve, iskelet eğrisi checkpoint sonrası eklendi; kaydedildi, dirty paket yok (`process/chain_F5.txt`). Harness yakalamaları: 20 tam boy + 48 yakın plan + 36 deformasyon (kil + ten, önce/sonra).

Eval montajı `BP_GD43_Character_Body` + `L_GD43_Eval_Body` (giysisiz): montaj temiz koştu (6 varlık; `data/uecams.json` bu kez baştan kopyalandı); BP yakalamaları (`g43bp_body_*`) ile harness piksel karşılaştırması: ön gövde bölgesi ortalama |d| 0.0021, p95 0.0118, >0.05 olan piksel %0.69 → kaydedilmiş BP aynı vücudu gösteriyor. PIE: 1 instance, hata yok; Body `SKM_GD43_BodyMesh` LOD0, Face `SKM_GD38_Face_t38` LOD0, 4 groom bağı görünür (`process/evalchain_F5.txt`).

## Panolar

- `boards/V1_TAM_BOY_CLAY_ONCE_SONRA.jpg`, `V2K_*`, `V3_*` — UE kil önce/sonra (önce = aynı mesh, morph 0 = üretim vücudu).
- `boards/B1..B4_blender_*.png` — LK → GD42 E6 → GD43 F5 ışıklı; göğüs ve tam boy E6 vs F5.
- Ten panoları yalnız yerel; üçüncü taraf referans yayınlanmaz.

## Dürüst değerlendirme

- **Teknik: PASS.** **Anatomik doğruluk: ölçülebilir olanlar büyük ölçüde norm bandında (bkz. tablo); görsel: PARTIAL / kullanıcı kararı.**
- Doğru olmayan / yapılamayan: MetaHuman dirsek konumu (iskelet), klavikula altı üst göğüs (kafa mesh'i), prosedürel kas geçişleri, meme ucu tek vertex, yan göğüs gerilmesi.
- Sonraki: giysi refit (GD41–43 çevreleri değiştirdi), SHC/RV yeniden tabanlama, gerekirse artist sculpt geçişi; bu ölçüm aracı her vücut pasında tekrar koşulmalı.

## Dosyalar

- UE: `/Game/Sphirus/CharacterLab/GD43_Anthro_20261012/Body/{SKM_GD43_BodyMesh, ABP_GD43_Body_PostProcess}`, `.../Assembly/BP_GD43_Character_Body`, `.../Maps/L_GD43_Eval_Body`, `.../Studio`; iskelet eğri metadata'sı (`GD43_Body`) checkpoint sonrası eklendi.
- Araçlar (`tools/`): `gd43_anthro.py`, `gd43_anthro_table.py`, `gd43_anatomy.py` (A/S/atlas/B3 göğüs/C düzeltme), diğerleri GD42 ile aynı.
- Veri (`data/`): `anthro_table.md`, `anthro_{LK,E6,F1,F2,F5}.json`, F1–F7 bodycheck, F5 rapor + env, `backline_F3.txt`.
- Kaynak kopyası: `SourceAssets/Characters/GD43_Anthro_20261012/`.
