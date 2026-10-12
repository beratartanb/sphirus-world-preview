# GD40 — Vücut hatları ve formu: referans anatomisi, Guardian görünüşü

Tarih: 2026-10-12. Başlangıç: değerlendirme vücudu (kabul edilmiş B2 + BR_Neutral v6 + LK_Neutral), GD38 yüzü (t38). GD39 (yumuşak tonlama) yetersiz bulundu: "düşük kaliteli vücutta çok fazla kaldı".

Durum: **PARTIAL.** Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED). Üretim karakterine uygulanmadı. Yöntem **PROCEDURAL** (kesit-kontur aktarımı + kas atlası; elle fırça yok): **ARTIST-GRADE = NO.**

## 1. İsteğin

"Vücut formunu, duruşunu, kaslarını ve dokularını bu referanslar üzerinden ver; genel formunda ve görünüşünde ana karakter referansını (Guardian) al." Sonra: "Vücut hatlarını ve formunu ustaca çözümle ve karakterimize yedir."

Önceki kararlar aynen: iskelet, boy ve eklemler değişmedi; göğüs boyutu korundu; giysiler sonraki geçişte. Üçüncü taraf referans levhası yerel klasörde kaldı; bu rapora konmadı.

## 2. Çözümleme (`tools/gd40_contour.py`)

Referansın beş görünümlü levhasından siluet eğrileri çıkarıldı ve bizim vücudun gerçek düzlem kesitleriyle (üçgen kenarı–düzlem kesişimi, kollar ağırlıklarla dışarıda) karşılaştırıldı. Her şey boya göre oranlı (ölçekten bağımsız).

**Hizalama.** Referansın bacakları bize göre daha uzun (çatal 0,49 H, bizde 0,54 H). Bu yüzden karşılaştırma, anatomik işaret noktalarıyla parça parça hizalandı: göğüs ucu, göbek, çatal, diz, baldır tepesi, bilek. Böylece oranlar dikey orantı farkından etkilenmiyor.

**Yan görünüm.** Referansın ön kolu ve eli 0,40–0,60 H aralığında karnın ve uyluğun önünde duruyor; o satırlarda ön hat temiz satırlar arasından doğrusal alındı. Sırt hattı temiz.

**Duruş.** Referans öne eğik duruyor (gövde, bilek hizasının 6–7 cm önünde). Bu iskeletsel bir duruş farkı; kopyalanmadı. Ölçülebilen biçim farkları: bel çukurunun kalça tepesine göre derinliği zaten benzer (4,6 / 4,2 cm); asıl farklar kalça tepesinin referansta daha aşağıda ve uyluğun çok daha derin olması.

Ölçülen farklar (önceki vücut / referans, boya oranla):

| Bölge | Fark |
|---|---|
| Bel | %13 geniş, %11 sığ; gövde kenarı düz, koniklik yok |
| Göbek hizası | %10 geniş |
| Kalça | %10 geniş (pelvis kemiği; korunacak) |
| Uyluk | derinlik %17–23 az (kuadriseps + hamstring), orta uylukta %13 dar |
| Diz | %13 geniş |
| Alt baldır / bilek | %14–20 kalın; baldır arkası %23 düz |
| Sırt | omurga oluğu, dikleştirici kaslar, kürek kemiği okunmuyor |
| Omuz | deltoid başı yok |
| Göğüs altı | sert "raf" çizgisi |

`process/05`: genişlik, derinlik ve yan hat eğrileri (sarı referans, mavi biz, yeşil hedef).

## 3. Yöntem (`tools/gd40_master.py`, aday C8)

Tek "her zaman açık" morph (`GD40_Body`) mevcut nötrün üstüne. Üç katman:

**A. Kesit blok-çıkarma.** Her yükseklikte kesit, hizalı referans oranıyla ölçeklendi:
- gövde (çatal üstü): genişlik orta hatta göre, derinlik kesit merkezine göre; göğüs bandı, boyun dikişi bandı ve ayaklar korundu; kemik bantları (göğüs kafesi altı, kalça) en fazla %5 daraltıldı;
- bacaklar (kemik eksenine göre, bacak başına): genişlik ve derinlik; iç uyluk orta hatta yakınken ölçeklenmedi (çatalda çarpışma); uyluk oranları kalça eklemine doğru 16 cm'de sönümlendi (raf çizgisi olmaması için);
- kollar dokunulmadı (Guardian'ın ince kolları);
- güç: genişlik 0,9, derinlik 0,8.

**B. Kas atlası.** Yüzeye oturan düz tepeli primitifler (lif yönü, kenarı belirli), yarıklara negatif:
karın sütunları (3 çift, en alttaki yumuşak) ve ara çizgiler, linea alba, yarım ay çizgileri, dış oblikler, kasık çizgisi, serratus, üst pektoral; dikleştiriciler, omurga oluğu, lats, infraspinatus, kürek kemiği iç kenarı, alt trapez, sakral çukurlar; gluteus maximus / medius, kalça altı kıvrımı, trokanter çukuru, TFL; rectus femoris, vastus lateralis / medialis, sartorius oluğu, adduktörler, hamstringler ve oluğu, IT bandı oluğu; patella, çevre çukurları, diz yanları; gastroknemius başları ve oluğu, soleus, Aşil, tibialis anterior; deltoid başları ve yapışma oluğu, biseps, triseps, ön kol ekstansörleri. Tepe değerleri 1–5,5 mm (`data/gd40_body_report_C8.json`).

**C. Doku ve koruma.** Alt karın düzleşme (7 mm), göğüs altı rafı hafif yumuşatma (boyut aynı); boyun dikişi bandı ve 92 kaynak çiftinin 1,5 cm çevresi, eller, ayaklar sabit; 1 Laplace adımı; LOD1–3'e barisentrik aktarım.

Toplam: 10.660 köşe, en fazla 21,6 mm, p99 18,2 mm.

### Reddedilen adaylar
| Aday | Sorun |
|---|---|
| B1–B4 | yalnız kas atlası: form değişmiyor, "bump" okunuyor (B4 UE'de çekildi, `g40_*`) |
| C1 | yan hat (duruş) aktarımı: referansın öne eğikliği taşındı, 36 mm hareket, 92 ters üçgen |
| C2 | 75 ters üçgen (göğüs altı bandı, çatal) |
| C3 | temiz ama uyluk üstünde yatay raf çizgisi (UE'de çekildi, `g40c_*`) |
| C4–C5 | bacak oranı kalçaya taşınınca kalça %14 genişledi |
| C6 | raf çizgisi sürdü (UE'de çekildi, `g40d_*`) |
| C7 | uyluk geçişi düzeldi; gövde derinliği eksik kaldı |
| **C8** | **seçilen** (gövde derinlik ölçeği eklendi) |

## 4. Sonuç: kesit ölçümleri (cm, bağlama pozu, kollar hariç)

| Bölge (z) | Genişlik önce → **C8** (ref) | Derinlik önce → **C8** (ref) |
|---|---|---|
| Göğüs kafesi (120) | 27,1 → 26,8 (18,8*) | 19,1 → 19,5 (18,5) |
| Bel (112) | 25,0 → **22,0** (21,9) | 19,2 → **21,4** (21,5) |
| Göbek (104) | 28,6 → **25,6** (25,5) | 20,0 → 19,9 (19,1) |
| Pelvis (96) | 31,8 → 29,9 (28,4) | 22,5 → **21,3** (21,3) |
| Kalça (90) | 34,2 → 35,0 (30,8**) | 24,1 → 23,8 (22,7) |
| Üst uyluk (74) | 15,8 → 16,0 (16,2) | 16,1 → **18,7** (19,0) |
| Orta uyluk (64) | 12,6 → 13,6 (14,3) | 14,1 → **16,6** (16,9) |
| Alt uyluk (56) | 11,2 → 11,3 (11,3) | 12,4 → **14,7** (15,2) |
| Diz (46) | 10,2 → **9,6** (9,6) | 11,1 → 11,2 (11,1) |
| Baldır (36) | 10,7 → 10,4 (10,3) | 11,2 → 11,7 (11,3) |
| Alt baldır (24) | 8,2 → **7,2** (7,0) | 8,5 → **10,1** (10,6) |
| Bilek (14) | 5,6 → 5,3 (5,1) | 7,5 → 8,0 (8,1) |

\* Göğüs kafesi genişliği referansta göğüs ucu altındaki dar kesit; bizde kemik + göğüs yanı, korundu. \*\* Kalça genişliği pelvis kemiği; bilinçli olarak korundu (Guardian'ın olgun kalça yapısı), yalnız yumuşak doku %3 daraldı.

Siluet oranları (C8 / referans, boya göre): bel 1,005 (önce 1,14), diz 1,04 (1,17), baldır 1,02, bilek 1,09 (1,13), bel derinliği 0,99 (0,91), uyluk derinliği 0,95 (0,84), baldır derinliği 0,98 (0,92), kalça derinliği 1,05. Kalça genişliği 1,13: pelvis + siluette iç uylukların daha aşağıda birleşmesi.

## 5. Panolar

- `V1_TAM_BOY_CLAY`: beş açı kil; üstte önce, altta sonra (aynı mesh, morph sıfırlanarak).
- `V2K_YAKIN_PLAN_KIL_1/2`: göğüs, bel, kalça yanı, kalça arkası ve 3/4, üst sırt, uyluk–diz, baldır, omuz–kol.
- `V3_DEFORMASYON_1/2`: dokuz poz (kol öne, sırt geri, çömelme, dirsek, 150°/180° kol kaldırma, kalça bükme, squat, dönüş).
- `V4K`: Guardian konsepti ve GD40 vücut (kil).
- `process/01–09`: aday karşılaştırmaları (yönlü ışıklı kil): önceki | B4 atlas | C6 | C7 | C8.
- `process/05`: kontur eğrileri.

## 6. Editörde değerlendirme

1. Şu haritayı aç: `/Game/Sphirus/CharacterLab/GD40_Body_20261012/Maps/L_GD40_Eval_Body`. Blueprint: `BP_GD40_Character_Body` (giysisiz).
2. Sakin göz pozu yalnız **Simulate (Alt+S) veya PIE** sırasında görünür.

## 7. Teknik testler

| Test | Sonuç |
|---|---|
| Hedef C8: ters üçgen 0; alan oranı 0,43–2,71; kenar oranı 0,69–1,28 | **PASS** |
| Kafa–vücut dikişi: 92 kaynak çiftinde değişiklik 0,000 mm | **PASS** |
| İskelet, bağlama pozu, SHCB değişmedi; yalnız morph eklendi | **PASS** |
| Morph aktarımı LOD0–3: taban geometri değişmedi (0,0 cm) | **PASS** |
| Önce/sonra aynı mesh ve aynı kamerada (morph sıfırlanarak) | **PASS** |
| Deformasyon pozları (9 poz, kil): yeni kusur görülmedi | **PASS** (görsel; ölçümsel penetrasyon testi yok) |
| Kayıtlı Blueprint ile harness çekimlerinin birebirliği: vücut bölgesinde ortalama fark 0.003–0.005, yalnız gürültü | **PASS** |
| PIE: vücut SKM_GD40_BodyMesh, yüz t38, 4 groom görünür, `eyeUpperLidUp` 0,6 | **PASS** |
| Düzeltici morph'lar (SHC, RV) yeni biçime göre yeniden hesaplanmadı | **NOT_TESTED** |
| Giysiler | **NOT_TESTED** (gizli; sonraki geçiş) |
| Üretim değişmedi (`data/outside_change_scan.txt`). qa_config geri yüklendi, editör kaydetmeden kapatıldı. Tek dış değişiklik: yalıtılmış iskelet kopyasına eklenen `GD40_Body` eğri kaydı (yedeği alındı). | **PASS** |
| ARTIST-GRADE | **NO** |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 8. Açık kalanlar

- **Kalça genişliği** pelvis kemiğinden; referansa göre %10 geniş kalacak. İstersen yumuşak doku bir %3 daha daraltılabilir.
- **Giysiler**: Henley ve şort yeni vücuda uyarlanmalı. Bel 3 cm daraldı, uyluklar 2,5 cm derinleşti; şort kalıbı ve Henley eteği etkilenir.
- **Düzeltici morph'lar**: omuz ve yumuşak doku düzeltmeleri yeni biçime göre yeniden temellendirilmeli; şu an değişmeden üstüne ekleniyor.
- **Sanatçı heykeli**: kas geçişlerinin son kalitesi (karın blokları, diz, kalça–hamstring) elle ister. Bu geçiş, blok-çıkarma ve kas yerleşimi olarak sağlam bir temel veriyor.
