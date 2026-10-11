# GD39 — Vücut: referans biçimi, Guardian karakterine bağlı yumuşak tonlama

Tarih: 2026-10-12. Başlangıç: mevcut değerlendirme vücudu (kabul edilmiş B2 + BR_Neutral v6 + LK_Neutral, `SKM_LK_BodyMesh`), GD38 yüzü (t38).

Durum: **PARTIAL.** Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED). Üretim karakterine uygulanmadı. Yöntem **PROCEDURAL**: script alanları kullanıldı, elle fırça yok. Bu yüzden **ARTIST-GRADE = NO**.

## 1. İsteğin ve kararlar

İsteğin: "Vücudu bu referanslar üzerinden yap, referanstaki kafayı dahil etme." Ardından: "Asıl karakterimizin yapısına ve görünümüne daha bağımlı kal" (Guardian konsepti).

Senin seçimlerin:

| Konu | Seçim |
|---|---|
| Kas tanımı | Referansın biçimi, ama **yumuşak** tanım |
| İskelet | **Aynı** kalacak; boy, eklemler ve kemik uzunlukları değişmeyecek, yalnız biçim değişecek |
| Giysiler | Önce vücut; Henley ve şort sonraki geçişte yeni vücuda uyarlanacak |

Verilen vücut referansı üçüncü taraf ticari bir çalışma ve çıplak figür içeriyor. Bu yüzden bu rapora **konmadı**, yalnız yerel ve özel klasörde tutuluyor. Karşılaştırmalar kil renderlarla ve Guardian konseptiyle yapıldı.

## 2. Teşhis

Referansla aynı yöntemle ölçüldü: siluet işaret noktaları, boya göre oranlanmış.

| Bölge | Mevcut vücut, referansa göre |
|---|---|
| Bel | Önden %14 geniş, yandan %9 sığ. Bel konikliği yok; gövde kenarı göğüs kafesinden kalçaya düz. |
| Diz | %17 geniş, diz okunmuyor |
| Ayak bileği | %13 geniş |
| Uyluk (yandan) | %16 ince; ön ve arka uyluk kas dolgunluğu az |
| Baldır arkası | %8 düz |
| Kalça (gluteal) | Derinlik eşit, ama basık ve aşağıda |
| Sırt | Özelliksiz: omurga oluğu, dikleştirici kaslar ve kürek kemiği okunmuyor |
| Omuz | Omuz başı (deltoid) tanımsız |
| Göğüs | Alt kenarda sert bir "raf" çizgisi |

Guardian konseptine sadık kalmak için korunanlar:
- göğüs boyutu;
- bacak uzunluğu ve oranlar (iskelete bağlı);
- genel incelik (bacaklar ince-tonlu).

## 3. Yöntem

### Morph `GD39_Body` (`tools/gd39_body_art.py`, A2 = genlik ×1,4)
Mevcut nötr vücudun üzerine üçüncü bir "her zaman açık" morph eklendi, LK_Neutral ile aynı düzende. Tepe değerleri mm cinsinden:

| Bölge | Değişiklik |
|---|---|
| Gövde | Bel yanları içe 7,0; alt karın düzleşme 4,2; hafif linea alba 1,1 ve kasık (inguinal) çizgisi 1,4; lats (V konikliği) 1,7 |
| Sırt | Omurga oluğu 2,1; dikleştirici kaslar 1,4; kürek kemiği altı dolgunluk 1,7; bel çukurları 0,9 |
| Kalça | Üst-orta kalça dolgunluğu 5,6 (kalkık görünüm); alt kalça sarkması −2,0; gluteus medius yuvarlaklığı 2,5. Kalça yarığına dokunulmadı. |
| Bacak | Uyluk önü 3,5 ve dış uyluk (vastus lateralis) 2,1; arka uyluk 2,1; diz yanları içe 2,8; baldır iç ve dış başları 3,5 / 2,1; alt baldır ve Aşil bölgesi incelme 1,7 |
| Kol | Deltoid başı 1,5; triseps 1,4 |
| Göğüs | Alt kenar "raf"ı maskeli gevşetme ile yumuşatıldı; boyut değişmedi |

Diğer özellikler:
- En büyük değişim 6,7 mm, p99 4,9 mm, 16.341 köşe.
- **Koruma:**
  - boyun dikişi bandı (z > 138,5 cm), eller ve ayaklar değişmedi;
  - kafa–vücut dikişindeki 92 kaynak çiftinde değişiklik en fazla 0,001 mm, morph'a yazılmadı;
  - 3 Laplace yumuşatma adımı uygulandı.
- LOD1–3'e en yakın nokta barisentrik aktarımla taşındı.

Mesh üzerinde ölçülen etki:
- bel (z 104–108) 1,0–1,3 cm daraldı;
- diz 4,4 mm inceldi;
- baldır arka derinliği 5 mm arttı;
- alt baldır 3 mm inceldi.

