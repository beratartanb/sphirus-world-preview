# SHME V2.17 — V2.16 gerilemeleri, kesiş→ters/geri zinciri, tempoludan depara itiş, toparlama adımı denemesi

Tarih 2026-10-19 · UE 5.8.1 · harita L_GR_SphirusHouse · başlangıç = V2.16 üretimi (`verify_prod216.txt`), checkpoint
`Saved/Codex/SHME_V217_20261019/checkpoint/baseline_v216/` (+ `pre_c1`, `pre_tiphand`, `pre_pawnresave`, `pre_promote`, `pre_remap`, `pre_timewarp`).

**Kabul ayrımı.** Bu rapordaki PASS/PARTIAL/FAIL değerleri **teknik** ölçümdür. Görsel değerlendirme kayıtlarla (`pub/vid`, `pub/img`)
senin içindir. Kullanıcı kabulü **verilmiş sayılmadı**. Ayrıca oyun içi deneme listesi var: `USER_PLAYTEST_V217.md`.

**Kanıt kuralı.** "Önce" = V2.16 üretiminin bu oturumda ölçülmüş hâli (`v217b1_*`). Bu ölçüm V2.16'ya yalnız yaw-snap düzeltmesi
eklenmiş hâlde alındı; geçiş içeriği değişmedi. "Sonra" = **tek, kaydedilmiş nihai üretim partisi** `v217z2_*`: 70 koşu, iki yön,
1–3 tekrar. Tüm aday kararlarından sonra koşuldu. Öncesinde ve sonrasında `verify_prod217*.txt` PASS, `scan_dormant_v217z2.txt` SCAN_OK.

İlk nihai deneme `v217z_*` (25 koşu) **geçersiz sayıldı ve kanıt olarak kullanılmadı**. O partide tempolu itiş, ters dönüşün yeniden
hızlanmasında da tetikleniyordu: çıkışta 16–26 cm kayma. Bu düzeltildi (§2.2) ve nihai parti baştan koşuldu.

Hücreler, tekrarların en kötüsüdür: ayak başına net kayma / sürükleme yolu (cm), `contact216` gerçek zemin ölçümü. Ayaklar hiç toplanmadı.

## 1. ONARIMLAR

