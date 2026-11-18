# SPHIRUS UE 5.9 — tam beden / kalça turu (2026-11-17)

Çalışma kopyası: `Documents\Unreal Projects\sphirus_UE59` (UE 5.9.0, CL 60351404). Orijinal 5.8.4 projesine dokunulmadı.
Önceki aşama raporları: `Saved/UE59Work/reports/sphirus-ue59-tam-beden-2026-11-16/` (faz0–faz3_4).

Durum etiketleri: IMPLEMENTED / TECH_TESTED / VISUALLY_INSPECTED / PERFORMANCE_TESTED / NOT_TESTED. **USER_ACCEPTED hiçbir madde için yok.**
Videoların hiçbiri benim tarafımdan gerçek hızda izlenmedi; görsel kabul kullanıcıda.

## Aktif oyuncuda kalıcı olan durum

| Alan | Değer | Durum |
|---|---|---|
| Profil | C: yürüyüş ve jog Normal (Neutral) aile; sprint, duruş, iniş, çömelme Relaxed | IMPLEMENTED, TECH_TESTED |
| Düz gidiş veritabanları | Yalnız ileri klipler: `PSD_Sph_N_{Walk,Run}_F_{Loops,Turns,Pivots,Starts}` (fwd=3); jog dönüş/pivotları Relaxed | IMPLEMENTED, TECH_TESTED |
| Hızlar | yürüyüş 180/170/150, jog **415**/350/300, sprint 585 | IMPLEMENTED, TECH_TESTED |
| Ayak kilidi | `PivotAroundBall` (LockRotation denemesi geri alındı) | TECH_TESTED |

Geri dönüş (her biri yeni manifestle `w_profile.py`): jog 430 → `run_speed` alanını kaldır; eski C → `"fwd":0`; A → `{"profile":"A","plant":"PivotAroundBall"}`.
Manifestler `changes/` altında.

## Kalça gözlemi (dönüşte fazla salınım)

- **45°/90° yürüyüş dönüşü:** kalça yanal sapması düz yürüyüşün 1,0–1,3 katı (3,6–4,8 cm; düz ±3,6), çökme 5–7 cm. Fazla salınım ölçülmüyor.
- **90° jog dönüşü:** kalça çerçevesinde yanal 2,8–6,4 cm (düz 3,1). Eski C'de 7,8–9,1 cm idi; ileri-yalnız veritabanları bunu düşürdü.
  Kapsül çerçevesindeki 15–17 cm değeri ölçüm yanılgısı: pelvis jog'da kapsül merkezinin ~13,6 cm gerisinde ve kapsül anında dönüyor.
- **135°/180° jog:** 7,4–14,6 cm, yerleşme 0,6–1,6 s, çökme 16–21 cm. Pivot kliplerinin kendisi; A profiliyle aynı düzeyde. Değiştirilmedi.
- **Yürüyüş sola 180°** (`M_Neutral_Walk_Turn_L_180_Lfoot`): yanal 12,4 cm, ayak kayması 85 cm/s. **Çözülmedi.**
- Korunan: yön değişimi, karşı ağırlık tepkisi (göğüs–pelvis karşı faz −0,35 / −0,40).
- Sinüs, sabit açı, pelvis ofseti, girdi yumuşatma eklenmedi.

Veri: `data/turn_hip_v5.txt`, `data/turn_hipframe_v5.txt`. Video: `videos/turn_walk_…mp4`, `videos/turn_jog_…mp4` (sol önce, sağ sonra).

## Jog duruşu düzeltmesi

