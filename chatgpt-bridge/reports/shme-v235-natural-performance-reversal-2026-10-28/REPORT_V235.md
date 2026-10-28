# SPHIRUS — SHME V2.35: donmadan yön değiştirme, duruş ve kamera (2026-10-28)

Taban: V2.34 üretimi (Bridge d71d03d). Blueprint-only UE 5.8, git yok; geri dönüş manifest yedekleriyle (sha1 doğrulamalı).
Sayılar sabit adımlı editörde, aynı girdiyle ölçüldü. Aksi yazılmadıkça 30 FPS kullanıldı.

**Ölçütler:**
- `contact231` en kötü basılı-top kayması / sürüklenmesi (cm).
- **"Bekleme" (s):** girdi basılıyken ters dönüş klibinde iki ayağın topu da 60 cm/s'den yavaş kalan en uzun süre. Kullanıcının tarif ettiği "donma" budur.

Teknik PASS, görsel ve oyun hissi kabulü değildir; ikisini ayrı yazıyorum. Görsel yargılarım zaman damgalı kare şeritlerinden (`sheets/fin_*`). Gerçek zamanlı videoyu oynatıp izleyemedim; kareleri inceledim. PS donanımında test yapılmadı.

**Üretime alınanlar (temiz açılışta VERIFY235 ALL_OK, 16:39):**

| Grup | İçerik |
|---|---|
| `rev` | ABP'nin 4 ters dönüş DB değişkeni → yeni `PSD_SHM235_JogRevFwd` / `PSD_SHM235_JogRevBwdX`, 64 yeni klip `SHM235_JogRev_*` |
| `route` | `RevOverHard`: ters istek, sert dönüş bölümünün asgari tutma süresini bekletmeden devralır |
| `gap` | `RevGapKeep`: bırak–yeniden bas boşluğu ters dönüş bölümünü bitirmez |
| `mouse` | Fare yürüyüş takibi ölçeği 0.35 → 0.7 |

**Reddedilen:** ileri jog duruşunun yerinde yeniden planı (`gen235_stop` r1–r6). V2.34 duruş klibi yedekten geri yüklendi, sha1 doğrulandı.

## 0. Kısa yanıtlar (12 soru)

1. **Donmanın gerçek sahibi.** İçerik (sınıf E + B). Saat tutulması (A) değil.
   - Üretim zinciri (`j35_rev`, `j30_rel_3200`): `SHM226_JogRev_F_B_P14` klip hızı 1.0'da oynuyor, iki ayak 0.64 s yerde, kollar jog duruşunda kalıyor.
   - V2.25/2.26 üreteci yeni yöndeki ilk adımı sıfır geçişinden 0.40 s sonraya koymuş (`T_FIRST`).
   - Kapsül tablosu sıfır civarında ~0.3 s boyunca 40 cm/s'nin altında oyalanıyor; ayak 0.6 s havada süzülüyor.
   - İki ek sahip:
     - **60 FPS (C, öncelik):** `RouteMinHold`, aile 2 → 3 geçişini bekletiyor. `RevOverHard` ile 37.1 → 7.7 cm.
     - **Bırak–yeniden bas:** boşlukta bölüm bitiyor. Girdi yokken yön vektörü 0, bu "yeni niyet" sayılıyor. Arama, zaten dönen klipten çıkıp tam hızlı bir bölmenin 0. karesine giriyordu. `RevGapKeep` ile 39–46 → 10.9 cm.
   - Karşı örnek (sağlam): düşük hızlı `SlowRev B_F` adımlaması kesintisiz.
2. **Beden şimdi ne yapıyor?** Fren ayağı basar, sıfır geçişinde yakalama adımı atılır, ardından ölçülü geri itiş gelir.
   - Bekleme 0.4–0.6 s'den 0.0–0.2 s'ye indi. Bu her FPS'te ve gerçek zamanda geçerli (bölüm 2 tablosu).
   - Kare şeridi (`fin_rev_pre235S` / `fin_rev_oS`):
     - Eski içerik 5.3–5.7 s arasında aynı adım açıklığında duruyor.
     - V2.35'te 5.3 s'de destek değişiyor, 5.7 s'de geri adımlar başlamış.
   - Kendi eleştirim:
     - Kollar fren boyunca jog taşımasını koruyor; frene bir kol/gövde tepkisi yok.
     - Gövde ileri bakarak geri koşuyor. S girdisinin bu kontrol düzeninde geri yürüyüş anlamına gelmesi bilinçli, ama "ağırlık aktarımı" yalnız bacaklarda okunuyor.