### UE (`tools/gd39_chain.sh`)
1. `SKM_GD39_BodyMesh` ve `ABP_GD39_Body_PostProcess` oluşturuldu: LK vücudunun ve ABP'sinin kopyaları, ABP'ye `GD39_Body = 1` eğrisi eklendi.
2. Morph LOD0–3'e aktarıldı; taban geometri değişmedi (0,0 cm).
3. Kompozisyon kuruldu: GD38 yüzü, bağlamaları ve görünümü, yeni vücut, giysisiz.
4. Çekimler alındı: tam boy, yakın plan ve deformasyon; her biri aynı mesh üzerinde morph sıfırlanarak **önce/sonra**.
5. Değerlendirme BP'si ve haritası kuruldu, PIE çalıştırıldı.

### Seçenek: daha belirgin A3 (genlik ×2,0)
Yalnız kil önizlemesi; UE'ye aktarılmadı (`process/01`, `process/02`). En büyük değişim 9,6 mm, p99 7,0 mm. İstersen sonraki adımda A3 ya da ikisinin arası aktarılabilir.

## 4. Panolar

- `V1_TAM_BOY_CLAY`: tam boy kil, beş açı; üstte önce, altta sonra.
- `V2K_YAKIN_PLAN_KIL_1/2`: göğüs, bel, kalça yanı, kalça arkası ve 3/4, üst sırt, uyluk-diz, baldır, omuz-kol; önce/sonra.
- `V3_DEFORMASYON_1/2`: kol öne, sırt geri, çömelme, dirsek, 150°/180° kol kaldırma, kalça bükme, squat, dönüş; önce/sonra (kil).
- `V4K`: Guardian konsepti ve GD39 vücut (kil); bacak, kol, omuz ve bel okuması.
- `process/01-02`: GD38 vücut | A2 (seçilen) | A3 (daha güçlü önizleme), Blender kil.
- Ten görünümlü (çıplak) panolar bu rapora konmadı; yerel klasörde duruyor.

## 5. Editörde değerlendirme

1. Şu haritayı aç: `/Game/Sphirus/CharacterLab/GD39_Body_20261012/Maps/L_GD39_Eval_Body`. Blueprint: `BP_GD39_Character_Body` (giysisiz).
2. Sakin göz pozu yalnız **Simulate (Alt+S) veya PIE** sırasında görünür.

## 6. Teknik testler

| Test | Sonuç |
|---|---|
| Morph aktarımı LOD0–3: başarılı, taban geometri değişmedi (0,0 cm) | **PASS** |
| İskelet, kemikler, bağlama pozu ve SHCB değişmedi; yalnız morph eklendi | **PASS** |
| Kafa–vücut dikişi: 92 kaynak çiftinde değişiklik ≤ 0,001 mm (morph'ta yok) | **PASS** |
| Önce/sonra aynı mesh ve aynı kamerada (morph sıfırlanarak) | **PASS** |
| Deformasyon pozları (9 poz, kil): GD39'a özgü yeni kusur görülmedi. Kildeki noktacık gürültüsü önce/sonra aynı. | **PASS** (görsel; ölçümsel penetrasyon testi yok) |
| Düzeltici morph'lar (SHC, RV yumuşak doku) yeni biçime göre yeniden hesaplanmadı; değişiklik ≤ 6,7 mm olduğu için toplanır biçimde geçerli varsayıldı | **NOT_TESTED** (rebase yok) |
| Kayıtlı BP ile harness çekimlerinin birebirliği: vücut bölgesinde ortalama fark 0,002–0,005 | **PASS** |
| PIE: vücut SKM_GD39_BodyMesh, yüz t38, 4 groom görünür, `eyeUpperLidUp` 0,6 | **PASS** |
| Giysiler (Henley, şort) | **NOT_TESTED** (bu geçişte gizli; yeni vücuda uyarlanmadı) |
| Üretim değişmedi (`data/outside_change_scan.txt`). Tek dış değişiklik: yalıtılmış CharacterLab iskelet kopyasına eklenen eğri kaydı; önce yedeği alındı. | **PASS** |
| ARTIST-GRADE | **NO** (procedural) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 7. Açık kalanlar

- **Değişim düzeyi.** Değişim bilinçli olarak küçük: Guardian'a bağlı ve yumuşak. Referansın kaslı ve kıvrımlı yapısına göre çok daha ölçülü. Daha belirgin istenirse A3 (×2,0) hazır.
- **Script ile yapılabilenin sınırı.** Script ile yapılan tonlama burada sınırına yakın. İnce kas geçişleri (karın blokları, diz çevresi, kalça–arka uyluk geçişi, sırt) için gerçek kalite elle heykel ister.
- **Giysiler.** Henley ve şort yeni vücuda uyarlanmalı; sonraki geçiş.
- **Düzeltici morph'lar.** SHC ve RV düzeltici morph'ları yeni biçime göre yeniden temellendirilebilir (rebase); şu an değişmeden üstüne ekleniyor.
