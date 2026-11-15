# SPHIRUS — Tam beden biyomekaniği, 1. tur (analiz + kanıtlanan ilk düzeltmeler) — 2026-11-15

**Bu rapor görevin tamamı değildir.** Bu turda yapılan: gerçek oyun kayıtlarından tam beden biyomekanik analizi, üç ölçülü
düzeltmenin aktif oyuncuya uygulanması, iki varsayımın yazmadan elenmesi, bir değişikliğin etkisiz çıktığı için geri alınması,
deformasyon katmanı denetimi ve gerçek kare süresi ölçümü. Kadın hareket içeriği, yeni fiziksel tepkiler, yumuşak doku, cilt,
kıyafet ve ışık koşulları **yapılmadı** (bölüm 7). Hiçbir başlık USER_ACCEPTED değildir.

Durum etiketleri: IMPLEMENTED · TECH_TESTED (oyun içinde ölçüldü) · VISUALLY_INSPECTED (kareleri inceledim) · PERFORMANCE_TESTED ·
USER_ACCEPTED. Ölçümler aktif `BP_HybridA_Player` üzerinde, PIE içinde, gerçek tuş girdisiyle, 30 Hz sabit adımda alındı
(kare süresi ayrı, gerçek zamanlı ölçüldü). Kullanıcı kaydı (SFSaveSlot, SHA1 4823d83a…) her batch'te kenara alınıp geri kondu.

---

## 1. Önceki düzeltmelerin durumu

- Boyun düzeltmesi korunuyor: bu turun değişikliklerinden sonra boyun eğimi, baş-köprücük ve göğüs ölçüleri aynı
  (bekleme 10,7° → 10,8°, yürüyüş 18,2° → 18,5°, jog 19,3° → 19,6°, çömelik idle 30,1° → 30,6°; baş-köprücük farkı ≤ 0,1 cm).
- Yeni sabit açı eklenmedi; `ABP_Sph_Body_GASP` ve `AC_Sph_Motion` bu turda değişmedi.
- Yüz / saç sınır kutusu düzeltmesi yerinde: odun alma kaydında baş her karede çiziliyor.

## 2. Biyomekanik analiz — sorulara ölçülmüş cevaplar

Araçlar: `Tools/Bio_20261115/an_bio.py` (döngü), `an_events.py` (olay), `an_leg.py` (sürücü / görünür bacak). Veriler `data/`.

| Soru | Ölçüm (düzeltmelerden önce) | Değerlendirme |
|---|---|---|
| Yürümeden önce ağırlık hangi ayağa? | Sağ ayak ilk kalkıyor (0,22 sn); pelvis sol destek ayağına 3,6 cm kayıyor (ayak 16,8 cm yanda), en çok 0,3–0,4 sn'de | Aktarım var ama küçük ve kapsül hızlanmasından geç: kapsül 0,3 sn'de tam hızdaydı |
| İlk itiş ve sonraki basış sıralı mı? | Sağ kalkış 0,22 sn → sol kalkış 0,53 sn; yürüyüşte basan ayak kayması ort. 4 cm/sn | Sıralı; yürüyüşte temas temiz |
| Pelvis–göğüs karşı hareketi | Yürüyüş: pelvis 17°, göğüs 15°, karşı faz (korelasyon −0,5); jog: pelvis 17°, göğüs 38°, **aynı faz** (+0,92); sprint: 29° / 44° | Yürüyüşte doğal; jog'da gövde pelvisle birlikte dönüyor (klibin kendisi) → açık bulgu |
| Koşuya geçiş hazırlığı | Jog: uçuş oranı 0,59, kadans ~167, adım 138 cm; sprint: uçuş 0,74 | Jog gerçek koşu döngüsü (uçuş evresi var), hızlı yürüyüş değil |
| Frende yükü hangi bacak alıyor? | Sprintten: sağ 0,33 sn'de pelvisin altına, sol 0,42 sn'de 68 cm öne; 0,85 sn / 264 cm'de duruş; **pelvis 30 cm çöküyor, dizler 53–58°** | Sıra doğru ama derinlik atletik bir "lunge". Klibin kendi kök hareketi 0,75 sn'de duruyor → animasyondan geliyor (açık bulgu) |
| Dönüşte ayak mı, kapsül mü? | 60°/sn yürüyüş dönüşünde basan ayak yerdeyken 13–36° dönüyor (top noktası 1–2 cm oynuyor) | **Kusur:** ayak top üzerinde kapsülle dönüyor. Bu turda çözülemedi (bölüm 4) |
| Eğilmede yalnız omurga mı? | Odun alma en derin an: kalça 67–71°, diz 61–65°, omurga katlanması 12°, pelvis 93 → 48 cm, ayaklar 50 cm açık | **Doğru:** kalça + dizle çömelerek kaldırma. Boyundaki 81° = gövde 39–47° + nesneye bakış |
| Kollar hareketle ilişkili mi? | Kol–karşı bacak korelasyonu yürüyüş +0,96 / +0,98, jog +0,80 / +0,59; yürüyüşte sol el 45 cm, sağ el 24 cm sallanıyor | Çapraz eşleşme doğru; yürüyüşte **sol/sağ salınım asimetrik** (açık bulgu) |
| Boyun başı doğal taşıyor mu? | Bölüm 1 | Evet, önceki düzeltme geçerli |