3. **Normal / sert / ters duruş ayrımı.**
   - **Ters istek:** yeni V2.35 ters dönüş DB'leri.
   - **Sert fren + bırakma (`j35_relstop`):** ters dönüşün yakalama adımında bitiyor. Üretimdeki 38 cm'lik açık, donuk duruş yerine 9.7 cm'lik toplu bir duruş kalıyor.
   - **Normal ileri duruş:** V2.34 CP2 duruşu, değişmedi.
   - Ayrım, istek türünün yönlendirilmesiyle yapılıyor. Yeni bir duruş ailesi **yok**.
4. **Hangi kadın-performans kaynakları üretildi?**
   - Dış video referansı incelemedim; incelenmiş gibi göstermiyorum.
   - Üslup çapası, projenin kendi kadın Core Motion döngüleri (`af_Loco_*` → `A_CT_Jog_Fwd` / `A_RB_Jog_Rear`). Ölçülen değerler: gövde eğimi ~8–10°, el yolu ±30 cm, pelvis salınımı 86–95 cm.
   - 64 yeni ters dönüş klibi bu döngülerden üretildi (aynı kol taşıması, aynı kadans). Abartılı kalça salınımı eklenmedi.
   - Üretime yeni duruş veya başlangıç kaynağı girmedi.
5. **Üç davranış:**
   - **A, sert frenden sonra yerleşme adımı:** KISMEN. Yakalama adımı `j35_relstop`'ta toplu duruşu sağlıyor; ayrı bir yerleşme klibi yok.
   - **B, yarım kalmış itişten destek yeniden düzeni:** KISMEN, içerikte var. Yere değmekte olan ayak hemen yeniden yönlendiriliyor; basılı ayak doğal parmak kalkışında ayrılıyor.
   - **C, birikmiş eforla ölçülü yeniden itiş:** HAYIR (efor bağımlı değil). İtiş 550 / 650 cm/s² sabit tasarlandı. Yüklü aile (LoadRev) yeniden üretilmedi.
6. **Ani duruş / kalkış çekişi düzeldi mi?** HAYIR.
   - Duruşta yeniden plan reddedildi (bölüm 3). Kare şeridi `fin_stop_oS` hâlâ şunları gösteriyor:
     - 10.5–10.8 s'de diz yüksekliğinde "yürüyüş adımı";
     - 10.9–11.2 s'de çömelik açık duruş;
     - 11.6 s'de dikleşme.
   - `jstart` çekişi açık: `TurnR045` dönüşlü başlangıç 50–79 cm.
7. **V2.34 gerilemeleri.**
   - Kapandı:
     - `j30_rel_3200`: 60 FPS'te 40.7 → 11.5, gerçek zamanda 15.2 → 10.0.
     - Sert frenden sonra uzun donuk duruş.
     - `wdiag`: 20.5 → 12.1.
   - Açık:
     - `jstart` (79 / 51 cm). Aynı başlangıç klibinde ve ters dönüş yolundan önce oluyor; 60/120/20'de üretimle aynı. V2.35'e bağlanamıyor ama çözülmedi.
     - Jog-sol başlangıcı 50 cm.
   - **V2.35'in getirdiği yeni gerilemeler:**
     - `j30_rel_3450`: 8.6 → 16.3 (ikinci ters dönüş, `B_F_P27`).
     - `c29_combo`: 9.9 → 15.4 (sonraki yürüyüş sol).
     - `jback`: 9.3 → 14.4 (geri yürüyüş duruşu).
     - `j35_rev` 30 FPS: 9.2 → 13.2. Yakalama ayağı klip noktasının 12 cm dışına iniyor: MM giriş karışımı. 60/120/real'de eskiden iyi.
8. **Kamera hâlâ alt beden seçimini değiştiriyor mu?** Hayır, kanıtlanmadı.
   - Aynı beden, kamera açık/kapalı, ikişer tekrar: 4 koşunun 3'ünde klip ve zaman birebir aynı.
   - Farklı çıkan koşu bir kamera-**kapalı** tekrarıydı; kapalı1 ile kapalı2 de birbirinden farklı.
   - Kapsül yolu fark 0.0. Kamera başı yalnız 1–11 cm oynatıyor (aim offset).
   - Son oturumda farklı kamera ölçeği, aynı beden (`camab234`): bütün çiftlerde hız / yön / yaw / yol farkı 0.0.
   - `PoseSearchHistoryCollector` hipotezi böylece desteklenmedi.
