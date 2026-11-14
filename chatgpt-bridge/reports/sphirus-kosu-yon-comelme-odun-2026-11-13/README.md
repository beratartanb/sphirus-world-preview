# SPHIRUS — Koşu, Yönlenme, Çömelme ve Odun (P0) + ana görev kalanları — 2026-11-13/14

İki metin tek görev olarak değerlendirildi: "Koşu, Yönlenme, Çömelme ve Odun Etkileşimleri" (P0 hata düzeltmeleri, öncelikli)
ve "Doğal İnsan Hareketi, Yaşayan Kamera ve Sinematik Dünya Bütünlüğü" (ana görev ve kabul koşulları). Çelişkide son kullanıcı
geri bildirimi ve son kontrol sözleşmesi esas alındı.

**Durum etiketleri:** IMPLEMENTED (uygulandı) · TECH_TESTED (oyun içinde gerçek girdiyle ölçüldü) · VISUALLY_INSPECTED (kareler/video
tarafımdan incelendi) · PERFORMANCE_TESTED · USER_ACCEPTED. **Hiçbir başlık USER_ACCEPTED değildir** — kabul yalnız sizin
denemenizle verilir. NOT_TESTED / PARTIAL / NOT_DONE açıkça yazıldı.

Tüm testler gerçek oyuncu girdisiyle (tuşlar, fare yönü; durum yazmadan) gerçek ev haritasında (`L_GR_SphirusHouse`) veya düz test
haritasında yapıldı. Kayıtlar 30 Hz sabit adımda (video) ve ayrıca gerçek zamanlı 30/60 Hz'de alındı. Kullanıcı kayıt dosyası
(SFSaveSlot, SHA1 4823d83a…) her testte kenara alındı ve aynı dosya geri kondu; her batch sonunda SHA1 doğrulandı (değişmedi).

---

## 1. P0 — yedi şikâyet (önce/sonra)

| # | Şikâyet | Kök neden | Düzeltme | Durum |
|---|---|---|---|---|
| 1 | Koşu tuşu hızlandırılmış yürüyüş; jog/sprint yok | Shift yalnız Walk gaitinde bağlam hız ölçeğini 1.30'a çıkarıyordu → GASP Walk ailesinde kalıp klipleri hızlı oynatıyordu; jog gizli Ctrl kip anahtarına bağlıydı | Shift (basılı) = gerçek Jog (GASP Run 375 cm/s), Ctrl / pad LB (basılı) = Sprint (585, hız >250'den sonra). Oynatma hızı yükseltilmedi | IMPLEMENTED, TECH_TESTED, VISUALLY_INSPECTED |
| 2 | Zıplama/aşma sonrası gövde çapraz kalıyor | Relaxed iniş veritabanlarında çapraz iniş klipleri seçiliyordu | 6 sahipli iniş DB'si (yalnız ileri inişler, vendor kopyası); ABP SphCM eşlemesiyle | IMPLEMENTED, TECH_TESTED (zıplama). Aşma (vault) NOT_TESTED |
| 3 | Odun alırken baş kayboluyor | Eğilme kadrajında kamera pitch'i başı kadrajdan çıkarıyordu | AC_Sph_Camera baş kenar payı (4° / baş üstü 14 cm) | IMPLEMENTED, TECH_TESTED, VISUALLY_INSPECTED |
| 4 | Kütük kütüğe gömülü | GR_Day_BlockLog z yanlıştı | z 165.2 → alt yüzey 149.8 / kütük üstü 149.5 | IMPLEMENTED, VISUALLY_INSPECTED |
| 5 | Yarılmış odun şömineye konmuyor, E çalışmıyor | Parça aktörlerinin tick'i kapalıydı → otomatik alma hiç çalışmıyordu (Split 0 kalıyordu); şömine 2 parça istiyordu | Parça görünürken tick açık; otomatik alma 70 cm yatay; şömine Split ≥ 1 | IMPLEMENTED, TECH_TESTED (3 başarılı akış + ret), VISUALLY_INSPECTED |
| 6 | Çömelmede sırt fazla dik, kollar sarkık | Çömelme sırasında beden duruş katmanı yoktu | ABP_Sph_Body_GASP çömelme katmanı: sırt yuvarlanır, kollar öne ve bükülü, boyun/baş göz hattı | IMPLEMENTED, VISUALLY_INSPECTED |
| 7 | S basınca karakter kameraya dönüyor | S, oryantasyon-hareket kipinde karakteri 180° döndürüyordu | S = GR_Back: strafe kipi, gerçek geri klipleri (Walk_Loop_B / Stop_B / Crouch_B), hız ×0.85, dönüş hızı 150°/s, havada durum korunur; ABP yön seçicisi deneysel olmayan dalda da güncellenir | IMPLEMENTED, TECH_TESTED, VISUALLY_INSPECTED |

