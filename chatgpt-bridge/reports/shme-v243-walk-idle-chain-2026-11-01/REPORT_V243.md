# SHME V2.43 — yürüyüş → duruş → bekleme → yeniden kalkış zinciri ve yanal fren (2026-11-01)

Taban: V2.42 üretimi (`VERIFY241 ALL_OK`). Yöntem: önce sahipliği ölç, sonra tek zinciri uçtan uca; her aday bir anahtarın arkasında; üretime yalnız ölçülmüş ve kare şeritleriyle incelenmiş olan alındı. Detay: `CHANGES_V243.md`, sayılar: `TABLES_V243.md`. **Gerçek hızlı videoları oynatıp izlemedim**; aynı karelerden kırpılmış şeritleri inceledim ve görsel kabulü buna göre, sınırlarıyla yazdım.

## 1. Öncelik 1 — idle ve zincir: gerçek sahip ve çözüm

**Sahip (ölçüldü, V2.29 ABP dökümü + LTP):** görünür idle MM değil. `SHM_Snapshot`: `SHM_IdleHold = (HumanStateEnabled ∧ StanceIdleGateEnabled) ∧ SpeedPeak > 30` (**sabit literal**; `IdleStanceTolerance` ABP tarafından okunmuyor — skill belgesi güncel değildi), idle girişinde bir kez karar veriliyor, yalnız ayakta dönüş veya sonraki giriş temizliyor. Hold varken alt beden = `PoseSnapshot 'SHM_StanceHold'` (+ V2.9 de-adaptasyon IK'si), spine_01'den yukarısı = `SequencePlayer_5 'A_Ranger_Idle_Neutral_CWF'` (`SHM_IdleUpperW`, τ 0,35). V1.2'de AAMS satıcı duruşları idle duruşundan 20–29 cm uzakta bittiği için konmuştu; V2.6 yeniden yazılmış yürüyüş duruşları zaten idle duruşunda bitiyor → tutuş bu zincirde gereksiz ama her gerçek duruşta latch'leniyor = **"donmuş manken" idle'ın sahibi**. Üst-beden sekans değişimi (bellek içi, `pre243_idle.py`) görünür hareket vermedi (ölçüldü; neden doğrulanamadı).

**Çözüm (aday `idlg`):** SHME profili `StanceIdleGateEnabled = false` (hold hiç latch'lenmez → alt beden MM) + V2.42 MM idle kancası (`SHM242_IdleOn` 1, `SHM242_IdleDB` = `PSD_SHM242_Idle`, klip `SHM242_Idle_Weighted`: ağırlık sağa/sola 3,8 cm, nefes 15/dk, mikro salınım, 11,2 s). Ölçüm (w42_id ve 8 s'lik `w43_idle`, 30 FPS):
- klip gerçek zamanda ilerliyor (SelectedTime 0,07 → 1,07 / s), `IdleHold False`;
- **ayak kayması 0,0** (devralmada ve bekleme boyunca), **kalkış pop 0** (> 25 m/s²), kalkış pelvis hız rampası üretimle aynı (39→132 cm/s);
- 7,3 s beklemede pelvis ayaklar arası ekseninde −1,1 → +4,8 cm (ağırlık sağ ayağa), göğüs z 3,5 cm p2p (duruş yerleşmesi + nefes), baş 9 cm (duruş + bakış);
- kontrol gecikmesi yok (kalkış `A_SHM222_WalkStart` CP evaluator'ında, değişmedi).
Görsel (yan şerit `sheets/idle_w43_*`): yanal ağırlık aktarımı yan kameradan okunmuyor (kamera eksenine paralel); çapraz/oyun kamerası şeritleri `sheets/idle_w43_*D*` (bkz. §5). Video: `vid/idle_w43_o_vs_idlg_side_realtime_part1.avi`.

**Yürüyüş değerlendirmesi:** izolasyon A/B'si (`oSCR`/`oPBI`/`oRAW`) yürüyüş metriklerini değiştirmedi → 23° pelvis–göğüs karşı dönüşü, kol taşıma ve pelvis hareketi **`A_LB_Walk_Fwd` klip içeriği**, runtime katmanı değil. İnsan referansına göre karşı dönüş %15–25 fazla, kol salınımı normal, kadans/adım normal; MM oynatma 1,245× (106 → 132 cm/s). Düzeltme = yürüyüş döngüsünün yeniden yazımı (temas-planlı, 132 cm/s'de doğal kadans) — bu turda yapılmadı (önce idle/kalkış zinciri). Kalkış öncesi ağırlık aktarımı V2.22 kalkış kliplerinde mevcut (apa 1,8 cm, 6° eğim).

**Regresyon ve ikinci idle klibi:** birleşik aday `all` (yanal + kapı + bakış kuralı + stance kapısı kapalı + ağırlıklı idle) tam regresyonda üç senaryoda geriledi (gait 8,3→14,6 cm / 0→4 pop, taps 17,3→20,1 / 0→3 pop, j40_rlw kalkışı 11→21 cm). Ayrıştırma (`TABLES` §8): yanal parça (`latgl`) ve kapı-kapalı (`og`) tek başlarına bu üç senaryoda üretimle **aynı**; gerileme ağırlıklı idle klibinden geliyor — klip duruştan 0,8 s sonra ağırlık kaymasına başlıyor, kısa dokunuş/erken kalkış bu kaymış pelvisten kalkıyor. Çözüm: aynı klip 2,5 s geç başlangıçla yeniden yazıldı (`SHM243_Idle_Weighted2`, 388 kare). İlk kurulumu (`PSD_SHM243_Idle`) **çalışmadı**: V2.42 kancası override'ı yalnız seçili DB adı `Stand_Idles` veya `SHM242_Idle` içerirken sürdürüyor; ad uymayınca her karede arama ping-pongu → görünen klip yine satıcı idle. DB `PSD_SHM242_IdleB` adıyla yeniden kuruldu (aday `idlg3`, sonuçlar §5). j40_rlw'deki 11,2↔17,2 cm farkı üretimde de koşudan koşuya değişiyor (3 tekrar) → varyans.

## 2. Öncelik 2 — yanal fren ve duruş sonrası yeniden yönelme

**Yeniden yönelme sahipliği (ölçüldü):** V2.34 loco çerçevesi (`SHM_UpdateCameraV21.dsl`: `lstart` = hız 60–380 ∧ 20° < |girdi − çerçeve| < 120° ∧ 1,6 s bakış yok) bakışa bağlı 90° strafe'i de keşfediyor (REPORT_V234 strafe'lerin ayrı kalmasını amaçlıyordu); bırakmada `lhold` ilerleme yaw'ını tutuyor; `GR_UpdateIdleTurn` (V2.34'ten beri referansı `Select(LocoOn, LocoYaw, kontrol)`) 90° montajı başlatıyor.
**Kural (aday `latgl`, pawn `GR243_TurnNeedsLook`):** keşfedilmiş çerçeve tek başına ayakta dönüş emretmez; dönüş için oyuncunun bakışı da bedenden ≥ 42° ayrışmalı. Sonuç: j41_rl_p04/p10, j42_lr_p10'da **montaj yok**, beden bakış yönünde (−78° vs bakış −74°) yerleşiyor; yürüyüş-keşif duruşunda (beden zaten çerçevede) davranış aynı; oyuncu bakınca dönüş yine çalışır. Ayak kayması p04 8,1 cm (kalkış klibi), sağ ayna devralmada 14,6 cm (idle devralma karışımı, açık).