9. **Fare / gamepad takibi ve gerçek 180°.**

   | Profil | Yerleşme | En yüksek hız | Son hata |
   |---|---|---|---|
   | Fare V2.35 | 2.37 s | 32°/s | 12.4° |
   | Fare V2.34 | yerleşmiyor | 16.5°/s | 28.4° |
   | Gamepad | 1.6 s | 46°/s | — |

   - Depar sağ dönüş: 4.33 s'den 2.17 s'ye.
   - Geri yürüyüşte kamera dönmüyor (kontrol değişimi 0.0); tasarım gereği.
   - Gerçek 180°: test senaryolarında **NOT_TRIGGERED**. Bedenin gerçekten döndüğü bir 180° zinciri oluşmadı (S girdisi geri koşu).
10. **Arazi:** Uygulama **yok**. Yalnız V2.34 teşhisi duruyor. `ter_*` değerleri değişmedi (6.5 / 6.5 / 16.8).
11. **Üretimde / reddedilen:**
    - Üretimde: `rev`, `route`, `gap`, `mouse`.
    - Reddedilen: duruş yeniden planı r1–r6, `rvSW` / `rvOW` / `rvFP` (warping/FootPlacement değişiklikleri hiçbir şey değiştirmedi).
    - Tasarlanmış kayma uygulanmadı.
12. **Süreler:**
    - Editör test süresi 13:38–18:46, yaklaşık 5 sa 8 dk.
    - 23 yeniden açılış, 308 PIE koşusu.
    - Yeniden açılış (kapatma + açılış + ısınma) yaklaşık 3–5 dk.
    - Son doğrulama: temiz açılış `finv` 16:38 → VERIFY235 ALL_OK 16:39.

## 1. Durum, koruma

- Kilit sahibi `v235`. Her yazma işi bir manifest ve yedekle yapıldı: `revdbs`, `stop1`..`stop6`, `PROMO235`.
- Yerinde içerik üretiminin her yinelemesinden önce yedek, editör kapalıyken geri yüklendi (sha1 kontrolü).
- DB oluşturduktan veya özellik değiştirdikten sonraki ilk koşu "DB None" okuyor (vendor pivot 63 cm). Bu ilk koşular yargıya katılmadı; ısınma koşusu kullanıldı.
- Anatomi, yüz, kıyafet ve harita değiştirilmedi. Ücretli ham animasyon ve yedek yayımlanmadı (`pub235.sh` ikili dosya denetimi).

## 2. Ters dönüş (paket A)

| Adım | Ayrıntı |
|---|---|
| İstenen | Ters istekte donmadan fren → destek değişimi → yeniden itiş |
| Neden | Bkz. 0.1 (içerik) |
| Uygulama | `gen235_rev.py`, aşağıda |
| Kuru doğrulama | Ayak hatası ≤ 6.1 cm, basılı kayma 64 klibin hepsinde < 3 cm |
| Üretim | Evet (`rev`) |

`gen235_rev.py` (`gen226` üzerine yamalı) şunları yapıyor:
- **Tasarlanmış kapsül:** fren 800 cm/s², itiş sıfırdan geçerek 550 (F_B) / 650 (B_F) cm/s², oyalanma yok.
- **Yakalama adımı:** S sıfır geçişinde (tS 0.28–0.57 s).
- Basılı S, parmak kalkışında ayrılıyor; yere değmekte olan S hemen yönleniyor.
- 64 klip, iki DB'de, `continuing_pose_cost_bias -0.5`.

Son tablo, en kötü kayma cm (bekleme s); `o` = V2.35 üretimi, `pre235` = V2.34 düğmeleri:

| Senaryo | 30 | 60 | 120 | 20 | Gerçek zaman |
|---|---|---|---|---|---|
| `j35_rev` | 13.2 / 9.2 (0.1 / 0.5) | 8.5 / 17.5 (0.1 / 0.5) | 14.1 / 23.7 (0.0 / 0.4) | – / 6.0 (– / 0.5)* | 7.2 / 8.5 (0.2 / 0.5) |
| `j35_rev2` | 9.3 / 11.9 (0.1 / 0.5) | 7.2 / 7.2 (0.1 / 0.5) | 14.9 / 5.4 (0.0 / 0.5) | 8.4 / 25.2 (0.1 / 0.5) | 8.4 / 8.1 (0.1 / 0.5) |
| `j30_rel_3200` | 9.0 / 13.5 (0.0 / 0.6) | 11.5 / 40.7 (0.0 / 0.3) | 24.9 / 25.6 (0.0 / 0.5) | 6.7 / 10.5 (0.1 / 0.4) | 10.0 / 15.2 (0.1 / 0.5) |
| `j30_slow` | 6.4 / 12.3 (0.1 / 0.5) | 7.1 / 15.4 (0.1 / 0.4) | 6.8 / 15.9 (0.1 / 0.2) | 7.6 / 16.3 (0.1 / 0.5) | 7.7 / 10.5 (0.2 / 0.4) |
| `j34_chain1` | 9.3 / 16.2 (0.1 / 0.4) | 16.3 / 9.7 (0.1 / 0.5) | 23.3 / 20.2 (0.1 / 0.3) | 6.8 / 7.6 (0.1 / 0.4) | 21.8 / 19.0 (0.1 / 0.5) |
| `c29_combo` | 15.4 / 9.9 | 11.8 / 11.3 | 12.9 / 14.5 | 8.9 / 11.4 | 7.3 / 12.8 |
| `e29_chain` | 6.5 / 11.1 | 19.8 / 19.8 | 18.9 / 17.6 | 6.0 / 9.0 | 25.7 / 11.8 |
| `s29_swl12` | 11.1 / 11.1 | 20.8 / 20.8 | 14.9 / 14.9 | 8.5 / 6.0 | 9.2 / 10.2 |

\* Yeniden açılıştan sonraki ilk 20 FPS koşusunun LTP dosyası yazılmadı (zincir ısınmadan sonra bu etiketi kaydetmedi). Eksik olarak bırakıldı, tahmin edilmedi.

**Okuma:**
- Bekleme her FPS'te ve gerçek zamanda 0.0–0.2 s.
- Kayma çoğu modda eşit veya daha iyi.
- Daha kötü olanlar:
  - `j35_rev` 30 FPS ve 120 FPS (yakalama ayağı girişi);
  - `j35_rev2` 120 FPS;
  - `e29_chain` gerçek zaman (`BackLink_4`, eski içerik; yol değişince oraya giriliyor).
- Kalan engel: MM giriş karışımı yakalama ayağını 12 cm kaydırıyor. Warping ve FootPlacement değişiklikleri bunu çözmedi.

## 3. Duruş (paket B), reddedildi

- **Sahip:** `SHM_A_CP2_Jog_Fwd_Stop`. Kapsül 357 cm/s'de sabit, sonra 800 cm/s² ile duruyor.
  - Fren adımı son kökün 55–63 cm önüne iniyor; tepe 26.9 cm ("yürüyüş adımı").
  - Kapanış adımı 41 cm açıklık bırakıyor; ardından ön ayak 43 cm geri çekiliyor (düzeltme adımı).
  - Gövde girişte 0.15 s'de dikleşiyor.
- **r1–r6 sonuçları:**
  - Yürüyüş adımı ve düzeltme adımı gitti.
  - Ama düzeltme adımı, faz dışı duruş girişlerinin **kapanış adımıymış**. Kaldırılınca duruşların yarısında 36 cm sürüklenme oluştu.
  - r5'in 4.6 cm kısa duruşu, sonraki başlangıcı dönüşlü başlangıca çevirdi (88–96 cm).
- **Karar:** V2.34 klibi geri yüklendi. Doğru yol, V2.8 yürüyüş duruşlarındaki gibi iki fazlı (L/R) bir jog duruş ailesi. Bu sürümde yapılmadı.

## 4. Yönlendirme ve boşluk (paket C)

- `RevOverHard`: aile 2'de ters aday, aile 3'e hemen geçebiliyor. 60 FPS `j30_rel_3200`: 37.1 → 7.7 cm (B8 seti), son tabloda 11.5.
- `RevGapKeep` v1 yalnız `rdLost`'u maskeliyordu; etkisizdi, çünkü girdi yokken `rdNewIntent` tetikleniyordu.
- v2 ikisini de aile 3 içinde `RevGraceTime` süresince maskeliyor. 30 FPS'te 39–46 → 10.9 cm.
- `j35_relstop` (S 0.25 s basılıp tamamen bırakılıyor): bölüm koşmaya devam etmiyor, 9.7 cm toplu duruşta bitiyor.

