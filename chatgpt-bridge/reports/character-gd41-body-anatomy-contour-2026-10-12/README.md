# GD41 — Vücut anatomisi: gerçekçi kadın formu (prosedürel kas/yağ atlası + göğüs geçişi + omuz)

Tarih: 2026-10-12 · Aday: **D6** (`GD41_Body` morph'u, `SKM_GD41_BodyMesh` üzerinde) · Durum: **PARTIAL** (teknik PASS, görsel kabul kullanıcıda)

Kullanıcı isteği: *"Vücut anatomisi üzerinde çok daha fazla çalış, gerçekçi bir kadın formundan ve referanslardan çok uzaktayız."*
Önceki pas (GD40) silueti referansa oturtmuştu (bel/kalça/uyluk/baldır kesit genişlikleri ≈ referans) ama yüzey formu
"yumuşak CG tüp" okunuyordu. GD41 aynı siluet üzerine **okunabilir anatomi** koyar: kas hacimleri ve sınırları, kemik
nirengileri, kadın yağ dokusu, göğüs biçimi/geçişi ve omuz (deltoid) başlığı.

Üretim karakterine dokunulmadı. GD38 yüz (`SKM_GD38_Face_t38`) + GD38 saç/kaş/kirpik bağları aynen; vücut = LK vücut +
her zaman açık `GD41_Body` eğrisi (ABP post-process Modify Curve). İskelet/eklemler değişmedi; giysi yok (giysiler sonraki pasta
yeni vücuda yeniden oturtulacak).

## Ne değişti (D6, bind uzayı cm)

| Bölge | Yapılan | Tepe |
|---|---|---|
| Blok | GD40 C8 kontur blok-out'u aynen (bel 25.0→22.2, göbek 28.6→25.7, uyluk derinliği 16.1→19.0, diz 10.2→9.6) + **derinlik pivotu**: pelviste sırt sabit (derinlik değişimi karna: alt karın düzleşir), belden yukarı kesit merkezi; pivot z 94→108 arasında rampalı | 20 mm |
| Kesit biçimi | gövde kesiti elips → yuvarlatılmış kutu (SN 2.5, SS 0.9; düz karın duvarı, düz oblik düzlemler) | 8.9 mm |
| Gövde ön | alt kaburga kafesi + kostal kenar + subkostal oluk; rektus blokları (3.5/3.5/2.8) + tendinöz kesişmeler + linea alba + semilunar; dış oblik + bel çentiği (flank tuck) + inguinal çizgi; serratus; pektoral taban; alt karın düzleştirme −7 | 7 mm |
| Pelvis | iliak krest sırtı **yalnız ön+yan** (arka sırt D5'te kaldırıldı), ASIS yumuşak, PSIS çukurları −1.5, sakral üçgen −1.5, pubik tümsek | 2.5 mm |
| Sırt | lumbar erektör (z 107, +4.0) + torasik erektör; omurga oluğu −3.5; latissimus kanadı; skapula dikeni + infraspinatus + teres + medial kenar; orta/alt trapez | 5 mm |
| Kalça | gluteus maximus +11 (alçak, dolu) + alt dolgunluk + infragluteal kıvrım −5.5; gluteus medius; trokanter çukuru −5; TFL +5 + oluk | 11 mm |
| Bacak | rektus femoris +6, vastus lateralis +8, VMO +8.5, sartorius oluğu (geniş/sığ), adduktör kütlesi (z aşağı, kasık dışlamalı); biseps femoris/semitendinosus +7 + oluk; IT bandı oluğu; patella, peripatellar çukurlar (geniş/sığ), tibial tüberkül, tibia ön kenarı; gastroknemius 9/7 + oluk; soleus; Aşil inceltme; tibialis ant.; peroneallar; malleoller | 9 mm |
| Kol | **deltoid başlığı +10 / ön +6 / arka +6** (kafa-gövde dikiş bandı z-koruması yalnız |x|<16.5 cm'e daraltıldı; D1-D2'de omuz tamamen korumaya takılıyordu), insersiyon oluğu, biseps 5.5, triseps 6.5, brakialis, ön kol ekstansör/fleksör | 10 mm |
| Göğüs | üst kutup −3.5 (eğimli düzlem), alt kutup +5.5 (sarkan dolgunluk), apeks aşağı/yana, aksiller kuyruk +4.5 (yan duvar göğüs kafesine karışır), hafif hacim +4; **çukur doldurma**: taban göğsü göğüs duvarına keskin bir kesikle buluşuyordu (Laplace içbükeyliği 1.9 mm) → yalnız içbükey köşeleri normal boyunca dışarı iten 12 iterasyon (teğetsel büzülme yok), sonra hafif IMF yumuşatma | 14 mm |
| Yağ/deri | yan uyluk dolgunluğu +4, alt karın kavisi, diz yastığı | 4 mm |
| Koruma | kafa-gövde kaynak çiftleri (92) ±1.5 cm, eller, ayaklar, gluteal yarık (|x|<1.2 kalça alanlarında); 1 Laplace; LOD1-3 barisentrik aktarım | — |

Toplam: 80 primitif, 12 079 vertex hareketli, en çok 27.9 mm (blok-out), p99 18.7 mm, dikiş çiftleri 0.0 mm.

## Aday merdiveni

- **D1** ilk atlas — ASIS yumru, krest "kemer", adduktör kasığı ezdi (alan oranı 0.157).
- **D2** nirengiler yumuşatıldı, derinlik pivotu, adduktör aşağı → kasık temiz; ama IMF 0.164 (Laplace fazla) ve omuz yok.
- **D3** genlikler ~1.3×, deltoid z-korumasından kurtarıldı, göğüs doldurma + hacim → alan oranı 0.35.
- **D4** diz iç çukurları (sartorius ucu + VMO + peripatellar üst üste "göçük") genişletildi/sığlaştırıldı, aksiller kuyruk büyütüldü → **UE'ye alındı**; UE kil arka görünümde belde yatay "kemer bandı" çıktı (arka krest sırtı + erektör tepesi + PSIS çukurları, tepe ışığı altında).
- **D5** arka krest kaldırıldı, PSIS/sakral yarıya, lumbar erektör yukarı ve hafif → UE'de bant **hâlâ** vardı (kil arka yakın plan).
- **D6** sebep bulundu: D2–D5'in derinlik pivotu (belde ön sabit) bütün lumbar sırt çizgisini z 102–108 arasında 2.5 cm dışarı itiyordu = yatay basamak (`gd41_backline.py` tablosu). Pivot artık pelviste sırt-sabit → belde merkez, z 94–108 rampası; basamak ≤1.2 cm / 4 cm, lumbar kavis geri geldi → **final**.

## Kesit ölçümleri (cm; LK = üretim, ref = EVE referans silueti, nirengi hizalı)

```
bölge        z |  W_lk  W_D6  W_ref |  D_lk  D_D6  D_ref
bel        112 |  25.0  22.2  21.9  |  19.2  22.4  21.5
göbek      104 |  28.6  25.7  25.5  |  20.0  20.1  19.1
pelvis      96 |  31.8  30.2  28.4  |  22.5  21.7  21.3
kalça       90 |  34.2  35.1  30.8  |  24.1  24.4  22.7   (pelvis kemiği: bilerek +%10 geniş)
üst uyluk   74 |  15.8  16.1  16.2  |  16.1  19.0  19.0
orta uyluk  64 |  12.6  13.7  14.3  |  14.1  17.0  16.9
diz         46 |  10.2   9.6   9.6  |  11.1  11.3  11.1
baldır      36 |  10.7  10.7  10.3  |  11.2  12.3  11.3
bilek       14 |   5.6   5.3   5.1  |   7.5   8.0   8.1
```

## Doğrulama

Blender (mesh): ters üçgen 0, alan oranı 0.38–2.43 (en kötü IMF altı), kenar oranı 0.64–1.42, dikiş 0.0 mm (`data/gd41_D6_bodycheck.json`); sırt/ön çizgi tablosu `data/backline_D6.txt`.

UE 5.8 (D6): morph `GD41_Body` GeometryScript ile `SKM_GD41_BodyMesh` LOD0-3'e yazıldı — LOD0 12 079 vertex / en çok 27.9 mm, LOD1 3 019 / 25.7 mm, LOD2 1 131 / 26.8 mm, LOD3 480 / 21.4 mm; taban mesh değişmedi (0.0 cm); ABP `GD41_Body=1` Modify Curve (BR_Neutral, LK_Neutral ile birlikte), iskelet eğrisi 31→32 (D4 turunda eklendi); kaydedildi, dirty paket yok (`process/chain_D6.txt`). Harness yakalamaları: 20 tam boy + 40 yakın plan + 36 deformasyon (kil + ten, önce/sonra).

Eval montajı `BP_GD41_Character_Body` + `L_GD41_Eval_Body` (giysisiz): BP + level D4 turunda oluşturuldu (üzerine yazılmaz; mesh varlığı D5 ve D6 ile yerinde yeniden bake edildi, BP aynı varlığa bakar); D6 sonrası BP yakalamaları (`g41bp_body_*`) ile harness piksel karşılaştırması: ön gövde bölgesi ortalama |d| 0.0039, p95 0.0157, >0.05 olan piksel %0.72 → kaydedilmiş BP aynı vücudu gösteriyor. PIE: 1 instance, hata yok; Body `SKM_GD41_BodyMesh` LOD0, Face `SKM_GD38_Face_t38` LOD0 (`AS_GD33_Rest_lid60`, lid 0.6), 4 groom bağı görünür (`process/evalchain_D6.txt`).

Deformasyon pozları (armsfwd, backext, crouch, elbow, elev150/180, hipflex, squat, twist; V3 panoları): kil önce/sonra; yırtılma, kıvrım veya diken görülmedi (göz kontrolü, otomatik ölçüm yok).

## Panolar

- `boards/V1_TAM_BOY_CLAY_ONCE_SONRA.jpg` — 5 görünüm kil, üst önce / alt GD41 (aynı mesh, morph sıfır = önce).
- `boards/V2K_YAKIN_PLAN_KIL_1/2.jpg` — göğüs ön/yan, bel 3/4, kalça yan, gluteal arka/3/4, üst sırt, uyluk-diz, baldır, omuz-kol.
- `boards/V3_DEFORMASYON_1/2.jpg` — 9 poz kil, ön 3/4 + arka 3/4.
- `boards/B1..B7_blender_*.png` — Blender kil/ışıklı: LK → GD40 C8 → GD41 D6; D3/D4/D5/D6 ara adımları (B7: D5→D6 bel bandı).
- Ten (skin) panoları ve referans karşılaştırmaları yalnız yerel (`bd/final/V1_TAM_BOY_REAL_*`, `V2_*`, `V4_*`); üçüncü taraf referans sayfaları yayınlanmaz.

## Dürüst değerlendirme

- **Teknik: PASS** — morph bake, ABP eğrisi, LOD0-3, kaydedilmiş BP/level = harness, PIE readback.
- **Görsel: PARTIAL / kullanıcı kararı.** Prosedürel atlas; artist elinden çıkmış bir sculpt değil. Okunur hale gelenler: bel/oblik, rektus blokları, deltoid başlığı, erektör/omurga oluğu, skapula, dolu-yuvarlak kalça + kıvrım, VL/VMO/rektus femoris, gastroknemius başları, göğüs dolgunluğu ve yan duvar geçişi.
- Bilinen sınırlar: göğüs alt kıvrımı (IMF) hâlâ belirgin bir gölge (taban mesh'in sarkan alt kutbu; kasıtlı bırakıldı); mesh çözünürlüğü (LOD0 ~30k) yüzünden ince kas kenarları yumuşak; iskelet duruşu (referansın öne eğimi) aktarılmadı (kemik işi); kalça genişliği pelvis kemiği nedeniyle referanstan +%10.
- Sonraki paslar: giysilerin yeni vücuda yeniden oturtulması (GD41 vücudu gövde/kol/bacak çevrelerini değiştiriyor); SHC/RV düzeltmelerinin yeni nötr üzerine yeniden tabanlanması; isteğe bağlı artist sculpt geçişi.

## Dosyalar

- UE: `/Game/Sphirus/CharacterLab/GD41_Body_20261012/Body/{SKM_GD41_BodyMesh, ABP_GD41_Body_PostProcess}`, `.../BP_GD41_Character_Body`, `.../Maps/L_GD41_Eval_Body`, `.../Studio`. İskelet eğri metadata'sı (`GD41_Body`) `metahuman_base_skel`'e eklendi (checkpoint `checkpoint_skeleton/`).
- Araçlar (`tools/`): `gd41_anatomy.py` (atlas; env ile bölge çarpanları), `gd41_lib.py`, `gd41_contour.py`/`shape_plan.json` (GD40 yöntemi), `gd41_bodycheck.py`, `gd41_measure.py`, `gd41_bodyrender.py`, `gd41_zoom.py`, `gd41_cmpboard.py`, `ue_gd41_body_setup.py`, `ue_gd41_bake_body.py`, `gd41_chain.sh`, `gd41_evalchain.sh`, `ue_gd41_assembly.py`, `ue_gd41_evalqa.py`, `ue_gd41_pie.py`, `make_gd41_boards.sh`, `publish_gd41.py`.
- Veri (`data/`): D1–D6 bodycheck, D6 rapor (primitif tepeleri, env), `measure_D6.txt`, `backline_D6.txt`, `shape_plan.json`.
- Kaynak kopyası: `SourceAssets/Characters/GD41_Body_20261012/`.