**Gerçek zaman 22 cm (klip ↔ kapsül):** sahibi bulundu, çözülmedi: V2.28 klip-bağlı kapsül yalnız yeniden yönlendirme episodunda (`SHM228_On` = episod ∧ `SHM226_W` eğrisi) açılıyor, pawn yazımı `ActorForward × ClipSpeed` (yanal hız ifade edemiyor) ve CMC freni sıfırlanmıyor (klip hızının üstüne fren biner). Yanal duruşu klip-bağlı yapmak için: yeni kapı terimi + yön + `BrakingDecelerationWalking 0`. Bu tur yapılmadı; sabit adımda (30/60/120) aile temiz.
**Kapanış adımı sıçraması (Bl_P21, 32 cm):** montaj değil — kapanış adımı 4 cm tepe ile FootPlacement'ta "basılı" kalıp bırakılınca sıçrıyor → aile `close_apex` 8 / `apex_min` 6 ile yeniden yazıldı (sonuç: §5 tablo).

## 3. Öncelik 3 — kalan kusurlar
P20 K seçimi / 0,2 s geri sarma, 60 FPS üçüncü komut, dönüşlü kalkışlar (`TurnL045` gerçek zaman kalkışı), itme, duvar/kamera: **bu turda ele alınmadı** (ilk iki zincir önce).

## 4. Üretime alınanlar / alınmayanlar
**Alındı (aday `latgl`, manifest `v243_prom_lat`, `verify241` sonucu §5):** `SHM242_DB_LatStop` = `PSD_SHM242_LatStop` (32 temas-planlı yanal fren klibi, kapanış adımı 8 cm), pawn `GR242_TurnSettleGate` = true, `GR243_TurnNeedsLook` = true. Gerekçe: kendi regresyonu üretimle aynı (taps/gait/j40_rlw; `TABLES` §8), yanal duruş kayması 39→8 cm (30 FPS), 60→9 (60 FPS), gerçek zaman 0,0 (tek koşu); duruş sonrası 90° montaj yok.

