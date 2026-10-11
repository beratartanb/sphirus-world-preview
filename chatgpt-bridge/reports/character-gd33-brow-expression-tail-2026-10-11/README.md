# GD33 — Kaş ve ifade (30 yaş hedefi), kaş kuyruğu senin işaretlediğin bölgeden

Tarih: 2026-10-11. Başlangıç: GD31 yüzü G31 ve GD32 birleşik değerlendirme düzeni. **Yüz mesh'i değişmedi.**

Durum: **PARTIAL.** Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** Yeni varlıklar yalnız `/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011` altında.

## 1. İsteklerin

1. "30 civarı yaşlarda bir karakter isteniyor." Seçimin: önce **kaş + ifade**.
2. "Şakaklarda kaş ucu yeterince uzayıp referanstaki formda devam etmiyor, modelde kısa."
3. "Referans kaş işaretlediğim yerler içerisinde. Saç ile karıştırıp modelin kaşına garip bir kıvrım ekleme; ana kaş formunu çözümleyip yap." İşaretlediğin bölgeler `M1` panosunda ve `data/usermask` klasöründe.

## 2. Teşhis: çatık ve sert okumanın kaynağı

`process/01` ve `process/02` aynı kamerada ölçüldü.

- **Kaş konumu sorun değildi.** Üst kenar referansla aynı satırda. Kaş eğimi de referansta daha fazla yükseliyor.
- **Kaş fazla koyuydu.** Koyuluk c4'te 0,62/0,64, referansta 0,53/0,52. İç uçlar küt, dik ve koyu bir blok gibiydi.
- **Asıl etken göz bölgesiydi.** Göz açıklığı referanstan yaklaşık %25 dardı. Üst kapak irisin üst üçte birini örtüyordu, kaş altı bölge de gölgedeydi.

## 3. Yapılanlar (yüz geometrisi değişmedi)

**Kaş c7u3** (`tools/gd33_brow.py`, `gd33_tail3d.py`):

1. **İç uç yumuşatıldı.** Daha seyrek, daha yatık ve daha kısa kıllar (`K1`).
   - İç uç koyuluğu c4'te 0,57/0,47 idi; c5hl1'de 0,48/0,42, c7u3'te 0,43/0,42. Referans 0,51/0,48.
2. **Ton bir kademe açıldı.** Melanin 0,72'den 0,65'e indi (`MI_GD33_BrowS_l1`). Kalınlık korundu, çünkü ince kızıl kaşı daha önce reddetmiştin.
3. **Kuyruk işaretlediğin bölgeden yeniden kuruldu.**
   - Kırmızı sınırlar görüntülerinden maske olarak çıkarıldı. Referans kaş yalnız bu maskenin içinde ölçüldü (`process/03`, `process/04`); saç teli dışarıda kaldı.
   - Ölçülen yol çözülmüş q3_faceR kamerasıyla kafa yüzeyine izdüşürüldü. Medial ve gövde istasyonları korundu; kuyruk kemerin devamı olarak, geçişi yumuşatılarak uzatıldı ve uca doğru inceltildi.
   - Sağ kaş aynı biçimin aynalanmışı. Profilde işaretlediğin bölgeyle doğrulandı.

| Kuyruk ucu (panel px) | c5hl1 (önce) | **c7u3** | Referans (işaretli bölge) |
|---|---|---|---|
| q3_faceR, sol kaş | (564, 370) | **(537, 386)** | (536, 386) |
| Profil, sağ kaş (profil ölçeği 1/1,087) | (267, 340) | **(305, 358)** | (306, 356) |

Uzunluk yaklaşık 15 mm arttı, uç yaklaşık 6,6 mm aşağı indi; kaşın yay uzunluğu 5,1 cm'den 6,7 cm'ye çıktı. Gövde yoğunluğunu korumak için tel sayısı orantılı artırıldı. Uçta kuyruk yoğunluğu 0,12'ye indirildi; uç sönümlenerek bitiyor.

**Reddedilen ara adım:** t1 ve t2 (`process/05`, `process/06`). Kuyruğa kısa mesafede aşağı kıvrım eklemiştim. Saç tellerini kaşla karıştırmıştım ve kanca oluşmuştu. Senin geri bildirimin üzerine bırakıldı.