| Konu | Gerçek uygulama | Tetik / çıkış koşulu | Önce (V2.16, b1) → Sonra (V2.17 nihai z2) | Gerileme kontrolü | Üretimde | Kalan kusur | Geri dönüş |
|---|---|---|---|---|---|---|---|
| **Yaw-snap (her iki çıkış)** | AAMS üst sınıfın `CoreMotion_ApplyPlayerRotationPolicy`'si tek karede controller yaw açıyordu (aktör 88° kamera yönüne zıplıyordu). BP_GR_Player bunu override ediyor; dönüşün sahibi GR. | Her karede | Snap satırı 9 → 0. `mws` 416→300→200 düşüşü yok | Kesiş, geri koşu, TIP değişmedi | EVET | — | `checkpoint/baseline_v216` pawn |
| **Sol kesiş → ters giriş** | `SHM217_RevFlip` (kesiş yönü kilidi; ters istekte kesişin karşı kesiş olarak yeniden sınıflanması engellenir; arama kısıtı temizlenir). RevTurn_R_Rfoot `entry_foot`: giriş duruşu, önceki klibin çıkış karesindeki kök-göreli ayak yerine konur. Topuk/top kalkış açıklığı. | Kesiş başlangıcından ≤1 s içinde, kilitli kesiş yönüne >120° ters istek | Giriş+dönüş: L 37.5/44.5 → **3.0/3.0**, R 15.7/28.3 → 6.5/12.9 | Sağ giriş R 19.7 → 2.4; slalom (W+A↔W+D) ters sayılmıyor | EVET | Ters isteğin karesinde tek karelik karşı kesiş seçimi hâlâ görülüyor (görsel etkisi ölçülmedi) | ABP `SHM217_RevFlip` 0 + `checkpoint/pre_c1` RevTurn |
| **Sol çıkış** | RevTurn kuyruklarında 1.3 s'den sonra kadans zaman bükme + kapsül yoluna yeniden yerleştirme | — | L 26.4/31.0 → **7.4/11.5**; R 7.4 → 6.4 | Sağ çıkış L 4.7 → 5.4, R 0.8 → 6.5 (küçük artış) | EVET | Sağ çıkışta R 6.5 cm | `checkpoint/pre_timewarp` |
| **Kesiş → S (geri koşu)** | Dört geri koşu ivmelenme bağlantısı `SHM217_BackLink_1..4` (A_RB_Run_Rear'in dört evresinden, kadans 0.42→0.32 s, ölçülen geri kapsül yoluna yerleştirildi, giriş penceresi [0, 0.2]); `PSD_RB_Run_Rear`'de | S basılı + geri koşu veri tabanı | Geri koşu girişi+koşu: R 58.5/69.6 → **7.3/14.7**; L 19.3 → 21.4 | k_walkback / k_jogback / k_ws_w sorunsuz | EVET | Geri koşu duruşunda sol top statik idle kalibrasyonundan 1–2 cm yüksek (HOVER sınıfı; içerik kaynaklı, kaynak döngüde de var) | integrate217_back `off` |
| **Diz içe kapanması** | Kesiş/ters kliplerinde `lat_cap` 18 cm (pelvis çizgisine göre), top pivotlu duruş yaw'ı, açık diz düzlemi çözücüsü (medial ≤ kaynak + 3 cm). Kalça/bacak oranı değişmedi, sabit yüzde daraltma yok. | — | Medial diz kayması (çalışma zamanı): sol kesiş→ters R 20.2 → 16.6; sağ L 11.8 → 5.8; S-kesiş L 16.4 → 9.8; diz düzlemi hızı 874–981 → 735–737 °/s | Geç ters (r2) L 21.0 → **26.2**, düzlem hızı 1394 → 1779 °/s (gerileme) | EVET | Geç ters tek açık nokta | `checkpoint/pre_remap` |
| **Çalışma zamanı pelvis düşmesi** | Katman ayrıştırması: klip 76.3 → HC girişi 75.4 (MM karışımı −0.9) → HC katmanı −2.9 → nihai 72.5 cm. HC, ayakların yere ulaşması için pelvisi indiriyor. Değişiklik yapılmadı: sabit pelvis tabanı veya karşı-additive yasak. | — | S-kesiş min 73.1 → 75.2 cm | — | ölçüm | HC −3 cm (bilinçli) | — |
| **Yürüyüş → depar evreleri** | Çeyrek adım giriş penceresi aday olarak denendi (8 bağlantı, `PSD_SHM217_WalkLink`): aynı oturumda V2.16'dan iyi değildi, kullanılmıyor. Üretim V2.16 bağlantıları. | — | std L 10.6 → 9.3; early R 10.6 → 8.8; mid R 23.4 → 21.9; late R 10.9 → 10.6 | **rel**: L 7.5/9.8 → 17.5/93.8 sürükleme yolu (bir koşuda; aynı klip zinciri, neden ayrıştırılmadı) | V2.16 hâli | mid R ~22 cm ve rel tek koşu sıçraması açık | — |
| **Yerinde ters dönüş devri** | Aday `GR217_TipHand` (pawn): ters istekte Stop → idle → başlat yerine yeni dönüş montajı, çalan montajın gerçek pozundan hemen başlar. 180°'de daha iyi (R 14.6 → 10.6), 90°'de daha kötü (planlı R 0.8 → 12) → **üretime alınmadı**. | — | Üretim değişmedi; nihai devir: L 1.6–7.4 cm, sürükleme ≤ 13 | — | HAYIR (aday, düğme 0) | Sabit idle başlangıç pozu sorunu çözülmedi (PARTIAL) | düğme 0 |
| **Çift ters (r_kb2)** | — | — | L 15.1 → **42.0**, R 16.6 → **54.8** (2 koşu; pivot→RR start arası düşük hız penceresi) | — | — | **Gerileme**. Aynı klip zinciri; olası neden itiş duruş veri tabanı kopyası (`PSD_SHM217_PushStandJ`), kanıtlanmadı | `SHM212_DB_PushStand` = PSD_RR_Start |
| **Çok erken ters (kesiş +0.15 s)** | Değişmedi (RevFlip bu zamanlamada devreye girmiyor; V2.16 ile aynı eğri → itiş zinciri) | — | Sağ: L 8.2 (V2.16, 2 koşu) → **54.5** (V2.17, 3 koşu) | Ara b-partilerinde 18–31 cm | — | Kusur; tekrar varyansı yüksek; toparlama adımı bunun için denendi (§2.1) | — |

## 2. YENİ DAVRANIŞLAR

| Davranış | Gerçek uygulama | Tetik / çıkış | Kapalı → açık kanıtı | Gerileme | Üretimde | Kalan kusur / engel | Geri dönüş |
|---|---|---|---|---|---|---|---|
| **2.1 Durumsal tek toparlama adımı** | İçerik: AAMS Run_Turn_180 (fren + tek yeniden yerleşme adımı + itiş), ölçülen çok-erken-ters kapsül yoluna (fren ayağının yere değdiği an = rel 0) zaman bükme + yeniden yerleştirme ile `SHM217_Recover_{L,R}_{L,R}foot` (4 klip), kendi DB'si `PSD_SHM217_Recover`. Rota: MontTick `SHM217_RecOn` → `SHM212_DB_CutRevL/R` = Recover. | İstek kilitlenir (kilitli kesiş yönüne >120° ters, kesiş yaşı < RecAge, hız > Recover). Bölüm, istekten sonra RecWait içinde ilk yüklü-ayak karesinde başlar; iki ayak havadaysa beklenir. Girdi yön değiştirir/bırakılırsa güvenli çıkış. | Kapalı: çok erken terste eğri + itiş. Açık (b6): 4 hedef koşunun 2'sinde tetiklendi. Geniş kavis ve S-kavis tetiklemedi. Bırakma ve ikinci yön değişikliği güvenli çıkış verdi. **Ancak** toparlama klibi sırasında ayaklar 1.2–1.4 s boyunca yere değmedi (SKIM/havada, ayak başına 25–50 cm) ve diz medial kayması 17–18 cm. Ek adım gerçekten yere basmıyor. | Normal ters zamanlamasında (0.35 s) tetiklenmemeli. b6'da eşik 250 cm/s iken tetiklendi → eşik 280 / RecAge 0.3 öneriliyor. | **HAYIR** (aday, `SHM217_Recover` = 0). Görsel kayıt: aday ayarlarıyla (280 / 0.3) alınan 3 kayıtta tetik **hiç ateşlenmedi**; bu da güvenilirlik engelinin kanıtı. Bu yüzden yanıltıcı olmasın diye o kayıtlar yayımlanmadı; ham kareler `v217cz_*_q*` | **FAIL**. Engel sınıfı: **içerik** (kaynak 60 cm fren çömelmesi; pelvis 72–80'e yükseltilince ayak erişimi bitiyor) + **kontrol tasarımı** (ters niyeti GR'nin döndürdüğü CMC ivmesinden ~0.15 s geç görünüyor; bileşen temas bayrağı inişi ~0.3 s geç bildiriyor) | Düğme 0 |
| **2.2 Tempoludan depara kısa itiş** | 4 bağlantı `SHM217_J2S_{L,R}foot_{a,b}` (projeye ait Run_to_Sprint kopyalarından). Kadans: tempolu 0.37 s → itiş 0.33 s → depar 0.34 s. Kapsül yoluna yeniden yerleştirildi, diz koruması, pelvis 87'ye. `armcap217`: el dış yanal tavanı 40 cm (kaynak 52 cm sprinter kolu). Pencere başları iniş karesinde (0.667 / 0.74). DB `PSD_SHM217_PushStandJ` = RR start girdileri + bağlantılar. MontTick'te kendi başlangıcı var (V2.12 guard itişi kapalı). | Başlangıç: sabit tempolu, depar niyeti, 260–400 cm/s, ivme > eşik, girdi hız yönüne yakın, başka itiş / ters penceresi / redirect yok, son tersin üzerinden > 1.5 s, öncesindeki Shift bırakışı ≥ 0.5 s. Bitiş: 470 cm/s, en fazla 1 s, niyet kaybı. | Kapalı (V2.16): tempolu döngüsü 0.35 s sürüyor, sonra depar döngüsüne kesiliyor; ilk adımlar 0.31 / 0.42 s, R 38.1/55.9. Açık (z2 ×3): itiş klibi +0.29–0.31 s'de giriyor ve +0.87 s'de depar döngüsüne geçiyor. Adımlar 0.30–0.33 s; kollar −40 cm (depar döngüsüyle aynı). Temas: L 11.8/17.8, R 6.3/11.8. mid L 10.2, R 4.5. | Kısa Shift bırak-bas (p_j2s_tap ×2, p_tapretrig ×2): **ikinci itiş yok**. W+A/W+D: yok. Ayakta depar başlangıcı RR start ile aynı. Ters dönüş kuyruğunda tetiklenmiyor (z2 çıkışları temiz). | **EVET** (PARTIAL) | Bir koşuda ilk itiş adımı 0.49 s (uzun). Giriş sol ayağı en kötü 11.8 cm, V2.16 tempolu L 7.3'ten kötü (R çok daha iyi). tapretrig'de L 44.7: itiş tetiklenmedi, depar döngüsüne yeniden giriş; V2.16 karşılaştırması yok. | ABP `SHM217_JogLink` 0 + `SHM212_DB_PushStand` / `SHM214_DB_PushStand0` = PSD_RR_Start |

Sayılar `final217_table.md` / `final217.json` (her koşu ayrı), aday kanıtları `abb4..abb8_run.out` + Evidence `v217b4..b8_*`.

## 3. Ölçüm ve yöntem
- `contact216.py`: gerçek zemin izi (gzl/gzr); DRAG / PIVSLIDE / SKIM / HOVER / SINK ayrı; ayaklar toplanmaz. Önce ve sonra aynı pencere ve kod (`final217.py`).
- `knee217.py`: valgus = ayak bileği aralığı − diz aralığı. Medial diz kayması kalça–bilek çizgisinden ölçülür. Diz düzlemi açısal hızı °/s (kare hızından bağımsız).
- Ayrı gecikmeler: girdi → kapsül 0.26–0.29 s (itiş); animasyon devri = seçilen klibin ilk karesi (`seq217.py`); fiziksel tamamlanma 300/420/480 cm/s zamanları (`w2s217.py`).
- Katmanlar ayrı ölçüldü: kaynak klip (`rm217_*.json` izleri) → zaman bükme → yeniden yerleştirme / diz → çalışma zamanı HC giriş/çıkış (`ac_SHM_HCi/HCo`) → nihai (`mx/vb`).
- Harness eklemeleri: `pawn_flags` (pawn CDO; base'de yok, çünkü sınıf paketini kirletiyor), yeni senaryolar `p_j2s_mid/rel/tap/dir`,
  `r_cutrev_l0/r1/r0_rel/r0_w`, avars `SHM217_*`.
- Kare kaybı: harness bazı montaj başlangıçlarında 0.1–0.4 s satır kaybediyor (ör. b1 t_tiprev 3.41→3.81). Kritik pencerelerde bu not edildi.

## 4. Gerçek hareket referansı (yalnız erişilen metinler; video izlenmedi)
- Tepkisel / toparlama adımı: başarılı toparlama, ayak temasında kütle merkezi hızını düşüren büyük ve hızlı bir adıma bağlı
  ([UManitoba tezi](https://mspace.lib.umanitoba.ca/items/5c380d3d-0e18-41c0-ab16-5f5de31f2d30)). İlk toparlama adımında önde kalan bacak geriye açısal impuls üretiyor
  ([Frontiers Neurol 2022](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2022.1032417/pdf), [bioRxiv](https://www.biorxiv.org/content/10.1101/2022.07.28.499225v1)).
  Bu çalışmalar yürüyüş pertürbasyonu üzerine; koşu kesişine doğrudan uygulanmıyor.
- Depara geçiş: erken ivmelenme daha kısa temas ve ~%9 daha yüksek adım frekansıyla geliyor, adım boyu değişmiyor
  ([JSSM](https://www.jssm.org/jssm-02-144.xml-abst)). Bilinçli öne eğilme ilk iki adımda frekansı artırıyor ([ISBS](https://ojs.ub.uni-konstanz.de/cpa/article/view/6932/6227)).
  Dikten öne eğik duruşa geçiş daha hızlı ivmelenmeyle ilişkili ([Gait & Posture 2023 özeti](https://researchers.westernsydney.edu.au/en/publications/transition-from-upright-to-greater-forward-lean-posture-predicts-/)).
  Bu, "daha hızlı adım + kısa itiş, büyük öne çökme yok" hedefini destekliyor. Kaynaklar sporcu örneklemi. Karakter sporcu değil; bu yüzden yalnız yön olarak kullanıldı.
- V2.16 kaynakları (kesiş, yürü→koş, yerinde dönüş) aynen geçerli: `REPORT_V216.md` §4. Ücretli kaynak, satın alma ya da harici yükleme yok.

## 5. Üretim, dosyalar, doğrulama
- **ABP varsayılanları** (kaydedildi; `promote217.py`): `SHM217_RevFlip` 1, `SHM217_JogLink` 470, `SHM212_DB_PushStand` =
  `SHM214_DB_PushStand0` = PSD_SHM217_PushStandJ, `SHM212_JogPush` 0. Kapalı adaylar: `SHM217_Recover` 0 (RecAge 0.3, RecLen 1.4, RecWait 0.4)
  ve pawn `GR217_TipHand` 0. MontTick DSL kaynağı: `install_route_src.lisp`. Yükleyiciler: `install_v217_route` / `recover` / `recover2` /
  `recwait` / `recfix` / `joglink` / `joglink2` / `joglink3` / `rotpolicy` / `tiphand`.
- **İçerik**: `V217/SHM217_BackLink_1..4` (üretim), `SHM217_J2S_*_{a,b}` (üretim), `SHM217_Recover_*` + PSD_SHM217_Recover (aday),
  `SHM217_W2S_*_{a..d}` + PSD_SHM217_WalkLink (aday, kullanılmıyor), `SHM217_J2S_{L,R}foot` (rev1, DB dışı).
  V216 RevTurn / Cut klipleri yeniden yazıldı (kuyruk kadansı, kalkış açıklığı, entry_foot). Satıcı orijinalleri değişmedi
  (`PSD_SM_LocoTransitions` mtime 2026-09-21, `PSD_RR_Start` mtime 2026-09-19).
- `verify_prod217.txt` (parti öncesi) ve `verify_prod217_after.txt` (parti sonrası, editör yeniden açıldıktan sonra): PASS, sızıntı yok.
  `scan_dormant_v217z2.txt`: 70 koşu SCAN_OK. Bu koşularda toparlama mandalı yok, aday DB yok, TIP adayı yok.
- Geri dönüş: ABP değerleri için `promote217.py` V2.16 değerleriyle; içerik için `checkpoint/*` editör kapalıyken geri kopyalanır.
  BackLink'leri çıkarmak için `integrate217_back.py` `off`.

## 6. Kabul
- Teknik: sol giriş/çıkış ve kesiş→S **PASS** (ölçülen büyük iyileşme). Diz **PARTIAL** (geç terste gerileme). Yürüyüş→depar **PARTIAL**
  (değişiklik yok; mid ve rel açık). TIP devri **PARTIAL** (aday üretime alınmadı). Tempolu itiş **PARTIAL** (çalışıyor, tekrarlamıyor;
  sol giriş teması kötüleşti). Toparlama adımı **FAIL** (aday; ek adım yere basmıyor). Çift ters ve çok erken ters **gerileme / açık kusur**.
- Görsel not (benim gözlemim, kabul değil): sol kesiş→ters yan görünümde fren duruşu geniş (karşılaştırma sayfası, yan satır f23–f27); değerlendirmen gerekiyor.
- Görsel: `pub/vid` (gerçek hız GIF + realtime AVI + 1/3 yavaş AVI; yan / çapraz / oyun kamerası, kesilmemiş kare, yalnız test dünyasında
  opak kil görünüm) ve `pub/img` önce/sonra sayfaları. Görsel ve oyun hissi kabulü **sende**.
