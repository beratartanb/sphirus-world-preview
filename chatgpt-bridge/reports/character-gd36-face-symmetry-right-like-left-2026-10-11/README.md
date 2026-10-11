# GD36 — Yüz simetrisi: sağa bakış, sola bakışın formuna

Tarih: 2026-10-11. Başlangıç: GD31 yüzü G31, GD35 görünümüyle (kaş ds7n4, ten n3, göz h6, sakin göz pozu).

Durum: **PARTIAL.** Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED). Üretim karakterine uygulanmadı. Yeni varlıklar yalnız `/Game/Sphirus/CharacterLab/GD36_IdentityMaster_20261011` altında.

## 1. İsteğin

"Sola baktığı açıda surat iyi, sağa baktığı açıda biraz garip ve referanstan uzak. Sağa bakışı sola bakış gibi yapalım; sağ ve sol oranları birbirine benzetelim."

- Sola bakış = `q3_faceL`: öznenin **sol** yüz yarısı (+x). İyi taraf.
- Sağa bakış = `q3_faceR`: öznenin **sağ** yüz yarısı (−x). Bu taraf, sol yarının aynasından yeniden kuruldu.

## 2. Teşhis: sağ yarı ile sol yarının aynası arasındaki fark (GD31, rig sonrası)

| Bölge | Önce (ortalama / p95) | **GD36** | Sağ yarıdaki yön (önce) |
|---|---|---|---|
| Çene gövdesi ve köşesi | 3,9 / 7,0 mm | **1,4 / 3,4** | 2,8 mm içeride, 1,2 mm geride ve aşağıda |
| Orta yanak | 3,0 / 4,7 | **1,1 / 4,0** | 1,8 mm dışarıda |
| Alt yanak | 2,8 / 4,4 | **1,0 / 1,6** | |
| Elmacık | 1,7 / 3,0 | **0,5 / 0,7** | dışarı ve öne |
| Kaş kemiği | 4,1 / 5,2 | **2,0 / 4,7** | 3,6 mm önde |
| Şakak | 2,7 / 5,2 | **1,0 / 3,7** | içeride |
| Çene ucu | 1,7 / 3,3 | **0,9 / 2,3** | |
| Üst göz kapağı (korundu) | 2,6 | 2,5 | |
| Dudaklar (korundu) | 1,2–1,6 | 1,2–1,6 | |
| **Yüz ortalaması** | **1,79 mm** | **1,22 mm** | |

Sağa bakıştaki köşeli, uzun çene ve düz yanak görüntüsü buradan geliyordu. Kalan ~1 mm, korunan göz kapakları ve dudakların doğal asimetrisi.

## 3. Yöntem

1. **Sürekli ayna eşlemesi** (`tools/gd36_uvmirror.py`). MetaHuman yüz UV'si sağ-sol simetrik (u ↔ 1−u). Her köşe için karşı yarıdaki aynı UV noktası barisentrik enterpolasyonla bulunup aynalandı. Kafanın kendi simetri düzlemine göre rijit olarak hizalandı (1,5–1,8° yaw).
   - Hazır köşe-köşe eşlemeleri (en yakın komşu: %69, UV köşe: %72 karşılıklı) yüzeyde çatlak oluşturdu, reddedildi (`process/01`).
2. **Hedef** (`tools/gd36_sym.py`, K100).
   - Sağ yarı, sol yarının hizalanmış aynasına %100 taşındı; aynalanan yer değiştirme alçak geçirgen süzgeçten geçirildi (60 Laplace adımı).
   - Orta hatta 0,6 cm'lik yumuşak geçiş var.
   - **Göz kapakları** (0,5 cm geçişle) ve **dudaklar** (1,4 cm geçişle) korundu, çünkü sağ göz küresine ve ağza oturmaları gerekiyor. Aynalandıklarında göz kapağı göze giriyor, ağız köşesinde kırışık oluşuyordu.
   - **Kafa arkası, boyun ve kulaklar** tamamen sabit.
   - **Sol yarı** hiç değişmiyor.