**Sakin göz (dinlenme ifadesi):** `AS_GD33_Rest_lid60`, RigLogic kontrolü `eyeUpperLidUp` = 0,6 (`E0`–`E2`).

- 0,15–0,30 ağırlıkları gözle görülmeyecek kadar küçüktü.
- 1,0 fazla açıktı; bakakalmış bir göz verdi.
- 0,6 göz açıklığını referansa yaklaştırıyor.

Bu, mesh'i değiştirmeyen bir rig pozu; kapatılabilir.

## 4. Editörde değerlendirme

1. Şu haritayı aç: `/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011/Maps/L_GD33_Eval_G31`
2. GD32'deki gibi `CAM_REF_*`, `CAM_HS_*` ve `CAM_BODY_*` kameralarından birine sağ tıklayıp **Pilot** de.
3. **Dinlenme pozunu (sakin göz) görmek için Simulate (Alt+S) veya PIE gerekiyor.** UE, `update_animation_in_editor` değerinin Blueprint şablonunda ayarlanmasına izin vermiyor. Bu yüzden düz editör görünümünde yüz nötr görünür.

Blueprint `Assembly/BP_GD33_Character_G31`: GD32 düzeni, kaş c7u3, yüzde `AS_GD33_Rest_lid60` döngüde. Saç h75c, kirpik S_Thin, ten n3, göz h6 GD31'deki gibi.

## 5. Panolar

- `F1`: REF | GD31 | GD33 kaş | GD33 final, saçlı, stüdyo ışığı, dört referans açısı.
- `F2`: kaş ve göz yakın plan.
- `T1`: kaş kuyruğu, saçlı (REF | c5hl1 | c7u3).
- `M1`: işaretlediğin bölge (kırmızı) referansın, eski kaşın ve yeni kaşın üstünde.
- `K1`: iç uç ve ton varyantları.
- `E0`, `E1`, `E2`: ifade ve göz açıklığı adayları.
- `C1`: baş-omuz dönüşü. `C2`: tam boy (kayıtlı Blueprint'ten).
- `process/07`: önden saçsız kuyruk. `process/08`: Blueprint ile çekim düzeni arasındaki fark (5×).

## 6. Teknik testler

| Test | Sonuç |
|---|---|
| c4 kaşın aynı parametrelerle yeniden üretimi | **PASS** (fark 0,0) |
| Kaş varyantlarının içe aktarımı ve G31 yüzüne bağlanması (10 varyant) | **PASS** |
| Blueprint: 4 groom bağlaması şablonda (`set_binding_asset`), temiz oturumda yükleme | **PASS** |
| PIE: kaş c7u3 bağlı ve görünür; yüzde `AS_GD33_Rest_lid60`, `eyeUpperLidUp` L/R = 0,6 | **PASS** (`data/pie_check.json`) |
| Kayıtlı Blueprint ile çekim düzeninin birebirliği (aynı kamera, ışık, kaş, poz) | **PASS** (yüz bölgesinde ortalama fark 0,012–0,016, yalnız gürültü; `data/verify_bp_vs_harness_pixels.txt`) |
| Yüz mesh'i değişmedi | **PASS** (GD31 `SKM_GD31_Face_g31` yalnızca referans) |
| Dinlenme pozu editör görünümünde | **PARTIAL** (yalnız Simulate/PIE'de) |
| Oyun içi idle yüz katmanı, animasyon | **NOT_TESTED** |
| Üretim değişmedi | **PASS** (`data/outside_change_scan.txt`; qa_config geri yüklendi; editör hep kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 7. Açık kalanlar

- **Kaş altı gölge ve koyu kirpikler** hâlâ biraz ağır duruyor. Sonraki geçişte kirpik tonu/yoğunluğu ve ten rengi ele alınabilir.
- **Kuyruk ucu, q3_faceL'de saçlı görünümde.** Uç, saçın dışında kaldığı için gövdeden koyu görünebilir; referansta bu bölge saçın altında. Gerekirse uç biraz daha açılabilir.
- **Dinlenme pozu oyunda.** Oyunda kullanılacaksa yüz animasyonuna idle katmanı olarak eklenmesi gerekir.
- **Diğer kaş varyantları.** c5hl2 (iki kademe açık ton), c6t1/c6t2 (reddedilen kanca), c7u1/c7u2 (ara sürümler) GD33 klasöründe test varlığı olarak duruyor.