Ek bulgular:
- **Beklemede ayak arası 34 cm**, kalça eklemi arası 19 cm (geniş duruş, kaynak klipten).
- **Yürüyüşte pelvis 9,8 cm inip kalkıyor**, pelvis yatması 11,8° (kaynak klibin "rahat" karakteri; kadın yürüyüşü normlarının üstünde).
- **Çömelik yürüyüş** 225 cm/sn (ayakta yürüyüş 165'ten hızlı), gövde 46–51° eğik.

## 3. Uygulanan düzeltmeler (`changes/degisiklik_manifesti.md`)

Üçü de mevcut sahibin mevcut değerini değiştirir; yeni düğüm, katman, IK çözümü veya sistem yok.

| # | Sahip | Değişiklik | Ölçülen neden | Sonuç (önce → sonra) | Durum |
|---|---|---|---|---|---|
| 1 | `RTG_Sph_UEFN_to_MH` Pelvis Motion | pelvis dikey ofseti 1,0 → 2,4 cm | Görünen bacak 87,6 cm, sürücününki 81,6 cm; görünen diz kaynağınki kadar açılamıyordu | Bekleme dizi 156° → **167°** (sürücü 162°); yürüyüşte topuk basışı 159° → **170°** (sürücü 168°); jog 151° → 158° (sürücü 159°). Bacak açıklık oranı en çok 0,996: aşırı gerilme yok | IMPLEMENTED, TECH_TESTED, VISUALLY_INSPECTED |
| 2 | `BP_Sph_GASPCharacter` CalculateMaxAcceleration | yürüme ivmesi 800 → 500 | Kapsül 0,3 sn'de 165 cm/sn'ye çıkıyordu; ilk ayak 0,22 sn'de kalkıyor, klibin kendi kalkışı ~0,55 sn | Hız profili 54 / 130 / 165 → 32 / 82 / 131 / 160 cm/sn (0,1 sn aralıklarla); tam hız ~0,45 sn. Jog ve sprint ivmesi aynı | IMPLEMENTED, TECH_TESTED |
| 3 | `BP_Sph_GASPCharacter` + `BP_HybridA_Player` CrouchSpeeds | 225 / 200 / 180 → 165 / 150 / 140 (ileri / yan / geri) | Çömelik yürüyüş ayakta yürüyüşten hızlıydı | İleri 215 → 165, geri 170 → 140 cm/sn; aynı klipler, basan ayak kayması aynı (4–7 cm/sn) | IMPLEMENTED, TECH_TESTED. Gövde eğimi değişmedi → PARTIAL |

Yürüyüş, jog ve sprint döngülerinde adım, kadans, ayak kayması, pelvis ve kol ölçüleri düzeltme 1'den sonra aynı
(`data/yuruyus_kosu_dongu_olcumleri.txt`): yalnız diz açıklığı değişti.

## 4. Elenen varsayımlar ve geri alınan değişiklik

| Aday | Nasıl sınandı | Sonuç |
|---|---|---|
| "Adım bacağa göre fazla uzun; sürücüyü ve hızları 0,944 ölçekle" | Çalışma anında, varlık yazılmadan | **Reddedildi.** Öncül yanlıştı: iskelet varlığının referans pozu 77 cm gösteriyor ama mesh'in gerçek bacağı 87,6 cm. Sondada adım aynı kaldı, kadans 116 → 106 düştü (ağır çekim yönü) |
| "Kurulu Relaxed çömelme klipleri daha dik" | Klip pozları ölçüldü + çalışma anında hız 165 / 140 | **Reddedildi.** Relaxed ve Neutral çömelik yürüyüş aynı duruş (gövde 46°, baş 102 cm); yalnız tempo farklı. Relaxed klipler veritabanlarında yok |
| Ayak yerleşimi kilidi: top üzerinde dönme → yön kilidi (35°) | Yazıldı, kayıt alındı | **Geri alındı** (manifest `day_bio_revert2_111014`): basan ayak dönüşte yine 15–27° döndü. Kusur duruyor; sahibi henüz bulunmadı |

## 5. Deformasyon katmanı ve performans denetimi

- **Beden düzelticileri etkin:** `ABP_Body_PostProcess` kapatılınca 76 yardımcı kemiğin (twist / corrective) 76'sı ana
  kemiğine göre 16–25° ve 3–5 cm kayıyor; LOD 0, zorlanmış LOD yok (`data/beden_duzeltici_kemik_denetimi.txt`). İkinci ölçüm
  pozu çömelme olarak planlanmıştı ama karakter ayaktaydı; çömelik pozda ayrı ölçüm yok.
- **Beden mesh'inde morph hedefi yok** (0 adet), tek malzeme `MI_Body_Baked_VT`. GD40–GD44 anatomik adayları üretim bedeninde
  (SKM_MHC_Sph8_BodyMesh) uygulanmış değil; bu turda yeniden değerlendirilmedi.
- **Gerçek kare süresi** (gerçek harita, gerçek zamanlı, editör içi PIE; idle → yürüyüş → jog → sprint → duruş, 418 kare):
  kare süresi p50 52 ms (ort. 17,9 FPS), GPU p50 51 ms, bunun 36 ms'si gölge derinliği (ShadowDepths); oyun iş parçacığı
  p50 15,7 ms, animasyon 0,83 ms. Bu turun değişiklikleri düğüm veya tick eklemiyor. Editör içi PIE'de GPU süresi yeniden
  başlatmalar arasında çok oynuyor (önceki raporda aynı durumda 19 ve 38 ms); bu ölçüm paketlenmiş oyunun FPS'i değildir.
  Önce / sonra karşılaştırması yapılmadı → PERFORMANCE_TESTED yalnız "mutlak ölçüm" anlamında.

## 6. Doğrulama

- Editör yeniden başlatıldıktan sonra kaydedilen değerlerle: düz haritada üç plan (yürüyüş / jog / sprint / fren; dönüş /
  çömelme / zıplama; çömelik ileri / geri / yan) ve gerçek haritada odun alma + taşıma.
- Odun alma düzeltmelerden sonra aynı: en derin an kalça 68–72°, diz 63–67°, pelvis 49 cm; kalkışta diz 159–170° (önce 151–159°).
- Görseller: `evidence/sonra_tam_beden_*.jpg` (bekleme, yürüyüş, jog, sprint, fren, geri, çömelik yürüyüş, zıplama),
  `evidence/once_ust_sonra_alt_kalca_diz_*.jpg`. Videolar: `videos/` (tam beden yan 30 Hz; kalça-diz önce / sonra; odun alma).
- **Denenmedi:** 60 Hz tekrar, gerçek haritada yürüyüş / jog / sprint videosu, eğimli zemin, 45° / 90° / 180° dönüşlerin gait
  bazında ayrı incelenmesi, kapı / çay / şömine / maske / balta akışları, kayıt-yükleme, gamepad, aşma (vault).
- Bilinen risk: pelvis 1,4 cm yükseldiği için oturma, yatak ve diz çökme gibi montajlarda temas noktaları ayrıca kontrol edilmeli.

## 7. Raporun sonunda istenen cevaplar

- **Daha doğal hâle gelenler:** bekleme ve yürüyüşte diz açıklığı (sürekli çökük diz kalktı), yürüyüşe başlama zamanlaması,
  çömelik yürüyüş temposu.
- **Değişen anatomik katmanlar:** yalnız retarget (pelvis yüksekliği) ve iki hareket parametresi. Duruş / boyun / kol katmanlarına dokunulmadı.
- **Ayak teması, ağırlık aktarımı, denge:** ölçüldü; yürüyüşte temas temiz (4 cm/sn), jog'da 11 cm/sn. Ağırlık aktarımı ve
  denge için yeni çözüm **eklenmedi**; yalnız kalkışta kapsül bedenin önüne geçmiyor.
- **Eklenen fiziksel tepkiler:** yok. Mevcut olanlar (fren, yorgunluk nefesi, iniş, iki elle yük) yeniden ayarlanmadı.
- **Animasyondan gelenler:** adım, kadans, pelvis hareketi, kol salınımı, fren ve çömelme pozları. **Prosedürel olanlar:**
  retarget pelvis ofseti, mevcut duruş / boyun katmanı, ayak yerleşimi, kök ofseti.
- **Hâlâ yapay olanlar:** dönüşte ayağın yerde dönmesi; sprintten duruşta derin çöküş; çömelik yürüyüşte 46–51° gövde;
  jog'da pelvis–göğüs aynı fazda; yürüyüşte geniş duruş, 10 cm pelvis salınımı ve asimetrik kol; S ile geri yürüyüşte kalça sapması.
- **Yapılmayan bölümler:** kadın performansına uygun kaynak içerik karşılaştırması; eğimli zemin; fiziksel tepki adayları
  (Physics Control vb.); yumuşak doku; cilt malzemesi; kıyafet oturması ve Chaos Cloth; saç tepkisi; ev içi / gölge ışık
  koşulları; kamera ilişkisi; kaynak → retarget → duruş → yeni aşamalarının yan yana videosu.
- **Kullanıcı kabulü:** yok.

## 8. Geri alma

- Manifest `day_bio_apply1_103307` (4 varlık) ve `day_bio_revert2_111014`; ek kopya `%USERPROFILE%\SphirusCheckpoints\Bio_Pre_20261115\` (6 varlık + sha1.txt).
- Değer düzeyinde: pelvis ofseti 2,4 → 1,0; yürüme ivmesi 500 → 800; CrouchSpeeds 165 / 150 / 140 → 225 / 200 / 180.