### 1.1 Koşu — test A (`data/kosu_olcumleri.txt`)
- Önce (`videos/once_kosu_tusu_hizli_yurume.mp4`): Shift 8 s → 209 cm/s, gait WALK, klip `Walk_Loop_F` (hızlandırılmış yürüyüş).
- Sonra, düz harita (`videos/sonra_kosu_jog15s_sprint10s.mp4`): Shift 15 s → ortalama 370 cm/s, gait RUN, `Run_Start` → `Run_Loop_F`
  (sürdürülebilir); Shift+Ctrl 10 s → 576 cm/s, gait SPRINT, `Transition_Run_to_Sprint` → `Sprint_Loop_F`; bırakınca
  `Sprint_to_Run` → `Run_to_Walk` → `Walk_Stop` (doğal iniş merdiveni).
- Gerçek harita patikası: jog çalışıyor; sprint bölümünde arazi eğimi nedeniyle tökezleme/yavaşlama görüldü — PARTIAL (ayrı arazi
  incelemesi gerekli).
- Açık bulgu: jog'da basan ayak 21–24 cm/s kayıyor (yürüyüşte 6–12). Görsel kabul sizde.

### 1.2 Koşu engeli ve geri dönüş — test B (`data/ev_ici_kosu_engeli.txt`, `data/yuk_maske_kosu_engeli.txt`)
- **Ev içi:** mutfak → arka kapı → avlu, Shift+W basılı (`videos/sonra_ev_ici_tempo_disari_jog.mp4`): içeride RunBlock=1, tempo
  yürüyüş; kapıdan çıkınca engel kalkıyor ve aynı tuşla jog başlıyor. TECH_TESTED.
- **İki el yükü (odun):** RunBlock=2; Shift = tempo yürüyüş 162 cm/s (WALK ailesi); Ctrl+Shift sprint vermiyor; S yükle geri
  yürüyüş 141 cm/s (`Walk_Loop_B`, yüz yönü korunuyor). Odun kütüğe konunca RunBlock hemen 0 ve Shift → GaitSel 1 (jog isteği);
  ancak test balta duruşunda (sol tık bekleyen kesme duruşu) kaldığı için yük bırakıldıktan sonraki **koşu hareketi gözlenmedi**
  → geri dönüş durum olarak TECH_TESTED, hareket olarak NOT_TESTED. (`videos/sonra_yukle_kosu_engeli_S_geri.mp4`)
- **Maske taşıma:** test maske tezgâhında (ev içinde) yapıldı: RunBlock=1 (ev içi baskın neden), CarryActive=1, Shift tempo 195,
  Ctrl+Shift sprint yok, S ve S+Shift geri yürüyüş. **Dışarıda maske taşıma (neden=3) ve maske bırakılınca geri dönüş NOT_TESTED.**
  Not: kod, maske taşımada (iki el yükü yoksa) sprint'i engeller ama nedeni 3 yalnız iki el yüküyle birlikte raporlar — dışarıda
  okunurluk eksik olabilir (PARTIAL). (`videos/sonra_maske_tasima_kosu_engeli.mp4`)

### 1.3 S geri yürüyüş — test C (`data/S_geri_yuruyus.txt`)
- Önce (`videos/once_S_kameraya_doner.mp4`): S → karakter 180° dönüp kameraya doğru yürüyordu.
- Sonra (düz harita, fare sabit, `videos/sonra_S_SA_SD_kosudan_S.mp4`): S 143 cm/s `Walk_Loop_B`; S+A / S+D 139 cm/s, geri-çapraz;
  jog → S: `Walk_Pivot_F_B` frenle geri; çömelik S: `Crouch_Start_B` 163 cm/s. Aktör yaw'ı değişmedi (kalıcı kilit yok: W ile
  bırakınca normal dönüş).