- Sorun: jog 430'da duruş `M_Relaxed_Sprint_Stop` klibini seçiyordu; pelvis 32 cm çöküyordu.
- Aday E (sprint+koşu birleşik duruş veritabanı): FAILED, **REVERTED** (veritabanı silindi).
- Çözüm: jog 415. Duruş artık `M_Neutral_Run_Stop_F`; çöküş 14–17 cm. Kısa tuş bırakmada da koşu duruşu.
- Bedeli: jog 15 cm/s yavaşladı. Jog ayak kayması 9,7 cm/s (430'da 10,6).
- Veri: `data/clips_stop_brake.txt`. Video: `videos/stop_jog_before430_after415.mp4`.

## Kayıtlı oyuncuda doğrulama (v5 dizisi)

| Test | Sonuç |
|---|---|
| Yürüyüş 180: kadans 115, adım 100 cm, kayma 5,0 cm/s, kol 36,4/40,4 | PASS (teknik) |
| Jog 415: kadans 161, kayma 9,7, gövde 20,7° | PASS (teknik) |
| Sprint 585 Relaxed; sprint duruşu pelvis hareketi 36,5 cm | Değişmedi; derin çöküş açık |
| Geri / çapraz geri yürüyüş, S ile geri adım, W dokunuşları | PASS (işlevsel) |
| Zıplama (tepe 59–65 cm, havada 0,60–0,63 s), çömelme A ile klip klip aynı | PASS (önceki koşu) |
| Odun al → kes → 2 parça topla → arka kapı → şömineye diz → yak | **PASS** (`data/wood_route_v5.txt`) |
| Kayıt yükle → 2 parça geri geldi → diz → yak | **PASS** (`data/wood_loadfire_v6.txt`) |
| Odunsuz şömine: reddetti, durum değişmedi | PASS |
| Performans, ev haritası oyun kamerası | 36,1 fps; kare p50 28,2 / p99 31,5 ms; GPU 27,2 ms; 50 ms üstü kare 0 (PERFORMANCE_TESTED) |
| Kapı (arka mutfak kapısı rota içinde geçildi), maske, çay, yatak | Ayrı test edilmedi: NOT_TESTED |

Not: ilk kayıt-yükleme koşusu geçersizdi (test kaydını saklayan klasör kopyada yoktu); klasör açılıp yeniden koşuldu.
Performans için aynı koşulda 5.8.4 karşılaştırması bu turda alınmadı; GPU sınırlı.

## Açık bulgular

1. **Ciltte beyaz lekeler (iç mekân):** omuz, üst kol ve ön kolda beyaza kırpılmış lekeler. 15 Kasım 5.8.4 karesinde de var; 5.9 kaynaklı değil.
   Teşhis (yalnız çalışma anı konsol değişkenleri): SSS kapalıyken de duruyor; yalnız ışık görünümünde tişört normal, cilt lekeli.
   Yani ekran-uzayı SSS değil; cilde özgü (cilt malzemesi ya da yalnız karaktere vuran bir ışık). Sahip kesinleşmedi, **düzeltme uygulanmadı**.
   Kanıt: `evidence/indoor_q34_body.png`, `evidence/skin_dx_*.png`.
2. **Eğim:** 18–25° yokuşta pelvis yüksekliği ~85 → 63–67 cm, gövde öne eğilmiyor. A'da da aynı; bu turun değişikliğinden değil. Çözülmedi.
3. **Yürüyüş sola 180°** kalıntısı (yukarıda).
4. **Sprint 90° dönüş ve sprint duruşu:** çöküş 13–19 cm / 32–36 cm; Relaxed klipler, değiştirilmedi.
5. `turn_sev` sinyali yürüyüş/jog'da en çok 0,21; dönüş şiddetini eksik bildiriyor. Teşhis edilmedi.
6. Dönüş hızına bağlı ayak kilidi adayı: uygulanmadı (5.9'da Blueprint grafik yardımcıları çalışmıyor).

## Aşama C–D (ağırlık, anatomi, saç, kumaş, cilt)

- Saç fiziği, kumaş simülasyonu, ML Deformer adayları **üretilmedi**. Neden: oyun zaten GPU sınırlı 36 fps; ML Deformer için eğitim verisi yok;
  önce cilt lekesi ve eğim gibi temel kusurlar geliyor. Ertelendi, düşürülmedi.
- Üç ışık koşulunda 15 kare alındı (`Saved/Codex/Bio_20261115/look_v5/`); beş tanesi ve iç mekân karşılaştırması incelendi (VISUALLY_INSPECTED, kare düzeyi).
  Orman ve gün ışığı karelerinde yakalama biçimi renk bantlı çıktı; bu kareler saç/cilt kalitesi yargısı için güvenilir değil.

## 5.9 araçları

| Araç | Durum bu derlemede | Karar |
|---|---|---|
| Motion Matching / Pose Search, Chooser | Çalışıyor | Kullanıldı (yeni veritabanları, eşleme) |
| Foot Placement plant ayarları | Çalışıyor | Sahip bulundu; LockRotation geri alındı |
| IK Retargeter Proximity IK / Pelvis Volume / Limb Twist | Yok | Kullanılamadı |
| MCP (ModelContextProtocol) | Editör açıkken yerel istemciyle çalışıyor; oturum bağlayıcısı bağlanamadı | Tanı için kullanıldı |
| ML Deformer, Chaos Flesh | Motorda var, projede kapalı | Uygulanmadı (veri yok) |
| Python ile Blueprint kök değişimi, betikle Deformer Graph, Dataflow seçenek pini | Bilinen çökme riskleri | Kaçınıldı |

## Güvenlik doğrulaması

- Orijinal 5.8.4: 1149/1149 dosya taban SHA1 listesiyle aynı.
- Test kaydı her koşudan sonra SHA1 4823d83a…; kullanıcının asıl kaydı değişmedi.
- Kilit serbest; bu turda git, yayın ya da dışa gönderim yapılmadı.
- Skill'lerin "Verified" bölümleri bu turda güncellenmedi.

## Ek (aynı gün): ciltteki beyaz lekelerin sahibi

Yalnız okuma ve çalışma anı denemeleri yapıldı; hiçbir varlık, harita ya da kayıt değişmedi.

| Deneme | Sonuç |
|---|---|
| Yalnız karaktere vuran ışık var mı | Yok; bütün ışıklar ve karakter parçaları kanal 0 |
| Cilt malzemesi parametreleri (renk çarpanı 1, specular 0, mikro maske 0, pürüzlülük +0,3) | Lekeler aynı |
| Ekran-uzayı SSS kapalı, güneşte ışık geçirgenliği (zaten kapalı) | Lekeler aynı |
| Beden düz gri motor malzemesiyle | Lekeler aynı → **malzeme değil** |
| Güneş (DirectionalLight_0, 1250) kapalı | Lekeler **kayboldu** |
| Poz değişince | Leke tişörte ve duvara da düşüyor |
| Yerel pozlama vurgu kontrastı 0,7 / 0,5 (çalışma anı) | Lekeler aynı; kırpma aralığın çok dışında |

**Sonuç:** kusur karakterde değil. Pencereden giren doğrudan güneş lekesi, iç mekân pozlamasında tam beyaza kırpılıyor; gürültülü kenar gölge yarı gölgesi.
Sahip: ev haritasının ışık/pozlama kurulumu (`L_GR_SphirusHouse`: güneş şiddeti, `PostProcessVolume_0` pozlaması). Bu, korunan ev sahnesi ve XR5 atmosferi olduğu için **düzeltme uygulanmadı**; karar kullanıcıda.
Kanıt: `evidence/skin_owner_sun_off_plain_material.jpg`, `evidence/skin_material_param_test.jpg`, `evidence/skin_highlight_contrast_test.jpg`; veri: `data/skin_probe.txt`, `data/ppv.txt`.