**Alınmadı (kapalı bırakıldı):** idle zinciri (`StanceIdleGateEnabled` false + `SHM242_IdleOn`/`IdleDB`). Bekleme ölçümü PASS (klip gerçek zamanda ilerliyor, 8 s'de kayma 0, pop 0, ağırlık aktarımı ölçülüyor), ama MM idle klibine herhangi bir zamandan giriyor (ör. 11,0 s = ağırlık tek ayakta) ve kalkış bu kaymış pelvisten karışıyor: taps 8. dokunuş kalkışı 17,3→22,7 cm, idle'dan jog kalkışı 11→21 cm, +2 kalkış popu; stance kapısı kapalıyken satıcı 135° dönüşlü kalkışlarda +2 omuz popu (26/32 m/s²). Kullanıcının "yeniden kalkışta kayma/pop yok" şartı sağlanmadı → üretim dışı, nedeni ve ölçümü `TABLES` §9. Ayrıca bu turda hiçbir satıcı asset değiştirilmedi; üst-beden sekans değişimi ve yürüyüş döngüsü yeniden yazımı yapılmadı.

## 5. Kanıt ve ölçüm
- **Üretim sonrası (yeniden başlatılmış editör, bayraksız):** `TABLES` §10 — j41_rl_p04 39,2→**8,1** (30 FPS), 59,5→**7,6** (60), gerçek zaman **11,9 / 9,2** (iki koşu, en kötü episod duruş değil); 90° montaj üç senaryoda yok; j41_rl_p10 **32,5** (Bl_P21 bini, açık), j42_lr_p10 **14,6** idle devralması (açık); taps/gait/w42_id/w43_idle/jstart/wdiag/wstart/j40_rlw terfi öncesiyle aynı.
- **Terfi tuzağı (düzeltildi, raporlandı):** aynı editördeki ilk üretim partisi eski değerleri gösterdi (çocuk BP CDO'ları); yeniden başlatma sonrası sonda ile doğrulandı. Kural: terfi sonrası üretim A/B'si yalnız yeniden başlatmadan sonra.
- **Aday matrisi:** `TABLES` §1–§9 (idle sahipliği, dönüş kuralı, yürüyüş izolasyonu, 8 s bekleme, FPS matrisi, regresyon, ayrıştırma, idlg3).
- **Görsel:** kare şeritleri `sheets/` (idle: `idle_w43_{o,idlg,idlg3}{S,D,G}_crop.png` — yan/çapraz/oyun kamerası; yanal: `lat_p04_latglS_stop_crop.png`); gerçek hızlı yan yana videolar `vid/` (idle yan/çapraz/oyun, yanal yan/oyun). **Videoları oynatıp izlemedim**; şeritlerden okuduğum: idle adayında 7–10 s arasında kalça/ağırlık kayması okunuyor ama küçük (çapraz kamera), üretimde beden donuk; yanal duruşta montaj yok, beden bakış yönünde yerleşiyor. Oyun hissi kabulü (akıcılık, ağırlık) bu şeritlerle verilemez → **NOT_TESTED**; teknik kabul yukarıdaki sayılarla.
- Kanıt dosyaları: LTP `v243*_*.ltp`, raporlar `Reports/v243*`, zincir çıktıları `chain.out`, manifestler `v243_*.json` (ikili yedekler yayımlanmadı).

## 6. Açık kusurlar (öncelik sırasıyla)
1. **Idle zinciri giriş fazı:** MM idle klibine ağırlık kaymış anından giriyor → kalkış kayması (+5…+10 cm). Tasarım: nötr giriş DB'si + IdleWait sonrası devam DB'si, ya da kalkış kliplerinin pelvis girişini idle pelvisine hedefleme; 135° dönüşlü satıcı kalkışların MM idle duruşuyla uyumu (+2 pop).
2. **j41_rl_p10 Bl_P21 bini:** fren ayağı 86° dönerek 32,5 cm kayıyor (klip içeriği/FootPlacement; apex yeniden yazımı etkisiz) — bin bazında yeniden üretim + leg-guard.
3. **Sağ ayna idle devralması:** yanal duruş bitiş ayak yönü ≠ `af_Stand_Idle` → 51° ayak dönüşü, 14,6 cm; duruş sonrası bin dolaşması (P19→P22→P07).
4. Gerçek zaman yanal sürüklenme: üretim iki koşuda 11,9 / 9,2 (V2.42'nin 22 cm'i tekrarlanmadı); klip-bağlı kapsül tasarımı hâlâ yok.
5. 60 FPS 90° jog kesme episodu (34–39 cm, 7,95 s) eski/yeni üretimde aynı — P20/60 FPS ailesi.
6. Yürüyüş döngüsü içeriği (23° karşı dönüş, 1,245× oynatma) — yeniden yazım bekliyor; üst-beden sekans değişiminin görünmeme nedeni doğrulanmadı.
7. `PSD_SHM243_Idle` (yanlış adlı DB) silinemedi (BranchIn referansı) — üretimde referanssız, temizlik bekliyor.
8. İtme toparlanması, duvar ayağı/kamera: V2.41 durumu.
