# GD42 — Göğüs anatomisi ve doğruluk (GD41 D6 vücudu üzerine; klavikula ağırlığı keşfi)

Tarih: 2026-10-12 · Aday: **E6** (`GD42_Body` morph'u, `SKM_GD42_BodyMesh` üzerinde) · Durum: **PARTIAL** (teknik PASS, görsel kabul kullanıcıda)

Kullanıcı isteği: *"Daha fazla anatomi ve doğruluk üzerine çalış, özellikle göğüste."*

## Keşif: GD41'in göğüs alanları hiç çalışmamıştı

- MetaHuman vücudunda **klavikula** deri ağırlığı bütün göğüs ön yüzünü (0.4–0.6) ve üst sırtı (0.2–0.4) sürer. GD39–GD41'in "kol" maskesi klavikulayı da sayıyordu → göğüs ve üst sırtın büyük bölümü "kol" sanılıp **tüm gövde primitiflerinden ve göğüs alanlarından dışlanmıştı**. GD41'deki "daha dolu göğüs" yalnızca göğüs ALTINA (kol ağırlığı < 0.25 olan kaburga bölgesine) itilen dolgunluktu.
- Işın-atımlı göğüs yükseklik haritası (`gd42_breastmap.py`) tabanın gerçek biçimini gösterdi: iki ayrı göğüs değil, **geniş düz bir raf** — en öndeki nokta x≈4 cm'de (sternumun yanı), alt göğüs duvarına göre yalnız 1.7 cm çıkıntı, sternal vadi 0.9 cm; kütle yanlarda (x 12) 4–5 cm kalın, üst kutup apeks kadar dolu.
- Referans (EVE yan silüet, bizim cm): apeks üstünde düz ~45° eğimli üst kutup (+3 cm'de 2.1, +6'da 5.3 cm geri), apeksin 3.8–4 cm altında kıvrım (IMF), kıvrım altı göğüs duvarı apeksten ~7 cm geride.

## Yöntem (E6)

1. **Doğru kol maskesi**: kol = üst kol + ön kol + el (klavikula hariç). Göğüs, üst sırt (skapula dikeni, infraspinatus, teres, trapez) ve pektoral bölge artık GD41 atlasına açık; sırt çizgisi tablosu D6 ile aynı (bel/lumbar değişmedi).
2. **Göğüs biçimlendirme** (mevcut kütle üzerinde, yumuşak çanlar, cm): apeks itmesi +2.5 (eksen 18° yana, 2° yukarı; düz tepeli çan p 2.6 / q 1.0, yarıçaplar iç 6.5 / dış 5.5 / alt 5.0 / üst 6.0), sternal vadi −0.6, üst kutup düzleştirme −0.9 (z 131.5), alt kutup dolgunluğu +0.4, yan kütle geri/içe −0.45 (düz raf yerine yuvarlak ön), aksiller kuyruk +0.2, areola +1.5 mm + meme ucu +2.2 mm (düzleştirmeden sonra). IMF oluğu yok: kıvrım taban mesh'in kendi alt yüzünden geliyor.
3. Reddedilen yol **E1**: "rafı kaldır + açık kubbe ekle" (satır başına elips göğüs duvarı, teardrop kubbe) → düz bir plaka üzerinde koniler, üst kenarda dikiş korumasına çarpan çizgi, 6 ters üçgen. **E2** (yığılmış yerel alanlar: apeks + sarkan alt kutup + IMF oluğu + derin vadi) → topaklı, sarkık, kesikli. E3→E6: tek geniş itme + hafif vadi, sonra yuvarlak ön ve düz tepe.

Göğüs ölçümleri (ışın haritası, sol göğüs, cm): apeks (7.5, 16.6, z 127.8) — LK (3.8, 14.7, 128.8); çıkıntı (kıvrım altı duvara göre) 5.0 — LK 1.7; sternal vadi 3.5 — LK 0.9; üst kutup +3 cm'de 1.6 geri, +6'da 5.1 geri (ref 2.1 / 5.3); yan %50 düşüş x 12.0. Baş-gövde dikişi (z 134–143, |x|<15.3) üst kutubun z 133 üstünü kilitler: üst kutup eğimi apeksi öne almakla elde edildi, klavikula altı bölge değiştirilemez (kafa mesh'i).

## Doğrulama

Blender (mesh): ters üçgen 0, alan oranı 0.61–2.69 (en büyük gerilme alt kutupta), kenar oranı 0.62–2.20, dikiş 0.0 mm (`data/gd42_E6_bodycheck.json`); sırt/ön çizgi tablosu D6 ile aynı (`data/backline_E6.txt`).

UE 5.8 (E6): morph `GD42_Body` GeometryScript ile `SKM_GD42_BodyMesh` (LK vücudundan yeni kopya) LOD0-3'e yazıldı — LOD0 12 554 vertex / en çok 28.5 mm, LOD1 3 143 / 26.4 mm, LOD2 1 178 / 26.8 mm, LOD3 502 / 24.5 mm; taban mesh değişmedi (0.0 cm); ABP `GD42_Body=1` Modify Curve, iskelet eğrisi 32→33 (checkpoint sonrası); kaydedildi, dirty paket yok (`process/chain_E6.txt`). Harness yakalamaları: 20 tam boy + 48 yakın plan (göğüs ön/yan/3-4/alçak 3-4 dahil) + 36 deformasyon (kil + ten, önce/sonra).

Eval montajı `BP_GD42_Character_Body` + `L_GD42_Eval_Body` (giysisiz): ilk montaj işi `data/uecams.json` (GD41'den kopyalanmamıştı) yüzünden BP + 2 MI'yi oluşturup level'den önce durdu; bu üç yarım varlık silinip montaj temiz yeniden koşuldu (6 varlık kaydedildi). BP yakalamaları (`g42bp_body_*`) ile harness piksel karşılaştırması: ön gövde bölgesi ortalama |d| 0.0044, p95 0.0157, >0.05 olan piksel %0.86 → kaydedilmiş BP aynı vücudu gösteriyor. PIE: ilk denemede readback `ObjectInstance is null` istisnası verdi (geçici), yeniden koşuldu: 1 instance, hata yok; Body `SKM_GD42_BodyMesh` LOD0, Face `SKM_GD38_Face_t38` LOD0 (`AS_GD33_Rest_lid60`, lid 0.6), 4 groom bağı görünür (`process/evalchain_E6_run2.txt`, `process/pie_rerun.txt`).

Deformasyon pozları (9 poz, V3 panoları): kil önce/sonra; göz kontrolü.

## Panolar

- `boards/V1_TAM_BOY_CLAY_ONCE_SONRA.jpg` — 5 görünüm kil, üst önce (aynı mesh, `GD42_Body` = 0 → üretim vücudu) / alt GD42.
- `boards/V2K_YAKIN_PLAN_KIL_1/2.jpg` — göğüs ön/yan/3-4/alçak 3-4, bel, kalça, sırt, bacak, omuz.
- `boards/V3_DEFORMASYON_1/2.jpg` — pozlar.
- `boards/B*_blender_*.png` — Blender ışıklı göğüs yakın planları: D6 → E1 (ret) → E3 → E5 → E6; sırt/3-4 D6 vs E6; LK ve E6 göğüs yükseklik haritaları.
- Ten panoları yalnız yerel; üçüncü taraf referans yayınlanmaz.

## Dürüst değerlendirme

- **Teknik: PASS** (bake, ABP eğrisi, LOD0-3, BP/level = harness, PIE).
- **Görsel: PARTIAL / kullanıcı kararı.** Göğüs artık düz raf değil, yuvarlak ve öne çıkan bir kubbe; sternal vadi, alt kıvrım ve meme ucu okunuyor. Sınırlar: üst kutup z 133 üstünde dolu kalır (kafa mesh'i), referansın 45° düz üst kutubu tam elde edilemedi; alt kıvrım tepe ışığında koyu gölge; mesh çözünürlüğü (~1 vertex/cm²) meme ucunu tek-vertex tümsek olarak verir; göğüs hacmi referanstan bir kademe küçük (çıkıntı 5.0 vs ~7 cm).
- GD41 D6'nın diğer bölgeleri (bel, kalça, bacak, kol) aynen; üst sırt alanları artık tam etkili (skapula/trapez biraz daha okunur).
- Sonraki paslar: giysi refit (göğüs çevresi değişti), SHC/RV yeniden tabanlama; isteğe bağlı: göğüs hacmi kademesi (BR_APEX 2.5→3.2) kullanıcı tercihine göre.

## Dosyalar

- UE: `/Game/Sphirus/CharacterLab/GD42_Breast_20261012/Body/{SKM_GD42_BodyMesh, ABP_GD42_Body_PostProcess}`, `.../Assembly/BP_GD42_Character_Body`, `.../Maps/L_GD42_Eval_Body`, `.../Studio`; iskelet eğri metadata'sı (`GD42_Body`) checkpoint sonrası eklendi.
- Araçlar (`tools/`): `gd42_anatomy.py` (B3 göğüs bölümü, env BR_*), `gd42_breastmap.py` (ışın haritası + ölçüler), `gd42_refbreast.py`, `gd42_probe*.py` (ağırlık sondaları), `gd42_backline.py`, `gd42_bodyrender.py` (CROP=chest), diğerleri GD41 ile aynı.
- Veri (`data/`): E1–E6 bodycheck, E6 rapor + env, göğüs ölçümleri (`breast_E6.json`), `backline_E6.txt`, yükseklik haritaları.
- Kaynak kopyası: `SourceAssets/Characters/GD42_Breast_20261012/`.
