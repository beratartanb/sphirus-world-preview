# SHME V2.21: hareket sürekliliği, araziye bedensel tepki ve yaşayan oynanış kamerası (2026-10-21/22)

**Taban:** V2.20 üretimi (commit `7e83941`). Motor UE 5.8, proje yalnız Blueprint, harita `L_GR_SphirusHouse`.

## Ölçüm düzeni

- **Nedensel kanıt: sabit adımlı editör** (`-UseFixedTimeStep -FPS=N`). Aynı ayar aynı santimi verir.
- **Dört yönlü karşılaştırma (30 FPS).** Rotalar: pilot rota, üç gerçek harita çizgisi (`map_r1..3`), tekil parkurlar.
  - **A:** üretim (V2.20).
  - **B:** beden + arazi açık, kamera taban.
  - **C:** kamera açık, beden taban.
  - **D:** hepsi açık (+ toparlama tutma).
- **Son durum.** Terfiden sonra editör kapatılıp açıldı, üretim doğrulaması çalıştırıldı. Ardından `fin` partisi koştu: `p` = kaydedilmiş V2.21 üretimi, `o` = aynı içerikte V2.21 kapalı.
- **FPS.** Sabit adım 20 / 30 / 60 / 120. Ayrıca gerçek zamanda değişken dt ve 0.08–0.20 s takılmalar.
  - Sabit adım ≠ üretim FPS bağımsızlığı. Takılma testleri bu yüzden gerçek zamanda yapıldı; gerçek zaman tekrarları gürültülü olduğu için tekrar sayısı verildi.
- **Ayak metriği** (`contact221`): ayak başına net kayma / sürükleme, gerçek zemine göre.
  - Bu sürümde kalibrasyon yalnız pencereden önceki satırlardan yapılıyor. V2.20'deki "sonraki olay önceki sayıyı değiştirir" tuzağı kapandı.
- **Pilot rota (`pilot`):** dokunuş → yürüyüş → tümsek → 10 cm eşik → 15 cm basamak + kenar düşüşü → 10° yan eğim (tempolu koşu) → depar → durma → depar → kesiş + ters → dinlenme.
- **Gerçek harita çizgileri.** `probe_route.py` gerçek çarpışmada küre süpürmesiyle buldu: evin yanında, 24 m açık, 76 / 223 / 125 cm kot farkı, ≤ 14°.
  - Her çizgide: dokunuş, yürüyüş, tempolu koşu, depar, durma, kamera 180°, geri depar, kesiş + ters.
- **Görsel inceleme.** Normal hızda GIF / AVI; ⅓ hız AVI yalnız destek. Görsel yorumlar teknik değerlendirmedir; **kullanıcının hareket üslubu / kontrol hissi kabulü verilmiş sayılmaz.**

---

## 1. ONARIMLAR