- Bahçede (`videos/sonra_S_bahce_geri_yuruyus.mp4`) S çalışıyor; S+A/S+D/Shift+S bitki örtüsüne takıldı.
- Açık bulgular (PARTIAL): düz S'de kalça ~20° (S+A'da ~35°) dönük görünüyor; geri ayak kayması 6–12 cm/s; çalı içinde geri
  yürürken kamera çarpışması omuza giriyor (`evidence/bulgu_S_cali_icinde_kamera_omuza_girer.png`).

### 1.4 Zıplama / aşma — test D (`data/ziplama_inis.txt`)
- Önce (`videos/once_ziplama_capraz_kalir.mp4`): inişten sonra omuz yönü harekete göre 12–35° çapraz kalıyordu.
- Sonra (`videos/sonra_ziplama_inis.mp4`): yürüyüş, dönüşlü yürüyüş, duran ve jog zıplamalarında iniş sonrası omuz ±5–7° içinde.
- **Aşma (GASP traversal):** test engelinde hiç tetiklenmedi → NOT_TESTED.

### 1.5 Çömelme — test E (`data/comelme.txt`, `evidence/sonra_comelme_yan_ve_arka.png`)
- Önce (`videos/once_comelme.mp4`): dik sırt, sarkık kollar. Sonra (`videos/sonra_comelme.mp4`): sırt yuvarlak, kollar önde ve
  bükülü, baş öne/aşağı değil ileri bakıyor. Çömelik yürüyüş, geri, yana, kalkış kaydedildi. VISUALLY_INSPECTED.
- Açık: çömelmeden kalkınca kalçada −34° yaw sapması bir kayıtta görüldü (PARTIAL); **alçak tavan altında kalkma NOT_TESTED.**

### 1.6 Odun → kesme → şömine — testler F, G, H (`data/odun_somine_akisi_hub.txt`)
- Odun alma: baş kadrajda (`evidence/sonra_odun_alma_kutuk_balta_parcalar.jpg`). Kütük kütüğün üstünde. Balta → 2 yarılmış parça
  iki yana düşer.
- Parçalar otomatik toplanıyor (Split 0 → 1 → 2).
- Şömine: E = odun koy (Fire 1), E = yak (Fire 2). Gerçek girdiyle **3 başarılı akış**: tam akış 1 ve 2
  (`videos/sonra_odun_balta_somine_1.mp4`, `_2.mp4`), test kaydından yükleme (oyunun kendi `LoadGame` çağrısı; Split 2 yüklendi
  → koy → yak, `videos/sonra_kayittan_yukle_somine.mp4`). Odunsuz şöminede E reddediliyor, durum değişmiyor
  (`videos/sonra_odunsuz_somine_ret.mp4`).
- Üçüncü tam akış (flow3) **başarısız**: otomatik test rotası odun yığınına takıldı (oyun hatası değil, test rotası).
- Not: PIE başlangıcı kaydı yüklemiyor; oyunda yükleme `SFSaveManager.LoadGame` ile (menü/devam yolu).
- **Taşıma iptali NOT_TESTED.**
- Açık görsel bulgular (`evidence/sonra_somine_odun_koy_yak.jpg`): taşınan odun demeti şömine rafının içinden geçiyor; diz
  çökme sırasında kaldırılan kol taş duvara giriyor; yanan ateşte "Odun koy / Yak" istemi hâlâ görünüyor; ateş yanınca
  şömine önü beyaza patlıyor (REVIEW_REQUIRED). Temas bütünlüğü: PARTIAL.

### 1.7 Kare hızı — 30 / 60 Hz gerçek zaman (`data/gercek_zaman_30_60hz.txt`)
- Ekran görüntüsü ve zaman genişletmesi olmadan, t.MaxFPS 30 ve 60 (düz harita): gerçek kare süresi p50 33.3 / 16.7 ms, p95 33.9 /
  17.5 ms; oyun dt = gerçek dt. İki hızda aynı zincir: Run_Start → Run_Loop (358–364 cm/s) → Run_to_Sprint → Sprint (552–567)
  → Sprint_to_Run → Run_to_Walk → Stop → S geri yürüyüş (135–141). TECH_TESTED.