3. **Motor zinciri.** GD31 MHC'sinin kopyası, 4 aşamalı geri beslemeli fit, otomatik rig (858 morph, DNA), GD35 kaşının yeni deri üzerinde yeniden üretilmesi, saç ve kirpiğin yeni yüze bağlanması, ardından çekimler.

**İlk deneme reddedildi (H100 → G36).** Koruma bölgelerinin ağırlığı tam sıfıra inmediği için hedef, saçın altındaki kafa arkasını ve kulakları da 8,7 mm'ye kadar oynatmıştı. Bu hata düzeltildi ve zincir K100 hedefiyle (K36) yeniden çalıştırıldı. İlk denemenin varlıkları GD36 klasöründe test kaydı olarak duruyor.

## 4. Panolar

- `S3`: sabit simetrik kameralarda sağa bakış ile sola bakışın yatayda çevrilmiş hâli, saçlı (üst GD35, alt GD36).
- `S4`: aynı karşılaştırma kil olarak (doku ve saç yok); geometri farkını en net bu gösteriyor.
- `F1`: REF | GD35 | GD36, saçlı, sakin göz, referansın dört açısı. `F2`: saç gizli.
- `process/02`: kilde hedef adayları (H70, H100).

## 5. Editörde değerlendirme

1. Şu haritayı aç: `/Game/Sphirus/CharacterLab/GD36_IdentityMaster_20261011/Maps/L_GD36_Eval_G36`. Kameralar ve ışık önceki geçişlerle aynı.
2. Sakin göz pozu yalnız **Simulate (Alt+S) veya PIE** sırasında görünür.

## 6. Teknik testler

| Test | Sonuç |
|---|---|
| Hedef: ters üçgen 0, kat 40 (başlangıçta 41), koruma bölgelerinde hareket 0,0 mm, sol yarıda hareket 0,0 mm | **PASS** |
| Fit (4 aşama) → hedef | **PASS** (ortalama 0,056 mm, p95 0,28, p99 0,75, en fazla 3,8 mm; GD31: 0,045 / 0,61 / 1,6) |
| Otomatik rig, DNA, 858 morph | **PASS** (`MHC_GD36_K36`, `SKM_GD36_Face_k36`) |
| Rig sonrası: ters üçgen 0, kat 40, alan oranı 0,55–3,0, göz kapağı ile göz küresi teması GD31 ile aynı | **PASS** |
| Sol yarı, GD31 rig sonrasıyla aynı | **PASS** (ortalama 0,013 mm, en fazla 0,15) |
| Kafa arkası / kulak / gövde dikişi, GD31'e göre | **PASS** (en fazla 0,14 / 0,28 / 0,000 mm) |
| Kaş, saç ve kirpik yeni yüze bağlı; PIE'de 4 groom görünür, `eyeUpperLidUp` 0,6 | **PASS** |
| Kayıtlı Blueprint ile çekim düzeninin birebirliği | **PASS** (yüz bölgesinde ortalama fark 0,012–0,017, yalnız gürültü) |
| İfadeler (RigLogic), LOD1–7, animasyon | **NOT_TESTED** (yeni rig; ifade testi bu turda yapılmadı) |
| Üretim değişmedi | **PASS** (`data/outside_change_scan.txt`; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 7. Açık kalanlar

- **Farkın büyüklüğü.** Değişim çoğunlukla çene hattında ve alt yanakta, birkaç milimetre düzeyinde. Dokulu ve saçlı görüntüde ince kalıyor; en net `S4` kil karşılaştırmasında görülüyor. Daha belirgin bir eşitleme istenirse göz kapakları da aynalanabilir; bunun için sağ göz küresinin konumu da düzeltilmeli.
- **Kaş kemiği.** Asimetri 2,0 mm'de kaldı, çünkü korunan göz kapağına yakın.
- **Kameralar.** Referansın iki 3/4 kamerası birbirinin tam aynası değil; sağa bakış daha yandan çekilmiş. Referans karşılaştırmasında açı farkı da rol oynuyor.
- **Testler.** Yeni rig için ifade testi ve LOD kontrolü istenirse ayrıca yapılabilir.