| Konu | Uygulanan | Ne zaman girer / çıkar | Önce → sonra | Doğrulandığı yer | Üretimde | Kalan hata | Geri alma |
|---|---|---|---|---|---|---|---|
| **A) `SHM213_MontTick` boş pawn okuması** | Hatanın sahibi eksik bir pawn değildi. DSL çevirisinde `TryGetPawnOwner` pawn'ı üzerinden yapılan `LastHitBy` okumasıydı. Düğümler `Pawn.GetController` ile değiştirildi (`fix_v221_lasthitby.py`). Yan bulgu: `camOK` kamera yönü yerine dünya X'ini kullanıyordu; bu da düzeldi | Her kare | PIE hatası 16/kare → **0**. `fin` partisinde tek bir Blueprint çalışma zamanı hatası yok | PIE, bütün partiler | **EVET** | Hataların takılmaları açıkladığı **iddia edilmiyor**. Editör hâlâ 38 GB'da her 3–4 QA koşusunda bir yeniden başlıyor (bellek davranışı değişmedi). Gerçek zaman pilotta ortalama kare süresi aynı (26 ms) | `checkpoint/baseline_v220/ABP_*` |
| **B) Toparlamada zaman geri sarması** | Motor kaynağı (`AnimNode_MotionMatching.cpp`, 5.8) okundu: düğüm `bShouldSearch` okumuyor. V2.20 kapısı bu yüzden ölüydü ve "arama değil" sonucu yanlıştı. Tek tutma yolu `ElapsedPoseSearchTime < SearchThrottleTime` (devam eden poz ilerleyebiliyorsa). `SearchThrottleTime = FMax(eski, Select(NOT SHM220_Search, 1.0, 0))`. Ardından **çıkış koruması:** `Search = önceki OR NOT SHM217_RecOn` | Toparlama klibi 0.08–0.62 s penceresindeyken. **Bırakma ve yeni yön aynı karede çıkar** (RecOn düşer, arama döner) | Gerçek zaman, fren duruşunda 0.15–0.18 s takılma: klip **geri sarması 4/12 → 0/12** (ilk parti). Tekrar partisinde 0.18 s takılmada **3/3 → 0/3** ve sol ayak 47–49 → 0.6–1.0 cm | Sabit 30: bırakma çıkışı R 18.5 = taban; yeni yön çıkışı = taban. Gerçek zaman 4 tekrar: bırakmada 3/4 tabana eşit. 1/4'te L 55: durma klibi adımın ortasından giriyor; tutma o karede açılmış, sahibi tutma değil | **EVET** (`SHM220_RecHold 1`) | Çok takılmalı (4 takılma) senaryoda geri sarma yok ama sürükleme gürültülü (her iki kolda da 2–69 cm) | `SHM220_RecHold 0` |
| **C) Kesiş → S pivotu frenini atlıyor** | (1) Pivot tutma (`SHM221_PivHold`): klip 0.13 → 0.80 atlamadan oynuyor. (2) Gerçek hat freni (pawn düğmeleri `GR215_RevBrake*`, giriş ivmesi bastırılmış): kapsül 242 → 27 cm/s sabit yönde duruyor | — | Pivot tutma: R 10 → 65 cm. Kapsül hızını *döndürüyor* (49 → 170°, 80–230 cm/s), hiç durmuyor. Hat freniyle: MM fren boyunca tempolu döngüyü çalıyor, pivota ancak basış karesinde giriyor: R 37–68. **İkisi de reddedildi** | k_cut_back, sabit 30 | **HAYIR** (düğmeler 0) | **AÇIK.** Geri koşu hızı 300 cm/s (tempo sınırı içinde). Eksik içerik aşağıda | — |
| **D1) Kesiş ortasında bırakma** | `GR220_StopFaceHoldMinErr` 45 → 20 / 10 | — | R 25.6 → 31.6 (kötüleşti) | chain_scutrel | HAYIR | **AÇIK** | — |
| **D2) TIP → W** | Ölçüldü | — | Erken W: L 7.8 / R 12.0. 180 → W: L 9.4 / R 6.9 (V2.20'deki 28 cm başka senaryoydu) | a_tipw, t_tipw_early, a_tipw180 | — | Değişiklik yok | — |
| **D3) Tam 180° ters istek** | Ölçüldü | — | Yerinde 180 erken ters: R 14.6, dönüş hızı 506°/s. Koşarken W → S: L 43 / R 29. Hat freni kötüleştirdi | t_trv180_e, k_ws_clean | HAYIR | **AÇIK** | — |
| **D4) S-kesişte yavaş çekim depar kavisi** | Sahip bulundu: depar veritabanı 230 cm/s'ye kadar seçilebiliyor. Kesiş sınırları ~300 cm/s'de tuttuğu için `A_SHM_Sprint_Curve` **0.53×** oynuyor. Aday: `SHM_SprintDBMinSpeed` 330 / 360 | — | Yavaş çekim kayboldu (310 cm/s'de tempolu kavis), ama sağ ayak 3 → 54 cm | chain_sscut | HAYIR | **AÇIK** | — |

**Korunan kazanımlar (son `fin` partisi, V2.20 değerleriyle aynı):**
- Kesiş → ters (`r_cutrev_r` L 3.2 / R 5.6).
- k_cut_back (L 0.9 / R 10.1).
- Erken ters çıkışları.
- Yürüyüş ve tempolu zincirler.
- Eğimde tempolu koşu.
- Yeniden başlama.

Pivot kilidi, TIP devri, durma yön tutma ve hız eğimi düğmeleri üretim değerlerinde (`verify_prod221`).

---

## 2. YENİ BEDEN VE ARAZİ DAVRANIŞLARI

| Davranış | Uygulanan | Ne zaman girer / çıkar | KAPALI / AÇIK farkı | Doğrulama | Üretimde | Kalan hata | Geri alma |
|---|---|---|---|---|---|---|---|
| **3. Duruşta yerleşme** | `SHM_UpdateBodyTargets`: gerçek bir hareket bölümü (≥ 60 cm, tepe hız > 60) durduğunda gövdeye tek bir öne-sonra-hafif-geri darbe: exp(−t/0.35)·cos(2πt/0.9), ≤ 1.4 s. İleri bölümünde diz 2 cm verir. Genlik giriş hızıyla (SpeedPeak/300). Mevcut fren duruşuna eklenir | Yerde, girdi yok, hız < 10. **Yeni girdi 0.08 s'de söndürür** (bekletmez). Dokunuşlarda girmez | Baş geri karşı hareketi: yürüyüş −0.8 → −1.4 cm, tempolu −0.8 → −1.9, depar −0.2 → −0.4. Göğüs ileri: depar +0.1 → +1.0. Depar `LeanFwd` 2.3 → 3.9 → 0 (0.7 s). Çoklu salınım yok, kambur yok | d_walk / d_jog / d_sprint; 20 / 30 / 60 / 120 FPS | **EVET** | **Küçük.** Normal hızda görülürlüğü görsel incelemeye ve kullanıcıya bırakıldı. Kol karşı tepkisi ayrıca eklenmedi (PBI kolları) | `SettleBodyEnabled false` |
| **4. Küçük yerleştirme adımları** | Önce sahibi ölçüldü: 0.15 s dokunuş kapsülü 2–4 cm taşırken MM bir başlangıç ADIMI çalıyor; ayak 8–22 cm sürükleniyor. Aday (`GR221_TapStepCm`): dokunuştan sonra kapsül adımı tamamlasın | — | 8–19 cm adım tamamlandı, ama MM 2–3 adım + yürüyüş durması çalıyor. Dinlenme 0.27 → 0.80 s, sürükleme azalmadı. **Reddedildi** | ss_taps / taphold / realign | **HAYIR** | **AÇIK.** Tutulan dokunuş zaten kesintisiz yürüyüşe geçiyor | — |
| **5. Arazide bütün beden tepkisi** | Gerçek çarpışmaya kare başına 3 çizgi izi: kapsül altı, hızla 35–140 cm ileri (yol yönü), 30 cm sağ. Etiket / isim yok. Süzülmüş eğim → gövde öne / geri. Yan eğim → yokuş tarafına denge. İnişte diz düşüşü. Ani zemin düşmesinde pelvis karşılaması (önceden görülen düşüşte yarısı). Ayak / pelvis uyarlaması (FootPlacement / LegIK) aynen kaldı, çift sayım yok | Yerde. Eğim tepkisi 20 → 80 cm/s ile açılır; ayrık yükseklikte dururken gövde eğilmez | **Taban:** 8° tepede gövde eğimi düz / yokuş / inişte aynıydı ("yalnız ayaklar oynuyor"). **Açık:** yürüyüş yokuş +4.1° / iniş −2.9°, tempolu +3.2° / −2.2°, gerçek harita tırmanışları +2.4…2.7°, 10° yan eğimde gövde 2.3° yokuş tarafına. Ayak / klip seçimi değişmedi | ter_hill8 / hill15 / bump / dip / roots / drop / xslope / split, pilot, map_r1..3. **20 / 30 / 60 / 120 FPS'de birebir aynı** | **EVET** | **Adımlama değişmedi:** yokuşta kısa / yüksek adım, inişte kontrollü indirme adımı ve yan eğimde ayrı diz bükümü klip ya da adım sahibi gerektiriyor. 15 cm kenardan tempolu inişte R 51 cm (açık ve kapalı aynı). Düşme / zıplama devri değişmedi | `TerrainBodyEnabled false` |

**Bileşik:** D (hepsi açık) ile A arasında pilot ve üç gerçek rotada ayak değerleri aynı (map_r2'de L 14.0 → 13.0). SHME maliyeti ortalama 1.13 ms, p95 1.66–1.68 ms; varyantlar arasında fark yok.

---

## 3. KAMERA, ODAK VE LENS DAVRANIŞI

**Taban (ölçüldü).**
- Mevcut FOV hızla zaten açılıyor: yürüyüş 60–60.9°, tempolu 62.6°, depar 65.0° (açıklık × yoğunluk). Depar kolu 254 cm.
- Lens V2.6'dan: sabit f/8, odak 260 cm, vinyet 0.2, fringe 0.1, hareket bulanıklığı 0.25.
- Black Eye Camera etkin değil. Kamera sahibi `GR_UpdateRig` + SHME sinyalleri; yeni katman açılmadı.

| Özellik | Uygulanan | Ne zaman | Fark | Doğrulama | Üretimde | Kalan | Geri alma |
|---|---|---|---|---|---|---|---|
| **Adım ritmi** | Doğrulanmış topuk temasında analitik dikey darbe z = −A·(ωa)·e^(1−ωa), ω 14. Sabit sinüs değil; kare hızından bağımsız. Çift tetik koruması: önceki adımdan ≥ 0.18 s sonra, ayaklar sırayla | Yerde, > 40 cm/s | Kamera adımı tempoluda 2.2–2.5/s (20 / 60 / 120 FPS aynı). 60 FPS'de temas titremesi ham kenarları ikiye katlıyor (34 / 15), koruma gerçek adımları tutuyor (16). Üretim derinliği 0.35 / 0.6 / 0.9 cm (yürüyüş / tempolu / depar) | d_*, ter_hill8, pilot, map_r* | **EVET** | Şiddet görsel kabul bekliyor. V2.6'da kullanıcı sarsıntıyı yarıya indirmişti; bu yüzden küçük tutuldu | `CamStepGain*` / `CamV221Enabled` |
| **İvme / ileri bakış** | Yol yönünde hızla 4 → 18 cm, τ 0.8. Yalnız pivot ofseti; kontrol dönüşüne asla geri beslenmiyor | > 60 cm/s | Yaw sıçraması yalnız bakış girdisinden (KAPALI / AÇIK eşit) | aynı | **EVET** | Çok ince | `CamLookAhead*` |
| **Hız FOV'u** | Kodda var | — | Mevcut FOV'un üstüne +3° = 68°: çift sayım. **0'a çekildi** | d_sprint | Kapalı | — | — |
| **Fren / dönüş karşı hareketi, yükseklik, iniş** | Mevcut sistem (fren 6, ivme 8, dönüş 6 cm; iniş çukuru; gövde Z takibi) korundu, değiştirilmedi | — | Arazide kamera yüksekliği KAPALI / AÇIK aynı (yokuşta asılı kalma / dalma yok) | pilot, map_r* | Değişmedi | — | — |
| **DOF / odak** | **Bilinçli olarak değiştirilmedi.** Sabit odak: otomatik odak avlanması ve bitki pompalaması yok | — | — | — | — | Etkileşim odağı sistemi yok; otomatik hedef kilidi eklenmedi | — |
| **Konfor** | `CamComfortScale` bütün SHME kamera ofsetini ve FOV değişimini ölçekler. Düşük hareket profili = 0.3 + `CamRollEnabled false`. Adım / ileri bakış / FOV kazançları ayrı | — | Düşük profil: yuvarlanma 0, dikey sıçrama 0.36 → 0.12 cm, FOV aralığı daralıyor | pilot, cam_corr | Var (varsayılan 1) | Menüye bağlı değil | — |
| **Çarpışma önceliği** | Ofsetler `GR_UpdateRig` küre izinden önce uygulanıyor | — | Koridorda (190 cm, tavanlı, uç duvar, 360° yörünge) KAPALI / AÇIK / düşük: **0 kare** duvar içi. Kare başına en büyük mesafe değişimi 18.5 cm ve üçünde aynı (mevcut çarpışma davranışı). Dar alanda adım darbesi 0.6 cm | cam_corr | — | Engel geçince geri çekilme mevcut sistemle aynı | — |
| **Sıfırlama** | > 2 m kapsül sıçraması veya ilk kare: V2.21 süzgeçleri sıfırlanır | Işınlanma / yeniden doğma / PIE başı | — | kod | **EVET** | Mod değişimi (nişan / çömelme) ayrıca sıfırlamıyor | — |

Hareket bulanıklığı, CA, vinyet ve distorsiyon artırılmadı. "mm lens" değişikliği yok.

---

## Eksik içerik (somut)

1. **Kesiş yönünden geriye fren-basış klipleri (sol / sağ).** Kesiş → S için: yanal hızdan durup geri koşuya geçen bir fren + basış. Mevcut `A_CP2_Jog_Fwd_Pivot` ileri → geri pivotudur. 90° yanal girişte kapsül hızı dönüyor; klip ise düz bir frenle duruyor.
2. **Küçük yerleştirme adımları için yol.** İçerik projede var:
   - `CoreMotion_Retargeted/AAMS/Idle/am_Stand_Idle_Step_{Fwd,Bwd}_{L,R}Foot`;
   - `am_Stand_Idle_Step_Left/Right`;
   - `am_Ready_*`;
   - kök hareketli ve `_NoRM` sürümleri.

   Bir sonraki adım: dokunuşu bunlara, yerinde dönüş montajlarına benzer bir kök hareketli yolla bağlamak. Bu sürümde uygulanmadı.
3. **Hareket halinde adım değiştiren arazi içeriği.** Yokuş, iniş ve basamakta yürüyüş / tempolu adımları. Satın alma / ücretli servis yetkisi yok; içerik isim taramasıyla bulunmadı.

## Doğrulama ve son durum

- **Terfi:**
  - ABP `SHM220_RecHold` 1.
  - SHME DA: Settle 6 / 2 / 60; Terrain 0.15 / 2.5 ve 0.1 / 1.2; CamV221 açık, adım 0.35 / 0.6 / 0.9, hız FOV'u 0.
- **İlk taze açılış doğrulaması.**
  - Bütün değerler beklenen üretimde, kirli paket yok.
  - Pawn profil referansları doğru.
  - Fonksiyonlar mevcut.
  - İki kontrol satırı hatalı yazılmıştı ve düzeltildi:
    - OR düğümünün tür adı (`ORBoolean`);
    - MontTick'te bağlantısız kalan bir `LastHitBy` düğümü. Bağlıysa hata sayılıyor; `fin` partisinde 0 çalışma zamanı hatası var.
- **Son taze açılış doğrulaması** (yakalamalardan sonra, `verify_prod221_fresh2.txt`): **ALL_OK**, kirli paket yok. MontTick'teki tek `LastHitBy` düğümü (`K2Node_VariableGet_3`) bağlantısız, yani işlevsiz bir artık.
- **Kendi yol açtığım gerileme.** Küçük adım kurulumu profil sınıfını yeniden derledi. `BP_PBI_Player.GR_Profile` boş geçersiz kılmaya düştü ve kaydedildi. Sonuç: bütün girdi kesildi (`b3` partisi geçersiz). Onarıldı, kaydedildi. Doğrulama artık bunu denetliyor.

## Geri alma

- Düğmeler:
  - `SHM220_RecHold 0`;
  - `SettleBodyEnabled`, `TerrainBodyEnabled`, `CamV221Enabled` false.
- Varlık kopyaları: `checkpoint/pre_promo/` ve `checkpoint/baseline_v220/`.
- DSL kaynak kopyası: `checkpoint/tools_v1/*.v221a`.

## Kanıt dosyaları

- `final221.txt` (son `fin` partisi, p / o).
- `jobs_final.txt`.
- `verify_prod221_fresh1.txt`, `verify_prod221_fresh2.txt`.
- `CHANGES_V221.md` ve `diff_*.txt`.
- `img/`, `vid/`: düzenlenmemiş kareler; PIE'ye özel kil test görünümü.
