# Sphirus: hareket gerilemesini geri al, beden tepkilerini geri kazan (2026-11-11)

Uygulama: 2026-11-11 13:50 – 19:40 (UE 5.8.4, `sphirus.uproject`, harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse`).
Önceki tur: [Core Motion kadın hareketi raporu](../sphirus-dogal-kadin-hareketi-2026-11-11/README.md) — bu raporla birlikte **REJECTED_REGRESSION** olarak işaretlendi.

Durum etiketleri: **IMPLEMENTED** (projede, kayıtlı) · **TECH_TESTED** (oyunda ölçüldü) · **VISUALLY_INSPECTED** (benim kare/video incelemem) · **USER_ACCEPTED** (yok — kullanıcı henüz oynamadı) · **PARTIAL** · **NOT_TESTED** · **REJECTED** (denendi, terfi etmedi).

## Başlık soruları

| Soru | Cevap |
|---|---|
| **Ne geri alındı?** | Core Motion adayı C'nin tamamı, editör üzerinden (dosya kopyası değil, `r1_profile.py`): `ABP_Sph_GASP.SphCM` True→**False** (Core Motion veritabanı eşlemesi devre dışı); Motion Matching PlayRate 0,80–1,05 → **0,85–1,15**; ivme 350/420/450→350 → **800/800/800→300**; hız 160/290/500 → **165/375/585** (oyuncu + GASP karakteri); ev içi ölçek 0,9375 → **0,9091** (=150 cm/s); fren 260/520 → **380/780** (CDO + iki şablon); bekleme kırılmaları CM af_Stand_Idle → **Relaxed Idle_Break v01/02/03/05/07**. |
| **Ne tutuldu?** | `MovementDirection_Recent` düzeltmesi (seçim tablosu girdisi, uyumlu); baş/beden/saç/kıyafet, kamera, Story Framework, kapılar, görevler, envanter, ev etkileşimleri dokunulmadı. Core Motion varlıkları diskte duruyor, kullanılmıyor. AAMS veya ikinci denetleyici yok. |
| **Hangi tepki önceden vardı ve kayboldu?** | Aynı girdi ve kamerayla (A = C'den önceki Relaxed, C = reddedilen): sprintte pelvis–göğüs karşı dönüşü **53° → 35°**, pelvis inip kalkması **15 → 6,6 cm**, gövde öne eğimi **35° → 24°**, sprintten duruşta yan beden tepkisi **26° → 7°**, fiziksel duruşta geri tepki **−32° → −16°**, yan tepki **35° → −6°**; yürüyüşte pelvis inip kalkması **9 → 5,5 cm**. Yürüyüşte C gövdeyi sürekli öne kilitliyordu (eğim 3° → 7°): "kalas" görüntüsü = daha az karşı dönüş + daha az inip kalkma + sabit öne eğim. |
| **Nerede kayboldu?** | **Kaynak kliplerde ve düşürülen hızda.** Sürücü (GASP UEFN iskeleti) ile görünen MetaHuman aynı karelerde ±1–2° aynı (`data/katman_surucu_gorunen.txt`): retarget, görünen beden ABP'si, SHME nefes/settle katmanı tepkiyi kesmiyor. Aynı grafikle R, A'yı birebir veriyor; yani kayıp, Core Motion klip içeriği ve onunla gelen daha yavaş hız/ivme. |
| **Nasıl geri kazanıldı?** | Relaxed ailesi kendi uyumlu ayarlarıyla geri kuruldu (R) ve aynı plandaki A kayıtlarıyla doğrulandı: klip dizileri birebir aynı, beden ölçüleri 1 birim içinde (§2). Sonra tek sınırlı düzeltme: **sprint kilidi** (§4). |
| **Hangi aile aktif?** | **GASP Relaxed** (UEFN Relaxed klipleri → `RTG_Sph_UEFN_to_MH` → MetaHuman), seçim tablosu `CHT_Sph_PoseSearchDatabases_Relaxed`, SHME katmanı açık (settle, göğüs önü, efor, fiziksel fren). |
| **Ne hâlâ açık?** | Fareyle hızlı dönüşte ayak kayması; sprint geri dönüşünün itiş adımında kalan kayma; yürüyüşte 180° dönüş klibinde kayma; tempo kalibrasyonu; kadın omuz/duruş inceltmesi; kullanıcının oyunda kabulü (§6). |

## 1. Güvenlik

- Kontrol noktası: `C:\Users\berat\SphirusCheckpoints\MotionRestore_Pre_20261111_1353` (+ `_sha1.txt`, 273 dosya: Content/Sphirus/Player, Hazel Playable, Config, uproject, kayıt kopyası).
- Her yazma kapılı runner ile, yazma manifesti + doğrulanmış yedekle: `day_mr_r1_135626`, `day_mr_m1rev_152713`, `day_mr_g1_162707`, `day_mr_m2rev_162912`, `day_mr_m3cap_171736`.
- Kullanıcı kaydı `SFSaveSlot.sav` başta ve sonda `8622025b…`. Her test kaydı kenara alıp geri koydu; eski bir kayıt üzerine yazılmadı.
- İki editör çökmesi (15:12, 16:12) oldu. İkisi de Blueprint grafiği okuyan bir işten sonra, editör yeniden başlatılmadan aynı editörde yeni iş çalışırken yaşandı. Hiçbir varlık yazılmadı (dosya tarihleri değişmedi). Sonrasında her grafik işinden önce editör yeniden başlatıldı.

## 2. C ile geri getirilen R: aynı MetaHuman, kamera, rota, girdi

Tam tablolar `data/tepki_A_C_R.md` dosyasında (A = C öncesi Relaxed referansı, C = reddedilen, R = geri getirilen; F1 = son üretim). Özet:

| Ölçü (aynı plan) | A | C | R | Son (F1) |
|---|---|---|---|---|
| Sprint pelvis–göğüs karşı dönüş (°) | 53,1 | 35,0 | 52,1 | — |
| Sprint pelvis inip kalkma (cm) | 15,1 | 6,6 | 15,0 | — |
| Sprint gövde öne eğim (°) | 34,6 | 24,3 | 34,5 | — |
| 20 s koşu karşı dönüş / eğim (°) | 49,4 / 26,4 | 36,4 / 23,3 | 49,2 / 26,3 | 49,0 / 26,3 |
| Sprintten duruş, yan tepki (°) | −26,5 | −7,0 | −25,5 | −30,0 (20 s koşu) |
| Fiziksel duruş, geri / yan tepki (°) | −31,7 / 34,8 | −16,3 / −6,2 | −30,3 / 32,7 | — |
| Yürüyüş pelvis inip kalkma (cm) | 9,1 | 5,5 | 9,0 | — |
| Yürüyüş gövde eğimi (°) | 3,2 | 7,3 | 3,1 | — |
| Yürüyüş 30 s temas kayması p50/p90 (cm) | 3,0 / 4,7 | 1,8 / 4,2 | 2,8 / 4,1 | — |

İstenen olaylar:

- **Kalkış hazırlığı.** R/A'da `Walk_Start_F → Run_Start_F → Transition_Run_to_Sprint`. C'de düz hızlanmada `Run_Start_TurnR180/135` dönüş kalkışı oynuyordu. Bu, Relaxed'ın koşu→sprint geçiş veritabanının C'de karşılığı olmadığı için yön kalkışı veritabanına eşlenmesinden kaynaklanıyordu (C'ye özgü; R'de yok).
- **Koşuya girerken kalça/göğüs/kol.** Öne/geri tepki tepe değeri A 41,9° @0,6 s, C 36,4° @0,7 s, R 41,7° @0,6 s. Pelvis çökmesi A −16,9, C −10,2, R −16,9 cm.
- **Fren ayağının yüklenmesi ve duruştan sonra toparlanma.** Duruştaki yan ve geri beden tepkisi R'de geri geldi (tablo). C'de duruş yavaş ve dikti.
- **90/180 gövde yönlendirmesi ve dönüş ortasında yeni komut.** §4.
- **Tempo kalibrasyonu.** Bu turda yapılmadı (§6). Karşılaştırmalar her adayın kendi uyumlu ayarlarıyla yapıldı; "daha hızlı = daha canlı" karışmasın diye beden ölçüleri hıza değil, aynı plandaki olaylara göre okundu.

Durum: R geri dönüşü **IMPLEMENTED, TECH_TESTED** (A ile birebir), **VISUALLY_INSPECTED** (kare tabloları). **USER_ACCEPTED değil.**

## 3. Katman denetimi (kaynak → sürücü → retarget → görünen → SHME)

| Katman | Gerçek çalışma durumu | Bulgu |
|---|---|---|
| Kaynak + Motion Matching | R: Relaxed veritabanları, PlayRate 0,85–1,15 | Kayıp burada: C'nin klipleri daha az karşı dönüş ve inip kalkma taşıyor. |
| GASP AnimGraph (yönelme bükmesi, steering, lean ek katmanı, OffsetRootBone, FootPlacement, LegIK) | Değiştirilmedi | Sürücü iskeletindeki ölçüler A ile R'de aynı. Bu turda düğüm düğüm kapatma deneyi yapılmadı, gerek görülmedi: A/R eşitliği ve sürücü = görünen eşitliği kaybın bu katmanlarda olmadığını gösteriyor. |
| Retarget `RTG_Sph_UEFN_to_MH` (köprücük −5°) | Değiştirilmedi | Sürücü/görünen farkı ±1–2°. |
| Görünen beden `ABP_Sph_Body_GASP` + SHME | `BodyOn`, `EffortEnabled`, `PhysBrake` açık; settle 4°, göğüs önü ≤9°, efor eğimi | Yaklaşık +1–2° öne eğim ekliyor. Kaynak tepkisini bastırmıyor, çift de saymıyor. |
| Hareket fiziği `AC_Sph_Motion` | Fren 380/780, SpeedScale (dönüş/ters istekte hız düşüşü), efor | §4: sert dönüşte asıl sorun burada değil, gait seçiminde çıktı. |

Destek aktarımı, fren sonrası oturma ve yeniden itiş için ayrı yeni katman eklenmedi. Bu turda kanıtlanan kayıp kaynaktaydı ve geri geldi. Sinüs salınımı eklenmedi.

## 4. Koşu ve dönüş toparlanması (ilk teslim)

**20 s kesintisiz koşu ve koşudan duruş** (`sonra_20s_kosu_durus.mp4`): `Walk_Start → Run_Start → Transition_Run_to_Sprint → Sprint_Loop`; koşu temasında kayma medyanı 2,8 cm, p90 4,8 cm; duruş `Sprint_Stop_F`, yan beden tepkisi −30° @0,5 s. **TECH_TESTED, VISUALLY_INSPECTED.**

**Sert dönüşte parça yığılması: sahibi bulundu ve düzeltildi.**
- Belirti (A ve R'de de vardı): sprintte 135°/180° dönüş 0,8 s içinde 4–5 parçaya bölünüyordu: `Sprint_Turn_180 → Run_Turn_180 → Transition_Walk_to_Sprint → Sprint_Reface_Start_090`. Basan ayak her geçişte 50–72 cm kayıyordu.
- Kök neden: `BP_HybridA_Player` (eski GR kuralı) sprinti yalnız "Shift > 0,9 s basılı **ve** hız > 250 cm/s" iken tutuyordu. Frende hız 250'nin altına inince, Shift basılı olduğu halde gait SPRINT → RUN → SPRINT oluyordu. Bu da seçim tablosunun geçerli veritabanlarını sprint dönüşlerinden koşu dönüşlerine çevirip Motion Matching'i oynayan klipten koparıyordu.
- Düzeltme (`g1_sprintlatch.py`): 250 cm/s şartı artık yalnız sprinte **girişi** sınırlıyor; Shift basılı kaldıkça sprint kendini koruyor. Shift bırakılınca hemen biter.
- Sonuç: her sprint geri dönüşü **tek klip**. `Sprint_Turn_180` fren–yüklen–dön–it akışını baştan sona oynuyor (`evidence/sprint180_kilitsiz_ust_kilitli_alt.png`, `ara_R_*` ve `sonra_*` videoları).

| Aynı plan | Kilitsiz (R1/M0) | Kilitli (G0) | Son üretim (F1) |
|---|---|---|---|
| Yan kamera sprint dönüşleri: toplam kayma / >30 cm temas | 557 cm / 10 | 489 / 6 | 493 / 6 |
| Oyun kamerası sprint dönüşleri | 660 / 8 | 500 / 6 | — |
| 4 art arda sprint geri dönüşü (tüm kayıt) | 1657 / 16 | 906 / 8 | 1100 / 9 |
| Sprint geri dönüşü başına klip sayısı | 4–5 | 1 | 1 |

Durum: **IMPLEMENTED, TECH_TESTED, VISUALLY_INSPECTED**; kayma azaldı ama bitmedi → **PARTIAL**.

**Denenip terfi etmeyen iki aday** (grafikte duruyor, bayrakları kapalı, sonuçsuz):
- `RevOn` (geri dönüşte hız vektörü yay çizmesin, klibin ölçülen ~1800 cm/s² freniyle çizgide fren). İlk sürümde fren klipten hızlı çıktı ve kapı 120 cm/s'te kapanınca yay sürdü. İkinci sürümde efon toplamı 906 → 710 düştü, ama dönüş testlerinde 489 → 518 ve 500 → 540'a çıktı. Net fayda yok. **REJECTED.**
- `TurnCapOn` (fare dönüşünde yanal ivme sınırıyla hız düşüşü). Hız 165 → 150'ye düştü, fare testinde kayma 592 → 768 cm arttı. **REJECTED.**

İkisi de kapalıyken matematik birebir eski hâl: fren `max(500, 0)`, sürtünme `×1`, hız `min(v, 100000)`.

**Fareyle yön değişimi** (`sonra_fare_donusleri.mp4`): 360°/s fare dönüşünde kapsül 165 cm/s'i koruyup ~26 cm yarıçaplı yay çiziyor ve Motion Matching düz yürüyüş döngüsünde kalıyor. Basan ayak temas başına 41–77 cm kayıyor. **PARTIAL (açık).** Gerçek çözüm içerik veya seçim düzeyinde: döner yürüyüş/spin kliplerinin bu durumda seçilmesi. Sadece kapsül sınırı yetmedi.

## 5. Uygulama, temiz açılış, regresyon

| Kontrol | Sonuç | Durum |
|---|---|---|
| Temiz yeniden açılış | 5 BP `UP_TO_DATE`; `SphCM=False`, `SphRelaxed=True`, `MovementDirection_Recent` var; hız 165/375/585 (oyuncu + GASP karakteri); fren 380/780; bekleme Relaxed v01; şablonlarda `RevOn=False`, `TurnCapOn=False`; açılış günlüğünde yalnız motorun kendi test/DLL satırları | TECH_TESTED |
| GameMode | Proje varsayılanı `BP_GM_GR_GraceRanger` → `BP_HybridA_Player_C`; haritada GameMode geçersiz kılma yok | TECH_TESTED |
| Kayıt/yükleme (gerçek ev haritası) | Tek piyon (`ABP_Sph_GASP` sürücü + `ABP_Sph_Body_GASP` beden); kaydet → 7 m ışınla → yükle → kaydedilen noktaya döndü, sonra 165 cm/s yürüdü; kullanıcı kaydı geri kondu | TECH_TESTED |
| Kapı (E) | Hedef `GR_Day_WardDoor`, `AM_GR_Day_Reach`, geçiş | TECH_TESTED |
| Mutfak kapısından çıkış/giriş | Çıktı (z 238 → 168), bahçede sprint, durdu, döndü, içeri girdi | TECH_TESTED |
| Odun al–taşı–kes | `AM_GR_Day_Pick → CarryArms → Chop` | TECH_TESTED |
| Koridor | Ev içi 150 cm/s; Shift ev içinde sprint açmıyor; kamera çarpışma düzeltmesi çalışıyor | TECH_TESTED |
| Yatak | E ile uzanma (`AM_Sph_Bed`), sol tıkla kalkış, yürüyüş | TECH_TESTED |
| Zıplama (yürürken, sprintte) | Kalkış → havada → hafif iniş → döngü | TECH_TESTED |
| Kamera | Aynı GR kamera, kol 83,8–90,8 cm; davranış değiştirilmedi | TECH_TESTED (değişiklik yok) |

Gerçek hızda önce/sonra videoları `videos/` içinde: `once_C_*` = reddedilen C, `ara_R_*` = geri dönüş, sprint kilidi yok, `sonra_*` = son üretim.

## 6. Açık işler (dürüst liste)

1. **Kullanıcı kabulü yok.** Hiçbir şey USER_ACCEPTED değil; bu tur yalnız C'nin kaybettirdiği canlılığı geri getirdi.
2. **Tempo kalibrasyonu yapılmadı** (bu tur için "sonra" denmişti). Sakin tempo klip + adım + kadans + ivme + frenle birlikte ele alınmalı; global yavaşlatma yok.
3. **Kadın duruşu (omuz, kol taşıma) inceltmesi yapılmadı.** Relaxed'ın omuzları C'den daha önde (köprücük protraksiyonu +2…+10°); canlılığı öldürmeden ayrı bir iş.
4. **Sprint geri dönüşünde itiş adımı kayması** (47–130 cm, tek temas, kapsül klipten erken hızlanıyor). Yürüyüşte 180° dönüş klibinde 32–93 cm. Fare dönüşü §4.
5. **Sprint kilidinin kenar durumu.** Shift basılıyken bir duvara koşulursa gait düşük hızda sprint kalır. Test haritasında duvar yok, **NOT_TESTED**.
6. Cook/paket, gerçek GPU/CPU maliyeti, eğim/merdiven: **NOT_TESTED**.

## Dosyalar

- `data/tepki_A_C_R.md`: dört planda A/C/R beden tepki tabloları.
- `data/katman_surucu_gorunen.txt`: sürücü ve görünen beden aynı karelerde.
- `data/klip_dizileri.txt`: her kayıtta segment başına oynayan klipler.
- `data/temas_kayma.txt`: temas başına kayma, segment, hız, klip.
- `data/donus_klip_kok_egrileri.json`: Relaxed dönüş kliplerinin ölçülen kök hızı ve yönü.
- `evidence/`: kare tabloları.
- `changes/changes.md`: değişen varlıklar ve araçlar.