## 5. Kamera

- **Kamera açık/kapalı ayrımı:** madde 8.
  - Kapalı varyant takibi gerçekten kapatıyor (`CamRecEnabled` false).
  - `body235` varyantı yalnız fare ölçeği farklı; ona "kapalı" demiyorum.
- **Fare yürüyüş takibi 0.7 (`rec233`):**
  - Yerleşme 2.37 s, ivme p95 33°/s².
  - Takip sırasında yol sapması 8.3°; 0.35 ile aynı, yani giriş çerçevesi bozulmuyor.
- **Gamepad akışı (`cam34_wflow`):** sürekli analog dönüş senaryosu. Yerleşme metriği burada anlamlı değil, kapalıyla eşit.
- **Gerçek 180° / geri yürüyüş:** madde 9. 180° tarafının seçimi V2.34'teki gibi; tetiklenmedi.

## 6. Arazi

Uygulama yok (madde 10). Bir basamak inme/çıkma için yazılmış bir çözüm üretime girmedi. Açık iş.

## 7. Skill güncellemeleri (yeni skill yok)

- `sphirus-natural-motion`:
  - "Kullanıcı incelemesinden kurallar (V2.35)": donma sınıfları A–E, yumuşak duruş ≠ düşük fren katsayısı, kadın tavrı ≠ kalça salınımı, tasarlanmış kayma ≠ gizli sürüklenme, top üzerinde plan;
  - 3 başarısız örnek.
- `sphirus-camera-direction`: 3 başarısız örnek (kamera seçimi suçlaması, fare 0.35, `body234` kapalı test sayılmaz).
- `sphirus-safe-unreal-iteration`: yinelemeden önce yedeği geri yükle; DB sonrası ilk koşu "DB None".
- `sync_claude_skills.py`, 0 hata.

## 8. Teslim tablosu

| Hedef | Durum |
|---|---|
| Ters istekte donma | TEKNİK PASS (bekleme 0.4–0.6 → 0.0–0.2 s, tüm FPS + real); görsel kabul sizde |
| Bırak–yeniden bas (`j30_rel_3200`) 60 FPS / real | PASS (40.7 → 11.5 / 15.2 → 10.0) |
| Sert fren sonrası uzun donuk duruş | PASS (`j35_relstop` 9.7 cm toplu) |
| Yerleşme / destek yeniden düzeni / efor itişi | PARTIAL / PARTIAL / FAIL |
| Doğal tam duruş | FAIL (yeniden plan reddedildi) |
| `jstart` / jog-sol | FAIL (açık) |
| Mouse depar kesiş: kamera sahibi mi? | PASS (kamera değil) |
| `wdiag` | PASS (20.5 → 12.1) |
| Yeni gerilemeler `rel_3450` / `c29` / `jback` / `j35_rev` 30 | FAIL (açık) |
| Fare yürüyüş takibi | PASS (2.37 s) |
| Gerçek 180° | NOT_TRIGGERED |
| Arazi | NOT_DONE |
| Tasarlanmış kayma | NOT_DONE |
| PS donanımı | NOT_TESTED |

## Kayıtlar (`vid/`)

30 FPS sabit adım, oyun zamanı = gerçek hız, kesilmemiş tam kareler; ağır çekim yok. Her kayıt `.gif` ve `_realtime.avi` olarak var.

| Kayıt | İçerik |
|---|---|
| `reversal_chain_before_side` / `reversal_chain_v235_side` / `_diag` / `_game` | Ana zincir, önce/sonra |
| `reversal_chain2_v235_side` | Ayna zincir (diğer destek) |
| `release_repress_before_side` / `release_repress_v235_side` | Bırak–yeniden bas |
| `back_start_forward_stop_v235_side` | Geri kalkış, ileri, duruş |
| `chain1_restart_v235_side` | Duruştan kısa yeniden hareket |
| `walk_right_mouse_before_game` / `walk_right_mouse_v235_game` | Fare takibi |
| `walk_flow_gamepad_v235_game` | Gamepad akışı |

Kare şeritleri `sheets/`: `fin_rev_*`, `fin_rel_*`, `fin_stop_oS`, `a1_*`, `b6_relstop`.