- Sınır: kaydedici plan adımlarını 30 Hz kare sayısıyla saydığı için 60 Hz'de her adım gerçek sürede yarı uzunlukta oynadı
  (60 Hz'de sprint klibi geçişte kaldı, döngüye az girdi).

### 1.8 Regresyon — test I
- Bu turda maske bağlama/alma/taşıma (yukarıda), şömine, kayıt/yükleme (oyun içi yükleme), ev içi kapı geçişi ölçüldü.
- **Kapı tutamağı, çay, yatak, yakın kamera, efor regresyonu bu turda yeniden kaydedilmedi → NOT_TESTED** (önceki rapor
  `sphirus-kamera-kalanlar-2026-11-13` durumu geçerli).

---

## 2. Ana görev kalanları

| Başlık | Bu turdaki durum |
|---|---|
| Ağırlık taşıyan hareket, beden dili, tempo yürüyüşün hızlandırılmış klip olmaması | Tempo artık yalnız ev içi/yükte (WALK ailesi, ölçek ≤1.3); dışarıda Shift gerçek jog. Ağırlık/efor katmanları önceki turdan. VISUALLY_INSPECTED (kısmi), USER_ACCEPTED değil |
| Zıplama ve iniş | İleri iniş DB'leri (yukarıda) — TECH_TESTED |
| Kamera kimliği, olaya bağlı tepkiler, DOF pompalamasız | Bu turda yeni iş yok (önceki turun AC_Sph_Camera durumu). NOT_DONE (bu tur) |
| Kapı gerçek kavrama | Önceki tur: prosedürel uzanma, el 17–27 cm kısa. Gerçek kavrama animasyonu NOT_DONE |
| Çay dökme/içme ayrı kadraj | NOT_DONE |
| Temas bütünlüğü (maske, odun, şömine, dolap, yatak) | Odun/şömine incelendi: PARTIAL (yukarıdaki bulgular). Dolap/yatak NOT_TESTED |
| Dar alan ve merdiven | NOT_TESTED (bu tur) |
| Yaprağın lense değdiği an solma | Önceki turda NearFade materyalleri (patika); bu tur yeni test yok |
| Efekt denetimi (CA, grain, vignette, bloom, DOF, motion blur, rezonans, ses) | NOT_DONE. Görülen: yanan şöminede bloom/patlama aşırı (REVIEW_REQUIRED) |
| Atmosfer adayı | IMPLEMENTED (KAPALI, geri alınabilir), A/B ve istatistik — bkz. bölüm 3. USER_ACCEPTED değil, yükseltilmedi |
| Konfor paneli gerçek fare/gamepad | Panel önceki turda (F10 / pad View); gerçek cihazla deneme yapılamaz (otomasyon girdisi) → NOT_TESTED |
| Gerçek performans | Bölüm 4 |
| 21:9 | NOT_TESTED (editör görünümü sabit) |
| Tek sürekli rota | Odun → kesme → arka kapı → mutfak → şömine akışı tek sürekli kayıt (81 s) olarak var; ev + bahçe + göl tam rota NOT_DONE |

---

## 3. Atmosfer adayı C1 — "serin nemli orman + yaşanmış sıcak ev + maske tekinsizliği"

Onaylı üretim görünümü (XR5 FINAL v2, 2026-11-01 onayınız) korunarak üstüne **uygulanmış, geri alınabilir** bir aday kuruldu.
Haritada `EX_Atmo_C1` klasöründe **KAPALI** olarak kayıtlı; oyunun mevcut görünümünü değiştirmez. Yükseltilmedi.

**İçerik (`Tools/Motion_20261112/atmo_c1.py`):**
1. Yükseklik sisi 2. katmanı (üretimde kullanılmıyordu): yoğunluk 0.035, düşüş 0.9, yerden −80 cm — çukurlarda yere yatan
   nem; sis duvarı değil.
2. 4 LocalFogVolume (`EX_Atmo_C1_Mist_EdgeE/EdgeS/EdgeW/Pond`): orman kenarları ve gölde yere yakın nem; yalnız yükseklik
   sönümü (XR5 v1'deki "ışıklı duvar → otomatik pozlama bozulması" tuzağından kaçınmak için radyal sönüm 0).
3. `EX_Atmo_C1_PPV` (sınırsız, öncelik 1.5 — ev/raf/açıklık bölge PPV'lerinin (2.0) **altında**, böylece sıcak ev kendi beyaz
   dengesini korur): kontrast 0.97, gölge kazancı (0.97, 0.99, 1.03), parlak alan doygunluğu 0.92.
4. Maske tekinsizliği: mevcut hikâye tetikli `EX_Look_Resonance` olduğu gibi bırakıldı (aday ona dokunmaz).

**A/B (`evidence/atmosfer_C1_sol_KAPALI_sag_ACIK_1.jpg`, `_2.jpg`; 24 oyuncu kamerası noktası; `data/atmosfer_C1_pozlama_istatistik.json`):**

| Ölçü (24 görüntü ort.) | KAPALI (üretim) | AÇIK (aday) |
|---|---|---|
| Ortalama parlaklık (0–255) | 79.4 | 78.6 |
| Beyaz kırpılma ≥245 | %0.26 | %0.07 |
| Siyah kırpılma ≤10 | %0.43 | %0.20 |
| Doygunluk | 0.291 | 0.262 |
| Ortalama R / G / B | 82.2 / 79.8 / 67.4 | 81.1 / 78.8 / 69.1 |

- Okuma: hafif nem pusu, daha yumuşak kontrast, gölgelerde serinlik, daha az kırpılma; sıcak ev (veranda/ev arkası) sıcaklığını
  koruyor; tek görüntüde parlaklık değişimi en fazla ±2.5 — sis duvarı ya da pozlama bozulması yok. Turuncu/turkuaz ayrımı yok.
- Fark **ince**; kenar sisi bu 24 noktadan az görünüyor. "Masalsı" kimlik için yeterli mi — karar sizin.
- Maliyet: bölüm 4 — ölçüm gürültüsü içinde (~1 ms).
- Süreç notu: ilk kurulumda zemin izi ağaç tepelerine çarptı (iki sis hacmi z 1767/2162'de kaldı); düzeltme işi ilk iki denemede
  haritayı kaydetmedi (Python konum değişikliği seviyeyi kirli işaretlemiyordu). Üçüncü denemede kaydedildi (harita SHA1
  bfa26d5… → 9a948f1…), A/B bu son durumla yeniden alındı.
- **Aç / kapat / kaldır:** `ATMO_MODE='on'|'off'` (yalnız editör belleği, kayıt yok), `'remove'` (kapılı yazma: aktörleri siler,
  sis 2. katmanını yedekten geri yazar), ya da `map_backup_atmo` haritasını geri koymak.
- Durum: IMPLEMENTED (KAPALI), VISUALLY_INSPECTED, PERFORMANCE_TESTED. **USER_ACCEPTED değil; yükseltme yalnız onayınızla.**
  Üretim görünümü değişmediği için `chatgpt-bridge/latest/LATEST.json` güncellenmedi.

---

## 4. Performans

Donanım: Intel i7-13650HX, 32 GB RAM, RTX 4060 Laptop 8 GB (sürücü 616.56). Ölçüm editör içinde PIE (editör arayüzü dahil,
PIE 60 Hz tick sınırı), ekran görüntüsü / zaman genişletmesi yok, motor CSV profilleyici + GPU geçiş istatistikleri
(`data/performans_atmosfer_AB.txt`). Rota: patika, yürü 4 s → jog 6 s → sprint 4 s → dur 3 s. Her ölçüm öncesi editör yeniden açıldı.

| Ölçüm (sıra) | Kare p50 / p95 / p99 ms | GPU p50 / p95 | Oyun iş parçacığı p50 | ort. fps | >50 ms kare |
|---|---|---|---|---|---|
| 1. tur A — aday KAPALI | 21.4 / 35.1 / 50.5 | 18.9 / 33.0 | 20.5 | 41.2 | 10 / 908 |
| 1. tur B — aday AÇIK | 45.0 / 55.6 / 76.6 | 43.9 / 51.6 | 19.4 | 22.3 | 100 / 501 |
| 2. tur B2 — aday AÇIK (önce) | 39.2 / 93.8 / 115.0 | 36.8 / 92.0 | 21.0 | 20.6 | 118 / 479 |
| 2. tur A2 — aday KAPALI (sonra) | 41.1 / 97.9 / 118.9 | 38.1 / 93.9 | 21.9 | 19.9 | 116 / 426 |

- **Atmosfer adayının maliyeti ölçüm gürültüsü içinde:** ters sırada aday açık/kapalı farkı ~1 ms (B2 36.8 vs A2 38.1 GPU).
  İlk turdaki 19 → 44 ms farkı adaydan değil: aynı kapalı durum ikinci turda 38 ms ölçüldü. **Ölçümler arası sapma büyük**
  (aynı durumda GPU p50 19–38 ms) — sanal gölge haritası önbelleği / akış durumu; güvenilir sayı için paketlenmiş Standalone ve
  çoklu tekrar gerekli (NOT_DONE).
- **Sistem başına maliyet (ortalama ms):** GPU: ShadowDepths 24.5–25.7 (bitki örtüsü sanal gölgeleri — en büyük kalem; önceki
  donanım raporuyla tutarlı), NaniteVisBuffer 2.3–3.5, saç (HairStrands) 1.8–7.2, ShadowProjection 2.1–2.4, DOF 0–2.3,
  PostProcessing 1.7, TSR 1.6, VolumetricFog 0.7. Oyun iş parçacığı: editör UI 6.3–7.7, TickActors 1.2–1.3, Animasyon 1.0–1.1,
  TimerManager 0.8–1.5, CharacterMovement 0.3–0.45. Bu turdaki oynanış değişikliklerinin (gait, geri yürüyüş, çömelme katmanı,
  parça tick 0.1 s) oyun iş parçacığı maliyeti ölçülebilir değil.
- Durum: PERFORMANCE_TESTED (editör PIE). Hedef 30 fps bu rotada **karşılanmıyor** (p50 37–44 ms GPU, 2. tur); asıl kalem
  bitki gölgeleri — ayrı optimizasyon işi.

---

## 5. Değişiklik manifestosu ve geri alma
`changes/changes.md`. Toplu geri alma noktası `C:\Users\berat\SphirusCheckpoints\P0_Pre_20261113_1426`; her yazma işi için
SHA1'li yedek manifesti; harita yedekleri `map_backup_p0w1`, `map_backup_atmo`, `map_backup_atmo_fix`.

## 6. Kapanış
- Temiz yeniden açılış denetimi (`data/temiz_acilis_denetimi.txt`, 2026-11-14): değişen 8 Blueprint (BP_HybridA_Player,
  ABP_Sph_GASP, ABP_Sph_Body_GASP, AC_Sph_Camera, BP_Sph_GASPCharacter, BP_GR_DayStation, BP_GR_DayHub, BP_GR_SplitPiece)
  BS_UP_TO_DATE, hata yok; giriş eşlemeleri (Shift = Gait, Ctrl / LB = Sprint); 6 sahipli iniş DB'si; kütük z 165.2; atmosfer
  adayı KAPALI (sis gizli, PPV karışımı 0, sis 2. katmanı yoğunluk 0); kirli paket yok. Günlükteki 17 "LogAutomationTest:
  Condition failed" satırı bu işten önceki (2026-11-12) açılışlarda da aynı sayıda — motor/eklenti başlangıcı.
- Editör temiz açık bırakıldı, kilit serbest. Kullanıcı kaydı (SFSaveSlot SHA1 4823d83a…) değişmedi.
- Vendor kaynaklarına, ana karakter kafa/beden/saç/giysi çalışmasına, ev sahnesine dokunulmadı; reddedilen Core Motion C profili
  açılmadı; ExecutionPolicy ve Smart App Control değiştirilmedi (pozlama istatistikleri Blender Python'a taşındı).
- **Sizden beklenen:** oyunda deneme (Shift jog / Ctrl sprint / S geri / çömelme / odun → şömine) ve atmosfer adayı için karar
  (aç ve yükselt / ayarla / kaldır). Hiçbir başlık sizin kabulünüz olmadan "tamamlandı" sayılmadı.
